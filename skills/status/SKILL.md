---
name: status
description: Where are we, what is pending, what is next — answered from the project files, never from memory.
disable-model-invocation: true
---

# /A.status — where are we

Also what any plain-language question about state means: "where were we", "what's pending", "what did we do", "what's next".

1. Read the shared folder: anything in flight between sessions (claims, waits, notes) is reported first, in plain words, with who waits on whom. Then read the board. Reminders next, one line, if due.
2. For every feature under **In progress**: read its file's header. Report one line each: `7 · CSV export (API) › 7.2 › 3/5 — next: <Next> — awaiting you: <count or none>`.
3. For **Planned**: one line each with `Waiting on`.
4. **Finished** since the last `/A.status` call recorded in the board's `## Log`, if any: one line each. Then append a dated line to that log: `status given`.
5. **Deferred** with a revisit date within seven days, and **To do** due within seven days: one line each.
6. If this workspace has `.a/mirror/MIRROR` and its commit differs from `~/.a/SOURCE`, say the mirror is behind and that `/A.skill-update` refreshes it.
7. If the board's `## Log` shows no `/A.drift` run within `drift.cadence_days`, say "drift check overdue" in one line.
8. End with the single most useful next action across everything, as the files state it.

Every line comes from a file read in this call. Nothing comes from the conversation. If a header and its board block disagree, the header wins; say so and fix the block.
