---
id: PROMPT-00
name: Kickoff template instantiation
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - ROOT/_prompts.md OP-0
---

# Prompt: Kickoff — instantiate template for new project

## Purpose
Walk the user through `KICKOFF.md` step-by-step to convert this template scaffold into a project-ready repo. Drive the conversation; never skip a step; refuse to do downstream work until kickoff is complete.

## Inputs
- Read `KICKOFF.md` first
- Ask the user for: project_id, client name, contract start/end dates, PM/BA Lead/Tech Lead names, sponsor + business owner contacts

## Output
- Edited `_index.md` (root) frontmatter — project_id, client, contract_start, contract_end
- Filled `00-overview/teams.md` with real names
- Filled `00-overview/stakeholders.md` with at least Sponsor + Business Owner rows
- Asked the user for vision text and filled `00-overview/vision.md`
- Asked for scope items and filled `00-overview/scope.md` in-scope/out-of-scope
- Asked for DPO contact and filled `00-overview/security.md`

## Prompt body
```
You are running the kickoff for a new project that's instantiating this AI-DLC template.

Read KICKOFF.md first. Then walk the user through steps 2-5 in order:
1. Ask for project_id and client name. Edit root _index.md frontmatter.
2. Ask for contract_start and contract_end (ISO dates). Edit frontmatter.
3. Ask for PM, BA Lead, Tech Lead names. Edit 00-overview/teams.md.
4. Ask for Sponsor + Business Owner (name + email). Edit stakeholders.md.
5. Ask for one-paragraph vision. Edit vision.md (replace example block).
6. Ask "in scope (3-5 items)" + "out of scope (3-5 items)". Edit scope.md.
7. Ask for DPO contact. Edit security.md.

After each edit, do NOT continue to the next step until the user confirms.

Run `python scripts/regen_indexes.py .` after each edit batch to ensure validators still pass.

Finally, run a search for "TBD-set-at-kickoff" and report any remaining matches. If
any remain (other than KICKOFF.md itself), tell the user the kickoff is incomplete.
```

## Guardrails
- Refuse to run any other operation (REQ creation, sprint planning, etc.) while project_id == "TBD-set-at-kickoff"
- Never invent stakeholder names or contact info
- Never set contract dates without explicit user input
- Append `- {today}: Kickoff completed by <PM name>` to each filled file's Change Log
