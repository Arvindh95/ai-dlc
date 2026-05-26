---
folder: client-emails
purpose: "Client emails."
owner: "BA Lead"
file_naming: "YYYY-MM-DD-short-title.md"
last_updated: 2026-05-26
ai_navigation_hint: |
  Client emails. One MD per source artifact.
---

# Index — client-emails/

## Purpose
Client emails.

## File naming
YYYY-MM-DD-short-title.md

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | RAW-NNN |
| source_type | enum | workshop, email, doc, call, chat |
| source_date | date | ISO 8601 |
| captured_by | string | Name |
| status | enum | unprocessed, partially-processed, fully-processed, superseded |
| generated_reqs | list[string] | REQ-IDs (required when partially/fully-processed) |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../`

## Common questions
- **Latest input?** → sort Catalog by Updated


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
