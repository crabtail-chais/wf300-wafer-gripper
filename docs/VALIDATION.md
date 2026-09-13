# Evidence and qualification status

## Historical CAD statements are not independent public test evidence

The unchanged assembly manual cites historical CAD checks associated with the original P1D1 engineering session. Detailed internal test reports and numerical validation records are **not included in this public repository**. Those historical statements cannot be independently reproduced from the published integrity checker. This release does not claim an independent CAD revalidation, manufacturing approval or physical wafer qualification.

Native file identity is recorded in [provenance.json](../validation/provenance.json). These are file hashes and publication mappings, not test results. The geometry, tolerances, BOM and manufacturing requirements were not changed during publication packaging.

## Current publication checks

`tools/verify_release.py` checks the release manifest, SHA-256 values, native ZIP/XML container structure, base64 JSON parameter syntax, STEP boundaries, CSV/JSON BOM agreement, BOM totals, 24 drawing files, local Markdown links, and selected path/credential patterns. It does not load a CAD kernel or execute embedded data. Tests exercise failure handling as well as the current package.

The release manifest deliberately excludes itself and `SHA256SUMS.txt` from its file list. These two index files are not self-authenticating; a trusted Git commit or independently delivered digest is still needed for authenticity. Passing checks does not guarantee the absence of every conceivable secret, legal encumbrance or design defect.

## Open engineering gates

Manufacturing capability / drawing approval; physical terminal compatibility and crimping; joint torque windows; hand-force / friction / harness behavior; operator load and fatigue; cleanroom particles and metal / ionic contamination; cleaning; wafer surface potential and ESD; wafer edge integrity at thickness limits; life testing and maintenance intervals. None are closed by publishing this repository.
