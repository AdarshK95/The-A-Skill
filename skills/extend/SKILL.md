---
name: extend
description: Continue or change something already built. Finds the design or earlier activity, measures drift between it and the code, and plans the remaining work. Also serves /A.reopen.
disable-model-invocation: true
---

# /A.extend — continue what exists

**Place in the flow:** needs something already built (design, earlier feature or code) and a request; produces a report at Gate; next: Review (M+), Approve, Implement. See `../core/references/flow.md`.

Runs the core spine (`../core/SKILL.md`). This file is its **Evaluate** step. `/A.reopen <activity file>` is the same skill with the earlier activity given explicitly.

**Input:** what the user wants changed or continued, and optionally a pointer: a design document, an earlier activity file, or a feature name. With no pointer, find it: search the board (Finished and Planned), the implementation log and the activity folder for the feature's name; ask only if two candidates fit.

## Evaluate

After Read has traced the current code:

1. **Baseline.** What the earlier design, activity or decisions said would exist, and what the code actually does now. Cite both sides. Where the user says "I asked for X and got Y", this is where X and Y are both written down.
2. **Drift.** List every difference between intent and code, each marked *doc is right* (code must change), *code is right* (doc must change), or *decide* (for the user). Drift the user did not ask about is still listed; it is not fixed unless approved.
3. **The new ask.** What the user wants now, pinned the same way as in `/A.plan` (restate, `[NEEDS CLARIFICATION]` where needed). Say where it conflicts with the earlier design or a logged decision.
4. **Converge.** The remaining work = unfinished parts of the earlier plan the user still wants + drift fixes approved + the new ask, as numbered steps with done-conditions and files. Steps the earlier plan already completed are listed as done, not repeated.
5. **Reuse first.** Before any new step, the ladder: the earlier work probably already has the helper, type or pattern.
6. **Tier** from `../core/references/sizing.md`. Large drift between design and code is a signal on its own.

## Report notes

Use the `[extend]` lines of the schema. *What exists today* carries the drift list. *Assessment* says which side of each drift is right and why.

## Reopen

When continuing a Closed activity: the new activity's header gets `Continues: <that file>`; the earlier activity's `## Open items` and `## Build findings` are read and anything still open appears in the new report. The earlier file is not edited.
