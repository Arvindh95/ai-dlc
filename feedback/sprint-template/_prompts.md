---
folder: sprint-template
purpose_of_this_file: Template ops file — copy to sprint-NN/ with {{SPRINT_NN}} substituted
canonical_prompts_location: ../../prompts/
last_updated: 2026-05-28
ai_behavior_hint: |
  Template — do not execute ops here. Copy this folder to sprint-NN/ first.
---

# Operations — {{SPRINT_NN}}/

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
- Sprint close → `../../tasks/{{SPRINT_NN}}/_prompts.md`
