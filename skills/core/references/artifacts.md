# Artifacts — the project's kept evidence

Activity files record **how** work was done. Decisions record **why**. Artifacts record **what is true** about the system or its environment, as established by measurement — facts the project will need again and should never have to rediscover. They live in `artifacts_folder` (default `docs/artifacts/`) with one row each in the artifacts ledger (`artifacts_ledger`, default `docs/artifacts/ARTIFACTS.md`).

## What is an artifact

An output becomes an artifact when all three hold:

1. **It is evidence, not opinion** — produced by running, probing, measuring, sampling or inspecting something real: an API, a deployment, a dataset, a dependency, an environment.
2. **It is project-level** — it describes the system or its surroundings, not one feature's work. A future feature touching the same area would want it.
3. **It would cost real effort to reproduce** — calls, time, data access, or a configuration that may no longer exist.

Examples: a probe matrix of which parameters each model accepts on each transport; a latency or cost baseline; a dependency inventory between environments (what dev has that prod lacks); a sampled classification of real traffic; an API's actual error shapes per transport; a measured performance profile; a schema as discovered from stored data rather than from documentation; a capability map of an external service.

Not artifacts: plans, reports, findings, decisions, code, scratch output, anything derivable from the code in seconds, anything already recorded verbatim in the activity file and never needed again. Working data copied from live systems is scratch and is deleted; an artifact keeps **results**, not the raw records of people.

## Shape of an artifact file

Named `<date>-<slug>.md` (file date in `filename_date_format`), containing:

- **What this establishes** — plain-English summary, one paragraph, for a reader who never saw the work.
- **How it was produced** — environment, dates, counts (calls, samples), tools, the exact scripts or commands if they are short, or where they live if not.
- **The facts** — the tables; every row attributable (request id, sample id, file:line) where that exists.
- **Valid for** — what makes this stale: a model version, a package version, a deployment change, a date. A reader must be able to tell whether to trust it.
- **Caveats** — what was not tested, single-run measurements, environment differences.
- **Produced by** — the feature file that created it.

## When to create one, and who

- At **Validate** or **Close** of a feature whose work produced evidence meeting the three conditions, the agent proposes the artifact — "this probe matrix should be kept as an artifact" — and writes it on the user's yes. The activity file keeps the full event log; the artifact keeps the distilled facts.
- Any time the user says "keep this as an artifact", write it, with the shape above, whatever its origin.
- The ledger row is written in the same step as the file; a feature's `## Links` names the artifact.

## Using artifacts

- **Start** searches the ledger for the request's terms, as it does the decisions log; a matching artifact is cited in `## Context` and read before Read re-measures anything. Re-measuring what an artifact already established is a build finding, not a step.
- **Reuse search** (`lean.md`) treats the ledger as an index of known facts.
- **`/A.drift`** checks each artifact's *Valid for* against the current environment (model version, package version, deployment) and marks stale artifacts; the ledger row says so and names what changed. A stale artifact is kept, never deleted.
- **Superseded**: a new measurement of the same thing adds a new artifact and marks the old row `superseded by <file>`.
