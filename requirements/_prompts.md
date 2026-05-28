---
folder: requirements
purpose_of_this_file: Operations playbook for AI working in this folder
canonical_prompts_location: ../prompts/
last_updated: 2026-05-26
ai_behavior_hint: |
  Match request to OP. Never invent ACs. Use [TBD] for ambiguous parts.
---

# Operations — requirements/

## When you (the AI) are in this folder
Read `_index.md` first, then match the user's request to one of the OPs below by trigger phrase. If no OP matches, do NOT improvise — escalate.

## OP-1: Create new requirement from raw input
- **Trigger phrases:** "create requirement from raw input", "process workshop transcript", "ingest email into REQs", "extract REQs from inventory"
- **Canonical prompt:** `../prompts/ingest-raw-input.md`
- **Inputs:** Source file(s) in `../raw-inputs/` — natural-language inputs (workshops/emails/docs) OR a filled Inventory section in a `../raw-inputs/legacy-system/` sidecar MD
- **Output:** New `REQ-XXX-*.md` files with `status: draft`
- **Inline summary:** Read source, generate one draft REQ per atomic requirement, cite source line ranges, write [TBD] for ambiguous parts, do not invent ACs. For migration inputs, the source is the **Inventory** section (not raw code) — each REQ cites both the inventory item and the original artifact line range. Legacy artifacts must be inventoried first (`../raw-inputs/legacy-system/_prompts.md` OP-2) before REQ extraction.

## OP-2: Refine acceptance criteria
- **Trigger phrases:** "improve AC for REQ-X", "make AC testable"
- **Canonical prompt:** `../prompts/refine-ac.md`
- **Inputs:** REQ-X file
- **Output:** REQ-X with rewritten AC section + Change Log append
- **Inline summary:** Rewrite each AC in Given/When/Then, verify observable/specific/singular. Flag untestable ACs.

## OP-3: Drift check
- **Trigger phrases:** "check req drift", "verify req traceability"
- **Canonical prompt:** `../prompts/req-check.md`
- **Inputs:** none
- **Output:** Report to `../dashboard/drift-report.md`
- **Inline summary:** For each approved REQ, verify spec_ref, design_ref, tasks, test_ref resolve. Report broken links.

## OP-4: Approve workflow
- **Trigger phrases:** "mark REQ approved", "client signed off"
- **Canonical prompt:** _(inline only)_
- **Inputs:** REQ-ID + signoff evidence path in `../signoffs/`
- **Output:** REQ frontmatter updated + Change Log entry
- **Inline summary:** Set status=approved, approved=today, approved_by=client name. Append Change Log. Refuse if no signoff evidence.

## Forbidden in this folder
- Do NOT mark `status: approved` without signoff evidence in `../signoffs/`
- Do NOT delete REQ files — set `status: rejected` or `status: deferred`
- Do NOT edit `## Change Log` retroactively — append only
- Do NOT modify auto-managed region of `_index.md`
- Do NOT invent acceptance criteria not derivable from source

## Escalate to human if
- Source raw-input has conflicting requirements
- Two existing REQs cover same scope — propose merge, never silently merge
- AC cannot be made specific — leave [TBD] + flag for BA
- Client signoff evidence missing for approval request

## Related operations in other folders
- Elaborate REQ into spec → `../spec/_prompts.md` OP-1
- Design implementation → `../design/_prompts.md` OP-1
- Break into tasks → `../tasks/_prompts.md` OP create-tasks-from-REQ
- Process CR against this REQ → `../change-requests/_prompts.md`
- Triage related feedback → `../feedback/_prompts.md`
