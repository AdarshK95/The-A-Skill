---
name: map
description: Build or refresh a codebase map: one short contract per directory, and the first nodes of the overview diagram. For projects that existed before the workflow.
disable-model-invocation: true
---

# /A.map — map the codebase

Alias: `/A.bootstrap`. Writes to `map_folder` from config (`none` → say so and stop). Offered by `/A.init` on a non-empty repository; re-runnable.

**Input:** optional — a path to map only that subtree; `changed` to refresh only directories with files newer than their contract.

## Procedure

1. **List** the directories under the project root, skipping dependency, build and VCS folders (`node_modules`, `dist`, `.git`, virtual environments and the like). More than 40 directories → show the count and ask which top-level folders matter before continuing.
2. **Leaves first.** For each leaf directory, read its files and write `<map_folder>/<dir-path>.md` with exactly these sections, each one to three lines: **Purpose** · **Public interface** (the symbols other code imports, `path:symbol`) · **Depends on** (directories or packages) · **Invariants** (what must stay true) · **Side effects** (storage, network, cache, events). Cite; a line you cannot cite is `UNVERIFIED`.
3. **Parents next**, from the leaf contracts upward, summarizing rather than re-reading.
4. **Root**: `<map_folder>/README.md` — the architecture in one screen: the areas (from config), the main parts in each, and the dependencies between parts, each with a link to its contract.
5. **Overview**: add one node per part to the board's `## Overview`, grey, under its area's subgraph, and one edge per dependency the contracts name. Existing nodes keep their colour.
6. **Report**: directories mapped, contracts with `UNVERIFIED` lines, parts that fit no configured area (ask whether to add an area).

Read uses the map as its starting point and cites it; the reuse search (`../core/references/lean.md`) treats the contracts as the capability index — what each directory already provides — so new code is proposed only after the map says nothing does it. `/A.drift` checks the map against the code.

Contracts are short on purpose: a directory's contract should fit on one screen. Detail belongs in the code.
