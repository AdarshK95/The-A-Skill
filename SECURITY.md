# Security

What The A Skill can touch, what it cannot, the risks that come with it, and how to report a problem.

## What it is

Markdown instructions that a coding agent follows, plus two installer scripts (`install.sh`, `install.ps1`) that copy those files into a project. There is no compiled code, no service, no background process.

## What it does not do

- No network calls of its own. The only network activity is the installer or `/A.skill-update` cloning this repository, and only when you run them.
- No telemetry, analytics or phone-home.
- No credentials read, stored or transmitted.
- No data leaves your machine because of this skill. Your agent host sends code and text to its model provider as it always does; this skill does not change that.
- It never bypasses or asks the agent to bypass your host's permission prompts.

## Where it does act, through your agent

| Action | When | Your control |
| --- | --- | --- |
| Reads your code and documents | Every command | Host file permissions |
| Writes documentation files (activity files, board, decisions, lessons, shared folder) | Continuously during work | Paths are set in `.a/project.md`; nothing outside them |
| Edits code | Implement stage only, after your approval | The Approve gate; host edit permissions |
| Runs commands | Validate (your project's checks), `/A.map` (listing files), installers, `/A.skill-update` | Host command permissions; each is visible before it runs |
| Fetches from the internet | `/A.skill-update`, `/A.skill-repair` (this repository only) | Both ask before acting |

## Known risks and how to handle them

**Supply chain.** `/A.skill-update` and the installers run a script fetched from this repository. If this repository or my account were compromised, that script could be malicious. Mitigations: the update asks for your confirmation and shows what changed; read `install.sh` / `install.ps1` before running (they are short); pin to a tagged version in regulated environments; `/A.skill-repair` detects files that differ from a release.

**Prompt injection through files the agent reads.** The skill makes the agent read your board, decisions log, lessons log, shared folder, reviewer comments and instruction files. Text in any of them — including text another session or another person wrote — could try to steer the agent. The skill tells the agent to treat all of that as data, never as instructions (`skills/core/SKILL.md`). It is still a surface: review what lands in the shared folder and in review comments as you would any input.

**Agent error.** Wrong analysis, a missed caller, an over-confident "verified". The workflow's gates, citations and runnable checks reduce this; they do not remove it. Nothing is built without your approval; keep it that way.

**Modified copies.** A fork or a hand-edited `.a/skills` file can say anything. Install from this repository, and run `/A.skill-repair` if behaviour looks wrong.

## Scratch and sampled data

When a command samples live data (conversations, records, logs) to answer a question, the copy goes to the project's ignored `.a/tmp/` or the OS temp folder and is deleted before the agent reports — the agent never asks the user to delete it, and never leaves users' data lying in a folder outside the project.

## Secrets

Never put API keys, tokens or passwords in `.a/project.md`, the board, activity files or the shared folder. They are plain text in your repository. The skill never asks for them.

## Reporting

Found something unsafe, or a way the skill could be misused? Open an issue at https://github.com/AdarshK95/The-A-Skill/issues with the host, version (`.a/VERSION`) and what you saw. If it is sensitive, say so in the issue title and I will arrange a private channel. I respond as a volunteer, as time allows.
