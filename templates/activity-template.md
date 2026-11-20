<!-- The status header is written above this by the skill. The first three sections are for the user and are what the project page shows on top: the user summary, the user's instructions, the questions and answers. Everything below them is for agents, fully technical. Nothing in this file is deleted; the six lines at the top of the user summary are rewritten in place, everything else is added to. -->

## User summary

**What this is:** <one line a stranger would understand>
**What you asked, as I understand it:** <the agent's reading of the ask, in plain words, corrected the moment the user corrects it>
**Now:** <the current step and what is happening in it>
**Running:** <every agent or background job and what each is doing — or "nothing">
**Next:** <the one next action, and whose it is>
**Waiting on you:** <how many things and what — or "nothing">

### What happened
- <date time> · <step> — <what was done> · <what it means for you> · <why, when a choice was made>

### What went wrong or needs your attention
- <date time> — <the problem in plain words> · <what it means for you> · <fixed | being fixed | needs your decision>

### Decided without you
- <date time> — <what I chose> · <why> · <what to say to change it>

### Changes of direction
- <date time> — <what changed> · <why> · <which instruction or answer>

### What you can check or test now
- <what to do> → <what you should see>

_(Sections with nothing in them are left out. Rules: `communication.md › The user summary`.)_

## Instructions

_The user's instructions for this feature, in their words, numbered as they arrive; never paraphrased, never merged. A later instruction that changes an earlier one is added as its own line and the earlier marked `superseded by I-n`. Every stage and every reviewer checks the work against this list._

- I1 · <date time> — "<the user's words>"

## Clarifications

_Every question the agent asked about this feature, at any stage, as a block with its context — and the user's answer in their words (`clarify.md › The record`). An answer that changes the ask is also added to Instructions. Read by every reviewer with the instructions._

### Q1 · <date time> · open
**Question:** <one sentence a person can answer without opening a file>
**Context:** <what came up, where we are, and why it matters to you — plain words>
**Options:**
- <option> — <what it means for you>
- <option> — <what it means for you>
**Suggested:** <option> — <the reason>
**Answer:** "<the user's words>" · <adds I-n | changes I-n | no change to the ask>

## Context

_Written once at Start: the constitution rules and lessons that bind this work, the decisions that bear on it, with references._

## Report

_Current report (see `report-schema.md`). A revised report is appended below the previous one with a dated heading; earlier versions stay._

## Items

_`### 7.n · <title> (<type>)` with Phase · Pointer · Last done · Next · Result, then its steps._

## Findings
_One line: rounds run, last round clean or not, counts by severity; the findings themselves are in `<nn>-<slug>.detail.md`._

_Review findings and verdicts (FIX / CONTEST / ESCALATE / DECLINE), with evidence. The build review's verdict, its obligation rows that are not held, and what it did not examine are recorded here too (`build-review.md`)._

## Decisions

_Each decision taken here; each also appears in the decisions log._

## Build findings

_Found while building: what · where (cited) · effect · proposed handling · decided or awaiting._

## Changes

_Quick reference: one line per file touched — `path` — `symbol` — what changed. Pulled from the event log for fast scanning._

## Realign

_After the last step or on a change of direction: does the build solve the original ask; what crept in; what the ladder removes._

## Verification

_Commands run and their output, or the check left behind. Requirements ticked with evidence._

## Open items

_Declined or deferred, each with where it is tracked._

## Links

_External work item(s) · related feature files (continues / superseded by) · related central docs._

## Event log (technical, in order, append-only)

_One line per step as it happened, each starting with `E<n> · <date>, <time>` — the user's ask (quoted), every file opened and what it showed, every command and its output, every dead end and why ruled out, every change (`path`, `symbol`, line, before → after, reason), every doc updated, every validation and its result. Nothing skipped, nothing removed. A later line that corrects an earlier one says `corrects E<n>`; the earlier line is left as written. A line the user stopped is tagged `DRIFT`._

- E1 · 13 Nov 26, 04:15 PM — User asked: "<exact ask>".
