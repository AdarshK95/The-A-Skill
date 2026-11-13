# /A.* commands

Type `/A.auto <ask>` or just say what you want — auto mode picks the right path. Type a command to steer.

## Start work (entry types)

| Command | Use it when | What you get |
|---|---|---|
| `/A.plan <idea>` | Something new | Fit against the code, alternatives, a step list, a report to approve |
| `/A.extend <what>` · `/A.reopen <file>` | Something exists and should change or continue | Baseline vs code, drift list, the remaining work as steps |
| `/A.bugfix <what broke>` | Something is wrong | Trace to root cause, fix at the root, fix-impact analysis |
| `/A.review <comments>` | Comments from a reviewer or tool | Each comment verified: fix / contest / defer / ask you |

## Move work along (stages)

Every activity flows: **Read → Evaluate → Clarify → Report → Review → Approve → Implement → Realign → Validate → Close.** Auto advances for you and stops at every approval. Call a stage directly to run it now.

| Command | Does |
|---|---|
| `/A.clarify` | Asks the open questions, one at a time, up to five |
| `/A.review` | Fresh-eyes review of the current plan or build (with pasted comments, it is the entry type above) |
| `/A.implement` · `/A.build` | Builds the approved steps, one at a time, logging as it goes |
| `/A.realign` | Checks the build against the original ask; removes what crept in, what duplicates something existing, what is hardcoded |
| `/A.simplify` · `/A.lean` | Behaviour-preserving cleanup of recently modified code, proven by the checks |
| `/A.validate` · `/A.verify` · `/A.test` | Runs the checks; proves the build matches the plan |
| `/A.close` · `/A.done` · `/A.finish` | Finishes this topic: updates the project ledgers, moves it to Finished |

## See where things stand

| Command | Does |
|---|---|
| `/A.status` | Where are we, what is pending, what is next — read from the files, never from memory |
| `/A.board` | The project board: Planned · In progress · Finished · Deferred · To do |
| `/A.tracker` · `/A.flow` · `/A.overview` | The project overview diagram, by area, coloured by state |
| `/A.resume` | Continue a feature at the exact step it stopped, after checking the files match the log |

## Keep the project healthy

| Command | Does |
|---|---|
| `/A.map` · `/A.bootstrap` | Maps an existing codebase: one short contract per directory, and the overview's first nodes |
| `/A.drift` | Finds where documents, decisions and the overview have diverged from the code; run weekly |

## Set up

| Command | Does |
|---|---|
| `/A.start-project` · `/A.init` · `/A.setup` · `/A.initialize` | Make this folder a project: config, docs, board, shared folder, always-on block, and a row in the machine-wide index. Run once per folder you work in |
| `/A.projects` | All projects on this machine and how they depend on each other |
| `/A.skill-update` | Checks for a newer release of The A Skill itself; tells you installed vs latest; updates only after you say yes |
| `/A.skill-uninstall` | Removes the skill's own files after you confirm; keeps every project's config, documentation, board and logs |
| `/A.skill-repair` | Checks the skill's own installed files; reports missing or altered; restores only after you say yes |
| `/A.help` · `/A.skills` · `/A.list` · `/A.tools` | Shows this page |
