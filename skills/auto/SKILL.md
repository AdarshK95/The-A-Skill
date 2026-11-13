---
name: auto
description: The default mode. Decides which activity a message belongs to and which stage it is in, so the user rarely needs to type a command.
disable-model-invocation: true
---

# Auto mode

Auto is on whenever the user did not type an `/A.*` command. It never does the work itself; it decides *where* the message belongs, says so in one line, and runs the spine (`../core/SKILL.md`) from there.

## On every message, in order

**0. Shared folder.** In a fresh conversation, read it first; non-empty means work is in flight — say what, in plain words, before locating anything.

**1. Locate.** Which activity is this conversation in?

- An activity file was opened or resumed earlier in this conversation → that one.
- Otherwise read the project board. A Planned or In-progress feature whose title, item or file matches the request → `/A.resume` it (`../resume/SKILL.md`).
- The message says continue, resume, pick up, or where did we leave off → `/A.resume` with no target: it lists what is in flight and asks which.
- Otherwise the request is new → step 2.

**2. Classify** a new request into one entry type, and say it in one line ("Treating this as a bug fix"):

| Type | Signals in the request |
|---|---|
| **plan** | something that does not exist yet: add, build, create, design, new, support X |
| **extend** | something exists and should change or continue: change, update, continue, finish, rework, "you did X but I wanted Y", reopen |
| **bugfix** | something is wrong: broken, fails, error, wrong result, crash, regression, "used to work" |
| **review** | comments from someone or something outside this conversation: pasted review notes, a PR link, "Copilot says" |
| **status** | a question about state: where are we, what is pending, what did we do, what is next → `/A.status`, no activity |
| **chat** | a question that changes no code and keeps no analysis: explain, what does this do, how does X work → answer it, no activity |

When two types fit, pick the one whose *first step* the user needs now and say the other is available. When none fits, ask one question with the two likeliest choices.

An activity opens when code will change or when analysis is to be kept. A `chat` answer that the user then wants kept becomes a `plan` or `extend` activity at that point.

**3. Stay.** Inside an open activity, every message is read *within its current stage*:

| Stage | A follow-up message is… |
|---|---|
| Clarify / Gate | An answer, a revision to the plan, or a new clarification — the report is revised; still Gate |
| Approved / Implement | A refinement of a step, a build finding, or a change of direction (→ Realign now) — still Implement |
| Realign / Verified | Acceptance, a further simplification, or a reopen of a step — still here |

Auto never reclassifies an open feature. The user changes type by command (`/A.bugfix` inside a feature opens an item) or by saying so.

**4. Advance.** When the current stage's done-condition is met, move to the next stage and say it in one line ("Report ready — your decision on 2 items", "Approved — implementing step 1/5"). Stop at every gate the spine defines. Nothing past Approve runs on auto; the user's go is required every time.

## Commands as overrides

An `/A.*` command typed inside an open activity is a temporary override:

- A **stage** command (`clarify`, `review`, `implement`, `realign`, `validate`, `close`) runs that stage on the current activity now, then returns to where it was.
- An **entry type** command (`plan`, `extend`, `bugfix`, `review` with pasted comments) opens a new **item** inside the current feature (spine → Items), runs it to its result, then returns the pointer to the item that was active. Promote it to its own feature when it is feature-sized.

Set `Mode:` in the header to the command that overrode auto for as long as the override lasts; back to `auto` afterwards.

## Fresh conversation, work in flight

When a new conversation starts and the board has In-progress rows but the message matches none of them, say which rows are in flight in one line each and ask whether this is new work or one of them. Do not guess.

## What auto never does

Answer "where are we" from memory (read the files). Build without an approved report. Switch an activity's type on its own. Open an activity for a question that changes nothing.
