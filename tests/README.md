# Tests

Scenario files, each with a prompt, the setup it needs, and a pass/fail rubric. Run every scenario on each host before tagging a release; record results in `tests/results/<version>-<host>.md` (date, pass/fail per line, notes). A scenario that cannot be run on a host is recorded `not run`, never as a pass.

How to run one: open the fixture project in the host, install the current build, start a new chat, paste the prompt, and judge the transcript against the rubric. Fixtures are any small repository with a few modules and a shared helper; `tests/fixture/` describes the minimum.

| # | Scenario | What it proves |
| --- | --- | --- |
| 01 | Plan on a small repo | Report before build; citations; options without a default; gate holds |
| 02 | Root cause with a shared caller | Four boxes; reverse lane to the origin; confirmation test; hand-off to plan; fix at the root |
| 03 | Review with one wrong comment | CONTEST with `path:symbol` evidence; FIX for the right one; nothing built before approval |
| 04 | Resume from a vague Next | Pointer repaired from the step list; files verified against Last done; continues at the right step |
| 05 | Where were we, in plain words | Reads board and headers; no claim from memory; one line per in-progress feature |
| 06 | Plain-English report | Two readers kept apart; conclusive answers with next steps; timed append-only event log |
| 07 | Reuse and duplication | Reuse search before new code; no parallel paths or hardcoded values; behaviour-preserving simplify |
| 08 | Parallel sessions | Claims respected; handoffs picked up; shared folder left empty |
| 09 | Build review: shallow and sound, every kind of ask | Eight cases, none naming its defect: the review classifies the ask, finds where the rule is not held (missing, stub, orphaned, hollow, surface only, open) even outside the diff, confirms it, surfaces silent decisions; honours an agreed change of direction; and passes each sound twin with every rule cited and nothing invented |
| 10 | The user summary and the page | Folder per feature with numbered files; the six summary lines and the trails kept current; every question with context, options and a reason; the page built with no format problem; changes highlighted; the tester never has to ask what happened |

`python templates/pages/page_build.py --selftest` checks the page builder itself in a second.

`install-matrix.ps1` (run it with both `powershell` and `pwsh`) and `install-matrix.sh` run the real installers and uninstallers against throwaway home folders: `settings.json` missing, empty, full of other settings and non-English text, or not plain JSON; no working Python; the pointer file deleted. They check the hook is added once, names its shell, prints the pointer (or a "missing" line, exit 0) in every shell present, and that uninstall removes only it. Run them before every release that touches an installer.

`check-spine.sh` is a one-second guard: it fails if any standing rule or required section is missing from `skills/core/SKILL.md`. Run it before every commit that touches the spine; editing scripts that search-and-replace can drop a block silently.
