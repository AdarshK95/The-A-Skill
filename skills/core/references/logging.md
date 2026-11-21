# Logging — where state lives and when it is written

The project's files are the memory: they outlive this session, this model and this agent. Writes happen at the moment of the event, never deferred to the end of a conversation. Nothing is read twice that was already summarized. Dates and times inside documents use `date_format` and `time_format` from config (defaults `13 Nov 26`, `04:40 PM`); file and folder names use `filename_date_format` so they sort.

**Two rules above all others.** Every document has two readers: the user, who gets plain language, and the agent, who gets full technical precision — never mixed. And the record is **append-only and timed**: nothing is deleted or rewritten to look cleaner; a correction is a new, timestamped line that points back to the line it corrects.

| Record | Scope | Written when | Read by |
|---|---|---|---|
| **Project board** | Every activity (planned, in progress, finished), deferred items, to-dos, overview diagram | Every phase or step change; `/A.project.board` | Any session starting or resuming; the user asking what is going on |
| **Activity file** | One piece of work | Continuously | The session doing the work; `/A.build.resume` |
| **Decisions log** | Whole project, append-only | At the moment a choice is made | Start of every activity (search), `/A.review` |
| **Implementation log, API docs, ledger** | Whole project | `/A.close` only | People, and agents mapping the system |
| **Constitution** | Whole project | Never by an agent; proposed wording only | Start of every activity |
| **Lessons log** | Whole project, append-only | When the user stops a drift; when Realign finds one | Start of every activity, with the constitution |
| **Elements registry** | Whole project | Report names elements touched; Close appends history; Decision names elements | Start, for the parts a request touches; `/A.project.map` |
| **Artifacts + ledger** | Whole project | At Validate/Close when work produced measured, reusable facts; on request | Start of work in the same area; `/A.project.drift` for staleness |
| **Deferred-decisions log** | Whole project, append-only | A finding or design question the user defers, with why and the condition that reopens it | Start of work touching the same area |
| **Month ledger** | One month of features | At feature creation and every status change | The user, scanning a month |
| **Shared folder** | Live claims, handoffs, notes between sessions | Before edits, on waits and completions; rows removed when acted on | Every session at Start, every stage move, every step |

## Project board

One file (`project_board` in config), created by `/A.project.start` from `templates/board.md`. Grouped by **Area**. Features are blocks; their items are rows under the block.

| Section | Holds | Moves |
|---|---|---|
| **In progress** | Features with an item being built, with every item listed (done, in progress, planned) | In from Planned on the first build step; out to Finished at `/A.close` |
| **Planned** | Features whose items are not yet building: in Start, Read, Evaluate, Clarify, Gate or Review, or parked by the user. Items listed | Added at Start |
| **Finished** | Closed features, one row each | Added at `/A.close`; never removed |
| **Deferred** | Parts set aside: reason and revisit date | From a DECLINE, a deferred build finding, or the user via `/A.project.board` |
| **To do** | The user's own items with due date and time | Via `/A.project.board`; removed when done or turned into a feature |
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

State questions are answered from these files, never from the conversation: `/A.project.status` reads the board and each in-progress header and reports every feature's pointer and next action; `/A.project.board` shows the file plus a three-line summary; `/A.project.map` shows the overview after checking its colours; `/A.build.resume` continues at a pointer.

The overview is a map of parts and what depends on what, not a list of tasks. Work inside a feature (items, steps, findings) never becomes a node; a promoted item does.

## Activity file

**One folder per feature, and every file carries the feature's number** (`activity_naming`, default `{feature}-{slug}/{feature}-{slug}.md`):

| File in `<activity_folder>/<n>-<slug>/` | Holds |
| --- | --- |
| `<n>-<slug>.md` | The main file: user summary, instructions, questions and answers, the plan, small items as sections |
| `<n>.<m>-<type>-<slug>.md` | One file per item that produces its own document — a build review, a root-cause report, a fix item, a triage of reviewer comments — `m` being the item number (`7.2-build-review-…`) |
| `<n>-<slug>.detail.md` | The agent's record: event log, transcripts, tables |

Nothing about a feature lives outside its folder, and no file is created without its number, so a person can find everything for feature 11 in one place and the page shows each file as a tab. An agent reads the file or the section it needs, never the folder. Projects that keep dated folders keep working: the pages group files by their `Feature:` header.

Created at Start: the folder, the main file with its status header and the body from the project's template or `templates/activity-template.md`. Sections and who they are for:

| Section | Reader | Rule |
| --- | --- | --- |
| `## User summary` | User | First in the file. Six fixed lines (what this is, the ask as understood, now, running, next, waiting on you) and the dated trails below them (`communication.md › The user summary`). Plain words; kept current at every write point |
| `## Instructions` · `## Clarifications` | Both | Second and third. The user's instructions in their words; every question, and every choice made for the user, as a block (`clarify.md › The block`). The standard every stage and every reviewer checks against |
| `## Context` | Agent | Once at Start: binding rules, lessons, bearing decisions |
| `## Report` | Both — chat summary for the user, full text for the agent | A revision is appended under a dated heading; earlier reports stay |
| `## Items` · `## Findings` · `## Decisions` · `## Build findings` · `## Realign` · `## Verification` · `## Open items` | Agent | Current state of each; entries are added, never removed |
| `## Changes` | Agent | Quick reference: one line per file touched, pulled from the event log |
| `## Links` | Both | Work item(s) under `tracker_label`; related features (continues / superseded by); central docs touched |
| `## Event log` | Agent | **The backbone.** One line per step, `E<n> · <date>, <time> — …`, in the order it happened: the ask quoted, every file opened and what it showed, every command and output, every dead end and why, every change with path · symbol · line · before → after · reason, every doc updated, every validation and result. Nothing skipped. A correction is `E<m> … corrects E<n>`; a stopped drift is tagged `DRIFT` |

