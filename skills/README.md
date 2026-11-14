# Skills — the method, by stage

Each folder holds one `SKILL.md`. Command wrappers in `../commands/` point at these; every skill except `core` sends the agent to `core/SKILL.md` for the shared workflow. Folder names mirror the commands: `plan-*` is the plan stage, `project-*` the project stage, `skill-*` the tool itself.

| Folder | What it is |
| --- | --- |
| `auto/` | Default mode: locate the subject and project, classify, stay in stage, advance; maps mistyped commands |
| `build/` | /A.build and /A.build.resume — build the approved plan; realign and simplify inside; resume an interrupted build from the tracker |
| `close/` | /A.close — finish a feature, update ledgers and element histories |
| `core/` | The shared spine and references/ (sizing, lenses, logging, lean, shared, communication, hierarchy, elements …) |
| `plan/` | /A.plan — plan something new |
| `plan-lean_overcomplication_check/` | /A.plan.lean_overcomplication_check — is the plan lean |
| `plan-realign/` | /A.plan.realign — continue or change what exists; reopen a closed feature |
| `plan-scope_check_drift_check/` | /A.plan.scope_check_drift_check — type still right; plan vs ask; code vs plan |
| `project-board/` | /A.project.board — the tracker |
| `project-drift/` | /A.project.drift — documents, decisions, elements and map vs code |
| `project-list/` | /A.project.list — all projects on this machine |
| `project-map/` | /A.project.map — the visual map, assembled after resolving name drift; pull the thread on an element |
| `project-start/` | /A.project.start — make a folder a project |
| `project-status/` | /A.project.status — where are we, from the files |
| `rootcause/` | /A.rootcause (and .m .l .xl) — understand, observe, three parallel lanes, coverage check, reconcile, confirm; a cause, never a fix |
| `review/` | /A.review (and .m .l .xl) — fresh-eyes review, or triage of pasted comments |
| `skill-help/` | /A.skill.help · /A.help — commands by stage |
| `skill-repair/` | /A.skill.repair — restore the skill's own files after confirmation |
| `skill-uninstall/` | /A.skill.uninstall — remove the skill's own files; never the user's data |
| `skill-update/` | /A.skill.update — update the skill after confirmation |
| `verify/` | /A.verify — checks, requirements, build vs plan |

Counts for verifying an install: **21 skill folders**, **21 reference files** in `core/references/`, **43 markdown files** under `skills/` including this one. The installer prints the number it copied.
