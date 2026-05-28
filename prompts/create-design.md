---
id: PROMPT-05
name: Create design from approved spec
version: 0.2.0
status: active
last_updated: 2026-05-28
used_by:
  - design/_prompts.md OP-1
---

# Prompt: Create technical design from approved spec

## Purpose
Generate a domain design document from an approved spec, producing concrete components, data model, and interfaces.

## Inputs
- SPEC-ID (must be status=approved)

## Output
- `design/<domain>-design.md`
- ADR drafts in `design/adrs/` for any architecture-level decision

## Prompt body
```
You are designing the implementation of SPEC-NN-<DOMAIN>.

1. Read the spec in full.
2. Read 00-overview/security.md for compliance constraints.
3. Read 00-overview/tech.md for target stack (frontend/backend/DB/hosting) + environments.
4. Read design/architecture.md (if exists) for current architecture.

Create design/<DOMAIN>-design.md with:
- Frontmatter:
    id: DES-NN-<DOMAIN>
    title: <domain> design
    status: draft
    version: 0.1.0
    last_updated: <today>
- Body sections:
    # DES-NN-<DOMAIN> — <title>
    ## Source spec
    <link to spec + version>
    ## Components
    <list of components/services/modules + responsibilities>
    ## Data model
    <tables, indexes, constraints — match spec entities>
    ## Sequence flows
    <one numbered sequence per major behaviour from spec>
    ## Error handling
    <how each error class is surfaced>
    ## Observability
    <metrics, logs, traces — must cover SLO mentions in spec>
    ## Security considerations
    <per 00-overview/security.md>
    ## Open questions
    - [TBD] ...
    ## Change Log
    - <today>: Created from SPEC-NN v<X>.

For each architecture-level decision (DB choice, framework, integration pattern, etc.):
- DO NOT decide inline in this design doc
- Draft an ADR in design/adrs/ via the draft-ADR OP
- Reference the ADR-ID in this design

Do NOT proceed with design if spec status != approved.
```

## Guardrails
- Architecture decisions → new ADR, never inline
- Cite spec source for every component / interface
- Security considerations are mandatory — do not skip even if spec didn't mention
