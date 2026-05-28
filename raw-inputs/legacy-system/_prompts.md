---
folder: legacy-system
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../../prompts/
last_updated: 2026-05-28
ai_behavior_hint: |
  Two-step migration flow: capture artifact -> build inventory -> extract REQs.
  Never extract REQs straight from code/schema; always inventory first.
---

# Operations — legacy-system/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Capture legacy artifact
- **Trigger phrases:** "add legacy schema", "dump old codebase", "capture legacy API spec", "add source code"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Original artifact file(s) + type + original-system name
- **Output:** Original file kept as-is + sidecar `RAW-NNN-*.md` with status=unprocessed
- **Inline summary:** Place original artifact in this folder unchanged. Create sidecar MD: allocate RAW-NNN, set source_type (code/schema/api-spec/db-erd/ui-mockup/user-manual), artifact_ref=<filename>, status=unprocessed. Do NOT inline a large file into the MD — point to it via artifact_ref.

## OP-2: Build inventory (the migration-specific step)
- **Trigger phrases:** "build inventory for RAW-X", "inventory the schema", "reverse-engineer RAW-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** RAW-NNN sidecar + its artifact_ref file
- **Output:** Filled `## Inventory` section in the sidecar MD
- **Inline summary:** Read the original artifact. Fill the Inventory section: entities/tables/modules, fields/columns/parameters, observed constraints + business rules, integrations, and an "Open questions for BA/client" list. CITE artifact line ranges for every item (e.g. `schema.sql:120-145`). Mark inferences explicitly as `[inferred]` and ambiguities as `[TBD]`. Do NOT invent rules the artifact doesn't support. Keep status=unprocessed until REQs are extracted.

## OP-3: Extract REQs from inventory
- **Trigger phrases:** "extract REQs from RAW-X", "generate requirements from inventory"
- **Canonical prompt:** `../../prompts/ingest-raw-input.md`
- **Inputs:** RAW-NNN sidecar with a filled Inventory section
- **Output:** Draft REQ-NNN files via `../../requirements/_prompts.md` OP-1
- **Inline summary:** Hand the Inventory section to requirements OP-1. Each REQ cites BOTH the inventory item AND the original artifact line range. After extraction, update sidecar: status=partially/fully-processed + generated_reqs list.

## Forbidden in this folder
- Do NOT extract REQs directly from raw code/schema — inventory first (OP-2 before OP-3)
- Do NOT edit the original artifact — it is immutable source
- Do NOT inline large artifacts into the sidecar MD — reference via artifact_ref
- Do NOT invent business rules the artifact doesn't evidence — mark `[inferred]` / `[TBD]`

## Escalate to human if
- Artifact uses an undocumented/obfuscated convention the inventory can't interpret
- Legacy behaviour contradicts a stated new requirement — flag to BA for reconciliation
- Schema implies PII handling — flag to DPO (cross-check `../../00-overview/security.md`)
- Stored-proc / trigger logic is too complex to reverse safely — request original dev's notes

## Related operations in other folders
- REQ creation → `../../requirements/_prompts.md` OP-1
- Migration design → `../../design/_prompts.md` OP-1 (may cite inventory directly)
- Architecture decision on migration strategy → `../../design/adrs/_prompts.md`
