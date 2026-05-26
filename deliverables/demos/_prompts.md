---
folder: demos
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Archive only. Heavy files — consider OneDrive link instead of binary in repo.
---

# Operations — demos/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Archive demo
- **Trigger phrases:** "archive sprint X demo"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Recording file + sprint
- **Output:** Filed with naming convention
- **Inline summary:** Drop file. Rename to `sprint-NN.mp4`. Add demo link to that sprint retro.

## OP-2: Link demo to retro
- **Trigger phrases:** "link demo to retro"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Demo file + retro path
- **Output:** Markdown link in retro.md
- **Inline summary:** Add link to `../../feedback/sprint-NN/retro.md` under 'Demo recording' heading.

## Forbidden in this folder
- Do NOT commit large unedited demo files — use OneDrive link in retro instead

## Escalate to human if
- Demo contains client-confidential content — check before sharing

## Related operations in other folders
- Retro → `../../feedback/sprint-NN/_prompts.md`
