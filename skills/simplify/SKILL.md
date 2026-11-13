---
name: simplify
description: Behaviour-preserving simplification pass over recently modified code — duplicates, dead code, nesting, pass-throughs, hardcoded literals — proven by the existing checks.
disable-model-invocation: true
---

# /A.simplify — make what was just written leaner

Alias: `/A.lean`. A stage call: runs on the current feature and returns to the active stage. Also what Realign runs as its last step.

**Input:** optional — a path or a feature number to scope to; default is code modified in this feature (`## Changes`) or, outside a feature, the working diff.

1. **Scope.** List the files and symbols in scope. Read the project's checks that cover them; run them once to establish green. No green → stop and say so; simplification without a check is guesswork.
2. **Check**, per `../core/references/lean.md › Duplication and complexity check`, items 1–5, each finding cited `path:symbol`, each with the proposed cut.
3. **Report to the user in plain words first**: how many places do something that already exists, how many values are hardcoded, how much code can go with no change in behaviour. Then the list. Ask before cutting anything that touches a trust boundary, error handling or an interface others use; everything else proceeds.
4. **Cut, one at a time**, running the check after each. A cut that changes behaviour is reverted and logged as a build finding. Each cut is one event-log line.
5. **Mark** any remaining deliberate ceiling with a one-line comment (`lean.md › Marked simplifications`).
6. **Close** with lines before → after, what was consolidated into what, and what was deliberately left and why.
