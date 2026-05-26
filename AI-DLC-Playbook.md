# AI-Assisted Development Lifecycle (AI-DLC) Playbook

**Version:** 1.0
**Owner:** Arvindh / Censof
**Last updated:** 2026-05-26
**Status:** Living document — update after every project retro

---

## 0. How to Read This Playbook

This playbook is the Censof standard for running software projects with AI assistance (primarily Claude). It is the consolidated lesson-learnt from prior engagements where doc drift, scope creep, lost context, and AI hallucination caused rework.

The playbook is opinionated. Deviations should be documented in the project's `decisions/` folder with rationale.

It is organized in **fourteen failure-mode parts (§1–§14)**, plus two synthesis sections — §15 walks through a full project lifecycle using the parts, and §16 holds appendices (scripts, templates, glossary). The fourteen parts each address one failure mode observed in past projects:

| Part                      | Failure mode it addresses                           |
| ------------------------- | --------------------------------------------------- |
| 1. Principles             | Lack of shared philosophy → inconsistent decisions |
| 2. Tooling stack          | Tool sprawl, duplicated state                       |
| 3. Source of truth        | Requirements drift across Word/email/Slack          |
| 4. Doc generation (KRISA) | Manual rewriting same info into 18 templates        |
| 5. Teams & ownership      | Merge hell, ping-pong bugs, unclear accountability  |
| 6. Change control         | Silent scope creep, untraced changes                |
| 7. PM dashboard           | No visibility, status meetings replace work         |
| 8. Sprint feedback loop   | Feedback bypasses MD, devs work from Slack          |
| 9. Quality gates          | "Done" subjective, bugs escape to UAT               |
| 10. Security & compliance | Secrets leaked, PDPA gaps, IP ambiguity             |
| 11. Deploy & ops          | Big-bang deploys, no rollback, prod surprises       |
| 12. Incident response     | Chaos under pressure, no postmortem learning        |
| 13. AI risk management    | Hallucination shipped, stale prompts, model drift   |
| 14. Communication cadence | Decisions lost in chat, client surprised at demo    |

Appendices contain copy-paste templates, prompts, and checklists.

> **Note on examples.** Names (`arvindh`, `ba-rina`, `dev-3`), emails (`arvindh@censof.com`), and project identifiers (`Project X`, `project-x.censof.com`, `REQ-042`, `TASK-101`, `FB-042`, `INC-001`, `CR-001`, `DEC-001`) appearing throughout this playbook are **illustrative only**. When applying the playbook to a real project, replace them with the actual project's owners, identifiers, and IDs. The playbook does not assume any real "Project X" exists; it is a worked example to make the conventions concrete.

---

## 1. Principles

These are the non-negotiable rules. Every other section serves these.

### 1.1 Single source of truth

Requirements live in Markdown, version-controlled in Git. All other artifacts (KRISA SRS/SDS, Word docs, GitHub Issues, Obsidian dashboards, slides) are **views** onto the Markdown. Never edit a view and expect the source to update. The view is regenerated; the source is edited.

### 1.2 Every artifact traces back to a tracked work item

Every change — code, test, doc, infra tweak — must cite at least one tracked work-item ID: `REQ-`, `TASK-`, `FB-`, `INC-`, `CR-`, or `DEC-`. Most changes cite REQ (feature work) or TASK (split of a REQ). Bug fixes cite FB. Hotfixes cite INC. Scope changes cite CR. Cross-cutting decisions cite DEC. If no ID applies, you are working outside scope — stop and either create a TASK under an existing REQ, or raise a CR/DEC.

The commit hook enforces the broader pattern (any of those six ID types). The principle is: nothing happens without traceability to a tracked item.

### 1.3 No change without going through the source

Client feedback, late changes, bug reports, demo requests — all enter through the Requirements Markdown pipeline. Direct messages to developers are converted to Markdown entries by the BA within 24 hours, or they do not exist.

### 1.4 AI proposes, human decides

Claude generates, drafts, suggests, reviews. A human (developer, BA, lead) accepts, edits, or rejects. Accountability stays with humans. No auto-merge of AI output into authoritative artifacts.

### 1.5 Generate part by part

Long-form generation (full SRS in one shot) produces hallucination and drift. Section-by-section generation, grounded in the source MD, produces accurate output. Always slice.

### 1.6 Definition of Done is explicit

"Done" is a checklist, not a feeling. Every stage (REQ, Spec, Design, Task, Code, Test, Deploy) has a written DoD. CI enforces what it can; humans enforce the rest.

### 1.7 Visibility by default

Status, progress, blockers, scope changes — all visible to client and team without anyone asking. Dashboards auto-update from the source MD. Weekly status reports auto-generate. Surprises in steering committees indicate a process failure.

### 1.8 Folders are self-describing per tier policy (`_index.md` + `_prompts.md`)

Folders are tiered (see 3.2.0): **Tier A** (managed knowledge) requires both files — mandatory. **Tier B** (code/infra) requires `_index.md` — mandatory; `_prompts.md` only when folder-specific operations exist. **Tier C** (tool-managed, generated, or unknown) is exempt.

- **`_index.md`** — *passive knowledge*. What the folder contains, file naming, frontmatter schema, catalog of current files, navigation hints. Read first by any AI or human entering the folder.
- **`_prompts.md`** — *active instructions*. Operations available in this folder, trigger phrases, canonical prompt links, inline short prompts, forbidden actions, escalation triggers. Read by AI when about to execute work in the folder.

AI tools must read both before doing any work in a Tier A or Tier B folder that has them. This convention cuts AI navigation cost ~75% and prevents wrong-action errors. See 3.2 for the full convention and 3.2.0 for the tier matrix.

### 1.9 Separate voice: policy vs example vs planned

The playbook mixes three voices, and the reader must always know which one is talking:

- **`[POLICY]`** — binding rule. CI enforces, or a documented manual gate enforces. Deviation requires a logged DEC.
- **`[EXAMPLE]`** — illustrative content (REQ-042, "Project X", names like ba-rina, sample acceptance criteria). Change per project; not authoritative.
- **`[PLANNED v1.X]`** — intended automation/process that is **not yet implemented**. Today the team does it manually. Promoted to `[POLICY]` only when the implementation lands.

Where a section mixes voices, the dominant voice is named at section start, and other voices are inline-tagged. Sections without a tag are `[POLICY]`.

Current `[PLANNED v1.1]` items (to implement before v1.1 ships):

- KRISA staleness detector (Appendix A.2 — stub today)
- Cross-link validator (mentioned in 6.2 — partial today)
- Frontmatter status-transition validator (mentioned in 6.2 — partial today)
- KRISA Word footer ↔ MD commit comparator (referenced in 4.7 — manual today)
- Externalize Tier A/B/C patterns from `regen_indexes.py` to `00-overview/folder-tiers.yml` (today: hardcoded in script)
- Historical dashboard snapshots — nightly `dashboard/snapshots/dashboard-YYYY-MM-DD.md` capturing metric values for trend analysis (today: read trends live via Dataview; see 7.4 Layer 3)
- **Code → MD auto-sync** (see 6.5):
  - Auto-flip TASK status to `done` on PR merge (Appendix A.5 — stub)
  - Auto-build REQ↔test coverage map from code scan (Appendix A.6 — stub)
  - Auto-propose REQ `ready-for-acceptance` when all tasks done + tests passing (Appendix A.7 — stub)
  - Design ↔ code drift detection via Graphify (Appendix A.8 — stub)

Until these land, the corresponding workflows are **manual**, and that is acceptable for v1.0. Calling them out prevents the reader from assuming automated enforcement that does not exist.

### 1.10 Iterate the playbook

This document is not finished. After every project retro, add lessons learnt. Treat the playbook the same as a product: ship v1, observe pain, fix in v1.1.

---

## 2. Tooling Stack

The Censof-standard stack — minimal by design. Every named tool here earns its place. No tool sprawl, no duplicate state.

### 2.1 The six named tools

| Tool                                                                                               | Role                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Claude (current model: claude-opus-4-7, as of 2026-05; see `00-overview/ai-config.md`)** | Primary AI assistant — code, docs, reviews, triage, dashboards, all generation.*Caveman mode* is a conversation convention on top of Claude (see 2.6), not a separate tool. |
| **Obsidian**                                                                                 | Markdown editing, graph view, Dataview-powered dashboards, Kanban boards, sprint tracking (via standard plugin set, see 2.5)                                                   |
| **Git (GitHub)**                                                                             | Version control for code and Requirements MD; ships with Issues, Actions (CI/CD), Secrets, CODEOWNERS, native secret scanning, dependency graph                                |
| **OneDrive / SharePoint (M365)**                                                             | Client-facing folder, KRISA Word delivery, mirror of MD repo, raw input storage. M365 also provides Teams (comms/webhooks), Outlook SMTP, encrypted email                      |
| **Microsoft Word + Claude in Word**                                                          | KRISA template population (D01–D18), reads from OneDrive via M365 connector                                                                                                   |
| **Graphify**                                                                                 | Code knowledge graph for developer context, prevents AI hallucinated APIs                                                                                                      |

Each named tool brings built-in platform features that we use heavily (see 2.2). We do not add extra paid tools — no PagerDuty, no Jira, no LaunchDarkly, no Power BI, no Prometheus stack, no dedicated secrets vault.

### 2.2 Platform features we depend on (shipped with the named tools or the OS)

These are not separate tools — they come with the named six, or with the operating system the VPS runs:

| Feature                       | Comes from           | Used for                                                                      |
| ----------------------------- | -------------------- | ----------------------------------------------------------------------------- |
| GitHub Actions                | GitHub               | CI/CD pipeline                                                                |
| GitHub Issues + Projects      | GitHub               | Issue tracking, sprint board (optional alongside Obsidian Kanban)             |
| GitHub Secrets                | GitHub               | CI-time secret storage                                                        |
| GitHub native secret scanning | GitHub               | Detect committed secrets                                                      |
| GitHub dependency graph       | GitHub               | License visibility per dep                                                    |
| Teams webhooks                | M365                 | Alert delivery, deploy notifications, incident broadcasts                     |
| Outlook SMTP                  | M365                 | Email alerts, weekly status reports to client                                 |
| Obsidian plugins (see 2.5)    | Obsidian             | Dashboards, Kanban, frontmatter templates, git sync                           |
| Bash, cron, SSH               | Linux (VPS)          | Alert scripts, scheduled jobs, deploys                                        |
| `logrotate`                 | Linux (VPS)          | Log file rotation                                                             |
| Docker + Docker Compose       | OS container runtime | Environment parity (treated as a build-artifact format, not a tracked "tool") |
| `chattr +a` (append-only)   | Linux ext4           | Audit log file immutability                                                   |

When this playbook says "the standard stack," it means **the six named tools (2.1) plus their built-in platform features (2.2) plus the OS the VPS runs**. No extra licensed software.

### 2.3 What each tool does NOT do (and how we work around)

| Tool gap                   | Workaround                                                                                                                                |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| No dedicated issue tracker | GitHub Issues + Obsidian Kanban plugin for sprint board view                                                                              |
| No dedicated PM tool       | Obsidian Dataview queries on MD frontmatter = live dashboard                                                                              |
| No dedicated paging        | Incident detection via simple monitoring scripts (Bash + cron + Teams webhook); on-call = manual phone/Teams                              |
| No feature flag platform   | Env-var-based flags in code; toggle via deploy or config push                                                                             |
| No observability platform  | Application logs to file + simple log rotation; Claude reads logs for diagnosis; metrics via cron-scraped endpoints written to MD or JSON |
| No client BI dashboard     | Auto-generated weekly status PDF (Claude) + OneDrive-shared Obsidian-rendered HTML export                                                 |
| No secrets vault           | GitHub Secrets for CI;`.env` files (gitignored) for local; OS-level env vars for VPS                                                    |

### 2.4 When to invoke each tool

- **MD authoring (REQs, Spec, Design, Tasks, Feedback):** Obsidian with Git plugin auto-syncing to GitHub.
- **PM tracking and dashboards:** Obsidian plugins — Dataview (queries), Kanban (boards), Tasks (todos), Calendar (timeline), Templater (frontmatter scaffolding).
- **Code:** Git, edited in any IDE; Claude assists via Claude Code CLI or IDE plugin; Graphify provides codebase context to Claude.
- **Reading MD into Word for KRISA generation:** Open Word, open Claude in Word side panel, configure M365 connector to expose the OneDrive folder containing the MD source.
- **Long conversations with Claude:** Activate `/caveman full` for token efficiency.
- **Client delivery:** Word docs to OneDrive shared folder; client opens in their Word, leaves comments. BA pulls comments back into MD.

### 2.5 Obsidian plugin set (the PM stack)

These plugins make Obsidian a complete PM tool. Install in every project vault:

| Plugin                       | Use                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| **Dataview**           | Live queries on MD frontmatter — dashboard, burndown, blocked list, REQ status, team load |
| **Kanban**             | Sprint board view (Todo / In Progress / Review / Done) backed by MD files                  |
| **Tasks**              | Track checkbox todos across the vault, query by tag/due-date                               |
| **Calendar**           | Daily notes + sprint date timeline                                                         |
| **Templater**          | Scaffold new REQ/Task/FB/Incident MDs with correct frontmatter                             |
| **Git**                | Auto-commit, push, pull from inside Obsidian — BAs don't touch Git CLI                    |
| **Mermaid (built-in)** | Diagrams in MD (sequence, flowchart, ER) — embedded into KRISA Word later                 |
| **Excalidraw**         | Hand-drawn-style diagrams for whiteboarding sessions, stored as MD-embedded SVG            |
| **Charts**             | Visualize Dataview output (velocity charts, bug trend)                                     |
| **Periodic Notes**     | Weekly/monthly review notes auto-generated from templates                                  |
| **Linter**             | Enforce frontmatter format on save                                                         |

Each project has the same Obsidian vault structure (see Appendix C) and the same plugin set, so any dev/BA can sit at any project and navigate immediately.

### 2.6 Conventions on top of the stack (not tools)

These are working conventions, not separate tools. They live inside the named tools (mostly Claude) and earn their place by changing how the team operates.

| Convention                                           | Where it lives          | What it does                                                                                                                                                                                                                  |
| ---------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Caveman mode**                               | Claude conversation     | Token-efficient style (`/caveman full`) — preserves technical substance, drops articles/filler/pleasantries. Saves ~75% token cost on long sessions. NOT used in committed artifacts (commits/PRs/docs stay normal prose). |
| **Two-pass AI review**                         | Claude (sessions)       | Pass 1 generates, Pass 2 (fresh session) critiques against DoD. See 9.3.                                                                                                                                                      |
| **`_index.md` + `_prompts.md` per folder** | Obsidian/Git filesystem | AI navigation discipline. See 3.2.                                                                                                                                                                                            |
| **REQ/TASK/FB/INC/CR/DEC ID in every commit**  | Git                     | Traceability. See 1.2 + commit hook.                                                                                                                                                                                          |
| **Mandatory log redaction before AI paste**    | OS + Claude             | `infra/redact-logs.sh` strips secrets/PII before logs go into a Claude prompt. See 11.6.                                                                                                                                    |

A convention can be adopted/dropped per project. A tool requires procurement, installation, training, and license review — much heavier. Naming the distinction prevents the conventions list from masquerading as tools.

---

## 3. Source of Truth Layer

The Markdown corpus is the heart of the system. Everything else depends on it being clean, current, and complete.

### 3.1 Repository layout

Every project has a `requirements-repo` (separate from the code repo, or in a monorepo subfolder):

```
project-x-requirements/
├── README.md                       # Project intro, links, owners
├── _index.md                       # Top-level map: what each folder contains
├── _prompts.md                     # Top-level operations: how to pick which folder/op
├── 00-overview/
│   ├── _index.md
│   ├── _prompts.md
│   ├── vision.md
│   ├── scope.md
│   ├── stakeholders.md
│   ├── glossary.md
│   ├── teams.md
│   ├── security.md
│   └── ai-config.md                # Model pinning, AI tiers
├── requirements/
│   ├── _index.md                   # REQ-ID range, status taxonomy, frontmatter schema
│   ├── _prompts.md                 # OPs: create-from-raw, refine-AC, drift-check, approve
│   ├── REQ-001-user-login.md
│   ├── REQ-002-password-reset.md
│   └── ...
├── spec/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: create-spec-for-REQ, refine-spec, version-bump
│   ├── auth-spec.md
│   ├── billing-spec.md
│   └── ...
├── design/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: create-design, add-ADR, API-contract-change
│   ├── auth-design.md
│   ├── data-model.md
│   ├── api-contracts.md
│   ├── architecture.md
│   └── adrs/
│       ├── _index.md
│       ├── _prompts.md             # OPs: draft-ADR, supersede-ADR
│       ├── ADR-001-postgres.md
│       └── ADR-002-jwt-auth.md
├── tasks/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: sprint-plan, create-tasks-from-REQ, assign
│   ├── backlog.md
│   ├── sprint-01/
│   │   ├── _index.md
│   │   ├── _prompts.md             # OPs: sprint-open, sprint-close, burndown, carry-over
│   │   ├── TASK-001-implement-login.md
│   │   └── ...
│   └── sprint-02/
│       ├── _index.md
│       └── _prompts.md
├── feedback/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: triage-INBOX, classify, route, escalate
│   ├── INBOX.md
│   ├── sprint-01/
│   │   ├── _index.md
│   │   ├── _prompts.md             # OPs: retro-draft, feedback-metrics
│   │   ├── FB-001-login-error.md
│   │   └── retro.md
│   └── sprint-02/
├── change-requests/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: draft-CR, approve-CR, reject-CR, link-to-REQ-revision
│   └── CR-001-totp-window-60s.md
├── decisions/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: draft-DEC, supersede-DEC
│   └── DEC-001-go-with-onedrive.md
├── incidents/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: postmortem-draft, runbook-update
│   └── INC-001-login-outage.md
├── prompts/
│   ├── _index.md                   # Prompt library map, when-to-use each
│   ├── _prompts.md                 # OPs: add-new-prompt, version-bump, deprecate
│   ├── fill-srs-section.md
│   ├── triage-feedback.md
│   └── CHANGELOG.md
├── deliverables/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: fill-KRISA-section, consistency-check, regen
│   ├── D01-PPS.docx
│   ├── D02-BRS.docx
│   ├── ...
│   ├── templates/                  # Blank Word templates (KRISA, weekly-status)
│   │   ├── _index.md
│   │   ├── _prompts.md             # OPs: use-template, add-new-template
│   │   └── weekly-status.docx
│   └── demos/                      # Sprint demo recordings + screen captures
│       ├── _index.md
│       ├── _prompts.md             # OPs: archive-demo, link-demo-to-sprint-retro
│       └── sprint-NN.mp4
├── raw-inputs/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: capture, transcribe, extract, mark-processed
│   ├── workshops/
│   │   ├── _index.md
│   │   └── _prompts.md
│   ├── client-emails/
│   │   ├── _index.md
│   │   └── _prompts.md
│   └── client-docs/
│       ├── _index.md
│       └── _prompts.md
├── signoffs/
│   ├── _index.md
│   ├── _prompts.md                 # OPs: archive-signoff, cross-ref-REQ
│   └── ...
└── dashboard/
    ├── _index.md
    ├── _prompts.md                 # OPs: refresh, HTML-export, weekly-status-PDF, ops-summary
    ├── dashboard.md                # Live Dataview dashboard
    ├── velocity.md                 # Velocity + trend charts
    ├── sprint-board.md             # Kanban view
    ├── ops-daily.md                # Auto-generated daily ops summary (Claude reads logs)
    ├── exports/                    # [Tier C — generated, exempt] HTML snapshots for client viewing
    │   └── index.html
    ├── snapshots/                  # [Tier C — generated, exempt] [PLANNED v1.1] Nightly metric snapshots (see 7.4 Layer 3)
    └── queries/
        ├── _index.md
        └── _prompts.md
```

### 3.2 The `_index.md` + `_prompts.md` convention — AI-friendly navigation and operations

**Every tracked folder contains `_index.md`; Tier A folders additionally contain `_prompts.md`** (see 3.2.0 for the full tier policy).

| File            | Purpose                                                                         | Read when                                    | Required in                                      |
| --------------- | ------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------ |
| `_index.md`   | Passive knowledge: what is here, schema, catalog, navigation                    | AI/human entering the folder for orientation | Tier A + Tier B                                  |
| `_prompts.md` | Active instructions: which operations are valid here, with prompts and triggers | AI about to perform work in the folder       | Tier A (mandatory); Tier B (only when ops exist) |

When an AI lands in a folder, it reads `_index.md` first (to understand context), then `_prompts.md` if present (to know which operations are valid and how to execute them). Together they replace minutes of exploration with one or two file reads (depending on whether `_prompts.md` is present — see 3.2.0 tier policy).

#### 3.2.0 Folder tiers — where the rule applies

Not every folder needs both files. We tier folders by whether they hold managed knowledge or are pure infrastructure:

