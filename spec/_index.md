---
folder: spec
purpose: "Elaborations of approved REQs, grouped by domain."
owner: "BA Lead"
file_naming: "<domain>-spec.md (e.g., auth-spec.md, billing-spec.md)"
last_updated: 2026-05-26
ai_navigation_hint: |
  One spec per domain. Each spec lists the REQ-IDs it covers in frontmatter `covers_req`.
---

# Index — spec/

## Purpose
Elaborations of approved REQs, grouped by domain.

## File naming
<domain>-spec.md (e.g., auth-spec.md, billing-spec.md)

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | SPEC-NN-domain |
| title | string | Free text |
| status | enum | draft, approved, deprecated |
| version | string | semver |
| last_updated | date | ISO 8601 |
| covers_req | list[string] | REQ-IDs |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../requirements/`
- `../design/`

## Common questions
- **Where is auth spec?** → `auth-spec.md`
- **Which REQs does spec X cover?** → frontmatter `covers_req`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
