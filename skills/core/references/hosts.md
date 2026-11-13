# Hosts — running a fresh reviewer, and knowing it was fresh

A lens (`goldfish-lenses.md`) is only a fresh review if the reviewer has no access to this conversation. What "fresh" means on each host, and the fallback when it is unavailable.

## Claude Code

Spawn one subagent per lens with the Agent tool. Give it:

- the lens prompt, verbatim, with its shared preamble;
- the path of the activity file (or its `## Report` section) and the paths of every file the report cites;
- the constitution path;
- read-only tools only (read, search, list); no edit, no shell;
- an instruction to return findings as the list format in `goldfish-lenses.md`, or `INCOMPLETE: <file>` when a file could not be read.

Give it nothing else: no summary of the conversation, no "the user wants", no instruction files. If the host offers a setting to withhold project instruction files from subagents, use it. Run the lenses of one round in parallel; rounds in sequence.

## GitHub Copilot in VS Code

As of this version, treat Copilot as **no fresh subagent** unless the isolation probe below passes with a delegated agent in your version. Default: cold self-review — run each lens prompt yourself, in a reply that quotes only the report and the cited files, and label every finding `cold self-review`. Say so to the user once per activity.

## Cold self-review — the protocol when no fresh reviewer exists

Fresh review is better; this is the honest substitute, and it is run *in this order*, one lens at a time:

1. Say to the user, once per activity: "No fresh reviewer is available on this host; I will run each review lens myself, cold, and label the findings."
2. Write the report section to the activity file first, then **close the thought**: for the review, read the report back **from the file**, not from memory, as if someone else wrote it.
3. For each lens the tier requires, in the order `sizing.md` gives: paste the lens prompt into your reasoning verbatim; read only the report text and the cited files; write the findings for that lens into `## Findings` labelled `cold self-review · <lens>` **before** starting the next lens. Do not reconcile lenses while running them.
4. A lens you cannot complete (a cited file is unreadable, the report is too long to re-read) is recorded `not run`, with the reason.
5. Resolve findings per `resolve-protocol.md` only after every lens has run. Contesting your own finding needs the same `path:symbol` evidence as contesting anyone's.
6. Tell the user, in plain words, how many findings each lens raised and that the review was not independent.

## Any other host

Same two questions: can a reviewer be started that did not see this conversation, and can its tools be limited to reading? Both yes → fresh review. Either no → cold self-review, labelled.

## Isolation probe — run once per project per host

Before the first fresh review in a project:

1. Write a nonsense phrase in the conversation (for example `the marker is "lantern-seven"`), and a different one at the end of the project's instruction file (`CLAUDE.md`, `.github/copilot-instructions.md`), temporarily.
2. Spawn one reviewer with the `comprehension` lens on any small file and ask it, in the same prompt, to list any marker phrases it has seen.
3. A reviewer that reports either phrase is **not isolated**: use cold self-review on this host and record it. A reviewer that reports neither is isolated.
4. Remove the temporary phrase from the instruction file. Record the result in `.a/project.md`: `review.isolation_verified: <host> <date> <fresh | not fresh>`.

Repeat after a host upgrade. The probe is cheap; a false "fresh" is not.

## XL hand-off (`review.xl_engine`)

`builtin` (default): the five XL stages in `sizing.md`, with these lenses. `egm`: when the Elephant-Goldfish Model plugin is installed on this host, run its review on the activity file's `## Report` and treat every finding it returns as a finding for `resolve-protocol.md`; when the plugin is absent, fall back to `builtin` and say so. The report, the gate and the logging stay ours either way.
