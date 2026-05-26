---
id: PROMPT-01
name: Ingest raw input → draft REQs
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - requirements/_prompts.md OP-1
  - raw-inputs/_prompts.md OP-3
---

# Prompt: Ingest raw input and generate draft REQs

## Purpose
Read a captured raw input (workshop transcript, client email, source doc) and generate one draft REQ per atomic requirement found.

## Inputs
- A file path in `raw-inputs/<subfolder>/<RAW-NNN>.md`
- (Optional) Existing REQ catalog from `requirements/_index.md` — to avoid duplicates

## Output
- One or more `requirements/REQ-NNN-short-kebab-title.md` files with `status: draft`
- Updated `raw-inputs/<RAW-NNN>.md` frontmatter: `status: partially-processed` or `fully-processed`, `generated_reqs: [REQ-XXX, REQ-YYY, ...]`

## Prompt body
```
You are generating draft requirements from a captured raw input.

INPUT: <path to RAW-NNN file>

Read the input verbatim. For each atomic, testable requirement you can extract:

1. Generate a new REQ file at requirements/REQ-NNN-short-kebab-title.md with:
   - Frontmatter (all mandatory fields populated):
     id: REQ-NNN          # next available number in team's REQ-ID range — check teams.md
     title: <free-text title>
     status: draft
     priority: <critical|high|medium|low>    # infer from source urgency cues; if unclear, leave high
     team: <team name>     # from 00-overview/teams.md
     estimate_days: TBD
     created: <today>
     last_updated: <today>
     tags: [<domain tags>]
   - Body sections:
     # REQ-NNN — <title>
     ## Context
     <1-2 sentences from source>
     ## Description
     <what the system must do>
     ## Acceptance Criteria
     - Given <state>, when <action>, then <outcome>.
     - (one AC per testable condition)
     ## Non-Functional Requirements
     - <perf/security/compliance, if mentioned in source>
     ## Out of Scope
     - <if source explicitly excludes something>
     ## Open Questions
     - [TBD] <ambiguity from source>
     ## Change Log
     - <today>: Created from raw-inputs/<RAW-NNN>.md (lines <range>).
     ## References
     - Source: raw-inputs/<RAW-NNN>.md

2. CITE the source line range for every claim. If the source doesn't support an AC,
   write `- [TBD] <what's missing>` instead of inventing one.

3. Do NOT invent acceptance criteria, NFRs, or scope decisions not in the source.

4. If two extracted requirements clash, generate both but add `## Open Questions`
   noting the conflict — leave [TBD] for BA to reconcile.

After generating REQs, update the raw input file:
- frontmatter: status = "partially-processed" (if [TBD]s remain) or "fully-processed"
- frontmatter: generated_reqs: [REQ-NNN, ...]
- append Change Log entry: `- <today>: Generated REQ-NNN..REQ-MMM. <P> [TBD]s remain.`

Report back to user: list of REQ-IDs created + count of [TBD]s.
```

## Guardrails
- Never mark `status: approved` here — only `draft`
- Never invent ACs — use `[TBD]` markers
- Cite source line ranges for every REQ
- One REQ per atomic requirement — never bundle (split if needed)
- If REQ candidate duplicates an existing REQ, flag as duplicate; do not silently merge

## Examples
Source line (workshop transcript): "User must be able to reset password via email link, link expires after 1 hour, max 3 attempts per day."

Generates:
- REQ-NNN: Password reset via email — AC: link is sent on submit; link expires 1h; rate-limit 3/day.
