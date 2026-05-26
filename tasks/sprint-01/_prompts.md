---
folder: sprint-01
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Sprint-scoped operations only. Cross-sprint moves use parent tasks/_prompts.md.
---

# Operations — sprint-01/

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
- **Inline summary:** Tally done/not-done. Generate retro skeleton in `../../feedback/sprint-01/retro.md`. Move incomplete tasks to next sprint.

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
- Retro → `../../feedback/sprint-01/_prompts.md`
