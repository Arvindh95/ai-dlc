---
folder: feedback
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Triage INBOX before sprint close. Route to REQ-edit / CR / TASK / reject.
---

# Operations — feedback/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Triage INBOX
- **Trigger phrases:** "triage feedback", "process INBOX"
- **Canonical prompt:** `../prompts/triage-feedback.md`
- **Inputs:** INBOX.md
- **Output:** FB-NNN-*.md files in current sprint subfolder
- **Inline summary:** For each entry: classify (bug/CR/clarification/enhancement), set severity, link related REQ. Move out of INBOX once filed.

## OP-2: Classify
- **Trigger phrases:** "classify FB-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** FB file
- **Output:** Updated frontmatter type+severity
- **Inline summary:** Pick from enum. If CR candidate, escalate to change-requests.

## OP-3: Route
- **Trigger phrases:** "route FB-X to REQ-edit / CR / TASK / reject"
- **Canonical prompt:** _(inline only)_
- **Inputs:** FB-ID + destination
- **Output:** Linked record + FB status update
- **Inline summary:** Bug touching active REQ → patch REQ + create TASK. Scope change → draft CR. Clarification → REQ edit only. Cosmetic → backlog.

## OP-4: Escalate
- **Trigger phrases:** "escalate FB-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** FB-ID + reason
- **Output:** Comment chain in FB file + Slack ping to PM/BA
- **Inline summary:** Append escalation note with reason. Notify PM.

## Forbidden in this folder
- Do NOT delete INBOX entries — file them, don't trash them
- Do NOT silently auto-accept feedback as scope — route through CR if scope-changing

## Escalate to human if
- Scope-changing feedback without CR
- Severity sev1 — escalate immediately

## Related operations in other folders
- Sprint retro → `sprint-NN/_prompts.md`
- CR → `../change-requests/_prompts.md`
