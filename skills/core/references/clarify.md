# Clarify — finding the questions, and the requirements checklist

## The seven categories

Scan the ask against each; raise a `[NEEDS CLARIFICATION]` only where the category is relevant to this work **and** the ask, the code and the decisions log do not answer it.

| Category | Ask yourself |
| --- | --- |
| Scope boundary | What is in and out? What nearby thing will the user assume is included? |
| Actors and permissions | Who triggers this, who is allowed to, who sees the result? |
| Data shape and lifetime | What is stored, in what shape, for how long; what about data that already exists? |
| States and transitions | What states can this be in; what moves it between them; what happens mid-transition? |
| Failure and empty cases | No rows, bad input, timeout, partial write, second attempt? |
| Non-functional limits | Volume, latency, retention, cost — is there a number that matters? |
| Integration points | What else calls this or is called by it; what contract must not change? |

At most five questions, one at a time, each answerable in a line, most consequential first. Everything else relevant but unasked is written in the report as **Assumptions**, one line each, so the user can object. A parked question is `parked: <reason>`.

## Requirements checklist (L and XL)

After Clarify, write `## Requirements` in the activity file: one checkable line per requirement, in the user's terms, phrased so that Validate can tick it.

```
- [ ] R1 An export with no matching rows returns an empty file with headers, not an error
- [ ] R2 Export respects the date filter shown on screen
```

Validate ticks each with the evidence that satisfied it. An unticked requirement at Validate is a Blocker. Tiers S and M may skip this; the step done-conditions carry the check.
