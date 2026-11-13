<!-- The status header is written above this by the skill. Two readers: the Summary is for the user, in plain words; everything below it is for agents, fully technical. Nothing in this file is deleted or rewritten; corrections are new lines that point back. -->

## Summary (plain language)

1. **The ask:** what the user wanted, in everyday words.
2. **The situation:** what was found to be true, and what it stopped or risked, from the user's point of view.
3. **What was decided and why:** one or two plain sentences.
4. **What was done:** one or two plain sentences; no paths or names.
5. **The result:** what works now that did not, or what no longer goes wrong. (Updated as the work progresses; the last line always reflects the current state.)

## Context

_Written once at Start: the constitution rules and lessons that bind this work, the decisions that bear on it, with references._

## Report

_Current report (see `report-schema.md`). A revised report is appended below the previous one with a dated heading; earlier versions stay._

## Items

_`### 7.n · <title> (<type>)` with Phase · Pointer · Last done · Next · Result, then its steps._

## Findings

_Review findings and verdicts (FIX / CONTEST / ESCALATE / DECLINE), with evidence._

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
