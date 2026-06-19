# Privacy And Sanitization

This repository is safe for public portfolio use only when it contains synthetic
or masked data.

## Do Not Commit

- Customer names, supplier names, or private site names.
- BOMs, routing exports, maintenance tickets, service reports, dispatch logs, or
  generated notice history from real operations.
- Local SQLite files, workstation logs, packaged executables, or generated
  workbook archives.
- Screenshots that reveal internal system URLs, user names, document IDs, or
  real production quantities.

## Public Sample Rules

- Use demo identifiers such as `ON-2026-DEMO-001`.
- Use rounded quantities and generic sources.
- Use generic teams such as `Planning`, `Warehouse`, `Control Desk`, or
  `Dispatch`.
- Describe business flow without naming real customers, products, suppliers, or
  factory lines.

## Adaptation Rule

When adapting the project for a real workflow, keep private payloads outside the
repository and write only masked examples back into `sample_data/`.
