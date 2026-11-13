---
description: Check for a newer release of The A Skill itself and, after you confirm, install it. Not a project command.
---

Run the `/A.skill-update` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/skill-update/SKILL.md` and follow it exactly. Its first step ends with a question to the user; ask it and stop. Take no action until the user answers yes.
2. `.a/project.md` is not needed for this command and is never written by it.
3. This command is about The A Skill's own files, not the user's project code.

User's request: $ARGUMENTS
