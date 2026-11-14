---
name: drift
description: Find where the project's documents and the code have diverged, and where the decisions log has gone stale. Run weekly.
disable-model-invocation: true
---

# /A.project.drift — documents, decisions and map versus code

**Place in the flow:** independent; produces a drift report; next: features for the drifts the user picks. See `../core/references/flow.md`.

**Input:** optional — a document path or a feature number to check only that.

1. **Collect** the documents the config names: constitution, decisions log, API docs, the codebase map, the activity files of Finished features (their *Proposed change* and *Impact*), and the board's overview.
2. **Check each claim** a document makes about the code against the code: a file or symbol named exists; a described behaviour, shape or contract matches; a dependency drawn in the overview exists in the code. Use the method in `../core/references/tracing.md` at claim level — open, don't assume.
3. **Report**, one table, grouped by document:

   | Document | Claim (`path:line` in the doc) | Code says (`path:symbol`) | Verdict |
   | --- | --- | --- | --- |

   Verdict is *doc is right* (code must change), *code is right* (doc must change), or *your call*. Nothing is changed in this command.
4. **Decisions hygiene**: list decisions whose cited files no longer exist; decisions contradicted by a later one with no reversal entry; decisions older than a year that no current code references. Each with a proposed action (mark superseded, add a reversal, keep).
4a. **Elements**: for each entry in the elements registry, check its `Code` anchors exist and the functions still do what `Purpose` says; flag moved or renamed anchors and elements whose code no longer matches their description. Never delete; propose the correction.
4b. **Artifacts**: for each row in the artifacts ledger, compare its *Valid for* (model version, package version, deployment, date) with the current environment; mark stale rows and say what changed. Never delete.
5. **Ceilings and duplicates**: list every marked simplification (`lean.md › Marked simplifications`) with its ceiling, and run the duplication check (`lean.md`, items 1–3) across the whole codebase rather than one feature; report both as tables with proposed actions.
6. **Record** the run as a dated line in the board's `## Log`. `/A.project.status` says drift is overdue when the last run is older than `drift.cadence_days`.
7. **Offer** the follow-ups as features or items: each *code is right* → an extend item to update the doc; each *doc is right* → a bugfix or extend item; each *your call* → a decision to make. The user picks; nothing is created unasked.
