# SPDX-License-Identifier: MIT
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('verify_release',ROOT/'tools/verify_release.py')
verify=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)

class ReleaseTests(unittest.TestCase):
    def test_current_release(self):
        self.assertEqual(verify.verify()['errors'],[])

    def test_reject_traversal(self):
        for p in ['../outside','/etc/passwd','a/../../b','a\\b','']:
            with self.assertRaises(ValueError):
                verify.safe_path(ROOT,p)

    def test_pattern_detection(self):
        self.assertIn('github-token',verify.suspicious(('ghp_'+'A'*36).encode()))
        self.assertIn('local-user-path',verify.suspicious(('/'+'Users/'+'example'+'/private.txt').encode()))
        self.assertEqual(verify.suspicious(b'https://github.com/crabtail-chais/wf300-wafer-gripper'),[])

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve()
            (root/'link').symlink_to(root/'target')
            with self.assertRaises(ValueError):
                verify.safe_path(root,'link')

    def test_hash_mismatch_fails(self):
        with patch.object(verify,'sha256',return_value='0'*64):
            result=verify.verify()
        self.assertEqual(result['status'],'fail')
        self.assertTrue(any('hash-mismatched' in e for e in result['errors']))

    def test_bad_bom_fails(self):
        with patch.object(verify,'check_bom',side_effect=ValueError('BOM mismatch')):
            result=verify.verify()
        self.assertEqual(result['status'],'fail')
        self.assertIn('BOM mismatch',result['errors'])

if __name__=='__main__':
    unittest.main()
