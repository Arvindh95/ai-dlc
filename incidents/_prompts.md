---
folder: incidents
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Speed > polish during incident. Postmortem is the deliverable, not the file content during the fire.
---

# Operations — incidents/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Postmortem draft
- **Trigger phrases:** "draft postmortem for INC-X"
- **Canonical prompt:** `../prompts/postmortem.md`
- **Inputs:** Incident timeline + logs
- **Output:** INC-NNN-*.md sections: timeline, root cause, contributing factors, action items
- **Inline summary:** Blameless. Focus on system, not people. Action items linked to TASK-IDs.

## OP-2: Runbook update
- **Trigger phrases:** "update runbook from INC-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** INC findings
- **Output:** Updated runbook in code repo `infra/runbooks/`
- **Inline summary:** If incident exposed missing/wrong runbook step, push fix to code repo runbook.

## Forbidden in this folder
- Do NOT name individuals in blame terms — describe role/action
- Do NOT close INC without postmortem (sev1/sev2)

## Escalate to human if
- Data loss or data breach — DPO + legal immediately
- Customer-facing outage > SLA

## Related operations in other folders
- Runbooks in code repo `infra/runbooks/`
