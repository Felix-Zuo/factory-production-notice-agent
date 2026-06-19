# Roadmap

The roadmap is intentionally public-demo friendly. Items describe reusable
product direction, not private customer commitments.

## Current Release: 0.2.1

- Keep the generator local-first and deterministic.
- Preserve compatibility with manufacturing production-notice payloads.
- Make the public contract useful across warehouse, maintenance, service, and
  review workflows.
- Keep synthetic samples and generated output out of the repository history.
- Validate sample payloads, artifact generation, and package contents in CI.
- Keep local API binding loopback-only unless explicitly overridden.
- Escape formula-like values before writing spreadsheet cells.

## Next: 0.3.x

- Add more sample adapters:
  - CSV to operations notice request
  - ERP/MES-style work order export
  - ticket or service-task export
- Add richer review flags in `agent_context.json`, including missing owner,
  missing control gate, and unusually high quantity checks.
- Add a lightweight static demo page for multiple scenarios.

## Later

- Add template profiles for manufacturing, warehouse, maintenance, service, and
  compliance review.
- Add signed manifest hashes for artifact integrity checks.
- Add optional storage adapters while keeping the default demo file-based.
- Add CI workflow for lint, unit tests, and package build.

## Non-Goals

- No private customer data in the public repository.
- No automatic release into a live operational system.
- No hosted production API without authentication, authorization, audit logging,
  and data retention controls.
