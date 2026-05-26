# AI-DLC Requirements Repo — Template

This is the **template scaffold** for an AI-DLC source-of-truth requirements repo. Each new project starts as a fresh, independent copy of this template — no fork, no upstream tracking, no auto-updates.

## How to use this template

**Do NOT `git clone` this repo to start a new project** — that would inherit the template's commit history. Use one of these instead:

1. **"Use this template" button (recommended)** — On the GitHub repo page, click the green **"Use this template"** button → **"Create a new repository"**. GitHub creates a fresh repo under your account/org with no template git history but already wired up to GitHub. Then `git clone` *that* new repo to your machine and follow `KICKOFF.md`.

2. **Download ZIP** — On the GitHub repo page, click **"Code" → "Download ZIP"**. Unzip into your project folder. Then `git init` to start your own version-controlled repo from scratch:
   ```powershell
   cd C:\Projects\<your-project-slug>
   git init
   git config core.hooksPath .githooks
   git add -A
   git commit -m "REQ-000: scaffold from AI-DLC template v<X.Y>"
   git remote add origin https://github.com/<org>/<your-project>.git
   git push -u origin main
   ```

Either way, your project's git history starts fresh. The template's version (see `CHANGELOG.md`) is recorded in your first commit so you know what you forked from.

## After instantiation

Open the folder in Claude Code. Say "Run kickoff". Claude reads `CLAUDE.md` → root `_index.md` → root `_prompts.md` → triggers OP-0 (kickoff) → walks you through `KICKOFF.md` step-by-step.

Until kickoff is complete, `project_id`, `client`, owner names and contract dates show `TBD-set-at-kickoff`. The folder structure, schemas, prompts, and CI are project-agnostic and ready to use.

## AI quickstart (every session)

1. Read `CLAUDE.md` (session bootstrap)
2. Read `_index.md` (project metadata + folder map)
3. Read `_prompts.md` (top-level operations)
4. Navigate to the relevant Tier A folder, repeat 2–3

## CI

- `scripts/validate_frontmatter.py` — record schema check
- `scripts/regen_indexes.py` — Tier A/B index + prompts validator + catalog regen

## Template lifecycle

The template is **maintained as its own repo**; existing projects do NOT auto-update when the template is enhanced. See `CHANGELOG.md` for version history. To adopt later improvements into an existing project, manually diff against the new template version and port the changes you want.

Built from AI-DLC Playbook v1.0 — see `AI-DLC-Playbook.md` at the repo root for the full canonical spec (~3,870 lines).
