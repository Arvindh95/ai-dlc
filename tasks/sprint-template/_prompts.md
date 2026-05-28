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

## OP-1: Sprint open
- **Trigger phrases:** "open sprint", "sprint kickoff"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Sprint dates + goals
- **Output:** Updated _index frontmatter + goals section
- **Inline summary:** Set dates, goals, planned REQs. Move chosen tasks here from backlog.

## OP-2: Sprint close
- **Trigger phrases:** "close sprint", "sprint review"
- **Canonical prompt:** _(inline only)_
- **Inputs:** none
- **Output:** Retro draft + carry-over list
- **Inline summary:** Tally done/not-done. Generate retro skeleton in `../../feedback/{{SPRINT_NN}}/retro.md`. Move incomplete tasks to next sprint.

## OP-3: Burndown
- **Trigger phrases:** "burndown", "sprint progress"
- **Canonical prompt:** _(inline only)_
- **Inputs:** none
- **Output:** Snapshot to dashboard
- **Inline summary:** Count tasks by status. Update `../../dashboard/dashboard.md` burndown query input.

## OP-4: Carry over
- **Trigger phrases:** "carry over to next sprint", "move task"
- **Canonical prompt:** _(inline only)_
- **Inputs:** TASK-ID + next sprint
- **Output:** Moved file + Change Log
- **Inline summary:** Move file to next sprint folder. Update sprint field in frontmatter. Append Change Log.

## Forbidden in this folder
- Do NOT close sprint without retro
- Do NOT silently move tasks across sprints — explicit carry-over only

## Escalate to human if
- Sprint goal cannot be met — replan, don't fudge
- Critical task blocked across sprint boundary

## Related operations in other folders
- Retro → `../../feedback/{{SPRINT_NN}}/_prompts.md`
