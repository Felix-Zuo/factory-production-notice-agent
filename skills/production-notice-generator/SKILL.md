# Operations Notice Generator Skill

Use this skill when an agent needs to turn a structured work package into an
operations notice workbook and preview. The public demo supports manufacturing,
warehouse, maintenance, service, and review workflows through the same contract.

## Required Input

Provide a JSON object matching `config/notice_schema.json`. Use
`sample_data/demo_notice_request.json` as the example shape. New integrations
should prefer `subject`, `resources`, `steps`, `fulfillment`, and `controls`;
legacy integrations may still use `product`, `materials`, `routing`,
`packaging`, and `quality`.

## Run

```powershell
python -m factory_production_notice.cli generate --input sample_data\demo_notice_request.json --output output
```

## Local API

```powershell
python -m factory_production_notice.cli serve --host 127.0.0.1 --port 8765 --output output
```

Then call:

```text
POST http://127.0.0.1:8765/api/generate-notice
POST http://127.0.0.1:8765/api/generate-operations-notice
```

## Output Handling

Read the manifest first. Then inspect:

- the Excel workbook for release-ready formatting
- the HTML preview for quick review
- the agent context JSON for risk checks and downstream reports

## Safety

Do not upload private BOM files, customer-specific data, supplier records,
generated notice history, or local executable packages into a public repository.
Keep final operational release behind human approval.
