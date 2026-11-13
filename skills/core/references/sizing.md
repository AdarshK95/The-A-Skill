# Sizing — how much review a piece of work gets

The tier is computed at the end of Evaluate from what Reading found, not from how the request was phrased. A one-line bug report that touches a function with twelve callers is not small.

## Signals

Start at **S**. Each signal that applies moves the tier up one step; stop at **XL**.

| Signal | Why it raises the tier |
|---|---|
| A function or module you will change has callers outside the file you are editing | A fix in one caller's path can leave siblings broken |
| A contract changes: API shape, payload, schema, stored format, event name | Consumers you cannot see depend on it |
| The change touches cache, permission, authentication, timestamp or ordering logic | These produce stale or wrong results silently |
| The change touches concurrency: multiple tabs, users, workers or retries acting on the same state | Races do not show in a single-path test |
| The plan contradicts, extends or reinterprets an entry in the decisions log | The earlier reason must be weighed, not overwritten |
| More than one module or layer changes in the same activity | Cross-module effects are where plans drift |
| New subsystem, new design document, or an extend activity where drift between doc and code is large | The design itself needs fresh eyes before detail |

The user may set the tier directly at the gate; record `Tier: M (user override, rubric said S)`.

`project.md` → `review.default_floor` raises the starting point for the whole project.

## What each tier runs

| Tier | Review | Who |
|---|---|---|
| **S** | None. Implement with the ladder; leave one runnable check | — |
| **M** | `implementation-readiness` + `impact` + `lean` lenses on the report | Fresh reviewers, or cold self-review |
| **L** | `zoom-out` first; then `critic` + `implementation-readiness` + `impact` + `lean` | Rounds until two consecutive clean (`goldfish-lenses.md › Rounds`); reviewers within a round may run in parallel |
| **XL** | `zoom-out` → `comprehension` → `critic` → `zoom-out` (additions only) → `implementation-readiness` + `codebase-details` + `impact` + `lean` — or the EGM review when `review.xl_engine: egm` (`hosts.md`) | Five sequential stages with a gate after each; rounds per `goldfish-lenses.md` |

Lens prompts are in `goldfish-lenses.md`. Findings are handled with `resolve-protocol.md`.

## Writing the tier

In the status header: `Tier: L (signals: shared callers in api/handlers.ts, contract change on /v2/items, contradicts decision 2026-03-14 "version-based invalidation")`. The signals are what the user checks, so name the file or decision for each.
