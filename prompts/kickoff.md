---
id: PROMPT-00
name: Kickoff template instantiation
version: 0.5.0
status: active
last_updated: 2026-05-28
used_by:
  - ROOT/_prompts.md OP-0
---

# Prompt: Kickoff — instantiate template for new project

## Purpose
Walk the user through `KICKOFF.md` step-by-step to convert this template scaffold into a project-ready repo. Drive the conversation; never skip a step; refuse to do downstream work until kickoff is complete. Every item in the `KICKOFF.md` "Definition of Done" must be covered.

## Inputs
- Read `KICKOFF.md` first
- Ask the user for: project_id, client name, contract start/end dates, PM / BA Lead / Tech Lead / Devs names, all 5 stakeholder rows (Sponsor, Business Owner, IT Lead, DPO, Account Manager) with approver-of, comms channels (chat, doc share, status email, incident pager), vision, scope (in/out/assumptions/constraints), security (data classification + compliance), tech (code repo URL + stack + envs), cadence (sprint length + working week + ceremonies + client reporting), sprint-01 goal, 3-5 seed risks, KRISA contract requirement

## Output
- Edited `_index.md` (root) frontmatter — project_id, client, contract_start, contract_end
- Filled `00-overview/teams.md` — PM, BA Lead, Tech Lead, Devs
- Filled `00-overview/stakeholders.md` — 5 stakeholder rows with email + comms cadence + approver-of + comms channels section
- Filled `00-overview/vision.md` — replaces example block
- Filled `00-overview/scope.md` — in-scope, out-of-scope, assumptions, constraints
- Filled `00-overview/security.md` — DPO contact (reused from stakeholders), data classification table, compliance frameworks
- Filled `00-overview/tech.md` — code repo URL, stack table, environments table
- Filled `00-overview/cadence.md` — sprint length, total sprints, working week, ceremonies
- Filled `tasks/sprint-01/_index.md` — sprint goal + start/end dates (derived from cadence)
- 3-5 RISK-NNN files created in `risks/` via `risks/_prompts.md` OP-5
- KRISA templates dropped in `deliverables/templates/` (if contract requires) or skipped
- Git + CI initialised (Step 6)
- First raw input handoff offered (Step 8)

## Prompt body
```
You are running the kickoff for a new project that's instantiating this AI-DLC template.

Read KICKOFF.md first. Then walk the user through every step below in order. After
each edit, do NOT continue to the next step until the user confirms. Run
`python scripts/regen_indexes.py .` after each edit batch to ensure validators still pass.

ROOT METADATA
1. Ask for project_id and client name. Edit root _index.md frontmatter.
2. Ask for contract_start and contract_end (ISO dates). Edit frontmatter.

TEAMS (00-overview/teams.md)
3. Ask for PM, BA Lead, Tech Lead names + emails.
4. Ask for Devs list (names + emails). At least one dev required; OK to mark "TBD"
   per role if not yet hired, but flag it in the response.

STAKEHOLDERS (00-overview/stakeholders.md)
5. Ask for Sponsor — name + email + comms cadence + approver-of (default: budget, scope, contract).
6. Ask for Business Owner — name + email + comms cadence + approver-of (default: REQs, signoffs, UAT).
7. Ask for IT Lead (client side) — name + email + approver-of (default: integration, security).
8. Ask for DPO — name + email + approver-of (default: data-handling). This same person also fills security.md DPO field.
9. Ask for Account Manager (Censof side) — name + email + approver-of (default: contract, escalation).
   Also ask "any other stakeholders to capture now?" — optional 0..N extra rows.

COMMS CHANNELS (00-overview/stakeholders.md — Communication channels section)
10. Ask for day-to-day chat channel (e.g. Slack `#proj-x`, Teams channel name + link).
11. Ask for async status / decisions channel (e.g. email DL `proj-x@censof.com`, or thread location).
12. Ask for document share location (SharePoint / OneDrive folder URL — non-repo artifacts).
13. Ask for incident pager / on-call contact (PagerDuty, phone tree, or escalation chain).

VISION (00-overview/vision.md)
14. Ask for one-paragraph vision + headline non-scope item. Replace example block.

SCOPE (00-overview/scope.md)
15. Ask "in scope (3-5 items)".
16. Ask "out of scope (3-5 items)".
17. Ask "assumptions (3-5 items)" — things we're taking as given.
18. Ask "constraints (3-5 items)" — hard limits (budget, tech, regulatory, deadline).

SECURITY (00-overview/security.md)
19. Ask for data classification — which tiers apply (Public / Internal / Confidential /
    Restricted) and what data lives in each. Fill the data classification table.
20. Ask for compliance frameworks in scope (e.g. PDPA, GDPR, ISO27001, SOC2, BNM RMiT).
    (DPO contact already captured in step 8 — copy into security.md DPO field.)

