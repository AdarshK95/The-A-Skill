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
| `init/` | /A.init — set a project up (required before first use) |
| `map/` | /A.map — map an existing codebase |
| `plan/` | /A.plan — design and build something new |
| `resume/` | /A.resume — continue at the exact step work stopped |
| `review/` | /A.review — triage an outside reviewer's comments |
| `simplify/` | /A.simplify — behaviour-preserving cleanup of recently modified code |
| `status/` | /A.status — where are we, from the files |
| `tracker/` | /A.tracker — the project overview diagram |

Counts for verifying an install: **16 skill folders**, **13 reference files** in `core/references/`, **30 markdown files** under `skills/` including this one. The installer prints the number it copied.
