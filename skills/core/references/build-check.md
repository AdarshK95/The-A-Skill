# Build check — the senior engineer's reflex during Implement

A step is not "edit the file the plan names". It is: understand what the change sits inside, make the change, prove the whole still works, and ask whether it still serves the ask. This is the review's lenses applied cheaply, by the implementer, to the code around each step — no subagents, no ceremony — so gaps are caught while building rather than after. Everything found goes to `## Build findings`; the user is interrupted only when a finding changes the plan.

## The scope wall

Before any edit: is the file inside `code_scope`? If not, stop — the step is a question to the user, not an edit. This applies to tests, docs inside code trees, generated copies and "small" fixes alike. A finding about a file out of scope is one line in the build findings ("out of scope: <path>, noted for its owner") and nothing else.

## Absence is a failure, not a value

Where a step is supposed to produce something — a model's reply, a parsed structure, a search result, a response from a service, a file — the plan names **what a valid output looks like** (a schema, a required set of fields, a non-empty result, a status) and **what happens when it is not there**. Empty, malformed or missing output is a failure state with a name that reaches the user or the log (`judge failed: no JSON in reply`), never a default that reads like a conclusion (`nothing answers`, `unknown`, `none found`, `[]`). A function that returns an empty collection where it should have returned a failure hides the failure; a parser that returns `{}` on garbage lies. The build check asks at every step that consumes an output: *if this came back empty, would we know?* If the answer is no, the step is not done.

## Before editing a symbol

Look around it, every time, however small the step:

1. **Callers and consumers.** Search the whole repository (tests, scripts, other packages, frontends) for every use of the function, type, route, table or config key you will change. The plan's list is a starting point, not the truth. A caller the plan did not name is a build finding before any edit.
2. **Contract.** What does it accept and return, what does it store, who reads what it writes, what does it log? If the change alters any of that, every consumer in step 1 is checked against the new shape.
3. **Siblings.** Code that does the same job elsewhere (the reuse search again, scoped to this step): if a sibling exists, the fix goes where both route through, or the plan was wrong.
4. **Tests and fixtures** that mention the symbol by name — monkeypatches, mocks, snapshots. They are consumers too.
5. **Config and environment.** Flags, settings, feature switches, environment differences (dev vs prod containers, TTLs, permissions) the symbol depends on.

**Telemetry names are claimed.** A new or renamed telemetry event name added in a step is claimed by an element's `Events:` line in the same step; when no element fits, the build says so in its finding rather than leaving the name to show up as unmapped later.

**Leave a drop.** The callers, consumers and siblings found in 1–5 are relations; the files touched are anchors. At the step's write point, append to the registry what it lacks (a `Depends on` / `Used by`, a `Code:` anchor, a `Part of:` now evident) — two lines, no question (`elements.md › Every pass leaves a drop`).

## After editing

6. **Wire it end to end.** Follow the path from where the request enters to where the result leaves, through the change. Does the new piece connect to the old pieces — is it called, does its output reach what needs it, is the dead old path removed?
7. **Run the nearest check**, and when the step touched a contract, the consumers' checks too. No check exists → leave the smallest one that fails if this breaks.
8. **Reground** (`lean.md › Reground`): scope — does what now exists serve the original request, or a neighbour of it; did this step add anything the plan did not name? Lean — is this the least structure that is still robust? Premise — has what I learned building this changed why we are doing it? Silent when yes; one line and the full check when not.
9. **Quality.** Is this the robust version or a quick fix? If a quick fix crept in, say so in the build finding with its ceiling, don't bury it.

## Failure handling is part of the step, not an afterthought

Every step enumerates how it can fail before it is built, and each failure is handled in the code — never swallowed, never left to surface as a stack trace or a silent fallback:

- **Preconditions** checked up front with a clear error: a container or table that must exist, a setting that must be present, a service that must answer. "Agent-feedback could not be saved: the `agent_feedback` store does not exist in this environment (prod). Create it or disable the feature." — not a generic 500.
- **Every error message has two layers**, in this order: **plain English** — what happened, which step or component, and what the reader can do — then the **technical detail** (the exception, the code, the identifiers) for whoever debugs it. A connection refused, a quota error, a timeout read the same across many steps; the plain-English line is what tells the reader *which* step and *why it matters here*.
- **Failure cases are enumerated per step** in the plan's step text and in the verification: what happens on bad input, missing dependency, timeout, partial write, duplicate, permission denied, empty result. A step whose failure cases are not written down is not ready to build.
- **Parallel or best-effort paths** (a second write that must not fail the first) still report their failure: log it with the plain-English line and raise a visible signal (metric, flag, event) — "best-effort" never means "silent".
- **Verification covers the failure paths**, not only the happy path: at least one check per enumerated failure that shows the message a user would see.

## What you do with what you find

| Found | Do |
|---|---|
| A caller or consumer the plan missed, fully handleable in this step | Handle it; one build finding line, marked *decided*; one event-log line |
| A gap that changes a later step | Build finding, *awaiting*; continue with unaffected steps; surface at the next gate |
| A gap that invalidates the plan, or a trust-boundary / data-loss issue | Stop. Build finding, *blocking*; tell the user now (one of the few allowed interrupts) |
| A quick fix where a robust one is feasible | Build it robust if within the step; otherwise build finding with the ceiling and the robust alternative |
| Something out of scope but real (a pre-existing bug nearby) | Build finding, *new item/feature proposed*; never fixed as a side effect |

## Per item, before marking it done

The item's steps are done when, taken together, they pass the lens questions the implementer can answer alone: every modified symbol's callers accounted for (impact); the plan's description of the code matched what was there (codebase-details); nothing duplicated or hardcoded was added (lean); the plan could have been built by someone else from its text — anything you had to decide on your own is now written into the plan (readiness). Two minutes, not a review round. Then `Result:` is filled.
