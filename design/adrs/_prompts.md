---
folder: adrs
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  ADRs are append-only. Never edit accepted ADRs — write a new one that supersedes.
---

# Operations — adrs/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Draft ADR
- **Trigger phrases:** "new ADR", "record decision"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Context, options considered, chosen, consequences
- **Output:** ADR-NNN-*.md with status=proposed
- **Inline summary:** Fill sections: Context, Decision, Consequences, Alternatives. status=proposed until team review.

## OP-2: Supersede ADR
- **Trigger phrases:** "supersede ADR-X", "ADR-X is outdated"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Old ADR-ID + new context
- **Output:** New ADR with `supersedes: ADR-X` + old ADR status flipped
- **Inline summary:** Write new ADR referencing old. Update old to status=superseded with link forward. Never delete.

## Forbidden in this folder
- Do NOT edit accepted/deprecated ADR body — write new one
- Do NOT renumber ADRs

## Escalate to human if
- Decision affects security or compliance — DPO/legal review first

## Related operations in other folders
- Cross-cutting non-architecture decision → `../../decisions/_prompts.md`
