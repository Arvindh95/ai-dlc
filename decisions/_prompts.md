---
folder: decisions
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  DECs are append-only. Supersede, never edit.
---

# Operations — decisions/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Draft DEC
- **Trigger phrases:** "record decision", "draft DEC"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Context + options + chosen + participants
- **Output:** DEC-NNN-*.md status=pending or decided
- **Inline summary:** Fill Context, Options, Decision, Consequences. List participants.

## OP-2: Supersede DEC
- **Trigger phrases:** "supersede DEC-X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Old DEC-ID + new context
- **Output:** New DEC + old status flipped
- **Inline summary:** Write new DEC referencing old. Set old status=superseded.

## Forbidden in this folder
- Do NOT edit decided/superseded DEC body
- Do NOT renumber

## Escalate to human if
- Decision conflicts with active ADR
- Decision implies policy/legal review

## Related operations in other folders
- ADR (architecture) → `../design/adrs/_prompts.md`
