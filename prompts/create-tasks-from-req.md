---
id: PROMPT-07
name: Break a REQ into tasks
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - tasks/_prompts.md OP-2
---

# Prompt: Generate implementation tasks from a REQ

## Purpose
Break one approved REQ into 3-8 implementation tasks with estimates.

## Inputs
- REQ-ID
- Target sprint (sprint-NN)

## Output
- TASK files in `tasks/sprint-NN/TASK-NNN-*.md`
- REQ frontmatter `tasks` list updated

## Prompt body
```
You are breaking REQ-NNN into tasks for sprint-NN.

1. Read REQ-NNN in full.
2. Read its spec (frontmatter spec_ref) and design (design_ref) if linked.

Generate 3-8 tasks. Typical breakdown for a CRUD-style REQ:
- TASK-A: data model + migration
- TASK-B: backend service / handler
- TASK-C: API endpoint(s)
- TASK-D: frontend component
- TASK-E: tests (unit + integration)
- TASK-F: docs / KRISA section fill

For each task, create tasks/sprint-NN/TASK-NNN-*.md with:
- Frontmatter:
    id: TASK-NNN          # next available number in tasks/
    title: <verb-led title, e.g., "Implement TOTP verify endpoint">
    status: todo
    team: <REQ.team>
    req_ref: REQ-NNN
    sprint: sprint-NN
    estimate_hours: <number — see estimation rules below>
    last_updated: <today>
- Body:
    # TASK-NNN — <title>
    ## REQ link
    REQ-NNN — <REQ title>
    ## Description
    <what to implement, scoped to this task only>
    ## Acceptance
    <how we'll know it's done — usually matches REQ AC partition>
    ## Dependencies
    - TASK-NNN (if blocked by another task in same sprint)
    ## Change Log
    - <today>: Created from REQ-NNN.

Estimation rules:
- Use hours, not story points (Censof convention)
- Round to nearest 2h, max 16h per task — split larger
- Add 30% buffer for unknowns (don't show as separate task)

Update REQ-NNN frontmatter:
- tasks: [TASK-NNN, TASK-MMM, ...]
- last_updated: <today>
- Append Change Log entry on REQ

Do NOT assign tasks here — assignment is a separate OP.
```

## Guardrails
- Every task has req_ref
- No task > 16h — split it
- Total hours per REQ should match REQ.estimate_days × 6 ± 20%; flag if not
