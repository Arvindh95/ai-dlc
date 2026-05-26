---
folder: ROOT
purpose_of_this_file: Top-level routing — pick which folder to enter for a given request
canonical_prompts_location: prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Match user request to a top-level operation. Then navigate into the named
  folder and read its _index.md + _prompts.md before acting. If _index.md
  shows project_id=TBD-set-at-kickoff, run OP-0 (kickoff) first.
---

# Operations — Project root

## When you (the AI) are in this folder
You are at the project root. Your job is to **route** the request to the right Tier A folder, not to do work here directly.

## OP-0: Initialise template for a new project
- **Trigger phrases:** "kickoff", "instantiate template", "new project setup", project_id == "TBD-set-at-kickoff"
- **Canonical prompt:** `prompts/kickoff.md`
- **Inputs:** Client name, project ID, contract dates, team list
- **Output:** Updated root `_index.md` frontmatter + filled `00-overview/*.md`
- **Inline summary:** Walk the user through `KICKOFF.md` checklist step-by-step. Fill in actual values for each TBD-set-at-kickoff field. Do NOT skip a step. Validators must still pass after each edit.

## OP-1: Start of new session orientation
- **Trigger phrases:** "start", "what is this project", "orient yourself", session begin
- **Canonical prompt:** _(inline)_
- **Inputs:** none
- **Output:** Verbal summary
- **Inline summary:** Read this `_index.md` Quick answers + Folder map. Read `00-overview/_index.md`. Report project name, client, current sprint, team list.

## OP-2: Route user request to correct folder
- **Trigger phrases:** any vague task ("update this", "fix this", "add requirement")
- **Inputs:** the user's request text
- **Output:** Named folder + named OP in that folder's `_prompts.md`
- **Inline summary:** Map intent → folder. Requirements creation/refinement → `requirements/`. Spec → `spec/`. Design → `design/`. Sprint task → `tasks/sprint-NN/`. Client gripe → `feedback/`. CR against approved REQ → `change-requests/`. Postmortem → `incidents/`. KRISA doc fill → `deliverables/`.

## OP-3: Run drift check across whole repo
- **Trigger phrases:** "check drift", "audit traceability", "are all REQs covered"
- **Canonical prompt:** `prompts/req-check.md`
- **Inputs:** none
- **Output:** Report of broken refs
- **Inline summary:** For each approved REQ, verify spec_ref, design_ref, tasks, test_ref resolve. Report to `dashboard/drift-report.md`.

## Forbidden in this folder
- Do NOT create record MDs (REQ/TASK/FB) at root — they belong in their folder
- Do NOT edit auto-managed region of `_index.md`
- Do NOT bypass `_prompts.md` lookup — always read the target folder's `_prompts.md` before acting

## Escalate to human if
- Request doesn't map cleanly to any folder/OP — ask BA for clarification
- Two folders both seem to apply — propose split, do not silently pick one
- User asks to "just do it" without context — refuse, demand context

## Related operations in other folders
- See each Tier A folder's `_prompts.md`
