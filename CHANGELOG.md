# Changelog

This changelog records the public demo evolution. Pre-public entries are
reconstructed from sanitized implementation milestones so the repository tells a
complete product story without exposing private operational data.

## 0.2.1 - 2026-06-19

### Added

- `operations-notice validate` command for preflight payload checks.
- CI checks for sample validation, artifact generation, and package archive
  verification.
- Dependabot configuration for Python and GitHub Actions updates.
- Code of Conduct, Support, and quality/security documentation.

### Changed

- API responses now return artifact file names plus output directory instead of
  nesting absolute paths under `artifacts`.
- The local API refuses non-loopback bind hosts unless `--allow-remote` is
  explicitly passed.

### Fixed

- Escaped formula-like user text before writing Excel workbook cells.
- Removed illegal control characters from workbook text values.

## 0.2.0 - 2026-06-19

### Added

- Generic operations notice contract with `subject`, `resources`, `steps`,
  `fulfillment`, and `controls`.
- Backward-compatible support for legacy manufacturing fields:
  `product`, `materials`, `routing`, `packaging`, and `quality`.
- Cross-domain sample request for a warehouse fulfillment work package.
- Local API alias: `POST /api/generate-operations-notice`.
- Request-size guard and structured local API errors.
- Product documentation: roadmap, architecture, operating playbook, privacy
  notes, and architecture decision records.

### Changed

- Repositioned the public demo from single-purpose production notice generation
  to a reusable operations notice workbench.
- Updated generated workbook and preview labels to use neutral operations
  language.
- Updated agent contract and workflow docs to describe cross-domain usage.

### Fixed

- Added validation for blank IDs and non-positive quantities.
- Kept a stable fresh-checkout test path through `pyproject.toml`.

## 0.1.1 - 2026-06-12

### Fixed

- Added pytest `src` import path configuration so `python -m pytest -q` works
  from a fresh checkout.

## 0.1.0 - 2026-06-07

### Added

- First public sanitized demo of the notice generator.
- CLI generation flow for workbook, HTML preview, manifest, and agent context.
- Local HTTP demo endpoint for agent integration.
- Synthetic sample payload and static showcase page.

## Pre-Public Extraction

### Added

- Contract-first notice payload shape.
- Workbook layout with review, resource, execution, fulfillment, and approval
  zones.
- Human approval gate as a product rule: the tool prepares artifacts, but does
  not release real operational work automatically.
