# Clarify — what becomes a question, how it is shown, and the requirements checklist

The one place that says what is asked, what is decided for the user, and the shape both take. Every stage that puts a choice in front of the user uses it: Clarify, the gate, a fork mid-build, a review escalation, a build finding. "Decision shape" anywhere in the skill means the block below.

## Where to look for open points

Scan the ask against each category; mark a `[NEEDS CLARIFICATION]` where the category bears on this work.

| Category | Ask yourself |
| --- | --- |
| Scope boundary | What is in and out? What nearby thing will the user assume is included? |
| Actors and permissions | Who triggers this, who is allowed to, who sees the result? |
| Data shape and lifetime | What is stored, in what shape, for how long; what about data that already exists? |
| States and transitions | What states can this be in; what moves it between them; what happens mid-transition? |
| Failure and empty cases | No rows, bad input, timeout, partial write, second attempt? |
| Non-functional limits | Volume, latency, retention, cost — is there a number that matters? |
| Integration points | What else calls this or is called by it; what contract must not change? |

## The filter — a question, decided for you, or neither

Every open point goes through these lines in order; the first that fits decides.

**Never a question**

1. The user already answered it: in the request, an earlier answer, the instructions ledger or the decisions log. Use that answer.
2. The agent can find it out: from the code, the docs, a command it may run, a quick trial. Find it out.

**Always a question**

3. Doing it would go beyond the task the user set.
4. It touches a file outside `code_scope`.
5. It builds something new where something already exists, or replaces or drops an existing part.
6. It is a significant change: it touches many places, or undoing it later would take real effort.

**In between**

7. The options differ in something the user would notice (what they see, days of work, cost, risk) and nothing points to one of them (the code, the constitution, a logged decision, the user's stated theme): a question.
8. Otherwise it is **decided for you**: the agent chooses and records the choice as a block. Only a choice that had a real alternative is recorded; routine coding choices are not.

There is no cap on the number of questions.

## Rounds

Ask in rounds. A round holds every question that can be answered now; a question whose answer depends on another still open waits for the next round. A round is shown as:

- once, above: where we are — what the user set out to do, what has happened since, why choices are needed now;
- the questions as numbered full blocks, the one with the most riding on it first;
- then **Decided for you**: the choices made since the last round, as full blocks;
- once, below: what happens after the answers, and "Say **go** to take all suggested answers, or change any by number."

Design nothing on top of an open question that would change the design. The user may say **"decide the rest"** at any time: every open question takes its suggested answer, recorded as their word.

## More than five: stop and split

More than five questions in one round is a signal, never a limit: the work is too big or the ask is unclear, and that is where assumptions, over-building and drift start. Before asking any of them, say which it is and act on it:

- **The ask is unclear.** Ask only the questions the others depend on, usually one or two. Their answers settle or remove most of the rest.
- **The work is big.** Propose splitting it into smaller pieces (items, or features of their own, `hierarchy.md`), each planned on its own. Ask what the first piece needs; a later piece's questions are asked when its turn comes.

A piece that still needs more than five after this asks them, and says in one line why.

## The block — one shape for a question and for a choice made for the user

```
### Q3 · 13 Nov 26, 04:22 PM · open
**Question:** <one sentence the user can answer without opening a file>
**What this is about:** <the part of the product or of the work, named as the user names it; where they would meet it>
**Why it comes up:** <what was found or what happened that makes this a choice now>
**Options:**
- <option> — <what you would see, what it costs in time, what could go wrong>
- <option> — <the same for this one>
**Suggested:** <option> — <the reason>
**To change it later:** <small | significant> — <what undoing it would involve>
**Answer:** "<the user's answer, in their words>" · <adds I3 | changes I1 | no change to the ask>
```

A choice made for the user has the state `decided` and, in place of *Suggested* and *Answer*:

```
**Decided:** <what was chosen> — <the reason>
**What it changes for you:** <what you will see or get, what it costs, what it rules out>
```

The state in the heading is `open`, `answered`, `parked` or `decided`. Each decided block also gets its one dated line in the user summary's *Decided without you* trail, naming the block.

- **Shown in full, in chat and in the file.** A block is never cut to one line per decision and never left in the document for the user to go and read. Length limits on chat replies do not apply to blocks.
- **Stands alone.** Someone who has not opened a file and does not remember the last hour can answer from the block. *What this is about* and *Why it comes up* are each a full sentence or more.
- **In the user's words.** Every line starts from what the user does, sees or gets, never from the system's parts. A term the user has not used is replaced by what it does. No codes (D3, option B, step 7b) and no setting, function or file names unless the user used them first.
- **Every option carries its consequence**, and an open question has at least two options.
- **When the user asks what a block means**, answer in the same slots, fuller, and correct the stored block.
- **The page build checks open and decided blocks** (`logging.md › The pages`): a missing slot, a too-short *about* or *why*, an option with no consequence, a code, a code name the user never used. Each is printed as `WARN` and fixed before the turn ends.

## The record

`## Clarifications` is the third section of the feature's main file, after the user summary and the instructions; the page shows it as *Questions and answers*, open ones first. A block is written when the question is asked or the choice is made, and completed the moment the answer arrives.

- Every question counts, at every stage. A question asked in chat and never written here was, for every later reader, never asked.
- The answer is quoted, never paraphrased or tidied. An answer that changes what is to be built is **also** appended to `## Instructions` as its own line; the block's Answer line points at it.
- When the user picks an option or says "go" to suggested answers, the Answer records what was chosen in the words shown to them: `"go" (took: <the option>)`. A yes to a deviation put to them as a block is the user's word that the earlier instruction is replaced: the new instruction is added and the earlier one marked `superseded by I-n`.
- A question the user did not answer, or parked, keeps its block with the state `open` or `parked` and, for a parked one, the reason as its Answer.
- A choice that is in no block and that the build nevertheless made is what the build review reports as *decided without you* (`build-review.md`).

The plan review and the build review both read this section with the instructions; it is how a reviewer tells what the user meant from what the plan says they meant.

## Requirements checklist (L and XL)

After Clarify, write `## Requirements` in the activity file: one checkable line per requirement, in the user's terms, phrased so that Validate can tick it.

```
- [ ] R1 An export with no matching rows returns an empty file with headers, not an error
- [ ] R2 Export respects the date filter shown on screen
```

Validate ticks each with the evidence that satisfied it. An unticked requirement at Validate is a Blocker. Tiers S and M may skip this; the step done-conditions carry the check.
