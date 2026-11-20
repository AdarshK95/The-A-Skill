# Flow — each command knows what comes before it and what comes after

Every command knows three things: what it **needs** to exist, what it **produces**, and what the **natural next step** is. That knowledge is used in two places: at the start, when something it needs is missing; and at the end, when the user should be told what comes next — with a default, so one word moves the work on.

## One job each

Each tool answers one question, goes to one depth, and never produces the next tool's output. When two of them would overlap, the one whose question it is does the work.

| Tool | The question | How deep | Produces | Never produces |
| --- | --- | --- | --- | --- |
| Root cause | Why did this happen? | To the origin — something the system received, not produced — confirmed by a test | A cause | A fix |
| Plan | What do we change, and where? | Every caller of what changes; the alternatives | Steps | Code |
| Plan review | Is this plan right? | The plan and the code it cites | Corrections folded into that plan | New work |
| Build | Make it | Each step and its surroundings | Code, build findings | Scope changes |
| Build review | Is it built as asked, all the way down? | From the user's words to where each rule has to live; outside the diff only where the ask depends on it | A verdict; findings, each with whose it is and where it goes | A fix, a plan |
| Verify | Does it work where users are? | Running it | Proof | — |

The build review stops at *where* a rule is not held and *how*. Root cause goes on to *why*. They differ only when the gap was itself caused by something upstream, and then the finding is handed over, not dug into.

## Whose finding is it — origin, then exit

Every finding, from any stage, says whose it is before it becomes anything else.

| Origin | Means | What happens |
| --- | --- | --- |
| **Ours** | This work added it or broke it | Fixed now, in this feature |
| **Exposed** | It was there before and this work never touched it, but what the user asked cannot be true without it | Fixed now when it sits at an owner this work already changed; otherwise a decision for the user |
| **Pre-existing** | It was there before, and what the user asked holds without it | One line on the board for later. Never in this feature's fixes. Never counted in a verdict |

Then exactly one exit:

| Exit | When | Next |
| --- | --- | --- |
| **Fix** | Ours or exposed; the cause is plain from the finding; one right place for it | A fix item at the owner, sized like any item |
| **Decide** | It comes from a design choice or from words that carry two needs; or several findings share one origin; or it is exposed and lies outside what this work touched | A decision for the user; the plan changes (`/A.plan.realign`) only if they choose a different design |
| **Diagnose** | The cause cannot be seen from the code — work that vanished, something that cannot happen | `/A.rootcause` on that finding or group, and nothing else |
| **Later** | Pre-existing, or noticed in passing | The board (Deferred or To do), shown once at Close to schedule, defer or drop |

Ours and exposed are finished, verified and shipped first. A pre-existing problem that loses data or opens access is raised to the user at once as its own proposed feature — raised, not folded in. What a build added that it should not have (duplication, dead code) is its own item, after the fixes for what was asked.

## The four paths, step by step

Every path ends the same way — **the ending**:

1. **Approve.** The user says go. Nothing is built before that.
2. **`/A.build`** builds the approved steps only. Anything else it notices is written down with its origin, not fixed. It ends with the scope check and the lean check, each saying its result.
3. **`/A.build.review`** (by size; small work only when called) checks the build against the user's words. Each finding leaves with its origin and its exit.
4. **The fix round.** Ours and exposed only, as an item sized like any other. Then the review re-checks only what the fixes touched.
5. **`/A.verify`**, then **`/A.close`**, which shows the later list.

**Something new.** 1. `/A.plan` — reads the code, asks up to five questions, records the user's words, runs the scope and lean checks on the plan, shows the plan with its options. 2. `/A.review` at M and above; corrections fold into the plan. 3. The ending.

**Changing something that exists.** 1. `/A.plan.realign` — what exists against what is wanted: what stays, what changes, what goes; the two checks. 2. `/A.review` by size. 3. The ending.

**A bug is reported.** 1. `/A.rootcause` — a cause confirmed by a test, or "not found" with what would find it; never a fix. 2. `/A.plan` from that cause — the fix at the origin, with a check that fails if it returns; the two checks. 3. `/A.review` by size (a small fix: none). 4. The ending.

**Issues are found in the code** (by a review, an audit, or the user noticing). 1. Sort each by origin. 2. By exit: *fix* → a small item through `/A.plan`; *diagnose* → `/A.rootcause` for that one; *decide* → the user, then `/A.plan.realign` if the design changes; *later* → the board. 3. The ending, per item.

## What ends the loop

1. **A review's findings are confirmed and answered, never reviewed.** There is no review of a review.
2. **A review's corrections fold into the thing reviewed** — the plan, or the build. They do not start the workflow again.
3. **A fix item is sized like any work** (`sizing.md` over the fix set). Tier S gets no plan review. That is the ordinary rule for a plan, not a second look at the review.
4. **After fixes, a build review re-runs only what the fixes touched**, and re-tests each problem it confirmed before.
5. **Rounds stop** at two clean rounds, at five rounds, or when a fix undoes an earlier fix. Then the user decides.
6. **Root cause runs once per finding or group.** "Not found" goes to the user with what would find it; it does not run again on its own.

**Which outranks which.** The user's latest word, then their earlier word, then the plan, then the build. A confirmed cause outranks a review's view of where a fix belongs. A review's verdict outranks the builder's claim. Nothing outranks the user.

## The map

