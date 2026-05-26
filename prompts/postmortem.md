---
id: PROMPT-10
name: Draft incident postmortem
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - incidents/_prompts.md OP-1
---

# Prompt: Draft postmortem for incident

## Purpose
Generate a blameless postmortem from incident timeline + logs.

## Inputs
- INC-ID
- Timeline events + redacted logs

## Output
- Updated `incidents/INC-NNN-*.md` with full postmortem body

## Prompt body
```
You are writing the postmortem for INC-NNN.

Required input: timeline (chronological events with timestamps) + redacted logs.

If logs are unredacted, REFUSE and direct user to infra/redact-logs.sh first.

Generate the postmortem body (replace any existing draft body):

# INC-NNN — <title>

## Summary
<2-3 sentences: what broke, who was affected, how long, how resolved>

## Severity
- Classification: <sev1 | sev2 | sev3>
- Customer impact: <users affected, duration>
- Data loss: <yes/no>
- Data breach: <yes/no — if yes, DPO already engaged>

## Timeline (UTC)
| Time | Event | Source |
|------|-------|--------|
| HH:MM | <event> | <log/alert/human> |
| ...  | ...   | ...    |

## Root cause
<the ONE primary cause, plain language>

## Contributing factors
- <factor 1 — system condition that allowed the failure>
- <factor 2>

## What went well
- <detection time was good, etc.>

## What went badly
- <missing runbook, etc.>

## Action items
| ID | Action | Owner role | Due | Linked TASK |
|----|--------|------------|-----|-------------|
| 1  | ...    | Tech Lead  | <date> | TASK-NNN |

## Lessons learnt
<1-2 sentences that future-you would want to know>

## Change Log
- <today>: Postmortem completed.

Blameless rule: describe roles and system states, never name individuals in blame
terms ("Tech Lead deployed at 14:02" is fine; "<Person> caused the outage" is not).

Update frontmatter: status = "resolved" (if mitigation done + action items filed)
or "postmortem-pending" (if still open).
```

## Guardrails
- Never accept unredacted logs — require redaction first
- Never name individuals in blame terms
- Sev1/sev2 require ALL sections filled before status=closed
- Action items must be concrete + dated + linked to TASK
