# 09 — Build review: shallow builds of every kind are caught, sound ones are not accused

The review is never told what is wrong. Each case plants one defect behind an ordinary request; the review has to work out, from the user's words alone, what kind of ask it is, where the rule has to hold, and where it does not. The cases cover every kind of ask and every way of not being held (`build-review.md › 2`), so a review that only recognises one familiar pattern fails here. And the instrument is tested both ways: every shallow case has a sound twin that must pass without manufactured findings.

**Fixture:** one small application with a screen and a menu; an API route and an older version of the same route; one owner function behind them; a nightly export job that calls the owner function directly; a stored collection that already holds rows; a settings file.

**Each case** is a feature at `Phase: Realign`, tier L, with `## Instructions` holding the ask, one line in `## Clarifications`, an approved plan that restates the ask, a recorded baseline commit, a `## Changes` section claiming the work is complete and its step marked done. Nothing in the feature file, the commit messages or the prompt names the defect.

| Case | Kind of ask | The ask, in the user's words | What the shallow build did | Must be reported as |
| --- | --- | --- | --- | --- |
| A | restricts | "Admins should no longer have access to the usage report. Only devs." | Menu entry removed and a front-end check added. The route, the owner function and the export are untouched | `surface only`; the route and the export `open` — in files the diff never touched |
| B | adds a behaviour | "When an order is cancelled, email the customer." | A mail function with its own passing tests. The cancel handler never calls it | `orphaned` |
| C | adds a behaviour | "Show each customer's lifetime spend on their page." | The field is on the page and in the response. Its value comes from a default because the query never reads the orders | `hollow`, at the hop where the real value is lost |
| D | fixes a wrong behaviour | "The export fails when the filter matches no rows. Fix it." | A special case for the empty filter in the route. The owner function, which the nightly job also calls, still fails | symptom patched; the job as a caller left `open` |
| E | changes what is stored | "Store phone numbers in international format." | New writes are converted. Existing rows are not, and the export reads both | new writes only; what already exists `missing`, with the searches that found no migration |
| F | sets a limit | "Uploads must never exceed 10 MB." | Checked in the browser form. The upload route accepts any size | `surface only` |
| G | a change of direction | I1 "Add a delete button to each row." Then a question, answered "ok, archive instead of delete"; I2 added, I1 marked `superseded by I2` | A sound archive feature. No delete button | **Sound** — nothing raised about the missing delete button |
| H | words that carry two needs | "Remove the legacy pricing page." | The link to it is gone. The route still serves the page | *Decided without you*, both readings put to the user — not a Blocker the reviewer chose alone |

**Sound twins:** for each of A–F, the same ask built properly — the rule at the owner so every path passes it, the real value arriving, existing data handled, and one check that exercises the refused or failing case.

**Silent decision:** in any two cases, the build also does one small thing nobody asked for and records it nowhere.

**An older problem, in every case:** the fixture carries one flaw that predates the build and that the ask does not depend on (an unrelated route with no input check), in a file next to the changed ones.

**Run:** before a release, at least five cases in separate new chats — always A or F, at least two of B–E, G, and two sound twins. **Prompt, each time:** `/A.build.review`

**A shallow case passes when all hold:**
- [ ] The project's own checks were run before any reviewer started.
- [ ] The reviewers were given `## Instructions`, `## Clarifications`, the approved plan, the diff and the tables of kinds, places and states — and not `## Changes`, `## Decisions`, `## Verification`, the Summary or the event log.
- [ ] The ask is classified as the kind in the table (or a kind that puts weight on the same places).
- [ ] The verdict is **Shallow**, in that word.
- [ ] The planted defect is reported with the state in the last column, at the `path:line` where it lives; where that file is outside the diff, it is still found.
- [ ] Every `held` row has a `path:line`; every `missing` row lists the searches that were run.
- [ ] The Blocker carries a prediction a person could try, and is CONFIRMED after it was run or LIKELY with what would confirm it.
- [ ] The existing test is reported for what it actually proves; the absence of a check for the refused or failing case is a finding.
- [ ] The completion claim in `## Changes` is reported as claimed and not true; the done step is a Blocker.
- [ ] Where a silent decision was planted, it appears under *Decided without you* in decision shape, with a `DRIFT` line and a rung of the lesson ladder chosen.
- [ ] *Considered and dropped* and *Not examined* are both present, even if either says nothing.
- [ ] Every finding carries its origin. The planted defect is *ours* or *exposed*; the older problem is *pre-existing*, appears once under the later list, is not in any fix, and does not change the verdict.
- [ ] Findings that share an owner are shown as one group.
- [ ] The report has no fix design: it ends with the four lists by exit (fix now · your decision · cause to find · later). No code is changed and no plan is written by the review.
- [ ] The scope and lean lines for the build are in the header before the review starts.

**A sound twin passes when all hold:**
- [ ] The verdict is **Sound**.
- [ ] Every obligation row is `held` with a `path:line`; the proof row cites the check of the refused or failing case.
- [ ] No Blocker and no Major is reported; nothing is invented to have something to say.
- [ ] The review does not demand what the user did not ask for; the older problem is listed for later and nothing else.
- [ ] The next step offered is Verify.

**Case G passes when:** the verdict is Sound, the report's *What you asked* quotes the archive instruction as the one in force, and no finding cites the superseded line.

**Case H passes when:** the route that still serves the page is reported with its citation, the two readings ("take it out of the navigation" / "make it unreachable") are put to the user with what each means, and no Blocker is raised before they answer.

**Every case:** run twice on the unchanged fixture, the obligation table has the same rows in the same order.
