# CHANGELOG — AI-DLC Template

All notable changes to the **template scaffold** are recorded here. Each release is a stable snapshot users can instantiate via "Use this template" or ZIP download.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · SemVer · dates ISO 8601.

## [Unreleased]

_(In-progress changes since last tag — promote to a version when shipping.)_

## [1.0.1] — 2026-05-26

### Fixed
- CI work-item-ID check (`.github/workflows/ci.yml`) and local commit-msg hook (`.githooks/commit-msg`) now exempt the template-instantiation commit. GitHub's "Use this template" generates an `Initial commit` message with no work-item ID, which previously failed CI on every fresh repo. The exemption matches `Initial commit` exactly or `Initial commit from <template>` prefix. Rule kicks in from the second commit onward — actual development commits still require a work-item ID.

## [1.0.0] — 2026-05-26

Initial template release. Built from AI-DLC Playbook v1.0.

### Added
- 28-folder Tier A / B / C structure per playbook §3.1
- `_index.md` + `_prompts.md` in every Tier A folder (15 folders, both files mandatory)
- `_index.md` only in Tier B folder (`scripts/`)
- Schemas for 10 record types: REQ, TASK, FB, SPEC, DES, ADR, DEC, INC, CR, RAW
- 13 canonical prompts in `prompts/`: kickoff, ingest-raw-input, refine-ac, req-check, create-spec, create-design, sprint-plan, create-tasks-from-req, triage-feedback, retro-draft, postmortem, fill-srs-section, krisa-consistency
- `CLAUDE.md` — session bootstrap for Claude Code
- `KICKOFF.md` — 10-step instantiation checklist
- `scripts/validate_frontmatter.py` — per-record schema validator
- `scripts/regen_indexes.py` — Tier-aware index + prompts validator + catalog regen
- `.githooks/commit-msg` — work-item ID required in commit messages
- `.github/workflows/ci.yml` — CI pipeline running both validators
- 7 `00-overview/` files in template form with `TBD-set-at-kickoff` placeholders

### Notes
- Role labels (`PM` / `BA Lead` / `Tech Lead`) used in all `_index.md` `owner:` fields. Names live only in `00-overview/teams.md` so cross-project reuse is name-agnostic.
- Project metadata (`project_id`, `client`, contract dates) carries `TBD-set-at-kickoff` until kickoff completes.
- Canonical Censof AI stack pre-pinned in `00-overview/ai-config.md`: Claude (Code + Word + web), Obsidian, GitHub, OneDrive, Graphify.

## Versioning policy

- **Major (X.0.0)** — breaking change to folder structure, schema fields, or `_prompts.md` OP contracts. Adopters must port carefully.
- **Minor (1.X.0)** — new folders, new prompts, new optional fields, new CI checks. Adopters can opt in.
- **Patch (1.0.X)** — wording fixes, typo corrections, tightened validators that catch existing-invalid data without changing schema.

## Adopting a later version into an existing project

The template is **never auto-applied** to existing projects. To pull in improvements:

1. Skim this CHANGELOG between your current version and target version.
2. For each change you want, manually edit the corresponding file in your project repo.
3. Re-run `python scripts/regen_indexes.py .` + `python scripts/validate_frontmatter.py .` to confirm both validators still pass.
4. Bump the template-version reference in your project's first-commit message (or add an ADR documenting the upgrade).

Most users skip this entirely — the v1.0 template is stable enough to ride out a full project.
