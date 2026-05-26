---
folder: change-requests
purpose: "Change requests against approved REQs (scope/schedule/budget/technical)."
owner: "PM"
file_naming: "CR-NNN-short-kebab-title.md"
last_updated: 2026-05-26
ai_navigation_hint: |
  CRs gate scope changes after REQ approval. Each CR links to affected REQ-IDs.
---

# Index — change-requests/

## Purpose
Change requests against approved REQs (scope/schedule/budget/technical).

## File naming
CR-NNN-short-kebab-title.md

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | CR-NNN |
| type | enum | scope, schedule, budget, technical |
| raised_by | string | Name |
| raised_date | date | ISO 8601 |
| affects_req | list[string] | REQ-IDs |
| status | enum | under-review, approved, rejected, deferred |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../requirements/`
- `../decisions/`

## Common questions
- **Open CRs?** → filter Catalog by status=under-review
- **How does a CR become a REQ change?** → see _prompts.md OP-link-to-REQ-revision


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
