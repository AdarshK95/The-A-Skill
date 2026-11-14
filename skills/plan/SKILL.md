---
name: plan
description: Design and build something new. The user describes an idea; you evaluate it against the code, report, wait for approval, then build.
disable-model-invocation: true
---

# /A.plan — something new

**Place in the flow:** needs a request and a project; produces a report at Gate; next: Review (M+), then Approve, then Implement. See `../core/references/flow.md`.

Runs the core spine (`../core/SKILL.md`). This file is its **Evaluate** step.

**Input:** the user's idea, in their words. Everything after the command is the request. If there is nothing after it, ask for the idea in one line.

**From a root-cause report:** when the subject (chat-first) is a `/A.rootcause` report at CONFIRMED or LIKELY, this is a **fix plan**: the ask is the user's expectation box; the change goes where the lanes converged (the origin), never at a cascade link, never at the symptom; the report's *Not the cause* section is a constraint on the plan; the user's wished-for fix is evaluated against the cause and kept, adapted, or set aside with the reason. The fix carries a check that fails if the cause returns. A report at HYPOTHESIS is sent back to `/A.rootcause`, not planned.

## Evaluate

After Read has traced the code the idea touches:

1. **Pin the ask.** Restate the idea as an outcome the user would recognize. Where it is ambiguous, raise `[NEEDS CLARIFICATION: ...]` — at most five, each answerable in a line. The Clarify stage asks them before the report is final; design nothing on top of an open one that changes the design.
2. **Fit.** For each part of the idea: already supported (cite), supported with a change (cite what changes), or new. Say which parts the constitution or a logged decision bears on.
3. **Alternatives.** Name at least one way to reach the outcome other than the obvious one, including the "do less" version from the ladder. A plan with one path and no rejected alternative is not ready.
4. **Shape.** Choose nothing on the user's behalf that is an architecture, data-shape or scope decision; present those as options with trade-offs. Decide everything else yourself and say so.
5. **Steps.** Break the proposed change into numbered steps, each one unit of work with a done-condition, in the order the code requires. Each step names the files it touches.
6. **Impact and verification** per the report schema.
7. **Tier** from `../core/references/sizing.md`. A new subsystem or a new design document is XL.

## Report notes

Use the schema as written; no type markers apply. *What exists today* is the baseline a stranger would need; *Assessment* says plainly whether the idea is sound and what it costs.

## On approval

Hand back to the spine at Gate. The approved report is the design document for this activity; if the project keeps design documents elsewhere (`docs_root`), copy the *Proposed change* and *Impact* sections there at Close and link both ways.
