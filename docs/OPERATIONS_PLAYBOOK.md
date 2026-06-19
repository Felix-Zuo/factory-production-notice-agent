# Operations Playbook

## Release Checklist

- Run `python -m pytest -q`.
- Run `scripts\run_demo.cmd` from a clean checkout or virtual environment.
- Open the generated HTML preview and confirm labels, quantities, and review
  sections render correctly.
- Check that `agent_interface.json`, `config/notice_schema.json`, and
  `workflows/agent_workflow.md` describe the same contract.
- Confirm no generated files, private records, local databases, or executable
  packages are staged.

## Demo Review Checklist

- The sample data must be synthetic.
- The README should show the generic operations contract first.
- The manufacturing legacy path should still be tested.
- The local API should return structured JSON for both success and invalid
  request cases.

## Incident Notes

For public demo issues, prefer a small reproducible JSON payload over screenshots
of real operational systems. If a bug came from a private workflow, rewrite the
report with synthetic field names and quantities before filing it.

## Versioning

- Patch releases: test, packaging, docs, and small compatibility fixes.
- Minor releases: contract additions, new sample domains, or new artifact types.
- Major releases: breaking changes to payload fields or generated artifact
  semantics.
