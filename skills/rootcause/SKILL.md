---
name: rootcause
description: Find why something went wrong, before anything is planned. Understand the user's account, observe the real artifacts, run reverse, forward and zoom-out passes in parallel, check coverage for gaps, reconcile, confirm by test. Output is a cause with confidence — never a fix.
disable-model-invocation: true
---

# /A.rootcause — find the cause first

**Place in the flow:** its own stage, before plan. Needs a reported wrong behaviour; produces a root-cause report at CONFIRMED or LIKELY, or an honest "not found" with what would find it; next: `/A.plan` from the report. See `../core/references/flow.md`.

Runs the spine (`../core/SKILL.md`) with `../core/references/rootcause.md` as its method. Subject resolved chat-first (Start step 0). `/A.rootcause.m`, `.l`, `.xl` force the depth; plain `/A.rootcause` chooses from the signals and escalates when a shallower pass does not close.

## Evaluate (this skill's part of the spine)

1. **Understand and compartmentalize** the account into symptom · expectation · the user's insights · what they want next (`rootcause.md › 1`). Write the four boxes into the report before touching code.
2. **Observe**: collect the real artifacts, reproduce where possible (`› 2`). No reproduction → say what prevents it; the report cannot reach CONFIRMED without one.
3. **Lanes in parallel**: reverse, forward, zoom-out, each blind to the others, each to an origin, each with a coverage statement (`› 3`). Fresh subagents at M and above; at S, run them yourself in sequence, writing each before the next.
4. **Coverage check**: the path map; gaps along the path, lateral, vertical; targeted passes until no unexamined segment could carry the error (`› 4`).
5. **Reconcile**: root-cause candidates, cascade chains, contributing, ruled out, the user's insights with verdicts (`› 5`).
6. **Confirm**: a prediction and a test per surviving candidate; CONFIRMED / LIKELY / demoted / not found (`› 6`). XL: a fresh critic on the confirmed cause.
7. **Report** (`› 7`), in the report schema with these sections in place of *Proposed change*: **Cause** (with condition and chain) · **Contributing** · **Ruled out** · **Your insights** (verdict each) · **Coverage map** · **Confirmation test** · **Not the cause** (what a fix must not be aimed at). Elements touched as usual. `### Decisions needed` only when the user must choose between confirmation tests the agent cannot run.

## Gate

The stage ends in one of two ways: a cause at CONFIRMED or LIKELY, handed to `/A.plan` ("plan the fix at <origin>"); or "not found", with the coverage map and the evidence that would find it. A HYPOTHESIS never passes to planning. The user's wished-for fix (box 4) is given to the plan stage with the report, labelled as the user's wish, so the plan can say whether it addresses the cause.
