---
id: PROMPT-02
name: Refine acceptance criteria
version: 0.1.0
status: active
last_updated: 2026-05-26
used_by:
  - requirements/_prompts.md OP-2
---

# Prompt: Refine acceptance criteria for a REQ

## Purpose
Rewrite vague or untestable ACs into Given/When/Then form. Flag any AC that cannot be made testable from the source.

## Inputs
- REQ-ID
- (Optional) raw-input source for re-reading

## Output
- Updated REQ file `## Acceptance Criteria` section
- Change Log appended

## Prompt body
```
You are refining the acceptance criteria of REQ-NNN.

Read the REQ file. For each AC in the `## Acceptance Criteria` section:

1. Rewrite in Given/When/Then form:
   - Given <observable starting state>, when <specific action>, then <observable outcome>.

2. Verify each AC is:
   - Observable (a tester can see the outcome)
   - Specific (no "appropriate", "reasonable", "fast" — quantify)
   - Singular (one assertion per AC; split compound ACs)

3. If an AC cannot be made specific from the source, leave it as:
   - `- [TBD] Cannot determine <X> from source — escalate to BA.`
   DO NOT invent specifics.

4. If you add quantification (e.g., "fast" → "≤300ms p95"), cite the source for that
   number. If no source, leave `[TBD: confirm threshold with stakeholder]`.

5. Append to ## Change Log:
   - <today>: Refined AC (was vague — rewrote in Given/When/Then form).

Report: list of ACs refined + count of [TBD] items remaining.
```

## Guardrails
- Never invent thresholds (latency, retries, concurrency limits) without source
- Never collapse multiple assertions into one AC
- Never edit any section other than `## Acceptance Criteria` and `## Change Log`
