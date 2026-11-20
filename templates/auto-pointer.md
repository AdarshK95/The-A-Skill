The A Skill is the default workflow on this machine. Method: `{{SKILLS_ROOT}}` (spine: `core/SKILL.md`).
- A message that names no skill and no /command goes through **auto mode**: read `{{SKILLS_ROOT}}/auto/SKILL.md` and follow it. Never handle a request that changes code, settles a decision or keeps analysis as plain chat.
- A typed `/A.*` command runs that command instead. Another skill the user names by name runs as asked.
- Where a `.a/project.md` exists (this folder or a parent), it and the documents it names win over CLAUDE.md, AGENTS.md, `*.instructions.md`, memory files and older rules on where documents go, how work is logged and which workflow runs. Mention a conflicting instruction once; follow the config.
- No `.a/project.md` here: say so in one line and offer `/A.project.start`; until then still follow the stages in chat — understand, plan, stop for approval, build, check.
- Every choice put to the user, or made for them, is shown as the full block in `{{SKILLS_ROOT}}/core/references/clarify.md`, in the user's own words — never a one-line list of decisions.
- Code in any answer follows `{{SKILLS_ROOT}}/core/references/lean.md`: reuse before writing; never cut corners on trust boundaries, data loss or security; mark a deliberate shortcut with its ceiling.
