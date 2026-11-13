---
mode: agent
description: Behaviour-preserving simplification of recently modified code: duplicates, dead code, nesting, hardcoded values.
---

Run the `/A.simplify` command of The A Skill.

1. Read `{{SKILLS_ROOT}}/simplify/SKILL.md` and follow it. It will send you to `{{SKILLS_ROOT}}/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.start-project` and stop.
3. Do only what the skill says for this command; stop at every gate the spine defines.

The user's request, if any, follows this prompt.
