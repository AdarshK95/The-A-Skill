---
mode: agent
description: Something is broken: trace to root cause, fix at the root, analyze fix impact, then fix.
---

Run the `/A.bugfix` command of The A Skill.

1. Read `.a/skills/bugfix/SKILL.md` and follow it. It will send you to `.a/skills/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.init` and stop.
3. Do only what the skill says for this command; stop at every gate the spine defines.

The user's request, if any, follows this prompt.
