---
folder: queries
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Queries are pure Dataview. Test in Obsidian before commit.
---

# Operations — queries/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Add query
- **Trigger phrases:** "add query for X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Name + intent
- **Output:** <query-name>.md
- **Inline summary:** Write Dataview block. Test in Obsidian. Link from parent dashboard file.

## OP-2: Fix query
- **Trigger phrases:** "query X is wrong"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Query name + symptom
- **Output:** Updated Dataview block
- **Inline summary:** Debug schema mismatch (frontmatter field name/type). Update query.

## Forbidden in this folder
- Do NOT inline complex queries in dashboard pages — extract here

## Escalate to human if
- Query requires data not in any frontmatter — propose schema change

## Related operations in other folders
- Dashboard → `../_prompts.md`
