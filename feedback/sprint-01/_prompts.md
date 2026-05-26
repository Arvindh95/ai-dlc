---
folder: sprint-01
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Sprint-scoped feedback ops. Cross-sprint analysis lives in parent.
---

# Operations — sprint-01/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Retro draft
- **Trigger phrases:** "draft retro", "sprint retro"
- **Canonical prompt:** `../../prompts/retro-draft.md`
- **Inputs:** Sprint stats + FBs + tasks status
- **Output:** `retro.md`
- **Inline summary:** Skeleton: stats, what-went-well, what-went-badly, action-items, metrics trend.

## OP-2: Feedback metrics
- **Trigger phrases:** "feedback metrics", "FB summary"
- **Canonical prompt:** _(inline only)_
- **Inputs:** All FBs this sprint
- **Output:** Snapshot for dashboard
- **Inline summary:** Count by type, severity, status. Compute time-to-triage. Write to dashboard input.

## Forbidden in this folder
- Do NOT cherry-pick FBs for retro — include all

## Escalate to human if
- Retro reveals systemic issue (>3 FBs same root cause)

## Related operations in other folders
- Sprint close → `../../tasks/sprint-01/_prompts.md`
