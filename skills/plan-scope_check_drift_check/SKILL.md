---
name: plan-scope_check_drift_check
description: Scope check and drift check on the current feature — has the work outgrown its type; has the plan drifted from the ask; has the code drifted from the plan.
disable-model-invocation: true
---

# /A.plan.scope_check_drift_check — scope check / drift check

**Place in the flow:** plan stage; runs on the current feature at any time; produces a verdict and, where scope changed, a promotion or demotion as a decision for the user. See `../core/references/flow.md`.

Subject resolution as the spine's Start step 0 (this chat first). Then three checks, each answered with evidence and reported in decision shape where a change is proposed:

1. **Scope — is the type still right?** Recompute the sizing signals (`../core/references/sizing.md`) over what the feature now touches: elements, callers outside the file, contract changes, cache/permission/concurrency paths, modules crossed, new subsystem. Apply the type rule (`../core/references/hierarchy.md`): a *fix* touching more than one element, changing a contract, or needing its own item list is feature-sized; a *feature* that collapsed to one step is an item of an existing feature. Propose promotion or demotion — never silently; the user decides.
2. **Drift — plan versus ask.** Re-read `What was asked` and the approved steps. What exists in the plan that the ask does not need; what the ask needs that the plan dropped; which decisions since changed the ask. Each as a finding.
3. **Drift — code versus plan.** For the files the plan names, compare their current state with the plan's description: built as planned / built differently / not built / changed by someone else since. Cite `path:symbol`.

Report: three short sections, findings with the structured shape (`goldfish-lenses.md`), then the decisions (promote / demote / revise plan / accept drift) with context, options and a suggested answer. Nothing is changed by this command except on the user's yes; a promotion or demotion is then recorded (`hierarchy.md`).
