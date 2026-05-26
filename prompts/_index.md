---
folder: prompts
purpose: "Versioned Claude prompts used by AI operations across folders."
owner: "Tech Lead"
file_naming: "<op-name>.md (e.g., ingest-raw-input.md, refine-ac.md). Version in frontmatter."
last_updated: 2026-05-26
ai_navigation_hint: |
  Read this folder to find canonical prompts referenced by `_prompts.md` OPs. Never inline a prompt — link here.
---

# Index — prompts/

## Purpose
Versioned Claude prompts used by AI operations across folders.

## File naming
<op-name>.md (e.g., ingest-raw-input.md, refine-ac.md). Version in frontmatter.

## Frontmatter schema
| Field | Type | Values |
|-------|------|--------|
| id | string | PROMPT-NN |
| name | string | Free text |
| version | string | semver |
| status | enum | draft, active, deprecated |
| last_updated | date | ISO 8601 |
| used_by | list[string] | Folder/op references |


## Catalog
_(auto-generated below — do not edit by hand)_

## Related folders
- `../requirements/`
- `../spec/`
- `../design/`
- `CHANGELOG.md`

## Common questions
- **Which prompt for ingest?** → `ingest-raw-input.md`
- **Prompt version history?** → `CHANGELOG.md`


## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Manual content lives **above** the marker. Below is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

| File | ID | Title | Status | Owner | Updated |
|------|----|----|--------|-------|---------|
| [CHANGELOG.md](CHANGELOG.md) | - | CHANGELOG | - | - | - |
| [create-design.md](create-design.md) | PROMPT-05 | create-design | active | - | 2026-05-26 |
| [create-spec.md](create-spec.md) | PROMPT-04 | create-spec | active | - | 2026-05-26 |
| [create-tasks-from-req.md](create-tasks-from-req.md) | PROMPT-07 | create-tasks-from-req | active | - | 2026-05-26 |
| [fill-srs-section.md](fill-srs-section.md) | PROMPT-11 | fill-srs-section | active | - | 2026-05-26 |
| [ingest-raw-input.md](ingest-raw-input.md) | PROMPT-01 | ingest-raw-input | active | - | 2026-05-26 |
| [kickoff.md](kickoff.md) | PROMPT-00 | kickoff | active | - | 2026-05-26 |
| [krisa-consistency.md](krisa-consistency.md) | PROMPT-12 | krisa-consistency | active | - | 2026-05-26 |
| [postmortem.md](postmortem.md) | PROMPT-10 | postmortem | active | - | 2026-05-26 |
| [refine-ac.md](refine-ac.md) | PROMPT-02 | refine-ac | active | - | 2026-05-26 |
| [req-check.md](req-check.md) | PROMPT-03 | req-check | active | - | 2026-05-26 |
| [retro-draft.md](retro-draft.md) | PROMPT-09 | retro-draft | active | - | 2026-05-26 |
| [sprint-plan.md](sprint-plan.md) | PROMPT-06 | sprint-plan | active | - | 2026-05-26 |
| [triage-feedback.md](triage-feedback.md) | PROMPT-08 | triage-feedback | active | - | 2026-05-26 |
