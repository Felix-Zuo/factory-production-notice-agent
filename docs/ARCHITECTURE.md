# Architecture

Structured Operations Notice Agent is a contract-first generator. It accepts a
small JSON work-package request, validates the minimum release fields, and emits
reviewable local artifacts.

## Components

- `models.py`: parses the request into a normalized notice model.
- `generator.py`: creates the Excel workbook, HTML preview, manifest, and agent
  context.
- `cli.py`: exposes deterministic command-line entry points.
- `server.py`: exposes a local-only HTTP demo boundary.
- `agent_contract.py`: describes capabilities for external agents and workflow
  orchestrators.

## Data Flow

```text
JSON request
  -> normalized notice model
  -> workbook + HTML preview
  -> manifest + agent context
  -> human review gate
```

## Contract Strategy

The v0.2 public contract uses neutral operations vocabulary:

- `subject`: the thing or job being coordinated
- `resources`: material, document, tool, label, or kit requirements
- `steps`: execution sequence and owners
- `fulfillment`: packing, dispatch, handoff, or delivery rules
- `controls`: approval, sampling, quality, or compliance checks

Legacy manufacturing fields remain supported to protect existing demo usage:

- `product`
- `materials`
- `routing`
- `packaging`
- `quality`

## Runtime Boundary

The HTTP server is for local demos and agent integration tests. It is deliberately
small, stateless, file-output based, and loopback-only by default. A production
deployment would need authentication, authorization, audit logging, retention
rules, and an external storage boundary.
