---
folder: tasks
purpose: "Sprint-organized implementation tasks. Each TASK traces back to a REQ."
owner: "Tech Lead"
file_naming: "heterogeneous (sprint-NN/ subfolders + backlog.md)"
last_updated: 2026-05-26
ai_navigation_hint: |
  Current sprint: see root `_index.md` frontmatter. Pre-sprint items in `backlog.md`.
---

# Index — tasks/

## Purpose
Sprint-organized implementation tasks. Each TASK traces back to a REQ.

## File naming
heterogeneous (sprint-NN/ subfolders + backlog.md)

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | TASK-NNN |
| title | string | Free text |
| status | enum | todo, in-progress, review, done, blocked |
| team | enum | See `../../00-overview/teams.md` |
| assignee | string | required when status != todo |
| req_ref | string | REQ-NNN |
| sprint | string | sprint-NN |
| estimate_hours | number | Decimal allowed |
| actual_hours | number | Optional, filled at done |
| last_updated | date | ISO 8601 |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../requirements/`
- `../spec/`
- `../feedback/`

## Common questions
- **Current sprint?** → see root `_index.md`
- **My open tasks?** → `../dashboard/dashboard.md` → My open tasks
- **Backlog?** → `backlog.md`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

| File | ID | Title | Status | Owner | Updated |
|------|----|----|--------|-------|---------|
| [backlog.md](backlog.md) | - | backlog | - | - | - |
