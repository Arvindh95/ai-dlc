---
id: PROMPT-03
name: Drift / traceability check across REQs
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - requirements/_prompts.md OP-3
  - ROOT/_prompts.md OP-3
---

# Prompt: REQ drift and traceability check

## Purpose
Verify every approved REQ has resolvable refs (spec, design, tasks, test) and no dangling references.

## Inputs
- None (scans repo)

## Output
- Report file at `dashboard/drift-report.md`
- Summary to console

## Prompt body
```
You are running a drift check across all REQs in this repo.

For each MD file in requirements/ with status in [approved, in-dev, ready-for-acceptance, done]:

1. Read frontmatter fields: spec_ref, design_ref, tasks, test_ref.

2. For each non-null ref:
   - spec_ref: resolve to spec/<path>#<anchor>. Verify file exists AND anchor exists.
   - design_ref: same.
   - tasks: list of TASK-IDs. Verify each TASK file exists under tasks/sprint-*/.
   - test_ref: resolve to code-repo test file path. Verify file exists (if code-repo is mounted).

3. Compute drift signals:
   - REQ status == "done" but any TASK status != "done"
   - REQ.last_updated > 30 days but no recent task or test activity
   - spec/design has higher version than REQ's spec_ref/design_ref anchor

4. Write dashboard/drift-report.md:
   ## REQ drift report — <today>

   ### Broken refs (P0)
   | REQ | Broken field | Target |
   |-----|--------------|--------|
   ...

   ### Status / task mismatch (P1)
   | REQ | REQ status | TASK status |
   |-----|------------|-------------|
   ...

   ### Stale REQs (P2 — no activity 30d+)
   ...

   ### Version drift (P2)
   ...

5. Append to Change Log of dashboard/drift-report.md:
   - <today>: <N> P0, <N> P1, <N> P2 findings.

Report total counts to console.
```

## Guardrails
- Do NOT auto-fix anything — report only
- Do NOT change any REQ frontmatter or status
- If `test_ref` field references a file outside this repo (code-repo), mark as "unverified" rather than broken
