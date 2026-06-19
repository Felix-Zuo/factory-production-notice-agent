# Security

This repository is prepared as a public demo. Do not commit private BOM files,
customer lists, supplier records, maintenance tickets, warehouse dispatch
history, service reports, generated notice archives, SQLite indexes, executable
launchers, or workstation logs.

The demo input in `sample_data/` is synthetic. Replace it only with masked
examples when adapting the project.

## Local API Scope

The demo HTTP server is intended for local development and agent integration
tests. It is not an authenticated production API. Put a real gateway, auth
layer, audit log, and storage boundary in front of it before connecting it to
live operational systems.
