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

## 3. Pull the thread — `/A.project.map <element | feature | decision>`

Given an element: its purpose, names, code, and its **history in order** — every feature and item that touched it, with types (and promotions), decisions, and one-line results, each linked to its file; then the elements it depends on and that depend on it, one line each. Given a feature: the elements it touched and their histories around that date. Given a decision: the elements it concerned and what happened to them after. This is the answer to "how did we get here" without a keyword search.

## 4. Report

Plain words first: how many elements, how many resolved as the same, what relations were added, what is still ambiguous. Then the diagram. Decisions (merges, relations) in decision shape. `Done / Not done / Your next step`.
