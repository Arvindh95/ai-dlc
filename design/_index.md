---
folder: design
purpose: "Technical design documents + ADRs."
owner: "Tech Lead"
file_naming: "<domain>-design.md, architecture.md, data-model.md, api-contracts.md; ADRs in `adrs/`"
last_updated: 2026-05-26
ai_navigation_hint: |
  One design per domain. Architecture overview in `architecture.md`. Decisions in `adrs/`.
---

# Index — design/

## Purpose
Technical design documents + ADRs.

## File naming
<domain>-design.md, architecture.md, data-model.md, api-contracts.md; ADRs in `adrs/`

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | DES-NN-domain |
| title | string | Free text |
| status | enum | draft, approved, deprecated |
| version | string | semver |
| last_updated | date | ISO 8601 |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../spec/`
- `adrs/`
- `../tasks/`

## Common questions
- **Overall architecture?** → `architecture.md`
- **Why postgres?** → `adrs/_index.md`
- **API contract for X?** → `api-contracts.md`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
