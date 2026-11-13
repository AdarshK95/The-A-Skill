# Logging — where state lives and when it is written

The project's files are the memory: they outlive this session, this model and this agent. Writes happen at the moment of the event, never deferred to the end of a conversation. Nothing is read twice that was already summarized. Dates and times inside documents use `date_format` and `time_format` from config (defaults `13 Nov 26`, `04:40 PM`); file and folder names use `filename_date_format` so they sort.

**Two rules above all others.** Every document has two readers: the user, who gets plain language, and the agent, who gets full technical precision — never mixed. And the record is **append-only and timed**: nothing is deleted or rewritten to look cleaner; a correction is a new, timestamped line that points back to the line it corrects.

| Record | Scope | Written when | Read by |
|---|---|---|---|
| **Project board** | Every activity (planned, in progress, finished), deferred items, to-dos, overview diagram | Every phase or step change; `/A.board` | Any session starting or resuming; the user asking what is going on |
| **Activity file** | One piece of work | Continuously | The session doing the work; `/A.resume` |
| **Decisions log** | Whole project, append-only | At the moment a choice is made | Start of every activity (search), `/A.review` |
| **Implementation log, API docs, ledger** | Whole project | `/A.close` only | People, and agents mapping the system |
| **Constitution** | Whole project | Never by an agent; proposed wording only | Start of every activity |
| **Lessons log** | Whole project, append-only | When the user stops a drift; when Realign finds one | Start of every activity, with the constitution |
| **Month ledger** | One month of features | At feature creation and every status change | The user, scanning a month |
| **Shared folder** | Live claims, handoffs, notes between sessions | Before edits, on waits and completions; rows removed when acted on | Every session at Start, every stage move, every step |

## Project board

One file (`project_board` in config), created by `/A.start-project` from `templates/board.md`. Grouped by **Area**. Features are blocks; their items are rows under the block.

| Section | Holds | Moves |
|---|---|---|
| **In progress** | Features with an item being built, with every item listed (done, in progress, planned) | In from Planned on the first build step; out to Finished at `/A.close` |
| **Planned** | Features whose items are not yet building: in Start, Read, Evaluate, Clarify, Gate or Review, or parked by the user. Items listed | Added at Start |
| **Finished** | Closed features, one row each | Added at `/A.close`; never removed |
| **Deferred** | Parts set aside: reason and revisit date | From a DECLINE, a deferred build finding, or the user via `/A.board` |
| **To do** | The user's own items with due date and time | Via `/A.board`; removed when done or turned into a feature |
| **Overview** | Mermaid `flowchart`: one subgraph per area, one node per feature or part, classed `planned` / `inprogress` / `finished` / `deferred` | Recoloured by the feature that touches it |

Shape of a feature block:

```
### 7 · CSV export · plan · Implement · pointer 7.2 › 3/5 · updated 13 Nov 26, 05:40 PM · 2026-11/2026-11-13/01-csv-export.md
| # | Item | Type | Phase | Step | Status | Next |
| --- | --- | --- | --- | --- | --- | --- |
| 7.1 | Export endpoint | build | Closed | 4/4 | done | — |
| 7.2 | Null range on empty filter | bugfix | Implement | 3/5 | in progress | wire route in api/index.ts |
| 7.3 | Review #42 comments | review | Planned | — | waiting on user | pick fixes |
```

Rules: a session edits only its own feature's block; re-read the board immediately before writing; rewrite the block, not the file. The feature file's header is the source of truth; the board is its index. Feature numbers are sequential across the board and never reused. When `reminders` is on, every `/A.*` command begins by naming, in one line, any To do or Deferred item due today or overdue.

State questions are answered from these files, never from the conversation: `/A.status` reads the board and each in-progress header and reports every feature's pointer and next action; `/A.board` shows the file plus a three-line summary; `/A.tracker` shows the overview after checking its colours; `/A.resume` continues at a pointer.

The overview is a map of parts and what depends on what, not a list of tasks. Work inside a feature (items, steps, findings) never becomes a node; a promoted item does.

## Activity file

One per feature, at the path `activity_naming` gives (month folder, day folder, zero-padded sequence per day, slug naming the work). Created at Start: the status header, then the body from the project's template or `templates/activity-template.md`. Sections and who they are for:

