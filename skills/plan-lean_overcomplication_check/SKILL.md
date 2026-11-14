---
name: plan-lean_overcomplication_check
description: Is the plan lean? Over-complication, speculative generality, duplication of what exists, reuse missed, hardcoding — checked against the code and the lean rules.
disable-model-invocation: true
---

# /A.plan.lean_overcomplication_check — lean / over-complication check

**Place in the flow:** plan stage; runs on the current plan (or build) at any time; produces findings and simplifications for the user to accept. See `../core/references/flow.md`.

Subject resolution as the spine's Start step 0. Then apply `../core/references/lean.md` to the plan as a reviewer would:

1. **Ladder, per proposed change:** needed at all? already in the codebase (re-run the reuse search over the plan's new symbols, routes, queries, config)? stdlib or platform? installed dependency? one line? — and note where the plan sits above the rung that holds.
2. **Modularity:** a second path to something an existing path reaches; literals that vary; one-implementation abstractions; new files and folders without a reason a reader would accept.
3. **Speculative generality:** infrastructure ahead of evidenced need, settings nobody asked for, states or fields with one user.
4. **Quality verdict:** robust / tactical / quick fix, against what a well-run team would do (`communication.md › Solution-architect judgement`).

Report in plain words first — how much of the plan is doing work the ask needs, and what can go — then the findings in the structured shape with a proposed cut for each, and the decisions (cut / keep with a ceiling comment / keep as is) in decision shape. The plan is edited only on the user's yes, in place before Approve, each change recorded in `## Findings`.
