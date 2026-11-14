---
name: plan-bugfix
description: Something is broken. Trace the symptom to its origin, name the root cause, propose the fix at the root, and analyze what the fix itself could break — before fixing.
disable-model-invocation: true
---

# /A.plan.bugfix — something is broken

**Place in the flow:** needs a described failure; produces a trace, root cause and a fix report at Gate; next: Review (if shared callers or contracts), Approve, Implement. See `../core/references/flow.md`.

Runs the core spine (`../core/SKILL.md`). This file is its **Evaluate** step.

**Input:** the bug as the user saw it: what happened, what was expected, where, and any error text. Missing pieces are asked for in one line each; a reproduction path is worth asking for.

## Evaluate

After Read has traced the code around the symptom:

1. **Reproduce or model.** Reproduce the bug if the project has a way to run it; otherwise write the exact sequence of calls and state that produces it, cited. A bug you cannot reproduce or model is reported as such, with what would be needed.
2. **Trace.** From the symptom back to the origin, one hop at a time: `path:symbol` → `path:symbol` → … Each hop says what the value or state is at that point and why it is wrong there. Stop at the place where correct input becomes wrong output. That is the origin.
3. **Root cause, one sentence.** Then one sentence on why this and not the nearer symptom. If the origin is a design decision rather than a slip, say so and cite the decision if one is logged.
4. **Callers.** List every caller of the function or path you will change, from the code. The fix lives where all of them pass through. A fix on only the reported path leaves the siblings broken; say so if the user asks for that anyway, and log it as a decision.
5. **Fix.** The smallest change that removes the cause. The ladder applies: a guard already present elsewhere, a stdlib behaviour, one line.
6. **Fix impact.** What the fix changes for each caller; what stored data, cache or concurrent path now behaves differently; whether the fix removes the cause or moves it. A fix that could serve a wrong result to a path that was previously correct is a Blocker until addressed.
7. **Steps.** Usually one or two; each with a done-condition. The last step is the check that fails if the bug returns.
8. **Tier** from `../core/references/sizing.md`. Shared callers, a contract change, or a cache/permission/timestamp/ordering path each move the tier up.

## Report notes

Use the `[bugfix]` lines of the schema. *What exists today* holds the trace; *Assessment* holds the root cause; *Impact* holds the fix impact. *After the change* is included when the bug was user-visible.

## Related findings

Other bugs noticed while tracing go under `## Build findings` with a proposed handling (fix here only if on the same path; otherwise a new `/A.plan.bugfix` activity, added to the board as Planned), and are surfaced at the gate. They are not fixed as a side effect.
