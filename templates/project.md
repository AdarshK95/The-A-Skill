---
schema_version: 1
project_name: {{project_name}}
docs_root: docs/
constitution: docs/constitution.md
decisions_log: docs/decisions.md
implementation_log: docs/implementation-log.md
api_docs: docs/api.md
activity_folder: docs/activity/
activity_template: docs/activity/_template.md
project_board: docs/activity/BOARD.md
reminders: on
gitignore: on
areas: General
depends_on: []
provides: []
activity_naming: "{yyyy}-{mm}/{yyyy}-{mm}-{dd}/{seq}-{slug}.md"
ledger_pattern: "docs/activity/{yyyy}-{mm}/_ledger.md"
date_format: DD MMM YY
time_format: 12h
filename_date_format: YYYY-MM-DD
tracker_label: Work item
lessons_log: docs/lessons.md
always_on_files: CLAUDE.md, AGENTS.md, .github/copilot-instructions.md
close_updates: implementation_log, api_docs, ledger
review:
  default_floor: S
  fresh_context: auto
  xl_engine: builtin
implement:
  posture: full
approval:
  second_reviewer: off
map_folder: docs/map/
shared_folder: .a/shared/
claim_stale_hours: 4
drift:
  cadence_days: 7
rules: |
  (Project-specific working rules go here. Standing principles belong in the constitution.)
---

# About this file

This is the only place the `/A.*` skills learn anything about this project. Every path above is relative to the project root. Change a path and the skills follow it; set a value to `none` and that behaviour is skipped.

- **constitution** — standing rules every piece of work is checked against. Agents read it first and never edit it without you.
- **decisions_log** — why things are the way they are. Agents append here at every approval gate and read it before proposing changes.
- **implementation_log** — what has shipped, one entry per closed activity.
- **depends_on / provides** — how this project relates to other projects on this machine. Empty means independent; that is a statement. Mirrored into `~/.a/projects.md`.
- **lessons_log** — drifts and mistakes with what to do instead; read before every piece of work.
- **activity_folder** — one file per feature, in month and day folders, with a month ledger; a new session resumes from it.

Field reference: `.a/skills/core/references/config-schema.md`.
