# Roadmap

The roadmap is intentionally public-demo friendly. Items describe reusable
product direction, not private customer commitments.

## Current Release: 0.2.x

- Keep the generator local-first and deterministic.
- Preserve compatibility with manufacturing production-notice payloads.
- Make the public contract useful across warehouse, maintenance, service, and
  review workflows.
- Keep synthetic samples and generated output out of the repository history.

## Next: 0.3.x

- Add optional JSON Schema validation dependency behind a dev extra.
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
