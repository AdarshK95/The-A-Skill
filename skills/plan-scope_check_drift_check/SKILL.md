---
name: plan-scope_check_drift_check
description: Scope check and drift check on the current feature — has the work outgrown its type; has the plan drifted from the ask; has the code drifted from the plan.
disable-model-invocation: true
---

# /A.plan.scope_check_drift_check — scope check / drift check

**Place in the flow:** plan stage; runs on the current feature at any time; produces a verdict and, where scope changed, a promotion or demotion as a decision for the user. See `../core/references/flow.md`.

**It also runs on its own, always:** before every plan is shown and after every build, at every tier (`../core/references/lean.md › The two mandatory checks`), and ends with its one line in the header and in chat — `Scope check: clean`, or what it found.

Subject resolution as the spine's Start step 0 (this chat first). Then four checks, each answered with evidence and reported in decision shape where a change is proposed:

1. **Scope — is the type still right?** Recompute the sizing signals (`../core/references/sizing.md`) over what the feature now touches: elements, callers outside the file, contract changes, cache/permission/concurrency paths, modules crossed, new subsystem. Apply the type rule (`../core/references/hierarchy.md`): a *fix* touching more than one element, changing a contract, or needing its own item list is feature-sized; a *feature* that collapsed to one step is an item of an existing feature. Propose promotion or demotion — never silently; the user decides.
2. **Drift — plan versus the user's instructions.** Read `## Instructions` line by line. For each instruction in force: honoured (where), deviation (what the plan does instead), or impossible as stated. Then: what exists in the plan that no instruction asked for; what an instruction asked for that the plan dropped. Every deviation is a decision to the user, never a note.
3. **Drift — code versus plan.** For the files the plan names, compare their current state with the plan's description: built as planned / built differently / not built / changed by someone else since. Cite `path:symbol`.
4. **Out of scope — whose is it.** Everything the plan proposes or the build touched, fixed or found: is it *ours* (this work added or broke it), *exposed* (older, untouched, but an instruction cannot be true without it) or *pre-existing* (`../core/references/flow.md › Whose finding is it`)? Pre-existing items leave the plan and the fix list and go to the board for later; an exposed item outside what this work touches is a decision for the user. What nobody asked for is named, with the same three choices: remove it, get it approved, or move it to later.

Report: four short sections, findings with the structured shape (`goldfish-lenses.md`), then the decisions (promote / demote / revise plan / accept drift) with context, options and a suggested answer. Nothing is changed by this command except on the user's yes; a promotion or demotion is then recorded (`hierarchy.md`).
