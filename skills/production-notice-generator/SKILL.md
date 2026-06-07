# Production Notice Generator Skill

Use this skill when an agent needs to turn a structured manufacturing work
order into a production notice workbook and preview.

## Required Input

Provide a JSON object matching `config/notice_schema.json`. Use
`sample_data/demo_notice_request.json` as the example shape.

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
```

## Output Handling

Read the manifest first. Then inspect:

- the Excel workbook for release-ready formatting
- the HTML preview for quick review
- the agent context JSON for risk checks and downstream reports

## Safety

Do not upload production BOM files, customer-specific data, generated notice
history, or local executable packages into a public repository. Keep final
production release behind human approval.
