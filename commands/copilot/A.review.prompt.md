---
mode: agent
description: Triage comments from a reviewer or tool, or run a fresh-eyes review of the current plan or build.
---

Run the `/A.review` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/review/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. With pasted comments or a link: run the review entry type (`{{SKILLS_ROOT}}/review/SKILL.md`). With nothing: run the Review stage of the spine on the current feature's current artifact and return to the active stage.

The user's request, if any, follows this prompt.
