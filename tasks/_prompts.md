---
folder: tasks
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Tasks always trace to a REQ. Open the sprint subfolder for sprint-specific ops.
---

# Operations — tasks/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Sprint plan
- **Trigger phrases:** "plan sprint", "sprint kickoff"
- **Canonical prompt:** `../prompts/sprint-plan.md`
- **Inputs:** Backlog + capacity
- **Output:** New `sprint-NN/` folder with TASK MDs
- **Inline summary:** Select REQs from backlog within capacity. Generate tasks per REQ (use create-tasks-from-REQ). Create sprint folder.

## OP-2: Create tasks from REQ
- **Trigger phrases:** "break REQ-X into tasks"
- **Canonical prompt:** `../prompts/create-tasks-from-req.md`
- **Inputs:** REQ-ID + sprint folder
- **Output:** TASK-NNN-*.md files
- **Inline summary:** Read REQ + spec. Generate 3-8 tasks. Estimate hours. Set status=todo. Reference req_ref.

## OP-3: Assign task
- **Trigger phrases:** "assign TASK-X to Y"
- **Canonical prompt:** _(inline only)_
- **Inputs:** TASK-ID + assignee
- **Output:** Updated frontmatter
- **Inline summary:** Set assignee, status=in-progress if started today.

## Forbidden in this folder
- Do NOT create tasks without a REQ ref
- Do NOT delete tasks — set status=blocked or move to next sprint with explicit carry-over

## Escalate to human if
- Capacity exceeded but stakeholder demands more
- Task requires undefined dependency

## Related operations in other folders
- Sprint lifecycle → `sprint-NN/_prompts.md`
