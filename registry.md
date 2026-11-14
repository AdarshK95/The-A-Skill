# /A.* commands — by stage

Type `/A.` and keep typing: the picker filters on any word in a name (`/A.scope` and `/A.drift` both find the scope/drift check). No command typed means **auto** — say what you want and the right command runs. A mistyped command also lands in auto.

## plan — decide what to do

| Command | Does |
|---|---|
| `/A.plan <idea>` | Plan something new: fit against the code, alternatives, steps, a report to approve |
| `/A.plan.realign <what>` | Realign the plan to what exists: continue or change built work; baseline, drift, remaining steps. Reopens a closed feature |
| `/A.plan.bugfix <what broke>` | Trace to root cause, plan the fix at the root, analyze what the fix could break |
| `/A.plan.scope_check_drift_check` | Scope check / drift check: has the work outgrown its type (promote or demote); has the plan drifted from the ask, or the code from the plan |
| `/A.plan.lean_overcomplication_check` | Is the plan lean: duplication, speculative generality, reuse missed, hardcoding |

## review — fresh eyes before building

| Command | Does |
|---|---|
| `/A.review` | Fresh-eyes review of the current plan or build; effort chosen by the rubric. Paste reviewer comments and it triages them instead |
| `/A.review.m` · `/A.review.l` · `/A.review.xl` | The same review at the effort you choose |

## build — make it

| Command | Does |
|---|---|
| `/A.build` | Build the approved plan step by step: look around before each edit, wire and check after; realign and simplify inside |
| `/A.build.resume` | Pick up an interrupted build: tracker read, done steps verified against the files, continue at the pointer |

## verify · close — prove it, finish it

| Command | Does |
|---|---|
| `/A.verify` | Run the checks, tick requirements with evidence, diff the build against the plan |
| `/A.close` | Finish the feature: ledgers, element histories, board to Finished |

## project — manage and see

| Command | Does |
|---|---|
| `/A.project.start` | Make this folder a project (one confirmation) |
| `/A.project.status` | Where are we, what is pending, what is next — from the files |
| `/A.project.board` | The tracker: planned, in progress, finished, deferred, to do |
| `/A.project.map` | The visual map of the system's elements and connections, with state; `/A.project.map <element>` pulls the thread: everything that happened to it, in order |
| `/A.project.drift` | Documents, decisions, elements and map versus the code |
| `/A.project.list` | All projects on this machine and how they depend on each other |

## skill — the tool itself

| Command | Does |
|---|---|
| `/A.skill.update` | Check for a newer release; install after you confirm |
| `/A.skill.repair` | Check the installed files against the release; restore after you confirm |
| `/A.skill.uninstall` | Remove the skill's own files after you confirm; never your projects' data |
| `/A.skill.help` · `/A.help` | This page |
