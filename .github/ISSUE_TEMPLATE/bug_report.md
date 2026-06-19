---
name: Bug report
about: Report a reproducible problem in the public demo
title: "bug: "
labels: bug
---

## Scenario

Describe the notice type, domain, and command or endpoint used.

## Reproduction

```powershell
python -m factory_production_notice.cli generate --input sample_data\demo_notice_request.json --output output
```

## Expected

What should happen?

## Actual

What happened instead?

## Sanitization Check

- [ ] The payload is synthetic or masked.
- [ ] No customer, supplier, site, workstation, or internal system data is included.
