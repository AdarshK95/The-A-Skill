---
description: Something is broken: trace to root cause, fix at the root, analyze fix impact, then fix.
argument-hint: <what broke>
---

Run the `/A.bugfix` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/bugfix/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. Do only what the skill says for this command; stop at every gate the spine defines.

User's request: $ARGUMENTS
