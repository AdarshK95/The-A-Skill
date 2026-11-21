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

## 1b. Consolidate the drops

Before drawing, fold what the passes left: merge fragments into their flows by element order (a fragment whose steps all appear in the flow in the same order adds nothing; one with a new element inserts it where its neighbours sit; a conflict — two fragments ordering the same elements differently — is a question in decision shape); dedupe anchors; make sure every element has a `Part of:` chain up to a container (a deployable unit: the frontend plugin, the proxy, the backend app, each external system) — propose the containers from the deployment (what is built, deployed or called as one unit) and the parents from the code (what runs, hosts or wholly contains what); label relations with their connection type and name where the code shows it (`(API: /chat)`, `(SSE: /chat/resume)`, `(Cosmos: conversations)`, `(call: run_generation)`, `(MCP: commvault)`). Report what was merged and filled in one line each; ask only on conflicts.

**The flow pass** (first run, or when the user asks "map the flows"): read-only, like the coverage pass — from the routes, the pipeline and the sub-agents, propose the containers, the main flows as ordered element lists (a chat turn, a Cockpit turn, an approval, feedback to diagnosis, ingestion, a routine), one line per step, and the parent of each element. The user confirms once. After that the flows grow from the drops every pass leaves.

## 1c. The observed layer

If `docs/map/observed.jsonl` exists (the contract in `elements.md › Observed`), the build adds telemetry to the map: turns, errors and median duration per element, traffic per relation, observed paths with their share of turns beside the declared flows, and the unmapped-events list. Setting it up in a project is the project's work, handed to the build: an exporter that writes the contract from the project's own telemetry store (read-only, no text, no identities, output git-ignored), and an `Events:` proposal for every element from the project's event-name registry, confirmed by the user; event names that fit no element are proposed as new elements or as external systems. After that, refreshing the file is one command, and the observed layer is a validation of the registry every time: an unmapped name is a gap, an element with patterns and no traffic is a question.

## 2. Assemble

Containers as subgraphs, parts inside them in flow order, one edge per `Depends on` relation labelled with its connection type and name where known; colour from `State`. In the Mermaid, nested parents are drawn as their card alone unless the user asks for the detailed view. Board features appear only through the elements they touch — the map shows the system, the board shows the work. Write the mermaid block into the board's `## Overview`; keep it a map of parts, not tasks.

Where the registry is thin (a new project, or an area no feature has touched), read the code to propose elements for that area — the per-directory contracts (`map_folder`) are the source — and ask before adding them. Never add elements from imports alone.

## 2b. The interactive map

The Mermaid in the board is the lean, always-readable view: elements, relations, state, nothing else. Under it, one pointer line:

> Interactive map: `python <method>/templates/map/map_build.py --root <project>` → `docs/map/map.html` (click an element to pull its thread).

The script (`<method>/templates/map/map_build.py`, run from the install with `--root <project>`; never copied into the project) reads the **same sources** — the registry, the board, the decisions and deferred-decisions logs — and writes one self-contained HTML file: the containers as boxes left to right in the order a request travels, their parts inside in flow order, nested containers as boxes inside boxes (top level open, inner ones collapsed to a card with "+N parts" until clicked); edges for *depends on* with the connection type and name written on the line when an element or a flow is selected; a **flow selector** that lights a flow's path with numbered steps and dims the rest; a badge per element with its feature, decision and relation counts; search and filters; and a side panel that pulls the thread: purpose, names, code anchors, relations, every feature that touched it in order with links to their files, every decision that names it. No network, no dependencies, standard-library Python. It never reads the Mermaid; both views come from the registry, so they cannot disagree.

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