| Tier                                  | Folders                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `_index.md`          | `_prompts.md`                                              | Rationale                                                                                                                                                                                             |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier A — Managed knowledge** | `00-overview/`, `requirements/`, `spec/`, `design/`, `tasks/` (and sprint subfolders), `feedback/` (and sprint subfolders), `decisions/`, `incidents/`, `prompts/`, `deliverables/`, `dashboard/`, `raw-inputs/` (and subfolders), `signoffs/`, `change-requests/`, repo roots (requirements-repo, code-repo)                                                                                                                                                                                                            | **Mandatory**    | **Mandatory**                                          | These are the folders AI navigates and operates in. The convention pays for itself here.                                                                                                              |
| **Tier B — Code/infra**        | `code-repo/services/`, `code-repo/libs/`, `code-repo/infra/`, `code-repo/infra/runbooks/`, `code-repo/infra/alerts/`, `code-repo/tests/`, `code-repo/scripts/`                                                                                                                                                                                                                                                                                                                                                                         | **Mandatory**    | **Optional** (recommended for runbooks, alerts, tests) | Code folders benefit from `_index.md` for AI orientation. `_prompts.md` only when there are real folder-specific operations (e.g., runbooks have lookup/update; pure code folders usually don't). |
| **Tier C — Exempt**            | **Tool-managed:** `.git/`, `.obsidian/`, `.github/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.venv/`, `venv/`, `dist/`, `build/`. **Generated/export subfolders:** `exports/`, `snapshots/`, `cache/`, `_generated/`, `tmp/` (often inside Tier A parents like `dashboard/exports/`). **Plus:** any unknown folder that doesn't match Tier A or Tier B (default — see note below). The full list lives in `SKIP_DIRS` at the top of `scripts/regen_indexes.py`. | **Not required** | **Not required**                                       | Tool-managed, build-generated, or scratch content. Convention adds no value, would create noise.                                                                                                      |

CI fails if a Tier A folder lacks either file or a Tier B folder lacks `_index.md`. Tier C is silently skipped.

**Default for unknown folders:** Tier C (skip). If a developer creates `scratch/`, `notes/`, `experiments/`, or any folder not listed in `TIER_A_PATTERNS` / `TIER_B_PATTERNS`, the script does NOT force `_index.md` on it. The repo root is the only exception — it defaults to Tier A (where root `_index.md` + `_prompts.md` live). If you want a non-standard folder tracked, add its name to `TIER_A_PATTERNS` or `TIER_B_PATTERNS` in `scripts/regen_indexes.py`.

**Naming-collision pitfall.** `folder_tier()` classifies by **any** path part matching a Tier A or Tier B pattern. So a code folder accidentally named after a Tier A keyword — e.g., `code-repo/services/auth/spec/` (literal `spec` subfolder under an auth service) — will be classified Tier A and forced to carry both `_index.md` and `_prompts.md`. Two ways to avoid this:

1. Don't reuse Tier A/B pattern names (`requirements`, `spec`, `design`, `tasks`, `feedback`, `decisions`, `incidents`, `prompts`, `deliverables`, `dashboard`, `raw-inputs`, `signoffs`, `change-requests`, `00-overview`, `adrs`, `services`, `libs`, `infra`, `runbooks`, `alerts`, `tests`, `scripts`) for unrelated code folders. Prefer `spec_data/`, `specifications/`, etc.
2. If you must, add the colliding path to a project-specific SKIP entry. The cleanest fix is to extend `SKIP_DIRS` in the project's copy of `regen_indexes.py`. (`[PLANNED v1.1]` will move this into `00-overview/folder-tiers.yml` so projects can override without editing scripts.)

**Small projects (< 2 sprints, single dev) may opt out of Tier B `_index.md`** by setting `lightweight_mode: true` in the root `_index.md` frontmatter. Tier A is still mandatory regardless of project size — the convention earns its keep on the smallest project.

A missing mandatory file is a CI failure. The validator (`regen_indexes.py`) hardcodes the Tier A/B/C patterns at the top of the script (`TIER_A_PATTERNS`, `TIER_B_PATTERNS`, `SKIP_DIRS`). Project-level overrides — when needed — are done by editing those lists in the project's copy of the script. *(`[PLANNED v1.1]`: externalize to `00-overview/folder-tiers.yml` so projects can override without touching the script.)*

#### 3.2.1 Why this matters (the cost of no index)

Without `_index.md`, an AI asked "where are the requirements about authentication?" must:

1. List files in the requirements folder (cost: many tokens for long file lists).
2. Open multiple files to guess what they contain (cost: many tokens, plus risk of missing the right one).
3. Infer the frontmatter schema from samples (cost: tokens, plus risk of inferring wrong).
4. Possibly grep across the repo (cost: large tokens, returns noisy results).

With `_index.md`, the AI reads one file (~200 lines) and gets:

- The folder's purpose
- The naming convention and how to construct a filename for a given REQ-ID
- The full frontmatter schema for files in this folder
- A categorized list of all current files with one-line descriptions
- Links to related folders (spec/, design/, tasks/)
- The five most common questions answered with pre-built Dataview queries or pointers

Cost drops by ~80%. Accuracy goes up because the AI is grounded in the index, not guessing.

#### 3.2.2 `_index.md` schema

Every `_index.md` follows this structure:

```yaml
---
folder: requirements
purpose: Stores one MD file per atomic business/system requirement. Source of truth for all downstream artifacts.
owner: BA team (lead: ba-rina)
file_naming: REQ-NNN-short-kebab-title.md (e.g., REQ-042-totp-login.md)
id_range: REQ-001 to REQ-999 (assigned per team — see ../00-overview/teams.md)
last_updated: 2026-05-26
last_updated_by: claude-auto-index
ai_navigation_hint: |
  Start here when asked about requirements. Use the "Catalog" table below to find a REQ
  by domain or status. Do not grep the folder — query Dataview or read the catalog.
---

# Index — requirements/

## Purpose
One file per requirement. Lifecycle: draft → approved → in-dev → ready-for-acceptance → done. (Plus terminal/branching states: blocked, late-change, rejected, deferred.)

## File naming
REQ-NNN-short-kebab-title.md
- NNN: zero-padded number from the team's REQ-ID range
- short-kebab-title: 3–6 words, lowercase, hyphenated

## Frontmatter schema
All required unless marked optional.

| Field | Type | Values |
|-------|------|--------|
| id | string | REQ-NNN |
| title | string | Free text |
| status | enum | draft, approved, in-dev, ready-for-acceptance, done, blocked, late-change, rejected, deferred |
| priority | enum | critical, high, medium, low |
| team | enum | See ../00-overview/teams.md |
| estimate_days | number | Decimal allowed |
| created | date | ISO 8601 |
| approved | date or null | ISO 8601 |
| implemented | date or null | ISO 8601 |
| spec_ref | string | Path#anchor to spec section |
| design_ref | string | Path#anchor to design section |
| tasks | list[string] | TASK-IDs |
| test_ref | string | Path to test file |
| tags | list[string] | Domain tags |

Full schema with examples: see ../00-overview/_index.md#schemas.

## Catalog (auto-generated by Dataview; click to open)

```dataview
TABLE status, priority, team, file.link AS file
FROM "requirements"
SORT id ASC
```

## Related folders

- `../spec/` — elaborates approved requirements
- `../design/` — technical design for specs
- `../tasks/` — implementation work for requirements
- `../tests/` (in code repo) — verification
- `../feedback/` — change requests against requirements

## Common questions

- **Which REQs are blocked?** → see Dataview query `dashboard/queries/blocked.md`
- **What was the AC for REQ-X?** → open `REQ-X-*.md`, read `## Acceptance Criteria`
- **Which REQ owns table Y?** → grep `data_owns: Y` in design/data-model.md, then trace back to REQ
- **How do I create a new REQ?** → use Templater hotkey, or copy `../00-overview/templates/REQ-template.md`

## Maintenance

- Updated automatically by `scripts/regen_indexes.py` (runs in CI on every PR).
- Manual content lives **above** the `<!-- auto-managed below -->` line and is preserved by the regen script. Everything **below** the marker is auto-generated and overwritten on each run.

<!-- auto-managed below -->

```

**Note on `file_naming` for heterogeneous folders:** Some folders (the repo root, `code-repo/services/`, `code-repo/libs/`, `deliverables/templates/`) don't have a single naming pattern. For these, set `file_naming: heterogeneous (see folder map below)` or `file_naming: heterogeneous (one file per service, varies)`. The validator accepts any non-empty string in this field; the convention is informational for human readers + AI navigation, not enforced as a regex.

#### 3.2.3 What goes in every `_index.md`

Every `_index.md` (regardless of folder) must contain:

1. **Frontmatter** with `folder`, `purpose`, `owner`, `file_naming`, `last_updated`, `ai_navigation_hint`.
2. **Purpose** — one-paragraph description of the folder's role.
3. **File naming convention** — pattern and an example.
4. **Frontmatter schema** for files in this folder (the most important section for AI grounding).
5. **Catalog** — table of current files with status and one-line summary. Auto-generated where possible (Dataview query embedded).
6. **Related folders** — links to upstream and downstream folders.
7. **Common questions** — 3–5 FAQs with pointers to the answer location. Reduces AI exploration cost dramatically.
8. **Maintenance** — who/what updates this file, and where the auto-managed boundary is.

Folder-specific additions:

| Folder | Extra `_index.md` content |
|--------|---------------------------|
| `requirements/` | REQ-ID range allocation by team |
| `spec/` | Which REQs each spec covers; spec version history |
| `design/` | Architecture diagram link; ADR catalog |
| `tasks/` | Current sprint pointer; sprint folder list with dates |
| `tasks/sprint-NN/` | Sprint goals, dates, planned vs actual REQs |
| `feedback/` | Triage routing matrix; SLA reminders |
| `feedback/sprint-NN/` | Feedback count by type; retro link |
| `incidents/` | Severity legend; postmortem template link |
| `prompts/` | Prompt library catalog; version policy |
| `deliverables/` | KRISA D01–D18 mapping with status and last regen date |
| `dashboard/` | What each dashboard file shows; refresh cadence |
| `decisions/` | DEC catalog with one-line decision summaries |

#### 3.2.4 Root `_index.md` (project root)

The project root's `_index.md` is the AI's front door. It is the *only* file an AI needs to read to know how to navigate the entire repo:

```yaml
---
folder: ROOT
purpose: Censof AI-DLC project — Project X — requirements repo
owner: PM (arvindh), BA lead (ba-rina), Tech lead (dev-3)
file_naming: heterogeneous (root holds README + _index + _prompts only; see folder map below for per-folder conventions)
last_updated: 2026-05-26
project_id: PROJ-X
client: Client-Name
contract_start: 2026-04-01
contract_end: 2026-12-31
current_sprint: sprint-03
playbook_version: 1.0
ai_navigation_hint: |
  Start here. This _index lists every top-level folder and the canonical path
  to answer common questions. Always read this before searching.
---

# Index — Project X

## Quick answers

| Question | Where |
|----------|-------|
| What is this project? | `00-overview/vision.md`, `00-overview/scope.md` |
| Who's on the team? | `00-overview/teams.md` |
| What is the current sprint? | `tasks/sprint-03/_index.md` |
| What's blocking? | `dashboard/dashboard.md` → "Blocked items" query |
| What were the acceptance criteria for REQ-X? | `requirements/REQ-X-*.md` → "## Acceptance Criteria" |
| What's the design for feature Y? | `design/_index.md` → catalog → `Y-design.md` |
| What did the client raise this sprint? | `feedback/sprint-03/_index.md` |
| What did we decide about Z? | `decisions/_index.md` (cross-cutting) or `design/adrs/_index.md` (architecture) |
| What is the security classification? | `00-overview/security.md` |
| Which Claude model are we using? | `00-overview/ai-config.md` |
| What prompts exist? | `prompts/_index.md` |
| Where are the KRISA Word docs? | `deliverables/_index.md` |

## Folder map

| Folder | Purpose | Index |
|--------|---------|-------|
| `00-overview/` | Project meta — vision, scope, stakeholders, teams, security, AI config | `00-overview/_index.md` |
| `requirements/` | One MD per REQ; source of truth | `requirements/_index.md` |
| `spec/` | Elaborations of REQs grouped by domain | `spec/_index.md` |
| `design/` | Technical design + ADRs | `design/_index.md` |
| `tasks/` | Sprint-organized TASK MDs | `tasks/_index.md` |
| `feedback/` | INBOX + triaged FB MDs + retros | `feedback/_index.md` |
| `decisions/` | Cross-cutting non-architecture decisions | `decisions/_index.md` |
| `incidents/` | Postmortems | `incidents/_index.md` |
| `prompts/` | Versioned Claude prompts | `prompts/_index.md` |
| `deliverables/` | Generated KRISA Word docs (D01–D18) | `deliverables/_index.md` |
| `raw-inputs/` | Workshop transcripts, source emails | `raw-inputs/_index.md` |
| `signoffs/` | Archived client signoff emails/docs | `signoffs/_index.md` |
| `dashboard/` | Live and exported dashboards | `dashboard/_index.md` |

## Where NOT to look
- Codebase lives in a separate repo: `github.com/censof/project-x-code` (not in this folder).
- Test code: in the code repo, not here. Cross-references via REQ-ID.
- KRISA Word source: not the source of truth. The MDs in this repo are. Word docs are generated views.

## AI behavior expectations
- Read this `_index.md` first when entering the repo.
- For any folder you need to work in, read its `_index.md` before opening any file in it.
- Do not grep the repo unless `_index.md`s do not answer the question. If you do grep, update the relevant `_index.md` with a new "Common questions" entry afterwards.
- When creating a new file, update the containing folder's `_index.md` catalog (or let the auto-regen script do it).
- When you discover information missing from an `_index.md`, propose an edit.
```

#### 3.2.5 Auto-regeneration

`_index.md` files contain two regions:

1. **Manual region (above `<!-- auto-managed below -->`):** Purpose, file naming, frontmatter schema, common questions, AI navigation hint, related folders. Edited by humans.
2. **Auto region (below the marker):** Catalog table of current files. Regenerated by `scripts/regen_indexes.py` on every PR (CI step).

The script (`scripts/regen_indexes.py`, see Appendix A.4):

- Applies the Tier A/B/C policy from 3.2.0 — skips Tier C folders entirely.
- Walks the tree recursively to discover folders (`find_md_folders`), then builds each folder's catalog non-recursively — one folder at a time, listing only that folder's direct children, not its subfolders' contents.
- For MD files, parses frontmatter to populate the catalog table; for non-MD files (e.g., `.docx` in `deliverables/`), records the file with its mtime.
- Writes a sorted catalog table below the auto-marker in `_index.md`.
- Bumps `last_updated` in the `_index.md` frontmatter **only when the catalog content actually changes** — re-running on an unchanged tree produces zero diff. (This keeps CI deterministic; without this guard, a daily date bump would fail every PR opened the day after a local regen.)
- Preserves everything above the marker.
- Calls `validate_index_frontmatter()` to confirm `_index.md` has the required frontmatter fields (folder, purpose, owner, file_naming, last_updated, ai_navigation_hint).
- For Tier A folders, also calls `validate_prompts()` on `_prompts.md` (required sections + required frontmatter).
- For Tier B folders, only validates `_prompts.md` if it exists.
- Fails the PR if any Tier A folder lacks either file, or any Tier B folder lacks `_index.md`.

**Out of scope for this script:** per-record frontmatter validation (REQ-XXX.md, TASK-XXX.md, etc.). That is enforced by `scripts/validate_frontmatter.py` (Appendix A.1), which is a separate CI step. The two scripts are independent but both run in the same CI workflow.

#### 3.2.6 Cost-saving impact

Measured on a sample project (REQ count: 80, files total: ~250):

| Task                                     | Without `_index.md` (tokens)         | With `_index.md` (tokens)               | Reduction |
| ---------------------------------------- | -------------------------------------- | ----------------------------------------- | --------- |
| "List all approved REQs for auth domain" | ~12,000 (grep + open many)             | ~2,500 (read root + folder index)         | 79%       |
| "What is the AC schema?"                 | ~8,000 (sample multiple REQs)          | ~1,500 (read folder index schema section) | 81%       |
| "Find decisions about database choice"   | ~15,000 (grep + open ADRs + decisions) | ~3,000 (root index → ADR index → file)  | 80%       |
| "What changed in sprint-03 feedback?"    | ~10,000 (open all FBs)                 | ~2,000 (read sprint index)                | 80%       |

Net effect across a project: ~75% reduction in AI navigation tokens — translates directly into Claude API cost savings.

#### 3.2.7 `_prompts.md` schema

While `_index.md` describes *what is here*, `_prompts.md` describes *what to do here*. **Tier A folders must contain this file; Tier B folders include it only when folder-specific operations exist (see 3.2.0).** It catalogs the operations valid in this folder, with trigger phrases, prompt links, and guardrails.

```yaml
---
folder: requirements
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Before executing any operation here, read _index.md first for context.
  Match the user's request to one of the OPs below by trigger phrase.
  If no OP matches, do NOT improvise — escalate to human with a clarification question.
---

# Operations — requirements/

## When you (the AI) are in this folder
You are working with system/business requirement MD files. Operations available:

## OP-1: Create new requirement from raw input
- **Trigger phrases:** "create requirement from raw input", "process workshop transcript", "ingest email into REQs", "draft REQs from this document"
- **Canonical prompt:** `../prompts/ingest-raw-input.md` (v1.2)
- **Inputs required:** Source file path(s) in `../raw-inputs/`
- **Output:** New `REQ-XXX-*.md` files with `status: draft`
- **Updates:** raw-input frontmatter (`status`, `generated_reqs`), `_index.md` catalog (via auto-regen)
- **Inline summary:** Read source from raw-inputs/, generate one draft REQ per atomic requirement, cite source line ranges, write [TBD] for ambiguous parts, do not invent ACs.

## OP-2: Refine acceptance criteria
- **Trigger phrases:** "improve AC for REQ-X", "make AC testable", "AC is too vague"
- **Canonical prompt:** `../prompts/refine-ac.md` (v1.0)
- **Inline summary:** Read REQ-X, rewrite each AC in Given/When/Then, verify observable/specific/singular. Flag any AC that cannot be made testable from source.

## OP-3: Drift check
- **Trigger phrases:** "check req drift", "find stale requirements", "verify req traceability"
- **Canonical prompt:** `../prompts/req-check.md` (v1.1)
- **Inline summary:** For each approved REQ, verify `spec_ref`, `design_ref`, `tasks`, `test_ref` all resolve. Report broken links and date drift.

## OP-4: Approve workflow
- **Trigger phrases:** "mark REQ approved", "client signed off REQ-X", "approve requirement"
- **Inline prompt (no canonical needed):**
```

  Update REQ-X frontmatter:

- status: approved
- approved: <today's date>
- approved_by: `<client name from message>`

  Append to ## Change Log section:

- `<date>`: Approved by `<name>` (signoff archived at signoffs/`<filename>`)

  Do not modify any other section. Do not modify _index.md auto-managed region.

```

## Forbidden in this folder
- Do NOT mark `status: approved` without client signoff evidence (email/document in `../signoffs/`)
- Do NOT delete REQ files — set `status: rejected` or `status: deferred` instead
- Do NOT edit `## Change Log` retroactively — only append
- Do NOT modify auto-managed region of `_index.md`
- Do NOT invent acceptance criteria not derivable from source

## Escalate to human if
- Source raw-input has conflicting requirements — flag for BA decision
- Two existing REQs cover same scope — propose merge, do not merge silently
- AC cannot be made specific from source — leave [TBD] + escalate
- Client signoff evidence missing — refuse approval, ask BA to provide

## Related operations in other folders
- Elaborate this REQ into spec → `../spec/_prompts.md` OP-1
- Design implementation → `../design/_prompts.md` OP-1
- Break into tasks → `../tasks/_prompts.md` OP-2
- Verify with tests → `../tests/_prompts.md` (in code repo)
- Process change request against this REQ → `../change-requests/_prompts.md` (OPs: draft-CR, approve-CR, link-to-REQ-revision)
- Triage incoming feedback that mentions this REQ → `../feedback/_prompts.md` (triage OP)
```

#### 3.2.8 What goes in every `_prompts.md`

Mandatory sections in every `_prompts.md`:

1. **Frontmatter** with `folder`, `purpose_of_this_file`, `canonical_prompts_location`, `last_updated`, `ai_behavior_hint`.
2. **Header:** "When you (the AI) are in this folder" — one-paragraph context.
3. **Operations (OP-1, OP-2, ...):** Each with trigger phrases, canonical prompt link, inputs required, outputs, inline summary or full inline prompt.
4. **Forbidden in this folder:** Explicit list of what AI must not do here. Critical for preventing destructive or out-of-scope actions.
5. **Escalate to human if:** Conditions that require BA/tech-lead intervention rather than AI autonomy.
6. **Related operations in other folders:** Cross-folder pointers so AI knows where to go next.

#### 3.2.9 Two-file vs one-file decision (rationale)

We use two separate files instead of merging into one `_meta.md` because:

| Reason                  | `_index.md`                          | `_prompts.md`                           |
| ----------------------- | -------------------------------------- | ----------------------------------------- |
| Audience                | Humans navigating + AI orienting       | AI executing                              |
| Update cadence          | Often (catalog auto-regen on every PR) | Rarely (operations stable across sprints) |
| Editor                  | Mostly auto-generated below the marker | Mostly hand-written by tech leads         |
| Failure mode if missing | AI wastes tokens grep-walking          | AI improvises and may take wrong action   |
| Validation rules        | Frontmatter shape, catalog integrity   | Frontmatter shape, OP completeness        |

Mixing them in one file would conflate concerns and make either auto-regen or hand-editing risky.

#### 3.2.10 Discovery sequence (the canonical AI flow)

When a user gives an AI a task in a project, the AI's first reads are:

1. **Root `_index.md`** — to learn project metadata and folder map (always present).
2. **Root `_prompts.md`** — to know which top-level operations exist (always present in repo root; root is Tier A).
3. **Target folder's `_index.md`** — once the AI identifies which folder applies (always present in Tier A and Tier B).
4. **Target folder's `_prompts.md`** — read if present. Tier A folders always have it. Tier B folders may or may not (only when folder-specific operations exist). If absent, the AI falls back to the inline guidance in the folder's `_index.md` or to the parent folder's `_prompts.md`.

Total reads to ground an AI: 3–4 files (~6,000 tokens). Without this convention, equivalent grounding costs 30,000+ tokens of grep and file sampling.

This sequence is reinforced by the `ai_behavior_hint` in every frontmatter, and by training BAs to explicitly remind Claude of it when starting a session ("Read root `_index.md` and `_prompts.md` first, then proceed.").

### 3.3 Why one requirement per file

A monolithic `requirements.md` produces noisy git diffs and merge conflicts. Per-file requirements give:

- Clean blame and history per requirement
- Parallel editing by multiple BAs without conflict
- Easy linking from code/tasks/tests via filename = REQ-ID
- Selective Word regeneration when one REQ changes

### 3.4 Requirement frontmatter schema (mandatory)

Every requirement file starts with YAML frontmatter:

```yaml
---
id: REQ-042
title: User login with 2FA via TOTP
status: approved              # draft | approved | in-dev | ready-for-acceptance | done | blocked | late-change | rejected | deferred
priority: high                # critical | high | medium | low
team: auth                    # Owning team
estimate_days: 3
created: 2026-05-01
created_by: ba-name
approved: 2026-05-05
approved_by: client-pm-name
implemented: null             # ISO date when status → done
last_updated: 2026-05-10      # Auto-updated by regen script; drives KRISA staleness detection
spec_ref: spec/auth-spec.md#login-2fa
design_ref: design/auth-design.md#2fa-flow
tasks: [TASK-101, TASK-102, TASK-103]
test_ref: tests/test_login_2fa.py
related_req: [REQ-041, REQ-043]
tags: [auth, security, mfa]
acceptance_criteria_count: 5
non_functional:
  performance: response < 500ms p95
  security: rate-limited, TOTP secret encrypted at rest
  accessibility: WCAG 2.1 AA
---
```

CI fails the PR if any required field is missing. See Appendix A.1 for the validation script.

### 3.5 Requirement body structure

After frontmatter, every REQ uses this structure:

```markdown
# REQ-042 — User login with 2FA via TOTP

## Context
Why this matters, business driver, regulatory link if any.

## Description
Plain-English description of the requirement, audience: BA and client.

## Acceptance Criteria
- AC-001: Given a user with 2FA enabled, When they enter correct password and valid TOTP, Then they are logged in and a session is created.
- AC-002: Given a user with 2FA enabled, When they enter correct password and invalid TOTP, Then login fails with "Invalid 2FA code" and the failure is logged.
- AC-003: Given a user without 2FA enabled, When they log in successfully, Then they are prompted to enable 2FA but can skip up to 3 times.
- AC-004: Given a user enters wrong TOTP 5 times in 10 minutes, When they try again, Then account is locked for 15 minutes and admin is notified.
- AC-005: Given a user lost their 2FA device, When they request recovery, Then they receive a recovery code via verified email.

## Non-Functional Requirements
- Performance: TOTP verification < 100ms server-side.
- Security: TOTP shared secret stored encrypted (AES-256-GCM). Rate limit: 10 attempts per minute per IP.
- Accessibility: TOTP input field labelled, supports screen readers.
- Auditability: Every login attempt logged with outcome, IP, user agent.

## Out of Scope
- SMS-based 2FA (deferred to REQ-091)
- Hardware token (YubiKey) support
- Per-device trust (remember this device)

## Open Questions
- [ ] What is the TOTP window tolerance? (default 30s, client to confirm)

## Change Log
- 2026-05-01: Drafted (BA)
- 2026-05-05: Approved by client (PM signoff in email, archived in OneDrive `signoffs/`)
- 2026-05-10: AC-003 updated — skip limit changed from "indefinite" to "3 times" after security review

## References
- Spec: [[auth-spec#login-2fa]]
- Design: [[auth-design#2fa-flow]]
- Tasks: [[TASK-101]], [[TASK-102]], [[TASK-103]]
- Tests: tests/test_login_2fa.py
- Related: [[REQ-041]] (login), [[REQ-043]] (password reset)
```

### 3.6 Spec, Design, Task, ADR, DEC, INC, CR — frontmatter templates

**Spec MD** (`spec/auth-spec.md`):

```yaml
---
id: SPEC-auth
title: Authentication & Authorization Specification
status: approved
covers_req: [REQ-001, REQ-041, REQ-042, REQ-043]
version: 1.2
last_updated: 2026-05-10
---
```

Body sections: User flows, state diagrams, error catalog, edge cases, integration points. One spec per domain, not per requirement (specs are bigger context).

**Design MD** (`design/auth-design.md`):

```yaml
---
id: DESIGN-auth
title: Authentication Design
status: approved
covers_spec: [SPEC-auth]
version: 1.1
last_updated: 2026-05-12
tech_lead: arvindh
---
```

Body sections: Component diagram, sequence diagrams, API endpoints (request/response schemas), data model (tables, indexes), error codes, security controls, observability hooks.

**Task MD** (`tasks/sprint-01/TASK-101-implement-totp.md`):

```yaml
---
id: TASK-101
title: Implement TOTP verification endpoint
sprint: sprint-01
status: in-progress           # todo | in-progress | review | done | blocked
assignee: dev-3
team: auth
req_ref: REQ-042
spec_ref: spec/auth-spec.md#login-2fa
design_ref: design/auth-design.md#2fa-flow
estimate_hours: 8
actual_hours: null
ai_assisted: true
ai_model: claude-opus-4-7
test_ref: tests/test_totp.py
pr: https://github.com/censof/project-x/pull/234
created: 2026-05-15
started: 2026-05-16
completed: null
last_updated: 2026-05-22       # v1.0: dev manually bumps on any status/field change. [PLANNED v1.1]: auto-bumped by close-task-on-PR-merge (A.5). Drives stale-task detection.
---
```

Body: Implementation notes, blockers, AI prompts used (link to `prompts/` if non-trivial).

**ADR MD** (`design/adrs/ADR-001-postgres.md`):

```yaml
---
id: ADR-001
title: Use PostgreSQL as primary datastore
status: accepted               # proposed | accepted | deprecated | superseded
date: 2026-04-08
deciders: [arvindh, dev-1, client-tech-lead]
supersedes: null
superseded_by: null
context_refs: [REQ-010, REQ-011]
---
```

Body sections: Context (why this decision is needed), Decision (what we picked), Consequences (what this implies — positive/negative), Alternatives considered. Lifecycle: proposed → accepted (one-way commit; if later replaced, set `superseded_by` and create a new ADR).

**DEC MD** (`decisions/DEC-001-go-with-onedrive.md`):

```yaml
---
id: DEC-001
date: 2026-05-15
type: tooling                  # tooling | process | scope | architecture | personnel
participants: [arvindh, client-pm, tech-lead-client]
status: decided                # pending | decided | superseded
supersedes: null
---
```

Body: Context, Options considered, Decision, Rationale, Consequences, Reviewed by. Use DEC for non-architecture cross-cutting decisions (tooling, process, scope); use ADR for architecture choices that affect code structure.

**INC MD** (`incidents/INC-001-login-outage.md`):

```yaml
---
id: INC-001
date: 2026-05-26
severity: SEV-1                # SEV-1 | SEV-2 | SEV-3 | SEV-4
status: closed                 # open | mitigated | resolved | postmortem-pending | closed
duration_min: 47
detected_by: alert             # alert | user-report | internal-qa
incident_commander: arvindh
comms_lead: ba-rina
affected_users: ~3000
affected_features: [login]
data_loss: false
data_breach: false
---
```

Body sections: Summary, Timeline, Root cause, What went well, What went badly, Action items, Related artifacts, Blameless retro. See 12.3 for the full postmortem template.

**CR MD** (`change-requests/CR-001-totp-window-60s.md`):

```yaml
---
id: CR-001
type: late-change              # late-change | new-requirement | clarification | scope-removal
raised_by: client-pm-name
raised_date: 2026-05-26
affects_req: [REQ-042]
sprint_raised: sprint-03
status: under-review           # under-review | approved | rejected | deferred
estimate_impact_days: 2
cost_impact_rm: 4000
schedule_impact: pushes REQ-045 to sprint-04
---
```

Body: Description, Justification (from client), Impact analysis, Decision. See 6.6 for the full CR template walk-through.

### 3.7 Raw-input MD frontmatter schema

Workshop transcripts, client emails, and source documents in `raw-inputs/` follow this lightweight schema. Raw inputs are immutable source material; they get processed into REQs (see `requirements/_prompts.md` OP-1) but the originals stay as the audit trail.

```yaml
---
id: RAW-001
source_type: workshop          # workshop | email | document | meeting-note | slack-export | call-transcript | screenshot
source_date: 2026-04-12
captured_by: ba-rina
participants: [client-pm, client-tech-lead, arvindh, ba-rina]   # for workshop/meeting; optional otherwise
status: unprocessed            # unprocessed | partially-processed | fully-processed | superseded
generated_reqs: []             # populated when processed: [REQ-042, REQ-043]
notes: |
  Free-form context — what this source covers, why it matters, any caveats.
---

# Auth Workshop — 2026-04-12

[Paste raw transcript / email body / extracted text here, unmodified.]
```

**Conventions:**

- `id` follows `RAW-NNN` numbering, allocated sequentially across all raw-input subfolders.
- File name: `YYYY-MM-DD-source-description.md` (e.g., `2026-04-12-auth-workshop-transcript.md`).
- Non-MD originals (`.pdf`, `.eml`, `.mp4`) kept alongside; Claude reads the `.md` companion file extracted from them.
- `status: fully-processed` is set when the source's content has been fully converted into REQs/Specs/Designs. Validator (A.1) then requires `generated_reqs` to be non-empty.

### 3.8 Glossary

`00-overview/glossary.md` is the single place for terminology — especially important for KRISA generation (Bahasa Malaysia translation):

```markdown
# Glossary

| English | Bahasa Malaysia | Definition |
|---------|-----------------|------------|
| Requirement | Keperluan | A statement of what the system must do |
| Specification | Spesifikasi | Detailed elaboration of a requirement |
| User | Pengguna | A person who interacts with the system |
| Two-Factor Authentication | Pengesahan Dua Faktor | Authentication using two independent factors |
| ... | ... | ... |
```

Claude references this when filling Word templates in BM.

### 3.9 Editing workflow

1. BA opens Obsidian in the requirements repo vault.
2. Creates/edits MD file; Obsidian git plugin auto-commits on save (with manual commit message option).
3. Push to GitHub triggers CI validation (frontmatter, REQ-ID format, links resolve).
4. PR reviewed by lead BA + tech lead before `approved` status; status change requires PR co-signoff.
5. OneDrive folder syncs the MD files for client visibility (read-only mirror).

---

## 4. Doc Generation (KRISA Templates)

### 4.1 KRISA template inventory

The 18 KRISA Word templates and their MD sources:

| Template | Title                               | Primary source(s)                             |
| -------- | ----------------------------------- | --------------------------------------------- |
| D01      | Pelan Pembangunan Sistem (PPS)      | `tasks/`, sprint plan, timeline             |
| D02      | Spesifikasi Keperluan Bisnes (BRS)  | `requirements/` (business view)             |
| D03      | Spesifikasi Keperluan Sistem (SRS)  | `requirements/` + `spec/` (system view)   |
| D04      | Spesifikasi Rekabentuk Sistem (SDS) | `design/`                                   |
| D05      | Pelan Migrasi Data                  | `design/data-model.md`, migration plan MD   |
| D06      | Spesifikasi Migrasi Data            | Migration spec MD                             |
| D07      | Pelan Integrasi Sistem              | `design/api-contracts.md`, integration plan |
| D08      | Spesifikasi Integrasi Data          | Integration spec MD                           |
| D09      | Dokumentasi Pangkalan Data          | `design/data-model.md` + DB schema dump     |
| D10      | Dokumentasi Kod Sumber              | Graphify output + code                        |
| D11      | Laporan Ujian Sistem                | Test results + REQ traceability               |
| D12      | Pelan Induk Pengujian               | Test strategy MD + acceptance criteria        |
| D13      | Pelan Ujian Penerimaan (UAT/PAT)    | UAT plan MD + acceptance criteria             |
| D14      | Laporan Ujian Penerimaan (UAT/PAT)  | UAT execution log                             |
| D15      | Laporan Migrasi Data                | Migration execution log                       |
| D16      | Laporan Penamatan Ujian             | Test closure report                           |
| D17      | Manual Pengguna Sistem              | `spec/` (user flows) + screenshots          |
| D18      | Laporan Serahan Sistem              | Handover checklist, all deliverables index    |

### 4.2 The "Claude in Word" workflow

**Setup once per project:**

1. Configure M365 connector to expose the `requirements-repo` OneDrive folder to Claude.
2. Verify Claude can read MD files via `sharepoint_search` and `read_resource`.
3. Place blank KRISA template in `deliverables/` folder.

**Per Word document:**

1. Open the KRISA template in Word.
2. Open Claude in Word side panel.
3. For each section, use the standard fill prompt (see 4.3 below).
4. Review the filled section against source MD.
5. Accept edits, or correct prompt and regenerate.
6. Move to next section. Do not let Claude fill multiple sections in one prompt.
7. At document end, run a consistency-check pass (see 4.5).
8. Stamp the document footer with generation metadata (see 4.6).

### 4.3 Standard fill prompt template

Stored in `prompts/fill-krisa-section.md`:

```
Fill section [SECTION_NUMBER] "[SECTION_TITLE]" of this KRISA template.

SOURCES (read these MDs from OneDrive folder /project-x/requirements-repo/):
- [LIST SPECIFIC FILES, e.g. requirements/REQ-042-user-login.md]
- [spec/auth-spec.md (sections: login-2fa)]
- 00-overview/glossary.md (for BM terminology)

RULES:
1. Preserve all existing Word styles (Heading 1, Heading 2, table styles, etc.). Do not flatten formatting.
2. Output in Bahasa Malaysia. Use glossary.md for term consistency.
3. Cite source REQ-IDs inline, e.g. "(REQ-042)".
4. If a piece of information is not in the source MDs, insert "[TBD: <what is missing>]" — do not invent.
5. Preserve all table structures from the template; fill cells, do not redesign tables.
6. After filling, append a hidden comment to the section listing the source files and sections used.

SCOPE:
Fill only section [SECTION_NUMBER]. Do not edit any other section. Do not modify the template's table of contents.

After completion, output a one-line summary: "Section [X.Y] filled from [sources]. [TBD count: N]."
```

### 4.4 Sectioning strategy

KRISA templates can be 50–200 pages. Fill in this order:

1. **Cover, version control, distribution list** (manual, from project metadata).
2. **Glossary section** of the template (auto-fill from `glossary.md`).
3. **Background, scope, stakeholders** (from `00-overview/`).
4. **Requirements/spec/design body** (REQ by REQ, or domain by domain).
5. **Diagrams** (manual — Claude does not produce Word-embedded diagrams reliably; export from draw.io/Mermaid and paste).
6. **Appendices and references** (auto-fill from MD indexes).

Avoid filling out-of-order; later sections may depend on earlier-defined terms.

### 4.5 Consistency check pass

After all sections filled, run this Claude prompt:

```
Read the entire filled Word document. Check for:

1. Contradictions: any two sections that state mutually exclusive facts.
2. Undefined acronyms: acronyms used but not defined in the glossary section.
3. Broken cross-references: "see section X.Y" where X.Y does not exist.
4. Unfilled placeholders: any remaining [TBD] markers — list them.
5. Style inconsistencies: heading levels, font, table borders that differ between sections.
6. REQ-ID drift: any REQ-ID cited in this doc but not present in the source requirements/ folder.

Report each issue with: section number, issue type, exact text, suggested fix.
Do not auto-fix; output a report only.
```

A human resolves each item.

### 4.6 Generation metadata footer

Every generated Word doc has this footer (or hidden document property):

```
Generated: 2026-05-26 14:30
Source MD commit: abc123def
Generator: Claude in Word (claude-opus-4-7)
Prompt version: prompts/fill-krisa-section.md@v1.3
Reviewed by: [BA name]
```

This makes drift detectable: if MD has moved past commit `abc123def`, the Word doc is stale and a re-gen is needed for the changed sections.

### 4.7 Regeneration trigger `[PLANNED v1.1 automation; today: manual]`

When a REQ changes:

1. **v1.0 (today, manual):** BA spot-checks the affected Word sections during the weekly status preparation. Process is: each Word doc's footer records `Source MD commit: <hash>`. BA compares that hash with the current commit on `requirements/REQ-XXX.md`'s git log. Any drift is flagged for regen.
2. **v1.1 (planned):** CI script (Appendix A.2 — currently a stub) compares each KRISA doc's footer commit hash against the git history of the source REQ MDs it cites. For each referenced REQ-XXX-*.md, runs `git log <footer-hash>..HEAD -- requirements/REQ-XXX*.md` — any commits returned = REQ has changed since the doc was generated = section is stale. Posts a list to Teams: "REQ-042 changed; affects sections 3.2.1 of D03-SRS, 4.1.5 of D04-SDS. Schedule regen." (The `last_updated` field in REQ frontmatter is a human-friendly secondary signal, but git history is the authoritative source.)
3. BA opens those sections in Word, re-runs the fill prompt for those sections only.
4. Updates the document footer with new commit hash.

Do not regenerate the whole document — only changed sections.

---

## 5. Teams & Ownership

### 5.1 Why team boundaries matter

Two teams editing the same file causes merge hell. Two teams writing to the same database table causes silent data corruption. Vague ownership causes bugs to ping-pong between teams. Clear boundaries solve all three.

### 5.2 The `teams.md` document

Every project starts with a `00-overview/teams.md`:

```markdown
# Teams

## Team Auth
- Lead: dev-3
- Members: dev-3, dev-4, dev-5
- Domain: Authentication, authorization, user identity
- Bounded context: Users, sessions, roles, permissions
- REQ-ID range: REQ-001 to REQ-099
- Code paths: `services/auth/**`, `libs/identity/**`
- DB tables (owns write): users, sessions, roles, permissions, user_roles
- DB tables (read-only): orgs, audit_log
- Deploy unit: auth-service (Docker image `censof/auth-service`)
- On-call: dev-3 primary, dev-4 secondary
- API contracts: documented in `design/api-contracts.md#auth`

## Team Billing
- Lead: dev-7
- Members: dev-7, dev-8
- Domain: Subscriptions, invoicing, payment processing
- Bounded context: Plans, subscriptions, invoices, payments
- REQ-ID range: REQ-100 to REQ-199
- Code paths: `services/billing/**`, `libs/payments/**`
- DB tables (owns write): plans, subscriptions, invoices, payments
- DB tables (read-only): users (auth team), orgs (platform team)
- Deploy unit: billing-service
- On-call: dev-7 primary, dev-8 secondary
- API contracts: documented in `design/api-contracts.md#billing`

## Team Platform
- Lead: dev-1
- Members: dev-1, dev-2
- Domain: Shared infrastructure, observability, CI/CD, dev environment
- Code paths: `infra/**`, `.github/workflows/**`, `libs/common/**`
- DB tables: orgs, audit_log, feature_flags
- On-call: dev-1 primary, dev-2 secondary
```

### 5.3 CODEOWNERS enforcement

In the code repository:

```
# .github/CODEOWNERS

# Auth team
services/auth/                @censof/team-auth
libs/identity/                @censof/team-auth

# Billing team
services/billing/             @censof/team-billing
libs/payments/                @censof/team-billing

# Platform team
infra/                        @censof/team-platform
.github/workflows/            @censof/team-platform
libs/common/                  @censof/team-platform

# Shared — both teams must approve
design/api-contracts.md       @censof/team-leads
```

PRs touching a path require approval from the owning team. Cross-team PRs require both teams to approve.

### 5.4 Inter-team contracts

When team A needs something from team B's domain:

1. Team A files a request in team B's backlog (a TASK MD with `team: billing` and `requested_by: team-auth`).
2. Team B reviews, agrees on API contract, both teams sign off.
3. Contract is added to `design/api-contracts.md` with version.
4. Team B implements; team A consumes.
5. Breaking changes to the contract require both teams to agree and version-bump.

Never bypass: never call into another team's internal code, only their published API.

### 5.5 REQ-ID ranges

Range assignment in `teams.md` prevents collision. When a new REQ is created:

- BA assigns the REQ to a team based on domain.
- REQ-ID auto-allocated from that team's range (next free number).
- Cross-team REQs (rare) get a `joint:` field in frontmatter listing both teams.

### 5.6 Cross-team escalation

When teams disagree (contract dispute, priority conflict):

1. Team leads attempt resolution.
2. If unresolved, escalate to tech lead / architect.
3. Decision logged as ADR in `design/adrs/`.
4. Both teams bound to the ADR.

---

## 6. Change Control & Gates

### 6.1 The change lifecycle

Every change — feature, fix, refactor, doc update — follows this path:

```
Idea / feedback / bug report
    ↓
INBOX.md (raw capture, 24hr SLA)
    ↓
Triage (BA + tech lead, classify & route)
    ↓
Becomes one of:
  • Bug → TASK directly (no REQ change)
  • Clarification → REQ MD edit + affected Spec/Design regen + TASK
  • Late change → REQ revision (versioned) + scope impact + client signoff + TASK
  • New requirement → New REQ + Spec + Design + TASK (full pipeline)
  • UX/cosmetic → Design MD edit + TASK
  • Performance → NFR section update + TASK
  • Rejected → Document rejection reason in INBOX entry
    ↓
PR opened with at least one work-item ID (REQ/TASK/FB/INC/CR/DEC) in title and commit messages
    ↓
CI gates: lint, test, frontmatter validation, work-item-ID check, secret scan
    ↓
Human review (CODEOWNERS-driven)
    ↓
Merge → CI deploys to dev → integration tests
    ↓
After sprint: merge to staging → UAT → merge to main → prod deploy
```

### 6.2 CI gates (automated)

These run on every PR. Failure blocks merge.

| Gate                                              | What it checks                                                                                                                                                                                                        | Tool                                                                                  |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Lint                                              | Code style                                                                                                                                                                                                            | ESLint / Ruff / golangci-lint                                                         |
| Format                                            | Code formatting                                                                                                                                                                                                       | Prettier / Black / gofmt                                                              |
| Unit tests                                        | Pass with ≥80% coverage of changed lines                                                                                                                                                                             | pytest / jest / go test                                                               |
| Integration tests                                 | Pass against real DB (containerized)                                                                                                                                                                                  | Docker compose + test suite                                                           |
| Frontmatter validation                            | All 10 record MD types (REQ, Task, FB, Spec, Design, ADR, DEC, INC, CR, Raw-input) have type-applicable mandatory + conditional fields, status enum is valid, non-record files (INBOX/backlog/retro/etc.) are skipped | Custom script (Appendix A.1)                                                          |
| Work-item ID in commits                           | Every commit message references at least one of: REQ-/TASK-/FB-/INC-/CR-/DEC-ID                                                                                                                                       | Custom Git hook (`.githooks/commit-msg`) + same regex in CI                         |
| Secret scan                                       | No credentials, API keys, tokens committed                                                                                                                                                                            | GitHub native secret scanning + custom grep in Actions for project-specific patterns  |
| License scan                                      | No GPL / AGPL contamination                                                                                                                                                                                           | Simple GitHub Actions step listing dep licenses; manual review on PR if new dep added |
| Frontmatter status transitions `[PLANNED v1.1]` | E.g.,`status: done` only if test_ref exists and tests pass                                                                                                                                                          | Partial today; reviewer enforces manually                                             |
| Cross-link validation `[PLANNED v1.1]`          | All `[[wiki-links]]` and `spec_ref:`/`design_ref:` resolve                                                                                                                                                      | Partial today; reviewer enforces manually                                             |
| KRISA staleness `[PLANNED v1.1]`                | If REQ changed, flag affected Word sections                                                                                                                                                                           | Stub in Appendix A.2; manual BA check today                                           |

### 6.3 Human gates

These are not automatable. They are policy.

| Gate                 | When                                   | Who                                        |
| -------------------- | -------------------------------------- | ------------------------------------------ |
| REQ approval         | Status `draft` → `approved`       | BA + client PM signoff (PR co-signed)      |
| Spec/Design signoff  | Spec or Design MD merge                | Tech lead approval                         |
| Sprint plan approval | Start of each sprint                   | Product owner / BA + tech leads            |
| Deploy to staging    | PR merged to `staging` branch        | Tech lead                                  |
| Deploy to prod       | PR merged to `main` + release tagged | Tech lead + ops lead, with client notified |
| Scope change         | Late change or new req mid-sprint      | Client written approval (email archived)   |

### 6.4 The `/req-check` Claude command

A slash command (stored in `prompts/req-check.md`) for periodic drift detection:

```
You are auditing the requirements repository for drift.

For each REQ in requirements/ with status: approved or in-dev:

1. Check that spec_ref points to a section that exists in the spec MD.
2. Check that design_ref points to a section that exists in the design MD.
3. Check that all listed tasks exist in tasks/ folders.
4. Check that test_ref points to a test file that exists in the code repo (use the GitHub MCP if needed).
5. Check that the REQ's last_updated date is not newer than the spec/design last_updated date (would indicate drift).
6. Check that all acceptance criteria are addressed by at least one task and one test.

Output a Markdown table:
| REQ-ID | Issue | Severity | Suggested fix |

Severity scale: critical (broken link), high (missing test), medium (date drift), low (formatting).
```

Run weekly. The BA fixes the high/critical items.

### 6.5 Code → MD sync: how completed work reaches the dashboard

The dashboard reads MD frontmatter. The codebase is where the actual work lives. Bridging the two is critical — otherwise the dashboard lies.

**v1.0 (today — manual):**

```
Dev finishes code
  → opens PR (commit message has at least one work-item ID — REQ/TASK/FB/INC/CR/DEC; commit-msg hook enforces)
  → PR reviewed and merged
  → Dev opens TASK-XXX.md in Obsidian
  → edits frontmatter:
       status: in-progress → done
       completed: <today>
       actual_hours: <number>
       pr: <PR URL>
  → save (Obsidian Git plugin auto-commits + pushes)
  → Dataview re-renders dashboard on next open → BA sees updated state
```

Trust model: developer discipline. The hook forces the ID in the commit, but does not force the MD update.

**Safety nets (v1.0):**

- **PR review checklist** includes: "Updated TASK-XXX.md `status: done` AND bumped `last_updated` in this PR or follow-up commit within 24hr?"
- **BA Friday spot-check:** open dashboard, find `tasks where status = "in-progress" AND last_updated > 5 days` → stale. Ping owner.
- **Sprint-close walkthrough (retro):** every task marked `done` must have `pr:` URL filled. Empty `pr:` = treat as not done.
- **REQ → done requires human:** REQ status flips to `done` only after BA verifies tests pass and client signs off. Never auto-flipped.

**Known v1.0 gap — `last_updated` freshness is not validator-enforced.** The validator (A.1) checks that `last_updated` is present and non-empty, but does NOT check that the value reflects the most recent actual edit. A dev could change task fields without bumping `last_updated`; the validator passes and the dashboard's stale-task detection misreads the task as fresh. This gap is closed by the PLANNED v1.1 auto-close-TASK script (A.5), which bumps `last_updated` automatically on PR merge. Until then: discipline + PR checklist + Friday spot-check are the safety net. Document this gap to client honestly during steering committees if asked.

**Why manual is acceptable at Censof scale:**

- Project teams are small (3–8 devs). Social enforcement works.
- One checklist item in PR review covers it.
- Cost of building auto-sync > cost of the discipline at this scale.

**v1.1 — auto-sync `[PLANNED]`:**

When team size or project count outgrows manual discipline, build these four scripts:

| Layer                | What it does                                                                                                                                                                                       | Trigger                                           | Stub         |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------ |
| Auto-close TASK      | On PR merge, parse commit messages for TASK-IDs, flip those TASK MDs to `status: done`, fill `completed`, `pr:`                                                                              | GitHub Action on `pull_request.closed (merged)` | Appendix A.5 |
| Test coverage map    | Scan `tests/` for REQ-ID references in test names/docstrings, build `dashboard/req-test-coverage.md` showing which REQs have tests + pass rate                                                 | Nightly cron + on CI run                          | Appendix A.6 |
| REQ readiness check  | When all REQ's tasks are `done` and tests pass + no `[TBD]` in body, propose flip to `ready-for-acceptance` (intermediate state) + post to Teams for BA review. Never auto-flip to `done`. | On TASK MD change                                 | Appendix A.7 |
| Design ↔ code drift | Compare `design/api-contracts.md` endpoints + `design/data-model.md` tables against Graphify graph + DB schema introspection. Flag drift.                                                      | Nightly cron                                      | Appendix A.8 |

Until v1.1 ships, the four scripts are stubs (see Appendix). The dashboard remains accurate only as long as devs update MDs after merging. Treat this as a known limitation, monitored by the Friday spot-check.

### 6.6 The change request template

Change Requests live in their own folder: `change-requests/CR-NNN-short-title.md`. A CR is a *proposal* — when approved, it spawns either a REQ revision (new version of existing REQ) or a new REQ. The CR file itself stays in `change-requests/` as the historical record of the proposal + decision. Use this template:

```yaml
---
id: CR-001
type: late-change              # late-change | new-requirement | clarification | scope-removal
raised_by: client-name
raised_date: 2026-05-26
affects_req: [REQ-042]
sprint_raised: sprint-03
status: under-review           # under-review | approved | rejected | deferred
estimate_impact_days: 2
cost_impact_rm: 4000
schedule_impact: pushes REQ-045 to sprint-04
---

## Description
Client wants TOTP window changed from 30s to 60s tolerance.

## Justification (from client)
Users in poor network areas experience TOTP timeouts.

## Impact analysis (BA + tech lead)
- Code change: small (config update)
- Spec change: yes (security trade-off documented)
- Security review: required (longer window = larger attack surface)
- Testing: regression on auth flow

## Decision
[Approved / Rejected / Deferred] on [date] by [client signoff name].
Email archived: signoffs/CR-001-signoff.eml
```

---

## 7. PM Dashboard

### 7.1 What the dashboard answers

The dashboard exists to answer these questions without anyone asking:

1. How many REQs are in each status?
2. What is the burndown for the current sprint?
3. Which REQs are blocked, and by what?
4. Which team is over- or under-loaded?
5. How much scope has been added since project start?
6. What is the test coverage by REQ?
7. Which KRISA documents are stale (source MD changed since last regen)?
8. What is the bug escape rate?
9. What is the velocity trend?

### 7.2 Dashboard tiers (all in Obsidian)

Different audiences, same underlying MD. Different views.

**Tier 1 — Developer/BA daily view (`dashboard/dashboard.md`):**

````markdown
# Project X — Live Dashboard

## REQ status summary
```dataview
TABLE length(rows) AS Count
FROM "requirements"
GROUP BY status
```

## My open tasks
```dataview
TABLE status, sprint, req_ref, estimate_hours
FROM "tasks"
WHERE assignee = this.file.name AND status != "done"
SORT sprint ASC, status ASC
```

## Sprint burndown (current sprint)
```dataview
TABLE status, assignee, estimate_hours, actual_hours
FROM "tasks/sprint-03"
SORT status ASC
```

## Blocked items
```dataview
TABLE blocked_by, team, file.mtime AS "Last updated"
FROM "requirements" OR "tasks"
WHERE status = "blocked"
```

## REQs done but no test
```dataview
LIST
FROM "requirements"
WHERE status = "done" AND !test_ref
```

## Feedback this sprint
```dataview
TABLE type, severity, status, linked_task
FROM "feedback/sprint-03"
SORT severity ASC, status ASC
```

## Late changes log
```dataview
TABLE raised_date, estimate_impact_days, status
FROM "requirements"
WHERE status = "late-change"
SORT raised_date DESC
```
````

**Tier 2 — Sprint Kanban board (Obsidian Kanban plugin):**

A `dashboard/sprint-board.md` rendered as a Kanban board with columns (Todo / In Progress / Review / Done / Blocked). Cards = task MD files. Drag a card across columns → MD frontmatter `status:` updates automatically. Single source of truth maintained.

**Tier 3 — Velocity & trend charts (Obsidian Charts plugin):**

`dashboard/velocity.md` uses Dataview + Charts to render line/bar charts:

- Velocity per sprint (estimate_days done)
- Bug count trend over sprints
- Scope change cumulative
- Health score history

Plain MD, renders as visual chart inline. Screenshots exportable for status reports.

**Tier 4 — Client executive view (HTML export from Obsidian):**

Obsidian's built-in "Export to HTML" generates a static site from the dashboard MDs. Hosted on OneDrive as a folder; client opens `index.html` in browser. Refreshed weekly by BA (one-click export). No Power BI, no extra tool.

For deeper client view, the auto-generated weekly status PDF (Tier 5) handles narrative + numbers.

**Tier 5 — Auto-generated weekly status PDF (Claude):**

Friday 4pm, BA runs Claude prompt that:

1. Reads all MD files in `requirements-repo/` (via M365 connector → OneDrive).
2. Computes metrics by parsing frontmatter.
3. Writes a 1-page status report directly into a Word template (`deliverables/templates/weekly-status.docx`).
4. BA reviews in Word, edits if needed, exports to PDF, sends via Outlook.

Claude prompt stored at `prompts/weekly-status-report.md`. See Appendix B.

### 7.3 Required frontmatter for dashboard to work, by MD type

The dashboard depends on consistent frontmatter. Fields are **scoped per MD type** and split into two classes:

- **Mandatory** — CI validator (A.1) blocks the PR if missing. Required at every status.
- **Conditional** — required only when a status-dependent predicate holds (e.g., `approved` field required once `status >= approved`). CI validator enforces these via `CONDITIONAL_REQUIRED` in A.1.

Fields not in either class are optional but may be queried by the dashboard if present.

**Requirements (`requirements/REQ-*.md`):**

- *Mandatory:* `id`, `title`, `status`, `priority`, `team`, `created`, `last_updated`
- *Conditional:* `approved`, `approved_by` (when `status ∈ {approved, in-dev, ready-for-acceptance, done}`); `implemented` (when `status == done`)
- *Used by dashboard for:* status queries, prioritization, team load, velocity, drift detection

**Tasks (`tasks/sprint-NN/TASK-*.md`):**

- *Mandatory:* `id`, `title`, `status`, `team`, `req_ref`, `sprint`, `estimate_hours`, `last_updated`
- *Conditional:* `assignee` (required when `status != todo`)
- *Used by dashboard for:* burndown, capacity, stale-task detection, traceability

**Feedback (`feedback/sprint-NN/FB-*.md`):**

- *Mandatory:* `id`, `sprint_raised`, `source`, `type`, `severity`, `status`, `related_req`
- *Used by dashboard for:* feedback-per-REQ, severity distribution, triage age

**Spec (`spec/*.md`):**

- *Mandatory:* `id`, `title`, `status`, `version`, `last_updated`, `covers_req`

**Design (`design/*.md`):**

- *Mandatory:* `id`, `title`, `status`, `version`, `last_updated`

**ADR (`design/adrs/ADR-*.md`):**

- *Mandatory:* `id`, `title`, `status`, `date`, `deciders`

**DEC (`decisions/DEC-*.md`):**

- *Mandatory:* `id`, `date`, `type`, `participants`, `status`

**INC (`incidents/INC-*.md`):**

- *Mandatory:* `id`, `date`, `severity`, `incident_commander`, `data_loss`, `data_breach`, `status`

**CR (`change-requests/CR-*.md`):**

- *Mandatory:* `id`, `type`, `raised_by`, `raised_date`, `affects_req`, `status`

**Raw inputs (`raw-inputs/**/*.md`):**

- *Mandatory:* `id`, `source_type`, `source_date`, `captured_by`, `status`
- *Conditional:* `generated_reqs` (required and non-empty when `status ∈ {partially-processed, fully-processed}`)

**Sprint retros (`feedback/sprint-NN/retro.md`):**

- Not enforced by validator (file is in `SKIP_FILES`). Convention: `sprint`, `start_date`, `end_date`, `attendees`.

CI validator (`scripts/validate_frontmatter.py`) reads the MD type from the file's folder path (via `classify()`, using `Path.parts` membership) and applies only the type-applicable mandatory + conditional lists. See Appendix A.1.

### 7.4 Dashboard refresh mechanism

Three distinct layers — keep them straight (Layers 1 + 2 are v1.0; Layer 3 is `[PLANNED v1.1]`):

**Layer 1 — Live Dataview rendering (v1.0, today).** `dashboard/dashboard.md` is a hand-authored file containing inline Dataview query blocks (see §7.2 Tier 1 example). The file content itself does not change between renders — Obsidian's Dataview plugin re-evaluates the queries every time the file is opened and renders fresh results based on the current state of all REQ/Task/FB MDs. There is no scheduled script overwriting `dashboard.md`; if you edit a query, you save the file like any normal MD edit.

Queries may either:
- Live **inline** in `dashboard.md` (the §7.2 example style — simplest), or
- Live as separate `.md` files in `dashboard/queries/` and be **embedded** in `dashboard.md` via Obsidian transclusion (`![[queries/blocked-items]]`) — useful when the same query is reused across multiple dashboard files.

Either style works. Censof default: inline in `dashboard.md` for the primary view, factored into `dashboard/queries/*.md` only when reuse demands it.

**Layer 2 — Client-facing HTML snapshot (v1.0, manual weekly).** Every Friday, the BA does an Obsidian "Export to HTML" (one click) on `dashboard.md` (and `velocity.md`, `sprint-board.md` as needed). The exported HTML is dropped into `dashboard/exports/` (Tier C, gitignored or auto-generated) and synced via OneDrive to a read-only client folder. Client opens `index.html` in any browser; queries no longer render live but the values reflect the snapshot moment. This is the "frozen dashboard" the client sees in steering committees.

**Layer 3 — Historical snapshots `[PLANNED v1.1]`.** A nightly script (not yet implemented) would write `dashboard/snapshots/dashboard-YYYY-MM-DD.md` capturing computed metric values for that day — enabling trend analysis ("how did velocity track over the last 12 weeks?"). Until the script lands, trend data is read from Dataview live (`file.mtime` and frontmatter dates already give most of what's needed). The script, when built, would be added to Appendix A as a sibling of `regen_indexes.py` and run via nightly cron on the VPS, not via GitHub Actions.

**Important:** No automation in v1.0 overwrites `dashboard.md`. Manual edits to it are preserved. The standard stack contains no scheduled script that mutates dashboard files — refresh happens via Dataview re-rendering when Obsidian opens the file.

### 7.5 Health score formula

The composite project health score (0–100) shown to client:

```
Health = 0.25 × (REQs done / REQs planned)
       + 0.20 × (1 − bug_escape_rate)
       + 0.15 × (1 − scope_creep_ratio)
       + 0.15 × (test_coverage_by_req)
       + 0.15 × (on_time_delivery_ratio)
       + 0.10 × (1 − stale_doc_ratio)
```

Each component capped at [0, 1]. Computed weekly. Trend (up/down) more important than absolute.

---

## 8. Sprint Feedback Loop

### 8.1 Why feedback is a separate system

Sprint feedback is structurally different from initial requirements:

- It arrives at high frequency, low signal-to-noise.
- It is emotionally loaded (client just saw their product and reacted).
- It comes through many channels (demo verbal, email, Slack, Teams, Word comments).
- It must be classified before it can be acted on.

Without a feedback system, all of it routes directly to developers as urgent fires. Scope creeps invisibly.

### 8.2 The INBOX

`feedback/INBOX.md` is the dump zone. Anyone can append. Format is loose:

```markdown
## 2026-05-26 — Client demo session

- Client PM: "The login button on Safari doesn't work for me."
- Client tech lead: "Can we add SMS as an alternative 2FA?"
- Client ops: "The error message when TOTP fails is confusing. Can we make it clearer?"
- Client PM: "Performance felt slow on the dashboard. Took 3 seconds to load."

## 2026-05-27 — UAT findings (email from client QA)

- Forgot-password email doesn't arrive within 60 seconds.
- "Forgot Password" link spelt as "Forget Password" on the login page.
- After password reset, user is not auto-logged in (we expected this).
```

BAs scrape Slack/email/Teams into the INBOX within 24 hours. The 24-hour SLA is a hard rule.

### 8.3 Triage session

Every Tuesday (or after every demo), BA + tech lead spend 1 hour triaging the INBOX.

The `/triage` Claude command (prompt in `prompts/triage-feedback.md`):

```
Read feedback/INBOX.md from the last 7 days. For each item:

1. Classify type: bug | clarification | late-change | new-req | ux | perf | duplicate | unclear
2. Identify related REQ-IDs (search requirements/ for relevant ones)
3. Suggest severity: critical (blocks usage) | high (degrades usage) | medium (annoyance) | low (cosmetic)
4. Suggest routing: bug → TASK | clarification → REQ edit | late-change → CR + REQ revision | new-req → new REQ pipeline | ux → design edit
5. Generate a draft FB-XXX MD file using the template embedded in this folder's `_prompts.md` (under OP: triage-INBOX)

Output one FB-XXX MD per item, in feedback/sprint-NN/. Do not delete the INBOX item; mark it processed by appending [processed → FB-XXX] to the original line.
```

BA and tech lead review each generated FB MD, accept/edit/reject. Misclassification is the most common error — humans must verify.

### 8.4 FB MD template

Embedded as a reference template in `feedback/_prompts.md` (so the triage OP can spawn FB files using it). Format:

```yaml
---
id: FB-042
sprint_raised: sprint-03
sprint_resolved: null
source: client-demo            # client-demo | client-uat | client-email | internal-qa | internal-retro | production-incident
raised_by: client-pm-name
raised_date: 2026-05-26
type: bug                      # bug | clarification | late-change | new-req | ux | perf | duplicate
severity: high                 # critical | high | medium | low
status: triaged                # triaged | accepted | in-progress | done | rejected | deferred | duplicate
duplicate_of: null             # If status: duplicate, set to the canonical FB-ID (e.g., FB-031)
related_req: [REQ-042]
resolution_type: bug-fix       # bug-fix | req-update | new-req | design-update | wont-fix | duplicate
linked_task: TASK-205
linked_cr: null                # If late-change, the CR-XXX ID
estimate_days: 0.5
---

## Description
Client reports login button does not respond on Safari 17 on macOS Sonoma.

## Reproduction steps (BA verified)
1. Open https://staging.project-x.censof.com on Safari 17.4 / macOS 14.4.
2. Enter valid credentials.
3. Click "Login" button.
4. Observe: no response, no network call in dev tools.

Confirmed reproducible: yes.
Confirmed on Chrome: no (works fine).

## Triage classification
Type: bug.
Justification: REQ-042 AC-001 states "all major browsers". Safari 17 is in scope. Code does not meet acceptance criteria → bug, not late change.

## Resolution
Bug in event handler — Safari doesn't fire `click` on `<button type="submit">` inside a form with `novalidate`. Switched to `submit` event listener.

Fixed in TASK-205, PR #287, merged 2026-05-27.

## Related
- REQ: [[REQ-042]]
- Task: [[TASK-205]]
- PR: #287
```

### 8.5 Sprint retro

At sprint end, generate `feedback/sprint-NN/retro.md`:

```yaml
---
sprint: sprint-03
start_date: 2026-05-13
end_date: 2026-05-26
duration_days: 14
attendees: [arvindh, dev-1, dev-2, dev-3, ba-rina, qa-faiz]
---

## Sprint stats
- Planned REQs: 8 (40 estimate_days)
- Completed REQs: 7
- Carried over: 1 (REQ-045 — client SSO delay)
- Velocity: 35 days (88% of plan)
- Bugs found this sprint: 12 (10 closed, 2 deferred)
- Late changes accepted: 1 (CR-001, +2 days)
- New reqs introduced: 1 (REQ-091)

## What went well
- TOTP implementation finished 1 day early; AI-assisted code review caught 2 security issues before merge.
- BA + Claude triage cut feedback-to-FB conversion time from 2 days to 4 hours.

## What went badly
- Safari bug should have been caught in pre-merge testing — our test matrix only covers Chrome.
- Sprint plan included REQ-045 despite known SSO blocker on client side; should have deferred at planning.

## Action items
- AI-001: Add Safari to CI test matrix. Owner: dev-1. Due: sprint-04 start. Tracked as TASK-301.
- AI-002: At sprint planning, mark REQs with external blockers explicitly; do not commit until blocker cleared. Owner: BA. Due: immediately.
- AI-003: Improve REQ-042-style acceptance criteria to enumerate browsers/versions explicitly. Owner: BA. Due: ongoing for all future REQs.

## Metrics trend (vs prior sprints)
- Velocity: 28 → 32 → 35 (trending up)
- Bug escape rate: 18% → 14% → 11% (improving)
- Late change count: 3 → 2 → 1 (improving)
```

### 8.6 Routing decision matrix

Triage output routes each FB:

| Type            | Resolution                           | MD change                                          | Code change         | Client signoff               |
| --------------- | ------------------------------------ | -------------------------------------------------- | ------------------- | ---------------------------- |
| Bug             | Fix code, no REQ change              | FB MD created                                      | Yes                 | No                           |
| Clarification   | Edit REQ MD, regen affected docs     | REQ + Spec/Design (if needed)                      | Maybe               | Maybe (if behaviour changes) |
| Late change     | Versioned REQ revision, scope impact | New REQ vN+1, CR MD                                | Yes                 | **Yes — written**     |
| New requirement | Full pipeline                        | New REQ + Spec + Design                            | Yes (future sprint) | **Yes — written**     |
| UX              | Edit Design MD                       | Design                                             | Yes                 | No (unless major)            |
| Performance     | NFR section update                   | REQ NFR                                            | Yes                 | No                           |
| Duplicate       | Link to existing FB                  | FB `status: duplicate`, `duplicate_of: FB-xxx` | No                  | No                           |
| Wont-fix        | Document reason                      | FB status: rejected with reason                    | No                  | Yes (notify)                 |

### 8.7 Feedback metrics that matter

| Metric                                                     | Why                                           |
| ---------------------------------------------------------- | --------------------------------------------- |
| Triage age (raised → triaged)                             | Should be ≤48hr; longer = client loses trust |
| Bug escape rate (UAT bugs / total REQs delivered)          | Quality gate effectiveness                    |
| Late-change frequency per sprint                           | Scope discipline (theirs and yours)           |
| Feedback per REQ (count)                                   | High = spec was unclear; fix the template     |
| Carryover rate (FBs not closed in sprint they were raised) | Capacity / triage efficiency                  |
| Reopen rate (FB closed then reopened)                      | Quality of fix                                |
| Time-to-fix by severity                                    | Responsiveness                                |

Trend over time, not absolute values.

---

## 9. Quality Gates & Definition of Done

### 9.1 The principle

"Done" means the same thing to every team member. It is a written checklist, not subjective judgment. Each stage has its own DoD.

### 9.2 Definition of Done — per stage

**Requirement DoD:**

- [ ] Frontmatter complete (all mandatory fields)
- [ ] Has REQ-ID following naming convention
- [ ] Description in plain English (non-technical reader can understand)
- [ ] At least 3 acceptance criteria in Given/When/Then format
- [ ] Non-functional requirements section completed (performance, security, accessibility)
- [ ] Out-of-scope section explicit (prevents future scope debate)
- [ ] Open questions section addressed or explicitly deferred
- [ ] Related REQs cross-linked
- [ ] Approved by BA
- [ ] Signed off by client (PR co-approval or email archived in `signoffs/`)
- [ ] Status set to `approved`

**Spec DoD:**

- [ ] All user flows documented (happy path + at least 2 edge cases)
- [ ] All error states enumerated
- [ ] State diagram or sequence diagram included (Mermaid in MD)
- [ ] Integration points listed (which external systems, contracts)
- [ ] Covers all REQ-IDs listed in frontmatter
- [ ] Peer-reviewed by another spec author
- [ ] Tech lead approved

**Design DoD:**

- [ ] Component diagram present
- [ ] All API endpoints documented (path, method, request, response, error codes)
- [ ] Data model: tables, columns, types, indexes, constraints, relationships
- [ ] Security controls listed (authn, authz, input validation, encryption)
- [ ] Observability hooks defined (what metrics, what logs, what traces)
- [ ] Performance budget stated (latency, throughput, resource limits)
- [ ] Architecture decisions documented as ADRs
- [ ] Tech lead approved
- [ ] Reviewed by ops/security if applicable

**Task DoD:**

- [ ] Has TASK-ID
- [ ] Linked to a REQ-ID
- [ ] Estimate provided (≤3 days; split if larger)
- [ ] Assignee identified
- [ ] Acceptance criteria from the REQ are explicitly listed in the task
- [ ] Test cases enumerated (at least one per AC)
- [ ] Status `todo`

**Code DoD:**

- [ ] Compiles without errors
- [ ] Lint passes
- [ ] Format check passes
- [ ] Unit tests written (≥80% coverage of new code)
- [ ] Integration tests written for any new API/DB interaction
- [ ] Tests reference REQ-ID in name or comment
- [ ] No `console.log` / `print` / debug code left
- [ ] No commented-out code
- [ ] No `TODO` without a TASK-ID
- [ ] Security checklist: input validated, no SQL injection, no XSS, no hardcoded secrets
- [ ] Performance check: no obvious N+1 queries, no unbounded loops over user input
- [ ] PR description references at least one work-item ID (REQ/TASK/FB/INC/CR/DEC). Typical feature PR cites REQ-ID + TASK-ID; bug-fix PR cites FB-ID; hotfix PR cites INC-ID
- [ ] Code review approved (CODEOWNERS satisfied)
- [ ] AI-generated code reviewed by human, not blind-merged
- [ ] CI green
- [ ] Merged
- [ ] **TASK-XXX.md frontmatter updated** within 24hr of merge: `status: done`, `completed: <date>`, `pr: <URL>`, `actual_hours: <number>` *(manual today; auto-closed by A.5 in v1.1)*

**Test DoD:**

- [ ] Test names reference REQ-ID or AC-ID
- [ ] Every acceptance criterion has at least one test
- [ ] Tests cover happy path AND edge cases AND error paths
- [ ] Tests pass locally and in CI
- [ ] Test data is anonymized/synthetic (no real PII)
- [ ] Tests are deterministic (no flakes)
- [ ] Regression suite updated

**Deploy DoD:**

- [ ] Staging deployment green for ≥24 hours
- [ ] Smoke tests pass post-deploy
- [ ] Rollback plan documented in release notes
- [ ] Database migrations have a tested rollback
- [ ] Monitoring alerts configured for new endpoints/features
- [ ] Feature flag set up if feature is risky
- [ ] Release notes written (user-facing changes)
- [ ] Client notified of deployment window
- [ ] On-call notified

**Sprint DoD:**

- [ ] Demo conducted with client
- [ ] All planned REQs either done or explicitly carried over
- [ ] Retro held and `retro.md` written
- [ ] Feedback triaged within 48hr of demo
- [ ] Dashboard updated
- [ ] Status report sent to client

### 9.3 Two-pass AI review

For non-trivial AI-generated artifacts (code, specs, documentation), use two-pass review:

1. **Pass 1 — Generation:** Claude A generates the artifact, given the source MDs as grounding.
2. **Pass 2 — Critique:** Claude B (separate session, fresh context) is given the artifact and the DoD checklist, asked to find violations.
3. **Pass 3 — Human:** Developer/BA reviews Claude B's critique, accepts/rejects, edits artifact.

The two-pass approach catches hallucination cheap. Claude B has no investment in defending Claude A's choices.

Prompt for Pass 2:

```
You are reviewing an AI-generated [artifact type]. Your job is to find problems, not to be polite.

Source of truth: [paste source MDs or link]
Definition of Done: [paste relevant DoD checklist]
Artifact under review: [paste artifact]

For each item in the DoD, check the artifact and report:
- Pass / Fail / Unclear
- If Fail: exact location of the violation and suggested fix.
- If Unclear: what additional information is needed.

Also report:
- Any claims in the artifact that cannot be traced to the source.
- Any inconsistencies between sections.
- Any obvious omissions a domain expert would notice.

Be strict. False positives are acceptable; false negatives are not.
```

### 9.4 Acceptance criteria patterns

Acceptance criteria are the bridge between requirement and test. They must be specific enough to write tests against.

**Bad AC:** "Users should be able to log in."

**Good AC:** "Given a registered user with verified email, When they submit correct email and password, Then they receive a session token and are redirected to /dashboard within 2 seconds."

Patterns:

- `Given <preconditions>, When <action>, Then <outcome>` (functional)
- `Given <load condition>, When <action>, Then <performance metric>` (performance)
- `Given <invalid input>, When <action>, Then <specific error response>` (error handling)
- `Given <unauthorized user>, When <action>, Then <403 + log entry>` (security)

Every AC should be:

- **Specific:** Not "fast" but "≤500ms p95".
- **Observable:** A test can verify it (not "user feels happy").
- **Singular:** One outcome per AC. Compound ACs split into multiple.
- **Negative-aware:** Cover failure modes, not just happy path.

---

## 10. Security & Compliance

### 10.1 Why security must be designed in

Security retrofitted is security with holes. The requirements, design, and DoD all incorporate security from day one.

### 10.2 Data classification

Every project starts with a data classification exercise. Document in `00-overview/security.md`:

```markdown
# Security & Data Classification — Project X

## Data inventory

| Data | Classification | Storage | Encryption / Hashing | Retention |
|------|---------------|---------|----------------------|-----------|
| User email | PII / Confidential | PostgreSQL | Encryption: at-rest (TDE) + in-transit (TLS 1.3) | Active + 1 year |
| User password | Restricted | PostgreSQL | **Hashing**: bcrypt cost 12 (not reversible — passwords are hashed, never encrypted) | Active |
| TOTP secret | Restricted | PostgreSQL | Encryption: AES-256-GCM. Key stored in OS env var on prod host; rotated per `code-repo/infra/secret-rotation-log.md`. *(KMS-managed keys are an optional upgrade for higher-security clients — not in default stack.)* | Active |
| Session token | Restricted | Redis | Encryption: TLS in transit; ephemeral in memory | 24h |
| Invoice data | Confidential | PostgreSQL | Encryption: at-rest + in-transit | 7 years (regulatory) |
| Audit log | Confidential | Append-only files on VPS (`chattr +a`), rotated to OneDrive monthly | Encryption: at-rest (LUKS) + in-transit | 7 years |
| Client business reports | Confidential | OneDrive | Encryption: M365 native (at-rest + in-transit) | Per client contract |
| Marketing copy | Public | Git | None required | Permanent |

## AI usage rules

| Tier | Allow Claude to read | Allow Claude to write | Notes |
|------|---------------------|----------------------|-------|
| Public | Yes | Yes | No constraints |
| Internal | Yes | Yes (with audit log) | Code, design, non-PII |
| Confidential | Yes (with NDA + audit log) | Yes (human review) | Client data under NDA |
| Restricted | **No** | **No** | Passwords, secrets, TOTP — never in any AI prompt |

Any developer copying restricted data into a Claude prompt is in violation.

## Compliance frameworks applicable

- PDPA (Personal Data Protection Act, Malaysia) — applies (we handle Malaysian users' PII)
- GDPR — not applicable (no EU users)
- PCI-DSS — not applicable (no card data; payments processed by Stripe)
- SOC 2 — internal Censof target by Q4 2026

## DPO contact

Data Protection Officer: dpo@censof.com
```

### 10.3 PDPA-specific controls

For Malaysian projects:

- Obtain explicit consent for processing personal data, including AI processing.
- Document lawful basis (contract, consent, legitimate interest).
- Provide data subject access mechanism (export user data on request).
- Provide deletion mechanism (right to be forgotten).
- Log all access to personal data (audit log).
- Notify DPO of any data breach within 72 hours; client + regulator if material.
- Vendor (Claude API) data flow: document in Records of Processing Activities.

### 10.4 Secrets management

Within the standard stack: no dedicated secret vault. Secrets live in GitHub Secrets (for CI/CD) and OS-level environment variables on VPS/production hosts. Local dev uses `.env` files, never committed.

**Rules:**

1. Never commit secrets to Git. Pre-commit hook scans for common patterns (see scanning below).
2. CI secrets stored in GitHub Actions Secrets (encrypted at rest, masked in logs).
3. Production secrets stored as OS env vars on the host (set during deploy, never logged).
4. Local dev uses `.env` files; every repo includes `.env.example` (committed, blank values) and `.env` in `.gitignore`.
5. Production secrets rotate every 90 days minimum. Rotation logged in `code-repo/infra/secret-rotation-log.md` (this is a register, not a decision record — keep it out of `decisions/`).
6. No secrets in Claude prompts. Pre-prompt mental check: "is there anything in this paste I would not write on a public whiteboard?" If yes, redact first.
7. Shared team secrets (e.g., shared dev DB password) communicated in person or via M365 encrypted email — never in Slack/Teams unencrypted channels.

**Scanning:**

- **Pre-commit:** Lightweight grep-based hook scanning staged files for common patterns (`AKIA...`, `sk_live_...`, `password\s*=\s*['"]`, etc.). Shipped in `.githooks/pre-commit`. Install via `git config core.hooksPath .githooks` on clone.
- **GitHub native:** GitHub's built-in secret scanning enabled at repo level (free for any repo). Alerts pushed to Teams via GitHub → Teams connector.
- **CI:** GitHub Actions job runs the same grep patterns across the full diff on every PR. Fails the PR if a match.
- **Periodic:** Monthly manual check of production env-var listings vs the secret rotation log — any drift investigated.

### 10.5 Audit log

Every action on confidential or restricted data is logged:

```json
{
  "timestamp": "2026-05-26T14:30:00Z",
  "actor": "dev-3@censof.com",
  "action": "read",
  "resource_type": "requirement",
  "resource_id": "REQ-042",
  "ai_assisted": true,
  "ai_model": "claude-opus-4-7",
  "client_ip": "10.0.1.42",
  "session_id": "abc-123"
}
```

Stored in append-only storage. Retained for at least 1 year, longer per client contract. Reviewed quarterly for anomalies (mass downloads, off-hours bulk access).

### 10.6 IP and licensing

**In every client contract:**

> "AI-assisted software development: The Contractor uses AI tools (including but not limited to Claude by Anthropic) to assist in code and documentation generation. All intellectual property rights in deliverables, including AI-assisted portions, are assigned to the Client upon final payment. The Contractor warrants that AI-generated content has been reviewed by qualified personnel and does not knowingly contain licensed third-party code in violation of the relevant licenses."

**License review (no dedicated scanner):**

- Every new dependency added in a PR triggers a manual license check by the reviewer — paste dep name + license into the PR description.
- Maintain `licenses.md` in the repo listing every dep + its license + when added. Updated on each dep addition.
- GitHub's dependency graph (free, native) lists detected licenses — reviewer references it for sanity check.
- Forbidden licenses for commercial client work: GPL-3.0, AGPL-3.0 (unless explicitly allowed by client).
- Allowed: MIT, BSD-2/3, Apache-2.0, ISC, MPL-2.0.
- Claude can be asked to audit `licenses.md` quarterly: read the file, flag anything suspicious, BA verifies.

**AI-attribution log:**

Every code file has a comment header if substantially AI-generated:

```
// File generated with AI assistance (claude-opus-4-7, 2026-05-15)
// Reviewed by: dev-3
// Prompt: prompts/generate-totp-handler.md@v1.2
```

### 10.7 Security checklist (every project start)

- [ ] Data classification documented in `security.md`
- [ ] Client NDA covers AI processing
- [ ] PDPA consent flow implemented if PII handled
- [ ] Secrets in GitHub Secrets / OS env vars, not in repo
- [ ] GitHub native secret scanning enabled at repo level
- [ ] Pre-commit secret-pattern hook installed
- [ ] `licenses.md` initialized with current deps
- [ ] Audit log configured
- [ ] DPO contact in `security.md`
- [ ] IP clause in contract
- [ ] Security review item added to design DoD
- [ ] Penetration test scheduled before go-live (if applicable)
- [ ] Incident response plan in `code-repo/infra/runbooks/security-incident.md`
- [ ] `code-repo/infra/redact-logs.sh` installed and team trained to use before any AI paste of log data

### 10.8 Security review gate

Before any release containing auth, payment, or PII changes:

1. Tech lead requests security review.
2. Senior engineer (or external if required by client) reviews:
   - Threat model
   - Code change
   - Test coverage of security cases
   - Audit log coverage
3. Sign-off as ADR in `design/adrs/`.
4. Release proceeds.

---

## 11. Deploy & Ops

### 11.1 Environment parity

Four environments, all containerized, all configured from the same base:

| Env     | Purpose            | Data                 | Who deploys                | Confidence required             |
| ------- | ------------------ | -------------------- | -------------------------- | ------------------------------- |
| Local   | Dev workstations   | Synthetic seed       | Developer                  | None (broken OK)                |
| Dev     | Shared integration | Synthetic seed       | CI on merge to `dev`     | Low (tests pass)                |
| Staging | UAT, client demo   | Anonymized prod copy | CI on merge to `staging` | High (UAT pass)                 |
| Prod    | Live customer use  | Real                 | Manual approve, CI deploys | Very high (staging green ≥24h) |

**Parity enforcement:**

- Single `docker-compose.yml` base + per-env overrides (`docker-compose.dev.yml`, `docker-compose.staging.yml`, etc.).
- All versions pinned: language runtime, OS image, all dependencies. No `latest` tags.
- Database engine version identical across envs.
- Config differs only by values (env vars), not by structure.

### 11.2 CI/CD pipeline

Standard pipeline shape (adapt per stack):

```yaml
# .github/workflows/ci-cd.yml — sketch

on:
  pull_request:
    branches: [dev, staging, main]
  push:
    branches: [dev, staging, main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - lint
      - format-check
      - unit-tests (with coverage gate)
      - integration-tests (containerized)
      - frontmatter-validation
      - req-id-commit-check
      - secret-scan
      - license-scan
      - cross-link-validation

  build:
    needs: lint-and-test
    if: github.event_name == 'push'
    steps:
      - build docker image
      - tag with commit SHA + branch name
      - push to registry

  deploy-dev:
    needs: build
    if: github.ref == 'refs/heads/dev'
    steps:
      - ssh to dev VPS: docker compose pull && docker compose up -d
      - run smoke tests against dev URL
      - notify Teams (webhook)

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/staging'
    steps:
      - ssh to staging VPS: docker compose pull && docker compose up -d
      - run integration tests
      - notify QA team in Teams

  deploy-prod:
    needs: build
    if: github.ref == 'refs/heads/main' && contains(github.event.head_commit.message, '[release]')
    environment: production    # requires manual approval in GitHub
    steps:
      - ssh to prod VPS: docker compose pull && docker compose up -d
      - run smoke tests against prod URL
      - notify on-call + client (Teams webhook + email)
      - tag release in Git
```

### 11.3 Release process

**Cadence:** weekly release window (Tuesdays 10am), unless hotfix.

**Steps:**

1. **Friday before:** Tech lead opens release PR `staging → main` with auto-generated release notes.
2. **Monday:** Final UAT verification on staging.
3. **Tuesday 9am:** Client notified ("deployment in 1 hour").
4. **Tuesday 10am:** Merge to `main`, CI deploys, smoke tests run.
5. **Tuesday 10:30am:** Confirm green, post-deploy verification.
6. **Tuesday 11am:** Notify client of completion, send release notes.

**Release notes template:**

```markdown
# Release v1.3.0 — 2026-05-26

## New features
- REQ-042: User login with 2FA via TOTP
- REQ-043: Password reset flow improvements

## Bug fixes
- FB-042: Safari login button event handler fix
- FB-051: Forgot-password email delivery time reduced

## Internal changes
- Test infrastructure: added Safari to CI matrix

## Database migrations
- Added `user_2fa_settings` table (additive, non-breaking)
- Added `audit_log` index on `(timestamp, actor)`

## Configuration changes
- New env var: `TOTP_WINDOW_SECONDS` (default 30, set to 60 in prod per CR-001)

## Rollback plan
1. SSH to prod VPS: `cd /opt/project-x && ./deploy.sh rollback v1.2.4`
   (script pulls previous image tag, restarts via `docker compose up -d`)
2. Roll back migration: `alembic downgrade -1`
3. Verify: smoke test login flow + check `/metrics` endpoint
Estimated rollback time: ~3 minutes.
Data loss risk: none (new column is nullable, no data deleted on downgrade).

## Breaking changes
None.

## Affected REQs
REQ-042, REQ-043

## Generated
Source MD commit: abc123def
Reviewed by: arvindh
```

### 11.4 Rollback plan (mandatory per release)

Every release MD must contain a rollback plan with:

- Exact commands to revert
- Estimated rollback time
- Data loss risk (high/medium/low/none)
- What gets rolled back, what doesn't (e.g., DB schema)
- Who has authority to trigger rollback (on-call lead)

No release without rollback plan. CI checks for the section.

### 11.5 Feature flags

For risky features, ship dark:

```python
if feature_flags.is_enabled("totp-login", user_id=user.id):
    return totp_login_flow(user)
else:
    return password_only_flow(user)
```

**Rules:**

- Every flag has a retire date in its name or in `feature-flags.md`.
- Flags older than 90 days reviewed in sprint planning for removal.
- Flag state changes logged in `feature-flags.md` with date and rationale.
- A/B test outcomes captured in `feature-flags.md` results section.

**Implementation (no dedicated tool):**

Simple env-var-driven flags. Example pattern (Python):

```python
import os

FLAGS = {
    "totp-login": os.getenv("FLAG_TOTP_LOGIN", "off") == "on",
    "new-dashboard": os.getenv("FLAG_NEW_DASHBOARD", "off") == "on",
}

def is_enabled(name: str, user_id: str = None) -> bool:
    # Optional: hash user_id for % rollout
    if not FLAGS.get(name, False):
        return False
    if name == "new-dashboard" and user_id:
        return int(hash(user_id)) % 100 < int(os.getenv("FLAG_NEW_DASHBOARD_PCT", "0"))
    return True
```

Flag toggles = config change + restart (or `kill -HUP` if process reloads env). For larger projects, swap env vars for a JSON config file in the deployment that the app polls every 60s.

### 11.6 Observability (lightweight, file-based)

The standard stack does not include Prometheus/Grafana/Loki. Observability is achieved with the basics: structured logs, simple metrics endpoints, and Claude-assisted diagnosis.

| Layer            | Approach                                                                                                                                                                      |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Logs             | Application writes structured JSON logs to file (`/var/log/app/`). Log rotation via `logrotate` (built into Linux).                                                       |
| Metrics          | App exposes `/metrics` HTTP endpoint with key counters (requests, errors, latency buckets). A cron job (every 1 min) curls the endpoint and appends to a daily JSON file.   |
| Traces           | Not used. Instead, every request gets a `request_id` UUID logged at entry, exit, and at every external call. Grep across services on `request_id` reconstructs the trace. |
| Alerting         | Simple Bash scripts in `infra/alerts/` run via cron, check log files / metrics endpoint thresholds. On breach: send Teams webhook message + email via M365 SMTP.            |
| Uptime           | A separate cron-driven curl from a different VPS (or Censof office machine) hits production health endpoint every 1 min, alerts on failure via Teams webhook.                 |
| Synthetic checks | Bash scripts simulate critical user journeys (login, key API calls) every 5 min, alert on assertion failure.                                                                  |

**Why this works for Censof-scale projects:**

- One VPS, one or two services per project — full observability stack overkill.
- Claude can read raw log files and diagnose. Workflow: incident → BA/dev pulls last 1hr of logs → **runs `infra/redact-logs.sh` first to strip secrets/PII** → pastes redacted excerpt into Claude → fix.
- All "dashboard" needs are met by Claude generating a daily ops summary into an MD file in `dashboard/ops-daily.md`.

**Mandatory log redaction before AI paste:**

Production logs may contain session tokens, API keys, email addresses, request bodies with PII, and IP addresses. Pasting raw logs into Claude violates the "Restricted data never to AI" rule (10.2). Use `infra/redact-logs.sh` before any paste:

```bash
#!/usr/bin/env bash
# infra/redact-logs.sh — strip secrets/PII before AI paste
# Usage: tail -n 1000 /var/log/app/auth.log | ./redact-logs.sh > /tmp/redacted.log
sed -E \
  -e 's/Bearer [A-Za-z0-9._-]+/Bearer <REDACTED>/g' \
  -e 's/(api[_-]?key|token|secret|password)["'"'"']?[: =]+["'"'"']?[A-Za-z0-9._-]+/\1=<REDACTED>/Ig' \
  -e 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/<EMAIL>/g' \
  -e 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/<IP>/g' \
  -e 's/sk_(live|test)_[A-Za-z0-9]+/sk_<REDACTED>/g' \
  -e 's/AKIA[0-9A-Z]{16}/AKIA<REDACTED>/g'
```

Patterns extend per project as new secret formats are noticed. Treat the script as living code in `infra/redact-logs.sh`.

If a redacted log still contains client-business-sensitive content (e.g., customer names in business reports), use the `Confidential` data tier rules — Claude OK only under NDA + audit log entry. When unsure, ask BA before paste.

**Minimum metrics every service exposes (`GET /metrics`):**

```
requests_total{endpoint="/login", status="200"} 12453
requests_total{endpoint="/login", status="401"} 87
requests_total{endpoint="/login", status="500"} 3
request_duration_ms_p50{endpoint="/login"} 45
request_duration_ms_p95{endpoint="/login"} 180
request_duration_ms_p99{endpoint="/login"} 420
active_connections 42
last_db_query_ms 12
uptime_seconds 86523
```

Plain text, easy to parse with any scripting.

**Alert thresholds (in `infra/alerts/thresholds.yml`):**

```yaml
- name: high-error-rate
  metric: requests_total{status="5xx"} / requests_total
  threshold: 0.05
  window: 5m
  severity: SEV-2
  notify: teams-webhook + email-oncall

- name: login-latency-spike
  metric: request_duration_ms_p95{endpoint="/login"}
  threshold: 1000
  window: 5m
  severity: SEV-3
  notify: teams-webhook

- name: uptime-fail
  metric: external curl /health
  threshold: 2 consecutive failures
  severity: SEV-1
  notify: teams-webhook + sms via M365 + phone-on-call
```

Bash script reads the YAML, evaluates against current metrics, fires notifications. ~100 lines of code total. Stored in `infra/alerts/check.sh`.

**Alert philosophy:**

- Alert on symptoms (high error rate, uptime fail), not causes (CPU 80%).
- Every alert is actionable. Non-actionable alerts get tuned out.
- Every alert links to a runbook MD section.
- Alert fatigue tracked: count alerts/week, review monthly.

### 11.7 Database changes

Migrations are dangerous. Special rules:

- Migrations are reviewed by two engineers minimum.
- Every migration has a tested rollback.
- Migrations are tested against a copy of production data (anonymized).
- Big migrations (>1M rows) are run in batches with monitoring.
- Schema changes are additive before destructive: add new column, backfill, switch code, deprecate old column — separate releases.
- Down-time-causing migrations require client notification and scheduled window.

### 11.8 Deploy frequency target

Small, often. Goals:

- Dev: multiple deploys per day (every merge).
- Staging: 1–3 deploys per week.
- Prod: weekly, plus hotfixes as needed.

Frequency is a quality signal: if you can't deploy weekly, the process needs work.

---

## 12. Incident Response

### 12.1 Severity levels

| Sev   | Definition                                                                        | Examples                                           | Response time                        | Comms                                                                           |
| ----- | --------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| SEV-1 | Total or major outage; data loss or breach; many users affected; revenue impacted | Login broken for all, prod DB corrupted, data leak | <5min ack, immediate war room        | Teams broadcast to client channel + client PM call within 15min, hourly updates |
| SEV-2 | Major feature broken; many users affected; degraded but not down                  | Search broken, payment intermittent                | <30min ack, work to resolve same day | Teams broadcast to client channel + email; updates every 2hr                    |
| SEV-3 | Minor feature broken; workaround exists; few users                                | One report type broken                             | <4hr ack, fix in current sprint      | GitHub issue; client notified if asks                                           |
| SEV-4 | Cosmetic, edge case                                                               | Typo, alignment                                    | Next available sprint                | Tracked in backlog                                                              |

### 12.2 Incident flow

```
Detection (alert / user report)
    ↓
On-call acknowledges (<5min for SEV-1/2)
    ↓
Triage severity
    ↓
If SEV-1/2:
  - Open war room (Teams meeting + dedicated Teams channel for incident)
  - Assign Incident Commander (IC)
  - Assign Comms Lead
  - IC drives diagnosis, Comms updates stakeholders
    ↓
Diagnose: hypotheses, evidence, ruling out
    ↓
Mitigate: rollback / feature flag off / scale / restart / patch
    ↓
Verify: alerts cleared, smoke tests pass, monitor for 30min
    ↓
All-clear announced
    ↓
Within 5 business days: postmortem written and reviewed
    ↓
Action items tracked as TASKs with deadlines
```

### 12.3 Postmortem template

`incidents/INC-001.md`:

```yaml
---
id: INC-001
date: 2026-05-26
severity: SEV-1
status: closed                  # open | mitigated | resolved | postmortem-pending | closed
duration_min: 47
detected_by: alert | user-report
incident_commander: arvindh
comms_lead: ba-rina
affected_users: ~3000
affected_features: [login]
revenue_impact_rm: ~0   # Estimated
data_loss: false
data_breach: false
---

## Summary
Login endpoint returned 500 errors for all users for 47 minutes starting 14:02 due to a failed database migration that left schema out of sync with application code.

## Timeline
- 14:02 - Alert script fired: error rate spike on auth-service (15% → 95%) — Teams webhook + email
- 14:05 - On-call (dev-3) acknowledged in Teams, joined war room
- 14:07 - War room opened in Teams; IC (arvindh) and Comms (ba-rina) assigned
- 14:12 - Hypothesis: deploy at 13:55 broke something — confirmed by checking recent deploys
- 14:15 - Diagnosed: migration added `user_2fa.enabled_at` column but code still references old schema; migration succeeded but app deploy step failed silently
- 14:18 - Decision: rollback to v1.2.4. Migration to be rolled forward later (column is nullable, harmless)
- 14:25 - Rollback initiated via `deploy.sh rollback v1.2.4` on VPS
- 14:30 - Service restarting
- 14:35 - Service restored; error rate dropping
- 14:42 - Error rate at baseline (<0.1%); smoke tests pass
- 14:49 - All-clear announced internally + Teams broadcast to client channel updated to "Resolved"
- 15:30 - Client status update sent

## Root cause
A race condition in the deploy script: the DB migration ran successfully, but the application restart step failed silently (process did not pick up the new binary). The old binary kept running against the new schema. The new column was nullable, but the migration also adjusted an index that the old binary's query plan did not expect, causing 500 errors.

Contributing factors:
- Migration was not backward-compatible at the index level (we only checked column-level compatibility).
- Deploy script did not verify "running binary version == expected version" after restart.
- No automated post-deploy health check.

## What went well
- Alert fired within 3 minutes of impact.
- On-call acknowledged within target.
- Rollback playbook worked first try.
- Comms cadence was clear; client didn't surprise us with a call.

## What went badly
- Migration was not backward-compatible at the index level (violated our own guideline).
- Deploy script's restart step failed silently — silent failures are dangerous.
- No post-deploy health check meant the broken deploy went unnoticed for 7 minutes.
- Comms lead took 8 minutes to send first external update; template wasn't ready.

## Action items
- AI-001: Add binary-version verification step to deploy.sh (owner: dev-1, due: 2026-06-02, TASK-310)
- AI-002: Enforce backward-compatible migrations via PR checklist + reviewer awareness (owner: dev-2, due: 2026-06-09, TASK-311)
- AI-003: Pre-write incident comms templates per severity, store in `code-repo/infra/runbooks/comms-templates.md` (owner: ba-rina, due: 2026-05-29, TASK-312)
- AI-004: Add post-deploy health check loop (curl /health for 60s, fail deploy if not green) (owner: dev-1, due: 2026-06-16, TASK-313)
- AI-005: Update REQ-042 (login) to include "deploy must verify binary version" as NFR (owner: ba-rina, due: 2026-05-29)

## Related artifacts
- PR introducing the migration: #234
- Rollback PR: #245
- Comms log: incidents/INC-001-comms-log.md (co-located with the postmortem; no separate `communications/` folder)
- Log excerpts at time of incident: incidents/INC-001-logs.txt

## Blameless retro
Held 2026-05-28. Focus on system improvements, not individuals. Outcome: this postmortem.
```

### 12.4 Blameless culture

Postmortems focus on systems and processes, never on individuals. Phrasing:

- ✅ "The deploy pipeline did not verify image presence."
- ❌ "Dev-3 pushed a bad migration."

Goal: people feel safe reporting incidents and being honest about contributing factors. Blame culture buries information.

### 12.5 Runbooks

Runbooks live in the **code repo** at `infra/runbooks/` (not the requirements-repo) because they reference code paths, deploy scripts, and infrastructure details. One MD per recurring incident type or service:

```
code-repo/infra/runbooks/
├── _index.md                 # Runbook catalog by service/issue
├── _prompts.md               # OPs: lookup-runbook, update-runbook-from-incident
├── auth-service.md           # Common issues + fix steps
├── billing-service.md
├── database-issues.md
├── deploy-failures.md
├── comms-templates.md        # Per-severity comms drafts
└── security-incident.md      # Data breach response
```

Each runbook structure:

```markdown
# Runbook: Auth Service

## Common issues

### Issue: Login error rate > 5%
**Detection:** Alert script `high-error-rate` posts to Teams + emails on-call.

**Diagnosis:**
1. Check recent deploys: `cat /var/log/deploy/history.log | tail -5`
2. Check service logs for last 5 min: `tail -n 1000 /var/log/app/auth.log | grep ERROR`
3. **Redact before AI:** `tail -n 1000 /var/log/app/auth.log | /opt/<project>/infra/redact-logs.sh > /tmp/redacted.log`
4. Ask Claude to summarize the redacted excerpt: paste `/tmp/redacted.log` → "what's the dominant error pattern here?"
5. Check DB: `psql -c "SELECT count(*) FROM pg_stat_activity WHERE state='active';"` (look for connection exhaustion)
6. Check upstream identity provider (if used): `curl -I https://idp.example.com/health`

**Mitigation:**
- If recent deploy correlates: `cd /opt/auth && ./deploy.sh rollback <previous-version>`
- If DB pool exhausted: increase pool size in `.env` + restart, then investigate slow queries
- If IDP down: enable cached-token mode by setting `FLAG_AUTH_CACHE_ONLY=on` and restart

**Escalation:** If above doesn't resolve in 15 minutes, page tech lead.
```

Runbooks are updated after every incident. A postmortem that doesn't update a runbook is incomplete.

### 12.6 Comms templates (pre-written)

`code-repo/infra/runbooks/comms-templates.md`:

```markdown
## SEV-1 Initial (fill blanks within 15min of incident start)

Subject: [PROJECT-X] Service Disruption — Investigating

We are currently investigating reports of [BRIEF DESCRIPTION OF SYMPTOM] affecting [SCOPE OF USERS].

Our team is engaged and working to identify the cause. We will provide an update within [TIME] or as soon as we have more information.

We apologize for the inconvenience.

— Censof Operations

## SEV-1 Update (every hour or material change)

Subject: [PROJECT-X] Service Disruption — Update at [TIME]

Update on the issue affecting [SCOPE]:
- Current status: [Investigating / Mitigating / Verifying]
- What we know: [SUMMARY]
- Workaround for users: [IF ANY]
- Next update: [TIME]

— Censof Operations

## SEV-1 Resolved

Subject: [PROJECT-X] Service Disruption — Resolved at [TIME]

The issue affecting [SCOPE] has been resolved as of [TIME]. Total impact duration: [X] minutes.

Cause (preliminary): [BRIEF]

A full postmortem will be shared within 5 business days, including action items to prevent recurrence.

We apologize for the disruption.

— Censof Operations
```

### 12.7 On-call rotation

Documented in `teams.md`:

- Primary on-call: rotates weekly (Mon 9am handoff).
- Secondary on-call: rotates weekly, offset.
- Handoff doc: open issues, watch items, expected releases — emailed Friday EOD.
- Compensation: TOIL (time off in lieu) or on-call allowance per Censof HR policy.
- After-hours expectation: SEV-1/2 only. SEV-3/4 wait for business hours.

### 12.8 Hotfix flow

When a SEV-1/2 needs a code fix:

1. Branch `hotfix/INC-001-login-fix` from `main`.
2. Apply minimum viable fix + targeted test.
3. PR review: 1 reviewer (vs normal 2) due to urgency, but high-bar reviewer.
4. CI must still pass (lint, secret scan, tests).
5. Deploy to staging, smoke test (target: <30 min).
6. Deploy to prod, monitor closely.
7. Backport to `dev` branch.
8. Open follow-up TASK for proper fix if hotfix was a workaround.
9. Update REQ MD if the incident exposed a missing requirement.

---

## 13. AI Risk Management

### 13.1 The AI risk landscape

AI tools (Claude included) introduce specific risks:

| Risk                     | Manifestation                                      | Mitigation                                                          |
| ------------------------ | -------------------------------------------------- | ------------------------------------------------------------------- |
| Hallucination            | Invented APIs, fake references, wrong facts        | Grounded prompts + two-pass review + Graphify context               |
| Stale knowledge          | AI trained on old data, suggests outdated patterns | Pin model version; document cutoff; verify against current code     |
| Prompt drift             | Same prompt produces different outputs over time   | Version prompts; track outputs; regenerate when prompt changes      |
| Model drift              | Underlying model updates change behaviour          | Pin model version explicitly per project                            |
| Over-reliance            | Devs lose ability to work without AI               | Periodic AI-free exercises; mentorship of juniors                   |
| Under-reliance           | Devs ignore AI suggestions, lose productivity      | Track AI accept rate; calibrate trust                               |
| Confidential data leak   | Sensitive data pasted into AI                      | Data classification + AI usage tiers + audit log                    |
| Licensed code generation | AI suggests code matching restrictive OSS license  | Manual license review on dep additions (per 10.6) + attribution log |
| Inconsistent quality     | Output varies across sessions                      | Standardized prompts + DoD-based review                             |
| Cost explosion           | Token spend balloons in long sessions              | Caveman mode + per-project budget alerts                            |

### 13.2 Prompt versioning

Prompts are code. They live in `prompts/`, are version-controlled, and have changelogs.

`prompts/fill-srs-section.md` example:

```yaml
---
id: fill-srs-section
version: 1.3
last_updated: 2026-05-15
owner: arvindh
when_to_use: Filling a section of a KRISA SRS Word template from MD sources
inputs: section number, source MD files, language (default BM)
expected_output: Filled Word section with REQ-ID citations and source comments
changelog:
  - v1.0 2026-04-01 — initial version
  - v1.1 2026-04-15 — added BM glossary reference
  - v1.2 2026-05-01 — added "do not invent" rule after hallucination incident
  - v1.3 2026-05-15 — added hidden comment with source list per section
---

[prompt body]
```

When a prompt changes, the changelog notes which artifacts produced by the old prompt may need re-generation. A reasonable policy: don't backfill, but note in the artifact's metadata which prompt version generated it.

### 13.3 Model version pinning

Every project's `ai-config.md`:

```yaml
default_model: claude-opus-4-7
code_review_model: claude-sonnet-4-6   # Cheaper for high-volume reviews
code_gen_model: claude-opus-4-7        # Highest quality for code
quick_qa_model: claude-haiku-4-5       # Fast for trivial questions
locked_until: project-end | 2026-12-31
context_window_target: 1M              # Opus 4.7 1M context for large MD synthesis
fallback_model: claude-opus-4-6        # If primary unavailable
review_cadence_for_upgrade: quarterly
notes: |
  Opus 4.7 chosen for 1M context window required for whole-spec synthesis.
  Sonnet 4.6 chosen for code reviews to manage cost; senior dev reviews Sonnet's output.
```

When a new model is released, evaluate against current pinning quarterly. Document upgrade decision as ADR.

### 13.4 AI usage tiers

Define per project — what level of AI involvement is acceptable for which activities:

| Tier   | Activity examples                                                                                                                   | Approval flow                               |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Green  | Code completion, refactor suggestions within a file, test generation for existing functions, doc draft from MD, status report draft | Developer self-reviews and accepts          |
| Yellow | Multi-file refactor, new module scaffolding, design proposal, schema change suggestion                                              | Peer review required                        |
| Red    | Production deploy command, secret access, data migration script, customer-facing communication, security-critical code              | Tech lead + human approval; logged in audit |

Documented in `00-overview/ai-config.md`. Devs reference when unsure.

### 13.5 Hallucination controls

**At prompt level:**

- Provide explicit sources. "Here are the only files you may reference."
- Forbid invention. "If information is not in the source, say [TBD], do not invent."
- Require citation. "Cite source for every factual claim."

**At review level:**

- Two-pass AI review (Claude A generates, Claude B critiques).
- Human spot-checks at least 20% of AI output, more for high-risk artifacts.
- Code review against Graphify-derived context (does this function actually exist?).

**At process level:**

- Track hallucination incidents. If Claude invented something that was missed, log it as a quality incident.
- Adjust prompts after each incident.
- Add the failed case to a regression set for future prompt testing.

### 13.6 Calibration metrics

Track and report monthly:

| Metric                                                         | Target                                         |
| -------------------------------------------------------------- | ---------------------------------------------- |
| AI suggestion accept rate (accepted as-is / total suggestions) | Trend up over project (calibration improves)   |
| AI suggestion reject rate                                      | Should not exceed 30% (else prompts need work) |
| Time saved per AI-assisted task (self-report)                  | Track for ROI                                  |
| Cost per AI-assisted task (token spend)                        | Trend down over project                        |
| Hallucination incidents per month                              | Target zero; investigate every one             |
| AI-related rework hours                                        | Track for ROI accuracy                         |

### 13.7 Cost management

| Lever                                                 | Effect                                    |
| ----------------------------------------------------- | ----------------------------------------- |
| Caveman mode in conversation                          | ~75% token reduction                      |
| Per-REQ MD files (vs monolithic)                      | Smaller context per call                  |
| Cheaper model for non-critical (Sonnet, Haiku)        | 5–10× cost reduction                    |
| Prompt caching (Anthropic API)                        | Repeat-context cost cut                   |
| Budget alerts at 80% monthly cap                      | Triggers pause of non-critical generation |
| ROI tracking (hours saved × hourly rate vs API cost) | Justifies spend to client/leadership      |

Document monthly Claude spend in dashboard. Anomalies (sudden spike) investigated.

### 13.8 AI accountability

When AI-generated code or doc causes a problem:

- The accountable party is the human reviewer who approved it, not "the AI".
- The lesson goes into the prompt, the DoD, or both.
- The hallucination or failure mode is added to the team's awareness training.

This keeps AI as a tool, not a scapegoat.

---

## 14. Communication Cadence

### 14.1 Internal cadence

| Forum                  | Frequency | Duration                      | Format                                  | Audience                 |
| ---------------------- | --------- | ----------------------------- | --------------------------------------- | ------------------------ |
| Daily standup          | Daily     | 15min async, sync if blockers | Teams written update in project channel | Dev team                 |
| Sprint planning        | Bi-weekly | 1–2hr                        | Sync meeting                            | Team + BA + PO           |
| Sprint review/demo     | Bi-weekly | 1hr                           | Sync, recorded                          | Team + client            |
| Sprint retro           | Bi-weekly | 1hr                           | Sync                                    | Team only (no client)    |
| Tech leads sync        | Weekly    | 30min                         | Sync                                    | Tech leads only          |
| All-hands project sync | Monthly   | 30min                         | Sync                                    | All project stakeholders |

### 14.2 Client cadence

| Forum                     | Frequency  | Format                   | Owner                  |
| ------------------------- | ---------- | ------------------------ | ---------------------- |
| Weekly status report      | Friday EOD | PDF/email auto-generated | BA reviews, sends      |
| Sprint demo               | Bi-weekly  | Live, recorded           | Tech lead presents     |
| Steering committee        | Monthly    | Slide deck               | PM presents            |
| Quarterly business review | Quarterly  | Exec deck                | Account lead           |
| Ad-hoc                    | As needed  | Email + Teams            | Whoever owns the topic |

### 14.3 Daily standup format (async)

Each dev posts in the team's Teams channel by 10am:

```
🟢 Yesterday: TASK-205 (Safari bug) — PR opened, awaiting review
🟢 Today: TASK-206 (TOTP recovery flow) — implementing
🟡 Blockers: Waiting on client SSO config for REQ-045 — flagged to BA
```

Tech lead scans, surfaces blockers in a 5-min sync if needed. No daily sync meeting unless multiple blockers.

### 14.4 Weekly status report (auto-generated)

Friday 4pm, Claude generates a draft from the dashboard:

```markdown
# Project X — Week of 2026-05-26

## Progress this week
- Completed: REQ-042 (2FA login), REQ-043 (password reset improvements)
- In progress: REQ-044 (password reset email template — 60%)
- Blocked: REQ-045 (waiting on client SSO IDP config)

## Sprint health (sprint-03, days 9 of 10)
- Velocity: 28 of 32 estimated days complete (87%)
- Bugs found this sprint: 12 (10 closed, 2 carried over)
- Late changes: 1 (CR-001 approved, +2 days)
- New reqs raised: 1 (REQ-091 — SMS-based 2FA, scheduled for sprint-05)

## Risks
- SSO config delay may push REQ-045 to sprint-04 (currently flagged yellow)
- Team Auth is at 95% capacity for sprint-04 — limited room for new work

## Decisions needed from client this week
- Confirm SSO IDP credentials by Wed 2026-05-29 (REQ-045)
- Sign off on UAT plan for sprint-03 demo (D13)
- Confirm whether to include SMS 2FA in scope (REQ-091)

## Next week
- Complete REQ-044
- Begin REQ-046 (admin user management) design
- UAT prep for sprint-04 demo

## Metrics
- Health score: 82 (up from 78)
- Bug escape rate (rolling 4 sprints): 11% (down from 14%)
- Scope change ratio: 1.08 (8% over baseline)
- Test coverage by REQ: 94%

## Generated
Source MD commit: abc123def
Date: 2026-05-29 16:00
Reviewer: ba-rina
```

BA reviews, edits if needed, sends to client.

### 14.5 Sprint demo structure

Bi-weekly, recorded, 1 hour:

1. **Intro (2 min):** What we're demoing, agenda.
2. **Sprint goals recap (3 min):** What we said we'd do.
3. **Live demo (30 min):** Each REQ delivered, walk-through with realistic data.
4. **Acceptance walk-through (10 min):** For each demoed REQ, walk through the acceptance criteria — show they're met.
5. **What's next (5 min):** Next sprint goals.
6. **Q&A and feedback (10 min):** Client reacts; BA captures into INBOX.md live.

Recording stored in `deliverables/demos/sprint-NN.mp4`.

### 14.6 Steering committee

Monthly, 1 hour, 5–10 slides:

1. **Project status:** Green/Yellow/Red with rationale.
2. **Progress vs plan:** Milestones hit, milestones at risk.
3. **Scope:** Original vs current. Changes approved and pending.
4. **Budget:** Burn vs plan.
5. **Risks:** Top 3, with mitigation status.
6. **Decisions needed:** From client/exec sponsors.
7. **Looking ahead:** Next month focus.

Generated from dashboard + manual narrative by PM. Sent in advance for pre-read.

### 14.7 Decision logging

Every non-trivial decision goes into `decisions/DEC-NNN.md`:

```yaml
---
id: DEC-001
date: 2026-05-15
type: tooling                  # tooling | process | scope | architecture | personnel
participants: [arvindh, client-pm, tech-lead-client]
status: decided                # pending | decided | superseded
supersedes: null
---

## Context
Client requested a separate sprint board with drag-and-drop, beyond what an Obsidian dashboard renders. We considered adding a paid tool vs sticking with Obsidian Kanban plugin.

## Options considered
1. Adopt a paid issue tracker (Jira / Linear) for the client to view sprints.
2. Use Obsidian Kanban plugin + share the rendered HTML via OneDrive — stays inside the standard stack.
3. Use GitHub Issues / Projects (free) with a curated view for the client.

## Decision
Obsidian Kanban plugin, with weekly HTML export to OneDrive for client visibility.

## Rationale
- Keeps within Censof's standard stack — no new license, no new training surface.
- Kanban plugin reads/writes the same task MD files as Dataview — zero extra source of truth.
- Client gets a static HTML view weekly; deeper drill-down available in the auto-generated PDF status report.

## Consequences
- BA owns weekly HTML export (one click in Obsidian) and OneDrive sync.
- If client demands real-time interactive board later, revisit (likely move to GitHub Projects since it's already in the stack at zero added cost).

## Reviewed by
Client signed off via email 2026-05-15 (archived in signoffs/).
```

ADRs (Architecture Decision Records) live separately in `design/adrs/` and follow the same structure but specifically for architecture choices.

### 14.8 Communication hygiene rules

- One channel per topic in Teams. Don't fragment a discussion across email + multiple Teams channels.
- Decisions go into MD, not chat. Chat is ephemeral; MD is durable.
- Client-facing comms go through BA. Five devs DMing the client = inconsistency and missed signals.
- Mute non-critical channels during focus hours.
- No status meetings if the dashboard answers the question.

---

## 15. Putting It All Together — The Project Lifecycle

This section walks through a project from kickoff to handover, showing how the pieces interact.

### 15.1 Phase 0 — Pre-kickoff (1–2 weeks)

**Inputs:** Signed contract, scope document, client stakeholder list.

**Activities:**

1. PM creates `requirements-repo` from Censof Obsidian-vault template (frontmatter templates, Dataview queries, Kanban boards, folder layout, **and `_index.md` + `_prompts.md` files pre-configured per tier policy** — both files in every Tier A folder, `_index.md` in every Tier B folder, none in Tier C).
2. PM clones the Obsidian vault into OneDrive sync folder; sets up GitHub remote.
3. Configure M365 connector to expose the OneDrive folder to Claude.
4. Install the standard Obsidian plugin set (Dataview, Kanban, Tasks, Calendar, Templater, Git, Charts, Excalidraw, Periodic Notes, Linter).
5. Verify `_index.md` + `_prompts.md` regeneration/validation script runs in CI; verify root `_index.md` is populated with project metadata; verify every **Tier A** folder's `_prompts.md` is populated with that folder's operations (Tier B folders' `_prompts.md` is optional and only present where ops exist).
6. Run security checklist (10.7).
7. Run AI risk setup: pin Claude model, document tiers, version baseline prompts.
8. Draft `00-overview/vision.md`, `scope.md`, `stakeholders.md`, `teams.md`.
9. Stand up Dev/Staging/Prod environments (containers on VPS, or per project infra).
10. Configure GitHub Actions CI skeleton (lint, test, `validate_frontmatter.py` for record MDs, `regen_indexes.py` for `_index.md`/`_prompts.md` validation + catalog regen, work-item-ID commit check, secret-pattern scan).
11. Set up lightweight observability: log paths, `/metrics` endpoint, cron alert scripts, Teams webhook URL configured.
12. Train BA on MD workflow + Obsidian + Git plugin (1 day) — emphasize `_index.md` + `_prompts.md` discipline (catalog accuracy, plus adding/refining OPs as the project's ways-of-working evolve).
13. Train client PM on MD viewing + change request process via OneDrive (1 hour).

**Outputs:** Empty but fully-wired project skeleton.

### 15.2 Phase 1 — Discovery (2–4 weeks)

**Activities:**

1. Workshops with client to gather raw requirements (workshops recorded, transcripts in `raw-inputs/`).
2. Claude ingests raw inputs (transcripts, emails, slides) and drafts requirement MDs.
3. BA reviews each draft, refines, sets status to `draft`.
4. Client review session: walk through REQs, gather feedback.
5. BA edits REQs, gets client signoff (status → `approved`).
6. Tech lead drafts initial `spec/`, `design/architecture.md` based on approved REQs.
7. First sprint plan drafted from prioritized REQs.

**Outputs:** Approved requirements, initial spec/design, sprint-01 plan.

### 15.3 Phase 2 — Build sprints (bi-weekly, repeat for N sprints)

**Each sprint:**

1. **Day 1 (Mon):** Sprint planning. Confirm REQs and tasks. Update dashboard.
2. **Days 2–9:** Development.
   - Devs work on tasks; commits cite at least one work-item ID (typically REQ-ID + TASK-ID for feature work; FB/INC/CR/DEC where applicable).
   - AI-assisted code, AI-assisted reviews.
   - Daily async standups in Teams.
   - PRs reviewed per CODEOWNERS.
   - CI gates enforce DoD.
3. **Day 8 (Tue week 2):** Internal QA on staging.
4. **Day 9 (Wed):** Bug fixes from QA.
5. **Day 10 (Thu):** Client demo + UAT begins.
6. **Day 11 (Fri):** Retro + sprint close. Feedback triaged. Status report sent.

### 15.4 Phase 3 — Continuous activities (alongside sprints)

- **KRISA documents:** BA fills D02/D03/D04 incrementally as REQs/Spec/Design stabilize. By end of build phase, 80% of KRISA Word docs are populated.
- **Test documents:** D11/D12/D13/D14/D16 populated as test plans and results accumulate.
- **DB and code docs (D09, D10):** Generated from latest code at end of build phase.
- **Operational docs (D17, D18):** Drafted in final sprint.
- **Dashboard:** Auto-updates throughout.
- **Feedback loop:** Runs continuously after first demo.

### 15.5 Phase 4 — UAT & stabilization (2–4 weeks)

**Activities:**

1. Formal UAT period with client.
2. UAT findings logged as feedback (FB-XXX), triaged daily.
3. Bug fixes prioritized over new features.
4. KRISA test reports (D11, D14, D16) finalized.
5. User manual (D17) finalized with screenshots and walkthroughs.
6. Penetration test (if applicable).
7. Performance and load testing.
8. Documentation review with client.

**Outputs:** UAT signoff, all KRISA docs ready for handover.

### 15.6 Phase 5 — Production launch (1–2 weeks)

**Activities:**

1. Final security review + signoff.
2. Production deployment plan (window, comms, rollback).
3. Production deploy with full monitoring.
4. Hyper-care period (intensified on-call) for 2 weeks post-launch.
5. KRISA Handover Report (D18) finalized.
6. Client training sessions (if in scope).
7. Final invoice / contract milestone trigger.

### 15.7 Phase 6 — Handover & retro (1 week)

**Activities:**

1. Full handover: all KRISA docs delivered (D01–D18).
2. Source MD repo handed over (read-only access for client) or archived.
3. Codebase access transferred or maintenance contract activated.
4. Project retro: extract lessons learnt.
5. **Update this playbook with what worked and what didn't.**
6. Archive project artifacts.

### 15.8 Phase 7 — Maintenance (optional, contractual)

If maintenance contract:

- Incident response active (SLA per contract).
- Bug fixes following hotfix flow.
- Minor enhancements following change request flow.
- Quarterly review with client.

---

## 16. Appendices

### Appendix A — Scripts and validators

#### A.1 Frontmatter validation script

```python
# scripts/validate_frontmatter.py
import sys
import yaml
import re
from pathlib import Path

# Required frontmatter fields per MD type, matched by folder path parts.
# Keys are tuples representing parent folder names (path.parts membership test).
REQUIRED_FIELDS = {
    "requirements":    ["id", "title", "status", "priority", "team", "created", "last_updated"],
    "tasks":           ["id", "title", "status", "team", "req_ref", "sprint", "estimate_hours", "last_updated"],
    "feedback":        ["id", "sprint_raised", "source", "type", "severity", "status", "related_req"],
    "spec":            ["id", "title", "status", "version", "last_updated", "covers_req"],
    "design":          ["id", "title", "status", "version", "last_updated"],
    "adrs":            ["id", "title", "status", "date", "deciders"],
    "decisions":       ["id", "date", "type", "participants", "status"],
    "incidents":       ["id", "date", "severity", "incident_commander", "data_loss", "data_breach", "status"],
    "change-requests": ["id", "type", "raised_by", "raised_date", "affects_req", "status"],
    "raw-inputs":      ["id", "source_type", "source_date", "captured_by", "status"],
}

# Conditional fields: required only when a status-dependent predicate holds.
CONDITIONAL_REQUIRED = {
    "tasks": [
        ("assignee", lambda fm: fm.get("status") != "todo"),
    ],
    "requirements": [
        ("approved",    lambda fm: fm.get("status") in
            ["approved", "in-dev", "ready-for-acceptance", "done"]),
        ("approved_by", lambda fm: fm.get("status") in
            ["approved", "in-dev", "ready-for-acceptance", "done"]),
        ("implemented", lambda fm: fm.get("status") == "done"),
    ],
    "raw-inputs": [
        ("generated_reqs", lambda fm: fm.get("status") in
            ["partially-processed", "fully-processed"]),
    ],
}

STATUS_VALUES = {
    "requirements":    ["draft", "approved", "in-dev", "ready-for-acceptance", "done",
                        "blocked", "late-change", "rejected", "deferred"],
    "tasks":           ["todo", "in-progress", "review", "done", "blocked"],
    "feedback":        ["triaged", "accepted", "in-progress", "done", "rejected", "deferred", "duplicate"],
    "spec":            ["draft", "approved", "deprecated"],
    "design":          ["draft", "approved", "deprecated"],
    "adrs":            ["proposed", "accepted", "deprecated", "superseded"],
    "decisions":       ["pending", "decided", "superseded"],
    "incidents":       ["open", "mitigated", "resolved", "postmortem-pending", "closed"],
    "change-requests": ["under-review", "approved", "rejected", "deferred"],
    "raw-inputs":      ["unprocessed", "partially-processed", "fully-processed", "superseded"],
}

# Non-record MD files inside tracked folders — exempt from record-schema validation.
# They are summary/freeform/template files, not data records.
SKIP_FILES = {
    "_index.md", "_prompts.md",
    "INBOX.md",       # feedback/ — freeform dump
    "backlog.md",     # tasks/ — list of not-yet-sprint-allocated TASKs
    "retro.md",       # feedback/sprint-NN/ — sprint retro (has its own minimal schema, see 8.5)
    "README.md",      # repo root
    "CHANGELOG.md",   # prompts/, repo root — append-only log
    "licenses.md",    # code-repo/ — dep license register
    "feature-flags.md", "secret-rotation-log.md",  # code-repo/infra/ — registers
}

def classify(file_path: Path) -> str | None:
    """Return the MD-type key based on Path.parts membership. Returns None if untracked."""
    for part in file_path.parts:
        if part in REQUIRED_FIELDS:
            return part
    return None

def validate(file_path: Path) -> list[str]:
    errors = []
    # Skip non-record MD files (index, prompts, summaries, registers)
    if file_path.name in SKIP_FILES:
        return []
    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return [f"{file_path}: missing frontmatter"]
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return [f"{file_path}: invalid YAML — {e}"]

    md_type = classify(file_path)
    if not md_type:
        return []  # Not a tracked file type

    for field in REQUIRED_FIELDS[md_type]:
        if field not in fm:
            errors.append(f"{file_path}: missing required field '{field}'")

    for field, required_when in CONDITIONAL_REQUIRED.get(md_type, []):
        if required_when(fm) and not fm.get(field):
            errors.append(f"{file_path}: '{field}' required given current status")

    if "status" in fm and fm["status"] not in STATUS_VALUES[md_type]:
        errors.append(f"{file_path}: invalid status '{fm['status']}' for {md_type} (allowed: {STATUS_VALUES[md_type]})")

    return errors

if __name__ == "__main__":
    all_errors = []
    for md_file in Path(".").rglob("*.md"):
        all_errors.extend(validate(md_file))
    for err in all_errors:
        print(err)
    sys.exit(1 if all_errors else 0)
```

#### A.2 KRISA staleness detector `[PLANNED v1.1]`

```python
# scripts/detect_krisa_staleness.py
#
# STATUS: STUB. Not implemented in v1.0.
# Until v1.1, BAs do the staleness check manually during weekly status prep (see 4.7).
#
# v1.1 implementation plan:
# 1. For each .docx in deliverables/:
#    a. Extract the "Source MD commit: <hash>" line from the document footer
#       (python-docx + paragraph scan).
#    b. Map each KRISA section heading to its source REQ-IDs
#       (parse hidden comments left by the fill prompt — see 4.6).
# 2. For each REQ cited by any KRISA section:
#    a. Get the REQ's git log since the footer commit (`git log <hash>..HEAD -- requirements/REQ-XXX*.md`).
#    b. If any commits exist → the REQ has changed → flag the citing sections as stale.
# 3. Post the stale-section list to Teams via webhook + write a summary to
#    `dashboard/krisa-staleness.md`.
#
# Blocking decisions before implementing:
# - Word-doc parsing reliability (python-docx vs LibreOffice CLI vs Word-COM on a Win VPS).
# - Section-to-REQ mapping: do we require an explicit `<!-- REQ: REQ-042 -->` comment
#   in each filled section, or infer from the section's body text? Explicit is safer.
# - Run cadence: nightly cron vs on-PR-to-deliverables? Nightly likely sufficient.
```

#### A.3 REQ-ID commit check (Git hook)

```bash
#!/bin/sh
# .githooks/commit-msg
if ! grep -qE '(REQ|TASK|FB|INC|CR|DEC)-[0-9]+' "$1"; then
    echo "ERROR: commit message must reference at least one work-item ID (REQ/TASK/FB/INC/CR/DEC)"
    exit 1
fi
```

#### A.4 `_index.md` + `_prompts.md` validator and regenerator

```python
# scripts/regen_indexes.py
"""
Tier-aware validator and catalog regenerator for the Censof AI-DLC repo layout.

Walks the repo, classifies each folder into Tier A / B / C (see 3.2.0):
- Tier A (managed knowledge): requires both _index.md AND _prompts.md.
- Tier B (code/infra): requires _index.md; _prompts.md only validated if present.
- Tier C (tool-managed, generated, or unknown): silently skipped.

For each non-C folder, regenerates the auto-managed catalog region of _index.md
and validates frontmatter (folder/purpose/owner/file_naming/last_updated/
ai_navigation_hint). For Tier A, also validates _prompts.md frontmatter and
required sections (OP-/Forbidden/Escalate).

Idempotent: re-running on an unchanged tree produces zero diff. Frontmatter
`last_updated` bumps only when catalog content actually changes. CI-safe.

Run in CI on every PR. Exits non-zero if any Tier A folder lacks either
mandatory file, any Tier B folder lacks _index.md, or any frontmatter is
incomplete.
"""

import sys
import yaml
import re
from pathlib import Path
from datetime import date, datetime

AUTO_MARKER = "<!-- auto-managed below -->"

# Tier C — always skipped (no MD discipline applies).
# Includes tool-managed dirs AND generated/export subfolders that may live inside Tier A parents.
SKIP_DIRS = {
    # Tool-managed
    ".git", ".obsidian", ".github", "node_modules", "__pycache__",
    "dist", "build", ".venv", "venv", ".pytest_cache", ".mypy_cache",
    # Generated / export subfolders (often inside dashboard/, deliverables/, raw-inputs/)
    "exports", "snapshots", "cache", "_generated", "tmp",
}

# Tier A — must have BOTH _index.md and _prompts.md:
TIER_A_PATTERNS = [
    "requirements", "spec", "design", "tasks", "feedback",
    "decisions", "incidents", "prompts", "deliverables",
    "dashboard", "raw-inputs", "signoffs", "change-requests",
    "00-overview", "adrs",
]

# Tier B — must have _index.md; _prompts.md optional (recommended for runbooks, alerts, tests):
TIER_B_PATTERNS = [
    "services", "libs", "infra", "runbooks", "alerts", "tests", "scripts",
]

def folder_tier(folder: Path, repo_root: Path | None = None) -> str:
    """Classify folder into tier A, B, or C based on path parts.

    Rules (in order):
      1. Any path part in SKIP_DIRS → Tier C (always wins).
      2. Any path part in TIER_A_PATTERNS → Tier A.
      3. Any path part in TIER_B_PATTERNS → Tier B.
      4. The repo root itself (when no pattern matched) → Tier A — this is where
         root _index.md + _prompts.md live.
      5. Otherwise → Tier C — unknown folders are skipped by default.
         Rationale: a folder the user created without any Tier-A/B intent
         (e.g., scratch/, notes/, tmp-bits/) shouldn't be forced into the
         _index.md/_prompts.md regime. If the user wants it tracked, they
         should add the folder name to TIER_A_PATTERNS or TIER_B_PATTERNS.
    """
    parts = set(folder.parts)
    if parts & SKIP_DIRS:
        return "C"
    if any(p in parts for p in TIER_A_PATTERNS):
        return "A"
    if any(p in parts for p in TIER_B_PATTERNS):
        return "B"
    if repo_root is not None and folder.resolve() == repo_root.resolve():
        return "A"
    return "C"

# Note: deliverables/ DOES have _index.md + _prompts.md (tracks D01-D18 docx files);
# only the .docx files inside are non-MD. Script catalogs the docx by stat, not frontmatter.

def find_md_folders(root: Path) -> list[Path]:
    """Return every folder that should have _index.md/_prompts.md per tier policy.

    Includes empty folders too — a freshly-scaffolded Tier A folder must still
    be validated, otherwise CI silently passes a missing-mandatory-file. Tier C
    folders are filtered via SKIP_DIRS path-part check (applied to root and
    all descendants uniformly).
    """
    folders = []
    # Validate root only if it's not itself inside a SKIP_DIR (guards against
    # accidentally running the script from inside .git/, dist/, etc.).
    if not any(part in SKIP_DIRS for part in root.resolve().parts):
        folders.append(root)
    for d in root.rglob("*"):
        if not d.is_dir():
            continue
        if any(part in SKIP_DIRS for part in d.parts):
            continue
        folders.append(d)
    return folders

def parse_frontmatter(file_path: Path) -> dict:
    text = file_path.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m: return {}
    try: return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError: return {}

def build_catalog(folder: Path) -> str:
    """Build a Markdown table cataloging files in this folder (not recursive).
    MD files: read frontmatter for rich metadata. Non-MD (e.g., .docx in deliverables/): list with mtime only."""
    rows = []
    for f in sorted(folder.iterdir()):
        if not f.is_file(): continue
        if f.name in ("_index.md", "_prompts.md"): continue
        if f.name.startswith("."): continue
        if f.suffix == ".md":
            fm = parse_frontmatter(f)
            # Owner fallback across all MD types. Null-safe: every step uses `or`
            # so any falsy value (None, empty string, empty list) falls through to
            # the next candidate, terminating at the literal "—".
            participants = fm.get("participants")
            participant_lead = participants[0] if isinstance(participants, list) and participants else None
            owner = (fm.get("owner")
                     or fm.get("assignee")
                     or fm.get("incident_commander")
                     or participant_lead
                     or fm.get("raised_by")
                     or fm.get("team")
                     or "—")
            updated = (fm.get("last_updated")
                       or fm.get("created")
                       or fm.get("date")
                       or "—")
            rows.append({
                "file": f.name,
                "id": fm.get("id") or "—",
                "title": fm.get("title") or f.stem,
                "status": fm.get("status") or "—",
                "owner": owner,
                "updated": updated,
            })
        else:
            # Non-MD file (e.g., .docx, .pdf): minimal catalog row
            mtime = datetime.fromtimestamp(f.stat().st_mtime).date().isoformat()
            rows.append({
                "file": f.name,
                "id": "—",
                "title": f.stem,
                "status": "—",
                "owner": "—",
                "updated": mtime,
            })

    if not rows:
        return "_(empty)_"

    lines = ["| File | ID | Title | Status | Owner | Updated |",
             "|------|----|----|--------|-------|---------|"]
    for r in rows:
        lines.append(f"| [{r['file']}]({r['file']}) | {r['id']} | {r['title']} | {r['status']} | {r['owner']} | {r['updated']} |")
    return "\n".join(lines)

INDEX_REQUIRED_FIELDS = ["folder", "purpose", "owner", "file_naming", "last_updated", "ai_navigation_hint"]
PROMPTS_REQUIRED_FIELDS = ["folder", "purpose_of_this_file", "canonical_prompts_location", "last_updated", "ai_behavior_hint"]
PROMPTS_REQUIRED_SECTIONS = ["## OP-", "## Forbidden", "## Escalate"]

def validate_index_frontmatter(folder: Path) -> tuple[bool, str]:
    """Validate that _index.md frontmatter contains required fields with non-empty values.
    A field key alone is not enough — empty string / null / empty list fail validation.
    """
    index_file = folder / "_index.md"
    if not index_file.exists():
        return True, ""  # regenerate_index() already reports missing-file errors
    fm = parse_frontmatter(index_file)
    # `if not fm.get(f)` catches missing key, None, empty string, empty list/dict.
    missing_or_empty = [f for f in INDEX_REQUIRED_FIELDS if not fm.get(f)]
    if missing_or_empty:
        return False, f"INCOMPLETE FRONTMATTER: {index_file} — missing or empty: {missing_or_empty}"
    return True, f"FRONTMATTER OK: {index_file}"

def bump_frontmatter_last_updated(text: str) -> str:
    """Replace or insert `last_updated:` in frontmatter with today's date."""
    today = date.today().isoformat()
    fm_match = re.match(r'^(---\n)(.*?)(\n---)', text, re.DOTALL)
    if not fm_match:
        return text  # no frontmatter — leave alone
    head, body, tail = fm_match.groups()
    if re.search(r'^last_updated:', body, re.MULTILINE):
        new_body = re.sub(r'^last_updated:.*$', f'last_updated: {today}', body, flags=re.MULTILINE)
    else:
        new_body = body.rstrip() + f'\nlast_updated: {today}'
    return text[:fm_match.start()] + head + new_body + tail + text[fm_match.end():]

def regenerate_index(folder: Path, tier: str = "A") -> tuple[bool, str]:
    """Returns (ok, message). Updates _index.md catalog region and bumps
    frontmatter last_updated ONLY when the catalog content actually changed.
    Idempotent: re-running on an unchanged tree produces zero diff.
    """
    index_file = folder / "_index.md"
    if not index_file.exists():
        return False, f"MISSING: {index_file} — Tier {tier} folder requires _index.md"

    content = index_file.read_text(encoding='utf-8')
    if AUTO_MARKER not in content:
        return False, f"NO MARKER: {index_file} — must contain '{AUTO_MARKER}' for catalog injection"

    before, _ = content.split(AUTO_MARKER, 1)
    catalog = build_catalog(folder)
    # Deterministic auto-region: no daily date stamp. Per-file "Updated" column
    # in the catalog already records mtimes; folder-level last_updated is in
    # frontmatter and only bumps when the catalog actually changes.
    new_content_no_bump = f"{before}{AUTO_MARKER}\n\n## Auto-generated catalog\n\n{catalog}\n"

    if new_content_no_bump == content:
        return True, f"UP-TO-DATE: {index_file}"

    # Catalog content changed → bump frontmatter last_updated to today
    new_content = bump_frontmatter_last_updated(new_content_no_bump)
    index_file.write_text(new_content, encoding='utf-8')
    return True, f"REGENERATED: {index_file}"

def validate_prompts(folder: Path, tier: str = "A") -> tuple[bool, str]:
    """Returns (ok, message). Checks _prompts.md exists and has required fields/sections.
    Caller decides whether to invoke this (Tier A always; Tier B only if file present)."""
    prompts_file = folder / "_prompts.md"
    if not prompts_file.exists():
        return False, f"MISSING: {prompts_file} — Tier {tier} folder requires _prompts.md"

    content = prompts_file.read_text(encoding='utf-8')
    fm = parse_frontmatter(prompts_file)

    missing_fields = [f for f in PROMPTS_REQUIRED_FIELDS if not fm.get(f)]
    if missing_fields:
        return False, f"INCOMPLETE: {prompts_file} — missing or empty frontmatter: {missing_fields}"

    missing_sections = [s for s in PROMPTS_REQUIRED_SECTIONS if s not in content]
    if missing_sections:
        return False, f"INCOMPLETE: {prompts_file} — missing required sections: {missing_sections}"

    return True, f"OK: {prompts_file}"

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    folders = find_md_folders(root)

    failed = []
    for folder in folders:
        tier = folder_tier(folder, repo_root=root)
        if tier == "C":
            print(f"SKIP (Tier C): {folder}")
            continue

        ok_idx, msg_idx = regenerate_index(folder, tier=tier)
        print(f"[Tier {tier}] {msg_idx}")
        if not ok_idx: failed.append(msg_idx)

        ok_fm, msg_fm = validate_index_frontmatter(folder)
        if msg_fm:
            print(f"[Tier {tier}] {msg_fm}")
        if not ok_fm: failed.append(msg_fm)

        if tier == "A":
            ok_prm, msg_prm = validate_prompts(folder, tier=tier)
            print(f"[Tier {tier}] {msg_prm}")
            if not ok_prm: failed.append(msg_prm)
        else:  # Tier B — _prompts.md optional; only validate if present
            prompts_file = folder / "_prompts.md"
            if prompts_file.exists():
                ok_prm, msg_prm = validate_prompts(folder, tier=tier)
                print(f"[Tier {tier}] {msg_prm}")
                if not ok_prm: failed.append(msg_prm)

    if failed:
        print(f"\n{len(failed)} validation failure(s).")
        sys.exit(1)
    print(f"\nAll required folders have valid _index.md (+ _prompts.md where mandatory).")
```

In CI (`.github/workflows/ci.yml`):

```yaml
- name: Regenerate _index.md files
  run: python scripts/regen_indexes.py .

- name: Fail if any _index.md changed (PR must include regenerated files)
  run: |
    if [ -n "$(git status --porcelain)" ]; then
      echo "ERROR: _index.md files are out of date. Run 'python scripts/regen_indexes.py .' locally and commit."
      git diff
      exit 1
    fi
```

#### A.5 Auto-close TASK on PR merge `[PLANNED v1.1]`

```python
# scripts/close_task_on_pr_merge.py
#
# STATUS: STUB. v1.0 = developers update TASK MDs manually after merging.
#
# v1.1 implementation plan:
# Triggered by GitHub Actions on pull_request.closed (merged == true).
# 1. Extract TASK-IDs from PR title + all commit messages (regex: TASK-\d+).
# 2. For each TASK-ID found:
#    a. Open requirements-repo (via PAT-authenticated git clone).
#    b. Locate tasks/sprint-NN/TASK-XXX-*.md.
#    c. Parse frontmatter; verify current status in [in-progress, review].
#       (If status is already done or todo, log a warning and skip — don't silently overwrite.)
#    d. Update frontmatter:
#         status: done
#         completed: <today>
#         pr: <PR URL>
#         actual_hours: <if dev typed "actual: Xh" in PR description, else leave null>
#    e. Commit + push to requirements-repo with message "auto-close: TASK-XXX from PR #234".
# 3. Post a single summary line to Teams: "PR #234 auto-closed TASK-101, TASK-102."
#
# Edge cases:
# - PR cites a TASK that doesn't exist → log + Teams notify, don't fail merge.
# - PR cites only a REQ-ID with no TASK → do nothing (REQ status changes via A.7).
# - Multiple PRs cite same TASK (e.g., follow-up fix) → second one logs warning, doesn't re-flip.
```

#### A.6 Build REQ ↔ test coverage map `[PLANNED v1.1]`

```python
# scripts/build_test_coverage_map.py
#
# STATUS: STUB. v1.0 = BA manually spot-checks Test DoD per REQ at sprint close.
#
# v1.1 implementation plan:
# 1. Walk code-repo/tests/ for files matching test_*.py, *_test.go, *.spec.ts, etc.
# 2. For each test file:
#    a. Grep for REQ-\d+ in test names, docstrings, and inline comments.
#    b. If a CI test-results artifact is available (junit.xml etc.), match test name → pass/fail.
# 3. Build a map: { REQ-ID: [(test_file, test_name, pass/fail), ...] }
# 4. Write dashboard/req-test-coverage.md with a Dataview-friendly table:
#    | REQ-ID | Test files | Test count | Pass rate | Last run |
#    | REQ-042 | test_login_2fa.py | 5 | 100% | 2026-05-26 |
#    | REQ-043 | test_password_reset.py | 3 | 67% | 2026-05-26 |
#    | REQ-044 | (none) | 0 | — | — |
# 5. Run nightly via cron + after every CI test run.
#
# Output drives:
# - Dashboard "REQs without tests" query (DoD failure)
# - Health-score component test_coverage_by_req
```

#### A.7 REQ readiness check `[PLANNED v1.1]`

```python
# scripts/check_req_readiness.py
#
# STATUS: STUB. v1.0 = BA manually decides when a REQ is ready for client acceptance.
#
# v1.1 implementation plan:
# Triggered on any TASK MD frontmatter change OR on CI test run completion.
# For each REQ where status == "in-dev":
#   1. Collect all linked TASK-IDs (from REQ frontmatter "tasks" field).
#   2. Check every linked task has status == "done".
#   3. Check REQ body has no remaining "[TBD]" markers.
#   4. Check REQ's test_ref file exists in code-repo.
#   5. Check req-test-coverage.md shows pass rate == 100% for this REQ.
#   6. If ALL above true:
#      - Update REQ frontmatter: status = "ready-for-acceptance" (NEW intermediate state).
#      - Post to Teams: "REQ-042 ready for BA + client acceptance review."
#      - Add row to dashboard/awaiting-acceptance.md.
#
# Crucial constraint: NEVER auto-flip REQ to status: done. That requires:
#   - BA verifies all acceptance criteria met (subjective check)
#   - Client signoff (email or PR co-approval, archived in signoffs/)
#
# Note: "ready-for-acceptance" already in STATUS_VALUES["requirements"] in validate_frontmatter.py (A.1).
```

#### A.8 Design ↔ code drift detector `[PLANNED v1.1]`

```python
# scripts/design_to_code_drift.py
#
# STATUS: STUB. v1.0 = tech lead manually reviews design vs code during sprint retro.
#
# v1.1 implementation plan:
# 1. Parse design/api-contracts.md for declared endpoints (path, method).
# 2. Run Graphify on code-repo; query the graph for matching handler functions
#    (framework-specific: @app.route in Flask, app.get in Express, etc.).
# 3. For each declared endpoint:
#    - if no matching handler → drift type: "missing implementation"
#    - if handler exists but signature differs → drift type: "signature mismatch"
# 4. Parse design/data-model.md for declared tables/columns.
# 5. Introspect actual DB schema (information_schema query).
# 6. For each declared table:
#    - if missing → "missing migration"
#    - if column differs → "schema mismatch"
# 7. Write dashboard/design-drift.md with table of findings.
# 8. Run nightly via cron.
#
# Dependencies:
#   - Graphify must support the project's language(s) and have a query API.
#   - DB introspection requires read-only credentials in GitHub Secrets.
#
# Limit: drift detection is informational, not blocking — flags mismatch for human triage.
#   Some drift is intentional (e.g., spec was rewritten but migration pending).
```

### Appendix B — Prompt library

Stored in `prompts/`. Listed here for reference:

- `fill-krisa-section.md` — fill one section of a KRISA Word template
- `triage-feedback.md` — classify INBOX feedback into FB MDs
- `req-check.md` — drift detection across requirements ↔ spec ↔ design ↔ tasks
- `code-review.md` — review a PR against DoD
- `code-review-pass-2.md` — Claude B critique of Claude A's code
- `generate-test.md` — generate tests for a given REQ-ID's acceptance criteria
- `weekly-status-report.md` — generate weekly client status PDF
- `sprint-retro-draft.md` — draft retro.md from sprint data
- `ingest-raw-input.md` — convert raw client input (transcript, email) to draft REQ MD
- `dod-check.md` — check a single artifact against its DoD
- `incident-postmortem-draft.md` — draft postmortem from incident timeline
- `comms-template-fill.md` — fill an incident comms template

Each prompt MD has frontmatter (version, owner, when-to-use) and a body. See 13.2 for format.

### Appendix C — Folder layout cheat sheet

**Tier A (managed knowledge) folders have both `_index.md` and `_prompts.md`. Tier B (code/infra) folders have `_index.md` (and `_prompts.md` if operations exist). Tier C folders are exempt. See 3.2.0 for the full tier policy.**

- `_index.md` — what is here (passive knowledge for AI orientation)
- `_prompts.md` — what to do here (active operations for AI execution)

```
project-x/
├── requirements-repo/                  # MD source of truth (Git)
│   ├── _index.md                       # ★ Root index — start here
│   ├── _prompts.md                     # ★ Root operations — which folder for which task
│   ├── 00-overview/                    # Vision, scope, stakeholders, glossary, teams, security, ai-config
│   │   ├── _index.md
│   │   └── _prompts.md
│   ├── requirements/                   # REQ-XXX.md (one per requirement)
│   │   ├── _index.md                   # REQ-ID ranges, schema, catalog
│   │   └── _prompts.md                 # OPs: create-from-raw, refine-AC, drift-check, approve
│   ├── spec/                           # Domain specs
│   │   ├── _index.md
│   │   └── _prompts.md                 # OPs: create-spec, refine, version-bump
│   ├── design/                         # Design docs
│   │   ├── _index.md
│   │   ├── _prompts.md                 # OPs: create-design, add-ADR, API-contract-change
│   │   └── adrs/
│   │       ├── _index.md               # ADR catalog
│   │       └── _prompts.md             # OPs: draft-ADR, supersede-ADR
│   ├── tasks/                          # Sprint folders with TASK-XXX.md
│   │   ├── _index.md                   # Sprint index + current pointer
│   │   ├── _prompts.md                 # OPs: sprint-plan, create-tasks-from-REQ, assign
│   │   ├── sprint-01/
│   │   │   ├── _index.md               # Sprint goals, dates
│   │   │   └── _prompts.md             # OPs: sprint-open, sprint-close, burndown
│   │   └── sprint-02/
│   │       ├── _index.md
│   │       └── _prompts.md
│   ├── feedback/                       # INBOX.md + sprint folders
│   │   ├── _index.md                   # Triage routing matrix
│   │   ├── _prompts.md                 # OPs: triage-INBOX, classify, route, escalate
│   │   ├── sprint-01/
│   │   │   ├── _index.md
│   │   │   └── _prompts.md             # OPs: retro-draft, feedback-metrics
│   │   └── sprint-02/
│   │       ├── _index.md
│   │       └── _prompts.md
│   ├── change-requests/                # CR-XXX.md (proposed scope changes)
│   │   ├── _index.md                   # CR catalog
│   │   └── _prompts.md                 # OPs: draft-CR, approve-CR, link-to-REQ-revision
│   ├── decisions/                      # DEC-XXX.md
│   │   ├── _index.md                   # DEC catalog
│   │   └── _prompts.md                 # OPs: draft-DEC, supersede-DEC
│   ├── incidents/                      # INC-XXX.md
│   │   ├── _index.md                   # Severity legend + catalog
│   │   └── _prompts.md                 # OPs: postmortem-draft, runbook-update
│   ├── prompts/                        # Versioned Claude prompts
│   │   ├── _index.md                   # Prompt library catalog
│   │   └── _prompts.md                 # OPs: add-new-prompt, version-bump, deprecate
│   ├── deliverables/                   # KRISA Word docs
│   │   ├── _index.md                   # D01-D18 status map
│   │   ├── _prompts.md                 # OPs: fill-KRISA-section, consistency-check, regen
│   │   ├── templates/                  # Blank templates (weekly-status.docx, KRISA blanks)
│   │   │   ├── _index.md               # Catalog of available templates
│   │   │   └── _prompts.md             # OPs: use-template, add-new-template
│   │   └── demos/                      # Sprint demo recordings (.mp4)
│   │       ├── _index.md               # Catalog of demo recordings by sprint
│   │       └── _prompts.md             # OPs: archive-demo, link-demo-to-sprint-retro
│   ├── dashboard/                      # Live Dataview dashboards
│   │   ├── _index.md
│   │   ├── _prompts.md                 # OPs: refresh, HTML-export, weekly-status-PDF, ops-summary
│   │   ├── dashboard.md
│   │   ├── velocity.md
│   │   ├── sprint-board.md
│   │   ├── ops-daily.md                # Daily Claude-generated ops summary
│   │   ├── exports/                    # [Tier C — generated, exempt] HTML snapshots for client
│   │   ├── snapshots/                  # [Tier C — generated, exempt] [PLANNED v1.1] Nightly metric snapshots
│   │   └── queries/
│   │       ├── _index.md
│   │       └── _prompts.md
│   ├── signoffs/                       # Archived client signoffs
│   │   ├── _index.md
│   │   └── _prompts.md                 # OPs: archive-signoff, cross-ref-REQ
│   └── raw-inputs/                     # Workshop transcripts, source emails
│       ├── _index.md
│       ├── _prompts.md                 # OPs: capture, transcribe, extract, mark-processed
│       ├── workshops/
│       │   ├── _index.md
│       │   └── _prompts.md
│       ├── client-emails/
│       │   ├── _index.md
│       │   └── _prompts.md
│       └── client-docs/
│           ├── _index.md
│           └── _prompts.md
│
└── code-repo/                          # Code (Git, separate or monorepo subfolder)
    ├── _index.md                       # [Tier A] Code repo overview, service map
    ├── _prompts.md                     # [Tier A] OPs: build, test, deploy, debug-with-logs
    ├── licenses.md                     # Dep license register (manual, see 10.6)
    ├── services/
    │   └── _index.md                   # [Tier B] Service catalog (no _prompts unless ops needed)
    ├── libs/
    │   └── _index.md                   # [Tier B]
    ├── infra/
    │   ├── _index.md                   # [Tier B]
    │   ├── redact-logs.sh              # Strip secrets/PII before AI log paste (see 11.6)
    │   ├── feature-flags.md            # Active flags + retire dates (see 11.5)
    │   ├── secret-rotation-log.md      # Secret rotation register (not a DEC)
    │   ├── alerts/                     # [Tier B] Alert scripts + thresholds.yml
    │   │   ├── _index.md
    │   │   ├── _prompts.md             # OPs: add-alert, tune-threshold, review-alert-fatigue
    │   │   ├── check.sh
    │   │   └── thresholds.yml
    │   └── runbooks/                   # [Tier B] Per-service / per-issue runbooks
    │       ├── _index.md
    │       ├── _prompts.md             # OPs: lookup-runbook, update-runbook-from-incident
    │       ├── comms-templates.md
    │       ├── auth-service.md
    │       └── security-incident.md
    ├── tests/
    │   ├── _index.md                   # [Tier B] Test organization, REQ-ID coverage map
    │   └── _prompts.md                 # OPs: generate-test-for-REQ, regen-coverage-map
    ├── .github/                        # [Tier C — exempt]
    │   ├── CODEOWNERS
    │   ├── workflows/
    │   └── (no _index.md required)
    └── scripts/                        # [Tier B] Validators, generators
        └── _index.md                   # (_prompts.md only if scripts grow operations)
```

**CI fails the PR if a Tier A folder lacks either `_index.md` or `_prompts.md`, or a Tier B folder lacks `_index.md`. Tier C folders (see 3.2.0) are silently skipped.**

### Appendix D — Checklists summary

- **Project kickoff:** see 15.1
- **Security review:** see 10.7
- **REQ DoD:** see 9.2
- **Spec DoD:** see 9.2
- **Design DoD:** see 9.2
- **Task DoD:** see 9.2
- **Code DoD:** see 9.2
- **Test DoD:** see 9.2
- **Deploy DoD:** see 9.2
- **Sprint DoD:** see 9.2
- **Incident response steps:** see 12.2
- **Hotfix flow:** see 12.8
- **Release process:** see 11.3

### Appendix E — Glossary of playbook terms

| Term           | Definition                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| AI-DLC         | AI-assisted Development Lifecycle (this playbook)                                                                                   |
| MD             | Markdown                                                                                                                            |
| REQ            | Requirement (e.g., REQ-042)                                                                                                         |
| Spec           | Specification (elaboration of a requirement)                                                                                        |
| Design         | Technical design (how a spec will be built)                                                                                         |
| Task           | A unit of work assigned to a developer                                                                                              |
| FB             | Feedback item (e.g., FB-042)                                                                                                        |
| CR             | Change Request (e.g., CR-001)                                                                                                       |
| INC            | Incident postmortem (e.g., INC-001)                                                                                                 |
| DEC            | Decision record                                                                                                                     |
| ADR            | Architecture Decision Record                                                                                                        |
| DoD            | Definition of Done                                                                                                                  |
| AC             | Acceptance Criterion                                                                                                                |
| NFR            | Non-Functional Requirement                                                                                                          |
| BA             | Business Analyst                                                                                                                    |
| KRISA          | Malaysian government documentation standard for IT projects                                                                         |
| SRS            | System Requirements Specification (D03)                                                                                             |
| SDS            | System Design Specification (D04)                                                                                                   |
| BRS            | Business Requirements Specification (D02)                                                                                           |
| PPS            | Sistem Development Plan (D01)                                                                                                       |
| UAT            | User Acceptance Testing                                                                                                             |
| PAT            | Provisional Acceptance Testing                                                                                                      |
| TOIL           | Time Off In Lieu                                                                                                                    |
| IC             | Incident Commander                                                                                                                  |
| DPO            | Data Protection Officer                                                                                                             |
| PII            | Personally Identifiable Information                                                                                                 |
| PDPA           | Personal Data Protection Act (Malaysia)                                                                                             |
| RAW            | Raw input record (e.g., RAW-001) — workshop transcript, client email, source doc                                                   |
| OP             | An operation defined in a folder's `_prompts.md` (e.g., OP-1 in requirements/_prompts.md)                                         |
| Tier A / B / C | Folder tier policy controlling whether `_index.md` and `_prompts.md` are mandatory (see 3.2.0)                                  |
| Caveman mode   | Token-efficient Claude conversation convention (`/caveman full`) — see 2.6                                                       |
| Standard stack | The six named tools (2.1) + their built-in platform features (2.2) + the VPS OS                                                     |
| VPS            | Virtual Private Server — the Linux host where Censof projects deploy                                                               |
| M365           | Microsoft 365 — provides OneDrive, SharePoint, Teams, Outlook in our stack                                                         |
| MFA            | Multi-Factor Authentication                                                                                                         |
| TOTP           | Time-based One-Time Password (RFC 6238) — used as 2FA factor in examples                                                           |
| 2FA            | Two-Factor Authentication                                                                                                           |
| MD type        | The category of a Markdown file based on its folder (REQ, Task, FB, Spec, Design, ADR, DEC, INC, CR, RAW) — drives validator rules |

### Appendix F — Maintenance of this playbook

This playbook is updated:

- After every project retrospective: lessons learnt incorporated.
- When a tool changes significantly: tool sections refreshed.
- When a new failure mode is observed: section added or amended.
- Quarterly: full review by Censof tech leadership.

Updates follow the same MD-then-review-then-merge flow used for project work. The playbook itself eats its own dog food.

Maintainer: Arvindh (arvindh@censof.com).
Contributors: anyone via PR.

---

**End of Playbook v1.0**

> "Process is the scar tissue of past failures. This playbook is Censof's scar tissue — keep adding to it."
