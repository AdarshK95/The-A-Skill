---
description: Triage comments from a reviewer or tool, or run a fresh-eyes review of the current plan or build.
argument-hint: <pasted comments or PR link, or empty>
---

Run the `/A.review` command of The A Skill.

1. Read `.a/skills/review/SKILL.md` and follow it. It will send you to `.a/skills/core/SKILL.md` for the shared spine and its `references/`.
2. Read `.a/project.md` for this project's paths and rules. If it is missing, tell the user to run `/A.init` and stop.
3. With pasted comments or a link: run the review entry type (`.a/skills/review/SKILL.md`). With nothing: run the Review stage of the spine on the current feature's current artifact and return to the active stage.

User's request: $ARGUMENTS
