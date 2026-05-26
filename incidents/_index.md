---
folder: incidents
purpose: "Production incidents + postmortems."
owner: "Tech Lead"
file_naming: "INC-NNN-short-kebab-title.md"
last_updated: 2026-05-26
ai_navigation_hint: |
  Severity legend: sev1=outage, sev2=degraded, sev3=minor. Every incident must have a postmortem within 5 business days.
---

# Index — incidents/

## Purpose
Production incidents + postmortems.

## File naming
INC-NNN-short-kebab-title.md

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | INC-NNN |
| date | date | ISO 8601 |
| severity | enum | sev1, sev2, sev3 |
| incident_commander | string | Name |
| data_loss | bool | true/false |
| data_breach | bool | true/false |
| status | enum | open, mitigated, resolved, postmortem-pending, closed |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../requirements/`
- `../design/`

## Common questions
- **Postmortem template?** → see _prompts.md
- **Open incidents?** → filter Catalog by status


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
