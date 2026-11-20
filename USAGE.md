# Using The A Skill

You describe work; the agent investigates, reports, waits for your approval, builds exactly that, verifies it, and logs everything in your project's files. You can type commands, or just talk — auto mode picks the path.

## Projects

The skill is installed once on your machine. A folder becomes a project when you run `/A.project.start` in it; from then on everything done there is that project's memory — board, logs, decisions — and nothing else's. Start as many projects as you like, and keep them all in one workspace if you prefer — the agent works out which project a message belongs to from the files involved and says so, or asks. If two projects work together (an MCP server and the frontend that calls it), say so in each one's `.a/project.md` under `depends_on` and `provides`; `/A.project.list` shows all projects on the machine and how they connect. A project that documents no dependency is independent — that is the statement.

## The shape of a piece of work

**Area › Feature › Item › Step.** A *feature* is a board topic with its own file (numbered 7, 8, 9 …). Inside it are *items* (7.1, 7.2 …): the planned build, plus any bugfix, review or change that comes up. Each item has *steps*. The feature's header always says which step work stopped at and what the next concrete action is.

## The workflow

```
Read → Evaluate → Clarify → Report → Review → Approve → Implement → Realign → Validate → Close
```

Nothing after **Approve** happens without you. Every stage is a command if you want to call it yourself; auto advances for you and announces each move in one line.

## Day to day

**Something new**

> `/A.plan` add CSV export to the orders page

You get: what the code supports today (cited), the idea assessed plainly, alternatives including the smaller version, items and steps, impact, how it will be verified, and the decisions only you can make. Approve, change it, or stop.

**It's built but not right**

> `/A.plan.realign` the export ignores the date filter, and I asked for a download button, not a link

You get the design versus the code, every drift marked *doc is right / code is right / your call*, and the remaining work as steps.

**Something went wrong**

> `/A.rootcause` export returns an empty file when the filter has no rows

Before anything is planned: your account split into what you saw, what you expected, your own suspicions (each tested, none assumed), and what you want next (kept for later). Then the real artifacts, three passes run in parallel — backward from the error, forward from the entry, and a step back to the design — a check that nothing between them was skipped, and a test that confirms the cause. You get the cause with its confidence and condition, what was ruled out, and your suspicions each with a verdict — never a fix. Then `/A.plan` plans the fix exactly where the passes converged.

**It's built — is it really done?**

> `/A.build.review`

After the build, reviewers who never saw the conversation get your own words — what you asked and what you answered — and the code, but not the builder's description of what it did. Three passes run in parallel: from your words to the need behind them and down to the code; forward from each promised behaviour to where it actually lands; and backward from each thing you wanted protected to every way of reaching it, including code the build never touched. You get one verdict — **Sound**, **Sound once fixed**, **Shallow** (it looks finished and is not) or **Off target** — with where each rule is enforced, what was decided without asking you, and what was not examined. Each finding says whose it is — caused by this work, older but needed for what you asked, or simply older — and only the first two are fixed now; the rest go on a list for later. The review never designs the fixes: those are planned, sized and approved like any other work. Nothing is fixed until you say go.

**Reviewer comments**

> `/A.review` *(paste the comments)*

Each comment comes back as **fix** (with the change), **contest** (with the code that shows why), **defer** (with where it is tracked) or **ask you**. Say "check these and keep it for later" and the analysis parks on the board under Planned.

**Just talk**

> the export is slow for large orders

Auto says "Treating this as a bug fix" and goes. Correct it with a command if it guessed wrong.

**Inside a feature, something else comes up**

> `/A.rootcause` while in the middle of a plan

Opens item 7.n inside the current feature, runs it through the same gate, returns to where you were. If it turns out feature-sized, the agent says so and makes it its own feature.

**Keeping it lean**

Before anything new is proposed, the agent searches the codebase for something that already does it and tells you what it found and what it will reuse or extend. Values that vary go in configuration, not code. After building, it checks its own work for duplicates and hardcoding and runs a cleanup that changes no behaviour. `/A.plan.lean_overcomplication_check` runs that cleanup any time on recently modified code.

**Working in several chats at once**

