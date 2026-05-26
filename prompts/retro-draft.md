---
id: PROMPT-09
name: Draft sprint retro
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - feedback/sprint-NN/_prompts.md OP-1
---

# Prompt: Draft sprint retro

## Purpose
Generate a retrospective skeleton at sprint close from sprint stats, FBs, and task outcomes.

## Inputs
- Sprint number (sprint-NN)

## Output
- `feedback/sprint-NN/retro.md`

## Prompt body
```
You are drafting retro.md for sprint-NN.

1. Read tasks/sprint-NN/ — count tasks by status (done / blocked / carry-over).
2. Read feedback/sprint-NN/ — count FBs by type / severity / status.
3. Read tasks/sprint-NN/_index.md — sprint goals.

Create feedback/sprint-NN/retro.md:

# Retro — sprint-NN

## Sprint stats
| Metric | Value |
|--------|-------|
| Goals planned | <N> |
| Goals achieved | <N> |
| Tasks done | <N> |
| Tasks carry-over | <N> |
| FBs raised | <N> (<sev1>: <N>, <sev2>: <N>, ...) |
| FBs closed in-sprint | <N> |
| Incidents | <N> |
| Planned hours | <N> |
| Actual hours | <N> |

## What went well
- TBD — facilitator to fill from team input

## What went badly
- TBD

## Action items
| ID | Action | Owner | Due |
|----|--------|-------|-----|
| TBD | TBD | TBD | TBD |

## Metrics trend (vs prior sprints)
| Metric | sprint-N-2 | sprint-N-1 | sprint-NN |
|--------|------------|------------|-----------|
| Velocity (tasks done) | ... | ... | ... |
| Carry-over % | ... | ... | ... |
| Sev1 FBs | ... | ... | ... |

## Demo recording
- [sprint-NN.mp4](../../deliverables/demos/sprint-NN.mp4) _(or link to OneDrive if too large)_

## Change Log
- <today>: Drafted from sprint stats (auto). Facilitator to fill "What went well/badly" + action items.

Report: filled stats section + 3 sections marked TBD for human fill.
```

## Guardrails
- Never invent "what went well/badly" content — that's human input
- Stats must be derived from actual files, not estimated
- Action items must link to TASK / REQ / DEC IDs once filled
