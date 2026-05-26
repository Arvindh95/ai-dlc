---
folder: design
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Design follows approved spec. Any architecture-level decision → new ADR.
---

# Operations — design/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Create design for spec
- **Trigger phrases:** "design for SPEC-X", "technical design for X"
- **Canonical prompt:** `../prompts/create-design.md`
- **Inputs:** Approved SPEC
- **Output:** <domain>-design.md
- **Inline summary:** Draft sections: components, data model, interfaces, sequence flows. Reference SPEC-ID.

## OP-2: Add ADR
- **Trigger phrases:** "new ADR", "record architecture decision"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Decision context + options + chosen
- **Output:** ADR file in `adrs/`
- **Inline summary:** Use `adrs/_prompts.md` OP draft-ADR. Link from this design doc.

## OP-3: API contract change
- **Trigger phrases:** "change API", "new endpoint"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Endpoint spec
- **Output:** Updated `api-contracts.md` + version bump
- **Inline summary:** Add/modify endpoint. Bump version. Notify code repo team.

## Forbidden in this folder
- Do NOT make architecture decisions without ADR
- Do NOT design for unapproved spec
- Do NOT delete design — set status=deprecated

## Escalate to human if
- Design implies spec change
- API change breaks existing consumer

## Related operations in other folders
- ADR → `adrs/_prompts.md`
- Tasks → `../tasks/_prompts.md`
