---
mode: agent
description: Pick up an interrupted build: read the tracker, verify done steps against the files, continue at the pointer.
---

Run the `/A.build.resume` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/build/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
   Run the `/A.build.resume` section of that file: read the tracker, verify done steps against the files, announce, then continue at the pointer.
2. Resolve the project as the spine's Start says — the one the user named, else the one containing the files involved, else the one this conversation is already in, else the only folder in the workspace that holds a `.a/project.md` (sub-folders count), else ask which. Read that project's `.a/project.md`. Only if no folder anywhere in the workspace holds one, say so and offer `/A.project.start` — and offer to proceed without the workflow if the user prefers.
3. Do only what the skill says for this command; stop at every gate the spine defines.

The user's request, if any, follows this prompt.
