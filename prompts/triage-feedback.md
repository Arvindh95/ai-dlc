---
id: PROMPT-08
name: Triage feedback INBOX
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - feedback/_prompts.md OP-1
---

# Prompt: Triage feedback INBOX

## Purpose
Convert raw INBOX entries into structured FB-NNN files in the correct sprint folder, classified and routed.

## Inputs
- `feedback/INBOX.md` entries

## Output
- FB files in `feedback/sprint-NN/`
- INBOX entries marked processed (or removed once filed)

## Prompt body
```
You are triaging feedback/INBOX.md.

For each unprocessed entry (date-prefixed block):

1. Determine current sprint from root _index.md frontmatter (current_sprint).

2. Classify:
   - type: bug | change-request | clarification | enhancement
   - severity: critical | high | medium | low
   - source: demo | UAT | email | call | internal

3. Identify related REQ-ID if possible (grep description for REQ-NNN or match by feature name).

4. Create feedback/sprint-NN/FB-NNN-short-kebab-title.md:
   - Frontmatter:
       id: FB-NNN          # next available in feedback/
       sprint_raised: sprint-NN
       source: <enum>
       type: <enum>
       severity: <enum>
       status: triaged
       related_req: <REQ-NNN or null>
       raised_date: <date from INBOX entry>
   - Body:
       # FB-NNN — <title>
       ## Description
       <verbatim from INBOX>
       ## Reproduction steps (BA verified)
       <if bug>
       ## Triage classification
       - Type: <type>
       - Severity: <severity>
       - Decision: <accept | reject | defer | duplicate of FB-NNN>
       ## Resolution
       <to be filled when status changes>
       ## Related
       - REQ: <REQ-NNN>
       ## Change Log
       - <today>: Triaged from INBOX.

5. Route decision (do NOT execute the route, just record it):
   - bug touching active REQ → "patch REQ + create TASK" (record in Triage section)
   - scope change → "draft CR in change-requests/"
   - clarification → "REQ edit only"
   - cosmetic → "add to backlog"

6. After filing all entries, replace processed INBOX entries with:
   `<original date>: Triaged → FB-NNN, FB-MMM. [removed from INBOX]`

Report: count by type + severity + open routing actions.
```

## Guardrails
- Never delete an INBOX entry without filing as FB
- Never silently auto-execute a route — record decision, let BA confirm
- Sev1 (critical severity) → escalate to PM immediately
