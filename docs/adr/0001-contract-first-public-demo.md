# ADR 0001: Contract-First Public Demo

## Status

Accepted

## Context

The project began as a production-notice generator, but a public portfolio repo
should demonstrate a reusable workflow rather than a single private process.

## Decision

Use a generic operations notice contract as the public interface. Keep legacy
manufacturing aliases working, but document `subject`, `resources`, `steps`,
`fulfillment`, and `controls` as the preferred fields.

## Consequences

- The demo can represent manufacturing, warehouse, maintenance, service, and
  review workflows.
- Existing production-notice examples remain compatible.
- Public documentation can be product-like without exposing private process
  details.
