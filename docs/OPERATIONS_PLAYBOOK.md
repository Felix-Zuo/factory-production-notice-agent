# Operations Playbook

## Release Checklist

- Run `python -m pytest -q`.
- Run `operations-notice profiles`.
- Run `operations-notice templates`.
- Run `operations-notice import-csv --input sample_data\csv\work_package_notices.csv --output-dir output_import_probe`.
- Run `operations-notice schedule-generate --input sample_data\scheduling_plan.json --output output_schedule_probe`.
- Run `operations-notice validate --input sample_data\demo_notice_request.json`.
- Run `operations-notice validate --input sample_data\production_notice_request.json`.
- Run `scripts\run_demo.cmd` from a clean checkout or virtual environment.
- Run `python scripts\verify_package.py output_package_probe\factory-production-notice-agent.zip` after packaging.
- Open the generated HTML preview and confirm labels, quantities, and review
  sections render correctly.
- Check that `agent_interface.json`, `config/notice_schema.json`, and
  `workflows/agent_workflow.md` describe the same contract.
- Confirm no generated files, private records, local databases, or executable
  packages are staged.

## Demo Review Checklist

- The sample data must be synthetic.
- The README should show the generic operations contract first.
- The CSV adapter should convert synthetic work-package rows into validated JSON
  without writing generated artifacts into source-controlled directories.
- Template and schedule samples should produce usable notice artifacts, not only
  catalog output.
- The manufacturing legacy path should still be tested.
- The local API should return structured JSON for both success and invalid
  request cases.
- Non-loopback HTTP binding should fail unless `--allow-remote` is used.
- Formula-like workbook text should be escaped before Excel opens the file.

## Incident Notes

For public demo issues, prefer a small reproducible JSON payload over screenshots
of real operational systems. If a bug came from a private workflow, rewrite the
report with synthetic field names and quantities before filing it.

## Versioning

- Patch releases: test, packaging, docs, and small compatibility fixes.
- Minor releases: contract additions, new sample domains, or new artifact types.
- Major releases: breaking changes to payload fields or generated artifact
  semantics.