| Command | Needs | Produces | Natural next |
| --- | --- | --- | --- |
| `/A.rootcause` (`.m` `.l` `.xl`) | a reported wrong behaviour, or a finding or group a review marked *diagnose*; a project | a root-cause report: CONFIRMED / LIKELY with its condition, or not-found with coverage | `/A.plan` from the report (fix at the origin) |
| `/A.plan` · `/A.plan.realign` | a request (chat or argument), or a root-cause report; a project | a report at Gate, with its scope and lean lines | Review (M+) → Approve → Implement |
| Clarify (inside `/A.plan`) | an ask with open questions | answers / assumptions | the report |
| `/A.review` (stage; `.m` `.l` `.xl` choose the effort) | something to review: a report or a plan (a build goes to `/A.build.review`) | findings resolved; a revised report | Approve, or back to the report if material |
| `/A.review` with pasted comments | the comments and the change they refer to | verdicts per comment; FIX steps | Approve the FIX steps → Implement |
| `/A.build` | an **approved** plan with steps | built steps, changes, build findings, the scope and lean lines for the build | Build review (M+) → Validate |
| `/A.plan.scope_check_drift_check`, `/A.plan.lean_overcomplication_check` | a plan or a build | their result in one line, and findings for the user | the stage that was active; they also run on their own before every plan is shown and after every build |
| `/A.build.review` (`.s` `.m` `.l` `.xl` choose the depth) | something built, and the user's words for it (`## Instructions`, `## Clarifications`, or the request in the chat) | a verdict — Sound / Sound once fixed / Shallow / Off target — with evidence per obligation; findings each with origin and exit; what was not examined; the decisions taken without the user | Sound → Validate; otherwise by exit: a fix item, a decision, a root cause, the board |
| `/A.verify` | something built, with its scope and lean lines; at L and XL, a build review on it | verification evidence | Close |
| `/A.close` | a verified feature | ledgers updated, the later list shown, board row to Finished | nothing; or `/A.plan` for the next thing |
| `/A.build.resume` | a feature with a pointer | continuation at the pointer | whatever stage the pointer is in |
| `/A.project.status` · `.board` · `.map` · `.list` | the project files | an answer | the single most useful action, from the files |
| `/A.project.map` · `/A.project.drift` | a project | a codebase map / a drift report | features for the drifts the user picks |

## When something needed is missing

Say what is missing and offer the shortest way through, with a default — one question:

- `/A.plan` asked to fix a wrong behaviour whose cause is unknown → "The cause isn't established yet. Run `/A.rootcause` first (recommended), or plan against the symptom knowing it may not be the cure?"
- `/A.review` on chat work that has no plan or report → review it anyway as a plan-in-the-making (the lenses apply to any design text), then at the end: "This has no plan on the board. Make it one, so it can be approved and built? (yes, recommended / no)".
- `/A.build` with nothing approved → "Nothing is approved yet. The report at Gate has <n> decisions; take the recommended answers and approve? (yes / show me)".
- `/A.verify` with nothing built → say so; offer `/A.project.status` or `/A.build.resume`.
- A plan about to be shown, or a build about to be reviewed, verified or closed, without its scope and lean lines → run the two checks now and say their results; this is never skipped and never asked.
- `/A.verify` or `/A.close` on a tier L or XL build with no build review → "This build hasn't been reviewed against what you asked. Run the build review first? (yes, recommended)". Not skippable at L and XL; at M it is offered once.
- `/A.build.review` with nothing built → say which stage the feature is at; a plan at Gate goes to `/A.review`.
- `/A.build.review` on code with no recorded ask → ask for it in one line ("What was this meant to do, in your words?"); the answer is written into the feature's `## Instructions` before the review starts, so the standard outlives the review.
- `/A.close` on an unverified feature → offer to run Validate first (default yes).
- Any stage command when the chat holds work the skill did not produce → treat the chat's work as the subject (`core/SKILL.md` Start step 0); never require the user to redo it "through the skill".

Running a predecessor as part of the command is allowed when the user says yes; it is logged as an item of the same feature, not a separate conversation.

## At the end: say what comes next, with a default

Every command ends by naming the next step **and its likely answer**, so the user can reply with one word:

- A report at Gate → "Next: Review (this is tier L). Say *go* to run it with the recommended decisions." (At L/XL the review is not skippable; the offer is only to start it.)
- A review that found nothing material → "Next: Approve. The <n> decisions below have recommended answers; say *go* to take them all."
- An approved plan → "Next: Build, 8 steps. Say *go*."
- A finished build → "Scope check: clean. Lean check: two helpers merged. Next: the build review (this is tier L) — fresh reviewers check it against what you asked. Say *go*." (Tier S: "Next: Verify. Say *go*.")
- A build review that came back Sound → "Next: Verify. Say *go*."
- A build review that came back Shallow or Sound once fixed → "<n> are ours to fix now, <n> need your decision, <n> need a cause found first, <n> are older problems noted for later. Next: your decisions, then I plan the fixes. Say *go* to take the suggested answers."
- A verified feature → "Next: Close. Say *go*, or keep working."
- A review of chat work with no feature behind it → "Next: make this a feature so it can be built (recommended), or leave it as a review only."

The next step is a recommendation grounded in the files, not a menu. Lists of every possible move ("approve, another review round, back to the report, or…") are not offered; the one the agent recommends is, with the alternative in a clause.
