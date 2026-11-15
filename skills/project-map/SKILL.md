---
name: project-map
description: The visual map of the system — its elements, how they connect, and the state of each — assembled from the elements registry after resolving name drift and duplicates against the code. Also pulls the thread: everything that happened to one element, in order.
disable-model-invocation: true
---

# /A.project.map — the map, and the thread

**Place in the flow:** project stage; independent; reads the elements registry, the board and the code; writes the overview diagram and, on the user's yes, consolidations into the registry. See `../core/references/flow.md`.

The map is **assembled**, not discovered. Its inputs are the elements registry (`elements.md`), the board, and the code the elements anchor to. It never draws every mentioned name as a node; it draws elements, after making sure they are really distinct.

## 1. Resolve before drawing

Name drift is expected: "chat system", "persisted chat system", "chat manager" may be one element with three names, or three elements. Decide from the code, not from the words:

1. **Collect candidates**: every element in the registry, plus names used in reports' `Elements touched`, decisions and the board that are not yet registered.
2. **Anchor each to code**: the functions and files its `Code` line names, or — for an unregistered name — the files the feature that used the name actually changed.
3. **Compare anchors.** Two candidates whose anchors overlap, or whose functions do the same thing (same inputs, outputs and side effects, read from the code — a renamed function is still the same function), are **the same element**: propose a merge with the names combined under one id. Anchors that are disjoint but connected are **distinct elements with a relation**; decide the relation from the code: *sequential* (one calls or feeds the other), *parallel* (both called by a third), *alternative* (one replaces the other — the older gets `State: superseded`), *part of* (one inside the other → the inner becomes a sub-element or is folded in).
4. **Present conflicts** to the user in decision shape before any merge: what two names, what the code shows, suggested resolution. No conflict → proceed silently.
5. **Write the resolution** into the registry on yes: merged names, relations, states. A rename becomes an alias, never a second element.

## 2. Assemble

One node per element inside its area's subgraph; one edge per `Depends on` / `Used by` relation (direction from the code); colour from `State` (grey planned · blue in progress · green finished · orange deferred · dimmed superseded). Board features appear only through the elements they touch — the map shows the system, the board shows the work. Write the mermaid block into the board's `## Overview`; keep it a map of parts, not tasks.

Where the registry is thin (a new project, or an area no feature has touched), read the code to propose elements for that area — the per-directory contracts (`map_folder`) are the source — and ask before adding them. Never add elements from imports alone.

## 2b. The interactive map

The Mermaid in the board is the lean, always-readable view: elements, relations, state, nothing else. Under it, one pointer line:

> Interactive map: `python .a/scripts/map_build.py` → `docs/map/map.html` (click an element to pull its thread).

The script (`templates/map/map_build.py`, copied to `.a/scripts/` by `/A.project.start`, or on the map's first run when missing) reads the **same sources** — the registry, the board, the decisions and deferred-decisions logs — and writes one self-contained HTML file: elements grouped by area and coloured by state, edges for *depends on*, a badge per element with its feature, decision and relation counts, search and filters, and a side panel that pulls the thread: purpose, names, code anchors, relations, every feature that touched it in order with links to their files, every decision that names it. No network, no dependencies, standard-library Python. It never reads the Mermaid; both views come from the registry, so they cannot disagree.

Whenever the overview is regenerated (by the map or by Close), the agent asks once in one line — "Overview updated. Regenerate `docs/map/map.html` too?" — and runs the script on yes; the user may also run it directly. The HTML is a build output: ignored by git unless the user says otherwise.

## 3. Pull the thread — `/A.project.map <element | feature | decision>`

Given an element: its purpose, names, code, and its **history in order** — every feature and item that touched it, with types (and promotions), decisions, and one-line results, each linked to its file; then the elements it depends on and that depend on it, one line each. Given a feature: the elements it touched and their histories around that date. Given a decision: the elements it concerned and what happened to them after. This is the answer to "how did we get here" without a keyword search.

## What the map does on its own, and what it asks

The registry is derived from the code and from the features' reports; most of its upkeep is fact, not judgement. The map **does without asking**: correct a code anchor or path that moved (the code is the truth); move an anchor to the element that owns it; register an element that a feature's `### Elements touched` already named (that report was approved); add relations the code shows; mark an element *unwired* when nothing calls it; redraw the overview from the registry (features never appear as nodes — they appear through the elements they touch). Each is one line in the report.

The map **asks, in decision shape**, only for judgement: merging two names into one element (an alias); drawing or moving an element boundary (splitting a package between two elements); registering parts no feature has touched — done as `untouched` elements when the user asks for full coverage ("leave nothing stray"), otherwise offered in one line; marking an element *superseded*. Two or three questions is normal on a first run; none on a routine one.

**States** (one per element, from the registry and the board): `stable` — in service, no feature touching it; `in change` — a feature on the board touches it now; `planned` — does not exist yet; `unwired` — kept in the repository, nothing calls it; `untouched` — registered from the code by a coverage pass so that no module is stray, no feature has touched it yet; it falls into line on its own when one does. The overview colours these; "finished" is a feature's state, not an element's.

**First run on an existing project** is a seeding pass: it reads the registry, every report's `### Elements touched`, the board and the code, proposes the registry it would write, and asks the judgement questions once. **After that, Close redraws the overview and appends element history itself**, so the map stays current without being run; `/A.project.map` is for pulling a thread, resolving drift the registry has accumulated, or when the user wants to look.

## 4. Report

Plain words first: how many elements, how many resolved as the same, what relations were added, what is still ambiguous. Then the diagram. Decisions (merges, relations) in decision shape. `Done / Not done / Your next step`.
