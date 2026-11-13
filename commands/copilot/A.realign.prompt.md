---
mode: agent
description: Check the build against the original ask; remove what crept in; simplify.
---

Run the `/A.realign` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/core/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. Run the Realign stage of the spine now, then return to the active stage.

The user's request, if any, follows this prompt.
