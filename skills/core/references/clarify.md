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

## The record — every question and answer, in the user's words

`## Clarifications` is the third section of the feature's main file, after the user summary and the instructions, and the page shows it as *Questions and answers*, open ones first. One block per question, written when it is asked and completed the moment the answer arrives:

```
### Q3 · 13 Nov 26, 04:22 PM · open
**Question:** <one sentence a person can answer without opening a file>
**Context:** <what came up, where we are, and why it matters to you — plain words>
**Options:**
- <option> — <what it means for you>
- <option> — <what it means for you>
**Suggested:** <option> — <the reason>
**Answer:** "<the user's answer, in their words>" · <adds I3 | changes I1 | no change to the ask>
```

The state in the heading is `open`, `answered` or `parked`. **A question is not asked until its block has Context, Options and Suggested** — in chat and in the file alike. In two audited sessions the user had to ask "what is the decision needed?" and "didn't understand" eleven times because a question arrived as one line with a recommendation and nothing else; the page marks a block with a missing part in red, and the page build prints it, so it is fixed before the turn ends.

- Every question counts, at every stage: Clarify, a decision at the gate, a fork mid-build, a question in a review. A question asked in chat and never written here was, for every later reader, never asked.
- The answer is quoted, never paraphrased or tidied. An answer that changes what is to be built is **also** appended to `## Instructions` as its own line; the block's Answer line points at it.
- A decision is a question too. When the user picks an option or says "go" to suggested answers, the Answer records what was chosen in the words that were shown to them: `"go" (took: <the option>)`. A yes to a deviation put to them in decision shape is the user's word that the earlier instruction is replaced: the new instruction is added and the earlier one marked `superseded by I-n`. This is how a change of direction agreed mid-way reaches a reviewer as the user's decision instead of looking like a broken instruction.
- A question the user did not answer, or parked, keeps its block, with the state `open` or `parked` and, for a parked one, the reason as its Answer; it is not deleted.
- What the agent settled **without** asking is not here: it is in the report's *Assumptions*, where the user can object. A point that is in neither place and that the build nevertheless decided is what the build review reports as *decided without you* (`build-review.md`).

The plan review and the build review both read this section with the instructions; it is how a reviewer can tell what the user meant from what the plan says they meant.

## Requirements checklist (L and XL)

After Clarify, write `## Requirements` in the activity file: one checkable line per requirement, in the user's terms, phrased so that Validate can tick it.

```
- [ ] R1 An export with no matching rows returns an empty file with headers, not an error
- [ ] R2 Export respects the date filter shown on screen
```

Validate ticks each with the evidence that satisfied it. An unticked requirement at Validate is a Blocker. Tiers S and M may skip this; the step done-conditions carry the check.
