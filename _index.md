---
folder: ROOT
purpose: AI-DLC requirements repo
owner: PM
file_naming: heterogeneous (root holds README + _index + _prompts only; see folder map below)
last_updated: 2026-05-26
project_id: TBD-set-at-kickoff
client: TBD-set-at-kickoff
contract_start: TBD-set-at-kickoff
contract_end: TBD-set-at-kickoff
current_sprint: sprint-01
playbook_version: "1.0"
lightweight_mode: false
ai_navigation_hint: |
  Start here. Read folder map below, then read the target folder's _index.md
  and _prompts.md before doing any work. Do not grep blindly. If project_id
  still shows TBD-set-at-kickoff, this is an uninitialised template — point
  the user at KICKOFF.md before doing any work.
---

# Index — Project

## Quick answers

| Question | Where |
|----------|-------|
| What is this project? | `00-overview/vision.md`, `00-overview/scope.md` |
| Who's on the team? | `00-overview/teams.md` |
| What is the current sprint? | `tasks/sprint-01/_index.md` |
| What's blocking? | `dashboard/dashboard.md` → "Blocked items" |
| AC for REQ-X? | `requirements/REQ-X-*.md` → "## Acceptance Criteria" |
| Design for feature Y? | `design/_index.md` → catalog |
| Client raised this sprint? | `feedback/sprint-01/_index.md` |
| Which Claude model? | `00-overview/ai-config.md` |
| Where are KRISA docs? | `deliverables/_index.md` |

## Folder map

| Folder | Purpose | Index |
|--------|---------|-------|
| `00-overview/` | Project meta — vision, scope, stakeholders, teams, security, AI config | `00-overview/_index.md` |
| `requirements/` | One MD per REQ; source of truth | `requirements/_index.md` |
| `spec/` | Elaborations of REQs grouped by domain | `spec/_index.md` |
| `design/` | Technical design + ADRs | `design/_index.md` |
| `tasks/` | Sprint-organized TASK MDs | `tasks/_index.md` |
| `feedback/` | INBOX + triaged FB MDs + retros | `feedback/_index.md` |
| `change-requests/` | CRs against approved REQs | `change-requests/_index.md` |
| `decisions/` | Cross-cutting non-architecture decisions | `decisions/_index.md` |
| `incidents/` | Postmortems | `incidents/_index.md` |
| `prompts/` | Versioned Claude prompts | `prompts/_index.md` |
| `deliverables/` | KRISA D01–D18 Word docs | `deliverables/_index.md` |
| `raw-inputs/` | Workshop transcripts, client emails, source docs | `raw-inputs/_index.md` |
| `signoffs/` | Client signoff evidence | `signoffs/_index.md` |
| `dashboard/` | Live PM dashboard | `dashboard/_index.md` |
| `scripts/` | CI scripts (Tier B) | `scripts/_index.md` |

## Where NOT to look
- Source code: separate code repo (see `00-overview/_index.md`)
- Build artifacts, node_modules, .git: not tracked here
- Slack/Teams chat: ephemeral, only triaged items end up in `raw-inputs/` or `feedback/`

## AI behavior expectations
- Always read this `_index.md` + `_prompts.md` first
- Then read target folder's `_index.md` + `_prompts.md`
- Never silently mutate frontmatter on records (REQ/TASK/FB/etc.) — append to Change Log
- Never edit auto-managed regions of `_index.md` files

## Maintenance
- Updated automatically by `scripts/regen_indexes.py` (CI on every PR).
- Below the marker is overwritten on each run.

<!-- auto-managed below -->

## Auto-generated catalog

| File | ID | Title | Status | Owner | Updated |
|------|----|----|--------|-------|---------|
| [CHANGELOG.md](CHANGELOG.md) | - | CHANGELOG | - | - | - |
| [CLAUDE.md](CLAUDE.md) | - | CLAUDE | - | - | - |
| [KICKOFF.md](KICKOFF.md) | - | KICKOFF | - | - | - |
| [README.md](README.md) | - | README | - | - | - |
