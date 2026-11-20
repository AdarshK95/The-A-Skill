# Pre-approve self-check — every tier, before the report is shown

Run on the finished report. A failed line is fixed before `Phase: Gate`. Record `Self-check: passed <date time>` in the activity file's `## Log`.

1. Every step traces back to a sentence in *What was asked* or to an approved build finding.
2. Every file a step names exists at that path (open it).
3. Every function, type or endpoint the report cites exists with the signature or shape described.
4. The caller inventory is complete: every caller of every changed symbol appears, with its handling.
5. No step contradicts the constitution; no step reverses a logged decision without saying so and asking.
6. Every step has a verification line, and together they cover the whole change.
7. Every option offered to the user has trade-offs on each side, the alternatives stay visible, and one line says which way you lean and why.
11. The chat summary is in plain language: no path or symbol the user did not ask for; it ends with the Done / Not done / Your next step block, and every item in that block names a file, a record or a command the user can check.
12. *Reuse candidates* is filled for every new symbol, route, query or config path the plan adds, and every *none* has a reason.
13. Anything the plan asks the user to run or install has passed the ladder: an existing tool or a single standard command was considered first and named if it suffices.
14. No step adds a second path to something an existing path already reaches, and no step introduces a literal that varies (URL, key, limit, path, label) outside config.
8. The tier's signals each name a file or a decision.
9. Assumptions and parked clarifications are listed, not buried.
10. The chat summary fits one screen, names the decisions the user must make, and at L/XL says Review runs next — never offers to skip it.
14. The plan does what the user asked, as asked. Where it does not, the report says so and why, and asks — it does not substitute.
15. Every path shown in chat is a full path from the root; every item has steps with done-conditions and the pointer's `N` is the real count; `## Requirements` is present at L/XL.
16. This self-check was run and the line `Self-check: passed <date time>` was written to `## Log` before the report was shown.
17. Nothing the agent created remains outside `$env:TEMP` / `.a/tmp/`; every temporary file is already deleted; *Your next step* contains no chore the agent caused.
18. Every decision carries what came up and why, the options with what each means, and a suggested answer with its reason — readable without opening the file — and the list ends with the "say go" line; the report states the solution quality (robust / tactical / quick fix) and names the next step with its default.
19. Every step lists its failure cases and the two-layer message (plain English, then technical) each produces; verification covers them.
20. The reply states the agent's own read of each instruction it acted on — agree / caveat / disagree with alternative / possible misunderstanding — in one line each.
21. `### Elements touched` names every system part the plan changes, with existing ids or a proposed new element; the type stated matches the signals or is raised as a proposal.
22. A plan that fixes a wrong behaviour names the root-cause report it plans from, with the cause at CONFIRMED or LIKELY; the change sits at the origin, not at a cascade link or the symptom.
23. The scope check and the lean check were both run in full on this plan and their one-line results are in the header and in the chat summary, clean or not; nothing they found is left untriaged.
24. `### Instruction check` lists every instruction in `## Instructions` in force, each honoured, a proposed deviation with its decision, or a question; none missing, none resolved by the agent alone.
25. The report is current state only, in plain words, readable in minutes; history, transcripts and tables are in the detail file in agent notation; every record the map, drift, resume or the conformance check reads (`logging.md › What is never minimized`) is present and complete.
26. Every output another step consumes has a named valid shape and a named, visible failure state for its absence; no step returns an empty collection, `{}`, `unknown` or `none` where it should return a failure.
27. Nothing a person will read names a thing by a code (D3, R-5, code-03, step 7b); decisions are named by their subject and their options are sentences.
28. Every file the plan edits is inside `code_scope`; any path outside it appears only as a question to the user or a one-line "out of scope" note.
29. Every finding in the report has a verdict (blocks / does not block / side work); every change outside `code_scope` is justified as unavoidable, owned to proof, and recorded as a decision; nothing we changed is handed over before it is shown working.
30. Every question asked about this feature so far is in `## Clarifications` with the user's answer in their words; every point the plan settles that the user was not asked about is in *Assumptions*.
