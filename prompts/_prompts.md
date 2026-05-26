---
folder: prompts
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Prompts are versioned. Bump version on any wording change. Never delete — deprecate.
---

# Operations — prompts/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Add new prompt
- **Trigger phrases:** "add prompt for X", "new prompt"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Op name + use case
- **Output:** <op-name>.md with status=draft v0.1.0
- **Inline summary:** Fill: purpose, inputs, output schema, prompt body. Add CHANGELOG entry.

## OP-2: Version bump
- **Trigger phrases:** "bump prompt X", "improve prompt X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Prompt file + change
- **Output:** Updated version + CHANGELOG entry
- **Inline summary:** patch=wording, minor=new input/output, major=behavior change. Update used_by callers if breaking.

## OP-3: Deprecate prompt
- **Trigger phrases:** "deprecate prompt X"
- **Canonical prompt:** _(inline only)_
- **Inputs:** Prompt-ID
- **Output:** status=deprecated
- **Inline summary:** Set status. Add reason. Add successor link if any.

## Forbidden in this folder
- Do NOT delete prompts — deprecate
- Do NOT edit active prompt without version bump

## Escalate to human if
- Prompt produces wrong/dangerous output — pull to draft immediately

## Related operations in other folders
- Folder ops that call prompts → respective `_prompts.md`