TECH (00-overview/tech.md)
21. Ask for code repo URL + default branch + visibility (private/internal/public) +
    this requirements-repo URL.
22. Ask for target stack — frontend, backend, database, cache/queue, auth, hosting (AWS/Azure/on-prem),
    CI/CD, observability. Fill the stack table. Versions optional at kickoff.
23. Ask for environments — dev, staging/UAT, prod URLs + owner + auto-deploy source +
    access scope. Fill environments table.

CADENCE (00-overview/cadence.md)
24. Ask for sprint length (1 week / 2 weeks / 3 weeks).
25. Compute total expected sprints from (contract_end - contract_start) / sprint length.
    Ask user to confirm or override.
26. Ask for working days (e.g. Mon-Fri, Sun-Thu) + public holidays calendar jurisdiction.
27. Ask for ceremony schedule:
    - Standup frequency + day/time (e.g. daily 09:30)
    - Sprint planning day/time (e.g. first Monday of sprint, 10:00)
    - Sprint review/demo day/time (e.g. last Friday of sprint, 14:00)
    - Retro day/time (e.g. last Friday of sprint, 16:00)
    - Backlog refinement cadence (e.g. mid-sprint Wednesday, 11:00)

SPRINT-01 (tasks/sprint-01/_index.md)
28. Ask for sprint-01 goal (one sentence).
29. Compute sprint-01 start + end from contract_start + sprint length (from cadence).
    Ask user to confirm or override.
30. Leave planned REQs empty — they come from raw-inputs processing.

RISKS (risks/)
31. Ask "what are the top 3-5 risks for this project?" For each: title + likelihood
    (low/medium/high) + impact (low/medium/high) + owner + brief mitigation.
    Hand off to `risks/_prompts.md` OP-5 to create RISK-001..RISK-005 records.
    Do NOT invent risks — only what user states.

KRISA DELIVERABLES (Step 5 of KICKOFF.md)
32. Ask "does the contract require KRISA D01–D18 deliverables?" If yes, instruct the
    user to drop blank templates into `deliverables/templates/` and confirm done.
    If no, skip and note in the response.

GIT + CI (Step 6 of KICKOFF.md)
33. Ask "has `git init` + `git config core.hooksPath .githooks` been run yet?" If no,
    walk through the commands. Do NOT run them yourself without explicit consent.

FIRST RAW INPUT (Step 8 of KICKOFF.md)
34. Ask "do you have a first raw input (workshop transcript, client email, source doc)
    ready to process?" If yes, route to `raw-inputs/_prompts.md` OP-3 after kickoff
    closes. If no, note that sprint-01 can't generate REQs until raw inputs arrive.

CLOSE
35. Run a search for "TBD-set-at-kickoff" and report any remaining matches. If any
    remain (other than KICKOFF.md itself), tell the user the kickoff is incomplete
    and list the files.
36. Run both validators (`validate_frontmatter.py` + `regen_indexes.py`) and report.
37. Tick off the Definition of Done in KICKOFF.md and report which (if any) are still open.
38. POST-KICKOFF HANDOFF — Print the following block to the user verbatim:

    ```
    Kickoff complete. Next steps:

    1. FIRST RAW INPUT — Drop a workshop transcript, client email, or source doc
       into the matching subfolder under raw-inputs/. Say: "log workshop transcript"
       or "add client email". Routes to raw-inputs/_prompts.md OP-1.

    2. EXTRACT REQs from raw input. Say: "extract REQs from RAW-001". Routes to
       raw-inputs/_prompts.md OP-3 → requirements/_prompts.md OP-1. Produces draft
       REQ-NNN files.

    3. REFINE AC for each draft REQ. Say: "refine AC for REQ-001". Rewrites
       acceptance criteria to Given/When/Then.

    4. CLIENT SIGNOFF → archive in signoffs/ → mark REQ approved. Approved REQs
       unlock spec → design → tasks → KRISA fills.

    5. OPEN SPRINT-01. Say: "open sprint" once you have ≥3 approved REQs.

    Continuous (no trigger needed — run on your own cadence):
    - Feedback triage every 1-2 days (INBOX → FB-NNN)
    - Risk register updates
    - Weekly dashboard refresh

    Re-orient anytime by saying "what next?" — routes to prompts/next-steps.md.
    ```

    After printing, stop. Do NOT auto-execute step 1 — wait for user.
```

## Guardrails
- Refuse to run any other operation (REQ creation, sprint planning, etc.) while project_id == "TBD-set-at-kickoff"
- Never invent stakeholder names, emails, contact info, dates, or compliance frameworks
- Never set contract dates without explicit user input
- Never run `git init` / `git push` / hook installs without explicit user consent
- Append `- {today}: Kickoff completed by <PM name>` to each filled file's Change Log
