---
folder: scripts
purpose: "CI scripts: frontmatter validator + Tier A/B index/prompts regenerator."
owner: "Tech Lead"
file_naming: "<purpose>.py (e.g., validate_frontmatter.py, regen_indexes.py)"
last_updated: 2026-05-26
ai_navigation_hint: |
  Tier B — _index.md required, _prompts.md optional. Run scripts locally before commit.
---

# Index — scripts/

## Purpose
CI scripts: frontmatter validator + Tier A/B index/prompts regenerator.

## File naming
<purpose>.py (e.g., validate_frontmatter.py, regen_indexes.py)

## Frontmatter schema
_(Python scripts — no MD record schema)_

## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../.github/workflows/`
- `../`

## Common questions
- **How do I validate locally?** → `python scripts/validate_frontmatter.py` + `python scripts/regen_indexes.py .`
- **Tier patterns?** → edit TIER_A_PATTERNS / TIER_B_PATTERNS / SKIP_DIRS at top of `regen_indexes.py`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

| File | ID | Title | Status | Owner | Updated |
|------|----|----|--------|-------|---------|
| [regen_indexes.py](regen_indexes.py) | - | regen_indexes | - | - | 2026-05-26 |
| [validate_frontmatter.py](validate_frontmatter.py) | - | validate_frontmatter | - | - | 2026-05-26 |
