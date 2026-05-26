---
folder: 00-overview
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Edits here change project-wide rules. Always escalate before changing teams, security, or ai-config.
---

# Operations — 00-overview/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Update vision/scope
- **Trigger phrases:** "update vision", "scope changed"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Stakeholder decision (link from `../decisions/`)
- **Output:** Edited vision.md / scope.md + DEC reference
- **Inline summary:** Append change to Change Log section, never overwrite history. Link DEC-ID.

## OP-2: Add/remove team member
- **Trigger phrases:** "new dev joining", "X left"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Name, role, REQ-ID range
- **Output:** Edited teams.md
- **Inline summary:** Update teams.md + CODEOWNERS (in code repo). Notify PM.

## OP-3: Change Claude model pin
- **Trigger phrases:** "upgrade Claude", "change model"
- **Canonical prompt:** _(inline only)_
- **Inputs:** New model ID + justification
- **Output:** Edited ai-config.md + DEC entry
- **Inline summary:** Only after DEC entry recorded. Note migration plan for in-flight prompts.

## Forbidden in this folder
- Do NOT change security classification without DPO approval
- Do NOT remove a team member while they own open REQs/TASKs
- Do NOT modify auto-managed region of `_index.md`

## Escalate to human if
- Vision/scope change without client signoff
- Security reclassification (data → PDPA-sensitive)
- Model change mid-sprint

## Related operations in other folders
- Record decision → `../decisions/_prompts.md` OP draft-DEC
- Update CODEOWNERS → code repo
