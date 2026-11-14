---
description: Show the commands by stage.
---

Run the `/A.skill.help` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/skill-help/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
   Its first step ends with a question to the user; ask it and stop. Take no action until the user answers yes.
2. `.a/project.md` is not needed for this command.
3. Do only what the skill says for this command; stop at every gate the spine defines.

User's request: $ARGUMENTS
