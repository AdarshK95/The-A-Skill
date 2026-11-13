---
name: review
description: Triage comments from an external reviewer (an automated PR reviewer, a colleague) who did not have the working context. Verify each against the code and the decisions log; return a verdict with evidence for each.
disable-model-invocation: true
---

# /A.review — triage reviewer comments

Runs the core spine (`../core/SKILL.md`). This file is its **Evaluate** step.

**Input:** the comments, pasted or as a link to a PR or review the agent can read, and which change they are about (branch, PR, or activity file). Each comment is a finding from a cold reader: it may be right, it may lack context, or it may be known and deferred. All three are expected.

## Evaluate

After Read has traced the code each comment points at:

1. **Split.** One entry per distinct comment, numbered, with the reviewer's words quoted briefly and the file and line they refer to.
2. **Verify each.** Read the code the comment is about and decide whether its claim is true as stated. Search the decisions log and the originating activity file for context the reviewer did not have.
3. **Verdict each**, per `../core/references/resolve-protocol.md`:
   - **FIX** — the comment is right; the proposed change, and its own fix-impact line.
   - **CONTEST** — the comment is wrong; the `path:symbol` evidence that shows it.
   - **DECLINE** — right, but known and deferred; the decision or open item where it is tracked. With no such record, it is not yet deferrable: offer the user FIX or a new Deferred entry.
   - **ESCALATE** — turns on something only the user knows; the one-line question.
4. **Group.** FIXes that touch the same code become one step. Steps get done-conditions and files.
5. **Impact of the fixes together**, and verification.
6. **Tier** from `../core/references/sizing.md`, computed on the FIX set only.

## Report notes

Use the `[review]` lines of the schema. *Assessment* is the numbered verdict list; *Proposed change* is the FIX steps; *Decisions needed* carries every ESCALATE and every DECLINE without a record. *After the change* is included when a FIX is user-visible.

## Park it

If the user asks for the analysis only ("check these and keep it for later"), stop after Report: the activity stays on the board under **Planned** with `Waiting on: user — pick fixes`, and the report is the record. `/A.resume` or `/A.extend` on that file continues from the gate.

## Resolved comments

When the user approves and the FIXes are built, the reply to each original comment is written into the activity file under `## Findings` — the verdict and its evidence — so it can be pasted back to the reviewer.
