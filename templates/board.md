# Project board

_Maintained by the `/A.*` skills. Features are numbered sequentially and never reused. A session edits only its own feature's block. Re-read before writing. Dates `DD MMM YY`, times `hh:mm AM/PM`._

## In progress

_One block per feature, grouped by area. Block line: `### <n> · <feature> · <type> · <phase> · pointer <n.i› k/N> · updated <date time> · <file>`. Item rows under it._

### Area: General

<!-- ### 7 · CSV export · plan · Implement · pointer 7.2 › 3/5 · updated 13 Nov 26, 05:40 PM · 2026-11/2026-11-13/01-csv-export.md
| # | Item | Type | Phase | Step | Status | Next |
| --- | --- | --- | --- | --- | --- | --- |
| 7.1 | Export endpoint | build | Closed | 4/4 | done | — |
| 7.2 | Null range on empty filter | bugfix | Implement | 3/5 | in progress | wire route in api/index.ts | -->

## Planned

_Same block shape as In progress; items listed with their planned steps count._

### Area: General

## Finished

| Area | # | Feature | Type | Tier | Closed | One-line result | File |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Deferred

| Area | Item | From | Reason | Revisit | File |
| --- | --- | --- | --- | --- | --- |

## To do

| Item | Due | Added | Notes |
| --- | --- | --- | --- |

## Overview

_How the project is shaping up: its areas, the parts in each, how they connect, and the state of each. Grey planned · blue in progress · green finished · orange deferred. Each board topic is a node under its area; updated by the activity that touches it._

```mermaid
flowchart LR
  classDef planned fill:#9e9e9e,stroke:#616161,color:#fff
  classDef inprogress fill:#1e88e5,stroke:#1565c0,color:#fff
  classDef finished fill:#43a047,stroke:#2e7d32,color:#fff
  classDef deferred fill:#fb8c00,stroke:#ef6c00,color:#fff

  %% One subgraph per area (from .a/project.md → areas). One node per component or
  %% feature inside its area. One edge per dependency or data flow. Board topics
  %% appear as nodes under their area; work inside a topic does not.
  %% Example:
  %% subgraph UI
  %%   ui[Web UI]:::inprogress
  %% end
  %% subgraph API
  %%   api[REST API]:::finished --> export[CSV export]:::planned
  %% end
  %% subgraph Data
  %%   db[(Database)]:::finished
  %% end
  %% ui --> api --> db
```
