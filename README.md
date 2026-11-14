# The A Skill

A development method for coding agents, as `/A.*` commands. Plan, extend, fix and review with a gate before every build; a project board that always knows where you left off; plain-English reporting; logs that live in your repo, not in any one agent's memory. Works in **Claude Code** and **GitHub Copilot in VS Code** from one install.

The A Skill gives a coding agent a working method instead of a prompt. You describe what you want; it reads the code and cites it, reports in plain English, waits for your approval, builds exactly what was approved, checks its own work for duplication and creep, verifies with evidence, and logs everything into your project's own files. A project board shows what is planned, in progress, finished and deferred, with a pointer to the exact step each piece of work stopped at, so "where were we?" has a one-file answer. Review scales with risk: a small fix gets none, a change to shared code gets fresh-eyes reviewers first. Several chats can work the same repo at once through a small shared folder. Nothing in it is specific to any project; your paths and rules live in one config file.

## Before you install

This is a personal, experimental project, shared as is. Your agent acts on these instructions under your account; you stay in control through its permission prompts and this workflow's approval gates. Please read [DISCLAIMER.md](DISCLAIMER.md) (two minutes, plain English) and [SECURITY.md](SECURITY.md) (what it can and cannot touch) before installing.

## 60-second start

1. Install once on your machine (pick one):
   - Ask your agent: *"Install https://github.com/AdarshK95/The-A-Skill following its SETUP.md"*
   - Or: `git clone https://github.com/AdarshK95/The-A-Skill /tmp/the-a-skill && sh /tmp/the-a-skill/install.sh` (PowerShell: `.\install.ps1`)
2. In the folder you want to work in, start a new chat and run `/A.project.start`. It asks a few questions and gives that folder its own memory: config, docs, board. Do this once per project; projects never mix.
3. Describe what you want, or run `/A.plan <idea>`. You get a report to approve before anything is built.
4. Any morning: `/A.project.status` → "where were we?" answered from the files. `/A.project.list` → every project on the machine and how they connect.

## What you get

| | |
| --- | --- |
| **Auto mode** | No command needed. Say what you want; it picks plan / extend / bugfix / review, stays in the current stage, and stops at every approval. |
| **One workflow** | Read → Evaluate → Clarify → Report → Review → Approve → Implement → Realign → Validate → Close. Each stage is a command. |
| **Root cause first** | A wrong behaviour is diagnosed before it is planned: parallel passes to the origin, a coverage check, a confirming test. A cause, never a symptom treatment. |
| **Gate** | Nothing is built until you approve a report that cites the code it describes. |
| **Project board** | Planned · In progress · Finished · Deferred · To do, per area, plus an overview diagram coloured by state. |
| **Exact resume** | Every feature carries a pointer to the step it stopped at and the next concrete action. |
| **Review that scales** | Small change, no ceremony. Shared callers or a contract change: fresh-eyes reviewers on the plan first. |
| **Logs you own** | A plain-language summary for you and a timed, append-only event log for the agent, per feature; decisions with reasons; lessons from drift — all in your project's files, readable by any agent. |
| **Lean by construction** | Searches for what already exists before proposing anything new; one path per purpose; nothing varying hardcoded; a behaviour-preserving simplify pass before close. |
| **Many projects, one install** | Install once; `/A.project.start` gives each folder its own memory. Projects that work together declare it in their config; `/A.project.list` shows the map. Undeclared means independent. |
| **Parallel sessions** | Several agents on one project coordinate through a small shared folder: claim before editing, hand off instead of merging, pick up where another left off. Empty folder means nothing in flight. |
| **Talks like a person** | Five-line progress updates you can stop; reports that say what it means; every answer ends with Done / Not done / Your next step; code paths only when you ask. |
| **Stays true** | `/A.project.map` learns an existing codebase; `/A.project.drift` finds where docs and code diverged; the first review proves its reviewers are really fresh. |

## Commands

See [registry.md](registry.md) — also shown by `/A.help`.

## Documentation

Repository: https://github.com/AdarshK95/The-A-Skill · Issues and install reports: https://github.com/AdarshK95/The-A-Skill/issues


- [SETUP.md](SETUP.md) — install, by agent or by hand, per host; verify; uninstall
- [USAGE.md](USAGE.md) — how to work with it day to day, with examples
- [sources.md](sources.md) — the ideas this method builds on and where they came from
- [SECURITY.md](SECURITY.md) — what the skill can touch, known risks, how to report
- [DISCLAIMER.md](DISCLAIMER.md) — terms of use in plain English
- [CHANGELOG.md](CHANGELOG.md)

## Layout

```
skills/          the method: core spine, auto mode, entry types, housekeeping commands
commands/        thin per-host wrappers (claude/, copilot/) that point at the skills
templates/       what /A.project.start creates in a project: config, board, docs, always-on block
registry.md      the command list /A.help shows
install.sh / install.ps1 / uninstall.sh / uninstall.ps1
```

MIT licence.
