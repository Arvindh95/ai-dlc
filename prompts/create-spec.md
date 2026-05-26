---
id: PROMPT-04
name: Create spec from approved REQs
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - spec/_prompts.md OP-1
---

# Prompt: Create spec document from approved REQ(s)

## Purpose
Generate or update a domain spec MD that elaborates one or more approved REQs into implementable specification text.

## Inputs
- One or more REQ-IDs (must be status=approved)
- Target domain name (e.g., "auth", "billing")

## Output
- `spec/<domain>-spec.md` (new or updated)
- frontmatter `covers_req` list updated

## Prompt body
```
You are creating a spec for domain "<DOMAIN>" covering REQ-IDs: <list>.

For each REQ-ID:
1. Verify status == "approved". If not, REFUSE — say "REQ-NNN is status=<X>, only approved REQs can be specced. Get signoff first."

2. Read the REQ in full.

If spec/<DOMAIN>-spec.md does NOT exist, create it with:
- Frontmatter:
    id: SPEC-NN-<DOMAIN>
    title: <domain> specification
    status: draft
    version: 0.1.0
    last_updated: <today>
    covers_req: [REQ-..., ...]
- Body sections:
    # SPEC-NN-<DOMAIN> — <title>
    ## Scope
    <which REQs this covers — one line each>
    ## Functional behaviour
    <elaboration of each REQ's behaviour, organised by topic — not REQ order>
    ## Data model
    <entities + fields + relations>
    ## Interfaces
    <APIs / events / contracts>
    ## State machines
    <if applicable>
    ## Constraints
    <perf / security / compliance from REQ NFRs>
    ## Open questions
    - [TBD] ...
    ## Change Log
    - <today>: Created covering <REQ-IDs>.

If spec exists:
- Add new REQ-IDs to covers_req list
- Add or extend relevant section(s) — never overwrite existing approved text
- Bump version (patch if clarification, minor if additive)
- Append Change Log entry

Do NOT mark spec status=approved — that requires tech-lead review.
Do NOT add behaviour not derivable from REQs.
```

## Guardrails
- Only spec approved REQs
- Spec must trace 100% to its covers_req — every claim cites a REQ
- Never edit an approved spec's body without bumping version
