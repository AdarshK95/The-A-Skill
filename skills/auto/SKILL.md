---
name: auto
description: The default mode. Decides which activity a message belongs to and which stage it is in, so the user rarely needs to type a command.
disable-model-invocation: true
---

# Auto mode

**Place in the flow:** the router; needs nothing; hands the message to the right command. See `../core/references/flow.md`.

Auto is on whenever the user did not type an `/A.*` command. It never does the work itself; it decides *where* the message belongs, says so in one line, and runs the spine (`../core/SKILL.md`) from there.

## A mistyped or unknown command is auto

Anything the user types that looks like a command but matches none (`/A.scopecheck`, `/A.drif`, `/A.plan.fix`, `/A review`) arrives as plain text. Treat it as auto with a strong hint: map the words to the nearest command by stage and action (`scope`, `drift` → `/A.plan.scope_check_drift_check`; `lean`, `simplif`, `overcompl` → `/A.plan.lean_overcomplication_check`; `fix`, `bug`, `root`, `cause`, `why`, `diagnose` → `/A.rootcause`; `extend`, `continue`, `reopen`, `realign plan` → `/A.plan.realign`; `implement`, `build` → `/A.build`; `resume`, `pick up` → `/A.build.resume`; `validate`, `test`, `verify` → `/A.verify`; `board`, `tracker`, `todo` → `/A.project.board`; `map`, `overview`, `diagram`, `thread` → `/A.project.map`; `status`, `where`, `pending` → `/A.project.status`; `init`, `setup`, `start project` → `/A.project.start`; `update skill`, `upgrade` → `/A.skill.update`), say the command you took it as in one line, and run it. No guess among several → one question naming them.

## On every message, in order

**0. Shared folder.** In a fresh conversation, read it first; non-empty means work is in flight — say what, in plain words, before locating anything.

**1. Locate — this chat first.** Resolve the subject exactly as the spine's Start step 0: what the user pointed at; else what this conversation is doing (an activity opened here, else the latest substantive work in the chat); else fetch the board's candidates and offer them by name with their next action; if both chat and board are plausible, one question naming both. Then the project (named → files → conversation → only one → ask). Only then, within that project:

**2. Classify** a new request into one entry type, and say it in one line ("Treating this as a bug fix"):

| Type | Signals in the request |
|---|---|
| **plan** | something that does not exist yet: add, build, create, design, new, support X |
| **plan.realign** | something exists and should change or continue: change, update, continue, finish, rework, "you did X but I wanted Y", reopen |
| **rootcause** | something went wrong and the cause is not known: broken, fails, error, wrong answer, wrong result, crash, regression, "used to work", "why did it do that", "is this a bug". The shape of a likely fix never decides this: a wrong behaviour is a root-cause investigation until the cause is CONFIRMED or LIKELY; only then does `/A.plan` plan the fix |
| **review** | comments from someone or something outside this conversation: pasted review notes, a PR link, "Copilot says" |
| **status** | a question about state: where are we, what is pending, what did we do, what is next → `/A.project.status`, no activity |
| **chat** | a question that changes no code and keeps no analysis: explain, what does this do, how does X work → answer it, no activity |

When two types fit, pick the one whose *first step* the user needs now and say the other is available. When none fits, ask one question with the two likeliest choices.

An activity opens when code will change or when analysis is to be kept. A `chat` answer that the user then wants kept becomes a `plan` or `extend` activity at that point.

**3. Stay.** Inside an open activity, every message is read *within its current stage*:

| Stage | A follow-up message is… |
|---|---|
| Clarify / Gate | An answer, a revision to the plan, or a new clarification — the report is revised; still Gate |
| Approved / Implement | A refinement of a step, a build finding, or a change of direction (→ Realign now) — still Implement |
| Realign / Verified | Acceptance, a further simplification, or a reopen of a step — still here |

Auto never reclassifies an open feature. The user changes type by command (`/A.rootcause` inside a feature opens an item) or by saying so.

**4. Advance.** Reground first (`../core/references/lean.md › Reground`): scope, lean, premise — silent when yes, one line and the check when not. When the current stage's done-condition is met, move to the next stage and say it in one line ("Report ready — your decision on 2 items", "Approved — implementing step 1/5"). Stop at every gate the spine defines. Nothing past Approve runs on auto; the user's go is required every time.

## Commands as overrides

An `/A.*` command typed inside an open activity is a temporary override:

- A **stage** command (`review`, `build`, `verify`, `close`, the scope/drift and lean checks) runs that stage on the current activity now, then returns to where it was.
- An **entry** command (`rootcause`, `plan`, `plan.realign`, `review` with pasted comments) opens a new **item** inside the current feature (spine → Items), runs it to its result, then returns the pointer to the item that was active. Promote it to its own feature when it is feature-sized.

Set `Mode:` in the header to the command that overrode auto for as long as the override lasts; back to `auto` afterwards.

## Fresh conversation, work in flight

When a new conversation starts and the board has In-progress rows but the message matches none of them, say which rows are in flight in one line each and ask whether this is new work or one of them. Do not guess.

## What auto never does

Answer "where are we" from memory (read the files). Build without an approved report. Switch an activity's type on its own. Open an activity for a question that changes nothing.
