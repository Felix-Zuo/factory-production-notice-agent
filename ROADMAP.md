# Roadmap

The roadmap is intentionally public-demo friendly. Items describe reusable
product direction, not private customer commitments.

## Current Release: 0.4.0

- Keep the generator local-first and deterministic.
- Preserve compatibility with manufacturing production-notice payloads.
- Make the public contract useful across warehouse, maintenance, service, and
  review workflows.
- Keep synthetic samples and generated output out of the repository history.
- Validate sample payloads, artifact generation, and package contents in CI.
- Keep local API binding loopback-only unless explicitly overridden.
- Escape formula-like values before writing spreadsheet cells.
- Provide built-in scenario profiles for common operations workflows.
- Convert CSV work-package rows into validated JSON notice requests.
- Keep the showcase page aligned with the current product surface.
- Provide built-in notice templates and user-owned template loading.
- Support custom fields in requests, generated previews, workbooks, and context.
- Convert schedule plans into production notice requests and generated release
  packets.

## Next: 0.5.x

- Add richer review flags in `agent_context.json`, including missing owner,
  missing control gate, and unusually high quantity checks.
- Add optional ERP/MES-style and ticket export adapters as examples.
- Add static generated examples for each built-in scenario profile.
- Add optional template validation reports for user-owned template files.

## Later

- Add signed manifest hashes for artifact integrity checks.
- Add optional storage adapters while keeping the default demo file-based.
- Add optional lint/type checks once the public API surface stabilizes.

## Non-Goals

- No private customer data in the public repository.
- No automatic release into a live operational system.
- No hosted production API without authentication, authorization, audit logging,
  and data retention controls.
