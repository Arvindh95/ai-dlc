---
folder: templates
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Don't fill templates in place — copy out to parent `deliverables/` first.
---

# Operations — templates/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Use template
- **Trigger phrases:** "start D01 from template", "new weekly status"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Template name + target file name
- **Output:** Copy in `deliverables/`
- **Inline summary:** Copy template to `../<target>.docx`. Then run fill ops in parent folder.

## OP-2: Add new template
- **Trigger phrases:** "add KRISA D19 template"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Template file
- **Output:** Added file + catalog update
- **Inline summary:** Drop file here. CI regen catalog on next PR.

## Forbidden in this folder
- Do NOT fill templates in place
- Do NOT modify a template after a project starts using it (version it instead)

## Escalate to human if
- Template change breaks existing filled docs

## Related operations in other folders
- Fill flow → `../_prompts.md`
