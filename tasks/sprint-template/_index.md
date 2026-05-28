---
folder: sprint-template
purpose: "Template — copy to sprint-NN/ when planning a new sprint. Substitute {{SPRINT_NN}}."
owner: "Tech Lead"
file_naming: "TASK-NNN-short-kebab-title.md"
last_updated: 2026-05-28
ai_navigation_hint: |
  This is the sprint scaffold template. Do NOT add real tasks here. When opening
  a new sprint, copy this folder to sprint-NN/ and replace {{SPRINT_NN}} tokens.
---

# Index — {{SPRINT_NN}}/

## Purpose
{{SPRINT_NN}} tasks.

## File naming
TASK-NNN-short-kebab-title.md

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | TASK-NNN |
| title | string | Free text |
| status | enum | todo, in-progress, review, done, blocked |
| team | enum | See `../../00-overview/teams.md` |
| assignee | string | required when status != todo |
| req_ref | string | REQ-NNN |
| design_ref | string | DES-NN-domain (the design doc this task implements; optional for spikes/infra) |
| sprint | string | sprint-NN |
| estimate_hours | number | Decimal allowed |
| actual_hours | number | Optional, filled at done |
| last_updated | date | ISO 8601 |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../`
- `../../feedback/{{SPRINT_NN}}/`

## Common questions
- **Sprint goal?** → see Sprint Goals section below
- **Burndown?** → `../../dashboard/dashboard.md`


## Sprint goals
- TBD

## Sprint dates
- Start: TBD
- End: TBD

## Planned REQs
- TBD


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