| Section | Reader | Rule |
| --- | --- | --- |
| `## Summary (plain language)` | User | Five points: the ask, the situation, what was decided and why, what was done, the result. No paths, no symbols. Kept current; the result line always reflects now. Written so it could become a work item on its own |
| `## Context` | Agent | Once at Start: binding rules, lessons, bearing decisions |
| `## Report` | Both — chat summary for the user, full text for the agent | A revision is appended under a dated heading; earlier reports stay |
| `## Items` · `## Findings` · `## Decisions` · `## Build findings` · `## Realign` · `## Verification` · `## Open items` | Agent | Current state of each; entries are added, never removed |
| `## Changes` | Agent | Quick reference: one line per file touched, pulled from the event log |
| `## Links` | Both | Work item(s) under `tracker_label`; related features (continues / superseded by); central docs touched |
| `## Event log` | Agent | **The backbone.** One line per step, `E<n> · <date>, <time> — …`, in the order it happened: the ask quoted, every file opened and what it showed, every command and output, every dead end and why, every change with path · symbol · line · before → after · reason, every doc updated, every validation and result. Nothing skipped. A correction is `E<m> … corrects E<n>`; a stopped drift is tagged `DRIFT` |

Time is the ordering: the time the event happened, not the time it was written. If the exact minute is unknown, use the best available and keep it increasing. A later line never edits an earlier one; it supersedes it by reference, so a reader can see what was believed at E12 and why E20 overturned it.

## Month ledger

`ledger_pattern` names it (default one `_ledger.md` per month folder). One row per feature file, added at creation, status edited in place as it changes; rows never reordered or removed:

```
| Date | # | Feature file | <tracker_label> | Summary (plain English) | Status |
| 13 Nov 26 | 7 | 2026-11/2026-11-13/01-csv-export.md | AB#1234 | Orders can be exported as CSV | In progress |
```

The Summary column is the feature file's title, in the user's words, so a month reads as a story without opening a file.

## Write points — batch the writing, not the recording

Recording and writing are different things. Every event is **recorded** when it happens — its timestamp, what was done, what was seen — so the order and times in the log are true. The file is **written** at boundaries, in one consolidated pass, not after every tool call; thirty single-line edits to the activity file during one stage is wasted motion and clutter. Write when:

- a **step** completes (its event lines, its `## Changes` lines, the pointer);
- a **decision** is made — immediately and alone, because its loss costs the most (dual write);
- a **finding** is logged as blocking — immediately;
- a **stage** changes;
- **before asking the user** anything, and **before any long-running action** (a reviewer run, a build, a migration);
- **before the turn ends**, always: a session can end at any moment and a resuming session reads the file, not your memory.

Between write points, hold the recorded events and write them together. The event log keeps the original timestamps, so a batch written at 05:40 still reads `E12 · 05:14 PM`, `E13 · 05:19 PM`, … in order. What is never deferred: decisions, blocking findings, the header's `Pointer` / `Next` when a turn is about to end.

## Decisions — dual write

A decision is any choice a later reader would otherwise re-derive: an architecture option, a scope cut, a constitution override, a contested finding the user upheld, a mid-build fork, a build finding's handling. At the moment it is made, in one step:

1. Append to the decisions log:

   ```
   ## 13 Nov 26, 04:40 PM — <one-line decision>
   Context: <the situation, one or two sentences>
   Decision: <what was chosen>
   Reasons: <why>
   Rejected: <alternatives and why not>
   Activity: <activity file>
   ```

2. Add the entry, or a one-line pointer to it, under `## Decisions` in the activity file.

The log is append-only; a reversal is a new entry naming the one it reverses.

## `/A.close`

Closes the **activity**, not the project. In the order `close_updates` gives:

- `implementation_log` — one entry: date, title, type, tier, one-paragraph summary, link to the activity file.
- `api_docs` — only when `## Changes` touched a contract.
- `ledger` — when `ledger_pattern` is set, index the activity in the current period.
- Constitution — propose exact wording for any standing rule the activity surfaced; the user adds it.

Then `Phase: Closed` in the header, the feature block replaced by one row under Finished with a one-line result, and the overview nodes this feature finished recoloured green. `/A.reopen` later starts a new activity with `Continues:` pointing here.

## Drift and lessons

When the user stops the agent for drifting, over-building or leaving scope, or Realign finds it: an event-log line tagged `DRIFT` (what happened, what was wanted), and an entry in `lessons_log` (date · what happened · instead · activity). Start reads the lessons log; a lesson that applies to the current work is quoted in `## Context`.

## Token discipline

Read the constitution and decisions once per activity and summarize into `## Context`. Read the board, not other activities' files. On resume read the header and `## Context`, then only the sections the current step needs. The always-on block in the host instruction file carries pointers only; it tells no session to read anything on every turn.
