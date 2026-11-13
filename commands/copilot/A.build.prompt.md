---
mode: agent
description: Alias of /A.implement.
---

Run the `/A.build` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/core/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. Run the Implement stage of the spine. Requires `Phase: Approved`; otherwise say what stage the feature is at.

The user's request, if any, follows this prompt.
