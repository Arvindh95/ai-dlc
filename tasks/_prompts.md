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
- **Inputs:** Backlog + capacity + next sprint number (NN)
- **Output:** New `sprint-NN/` folder (tasks side) + `../feedback/sprint-NN/` folder (feedback side), both with `_index.md` + `_prompts.md` cloned from templates and TASK MDs filed
- **Inline summary:**
  1. Copy `sprint-template/` → `sprint-NN/` (tasks side).
  2. Copy `../feedback/sprint-template/` → `../feedback/sprint-NN/` (feedback side).
  3. In all four copied files, replace every `{{SPRINT_NN}}` token with the actual sprint id (e.g. `sprint-02`). Update `folder:` frontmatter, `last_updated:`, and remove the "do NOT add real entries here" hint in `ai_navigation_hint`.
  4. Set sprint goal + start/end dates in the new `sprint-NN/_index.md` (use `00-overview/cadence.md` for length).
  5. Select REQs from backlog within capacity. Generate tasks per REQ via OP-2 (create-tasks-from-REQ). File TASK MDs in `sprint-NN/`.
  6. Run `python scripts/regen_indexes.py .` — confirm both new folders pass Tier A check.

## OP-2: Create tasks from REQ
- **Trigger phrases:** "break REQ-X into tasks"
- **Canonical prompt:** `../prompts/create-tasks-from-req.md`
- **Inputs:** REQ-ID + its spec + its design doc + sprint folder
- **Output:** TASK-NNN-*.md files
- **Inline summary:** Read REQ + spec + **the relevant design doc** (components, interfaces, data model, sequence flows) — the design is where the actual work breakdown lives. Generate 3-8 tasks reflecting the design's technical units. Estimate hours. Set status=todo. Set `req_ref` (mandatory) and `design_ref` (the design doc the task implements; omit only for non-design tasks like spikes/infra). If no approved design exists for the REQ's domain, escalate — do not invent the breakdown.

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
