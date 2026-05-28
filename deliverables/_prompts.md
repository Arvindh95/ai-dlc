---
folder: deliverables
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Use Claude-in-Word with M365 connector exposing this repo. Always cite source MDs.
---

# Operations — deliverables/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Fill KRISA section
- **Trigger phrases:** "fill D01 section X", "regenerate KRISA D02 section Y"
- **Canonical prompt:** `../prompts/fill-srs-section.md`
- **Inputs:** KRISA doc + section heading + source REQ-IDs
- **Output:** Filled section + hidden source comment + footer hash
- **Inline summary:** Read cited REQs/spec/design. Fill section per template style. Insert `<!-- REQ: REQ-XXX -->` hidden comment per section.

## OP-2: Consistency check
- **Trigger phrases:** "check KRISA consistency"
- **Canonical prompt:** `../prompts/krisa-consistency.md`
- **Inputs:** Docx + source MDs
- **Output:** Discrepancy report
- **Inline summary:** Compare cited MDs vs filled section. Flag drift.

## OP-3: Regen on source change
- **Trigger phrases:** "regenerate KRISA after REQ change"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Changed REQ-ID + affected D-docs
- **Output:** Updated sections + new footer hash
- **Inline summary:** [PLANNED v1.2 automation; today: manual] Re-fill sections that cite changed REQ-ID. Update footer hash.

## Forbidden in this folder
- Do NOT fill KRISA from a draft (unapproved) REQ
- Do NOT manually edit a filled section — re-run the fill prompt
- Do NOT remove the source-citation comments or footer hash

## Escalate to human if
- Source MD insufficient to fill mandatory section
- Client requests text not derivable from source

## Related operations in other folders
- Templates → `templates/_prompts.md`
- Demos → `demos/_prompts.md`
