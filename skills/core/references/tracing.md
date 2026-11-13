# Tracing — the Read method

"Read the code first" is an instruction; this is the method. Read ends when the three shapes below are filled for the code the request touches, every row cited `path:symbol` or `path:line`. Write them into the activity file under `## Report › What exists today` (or a `## Trace` section when long).

## 1. Trace table — how a value or request moves

One row per hop, from where the request enters to where the result leaves (for a bug: from the symptom back to the origin).

| # | Where (`path:symbol`) | What arrives | What leaves | Notes (bug: why wrong here) |
| --- | --- | --- | --- | --- |

Rules: a hop you did not open is not a row; write `UNVERIFIED` and open it before the report. For a bug, the origin is the first row where correct input produces wrong output; everything downstream is a symptom.

## 2. Caller inventory — who else depends on what you will change

One row per function, type, query or contract the plan may change.

| Changing | Callers / consumers (`path:symbol`, from search, not memory) | Accounted for in the plan? |
| --- | --- | --- |

Rules: search the whole repository, including tests and scripts; an unaccounted caller is a Major finding before any reviewer sees it. Two or more callers outside the edited file raise the tier (`sizing.md`).

## 3. Boundary list — where things can go quietly wrong

One line per place in the traced path where data changes shape, is stored or cached, is checked for permission, is ordered or timestamped, or is touched by more than one actor (tabs, users, workers, retries).

| Boundary | Where | Risk if the change is wrong |
| --- | --- | --- |

Rules: each boundary gets a line in the report's *Impact*; a cache, permission, timestamp or concurrency boundary raises the tier.

## How much to read

Everything the three tables need, and nothing more. Breadth comes from search (every caller), depth from opening the hops. Stop reading when the tables are complete; do not stop before.
