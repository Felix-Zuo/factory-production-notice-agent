# Agent Workflow: Production Notice Generation

This workflow is written for an external agent that needs to prepare a
production notice while keeping final release under human control.

## Inputs

- A `ProductionNoticeRequest` JSON payload.
- Optional upstream context from ERP, MES, WMS, BOM, or planning adapters.
- A target output directory.

## Steps

1. Validate that `notice_id`, `work_order`, `product`, `quantity`, and
   `due_date` are present.
2. Check that material, routing, packaging, and quality fields are consistent
   with the request.
3. Call the generator through CLI or HTTP.
4. Read the manifest and `agent_context.json`.
5. Summarize risks for a human reviewer:
   - missing product or routing details
   - unusually high quantity
   - missing packaging rule
   - missing first-piece or inspection rule
6. Wait for human approval before treating the notice as released.

## CLI

```powershell
python -m factory_production_notice.cli generate --input sample_data\demo_notice_request.json --output output
```

## HTTP

```text
POST /api/generate-notice
```

Body: `ProductionNoticeRequest` JSON.

## Expected Artifacts

- Excel production notice
- HTML preview
- manifest JSON
- agent context JSON

## Human Gate

The tool can generate a notice, but it should not automatically release a real
production order. Treat final release as a human approval step.
