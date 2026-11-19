# Flow — each command knows what comes before it and what comes after

Every command knows three things: what it **needs** to exist, what it **produces**, and what the **natural next step** is. That knowledge is used in two places: at the start, when something it needs is missing; and at the end, when the user should be told what comes next — with a default, so one word moves the work on.

## The map

| Command | Needs | Produces | Natural next |
| --- | --- | --- | --- |
| `/A.rootcause` (`.m` `.l` `.xl`) | a reported wrong behaviour; a project | a root-cause report: CONFIRMED / LIKELY with its condition, or not-found with coverage | `/A.plan` from the report (fix at the origin) |
| `/A.plan` · `/A.plan.realign` | a request (chat or argument), or a root-cause report; a project | a report at Gate | Review (M+) → Approve → Implement |
| Clarify (inside `/A.plan`) | an ask with open questions | answers / assumptions | the report |
| `/A.review` (stage; `.m` `.l` `.xl` choose the effort) | something to review: a report or a plan (a build goes to `/A.build.review`) | findings resolved; a revised report | Approve, or back to the report if material |
| `/A.review` with pasted comments | the comments and the change they refer to | verdicts per comment; FIX steps | Approve the FIX steps → Implement |
| `/A.build` | an **approved** plan with steps | built steps, changes, build findings | Realign → Build review (M+) → Validate |
| Realign (inside `/A.build`); `/A.plan.scope_check_drift_check`, `/A.plan.lean_overcomplication_check` at any time | something built | simplifications, findings for the user | Build review (M+), else Validate |
| `/A.build.review` | something built, and the user's words for it (`## Instructions`, `## Clarifications`, or the request in the chat) | a verdict — Sound / Sound once fixed / Shallow / Off target — with evidence per obligation, what was not examined, the decisions taken without the user | Sound → Validate; otherwise the fixes as a new item at Gate → Build → the review again |
| `/A.verify` | something built; at L and XL, a build review on it | verification evidence | Close |
| `/A.close` | a verified feature | ledgers updated, board row to Finished | nothing; or `/A.plan` for the next thing |
| `/A.build.resume` | a feature with a pointer | continuation at the pointer | whatever stage the pointer is in |
| `/A.project.status` · `.board` · `.map` · `.list` | the project files | an answer | the single most useful action, from the files |
| `/A.project.map` · `/A.project.drift` | a project | a codebase map / a drift report | features for the drifts the user picks |

## When something needed is missing

Say what is missing and offer the shortest way through, with a default — one question:

- `/A.plan` asked to fix a wrong behaviour whose cause is unknown → "The cause isn't established yet. Run `/A.rootcause` first (recommended), or plan against the symptom knowing it may not be the cure?"
- `/A.review` on chat work that has no plan or report → review it anyway as a plan-in-the-making (the lenses apply to any design text), then at the end: "This has no plan on the board. Make it one, so it can be approved and built? (yes, recommended / no)".
- `/A.build` with nothing approved → "Nothing is approved yet. The report at Gate has <n> decisions; take the recommended answers and approve? (yes / show me)".
- `/A.verify` with nothing built → say so; offer `/A.project.status` or `/A.build.resume`.
- `/A.verify` or `/A.close` on a tier L or XL build with no build review → "This build hasn't been reviewed against what you asked. Run the build review first? (yes, recommended)". Not skippable at L and XL; at M it is offered once.
- `/A.build.review` with nothing built → say which stage the feature is at; a plan at Gate goes to `/A.review`.
- `/A.build.review` on code with no recorded ask → ask for it in one line ("What was this meant to do, in your words?"); the answer is the standard.
- `/A.close` on an unverified feature → offer to run Validate first (default yes).
- Any stage command when the chat holds work the skill did not produce → treat the chat's work as the subject (`core/SKILL.md` Start step 0); never require the user to redo it "through the skill".

Running a predecessor as part of the command is allowed when the user says yes; it is logged as an item of the same feature, not a separate conversation.

## At the end: say what comes next, with a default

Every command ends by naming the next step **and its likely answer**, so the user can reply with one word:

- A report at Gate → "Next: Review (this is tier L). Say *go* to run it with the recommended decisions." (At L/XL the review is not skippable; the offer is only to start it.)
- A review that found nothing material → "Next: Approve. The <n> decisions below have recommended answers; say *go* to take them all."
- An approved plan → "Next: Build, 8 steps. Say *go*."
- A finished build → "Next: the build review (this is tier L) — fresh reviewers check it against what you asked. Say *go*." (Tier S: "Next: Verify. Say *go*.")
- A build review that came back Sound → "Next: Verify. Say *go*."
- A build review that came back Shallow or Sound once fixed → "Next: the <n> fixes, as one item. The decisions below have suggested answers; say *go* to take them and build."
- A verified feature → "Next: Close. Say *go*, or keep working."
- A review of chat work with no feature behind it → "Next: make this a feature so it can be built (recommended), or leave it as a review only."

The next step is a recommendation grounded in the files, not a menu. Lists of every possible move ("approve, another review round, back to the report, or…") are not offered; the one the agent recommends is, with the alternative in a clause.
