---
folder: raw-inputs
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Captured inputs, not edited. Status tracks processing. Never delete — supersede.
---

# Operations — raw-inputs/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Capture
- **Trigger phrases:** "add workshop transcript", "log client email"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Source content + type + date
- **Output:** RAW-NNN-*.md in correct subfolder
- **Inline summary:** File under workshops/ / client-emails/ / client-docs/. Set status=unprocessed.

## OP-2: Transcribe
- **Trigger phrases:** "transcribe call", "transcribe meeting"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Audio/video file
- **Output:** Transcript MD in workshops/
- **Inline summary:** Run transcription. File MD. Set captured_by + source_date.

## OP-3: Extract
- **Trigger phrases:** "extract REQs from RAW-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** RAW-ID
- **Output:** REQ files via requirements/_prompts.md OP-1
- **Inline summary:** Hand off to requirements/_prompts.md OP-1 (create-from-raw). Update generated_reqs.

## OP-4: Mark processed
- **Trigger phrases:** "mark RAW-X processed"
- **Canonical prompt:** _(inline only)_
- **Inputs:** RAW-ID + generated REQ-IDs
- **Output:** Updated frontmatter
- **Inline summary:** Set status=partially/fully-processed + generated_reqs list.

## OP-5: Build inventory from legacy artifact (migration projects)
- **Trigger phrases:** "build inventory for RAW-X", "reverse-engineer schema", "inventory the codebase"
- **Canonical prompt:** _(inline only)_ — see `legacy-system/_prompts.md` OP-2
- **Inputs:** Legacy artifact (code, SQL schema, API spec, ERD) in `legacy-system/`
- **Output:** Filled Inventory section in the artifact's sidecar MD
- **Inline summary:** For source code / schema / API specs, do NOT extract REQs directly. Two-step: capture artifact in `legacy-system/` (OP-1 there) → build inventory (OP-2 there, cite line ranges) → THEN extract REQs from the inventory (OP-3 there → requirements OP-1). Preserves REQ → inventory → artifact traceability.

## Forbidden in this folder
- Do NOT edit captured content — append metadata only
- Do NOT delete — set status=superseded with successor link

## Escalate to human if
- Captured input conflicts with prior input — flag for BA reconciliation

## Related operations in other folders
- REQ creation → `../requirements/_prompts.md` OP-1
