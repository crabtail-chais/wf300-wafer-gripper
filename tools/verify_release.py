# SPDX-License-Identifier: MIT
"""Read-only release integrity checks. Never execute CAD data or certify hardware."""
from __future__ import annotations

import base64
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INDEXES = {'release-manifest.json', 'SHA256SUMS.txt'}
IGNORED_DIRS = {'.git', '__pycache__', '.venv'}
PATTERNS = {
    'local-user-path': re.compile(rb'/(?:Users|home)/[^/\s]+/|/private/(?:var|tmp)/', re.I),
    'github-token': re.compile(rb'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}'),
    'private-key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'aws-key-id': re.compile(rb'AKIA[A-Z0-9]{16}'),
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def safe_path(root: Path, relative: str) -> Path:
    p = PurePosixPath(relative)
    if not relative or p.is_absolute() or '..' in p.parts or '\\' in relative:
        raise ValueError('unsafe release path')
    target = root.joinpath(*p.parts)
    if any(q.is_symlink() for q in [target, *target.parents] if q != root.parent):
        raise ValueError('symlink in release path')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes release root')
    return target

def suspicious(data: bytes) -> list[str]:
    return [name for name, regex in PATTERNS.items() if regex.search(data)]

def check_fcstd(path: Path) -> None:
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError('FCStd CRC mismatch')
        if sum(i.file_size for i in z.infolist()) > 256_000_000:
            raise ValueError('FCStd uncompressed size exceeds review limit')
        if len(z.namelist()) != len(set(z.namelist())):
            raise ValueError('duplicate FCStd member')
        for name in z.namelist():
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts:
                raise ValueError('unsafe FCStd member name')
            data=z.read(name)
            if suspicious(data):
                raise ValueError('sensitive pattern in FCStd member')
            if name.endswith('.xml'):
                if b'<!DOCTYPE' in data or b'<!ENTITY' in data:
                    raise ValueError('unexpected XML entity declaration')
                tree=ET.fromstring(data)
                for py in tree.iter('Python'):
                    if py.get('encoded')=='yes' and py.get('value'):
                        payload=base64.b64decode(py.get('value'),validate=True)
                        json.loads(payload)  # Deliberately never use pickle or eval.
                        if suspicious(payload):
                            raise ValueError('sensitive pattern in serialized parameters')
        if 'Document.xml' not in z.namelist() or 'GuiDocument.xml' not in z.namelist():
            raise ValueError('missing native document XML')
        if sum(n.endswith('.Shape.brp') for n in z.namelist()) != 41:
            raise ValueError('expected 40 represented components plus reference wafer')

def check_bom(root: Path) -> None:
    rows=json.loads((root/'manufacturing/BOM_P1D1.json').read_text(encoding='utf-8'))
    with (root/'manufacturing/BOM_P1D1.csv').open(encoding='utf-8-sig',newline='') as f:
        csv_rows=list(csv.reader(f))[1:]
    if csv_rows != [[str(v) for v in row] for row in rows]:
        raise ValueError('CSV/JSON BOM mismatch')
    if len(rows)!=13 or sum(r[3] for r in rows)!=48:
        raise ValueError('expected 13 BOM rows / 48 pieces including off-model harness')
    if sum(r[3] for r in rows if r[1].startswith('ISO4762-'))!=16:
        raise ValueError('expected 16 screws')

def verify(root: Path=ROOT) -> dict:
    root=root.resolve()
    errors=[]
    manifest=json.loads((root/'release-manifest.json').read_text(encoding='utf-8'))
    entries=manifest['files']
    paths=[r['path'] for r in entries]
    if len(paths)!=len(set(paths)):
        errors.append('duplicate manifest entry')
    for row in entries:
        try:
            p=safe_path(root,row['path'])
            if not p.is_file() or p.stat().st_size!=row['bytes'] or sha256(p)!=row['sha256']:
                raise ValueError('missing, resized or hash-mismatched file')
            flags=suspicious(p.read_bytes())
            if flags:
                raise ValueError('sensitive pattern: '+', '.join(flags))
            if p.suffix=='.FCStd':
                check_fcstd(p)
            elif p.suffix=='.step':
                s=p.read_text(encoding='utf-8').strip()
                if not s.startswith('ISO-10303-21;') or not s.endswith('END-ISO-10303-21;'):
                    raise ValueError('invalid STEP boundary markers')
            elif p.suffix=='.json':
                json.loads(p.read_text(encoding='utf-8'))
            elif p.suffix=='.svg':
                s=p.read_text(encoding='utf-8')
                ET.fromstring(s)
                if re.search(r'<script|\bon\w+\s*=|(?:href|src)=[\"\x27](?:https?:|file:)',s,re.I):
                    raise ValueError('active or externally loaded SVG content')
        except (OSError,ValueError,KeyError,ET.ParseError,zipfile.BadZipFile) as exc:
            errors.append(f"{row['path']}: {exc}")
    actual={p.relative_to(root).as_posix() for p in root.rglob('*')
            if p.is_file() and not any(x in IGNORED_DIRS for x in p.relative_to(root).parts)}
    if actual != set(paths)|INDEXES:
        errors.append('manifest coverage mismatch: '+str(sorted(actual^(set(paths)|INDEXES))))
    expected=''.join(f"{r['sha256']}  {r['path']}\n" for r in entries)
    if (root/'SHA256SUMS.txt').read_text(encoding='utf-8')!=expected:
        errors.append('SHA256SUMS index does not match manifest')
    for p in root.rglob('*.md'):
        if '.git' in p.parts:
            continue
        for href in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            href=href.split('#')[0]
            if not href or re.match(r'[a-z]+:',href):
                continue
            q=(p.parent/href).resolve()
            if not q.is_relative_to(root) or not q.exists():
                errors.append(f'{p.relative_to(root)}: broken local link {href}')
    try:
        check_bom(root)
        if len(list((root/'drawings').glob('[0-9][0-9]_*.svg')))!=12 or len(list((root/'drawings').glob('[0-9][0-9]_*.dxf')))!=12:
            raise ValueError('expected 12 SVG and 12 DXF drawings')
    except (OSError,ValueError,IndexError) as exc:
        errors.append(str(exc))
    return {'status':'fail' if errors else 'pass','files_checked':len(entries),
            'scope':'release integrity only; no geometry recompute or physical qualification',
            'errors':errors}

if __name__=='__main__':
    try:
        result=verify()
    except (OSError,ValueError,KeyError,TypeError) as exc:
        result={'status':'fail','errors':[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result['status']=='pass' else 1)
