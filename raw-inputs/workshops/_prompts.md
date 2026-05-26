---
folder: workshops
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Workshop transcripts-specific capture. Use parent for extraction flow.
---

# Operations — workshops/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Capture
- **Trigger phrases:** "add workshop"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Source content + date
- **Output:** RAW-NNN-*.md here
- **Inline summary:** File with date prefix. Set status=unprocessed.

## Forbidden in this folder
- Do NOT edit captured content

## Escalate to human if
- Conflicts with prior input

## Related operations in other folders
- Extract → `../_prompts.md` OP extract
