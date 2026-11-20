---
name: build
description: Build the approved plan — every step with the look-around before and the wiring check after, realign and simplify inside, nothing silent. /A.build.resume picks up an interrupted build at its pointer.
disable-model-invocation: true
---

# /A.build — build the approved plan

**Place in the flow:** build stage; needs `Phase: Approved`; produces built steps, changes, build findings, a realigned build; next: the build review (`/A.build.review`; tier M and above), then Verify. See `../core/references/flow.md`.

Runs the spine's **Implement** and **Realign** stages (`../core/SKILL.md`) on the current feature — subject resolved chat-first. Not approved → say which stage the feature is at; if the report has decisions with suggested answers, offer "take the suggested answers and approve" as one question. Realign is part of this command, not a separate one, and it always ends with the two mandatory checks on the build — the scope check (drift, what nobody asked for, whose each finding is) and the lean check (duplication, the simplify pass) — each saying its result in one line, clean or not.

## Order and builders

The approved plan gives every item a `Needs:` line. That line, never the item number, decides the order.

- **Ready** means every item it needs is done **and that item's check has passed**. Only a ready item is started. A waiting item is not started at all: no builder exists for it, so nothing is assumed or built ahead on its behalf.
- **At the same time** only for ready items that touch no file in common (their steps' file lists, plus anything the look-around adds). A shared file means one after the other.
- **Builders.** A feature with one item is built by this session. With several, each ready item goes to a fresh builder where the host has fresh agents (`../core/references/hosts.md`; unlike a reviewer, a builder may edit and run commands), so each starts with a clean context; this session orchestrates. No fresh agents on this host → this session builds the items one by one in `Needs:` order.
- **A builder's brief** is the item's section of the plan, `## Instructions`, `## Clarifications`, `## Context`, and the paths of `build-check.md` and `shared.md` to read first — never the conversation. It ends: build only this item; claim each file before editing it; if something this item needs is missing or is not as the plan describes, stop and report it — never build it, stub it or assume it.
- **Done is decided here.** When a builder reports, this session reads the diff, runs the item's check itself, and only then marks the item done, releases its claims and starts what became ready. A builder's "done" is a claim.
- **A failed or stopped item** holds back only the items that need it; the others continue. Its report goes to `## Build findings`.

The feature's `Pointer` names the earliest unfinished item; each running item keeps its own.

## /A.build.resume — pick up an interrupted build

For a build that stopped: session cut, tab closed, planning or realigning happened in between, or the user simply came back. Before writing anything:

1. **Read the tracker**: the report first (header (`Pointer`, `Last done`, `Next`), the item list with each step's status (planned / in progress / done / blocked), `## Changes`, `## Build findings` awaiting), then from the detail only what the report points at and the last five event-log lines; the shared folder (another session may hold a claim).
2. **Verify against the files**: every step marked done has its change present in the named files; every step marked in progress is checked for partial edits (read the file; `git status` / `git diff` where available). Mismatches are reported before anything else — the tracker is corrected to what the files show, not the other way round.
3. **Re-read the ask and the approved steps**; if the plan was realigned since the build started, name what changed and which steps it affects.
4. **Announce** in one block: feature › item › step; done since last report; mismatches found; next concrete action; anything awaiting the user.
5. **Continue** at the pointer under the same rules as `/A.build`. Never start a step the pointer does not name; never redo a step whose change is verified present.

`/A.build` with no interruption does the same tracker read silently; `/A.build.resume` does it visibly and stops on any mismatch.
