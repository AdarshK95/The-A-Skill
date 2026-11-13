# Tests

Scenario files, each with a prompt, the setup it needs, and a pass/fail rubric. Run every scenario on each host before tagging a release; record results in `tests/results/<version>-<host>.md` (date, pass/fail per line, notes). A scenario that cannot be run on a host is recorded `not run`, never as a pass.

How to run one: open the fixture project in the host, install the current build, start a new chat, paste the prompt, and judge the transcript against the rubric. Fixtures are any small repository with a few modules and a shared helper; `tests/fixture/` describes the minimum.

| # | Scenario | What it proves |
| --- | --- | --- |
| 01 | Plan on a small repo | Report before build; citations; options without a default; gate holds |
| 02 | Bugfix with a shared caller | Trace to origin; caller inventory; tier raised; fix at the root; fix impact |
| 03 | Review with one wrong comment | CONTEST with `path:symbol` evidence; FIX for the right one; nothing built before approval |
| 04 | Resume from a vague Next | Pointer repaired from the step list; files verified against Last done; continues at the right step |
| 05 | Where were we, in plain words | Reads board and headers; no claim from memory; one line per in-progress feature |
| 06 | Plain-English report | Two readers kept apart; conclusive answers with next steps; timed append-only event log |
| 07 | Reuse and duplication | Reuse search before new code; no parallel paths or hardcoded values; behaviour-preserving simplify |
| 08 | Parallel sessions | Claims respected; handoffs picked up; shared folder left empty |
