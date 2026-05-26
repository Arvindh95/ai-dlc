---
folder: spec
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Specs trace back to approved REQs only. Never spec a draft REQ.
---

# Operations — spec/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Create spec for REQ
- **Trigger phrases:** "create spec for REQ-X", "elaborate REQ-X"
- **Canonical prompt:** `../prompts/create-spec.md`
- **Inputs:** Approved REQ-ID
- **Output:** <domain>-spec.md with covers_req updated
- **Inline summary:** Verify REQ.status == approved. Draft spec sections. Update `covers_req`. Set status=draft, version=0.1.0.

## OP-2: Refine spec
- **Trigger phrases:** "refine spec", "spec is unclear"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Spec file + feedback
- **Output:** Updated spec + version bump
- **Inline summary:** Edit specific section. Bump patch version. Append Change Log.

## OP-3: Version bump
- **Trigger phrases:** "bump spec version", "spec breaking change"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Spec file + bump type
- **Output:** Updated version field + Change Log
- **Inline summary:** patch=clarification, minor=additive, major=breaking. Notify dependent design docs.

## Forbidden in this folder
- Do NOT spec a draft/unapproved REQ
- Do NOT mark spec approved without tech-lead review
- Do NOT delete a spec — set status=deprecated

## Escalate to human if
- Spec contradicts the REQ it covers
- Multiple specs claim same REQ-ID coverage

## Related operations in other folders
- Design from spec → `../design/_prompts.md`
- Tasks from spec → `../tasks/_prompts.md`
