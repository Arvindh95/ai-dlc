---
id: PROMPT-11
name: Fill KRISA section from source MDs
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - deliverables/_prompts.md OP-1
---

# Prompt: Fill KRISA document section from source MDs

## Purpose
Fill one section of a KRISA Word deliverable (D01–D18) by reading the cited REQ / spec / design MDs and rendering the section text in the document's required style. Run inside Claude-in-Word via M365 connector.

## Inputs
- KRISA doc + section heading (e.g., "D02 BRS, section 3.2 Functional Requirements")
- Source REQ-IDs the section must cover

## Output
- Filled section text inserted into Word doc
- Hidden source-citation comment per section: `<!-- REQ: REQ-NNN, REQ-MMM -->`
- Footer updated: "Source MD commit: <hash>"

## Prompt body
```
You are filling section "<SECTION>" of <KRISA-D-NN-*.docx>.

INPUTS:
- Section heading: <SECTION>
- Source REQ-IDs: <REQ-NNN, ...>

For each source REQ:
1. Read requirements/REQ-NNN-*.md in full.
2. Verify status == "approved". If any source REQ is not approved, REFUSE — say
   "REQ-NNN is status=<X>. Cannot fill KRISA from unapproved source."
3. If REQ has spec_ref or design_ref, read those too.

Generate section text in the KRISA template's required style:
- Numbered list for functional requirements (1.1, 1.2, ...)
- Each numbered item phrased as "The system shall <verb> <object> <conditions>."
- Acceptance criteria flow into "Acceptance" sub-bullets where the template allows
- NFRs in the dedicated NFR sub-section, never mixed with functional

Insert at the start of the section: `<!-- REQ: REQ-NNN, REQ-MMM -->` (hidden comment)

Update the doc footer to include:
"Source MD commit: <latest commit hash of requirements/ folder>"

Do NOT:
- Add behaviour not in source REQs
- Paraphrase ACs into vague prose — keep them specific
- Fill from a draft / rejected / deferred REQ

After filling, ask the user to run the consistency-check OP before declaring section done.
```

## Guardrails
- Refuse to fill from non-approved REQs
- Every section must carry source-citation comment
- Footer commit hash required for downstream staleness detection
