---
folder: legacy-system
purpose: "Legacy artifacts for migration projects — source code, SQL schema, stored procs, API specs, ERDs, UI mockups, old manuals."
owner: "Tech Lead"
file_naming: "Original artifact kept as-is (e.g. licensing-schema.sql) + sidecar RAW-NNN-*.md per artifact."
last_updated: 2026-05-28
ai_navigation_hint: |
  Migration source material. Two-step flow: artifact -> inventory (in sidecar MD) -> REQs.
  Original code/schema files are kept as-is (validator ignores non-MD). Each artifact gets
  a sidecar RAW-NNN MD holding frontmatter + a pointer to the original + the extracted inventory.
  Never inline a huge file into the MD — point to it.
---

# Index — legacy-system/

## Purpose
Legacy artifacts for migration projects — source code, SQL schema, stored procedures, API specs, ERDs, UI mockups, old user manuals. The feed for reverse-engineering requirements when replacing an existing system.

## File naming
- Original artifact: kept as-is, e.g. `licensing-schema.sql`, `ApplicantService.java`, `openapi.yaml`
- Sidecar record: `RAW-NNN-short-title.md` (one per artifact) — holds frontmatter + inventory

## Why a sidecar?
Source code and schemas are not natural language — the AI cannot extract REQs from them directly the way it does from a workshop transcript. The sidecar holds an **inventory**: the AI's structured reading of the artifact (entities, fields, constraints, observed business rules), each line cited to the original. REQs then extract from the inventory, preserving the chain: REQ -> inventory -> original artifact.

## Frontmatter schema (sidecar MD)
| Field | Type | Values |
|-------|------|--------|
| id | string | RAW-NNN |
| source_type | enum | code, schema, api-spec, db-erd, ui-mockup, user-manual |
| source_date | date | ISO 8601 (artifact's date, or capture date if unknown) |
| captured_by | string | Name |
| status | enum | unprocessed, partially-processed, fully-processed, superseded |
| artifact_ref | string | Filename of the original artifact in this folder |
| generated_reqs | list[string] | REQ-IDs (required when partially/fully-processed) |

## Sidecar body structure
```
# RAW-NNN: <artifact title>

## Source artifact
- File: `<artifact_ref>`
- Type: <schema | code | ...>
- Size: <lines / tables / endpoints>
- Original system: <name, version if known>

## Inventory
_(AI-built — structured reading of the artifact, each item cited to artifact line ranges)_

### Entities / tables / modules
...

### Fields / columns / parameters
...

### Constraints / business rules (observed)
...

### Integrations / external touchpoints
...

### Open questions for BA / client
- [TBD] ...

## Change Log
- YYYY-MM-DD: Artifact captured by <name>.
```

## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../` (parent raw-inputs — extraction flow)
- `../../requirements/` (REQs flow out)
- `../../design/` (migration design may reference inventory directly)

## Common questions
- **Where do I dump the old schema / codebase?** → here, keep original + create sidecar
- **Has this artifact been mined for REQs?** → sidecar frontmatter `status`
- **Which REQs came from the old system?** → sidecar `generated_reqs`

## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

_(empty)_
