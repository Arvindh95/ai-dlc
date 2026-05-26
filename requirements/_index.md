---
folder: requirements
purpose: "One MD file per atomic business/system requirement. Source of truth."
owner: "BA Lead"
file_naming: "REQ-NNN-short-kebab-title.md (e.g., REQ-042-totp-login.md)"
last_updated: 2026-05-26
ai_navigation_hint: |
  Use the Catalog below to find a REQ. Do not grep — read the index. REQ-ID range assigned per team (see `../00-overview/teams.md`).
---

# Index — requirements/

## Purpose
One MD file per atomic business/system requirement. Source of truth.

## File naming
REQ-NNN-short-kebab-title.md (e.g., REQ-042-totp-login.md)

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | REQ-NNN |
| title | string | Free text |
| status | enum | draft, approved, in-dev, ready-for-acceptance, done, blocked, late-change, rejected, deferred |
| priority | enum | critical, high, medium, low |
| team | enum | See `../00-overview/teams.md` |
| estimate_days | number | Decimal allowed |
| created | date | ISO 8601 |
| approved | date or null | ISO 8601 |
| implemented | date or null | ISO 8601 |
| spec_ref | string | Path#anchor |
| design_ref | string | Path#anchor |
| tasks | list[string] | TASK-IDs |
| test_ref | string | Path to test file |
| tags | list[string] | Domain tags |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../spec/`
- `../design/`
- `../tasks/`
- `../feedback/`
- `../change-requests/`

## Common questions
- **Which REQs are blocked?** → `../dashboard/queries/blocked.md`
- **AC for REQ-X?** → open `REQ-X-*.md`, see `## Acceptance Criteria`
- **How to create a new REQ?** → see `_prompts.md` OP-1


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
