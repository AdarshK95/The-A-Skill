# Report schema

One report format for every type. The user reads the same headings whether the work is a new feature or a one-line fix, so they know where to look. Sections marked *(if relevant)* are omitted when they would say nothing.

Write it under `## Report` in the activity file. Every statement about the code carries a `path:symbol` citation.

```markdown
## Report

### What was asked
One or two sentences, in your words. Where the request was ambiguous, the reading you took and why.

### What exists today
The current state of the code the request touches: structure, flow, data shapes, the callers involved. Citations on every line.
[extend] Where the implementation has drifted from its design document or from the decisions log, and which side is right.
[bugfix] How the bug reproduces, and the trace from symptom to origin: each hop cited.

### Assessment
Whether the request is sound as stated, what the code already supports, what it does not, and anything the constitution or a logged decision says about it.
[bugfix] The root cause, stated in one sentence, and why that and not the nearer symptom.
[review] For each reviewer comment: correct / incorrect / known and deferred — with the evidence for each verdict.

### Reuse candidates
The reuse search (`lean.md`): one row per new need — candidate `path:symbol`, match (exact / close / pattern / none), decision. Never empty: a need with no candidate says so and why.

### Proposed change
What will be modified, file by file, and how. The rung of the ladder each change sits on. For a choice the user must make: the options, the trade-offs, and one line on which way you lean and why; the alternatives stay visible.

### Impact
What else this change touches: callers, consumers, data already stored, caches, permissions, concurrent paths. For each: handled how, or accepted as a risk and why. What could break if this is wrong.

### Verification
How you will prove the change works and that nothing planned was missed: the checks to run, the one check you will leave behind if none exists.

### After the change *(if relevant)*
What the user or end user will see or experience afterwards, as a reference for judging the result. Included when the change is user-visible or when the report's correctness depends on it.

### Tier
`S | M | L | XL` with the signals that chose it, one per line, each naming its file or decision.

### Decisions needed from you
Numbered. Each one a single question the user can answer in a line.
```

## Chat version

Per `communication.md`: what this means for the user; what was found, in plain words; what they must decide (the *Decisions needed* list, each in a line); what happens next. The tier in one phrase ("small change, no extra review" / "touches shared code, I'll have it reviewed first"). No path or symbol unless asked; point to the activity file for the detail. One screen at most.

## Revising

A revised report is appended under `## Report` with a dated heading (`### Revision — 13 Nov 26, 05:10 PM`); earlier versions stay above it, unchanged. The event log records why.
