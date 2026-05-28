---
folder: risks
purpose: "Project risk register. Seeded at kickoff, evolves continuously."
owner: "PM"
file_naming: "RISK-NNN-short-kebab-title.md"
last_updated: 2026-05-28
ai_navigation_hint: |
  Living risk register. Add at kickoff + when feedback/incidents reveal new risks.
  Append-only history via Change Log. Closed risks stay in catalog, do not delete.
---

# Index — risks/

## Purpose
Project risk register. Seeded at kickoff, evolves continuously.

## File naming
RISK-NNN-short-kebab-title.md

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | RISK-NNN |
| title | string | Free text |
| raised_date | date | ISO 8601 |
| raised_by | string | Name |
| likelihood | enum | low, medium, high |
| impact | enum | low, medium, high |
| status | enum | open, mitigated, accepted, closed, materialised |
| owner | string | Name (who watches this risk) |
| linked_inc | string or list | INC-NNN (only if status=materialised) |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../incidents/` (when a risk materialises)
- `../feedback/` (feedback may surface new risks)
- `../change-requests/` (CR impact may raise new risks)
- `../00-overview/cadence.md` (steering review cadence for sev-high risks)

## Common questions
- **Top open risks?** → filter catalog by status=open + impact=high
- **Did RISK-X materialise?** → check status=materialised + linked_inc
- **Risk owner for X?** → frontmatter owner field

## Conventions
- Add 3-5 seed risks at kickoff. Don't try to be exhaustive.
- Sev (high likelihood × high impact) → escalate to Sponsor at next steering.
- Renumber never. Closed risks stay in catalog.
- Status flow: open → mitigated → closed. Or open → materialised (link INC).
- Re-open closed risk = new RISK-NNN record, link old in body.

## Body structure (per RISK file)
```
# RISK-NNN: <title>

## Description
What could go wrong. One paragraph.

## Trigger / signal
What we'd see if this is materialising.

## Mitigation
Action(s) we're taking now or planning. Link TASKs if any.

## Contingency
What we do if it materialises despite mitigation.

## Change Log
- YYYY-MM-DD: Raised by <name>.
```

## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
