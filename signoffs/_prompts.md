---
folder: signoffs
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Archive only. Never delete.
---

# Operations — signoffs/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Archive signoff
- **Trigger phrases:** "archive signoff for REQ-X", "client emailed approval"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Evidence file + REQ/CR-ID + date
- **Output:** Filed with naming convention
- **Inline summary:** Drop file. Rename per convention. Reference from REQ/CR Change Log.

## OP-2: Cross-ref REQ
- **Trigger phrases:** "link signoff to REQ"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Evidence filename + REQ-ID
- **Output:** Updated REQ Change Log
- **Inline summary:** Append to REQ Change Log: `signoff archived at signoffs/<filename>`.

## Forbidden in this folder
- Do NOT delete evidence
- Do NOT modify evidence after archival

## Escalate to human if
- Evidence unclear or unsigned
- Approver lacks authority

## Related operations in other folders
- REQ approval → `../requirements/_prompts.md` OP approve
- CR approval → `../change-requests/_prompts.md` OP approve
