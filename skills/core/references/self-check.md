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
