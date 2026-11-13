---
description: Triage comments from a reviewer or tool, or run a fresh-eyes review of the current plan or build.
argument-hint: <pasted comments or PR link, or empty>
---

Run the `/A.review` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/review/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Resolve the project as the spine's Start says — the one the user named, else the one containing the files involved, else the one this conversation is already in, else the only folder in the workspace that holds a `.a/project.md` (sub-folders count), else ask which. Read that project's `.a/project.md`. Only if no folder anywhere in the workspace holds one, say so and offer `/A.start-project` — and offer to proceed without the workflow if the user prefers.
3. With pasted comments or a link: run the review entry type (`{{SKILLS_ROOT}}/review/SKILL.md`). With nothing: run the Review stage of the spine on the current feature's current artifact and return to the active stage.

User's request: $ARGUMENTS
