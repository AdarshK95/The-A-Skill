---
description: Continue a closed feature as a new one.
argument-hint: <feature number or file>
---

Run the `/A.reopen` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/extend/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. This is /A.extend pointed at a closed feature: the new feature gets `Continues:` and the old file is not edited.

User's request: $ARGUMENTS
