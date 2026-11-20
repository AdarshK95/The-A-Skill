# 10 — The user summary and the page: the user never has to ask

What two audits of real sessions found (78 times the user had to ask or correct) is the checklist here: the reading of the ask, the current state, context on every question, plain words, the reason, the next step, and choices made alone.

**The script first (one command, no host needed):** `python templates/pages/page_build.py --selftest` prints `ok` on every line. It builds a sample feature and checks the tabs, the summary tiles, the step trail, the instruction status, a question with context, a question without context flagged, an older-format file, escaping, and the index.

**Setup:** the fixture project with `.a/scripts/page_build.py` in place.

**Prompt 1:** `/A.plan add a CSV export to the orders page` — and answer the first question it asks.

**Pass when all hold:**
- [ ] The feature has its own folder, `<n>-<slug>/`, and the main file inside it is `<n>-<slug>.md`.
- [ ] The main file opens with `## User summary`, then `## Instructions`, then `## Clarifications`.
- [ ] The six lines are filled before any plan text exists: what this is, the ask as understood, now, running, next, waiting on you. *Running* says what is running or "nothing"; *Next* names one action and whose it is.
- [ ] The question was asked as a block with Context, Options (each with what it means) and Suggested with a reason — in chat and in the file. After the answer, the block's state is `answered` and the Answer quotes the user's words.
- [ ] `docs/pages/index.html` shows the feature under *Your next steps* with the question's own text while it is open, and the plan step as the newest line under *Recent activity*.
- [ ] The home page links the project's documents that exist (board, decisions, lessons, standing rules) and each opens.
- [ ] With `--watch` running and the page left open, a new line the agent adds to the summary appears on the home page within about 20 seconds, with nobody reloading it.
- [ ] The page build printed no `WARN`.

**Prompt 2 (same chat, after go and a build):** `/A.build.review`

**Pass when all hold:**
- [ ] The review is its own file in the feature's folder, `<n>.<m>-build-review-<slug>.md`, and shows as a tab on the feature's page.
- [ ] The main file's user summary has new dated lines under *What happened*, and the verdict and what needs the user under *What went wrong or needs your attention*.
- [ ] Any choice the build made alone is under *Decided without you* with why and how to change it.
- [ ] Nothing about the feature was written outside its folder; no file lacks the feature number.

**Prompt 3:** change one line of the user summary by hand, rebuild, open the page.

**Pass when all hold:**
- [ ] The changed line is green. After *Mark as read* and another edit, the new edit is green and the earlier one light blue.
- [ ] Removing the Context from an open question and rebuilding prints `WARN … has no Context` and shows it red on the page.

**The count that matters:** over the whole scenario, the tester should not need to ask "what happened", "what is next", "what is running" or "what does this question mean". Each time they do is a fail, recorded with the question.
