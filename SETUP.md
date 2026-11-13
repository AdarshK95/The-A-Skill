# Setup

Before installing, read `DISCLAIMER.md` and `SECURITY.md`. The installer is a short script; read it too.

For a person, or for an agent asked to "install this repo into my project". Steps are the same.

## How it is laid out

**Install once per machine. Start projects per folder.**

| Where | What | Why |
| --- | --- | --- |
| `~/.a/skills/`, `~/.a/templates/`, `~/.a/registry.md`, `~/.a/VERSION`, `~/.a/SOURCE` | The method, templates, command list, version, origin | One copy; `/A.skill-update` keeps it current |
| `~/.a/projects.md` | Index of every project on this machine and their dependencies | `/A.projects`; read at the start of every piece of work |
| `~/.claude/commands/A.*.md` | One file per command | Claude Code shows `/A.plan`, `/A.bugfix`, … in every folder |
| `~/.a/commands/copilot/A.*.prompt.md` | One file per command | Copilot in VS Code, after adding that folder to `chat.promptFilesLocations` |
| **Inside each project:** `.a/project.md`, the docs it names, the board, `.a/shared/`, the always-on block in `CLAUDE.md` / `AGENTS.md` / `.github/copilot-instructions.md` | That project's memory | Created by `/A.start-project`, never by the installer |

Project-level install (`install.sh --project DIR` / `install.ps1 -Project DIR`) puts the method and commands inside one repository instead, for teams that want it to travel with the code. Not both for the same folder.

## Install

### A — ask your agent

In any chat:

> Install https://github.com/AdarshK95/The-A-Skill following its SETUP.md. Clone it to a temporary folder, run its install script (global, the default), then tell me what was installed. Do not run /A.start-project; I will.

### B — script

```sh
git clone https://github.com/AdarshK95/The-A-Skill /tmp/the-a-skill
sh /tmp/the-a-skill/install.sh
```

PowerShell:

```powershell
git clone https://github.com/AdarshK95/The-A-Skill $env:TEMP\the-a-skill
powershell -ExecutionPolicy Bypass -File "$env:TEMP\the-a-skill\install.ps1"
```

Windows blocks unsigned scripts by default ("not digitally signed"). `-ExecutionPolicy Bypass -File …` allows that one run only; or `Set-ExecutionPolicy -Scope Process Bypass` allows the current window. Neither changes your machine's policy.

On a **managed machine** (work laptop) the policy is set by Group Policy and even `Bypass` is refused. Then run the script as text, from inside the cloned folder:

```powershell
cd $env:TEMP\the-a-skill
& ([scriptblock]::Create((Get-Content .\install.ps1 -Raw)))
& ([scriptblock]::Create((Get-Content .\uninstall.ps1 -Raw))) -Project D:\path\to\project -Yes   # uninstall, same way
```

The policy governs script files, not script blocks. Or use Git Bash with the `.sh` scripts: `sh install.sh`.

Re-running updates the method and the commands. It never touches any project's `.a/project.md` or documents.

### C — by hand

Copy `skills/` → `~/.a/skills/`, `templates/` → `~/.a/templates/`, `registry.md` and `VERSION` → `~/.a/`, `templates/projects.md` → `~/.a/projects.md`, `commands/claude/*` → `~/.claude/commands/`, `commands/copilot/*` → `~/.a/commands/copilot/`. In every copied command file replace `{{SKILLS_ROOT}}` with the full path of `~/.a/skills`.

### D — Claude Code plugin (optional)

```
claude plugin marketplace add AdarshK95/The-A-Skill
claude plugin install a@the-a-skill
```

Plugin commands are namespaced by Claude Code: `/a:A.plan` instead of `/A.plan`. Use B or C for bare `/A.*` names.

## Then

