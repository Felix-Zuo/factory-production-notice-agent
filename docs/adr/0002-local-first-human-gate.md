# ADR 0002: Local-First Generator With Human Gate

## Status

Accepted

## Context

Notice generation can prepare release artifacts, but automatically releasing a
real work order would require approvals, audit logging, permissions, and system
integration.

## Decision

Keep this project local-first and artifact-generating. The generator outputs a
workbook, preview, manifest, and workflow context, then stops at a human review
gate.

## Consequences

- The public demo stays deterministic and safe to run.
- The local HTTP server remains an integration demo, not a production API.
- Any production adoption needs an explicit gateway, auth, audit, and storage
  design.
