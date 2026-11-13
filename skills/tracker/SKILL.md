---
name: tracker
description: Show the project overview diagram — areas, parts, connections, state by colour — after checking it against the board.
disable-model-invocation: true
---

# /A.tracker — project overview

Aliases: `/A.flow`, `/A.overview`.

1. Read the board. For every feature: Finished → its node is `finished` (green); In progress → `inprogress` (blue); Planned → `planned` (grey); Deferred → `deferred` (orange). A node whose colour disagrees with the board is corrected; say what was fixed.
2. A feature on the board with no node → add it under its area's subgraph, grey or blue as its section says, and ask the user in one line what it connects to if the activity file does not say.
3. Show the `## Overview` mermaid block. One sentence under it: how many parts per area, how many in each state.
4. With input ("connect X to Y", "X belongs to area Z", "rename X") → edit the diagram accordingly and show it again.

The diagram is a map of parts and dependencies. Steps, findings and items never become nodes; a promoted item does.
