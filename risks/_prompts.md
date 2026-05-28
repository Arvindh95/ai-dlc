---
folder: risks
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-28
ai_behavior_hint: |
  Append-only register. Status transitions via Change Log. Never delete a closed risk.
---

# Operations — risks/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Add risk
- **Trigger phrases:** "add risk", "log risk", "new RISK", "seed risks at kickoff"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Title + description + likelihood + impact + owner + mitigation
- **Output:** RISK-NNN-*.md with status=open
- **Inline summary:** Allocate next RISK-NNN. Fill frontmatter + body (Description, Trigger, Mitigation, Contingency). Set raised_date=today. Append `- {today}: Raised by <name>` to Change Log.

## OP-2: Update status
- **Trigger phrases:** "update RISK-X", "mitigate RISK-X", "close RISK-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** RISK-ID + new status + reason
- **Output:** Updated frontmatter + Change Log
- **Inline summary:** Valid transitions: open → mitigated → closed. Or open → accepted. Or open → materialised (must provide linked_inc=INC-NNN). Never edit body of older entries — append Change Log.

## OP-3: Escalate
- **Trigger phrases:** "escalate RISK-X", "raise RISK-X to Sponsor"
- **Canonical prompt:** _(inline only)_
- **Inputs:** RISK-ID + reason
- **Output:** Change Log entry + flag in `../dashboard/dashboard.md` for steering
- **Inline summary:** For sev (high/high) or status=open beyond agreed window. Append `- {today}: Escalated to Sponsor — <reason>` to Change Log. Add to dashboard steering queue.

## OP-4: Link to incident (materialised)
- **Trigger phrases:** "RISK-X materialised", "link RISK-X to INC-Y"
- **Canonical prompt:** _(inline only)_
- **Inputs:** RISK-ID + INC-ID
- **Output:** Updated frontmatter status=materialised, linked_inc=INC-ID + Change Log
- **Inline summary:** Confirm INC exists in `../incidents/`. Set status=materialised, linked_inc. Append Change Log on BOTH the RISK and the INC referencing each other.

## OP-5: Seed at kickoff
- **Trigger phrases:** "seed risks", "kickoff risk register", "top 3-5 risks"
- **Canonical prompt:** _(inline only)_
- **Inputs:** 3-5 risk titles + impact assessment from user
- **Output:** 3-5 RISK-NNN-*.md files via OP-1
- **Inline summary:** Loop OP-1 for each. Allocate sequential IDs starting RISK-001. Do NOT invent risks — only what user states.

## Forbidden in this folder
- Do NOT delete a risk — set status=closed instead
- Do NOT renumber RISK-IDs
- Do NOT edit body of an older RISK retroactively — append Change Log
- Do NOT invent risks the user didn't state
- Do NOT mark status=materialised without a linked_inc in `../incidents/`

## Escalate to human if
- Materialised risk + no INC exists yet — create INC first via `../incidents/_prompts.md`
- Risk requires legal/compliance review (data, contract) — DPO + Account Manager
- Cumulative risk exposure threatens contract delivery — Sponsor escalation

## Related operations in other folders
- Incident from materialised risk → `../incidents/_prompts.md`
- Risk surfaced from feedback → `../feedback/_prompts.md` OP-3 (route)
- Risk from CR impact analysis → `../change-requests/_prompts.md`
