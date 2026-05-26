---
folder: dashboard
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Dashboard is generated. Edit queries, not output. Refresh via Obsidian.
---

# Operations — dashboard/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Refresh
- **Trigger phrases:** "refresh dashboard"
- **Canonical prompt:** _(inline only)_
- **Inputs:** none
- **Output:** Re-rendered Dataview blocks
- **Inline summary:** Tell user to open Obsidian and trigger Dataview refresh (Ctrl+P → Dataview: Refresh).

## OP-2: HTML export
- **Trigger phrases:** "export dashboard for client"
- **Canonical prompt:** _(inline only)_
- **Inputs:** none
- **Output:** `exports/index.html`
- **Inline summary:** Render Markdown → HTML (Pandoc). Strip internal-only sections. Write to exports/.

## OP-3: Weekly status PDF
- **Trigger phrases:** "weekly status"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Week range
- **Output:** PDF in `../deliverables/`
- **Inline summary:** Fill `../deliverables/templates/weekly-status.docx` from dashboard snapshot. Export PDF.

## OP-4: Ops summary
- **Trigger phrases:** "daily ops summary"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Logs (redacted)
- **Output:** `ops-daily.md`
- **Inline summary:** Claude reads redacted logs, summarises errors/latency/incidents. Write to ops-daily.md.

## Forbidden in this folder
- Do NOT hand-edit auto-generated output blocks
- Do NOT include unredacted logs in any export

## Escalate to human if
- Dashboard health-score < threshold
- ops-summary detects sev1 signal

## Related operations in other folders
- Queries → `queries/_prompts.md`
