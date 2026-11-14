# Hierarchy — Project › Area › Feature › Item › Step, with Elements

Work is organized so that its size, its place in the system and its history are always visible.

| Level | What | Lives in |
| --- | --- | --- |
| Project | One folder with `.a/project.md` | — |
| Area | A section of the project (`areas` in config) | board grouping, map subgraph |
| **Feature** | A board topic with its own activity file. Types: `feature` (something new), `change` (what exists, altered), `fix` (a standalone bug — assigned only after `/A.rootcause` has named the cause; a wrong behaviour with an unknown cause is a root-cause investigation, not yet a fix) | activity file, board block, map node |
| **Item** | A piece of work inside a feature: `build`, `change`, `fix`, `review` | section in the feature's file, row under its block |
| Step | One unit of work with a done-condition | the item's step list |
| **Element** | A named part of the *system* — a component, service, store, pipeline, adapter — that work is done *to*. Not work | `elements_registry` (`elements.md`) |

Features and items are **work**; elements are **what the work touches**. Every report names the elements it touches; every element keeps the history of the work that touched it. That is how a thread is pulled later.

## Type follows scope, and scope is measured

A feature's type is not what the user called it at the start; it is what the sizing signals say it is now (`sizing.md`). The rule, applied at **Evaluate** and again at **Realign** and by `/A.plan.scope_check_drift_check`:

| Signals found | Type |
| --- | --- |
| One element, no contract change, one step or two, callers all local | `fix` (standalone) or an item of an existing feature |
| One element, a few steps, no new subsystem | `change` |
| More than one element, or a contract change, or a new subsystem, or its own item list | `feature` |

**Promotion** — a `fix` or `change` that turns out feature-sized: say so to the user in decision shape ("this started as a bug fix; it now redesigns the chat write path across three elements — promoting to a feature, your word"); on yes, change `Type` in the header, move the board block to the right place, add `Promoted from: <type>, <date>, <reason>` to the header and a decision entry. The file and number stay. **Demotion** — a feature that collapsed to one step: becomes an item of the feature that owns that element (or a standalone `fix`), with `Demoted from` recorded, the original file kept and marked.

Never silently. A type change is a decision, and the reason is the signals, named with their files.

## Elements

See `elements.md` for the registry, the `Elements touched` section every report carries, and how `/A.project.map` resolves name drift before drawing.
