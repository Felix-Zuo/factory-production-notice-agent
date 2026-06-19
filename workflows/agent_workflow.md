# Agent Workflow: Operations Notice Generation

This workflow is written for an external agent that needs to prepare a
structured operations notice while keeping final release under human control.

## Inputs

- An `OperationsNoticeRequest` JSON payload.
- Optional upstream context from ERP, MES, WMS, CMMS, ticketing, inventory, or planning adapters.
- A target output directory.

## Steps

1. Validate that `notice_id`, `work_order`, `subject` or `product`, `quantity`,
   and `due_date` are present.
2. Check that resource, step, fulfillment, and control fields are consistent
   with the request.
3. Call the generator through CLI or HTTP.
4. Read the manifest and `agent_context.json`.
5. Summarize risks for a human reviewer:
   - missing subject or execution details
   - unusually high quantity
   - missing fulfillment rule
   - missing approval, review, or inspection rule
6. Wait for human approval before treating the notice as released into a live workflow.

## CLI

```powershell
python -m factory_production_notice.cli generate --input sample_data\demo_notice_request.json --output output
```

## HTTP

```text
POST /api/generate-notice
POST /api/generate-operations-notice
```

Body: `OperationsNoticeRequest` JSON.

## Expected Artifacts

- Excel operations notice
- HTML preview
- manifest JSON
- agent context JSON

## Human Gate

The tool can generate a notice, but it should not automatically release a real
production, warehouse, service, maintenance, or compliance task. Treat final
release as a human approval step.
