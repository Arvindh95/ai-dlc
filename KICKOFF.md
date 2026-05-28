# KICKOFF — Instantiate this template for a new project

This is a **template scaffold**. Until you complete the steps below, every search for `TBD-set-at-kickoff` will turn up unfilled fields.

You can do this manually, or ask Claude: **"Run kickoff"** — Claude will walk you through this checklist interactively (root `_prompts.md` OP-0).

---

## Step 1 — Clone the template (skip if you already cloned)

Copy the entire `AI-DLC/` folder to a new project location. Rename to your project slug.

```powershell
$dst = "C:\Users\<you>\OneDrive - Censof Holdings\Desktop\Projects\<project-slug>"
Copy-Item -Path "C:\...\AI-DLC" -Destination $dst -Recurse
```

## Step 2 — Fill root metadata

Open `_index.md` at the root. In the frontmatter, replace these `TBD-set-at-kickoff` values:

| Field | Example |
|-------|---------|
| `project_id` | `PROJ-ALPHA` or `2026-CRM-MIGRATION` |
| `client` | `Acme Bank` |
| `contract_start` | `2026-06-01` |
| `contract_end` | `2027-02-28` |
| `current_sprint` | leave as `sprint-01` |

## Step 3 — Fill `00-overview/`

Seven files, ~30 min total:

- [ ] `vision.md` — one paragraph, what success looks like + headline non-scope item
- [ ] `scope.md` — in-scope / out-of-scope / assumptions / constraints
- [ ] `stakeholders.md` — 5 stakeholder rows (Sponsor, BO, IT Lead, DPO, Account Manager) + comms channels
- [ ] `teams.md` — **single source of truth for names**. Map PM / BA Lead / Tech Lead / Devs → real people
- [ ] `security.md` — data classification, DPO contact, compliance frameworks
- [ ] `cadence.md` — sprint length, total sprints, working week, ceremony schedule
- [ ] `tech.md` — code repo URL, target stack, environments
- [ ] `ai-config.md` — already filled with Censof defaults; only edit if model strategy changes

Plus seed `risks/` with 3-5 RISK-NNN records.

> All other `_index.md` files refer to **role labels** (`owner: PM`, `owner: BA Lead`, `owner: Tech Lead`) — they don't need name updates. Names live only in `teams.md`.

## Step 4 — Set the first sprint

Open `tasks/sprint-01/_index.md`. Fill:

- [ ] Sprint goals
- [ ] Sprint start + end dates
- [ ] Planned REQs (empty until you generate them from `raw-inputs/`)

## Step 5 — Drop KRISA Word templates

If your contract requires KRISA D01–D18 deliverables:

- [ ] Copy your blank `D01-PPS.docx`, `D02-BRS.docx`, … into `deliverables/templates/`
- [ ] Copy `weekly-status.docx` template into `deliverables/templates/`

> If contract doesn't require KRISA, leave `deliverables/` mostly empty — keep `_index.md` + `_prompts.md`.

## Step 6 — Configure git + CI

```powershell
cd <project-folder>
git init
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg   # WSL/git-bash; on pure Windows the hook still runs in git-bash invoker
git add -A
git commit -m "REQ-000: initial scaffold from AI-DLC template"
```

Set the remote to a fresh repo (do NOT push to a shared repo's `main` until reviewed):

```powershell
git remote add origin https://github.com/<org>/<project-slug>.git
git push -u origin main
```

CI from `.github/workflows/ci.yml` runs both validators on every PR.

## Step 7 — Set up Obsidian vault on the repo

- [ ] Open the project folder as an Obsidian vault
- [ ] Install plugins: Dataview, Kanban, Tasks, Calendar, Templater
- [ ] Open `dashboard/dashboard.md` — Dataview blocks render against your REQ/TASK/FB frontmatter

## Step 8 — Capture your first raw input

Drop the first workshop transcript / client email / source doc into the matching `raw-inputs/` subfolder. In Claude: **"Process this raw input."**

That triggers root `_prompts.md` OP-2 → routes to `raw-inputs/_prompts.md` OP-3 (extract) → routes to `requirements/_prompts.md` OP-1 (create from raw). First REQ files land in `requirements/` as `status: draft`.

## Step 9 — Run validators locally

```powershell
python scripts/validate_frontmatter.py .
python scripts/regen_indexes.py .
git status                       # should be clean if regen made no changes
```

## Step 10 — Search for any unfilled placeholders

```powershell
Select-String -Path . -Pattern "TBD-set-at-kickoff" -Recurse
```

If anything still shows, fill it before sprint-01 starts.

---

## Kickoff completion criteria (Definition of Done)

- [ ] No `TBD-set-at-kickoff` strings anywhere in the repo (except this `KICKOFF.md` itself)
- [ ] `teams.md` has real names for PM, BA Lead, Tech Lead
- [ ] `vision.md` has actual vision text (not example block)
- [ ] `stakeholders.md` has all 5 default rows filled + Approver-of + Communication channels section
- [ ] `security.md` has DPO contact + data classification table filled
- [ ] `cadence.md` has sprint length + ceremony schedule filled
- [ ] `tech.md` has code repo URL + stack table + environments table filled
- [ ] `risks/` has 3-5 RISK-NNN-*.md seed records
- [ ] First sprint folder has goal + dates
- [ ] Both validators pass
- [ ] First commit landed with a work-item ID

When all boxes are checked, the template is **instantiated** and ready for sprint-01.
