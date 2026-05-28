---
folder: sprint-template
purpose: "Template — copy to sprint-NN/ when planning a new sprint. Substitute {{SPRINT_NN}}."
owner: "BA Lead"
file_naming: "FB-NNN-short-kebab-title.md, retro.md"
last_updated: 2026-05-28
ai_navigation_hint: |
  This is the sprint feedback scaffold. Do NOT add real FB entries here. When opening
  a new sprint, copy this folder to sprint-NN/ and replace {{SPRINT_NN}} tokens.
---

# Index — {{SPRINT_NN}}/

## Purpose
Feedback raised during {{SPRINT_NN}} + retro.

## File naming
FB-NNN-short-kebab-title.md, retro.md

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | FB-NNN |
| sprint_raised | string | sprint-NN |
| source | enum | demo, UAT, email, call, internal |
| type | enum | bug, change-request, clarification, enhancement |
| severity | enum | critical, high, medium, low |
| status | enum | triaged, accepted, in-progress, done, rejected, deferred, duplicate |
| related_req | string or list | REQ-NNN |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../`
- `../../tasks/{{SPRINT_NN}}/`

## Common questions
- **Open FBs this sprint?** → filter Catalog by status
- **Retro notes?** → `retro.md`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
