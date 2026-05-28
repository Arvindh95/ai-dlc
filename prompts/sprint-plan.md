---
id: PROMPT-06
name: Plan a new sprint
version: 0.2.0
status: active
last_updated: 2026-05-28
used_by:
  - tasks/_prompts.md OP-1
---

# Prompt: Plan next sprint

## Purpose
Select REQs from backlog for the next sprint within team capacity, generate tasks, set sprint metadata.

## Inputs
- Sprint number (e.g., sprint-02)
- Sprint start/end dates
- Team capacity in hours (per dev × num devs × days × focus factor 0.6)
- Backlog priorities

## Output
- New `tasks/sprint-NN/` folder (copied from `tasks/sprint-template/`) with `_index.md` + `_prompts.md`
- New `feedback/sprint-NN/` folder (copied from `feedback/sprint-template/`) with `_index.md` + `_prompts.md`
- All `{{SPRINT_NN}}` tokens in the 4 copied files replaced with the actual sprint id
- Sprint goals + dates filled in `tasks/sprint-NN/_index.md`
- TASK files generated per chosen REQ

## Prompt body
```
You are planning sprint-NN.

1. Read tasks/backlog.md + tasks/_index.md to see candidate REQs.
2. Read 00-overview/teams.md to count devs.
3. Compute capacity:
   capacity_hours = num_devs × sprint_days × 6 × 0.6
4. Sort backlog REQs by priority (critical > high > medium > low) then by created date asc.
5. Walking down sorted backlog, run create-tasks-from-req for each REQ to estimate
   total hours. Add REQ to sprint if cumulative_hours + req_hours <= capacity_hours.
6. Stop when capacity reached or backlog exhausted.

Scaffold the sprint folders:
- Copy tasks/sprint-template/ → tasks/sprint-NN/
- Copy feedback/sprint-template/ → feedback/sprint-NN/
- In all 4 copied files, replace every {{SPRINT_NN}} token with the actual id (e.g. sprint-02),
  update folder: frontmatter + last_updated, and remove the "do NOT add real entries here" hint.

Then in tasks/sprint-NN/_index.md:
- Set sprint dates (derive from 00-overview/cadence.md sprint length if not given)
- Set sprint goals (one bullet per chosen REQ)
- Set planned REQs list

For each chosen REQ, call create-tasks-from-req with target sprint=sprint-NN.

Update tasks/backlog.md by removing chosen REQs.

Report: chosen REQs + total estimated hours + capacity remaining.
```

## Guardrails
- Never plan above capacity (focus factor 0.6, not 1.0)
- Never include a REQ with status != approved
- Never silently drop a backlog item — explicit defer or carry-over only
