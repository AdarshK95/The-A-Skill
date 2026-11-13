---
name: board
description: Show the project board, or add to it in plain language.
disable-model-invocation: true
---

# /A.board — the project board

**No input:** show the board file as it stands, then a three-line summary: counts per section by area; what is waiting on the user; what is due within seven days.

**With input**, in plain language:

- "add to do: <item> due <date> [<time>]" → row under **To do** with `Added` now. A date in any format is written in the project's `date_format`.
- "defer <item or 7.n> until <date>: <reason>" → row under **Deferred**, with `From` the feature or item; the item's header gets `Phase: Deferred` and the overview node turns orange.
- "done <to do item>" → remove the row.
- "promote 7.n" → the item becomes a feature (spine → Promotion).
- "move <feature> to <area>" → change its Area and its overview subgraph.

Re-read the board immediately before writing. Write only the rows asked for. Confirm in one line what changed.
