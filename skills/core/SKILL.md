---
name: core
description: The shared spine every /A.* command runs on. Loaded by path; never run on its own.
disable-model-invocation: true
---

# Core spine

You are the engineer. The user is the architect. You investigate, propose and build; the user decides. Nothing is built until approved, and what is built matches what was approved. Keep every artifact plain and short.

Work is organized in a hierarchy and a workflow:

**Hierarchy — Area › Feature › Item › Step.** An *area* is a section of the project (`areas` in config). A *feature* is a board topic with its own activity file and overview node, numbered sequentially (`7`). An *item* is a piece of work inside a feature, numbered `7.1, 7.2 …`, of type *build* (the planned work), *bugfix*, *review* or *change*; it lives as a section in the feature's file. A *step* is one unit of work inside an item with a done-condition. The feature's report defines its items up front (a small feature is one build item); items that emerge later get the next number. Every item runs the full workflow below and stops at the same gate.

**Entry types** decide *how the work is evaluated*: `plan` (new), `extend` (continue or change what exists; also `reopen`), `bugfix` (broken), `review` (comments from an outside reviewer). Each has a skill folder beside this one and supplies the **Evaluate** stage only. At feature level the type is plan or extend; a bugfix or review asked for on its own becomes an item of the feature it belongs to, or a new feature when it belongs to none.

**Stages** are the workflow every feature and item moves through. Each is a command; in auto mode (`../auto/SKILL.md`) you advance through them yourself and say so at each move.

## The workflow

```
Start → Read → Evaluate → Clarify → Report → Review → Approve → Implement → Realign → Validate → Close
                                      └─────── Gate: nothing past here without the user ───────┘
```

| Stage | Command | Done when |
|---|---|---|
| Start | (entry type) | Config read; reminders given; constitution and matching decisions summarized into `## Context`; board row under Planned |
| Read | — | What exists and what the request touches, paraphrased, every claim cited `path:symbol` |
| Evaluate | (entry type) | The type's questions answered; tier chosen with signals (`references/sizing.md`) |
| Clarify | `/A.clarify` | Every `[NEEDS CLARIFICATION]` resolved or explicitly parked; at most five questions, one at a time |
| Report | — | `## Report` written (`references/report-schema.md`) with numbered steps; chat summary given |
| Review | `/A.review` | The tier's lenses run (`references/goldfish-lenses.md`); findings resolved (`references/resolve-protocol.md`) |
| Approve | — | The user has said go. Decisions dual-written. `Phase: Approved` |
| Implement | `/A.implement` (`/A.build`) | Each step built in order; counter and board current; build findings logged |
| Realign | `/A.realign` | Build checked against the original ask; creep removed; duplication and hardcoding found and removed; simplify pass run (`/A.simplify` on demand) |
| Validate | `/A.validate` (`/A.verify`, `/A.test`) | A runnable check passes; build matches the approved steps, with evidence |
| Close | `/A.close` (`/A.done`, `/A.finish`) | Activity finalized; project ledgers updated; board row to Finished; overview recoloured |

Stages run in this order. Clarify and Review may also be called at any time on the current artifact ("clarify this", "review this") and return to the stage that was active. Realign runs on its own whenever the user changes direction. Nothing after Approve runs without the user's go.

## Start

