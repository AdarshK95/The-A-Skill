# Config — `~/.a/settings.md` and `.a/project.md`

Two files. **`~/.a/settings.md`** (machine-wide, created by the installer from `templates/settings.md`) holds behaviour: verbosity, interrupts, whether chat work is offered for recording, review tier limits, date formats. **`.a/project.md`** holds everything about one project and may override any settings key for that project. Precedence: `project.md` > `settings.md` > the defaults below.

## Settings keys (`~/.a/settings.md`)

| Key | Meaning | Default |
|---|---|---|
| `verbosity` | `quiet` (decisions, stop points, answers only) · `normal` (plus a line per stage) · `verbose` (plus progress every few steps) | `quiet` |
| `progress_interrupts` | `blockers` (interrupt a running stage only for a blocking finding) · `findings` (also Majors) | `blockers` |
| `solution_mode` | `balanced` (recommend robust, name quick fixes, follow the user's stated theme) · `robust` · `quick` | `balanced` |
| `record_chat_work` | When a command runs on chat work not on the board: `ask` (offer once, afterwards) · `always` · `never` | `ask` |
| `review.auto_tier` | `on`: the rubric picks the tier within the limits; `off`: the floor unless the user sets one | `on` |
| `review.max_tier` | Highest tier the rubric may choose on its own | `XL` |
| `review.default_floor`, `review.fresh_context`, `dates.*` | As below; copied into new projects by `/A.start-project` | — |

## Project config — `.a/project.md`

The only file that knows anything about the project. The skill never contains a project name, path or tool; it reads them from here. `/A.start-project` creates it from `templates/project.md` and asks the user to confirm each value.

## Fields

| Key | Meaning | Default from `/A.start-project` |
|---|---|---|
| `schema_version` | Version of this config shape, so a newer skill can detect an older config and say what to migrate | `1` |
| `project_name` | The project's name in logs, chat, and the machine-wide projects index (`~/.a/projects.md`); unique on this machine | folder name |
| `depends_on` | Other projects this one uses, by `project_name`, each with one line on what it uses (for example `api-backend: REST contract in docs/api.md`). Empty means independent — and that is a statement, not an omission | empty |
| `provides` | What this project offers to others, one line each (a contract, a package, an MCP server). Read by dependents' sessions when their work touches it | empty |
| `docs_root` | Folder that holds the project's living documentation | `docs/` |
| `constitution` | Standing rules every phase gates against. Read whole in Phase 0 | `docs/constitution.md` |
| `decisions_log` | Append-only log of decisions with reasons. Searched in Phase 0, appended at every gate | `docs/decisions.md` |
| `implementation_log` | Project-level ledger of completed work, one entry per closed activity | `docs/implementation-log.md` |
| `api_docs` | Where API contracts are recorded; updated at close when an API changed. May be `none` | `docs/api.md` |
| `activity_folder` | Where per-activity files live | `docs/activity/` |
| `activity_template` | Body template for a new activity file (the skill writes the status header above it) | `docs/activity/_template.md` |
| `project_board` | The project board: Planned / In progress / Finished tables, Deferred, To do, and the overview diagram. Updated at every phase or step change; what parallel sessions and the user read instead of each other's files | `docs/activity/BOARD.md` |
| `areas` | The project's sections, used as the Area column on the board and as subgraphs in the overview (for example `UI, Backend, API, Data`). `/A.start-project` asks for them; the agent asks once when an activity fits none | `General` |
| `shared_folder` | Live coordination between parallel sessions: claims, handoffs, notes (`shared.md`). Empty means nothing in flight | `.a/shared/` |
| `claim_stale_hours` | A claim older than this with no newer activity from its session may be taken over, with a note | `4` |
| `gitignore` | `on`: `/A.start-project` adds `.a/` and the documentation paths it created to the project's `.gitignore` (marked block, removable); `off`: touches `.gitignore` never | `on` |
| `tmp_folder` | Where the agent keeps scratch that must live inside the project (sampling output, fixtures); ignored by git, emptied at Close. Scratch that need not be in the project goes to the OS temp folder instead | `.a/tmp/` |
| `reminders` | When `on`, every `/A.*` command first checks To do and Deferred for items due today or overdue and says so in one line | `on` |
| `activity_naming` | File path pattern inside `activity_folder`; may contain `/` to create month and day folders on demand. Tokens: `{yyyy}` `{mm}` `{dd}` `{date}` (uses `filename_date_format`) `{seq}` (zero-padded per day) `{type}` `{slug}` `{feature}` | `{yyyy}-{mm}/{yyyy}-{mm}-{dd}/{seq}-{slug}.md` |
| `tracker_label` | Name of the external work-item system shown in headers and ledgers (`Work item`, `ADO`, `Jira`, `Issue`); `none` hides the field | `Work item` |
| `deferred_decisions_log` | Decisions deliberately put off, each with its reasoning and the condition that reopens it; consequential and read at Start for work touching the same area | `docs/deferred-decisions.md` |
| `lessons_log` | Append-only log of drifts and mistakes with what to do instead; read at Start with the constitution | `docs/lessons.md` |
| `date_format` | How dates are written inside files and in chat. Tokens: `DD` `MMM` `MM` `YY` `YYYY`, spaces and punctuation kept | `DD MMM YY` (e.g. `13 Nov 26`) |
| `time_format` | `12h` → `hh:mm AM/PM`; `24h` → `HH:mm` | `12h` |
| `filename_date_format` | Date format used only for the `{date}` token in file and folder names, which are not prose and may sort chronologically | `YYYY-MM-DD` |
| `always_on_files` | Host instruction files `/A.start-project` appends the always-on block to, so every turn starts knowing this project uses the workflow | `CLAUDE.md, AGENTS.md, .github/copilot-instructions.md` |
| `ledger_pattern` | Optional periodic index (for example a monthly ledger). Tokens: `{yyyy}` `{mm}`. `none` disables it | `none` |
| `close_updates` | Which project-level files `/A.close` touches, in order | `implementation_log, api_docs, ledger` |
| `review.default_floor` | Lowest tier the project allows. `S` means the rubric decides freely | `S` |
| `review.fresh_context` | `auto` (use subagents when the host has them), `always` (refuse to review without them), `never` (cold self-review only) | `auto` |
| `review.isolation_verified` | Written by the isolation probe (`hosts.md`): `<host> <date> <fresh | not fresh>`, one per host | empty |
| `review.xl_engine` | `builtin` runs this skill's XL stages; `egm` hands XL review to the Elephant-Goldfish Model plugin when installed | `builtin` |
| `implement.posture` | `lite` builds as planned and names the lazier alternative; `full` enforces the ladder; `ultra` ships the smallest version and questions the rest | `full` |
| `approval.second_reviewer` | `on` requires a named second person's go, logged as a decision, after the user's | `off` |
| `map_folder` | Where `/A.map` writes the codebase map (one short contract per directory). `none` disables the map | `docs/map/` |
| `drift.cadence_days` | After this many days without `/A.drift`, `/A.status` says it is overdue | `7` |
| `rules` | Free-text project rules that are too operational for the constitution (branch naming, commit message shape, where tests live) | empty |

## The central repository

Everything the config names forms one documentation set any agent can read. The default `/A.start-project` layout, extendable by adding keys:

| Default file | Holds | Written |
| --- | --- | --- |
| `docs/constitution.md` | Standing rules | By the user only |
| `docs/implementation-log.md` | One line + link per closed feature | `/A.close` |
| `docs/api.md` | Contracts as they exist now | `/A.close` when a contract changed |
| `docs/decisions.md` | Why, with alternatives rejected | At every gate and fork |
| `docs/lessons.md` | Drift and mistakes, what to do instead | When the user stops a drift; Realign |
| `docs/deferred-decisions.md` | Decisions deliberately put off, with the reasoning and the condition that reopens them | A review finding or design question the user defers; Realign |
| `docs/board.md` | Planned · In progress · Finished · Deferred · To do · Overview | Every stage or step move |
| `docs/map/` | One contract per directory | `/A.map`, `/A.drift` |
| `.a/shared/` | Live claims, handoffs and notes between sessions; empty when nothing is in flight | Every session, continuously |
| `docs/activity/<yyyy>-<mm>/_ledger.md` | One row per feature that month | At creation and every status change |
| `docs/activity/<yyyy>-<mm>/<yyyy>-<mm>-<dd>/<seq>-<slug>.md` | The feature: summary, event log, items, findings, changes | Continuously |

Projects that already have numbered files (`01.Implementation logs.md`, `02.API Documentation.md`, `03.Decisions.md` …) point the keys at them; `/A.start-project` offers to add the missing ones with the next numbers.

## Resolution

Paths are relative to the project root. A key that is missing takes the default above. A key set to `none` disables that behaviour and the skill says so once when it would have used it.

## Example

```markdown
---
schema_version: 1
project_name: Example Service
docs_root: documentation/
constitution: documentation/00.Constitution.md
decisions_log: documentation/03.Decisions.md
implementation_log: documentation/01.Implementation logs.md
api_docs: documentation/02.API Documentation.md
activity_folder: documentation/Activity log/
activity_template: documentation/Activity log/_template.md
project_board: documentation/Activity log/BOARD.md
areas: UI, Backend, API, Data, Infra
activity_naming: "{yyyy}-{mm}/{yyyy}-{mm}-{dd}/{seq}-{slug}.md"
date_format: DD MMM YY
time_format: 12h
filename_date_format: YYYY-MM-DD
tracker_label: ADO
lessons_log: documentation/06.Lessons.md
ledger_pattern: "documentation/Activity log/{yyyy}-{mm}/_ledger.md"
close_updates: implementation_log, api_docs, ledger
review:
  default_floor: S
  fresh_context: auto
  xl_engine: builtin
implement:
  posture: full
approval:
  second_reviewer: off
map_folder: documentation/Map/
shared_folder: .a/shared/
claim_stale_hours: 4
drift:
  cadence_days: 7
depends_on:
  - api-backend: REST contract in documentation/02.API Documentation.md
provides:
  - Web UI consuming the API; nothing other projects import
rules: |
  Every fix ships for all environments; no dev-only or partial fixes.
  Cache invalidation is version-based, never TTL-based.
  Citations in generated answers map to exactly one source chunk.
---
```

## Migration

When `schema_version` is lower than the version this skill expects, list the keys added or renamed since, propose the new values, and write nothing until the user confirms.