1. **Copilot in VS Code only:** Settings → search `promptFilesLocations` → add the Copilot commands folder the installer printed (`~/.a/commands/copilot`) → Reload Window. Claude Code needs nothing.
2. Open your workspace as you normally do — a single project, a parent folder holding several, or a multi-root workspace all work. Start a **new chat**.
3. Run `/A.start-project` (or `/A.start-project <folder>` to start a project in a sub-folder of the workspace). It asks about your areas, where docs should live, date format, and whether this project depends on or provides something to another project. It creates only what is missing and registers the project in `~/.a/projects.md`.
4. Run `/A.help` to confirm the commands resolve.
5. Repeat step 3 for every folder you want as a separate project; they can all live in the same workspace. The agent works out which project a message belongs to from the files involved, or asks. One repository with parallel parts (UI, backend, API) is **one** project with areas; separate repositories are separate projects. Full guidance: `skills/core/references/projects.md`.

## Verify

- `/A.help` prints the command table in any folder.
- In a started project: `.a/project.md` exists and its paths point where you expect; the board file exists with your areas; `CLAUDE.md` / `.github/copilot-instructions.md` contain the block between `A-skill: begin` and `A-skill: end`.
- `/A.projects` lists the project.

## Command names on your host

Both hosts derive the command from the file name, so `A.plan.md` → `/A.plan`. If `/A.*` commands do not appear in Copilot after the global install, check the `chat.promptFilesLocations` setting from step 1 and Reload Window. If your host lowercases command names, type `/a.plan`; the files still resolve. If a host rejects the dot, rename the wrapper files to `A-plan.md` (and the prompt files likewise); nothing else references the wrapper names.

## Install test protocol

Run once per host when adopting or upgrading, in a scratch copy of a real project. Record in `tests/results/<version>-<host>.md`.

1. Fresh clone; install by the agent sentence (A) in one host and by script (B) in the other; note the time to a working `/A.help`.
2. Casing and dots: does `/A.plan` autocomplete as typed, as `/a.plan`, or not at all? If not at all, apply the rename in "Command names on your host" and note it.
3. `/A.start-project` on a non-empty repo: did it find existing docs and point at them? Were its questions clear to someone who has not read this repo? Did it offer `/A.map`?
4. Run `tests/01` and `tests/05`. Then run the isolation probe (`.a/skills/core/references/hosts.md`) and record its result.
5. File what failed as issues on this repository with the host, version and transcript excerpt.

## Note for maintainers uploading through the GitHub website

The web uploader takes at most 100 files per commit and refuses files or folders whose name starts with a dot. Upload in batches (root files + `skills` + `templates` + `tests`; then `commands/claude`; then `commands/copilot`), and create `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` with **Add file → Create new file**, typing the folder in the file name. Pushing with git has neither limit.

## Upgrade

In the project, run `/A.skill-update`. It compares `.a/VERSION` with the repository, shows the changelog entries in between, re-runs the installer, and proposes any new config keys without writing them. Or do the same by hand: re-run the install script from a fresh clone and compare `.a/VERSION` before and after.

## Repair

A command fails to load, or a file under `.a/` or the command folders was changed by mistake: run `/A.skill-repair`. It compares the installed files with the release, reports what is missing or altered, and restores only after you confirm. Your config and documents are never touched.

## Uninstall

Run `/A.skill-uninstall`, or the script directly: `powershell -ExecutionPolicy Bypass -File ~/.a/templates/uninstall.ps1 -Yes` (`sh ~/.a/templates/uninstall.sh --yes`; add `-Project <dir>` / `--project <dir>` for a project-level install). Without `-Yes` it only lists what it would remove. It removes exactly what the installer created: the method, templates, registry, version, source note, and the `/A.*` command files. It never touches any project's `.a/project.md`, `.a/shared/`, documentation, board, activity files, decisions, lessons, or `~/.a/projects.md` — that is your work. If you also want the `A-skill` block out of a project's instruction files, `/A.skill-uninstall` offers that as a separate question.

## Git and the documentation

`/A.start-project` adds `.a/` and the documentation paths it created to the project's `.gitignore` in a marked block, so agent metadata and working notes stay out of commits by default. It tells you the exact lines. Remove the block if you want the documentation committed — many teams do, for shared history. Paths already tracked by git are never added.
