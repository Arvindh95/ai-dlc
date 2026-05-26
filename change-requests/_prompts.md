---
folder: change-requests
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  CRs are the only path to change an approved REQ. Never edit approved REQ silently.
---

# Operations — change-requests/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Draft CR
- **Trigger phrases:** "draft CR", "raise change request"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Source feedback + affected REQ-IDs
- **Output:** CR-NNN-*.md with status=under-review
- **Inline summary:** Fill Description, Justification (from client), Impact analysis (BA+TL), affects_req.

## OP-2: Approve CR
- **Trigger phrases:** "approve CR-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** CR-ID + signoff evidence
- **Output:** Updated CR + REQ revision
- **Inline summary:** Set status=approved. Revise affected REQs (status=late-change). Append Change Log to REQ + CR.

## OP-3: Reject CR
- **Trigger phrases:** "reject CR-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** CR-ID + reason
- **Output:** Updated CR status
- **Inline summary:** Set status=rejected. Document reason.

## OP-4: Link to REQ revision
- **Trigger phrases:** "CR-X done, update REQ-Y"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Approved CR-ID
- **Output:** REQ frontmatter status=late-change + Change Log
- **Inline summary:** On affected REQs: set status=late-change, append Change Log citing CR-ID.

## Forbidden in this folder
- Do NOT approve CR without client signoff
- Do NOT edit approved REQ outside CR flow

## Escalate to human if
- CR impacts schedule beyond contract end
- CR impacts budget

## Related operations in other folders
- REQ revision → `../requirements/_prompts.md`
- Decision log → `../decisions/_prompts.md`
