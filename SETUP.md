# Setup

For a person, or for an agent asked to "install this repo into my project". Steps are the same.

## What gets installed where

| In your project | What | Why |
| --- | --- | --- |
| `.a/skills/` | The method (core spine, auto, plan, extend, bugfix, review, resume, status, board, tracker, close, init, help) | Both hosts read the skills from here by path |
| `.a/templates/` | Config, board, docs and always-on templates | `/A.init` creates project files from these |
| `.a/registry.md`, `.a/VERSION` | Command list; installed version | `/A.help`; upgrade checks |
| `.claude/commands/A.*.md` | One file per command | Claude Code shows them as `/A.plan`, `/A.bugfix`, … |
| `.github/prompts/A.*.prompt.md` | One file per command | Copilot in VS Code shows them as `/A.plan`, `/A.bugfix`, … |

Created later by `/A.init`, with your answers: `.a/project.md` (config), the docs the config names, the board, and the always-on block appended to `CLAUDE.md`, `AGENTS.md` and `.github/copilot-instructions.md`.

## Install

### A — ask your agent

In a chat opened at your project root:

> Install https://github.com/<owner>/<repo> into this project following its SETUP.md. Clone it to a temporary folder, run its install script against this project, then tell me what was installed.

The agent runs section B. If it cannot run scripts, it copies the files listed above by hand.

### B — script

```sh
git clone https://github.com/<owner>/<repo> /tmp/a-workflow
sh /tmp/a-workflow/install.sh /path/to/your/project
```

PowerShell:

```powershell
git clone https://github.com/<owner>/<repo> $env:TEMP\a-workflow
& "$env:TEMP\a-workflow\install.ps1" -Dest C:\path\to\your\project
```

Re-running updates the method and the commands. It never touches `.a/project.md` or your documents.

### C — by hand

Copy `skills/` → `.a/skills/`, `templates/` → `.a/templates/`, `registry.md` and `VERSION` → `.a/`, `commands/claude/*` → `.claude/commands/`, `commands/copilot/*` → `.github/prompts/`.

### D — Claude Code plugin (optional)

```
claude plugin marketplace add <owner>/<repo>
claude plugin install a@a-workflow
```

Plugin commands are namespaced by Claude Code: `/a:A.plan` instead of `/A.plan`. Use B or C for bare `/A.*` names.

## Then

1. Start a **new chat** (hosts load commands at startup; in VS Code, Reload Window also works).
2. Run `/A.init`. Answer its questions: your project's areas, where docs should live, date format if you have one.
3. Run `/A.help` to confirm the commands resolve.

## Verify

- `/A.help` prints the command table.
- `.a/project.md` exists and its paths point where you expect.
- The board file the config names exists with your areas.
- `CLAUDE.md` / `.github/copilot-instructions.md` contain the block between `A-skill: begin` and `A-skill: end`.

## Command names on your host

Both hosts derive the command from the file name, so `A.plan.md` → `/A.plan`. If your host lowercases command names, type `/a.plan`; the files still resolve. If a host rejects the dot, rename the wrapper files to `A-plan.md` (and the prompt files likewise); nothing else references the wrapper names.

## Install test protocol

Run once per host when adopting or upgrading, in a scratch copy of a real project. Record in `tests/results/<version>-<host>.md`.

1. Fresh clone; install by the agent sentence (A) in one host and by script (B) in the other; note the time to a working `/A.help`.
2. Casing and dots: does `/A.plan` autocomplete as typed, as `/a.plan`, or not at all? If not at all, apply the rename in "Command names on your host" and note it.
3. `/A.init` on a non-empty repo: did it find existing docs and point at them? Were its questions clear to someone who has not read this repo? Did it offer `/A.map`?
4. Run `tests/01` and `tests/05`. Then run the isolation probe (`.a/skills/core/references/hosts.md`) and record its result.
5. File what failed as issues on this repository with the host, version and transcript excerpt.

## Upgrade

Re-run the install script from a fresh clone. Compare `.a/VERSION` before and after. Read `CHANGELOG.md` for config keys added; `/A.init` will propose new keys and write nothing without you.

## Uninstall

Delete `.a/`, `.claude/commands/A.*.md`, `.github/prompts/A.*.prompt.md`, and the block between the `A-skill` markers in your instruction files. Your documentation and board stay; they are yours.
