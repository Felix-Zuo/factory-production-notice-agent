# Contributing

Keep the public demo small and deterministic:

- Use synthetic data only.
- Keep generated files in `output/`.
- Add tests when changing payload parsing, workbook layout, HTTP behavior, or
  agent contracts.
- Run `operations-notice validate --input sample_data\demo_notice_request.json`
  before publishing contract changes.
- Keep generated Excel-safe text handling in place for every spreadsheet export.
- Keep the public contract generic. Prefer `subject`, `resources`, `steps`,
  `fulfillment`, and `controls`; keep legacy manufacturing aliases compatible.
- Avoid adding local launchers, packaged runtimes, private BOM files, or notice
  history to the repository.
- Keep roadmap and changelog entries honest: describe public demo evolution and
  sanitized reconstruction, not private customer facts.