Time is the ordering: the time the event happened, not the time it was written. If the exact minute is unknown, use the best available and keep it increasing. A later line never edits an earlier one; it supersedes it by reference, so a reader can see what was believed at E12 and why E20 overturned it.

## The pages — what the user opens

`<method>/templates/pages/page_build.py` (the A Skill's page script, run from the install with `--root <project>` and never copied into the project; `<method>` is the folder that holds `skills/` and `templates/`, `~/.a` on a global install; standard-library Python, no network, no model tokens) draws `<pages_folder>/index.html` and one page per feature from these files. The markdown stays the source and stays what agents read; the pages are only a view of it.

- **The home page** (`index.html`) is the one the user keeps open while the agent works, and it answers four questions without anyone being asked: *what do I need to do* — **Your next steps**, everything waiting on the user across all features, each open question by its text; *what just happened* — **Recent activity**, the dated lines of every feature's trails, newest first, problems and choices made alone marked as such; *what is in progress* — **Ongoing**, most recently worked on first, each with now, running and next; *where is the rest* — **Project documents** (board, decisions, deferred decisions, lessons, standing rules, the map), and finished features folded below. It reloads itself every 15 seconds unless the user switches *live* off.
- **Feature page:** the user summary on top with the step trail; each instruction with whether it is honoured; each question as a card, open ones first, with a line to copy into the chat so the answer names its question; one tab per file of the feature; agent sections folded.
- **What changed:** anything new since the user last pressed *Mark as read* is green, the batch before that light blue. The browser remembers it; the agent writes nothing for it.
- **Format problems** are shown on the page in red and printed by the script, so the page is also the check that the fixed shape was followed.

**The live server** (`page_build.py --serve`, standard-library Python, started hidden — no window — and reachable at a fixed address per project, `http://localhost:87xx/index.html`, printed by the command). Opened through it, the page follows the agent by itself, a **Resync** button rebuilds in the background and says *Syncing…* then *Synced 11:42*, and the build's format warnings still reach the agent. Opened as a plain file, the page reloads every 15 seconds and the button is disabled with a note. The server listens on this machine only, refuses requests from other web pages and other host names, and can do exactly two things: rebuild, and stop itself (`--stop`).

**Who starts it, and when.** The skill detects Python first (`python --version`, then `py -3 --version`). Missing → no page server is offered or mentioned and documentation is written exactly as before; the page can still be built wherever Python later appears. Present → `pages_server` decides (`.a/project.md` if it sets it, else `~/.a/settings.md`; default `session`): `off` → started only by `/A.show`; `session` → also at the first write of each session (`--serve` is safe to repeat: it says *already running*); `login` → also at Windows login, through the startup entry `/A.project.repair` installs (`--install-startup`; `--remove-startup` undoes it). Nobody is asked: the setting is the answer, and the page's **Help** section says how to change it. `/A.show` always starts it and opens the browser. `--watch` remains for a user who prefers a terminal.

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
- the **user gives an instruction** — appended to `## Instructions` at once, in their words;
- the **user answers a question** — the question and the answer appended to `## Clarifications` at once, in their words;
- a **finding** is logged as blocking — immediately;
- a **stage** changes;
- **before asking the user** anything, and **before any long-running action** (a reviewer run, a build, a migration);
- **before the turn ends**, always: a session can end at any moment and a resuming session reads the file, not your memory.

At every write point the user summary is brought up to date first, and after the write `python <method>/templates/pages/page_build.py --root <project>` rebuilds the pages. Whatever it prints as `WARN` — a question with no context, a summary with no next step — is fixed before the turn ends.

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
   Elements: <element ids this concerns>
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

Then `Phase: Closed` in the header, the feature block replaced by one row under Finished with a one-line result, and the overview nodes this feature finished recoloured green. `/A.plan.realign` later starts a new activity with `Continues:` pointing here.

## Drift and lessons

When the user stops the agent for drifting, over-building or leaving scope, when Realign finds it, or when a build review finds a decision taken silently: an event-log line tagged `DRIFT` (what happened, what was wanted), at once. What it becomes after that is decided by the **lesson ladder** — the cheapest thing that stops it happening again, first rung that holds:

1. **Nothing.** It would not recur, or the code now makes the right way obvious. The `DRIFT` line says so.
2. **A check.** A test, a lint rule or an assert that goes red if it recurs — proposed to the user as a step, and trusted only once it has been seen to fail.
3. **A standing rule.** Proposed wording for the constitution or the project's `rules`; the user adds it.
4. **A lesson.** An entry in `lessons_log`: date · what happened · instead · activity · **retire when** — the condition under which it stops being needed (the check exists, the rule is in the constitution, the module is gone).

A written lesson is the last rung because every lesson is read at every Start: a log that only grows buries the lessons that matter. Start reads the lessons **in force**, checks each one's retire condition against the project as it is now, and marks one whose condition has arrived `retired <date> — <why>` (the entry stays; the log is append-only). An entry with no retire condition is in force. A lesson that applies to the current work is quoted in `## Context`. Close asks the ladder's question once per feature: did this work correct a wrong belief about how the system behaves — and if so, which rung holds it?

## Token discipline

Read the constitution and decisions once per activity and summarize into `## Context`. Read the board, not other activities' files. On resume read the header and `## Context`, then only the sections the current step needs. The always-on block in the host instruction file carries pointers only; it tells no session to read anything on every turn.
