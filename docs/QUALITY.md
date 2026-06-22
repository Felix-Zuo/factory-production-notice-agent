# Quality And Security Notes

This document captures the practical checks that keep the public demo stable.

## Runtime Guarantees

- The CLI reads a JSON object, validates it, and writes local artifacts.
- The CSV adapter limits row count and cell length before conversion.
- CSV imports validate required fields, booleans, numbers, and the normalized
  notice payload before writing generated request files.
- Generated HTML escapes user-provided values before rendering.
- Generated Excel cells escape formula-like text before writing workbook cells.
- The demo HTTP server refuses non-loopback hosts unless `--allow-remote` is
  explicitly passed.
- The request body limit is 1 MB for the local HTTP demo server.
- CLI and HTTP generation return artifact names without exposing local absolute
  file paths under the artifact fields.

## Validation Surface

```powershell
operations-notice validate --input sample_data\demo_notice_request.json
operations-notice profiles
operations-notice import-csv --input sample_data\csv\work_package_notices.csv --output-dir output_import_probe
python -m pytest -q
python scripts\package_project.py --output output_package_probe
python scripts\verify_package.py output_package_probe\factory-production-notice-agent.zip
```

## Security Boundaries

- No generated workbooks or local output directories should be committed.
- No live operational records belong in `sample_data/`.
- The local HTTP server is not a production API and has no authentication.
- Remote binding is blocked by default to avoid accidental network exposure.

## User Experience Checks

- README commands should run from a fresh checkout.
- `scripts\run_demo.cmd` should create a virtual environment if needed.
- `docs/showcase.html` should use only committed assets.
- `docs/index.html` should route to the current showcase page for GitHub Pages.
- The generated manifest should use relative artifact names for portability.
