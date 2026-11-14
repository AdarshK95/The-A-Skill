# Review lenses

Each lens is a prompt for a reviewer that has **not** seen the working conversation. Give it: the activity file (at least the `## Report` section), the project files the report cites, and the constitution. Nothing else. It reads, it reports, it changes nothing.

The reviewer returns findings as a list, each tagged **Blocker** (the plan cannot proceed as written), **Major** (must be addressed or explicitly accepted), or **Low** (worth knowing, never worth a discussion), and each with a **confidence** (`high` — pointed at in the files; `medium` — inferred from them; `low` — suspected). Any finding that contradicts the project's constitution is a Blocker regardless of the lens. **"No findings" is a complete and valid review**: a reviewer that found nothing says so in one line and stops; it does not manufacture Lows to have something to say.

Each finding has one shape, so it can be scanned, compared across lenses, and acted on without re-reading the plan:

```
[Blocker|Major|Low · confidence] <one-line summary>
Where: <path:symbol or report section>
Now: <the existing text or code, quoted briefly>
Gap: <what is wrong or missing, as a fact>
```

No proposed rewrite — the author resolves; the reviewer names the gap. A finding names the exact text or file it is about. A reviewer that cannot read a file it needs returns `INCOMPLETE: <file>` instead of a verdict.

The same questions, asked by the implementer of their own work during Implement, are `build-check.md`; this file is the independent version.

Spawn one fresh subagent per lens where the host allows. Otherwise run the lens yourself, with its prompt verbatim, and label the output `cold self-review`.

Shared preamble for every lens:

> You are reviewing a plan you did not write, for a codebase you are seeing for the first time. You have the plan, the files it cites, and the project's standing rules. Read everything you were given before writing. Report only what you can point at in those files. Tag each finding Blocker, Major or Low. Do not propose rewrites; name the gap.

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

## A premise finding stops the round

A `zoom-out` finding that questions the **premise** of the design — "this builds permanent machinery on a path marked temporary", "this solves a neighbouring problem", "the cause is elsewhere" — is not resolved by the author and is not carried into the next lens group. It goes to the user at once, in decision shape (what came up and why, the options and what each means, suggested), and the review pauses until they answer. Detail lenses run on a design whose premise the user has confirmed; running them first spends rounds on text that may be discarded.

## Synthesis before resolution

When a group has more than one lens, merge their findings before resolving: drop duplicates (the same gap found by two lenses is one finding, credited to both), group by the part of the plan they concern, order by severity then confidence. Resolve Blockers and Majors; Lows are applied silently when trivial and otherwise listed, never discussed. Low-confidence findings are verified against the code before they get a verdict, and dropped with one line if the code does not bear them out. This is what keeps a five-lens group from producing twenty threads for the user: the user sees the merged, ordered result — Blockers and Majors only — and the Lows as a count.

## Rounds (L and XL)

A **round** is one complete pass of the tier's lens groups (`sizing.md`) over the current report, with each group's findings resolved before the next group runs. After a round, the report has usually changed. A round is **clean** when no Blocker or Major was raised in it that is still unresolved (contested or declined with the user's agreement counts as resolved). Rounds continue until **two consecutive clean rounds**, or **five rounds**, or **churn** — a fix from a previous round is itself flagged and reverting it would resolve the new finding.

The second and later rounds re-run only the lenses whose area the previous round's fixes touched (a Blocker from `impact` → `impact` and `codebase-details` again on the revised text), not the whole sequence, unless the plan changed materially.

Stopping at the cap or on churn is a **user decision**, not an automatic close: say "five rounds reached; the last round raised <n> Blockers that are now fixed but unreviewed" and let the user choose to accept the residual risk, run once more, or return to Report. A round that ended with new Blockers is never reported as "review complete" without that sentence.

## What a reviewer is told

A reviewer receives the lens prompt with its preamble, the path of the report (and which sections to read), the paths of the files it cites, and the constitution — nothing about the conversation, and **nothing about earlier rounds**: not what was already fixed, not what to avoid re-flagging. Fresh means fresh. The one exception is the additions-only `zoom-out`, whose job is defined relative to the previous zoom-out report and therefore receives that report's path.
