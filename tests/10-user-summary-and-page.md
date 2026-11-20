# 10 — The user summary and the page: the user never has to ask

What two audits of real sessions found (78 times the user had to ask or correct) is the checklist here: the reading of the ask, the current state, context on every question, plain words, the reason, the next step, and choices made alone.

**The script first (one command, no host needed):** `python templates/pages/page_build.py --selftest` prints `ok` on every line. It builds a sample feature and checks the tabs, the summary tiles, the step trail, the instruction status, a question with context, a question without context flagged, a choice made for the user, a code and a code name flagged, an older-format file, escaping, and the index.

**Setup:** the fixture project with `.a/scripts/page_build.py` in place.

**Prompt 1:** `/A.plan add a CSV export to the orders page` — and answer the first question it asks.

**Pass when all hold:**
- [ ] The feature has its own folder, `<n>-<slug>/`, and the main file inside it is `<n>-<slug>.md`.
- [ ] The main file opens with `## User summary`, then `## Instructions`, then `## Clarifications`.
- [ ] The six lines are filled before any plan text exists: what this is, the ask as understood, now, running, next, waiting on you. *Running* says what is running or "nothing"; *Next* names one action and whose it is.
- [ ] The question was shown in chat as the full block — what it is about, why it comes up, options each with what it means, a suggestion with its reason, the effort to change it later — and the same block is in the file. It was not a one-line list and the tester was not sent to a document. After the answer, the block's state is `answered` and the Answer quotes the user's words.
- [ ] No block uses a code (D3, option B) or a setting, function or file name the tester did not use first.
- [ ] Nothing was asked that the prompt already answered or that the code could answer. A choice the agent made alone that had a real alternative is a `decided` block, shown in chat under *Decided for you*.
- [ ] The plan's items each have a `Needs:` line, and the chat says in one line what is built first, what can be built at the same time and what waits.
- [ ] `docs/pages/index.html` shows the feature under *Your next steps* with the question's own text while it is open, and the plan step as the newest line under *Recent activity*.
- [ ] The home page links the project's documents that exist (board, decisions, lessons, standing rules) and each opens.
- [ ] With `--watch` running and the page left open, a new line the agent adds to the summary appears on the home page within about 20 seconds, with nobody reloading it.
- [ ] The page build printed no `WARN`.

**Prompt 2 (same chat, after go and a build):** `/A.build.review`

**Pass when all hold:**
- [ ] The review is its own file in the feature's folder, `<n>.<m>-build-review-<slug>.md`, and shows as a tab on the feature's page.
- [ ] The main file's user summary has new dated lines under *What happened*, and the verdict and what needs the user under *What went wrong or needs your attention*.
- [ ] Any choice the build made alone is a `decided` block with what it changes for the tester, and has its line under *Decided without you*.
- [ ] Nothing about the feature was written outside its folder; no file lacks the feature number.

**Prompt 3:** change one line of the user summary by hand, rebuild, open the page.

**Pass when all hold:**
- [ ] The changed line is green. After *Mark as read* and another edit, the new edit is green and the earlier one light blue.
- [ ] Removing *What this is about* from an open question and rebuilding prints `WARN … has no What this is about` and shows it red on the page. Writing a setting name such as `max_tokens` into the question prints a `WARN` naming it.

**Prompt 4 (only on a machine with Python):** accept the offer to start the live server.

**Pass when all hold:**
- [ ] The offer was made once, after the first page existed, and the answer is in `pages_server` in `.a/project.md`; on a machine without Python it was never made or mentioned.
- [ ] The server started with no window, and the address it printed opens the home page.
- [ ] With the page open, a line the agent adds to the summary appears on the home page by itself within about 20 seconds.
- [ ] *Resync* shows *Syncing…* then *Synced*, and the page is current afterwards.
- [ ] `--stop` ends it; the button then says the server is not running instead of failing silently.

**The count that matters:** over the whole scenario, the tester should not need to ask "what happened", "what is next", "what is running", "what does this question mean" or "elaborate". Each time they do is a fail, recorded with the question.