Each chat works on its own feature. They coordinate through `.a/shared/`: before editing a file a session claims the parts it will touch; a session that needs another's work writes a wait and carries on with other steps; when the work lands, the waiting session picks it up and clears the entry. Nothing finished stays there — an empty folder means nothing is in flight. If a chat is cut off mid-work, the next one that opens the project reads what was left and tells you.

## The page you keep open

Open `docs/pages/index.html` in a browser. It is redrawn from the skill's own files every time the agent writes, at no token cost, so you do not have to ask the agent what happened.

- **The home page** is the one to keep open. At the top, *Your next steps*: everything waiting on you across all features, with each open question spelled out. Then *Recent activity*: what the agent did, what went wrong and what it decided without you, newest first. Then the features in progress, most recently worked on first, and links to the project's documents (board, decisions, lessons, standing rules, the map).
- **A feature's page** starts with the user summary: what you asked as the agent understood it, the steps so far with the current one marked, what went wrong, what was decided without you, and what you can test. Below it are your instructions, each marked honoured or not, and every question with its context, options and suggestion.
- **Tabs** hold the feature's other documents: reviews, the build review, the agent's detail.
- **Colours:** what is new since you last pressed *Mark as read* is green; the batch before that is light blue.
- **Red** means the agent left something out, such as a question with no context. It is told to fix those before it finishes.

The page reloads itself every 15 seconds (the *live* switch turns that off). Run `python .a/scripts/page_build.py --watch` once and it also follows every file change by itself, so it stays current even if the agent forgets to rebuild it. On an open question, *copy reply line* gives you a line to paste into the chat so the agent knows which question you are answering.

## Where things stand

| Ask | Command | You get |
| --- | --- | --- |
| Where were we? What's pending? | `/A.project.status` | Every in-progress feature with its pointer and next action, what waits on you, what is due — read from the files |
| Show me everything | `/A.project.board` | The board: Planned · In progress · Finished · Deferred · To do, per area |
| How is the project shaped? | `/A.project.map` | The overview diagram: areas, parts, connections; grey planned, blue in progress, green finished, orange deferred |
| Continue | `/A.build.resume` | Picks up at the exact step, after checking the files match what the log says was done |
| Remind me | `/A.project.board add to do: rotate the API key due 20Nov2026 10:00 AM` | Any `/A.*` command on or after that date starts by reminding you |

## Finishing

> `/A.close`

Finalizes the feature's log, writes the implementation-log entry, updates API docs if a contract changed, moves the feature to Finished, turns its overview nodes green. The project stays open. `/A.plan.realign 7` continues it later as a new feature that points back.

## How the agent talks to you

By default the agent is quiet: it speaks when you have to decide something, at a point where you might want to stop it, or to answer you. Everything else it does — checks, bookkeeping, cleanup — goes into the activity file's event log, not the chat. A long stage starts with one line and ends with one report. Want more? Set `verbosity: normal` or `verbose` in `~/.a/settings.md` (or per project in `.a/project.md`). Reports open with what the finding means for you, in plain words; file paths and code names stay in the activity file unless you ask. Every answer ends with the same block — Done / Not done / Your next step — so you can skip straight to what you have to do. If you stop it for drifting, that goes into the lessons log so it is not repeated.

## What the agent writes, and where

| Record | Where | When |
| --- | --- | --- |
| Plain-language summary for you; timed, append-only event log of every step for the agent; report, items, findings, changes, verification | The feature's activity file (month/day folder) and the month ledger | As work happens |
| Drifts and mistakes, with what to do instead | The lessons log | When you stop it, or Realign catches it |
| Decisions with reasons and rejected alternatives | The decisions log **and** the activity file | At the moment they are made |
| The board and the overview | The board file | At every phase or step change |
| Implementation log, API docs | Project files named in config | At `/A.close` |
| Constitution | — | Never by the agent. It proposes wording; you add it |

Everything is plain markdown in your repository. Any agent, any model, any session reads the same record.

## Tuning

`~/.a/settings.md` holds how the agent behaves everywhere: verbosity, when it may interrupt, whether it offers to record chat work, the highest review tier it may choose on its own, date formats. `.a/project.md` holds every path, your areas, which projects this one depends on, date and time formats, which ledgers close updates, the review floor, and project rules. `/A.project.start` writes it; edit it any time. Field reference: `.a/skills/core/references/config-schema.md`.
