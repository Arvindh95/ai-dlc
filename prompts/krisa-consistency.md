---
id: PROMPT-12
name: KRISA consistency check
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - deliverables/_prompts.md OP-2
---

# Prompt: KRISA deliverable consistency check

## Purpose
Compare a filled KRISA section against its cited source MDs and flag any drift.

## Inputs
- KRISA doc file
- (Reads hidden `<!-- REQ: ... -->` comments to find sources)

## Output
- Drift report (text or appended note)

## Prompt body
```
You are checking consistency between <KRISA-D-NN-*.docx> and the source MDs it cites.

For each section in the doc:
1. Read the hidden `<!-- REQ: REQ-NNN, ... -->` comment at section start.
2. For each cited REQ:
   a. Read requirements/REQ-NNN-*.md.
   b. Compare the section text against the REQ's current content.
3. Flag drift signals:
   - SECTION mentions behaviour NOT in REQ — possible invention
   - REQ has AC NOT covered by SECTION — possible omission
   - REQ.status != approved — section was filled from a now-unapproved REQ
   - REQ.last_updated > footer commit hash date — section is stale

Generate consistency report:

# Consistency check — <KRISA-D-NN> — <today>

## Sections with drift (P0)
| Section | Cited REQ | Drift type | Detail |
|---------|-----------|------------|--------|
| 3.2.1   | REQ-042   | Stale      | REQ updated 2026-04-12; footer hash from 2026-04-01 |
| 4.1     | REQ-055   | Invention  | Section mentions "rate limit 100/min" — not in REQ |

## Sections OK (P3)
- <count>

## Sections without citation (P1)
- <list — these need to be re-filled with source citation>

Report counts to user.
```

## Guardrails
- Never auto-fix — report only
- Stale = trigger to re-run fill-srs-section, not silent edit
