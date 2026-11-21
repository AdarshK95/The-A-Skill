---
name: skill-help
description: Show the command list and the workflow.
disable-model-invocation: true
---

# /A.help · /A.skill.help

The two names are the same command.

Show `.a/registry.md` as it stands — commands grouped by stage (plan, review, build, verify, close, project, skill), one line each. Then, in one line each: whether this project is set up (`.a/project.md` present); how many features are in progress (from the board); the one command the user most likely wants next.

Then a **Pages** block for this project, every value checked now, never remembered: run `<method>/templates/pages/page_build.py --root <project> --status` (prints the address and whether the server answers; changes nothing) and show both; `/A.show` to open it live; the stop command with the real paths (`... --stop`); the `pages_server` value in force and where it is set (`.a/project.md` wins over `~/.a/settings.md`). Python missing → say so instead. No project → only "`/A.show` opens a project's pages once a project exists".
