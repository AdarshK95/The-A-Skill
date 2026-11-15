# Elements — the system's parts, and the history of the work done to them

The **elements registry** (`elements_registry` in config, default `docs/map/elements.md`) is the map's metadata and the project's memory of *what* was changed, as opposed to the activity files' memory of *how*. It is built incrementally — a few lines per feature — so that `/A.project.map` assembles rather than discovers, and so that "what has happened to the chat persistence" is one lookup instead of a grep.

## Structure: layers, containment, flows

A dependency graph shows what calls what; a project's true form is its **containers** — the deployable units (a frontend plugin, a proxy, the backend app, the external systems it talks to) — with their parts inside, arranged in the order a request travels, and the **kind of connection** written on each line. Two fields and a section:

- **Containers are elements.** The top of the registry is the deployable units themselves (`medha-plugin`, `backstage-proxy`, `medha-backend`, `cosmos`, `foundry`, …), each an element with its own anchors; every other element has `Part of:` up to one of them. The map draws a container as a box with its parts inside; a container inside a container is a box inside a box.
- **The connection type is a label on the relation**, never a grouping: `Depends on: chat-store (Cosmos: conversations) · agent-pipeline (call: _run_generation) · live-feed (SSE: /chat/resume)` — type, colon, name, in parentheses after the element id. The map writes it on the line.

- **`Part of:`** — the element this one is a part of. The test: an element that **runs, hosts or wholly contains** another is its parent (a pipeline and the sub-agents it runs; an answer step and the retrieval inside it); a caller is not a parent, and a module shared by two elements belongs to neither's parts. The map draws a parent as one card with a count and expands it on click.
- **`## Flows`** — a section at the top of the registry, after the header and before the first element: named sequences of elements in the order they run when something happens — *chat turn*, *Cockpit turn*, *approval*, *feedback to diagnosis* — one numbered line per step: `1. <element-id> · <what happens here, few words>`, then `Sources: F<n> …`. A flow is how the system actually behaves; the map lights it up step by step.

The former `Layer:` field is retired: a technology type is not a place in the system, and grouping by it hides the structure. The map ignores it where it still appears.

```
## Flows

### chat-turn · a user sends a message and gets an answer
1. chat-renderer · the browser posts /chat with the turn id
2. chat-reception · stamps the record, opens the turn
3. agent-pipeline · plans and runs the agents
4. knowledge-answer-step · answers from what was retrieved
5. scout-v2-retrieval · searches the tiers
6. chat-store · saves the turn
7. live-feed · streams the records to the browser
Sources: F5 root cause (14 Nov 26) · F6 plan

### chat-turn (fragment, F15) · after step 4
4a. scout-v2-retrieval · start-up index check runs first
Sources: F15 plan
```

A step whose element does not exist yet, or whose behaviour is designed but not built, carries **`(planned)`** in its note: flows will always mix what runs and what is planned, because every plan traces a path before it is built, and the map dims those steps so a reader sees what runs today.

A **fragment** is a partial path a pass learned — a few steps of a flow, or a new branch — written under the flow's name with `(fragment, F<n>)`; the map merges fragments into the flow by element order. No pass has to know the whole flow to contribute to it.

## Every pass leaves a drop

Any command that reads the code learns structure, and writes it down where it already writes: a plan's Read, a root cause's lanes (their chains *are* flows), a review lens's spot-checks, the build check's look-around (callers and consumers *are* relations), a coverage pass. At that command's write point, the agent appends to the registry — claiming the file as `shared.md` says — whatever it saw that the registry lacks: a code anchor on an element; a `Part of:` or `Layer:` it is now sure of; a relation the code showed; a flow fragment from the path it walked, under the flow's name. Two or three lines, never a rewrite, never a question to the user. The map consolidates them: merges fragments, resolves duplicates, redraws. One pass alone draws nothing; twenty passes draw the project.

## An element

```
## chat-persistence
Names: chat persistence · persisted chat system · chat store   ← every name the project has used; the first is current
Part of: medha-backend
Purpose: stores conversations and turns; the single writer of chat history
Code: agent/conversation_store.py (persist_turn, _merge_turn, update_conversation_read_at) · agent/stream_buffer.py
Interfaces: POST /chat · /chat/sync · /chat/read
Depends on: cosmos-conversations · turn-ids
Used by: chat-pipeline · frontend-chat
State: in change
History:
- 23 Sep 26 · F2 Backend owns the turn (feature) · decisions D4, D7 · moved the writer from the browser to the backend
- 02 Nov 26 · F9 Cockpit handoff (change) · added /chat/handoff-answer writing by position
- 14 Nov 26 · F5 Chat answers under the wrong turn (fix → feature) · removed by-position merge …
```

`State:` is one bare word from the list below; anything to say about it goes on a separate `Note:` line. History lines name the feature as `F<n>` so the thread and the map can count it. Any `###` heading ends the element: owner notes belong above the first element or under their own `##` heading that is not an element id.

The id (`chat-persistence`) is stable and never renamed. **Names** is the alias list; a rename adds a name, it does not create an element. **Code** anchors the element to functions and files, which is what lets name drift be detected later. **History** is append-only, one line per feature or item that touched it, with the type and the decisions.

Elements are parts of the system at the level a solution architect would draw: a store, a pipeline, an adapter, an API surface, a frontend module. Not a function, not a file, not a feature.

## Write points

| When | What |
| --- | --- |
| **Report** — every plan, every type | `### Elements touched`: existing element ids, or `new: <proposed id> — <one-line purpose>`; for each, what this work changes about it. Five lines, never skipped; an empty section fails the self-check |
| **Decision** | Names the elements it concerns, so a decision is findable from the part it shaped |
| **Close** | Appends one history line to each touched element: date · feature number and title · type (with promotion if any) · decisions · one-line result. Creates proposed new elements |
| **Start** | When the request names or touches an element, its entry — purpose, code, history — goes into `## Context`. The lineage is read, not rediscovered |
| **`/A.project.drift`** | Checks each element's `Code` still exists and still does what `Purpose` says; flags elements whose functions moved or were renamed |

## Area

Each element carries `Area: <one of the project's areas>`; the map groups by it. When absent, the map takes the area of the first feature that touched the element.

## States

`stable` (in service, no feature touching it) · `in change` (a feature on the board touches it now) · `planned` (does not exist yet) · `unwired` (kept in the repository, nothing calls it) · `untouched` (mapped from the code by a coverage pass; no feature has touched it yet — it becomes `stable` or `in change` on its own when a feature's report names it) · `superseded` (replaced; kept for history). Close sets them; the map colours them.

## Name drift and resolution

Different sessions and different models will call the same thing by different names, and the system itself renames things. The registry handles this with the alias list, and `/A.project.map` resolves what the registry did not catch (see `../project-map/SKILL.md`): candidate elements that share code anchors, or whose functions do the same thing, are presented as one with the names merged — after the user confirms.
