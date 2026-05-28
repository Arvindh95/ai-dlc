# Prompts CHANGELOG

## 2026-05-28
- `kickoff.md` (PROMPT-00) v0.1.0 → v0.5.0: expanded to 37 steps covering full KICKOFF.md DoD; added cadence, tech, stakeholders-expansion, comms-channels, risks-seed, sprint-NN derivation sections; added post-kickoff handoff block (step 38).
- `req-check.md` (PROMPT-03) v0.1.0 → v0.2.0: added reverse task→design traceability check (design_ref resolves, domain match, approved-design gate) + new "Task traceability (P1)" report section.
- `next-steps.md` (PROMPT-13) NEW v0.1.0: post-kickoff / return-from-break orientation; stage diagnosis (A-E) + ranked next moves. Wired to ROOT/_prompts.md OP-4.
- `create-design.md` (PROMPT-05) v0.1.0 → v0.2.0: reads `00-overview/tech.md` for target stack (was incorrectly pointing at `ai-config.md`, which is Claude-model pinning only).
- `create-tasks-from-req.md` (PROMPT-07) v0.1.0 → v0.2.0: design is now a mandatory input (escalate if no approved design); emits `design_ref` in task frontmatter so drift check passes.
- `sprint-plan.md` (PROMPT-06) v0.1.0 → v0.2.0: clones from dedicated `sprint-template/` (tasks + feedback sides) with `{{SPRINT_NN}}` token substitution, instead of cloning sprint-01.

## 2026-05-26
- Scaffolded.
