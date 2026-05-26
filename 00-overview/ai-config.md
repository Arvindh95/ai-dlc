# AI Configuration

## Model pinning

| Tier | Use case | Model | Notes |
|------|----------|-------|-------|
| Premium | Spec / design / ADR drafting, KRISA fill | claude-opus-4-7 | Highest reasoning quality |
| Standard | Task generation, refactoring, code review | claude-sonnet-4-6 | Default for code work |
| Fast | Triage, summarisation, classification | claude-haiku-4-5 | Lowest latency |

## Approved tools (Censof AI-DLC stack)
- **Claude** — Code (CLI), claude.ai web, in-Word via M365 connector
- **Obsidian** — local PM dashboard (Dataview, Kanban, Tasks, Calendar, Templater)
- **GitHub** — version control, CI, CODEOWNERS, PR review
- **OneDrive / M365** — source-of-truth storage, in-Word AI connector
- **Graphify** — code-context graph for dev sessions
- **Caveman mode** — token-saving conversation convention (not a tool)

## Not approved (do not use)
- Other LLMs for project work (ChatGPT, Gemini, etc.) — Censof AI policy
- Cursor / Windsurf — not on supported list yet
- External diagramming SaaS that uploads content (Mermaid live, draw.io public, etc.) — use local Obsidian Mermaid

## Prompt-source-of-truth
Canonical prompts live in `prompts/` (this repo). Versioned. Never inline a prompt in a `_prompts.md` OP — link the canonical file.

## Change Log
- 2026-05-26: Template created with default Censof stack.
