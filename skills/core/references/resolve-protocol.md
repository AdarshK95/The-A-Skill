# Resolve protocol

How every finding is answered — from a review lens in Phase 5, or from an external reviewer's comments in `/A.review`. The same four verdicts, the same evidence rule, so the user reads one shape everywhere.

## Verdicts

| Verdict | Meaning | Required with it |
|---|---|---|
| **FIX** | The finding is right; here is the change to the plan or code | The concrete change, and which report section or file it touches |
| **CONTEST** | The finding is wrong | Evidence the reviewer could have read: `path:symbol` or `path:line` that shows it. Without such evidence, the verdict is not available |
| **ESCALATE** | The finding turns on something outside the files — a product decision, a constraint only the user knows, context from a past conversation | The question for the user, in one line |
| **DECLINE** | The finding is right but will not be addressed now | The reason, and where it is recorded: a **deferred decision** (`deferred_decisions_log`) when it does not apply under today's conditions — with the reasoning and the condition that reopens it; the board's Deferred table when it is work to do later; a decision when it changes direction |

A comprehension finding — "I could not follow this" — takes FIX or ESCALATE only. Wanting to contest is not evidence that the reviewer is wrong.

A FIX adds what a *human* reader of the plan needs. Context that only a zero-context reviewer needs — restating what the project already knows everywhere — is not added to the plan to satisfy the reviewer; that finding is ESCALATED or, with the user's agreement, DECLINED with the note that the project's readers have the context. Plans are written for the people who will build and maintain them, not for the reviewers.

## Recording

Under `## Findings` in the activity file, one line per finding:

```
- [Blocker] <source lens or reviewer>: <finding> → FIX: <change>
- [Major] impact: callers of parseRange in report/*.ts unaccounted → CONTEST: all three call through normalizeRange (lib/range.ts:normalizeRange), which the plan changes
- [Nit] style: ... → DECLINE: cosmetic, tracked in open items
```

Every ESCALATE becomes a row in the report's *Decisions needed from you*, in the full shape — what came up and why, the options and what each means, suggested — never a bare question (`communication.md › Decisions arrive with their context`). Every DECLINE of a Blocker or Major becomes an open item in the status header count.

## Settling

A finding that was FIXed is closed. A finding that was CONTESTed or DECLINEd with the user's agreement is settled and stays closed if a later reviewer raises it again; point at the earlier line. A FIXed finding re-opens if a later reviewer finds the fix insufficient.

## External reviewers

Comments from a tool or a colleague who did not see the working context (an automated PR reviewer, for instance) are findings from a cold reader. Treat each one exactly as above. Three outcomes are expected and all are fine: the reviewer caught something real (FIX), the reviewer lacked context the decisions log holds (CONTEST, citing the decision), or the point is known and deliberately deferred (DECLINE, citing where it is tracked).

## Sharing findings

When the user wants to show a review to someone else — a colleague, or the reviewer whose comments were triaged — write `## Findings` as a standalone block: one line per finding with its severity, source, the finding in one sentence, the verdict and its evidence. No internal references; a reader outside the project should follow it.
