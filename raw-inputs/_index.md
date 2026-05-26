---
folder: raw-inputs
purpose: "Workshop transcripts, client emails, source documents — feed for REQ generation."
owner: "BA Lead"
file_naming: "heterogeneous (workshops/, client-emails/, client-docs/ subfolders with date-prefixed MDs)"
last_updated: 2026-05-26
ai_navigation_hint: |
  Inputs flow IN here, REQs flow OUT (via `requirements/_prompts.md` OP-1). Track status to know which inputs are processed.
---

# Index — raw-inputs/

## Purpose
Workshop transcripts, client emails, source documents — feed for REQ generation.

## File naming
heterogeneous (workshops/, client-emails/, client-docs/ subfolders with date-prefixed MDs)

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
- `../requirements/`
- `workshops/`
- `client-emails/`
- `client-docs/`

## Common questions
- **Where do I dump a transcript?** → `workshops/`
- **Where do client emails go?** → `client-emails/`
- **Has this input been processed?** → frontmatter `status`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
