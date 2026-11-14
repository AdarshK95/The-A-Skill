# Elements — the system's parts, and the history of the work done to them

The **elements registry** (`elements_registry` in config, default `docs/map/elements.md`) is the map's metadata and the project's memory of *what* was changed, as opposed to the activity files' memory of *how*. It is built incrementally — a few lines per feature — so that `/A.project.map` assembles rather than discovers, and so that "what has happened to the chat persistence" is one lookup instead of a grep.

## An element

```
## chat-persistence
Names: chat persistence · persisted chat system · chat store   ← every name the project has used; the first is current
Purpose: stores conversations and turns; the single writer of chat history
Code: agent/conversation_store.py (persist_turn, _merge_turn, update_conversation_read_at) · agent/stream_buffer.py
Interfaces: POST /chat · /chat/sync · /chat/read
Depends on: cosmos-conversations · turn-ids
Used by: chat-pipeline · frontend-chat
State: in progress
History:
- 23 Sep 26 · F2 Backend owns the turn (feature) · decisions D4, D7 · moved the writer from the browser to the backend
- 02 Nov 26 · F9 Cockpit handoff (change) · added /chat/handoff-answer writing by position
- 14 Nov 26 · F5 Chat answers under the wrong turn (fix → feature) · removed by-position merge …
```

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

## Name drift and resolution

Different sessions and different models will call the same thing by different names, and the system itself renames things. The registry handles this with the alias list, and `/A.project.map` resolves what the registry did not catch (see `../project-map/SKILL.md`): candidate elements that share code anchors, or whose functions do the same thing, are presented as one with the names merged — after the user confirms.
