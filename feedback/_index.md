---
folder: feedback
purpose: "Feedback intake, triage, classification, sprint retros."
owner: "BA Lead"
file_naming: "heterogeneous (INBOX.md + sprint-NN/ subfolders with FB-NNN-*.md)"
last_updated: 2026-05-26
ai_navigation_hint: |
  New raw feedback → INBOX.md. After triage → FB-NNN-*.md in correct sprint subfolder.
---

# Index — feedback/

## Purpose
Feedback intake, triage, classification, sprint retros.

## File naming
heterogeneous (INBOX.md + sprint-NN/ subfolders with FB-NNN-*.md)

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
- `../requirements/`
- `../change-requests/`
- `../tasks/`

## Common questions
- **Where to dump client feedback?** → `INBOX.md`
- **FB triage SLA?** → see _prompts.md
- **Sprint retro?** → `sprint-NN/retro.md`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

| File | ID | Title | Status | Owner | Updated |
|------|----|----|--------|-------|---------|
| [INBOX.md](INBOX.md) | - | INBOX | - | - | - |
