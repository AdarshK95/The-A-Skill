# Skills — the method

Each folder holds one `SKILL.md`. Every command's wrapper (in `../commands/`) points at one of these; every skill except `core` sends the agent to `core/SKILL.md` for the shared workflow. There is no `SKILL.md` at this level on purpose: start with `core/SKILL.md`.

| Folder | What it is |
| --- | --- |
| `auto/` | Default mode: locate the activity, classify a new request, stay in the current stage, advance when done |
| `board/` | /A.board — show the project board or add to it in plain language |
| `bugfix/` | /A.bugfix — trace to root cause, fix at the root, analyze fix impact |
| `close/` | /A.close — finish a feature, update the ledgers, move it to Finished |
| `core/` | The shared spine every command runs on, plus references/ (sizing, lenses, logging, lean, shared, communication …) |
| `drift/` | /A.drift — documents and decisions versus code |
| `extend/` | /A.extend and /A.reopen — continue or change what exists |
| `help/` | /A.help — show the command list |
| `start-project/` | /A.start-project (aliases init, setup, initialize) — make this folder a project; register it in the machine-wide index |
| `projects/` | /A.projects — all projects on this machine and how they depend on each other |
| `map/` | /A.map — map an existing codebase |
| `plan/` | /A.plan — design and build something new |
| `resume/` | /A.resume — continue at the exact step work stopped |
| `review/` | /A.review — triage an outside reviewer's comments |
| `simplify/` | /A.simplify — behaviour-preserving cleanup of recently modified code |
| `status/` | /A.status — where are we, from the files |
| `skill-repair/` | /A.skill-repair — check the skill's own files against the release; restore after confirmation |
| `skill-uninstall/` | /A.skill-uninstall — remove the skill's own files after confirmation; the user's work is never touched |
| `skill-update/` | /A.skill-update — check for a newer release of the skill; update after confirmation |
| `tracker/` | /A.tracker — the project overview diagram |

Counts for verifying an install: **20 skill folders**, **15 reference files** in `core/references/`, **36 markdown files** under `skills/` including this one. The installer prints the number it copied.
