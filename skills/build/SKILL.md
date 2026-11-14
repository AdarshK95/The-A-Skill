---
name: build
description: Build the approved plan — every step with the look-around before and the wiring check after, realign and simplify inside, nothing silent. /A.build.resume picks up an interrupted build at its pointer.
disable-model-invocation: true
---

# /A.build — build the approved plan

**Place in the flow:** build stage; needs `Phase: Approved`; produces built steps, changes, build findings, a realigned and verified-ready build; next: Verify. See `../core/references/flow.md`.

Runs the spine's **Implement** and **Realign** stages (`../core/SKILL.md`) on the current feature — subject resolved chat-first. Not approved → say which stage the feature is at; if the report has decisions with suggested answers, offer "take the suggested answers and approve" as one question. Realign (original ask, creep, the lean pass) and the simplify pass are part of this command, not separate ones.

## /A.build.resume — pick up an interrupted build

For a build that stopped: session cut, tab closed, planning or realigning happened in between, or the user simply came back. Before writing anything:

1. **Read the tracker**: the feature header (`Pointer`, `Last done`, `Next`), the item list with each step's status (planned / in progress / done / blocked), `## Changes`, `## Build findings` awaiting, the last five event-log lines, the shared folder (another session may hold a claim).
2. **Verify against the files**: every step marked done has its change present in the named files; every step marked in progress is checked for partial edits (read the file; `git status` / `git diff` where available). Mismatches are reported before anything else — the tracker is corrected to what the files show, not the other way round.
3. **Re-read the ask and the approved steps**; if the plan was realigned since the build started, name what changed and which steps it affects.
4. **Announce** in one block: feature › item › step; done since last report; mismatches found; next concrete action; anything awaiting the user.
5. **Continue** at the pointer under the same rules as `/A.build`. Never start a step the pointer does not name; never redo a step whose change is verified present.

`/A.build` with no interruption does the same tracker read silently; `/A.build.resume` does it visibly and stops on any mismatch.
