# Architecture

Structured Operations Notice Agent is a contract-first generator. It accepts a
small JSON work-package request or a tabular CSV work-package export, validates
the minimum release fields, and emits reviewable local artifacts.

## Components

- `models.py`: parses the request into a normalized notice model.
- `profiles.py`: exposes built-in scenario profiles for common operations
  workflows.
- `csv_adapter.py`: converts bounded CSV work-package rows into normalized JSON
  request files.
- `generator.py`: creates the Excel workbook, HTML preview, manifest, and agent
  context.
- `cli.py`: exposes deterministic command-line entry points.
- `server.py`: exposes a local-only HTTP demo boundary.
- `agent_contract.py`: describes capabilities for external agents and workflow
  orchestrators.

## Data Flow

```text
Scenario profile or CSV export
  -> normalized JSON request
  -> normalized notice model
  -> workbook + HTML preview
  -> manifest + agent context
  -> human review gate
```

## Contract Strategy

The v0.3 public contract uses neutral operations vocabulary:

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
