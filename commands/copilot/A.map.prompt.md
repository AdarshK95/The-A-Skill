---
mode: agent
description: Map an existing codebase: a short contract per directory and the overview's first nodes.
---

Run the `/A.map` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/map/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. Do only what the skill says for this command; stop at every gate the spine defines.

The user's request, if any, follows this prompt.