1. Read `.a/project.md`. Missing → tell the user to run `/A.init`; stop. Set this session's tag (`references/shared.md › Session identity`).
2. Read the shared folder (`shared_folder`). Non-empty → report in plain words what is in flight, who waits on whom, and whether any of it is this session's to resume, before anything else. Then open the project board (`project_board`). `reminders: on` → say in one line any To do or Deferred item due today or overdue. A Planned or In-progress row matching the request → offer `/A.resume`. Name any In-progress row touching the same files.
3. Read the constitution and the lessons log whole; search the decisions log for the request's terms and read the matches. Write `## Context` in the activity file: binding rules, lessons that apply, bearing decisions, references. Read once per activity; a resumed session reads `## Context`, not the sources.
4. New feature: take the next feature number from the board, create the activity file at the path `activity_naming` gives (month and day folders on demand; status header, then the body from `activity_template` or `templates/activity-template.md`; `E1` is the user's ask, quoted), add its row to the month ledger, add its block under **Planned** in its **Area** (`areas` in config; ask once if none fits), and add its overview node, grey, inside the area's subgraph. New item in an existing feature: add `### 7.n · <title> (<type>)` under `## Items` in the feature's file with its mini header, and a row under the feature's block on the board.

## Read

Follow `references/tracing.md`: fill the trace table, the caller inventory and the boundary list for the code the request touches. Read is done when all three are complete; not before. Where the project has a codebase map (`map_folder`), start from it and cite it. **Evidence rule:** every statement about the code cites `path:symbol` or `path:line`, or is labelled `UNVERIFIED`.

## Evaluate

Run the entry type's Evaluate. Apply the ladder to anything proposed: needed at all → already here → stdlib → platform → installed dependency → one line → minimum code. End with the tier and its signals in the header.

## Clarify

Scan the ask against the seven categories in `references/clarify.md`; add markers where a category is relevant and unanswered. Ask at most five, one at a time, most consequential first; the rest become **Assumptions** in the report. The user may park one (`parked: <reason>`). Answers that are choices go under `## Decisions`. For L and XL, write `## Requirements` as checkable lines. Design nothing on top of an open clarification that would change the design.

## Report

Write `## Report`. For a feature, *Proposed change* lists the **items** (`7.1 … 7.n`, each a deliverable piece with its type) and, under each, its numbered **steps** — one unit of work each, with files and a done-condition. For a single item, just its steps. Options for the user carry trade-offs, and one line on which way you lean and why; your assessment of the request is stated plainly. Run `references/self-check.md` and fix what fails. Fill the `## Summary (plain language)` points 1–3. Then the chat version per `references/communication.md`: what this means for the user, what was found in plain words, what they must decide, what happens next — paths and symbols stay in the file. Set `Phase: Gate`, `Pointer: 7.1 › 0/N`.

## Review

Per tier. Spawn reviewers as `references/hosts.md` says for this host; run the isolation probe once per project per host first. Without fresh reviewers, follow the cold self-review protocol in `hosts.md` step by step, one lens at a time, labelled. A lens that fails is `not run`. Resolve every finding; L and XL run rounds until two consecutive clean rounds (`goldfish-lenses.md › Rounds`). XL uses `review.xl_engine`. A material change revises the report and stays at Gate. Tier S: `Review: none (tier S)`. The same lenses answer "review this" at any stage, on whatever artifact is current. External reviewer comments are the `review` entry type, not this stage. When the user wants to share findings with a colleague, write the findings-and-verdicts list from `## Findings` as a standalone block they can paste.

## Approve

Wait for an explicit go. One question at a time. Each decision → dual write (`references/logging.md`). Changed plan → revised report. Stopped → `Phase: Stopped` with reason. With `approval.second_reviewer: on`, the user's go sets `Phase: Approved (pending second reviewer)`; a named person's go, logged as a decision, completes it. Otherwise on go: `Phase: Approved`.

## Implement

Before each step, re-read the shared folder; before each file edit, claim it (`references/shared.md › Claims`); release the claim when the step's check passes. A step that needs another session's work writes a handoff and continues with unblocked steps or waits.

First step → feature block to **In progress**, overview nodes blue. Items in order, steps in order. Per step: `Pointer: 7.2 › 3/5 — <name> — in progress` in the header and the board; build; `## Changes` one line per file prefixed with the item number; `Last done:` updated; `done`. Build only what the approved steps say.

Posture from `implement.posture` (default `full`): `full` enforces the ladder; `lite` builds as planned and names the lazier alternative in one line; `ultra` ships the smallest version and questions the rest in the same breath.

- Fix at the root: where several callers share a function, the fix lives where they all pass.
- Reuse before writing: the *Reuse candidates* decisions are followed; a new need discovered mid-build gets its own reuse search before new code. No abstraction, config or scaffolding the plan does not name; nothing varying hardcoded; dependencies accepted, not created.
- Never simplified away: trust-boundary validation, error handling that prevents data loss or a silent wrong answer, security, accessibility, anything explicitly asked for (`lean.md › When not to be lean`).
- A deliberate simplification carries a one-line comment naming its ceiling and upgrade path.
- An unanticipated fork → stop, log under `## Decisions` as pending, ask.

**Build findings.** Anything discovered while building — a bug, an inconsistency, a surprise — goes under `## Build findings` as found: what · where (cited) · effect on this work · proposed handling (fix in this step / new item / new feature / leave). Blocking → ask now. Otherwise surfaced at Realign. Nothing fixed silently, nothing dropped silently.

## Realign

After the last step, and at once when the user changes direction, stops you for drifting, or a finding changes the plan. A stop for drift is logged `DRIFT` in the event log and as a lesson (`references/communication.md › Drift and scope`). Under `## Realign`, dated: Does what exists solve the original ask or a neighbour? What exists that no approved step names — delete or get approved? What does the ladder remove from what was built? Which build findings await the user? Then run the **duplication and complexity check** and the **simplify pass** from `references/lean.md` over what this feature added or changed. Apply simplifications that need no decision; the rest go to the user. A material change returns to Approve.

## Validate

Evidence before claims. Run the project checks covering the change; where none exists, leave the smallest runnable check that fails if the logic breaks. Record command and result under `## Verification`. Diff the build against the approved steps: each present, nothing extra. Tick every line of `## Requirements` with its evidence; an unticked one is a Blocker. `Phase: Verified`; tell the user it is ready to close or continue.

## Close

Only on the user's word. The feature has no rows left in the shared folder (release or resolve them first). Finalize the file: Summary points 4–5 current, `## Changes` complete, `## Links` filled, the Done / Not done / Your next step block as the Summary's last lines. Run `close_updates` (`references/logging.md`); ledger status; `Phase: Closed`; board row to **Finished** with a one-line result; overview nodes green. Closing ends the activity, not the project; `/A.reopen` continues it later with `Continues:`.

## Items

A different kind of work needed inside the current feature — a quick bug that unblocks the build, a review of one piece, a small change — is a new **item**: `### 7.n · <title> (<type>)` under `## Items`, with its mini header (`Phase · Pointer · Last done · Next · Result`), the type's Evaluate at item scope, its own steps, the same stages and the same gate. When it finishes, `Result:` is filled and the feature's pointer returns to the item that was active before. The board lists the item under the feature; the overview does not change.

**Promotion.** When an item or a build finding turns out feature-sized — a new component, a new integration, a change users will notice on its own, work that needs its own item list — it becomes its own **feature**: next number, own file, own board block in its area, own overview node, and a line in the originating feature's `## Log` pointing to it. Say "this is feature-sized; making it feature N" and do it. The board holds features and their items; the file holds the work.

## Pointer and Next

The header's `Pointer`, `Last done` and `Next` are the exact place work stopped and are authoritative: a resuming session continues there and nowhere else. **Before any turn ends with work pending, rewrite `Next` as one concrete action naming the file and the change** — never "continue implementing". The board row mirrors the pointer. `/A.resume` (`../resume/SKILL.md`) reads these first.

## Status header

```
---
Feature: 7 · <short title>
Area: <one of config areas>
Work item: <id under tracker_label, or "not tracked">
Session: <host>-<feature>-<date time>   (the session currently working here)
Type: plan | extend
Mode: auto | <command that overrode auto>
Phase: Start | Read | Evaluate | Clarify | Gate | Approved | Implement | Realign | Verified | Stopped | Closed
Tier: S | M | L | XL (signals: ...)
Pointer: 7.2 › 3/5 — <step name> — in progress | done | blocked
Last done: 7.2 step 2 — <what, where> (13 Nov 26, 05:31 PM)
Next: <one concrete action: file and change>
Opened: 13 Nov 26, 04:15 PM
Updated: 13 Nov 26, 05:40 PM
Continues: <closed feature file, when reopened>
Open items: <count>
---
```

Each item under `## Items` repeats `Phase · Pointer · Last done · Next · Result` for itself. The feature's board block mirrors this header; its item rows mirror the item headers. Dates and times follow config.

## Output

In chat: plain language, the user's words, what it means and what is next; detail by reference to the file (`references/communication.md`). In the file: everything, precisely, timed, append-only. Code first when code is the answer; then at most three lines on what was skipped and when to add it.
