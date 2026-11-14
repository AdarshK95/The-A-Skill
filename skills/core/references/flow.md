# Flow — each command knows what comes before it and what comes after

Every command knows three things: what it **needs** to exist, what it **produces**, and what the **natural next step** is. That knowledge is used in two places: at the start, when something it needs is missing; and at the end, when the user should be told what comes next — with a default, so one word moves the work on.

## The map

| Command | Needs | Produces | Natural next |
| --- | --- | --- | --- |
| `/A.plan` · `/A.plan.realign` · `/A.plan.bugfix` | a request (chat or argument); a project | a report at Gate | Review (M+) → Approve → Implement |
| Clarify (inside `/A.plan`) | an ask with open questions | answers / assumptions | the report |
| `/A.review` (stage; `.m` `.l` `.xl` choose the effort) | something to review: a report, a plan, a build | findings resolved; a revised report | Approve, or back to the report if material |
| `/A.review` with pasted comments | the comments and the change they refer to | verdicts per comment; FIX steps | Approve the FIX steps → Implement |
| `/A.build` | an **approved** plan with steps | built steps, changes, build findings | Realign → Validate |
| Realign (inside `/A.build`); `/A.plan.scope_check_drift_check`, `/A.plan.lean_overcomplication_check` at any time | something built | simplifications, findings for the user | Validate |
| `/A.verify` | something built | verification evidence | Close |
| `/A.close` | a verified feature | ledgers updated, board row to Finished | nothing; or `/A.plan` for the next thing |
| `/A.build.resume` | a feature with a pointer | continuation at the pointer | whatever stage the pointer is in |
| `/A.project.status` · `.board` · `.map` · `.list` | the project files | an answer | the single most useful action, from the files |
| `/A.project.map` · `/A.project.drift` | a project | a codebase map / a drift report | features for the drifts the user picks |

## When something needed is missing

Say what is missing and offer the shortest way through, with a default — one question:

- `/A.review` on chat work that has no plan or report → review it anyway as a plan-in-the-making (the lenses apply to any design text), then at the end: "This has no plan on the board. Make it one, so it can be approved and built? (yes, recommended / no)".
- `/A.build` with nothing approved → "Nothing is approved yet. The report at Gate has <n> decisions; take the recommended answers and approve? (yes / show me)".
- `/A.verify` with nothing built → say so; offer `/A.project.status` or `/A.build.resume`.
- `/A.close` on an unverified feature → offer to run Validate first (default yes).
- Any stage command when the chat holds work the skill did not produce → treat the chat's work as the subject (`core/SKILL.md` Start step 0); never require the user to redo it "through the skill".

Running a predecessor as part of the command is allowed when the user says yes; it is logged as an item of the same feature, not a separate conversation.

## At the end: say what comes next, with a default

Every command ends by naming the next step **and its likely answer**, so the user can reply with one word:

- A report at Gate → "Next: Review (this is tier L). Say *go* to run it with the recommended decisions." (At L/XL the review is not skippable; the offer is only to start it.)
- A review that found nothing material → "Next: Approve. The <n> decisions below have recommended answers; say *go* to take them all."
- An approved plan → "Next: Build, 8 steps. Say *go*."
- A finished build → "Next: Verify. Say *go*."
- A verified feature → "Next: Close. Say *go*, or keep working."
- A review of chat work with no feature behind it → "Next: make this a feature so it can be built (recommended), or leave it as a review only."

The next step is a recommendation grounded in the files, not a menu. Lists of every possible move ("approve, another review round, back to the report, or…") are not offered; the one the agent recommends is, with the alternative in a clause.
