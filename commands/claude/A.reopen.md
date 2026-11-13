---
description: Continue a closed feature as a new one.
argument-hint: <feature number or file>
---

Run the `/A.reopen` command of The A Skill.

1. Resolve the method: if `<workspace root>/.a/mirror/skills/` exists, use it as the skills folder; otherwise use `{{SKILLS_ROOT}}`. Read `<skills folder>/extend/SKILL.md` and follow it. It will send you to `<skills folder>/core/SKILL.md` for the shared spine and its `references/`.
2. Resolve the project as the spine's Start says — the one the user named, else the one containing the files involved, else the one this conversation is already in, else the only folder in the workspace that holds a `.a/project.md` (sub-folders count), else ask which. Read that project's `.a/project.md`. Only if no folder anywhere in the workspace holds one, say so and offer `/A.start-project` — and offer to proceed without the workflow if the user prefers.
3. This is /A.extend pointed at a closed feature: the new feature gets `Continues:` and the old file is not edited.

User's request: $ARGUMENTS
