# Review lenses

Each lens is a prompt for a reviewer that has **not** seen the working conversation. Give it: the activity file (at least the `## Report` section), the project files the report cites, and the constitution. Nothing else. It reads, it reports, it changes nothing.

The reviewer returns findings as a list, each tagged **Blocker** (the plan cannot proceed as written), **Major** (must be addressed or explicitly accepted), or **Nit**. A finding names the exact text or file it is about. A reviewer that cannot read a file it needs returns `INCOMPLETE: <file>` instead of a verdict.

Spawn one fresh subagent per lens where the host allows. Otherwise run the lens yourself, with its prompt verbatim, and label the output `cold self-review`.

Shared preamble for every lens:

> You are reviewing a plan you did not write, for a codebase you are seeing for the first time. You have the plan, the files it cites, and the project's standing rules. Read everything you were given before writing. Report only what you can point at in those files. Tag each finding Blocker, Major or Nit. Do not propose rewrites; name the gap.

## zoom-out

> Judge the framing, not the detail. Is the problem stated so that you could explain it to a stranger? Does the plan solve that problem or a neighbouring one? Does anything in the cited code already do what the plan proposes to build? Which parts exist for a need the plan does not evidence? Which infrastructure is introduced ahead of a demonstrated need? Report each as a finding; a speculative feature is a Major.

When run a second time (XL, after fixes): "Review only what was added or changed since the previous zoom-out report, which you also have. Re-flag nothing already accepted there. Look for complexity the fixes introduced."

## comprehension

> First write a paraphrase of the plan in your own words: what exists today, what will change, and why. Then list every term, component or behaviour the plan uses without defining, that you could not resolve from the cited files. A plan you cannot paraphrase is a Blocker; an undefined term is a Major.

A comprehension finding is never contested by the author: if a cold reader could not follow it, the plan is missing context.

## critic

> Assume the plan is wrong and find where. Which assumptions does it make about the code that the cited files do not support? Where is the single point of failure? Which error path, empty state, concurrent access or stale data case is unhandled? What happens when the step before this one fails? Each unsupported assumption is a Major; an unhandled path that loses data or serves a wrong answer is a Blocker.

## implementation-readiness

> Could an engineer who has only this plan and the codebase build it with no further decisions? Check: every file to change is named; every new or changed function has its signature; every data shape is spelled out; every dependency is named and already present or explicitly added; the order of changes is stated where it matters. Each decision left to the implementer is a Blocker.

## codebase-details

> Check the plan against the code it cites, line by line. Where does the plan describe the code incorrectly? Where does it call a function that does not exist, with a shape it does not accept, or from a place that cannot reach it? Where does it ignore a caller, consumer or sibling path that the code shows? A contradiction between plan and code is a Blocker.

## lean

> Find what the plan builds that the codebase already has, and what it builds that it should not. For every new symbol, route, query or helper: search the code for an existing one with the same purpose and name it if found. Flag any second path to a thing an existing path reaches, any literal that should be configuration, any abstraction with a single implementation, any dependency added for something a few lines or the standard library would do. A duplicate of an existing capability is a Blocker; a hardcoded varying value or a one-implementation abstraction is a Major.

## impact

> The plan says what it changes. You find what else changes with it. For every modified function: list its callers from the code and say whether the plan accounts for each. For every changed contract or stored shape: who reads it, and what happens to data already written. For every cache, permission or ordering path touched: how it could now serve a stale or wrong result. For a bug fix: does the fix remove the cause, or move it? An unaccounted caller or consumer is a Major; a fix that moves the cause is a Blocker.

## Rounds (L and XL)

A **round** is one run of the tier's lenses on the current report. After resolving its findings, run the next round. A round is **clean** when no Blocker or Major is unresolved (contested or declined with the user's agreement counts as resolved). Stop at **two consecutive clean rounds**, or at **five rounds**, or on **churn** — a fix from a previous round is itself flagged, and reverting it would resolve the new finding. At five rounds or on churn, the user chooses: accept the residual findings as recorded trade-offs, run another round, or return to Report. Fresh reviewers sample differently each round, which is why one clean round is not enough and zero findings is not the target.
