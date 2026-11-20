# Build review — the method

A plan review (`goldfish-lenses.md`) asks, before anything is built, whether the design is right. This asks, after the build, whether what now exists is **what the user asked for, built all the way down** — or something that only looks like it from where the user stands. Its output is a verdict with evidence for every obligation, and findings that each say whose they are and where they go next (§7). Never a fix, and never a plan.

It is a different review, not the same lenses pointed at code. A plan fails by describing the wrong thing. A build fails in ways a plan cannot: a behaviour present at the surface and absent beneath it; a rule enforced where the user looks and not where the thing lives; a decision the builder took alone on an ambiguous point; a check that passes without proving anything.

**The scope is the ask, not the diff.** The diff shows what was built. The ask says what has to be true. Code the build never touched is in scope whenever the ask depends on it: the door that was always open, the caller nobody updated, the job that still writes the old shape. A review that reads only the diff confirms the work that was done and never sees the work that was not. The ask also bounds it: a problem the ask does not depend on is noted in one line and left for later, however real — a review that chases everything it can find turns one feature into the upkeep of the whole codebase.

## 1. Four sources, kept apart

| Source | Is | Used as |
| --- | --- | --- |
| **The ask** | `## Instructions` and `## Clarifications` — the user's words, and their answers and decisions, in order | The standard. Never the plan's paraphrase of it |
| **The plan** | The approved `## Report`: proposed change, requirements, assumptions | What was agreed — and itself checked against the ask |
| **The build** | The diff from the feature's baseline, and the repository around it, read from the files | The thing under review |
| **The builder's account** | Summary, `## Changes` descriptions, `## Build findings`, `## Decisions`, `## Realign`, `## Verification`, the event log, the chat | **Claims.** Withheld from every reviewer; read only at Reconcile (step 5) |

A reviewer told "step 3 done — the rule is enforced" looks for an enforcement and finds the one that is there. A reviewer given only the ask and the code looks for where it has to be, and finds where it is not. That is the reason for the fourth row.

**Order of authority.** The user's latest word on a point — a later instruction, an answer, a decision they took — outranks their earlier word; any of those outranks the plan; the builder's account outranks nothing. A line marked `superseded` is not a standard: the reviewer checks the line that replaced it. This is why every answer and every decision is written into `## Clarifications` with what was chosen (`clarify.md › The record`): a change of direction the user agreed to reaches the reviewer as the user's words, not as the builder's claim.

**Checks first.** Before any reviewer is started, run the project's own checks over the build — tests, type check, linter, whatever the project's config and `rules` name. A failure the build caused stops the review: say what failed and hand back to `/A.build`; reviewers are not spent on what a machine already caught. A failure that was there before the build is named under *Not examined* and the review goes on.

**The diff.** Everything this feature changed, uncommitted work included: `git diff` from the baseline commit the first build step recorded (`core/SKILL.md › Implement`); with no recorded baseline, from the merge-base with the main branch; with no git, the paths in `## Changes` — the paths only. The orchestrator writes the diff and the list of changed paths to `.a/tmp/` for the reviewers and deletes both before the report.

**No `## Clarifications` section** (a feature opened before 0.10.0, or work that never went through Clarify): say so once, and *Not examined* carries "questions and answers were not recorded for this feature; intent checked against the instructions only".

## 2. Obligations — what has to be true for the ask to hold

The unit of this review is the **obligation**: one rule from the ask, at one place it has to hold. A rule is true only when it holds at every place it applies to. The reviewer is not told what to look for; it works it out from the ask in two steps.

**Step one — what kind of ask is it.** The kind decides where the weight falls. An instruction can be more than one kind and takes the places of each.

| The ask… | The rule reads | The weight falls on |
| --- | --- | --- |
| restricts or permits — who may see, do or change something | "only X may…" | every way in · the owner · other readers and callers · what already exists |
| adds a behaviour | "when A happens, B results" | every way in · the owner · the effect · failure |
| changes or removes a behaviour | "no longer…", "instead…" | every way in (the old one closed) · other readers and callers · what already exists |
| fixes a wrong behaviour | "A no longer produces B" | the owner (the origin, not the symptom) · other readers and callers · proof |
| changes what is stored or exchanged | "is kept as…", "is sent as…" | the effect · other readers and callers · what already exists |
| sets a limit or a quality — speed, size, retention, cost | "never more than…", "within…" | the owner · failure · proof |

**Step two — the places, and the question at each.** Proof is owed for every kind.

| Place | The question |
| --- | --- |
| **Surface** | Where is it shown or offered — screen, menu, command output, message? |
| **Every way in** | Which routes, handlers, commands, jobs, webhooks, exports and older versions of the same thing reach it? |
| **The owner** | Which function, service or query owns the resource, the state or the behaviour? The rule has to live here, where every path passes |
| **The effect** | Where does the result land — record, response, message, side effect — and does the real thing arrive there? |
| **What already exists** | Rows, caches, exports, sessions, tokens and files made before the change: does the rule cover them? |
| **Other readers and callers** | Which other roles, clients, internal callers and workers get or use the same thing another way? |
| **Failure** | What does someone get when it is refused, missing, empty or over the limit? |
| **Proof** | Which check goes red if the rule is removed? |

Each obligation ends in one state. A row that is not held says **how**:

| State | Means | Carries |
| --- | --- | --- |
| `held` | The rule is enforced, or the behaviour is real, at this place | The `path:line` that does it, and the check that proves it (or `no check`) |
| `not held` · `missing` | Nothing is there | Where it would have to be, and **the searches that found nothing** |
| `not held` · `stub` | Something is there and is not real: a constant, sample data, a TODO, a mock in a real path, a name that promises what the body does not do | The `path:line` |
| `not held` · `orphaned` | It is real, and nothing calls, registers, runs or reads it; or its switch is off | The `path:line`, and the search for its users |
| `not held` · `hollow` | It is reached, and the real data never arrives: the chain ends in a literal, a default or an empty value | The hop where the real value is lost |
| `not held` · `surface only` | Held where it is shown, not where it is owned | Both citations: where it is shown, and the path that stays open |
| `not held` · `open` | A way in that the rule does not stand in front of | The path, and where the rule lives instead |
| `not examined` | Nobody opened this place | Why |

**A clean result is evidence too, and so is an absence.** `held` without a citation is `not examined`. `missing` without the searches that were run is `not examined`: the code will not use the ask's words, so the vocabulary is varied before nothing is concluded. A review cannot say "looks fine" or "it isn't there"; it says where, or what it searched, or that it did not look.

**An obligation comes from the user's words, not from the reviewer's taste.** A place belongs on the list when the rule the user stated would be *false* there — not when the system would merely be better. Where the words can carry two needs (to take something off the screen, or to stop it being possible), the reviewer does not pick one and grade the build against it; that point goes to the user as *decided without you* (§8). A review that invents scope is as wrong as a build that drops it.

**Rows are keyed by instruction and place**, in the order of the places table, so two runs on an unchanged build produce the same rows and can be compared line by line.

## 3. Three lanes and two lenses, in parallel, each blind to the others

The lanes are the root-cause lanes (`rootcause.md › 3`) run on a build instead of a fault: the same three directions, the same blindness, the same coverage statement.

| Lane | Starts from | Moves | Finds |
| --- | --- | --- | --- |
| **Intent** (zoom-out) | the user's words | words → the need behind them → what must be true → the plan → the code | built to the words and not the need; the plan or the code reading the ask differently; decisions taken without the user; things nobody asked for |
| **Forward** | each place a promised behaviour enters | forward, hop by hop, to where its effect lands | the hop where the behaviour stops being real |
| **Reverse** | each thing the ask protects, restricts, changes or produces | backward, to every path that reaches it | a path the rule does not stand in front of |

Shallowness is what Forward and Reverse find between them; Intent runs beside them, not before, so the alignment check is never shaped by what the depth lanes saw. Two lenses read the diff itself: **correctness** and **impact**.

Each reviewer returns: the obligations it derived, each with its state and citations; its findings; and a **coverage statement** — the files, entry points and layers it opened, and what it did not.

### Signatures — ways for work to look done that the states do not name

Given to Forward and Reverse with §2.

1. **Copied, not shared.** The same check pasted into some callers; the rule does not live where all callers pass, so the next caller will lack it.
2. **Happy path only.** The failure is caught and dropped; empty or missing comes back as a value that reads like a result (`build-check.md › Absence is a failure`).
3. **Symptom patched.** A special case for the reported input, a condition keyed on a literal, the cause upstream untouched.
4. **New writes only.** The rule applies from now on; what already exists still carries the old state.
5. **A check that cannot fail.** It asserts the mock, asserts something is truthy, tests the helper instead of the behaviour, is skipped, or was edited to match the new output; nothing tests the refused or failing case.
6. **A check weakened to pass.** A test, fixture, type, lint rule or threshold changed in the same diff so that a failure went away.
7. **Done by declaration.** A plan step whose done-condition the code does not meet.

### Shared preamble for every reviewer

> You are reviewing code you did not write, in a codebase you are seeing for the first time. You have: what the user asked for, in their own words (`## Instructions`), and their answers and decisions (`## Clarifications`); the plan that was approved; the diff of what was built; the project's standing rules; the kinds, places and states you will report in; and the repository to read. You have not been given the builder's account of the work, and you do not need it: the code is the only evidence of what was built. The user's words are the standard — not the plan, and not the diff — and their latest word on a point replaces an earlier one. Code the diff never touched is in scope whenever the ask depends on it. Read before you write. Every finding cites `path:line`. Every statement that something **is** in place cites the code that puts it there, and every statement that something is **absent** lists the searches you ran; without either, write `not examined`. Tag each finding Blocker, Major or Low, with a confidence, and say whether the code it is about is in the diff or outside it. A problem you notice that the ask does not depend on gets one line under *noticed, not ours*; do not investigate it. Do not propose rewrites; name the gap. Change nothing. "No findings" is a complete answer when it comes with what you opened. End with your coverage statement: the files, entry points and layers you opened, and what you did not.

### intent

> First, before you open the instructions or the plan, read the diff and write in your own words what this build does — what a person can now do, see or no longer do, and what is stored or sent differently. Keep that paragraph; it is returned unedited. Then start from the user's words. For each instruction and each answer still in force: write the **rule** behind it in one sentence and the need it serves; say which kind of ask it is; and list the places it has to hold. A place belongs on the list only when the stated rule would be false there; where the words can carry two different needs, do not choose — list it under *decided without the user*. Then read the plan, then the code, and say for each instruction: *honoured in substance* · *honoured in form only* (the words are satisfied, the need is not) · *not honoured* · *contradicted*. Then three lists. **Decided without the user:** each point where the ask and the answers are silent or can be read two ways and the code took one reading — the reading taken, the other reading, and whether the plan's assumptions show the user saw it. **Not asked for:** what the code does that no instruction and no plan step names. **Plan against ask:** where the plan narrowed, widened or reinterpreted what the user said. An instruction not honoured in substance is a Blocker. A decision the user never saw is a Major, and a Blocker when it changes what someone can do, see or lose.

### forward

> For each behaviour the ask promises, find where it enters the system — the screen, the route, the command, the job — and follow it forward through every layer to where its effect lands: the stored record, the response, the side effect. One row per hop, cited; a hop you did not open is not a row. At each hop give its state: real, or `missing`, `stub`, `orphaned` or `hollow` — is it there, is it more than a placeholder, does anything reach it, does the real value pass through it. Stop only at the effect: a behaviour you followed to a function you did not open is `not examined` from there on. For the last hop, name the check that would go red if this path were broken, or write `no check`. Use the signatures you were given. A behaviour that stops being real before its effect is a Blocker. One that is real and has no check is a Major.

### reverse

> Start from the other end. List each thing the ask protects, restricts, changes or produces: a set of records, a permission, a stored state, a contract, a limit. For each, search the whole repository for **every** path that reaches it: search for the name of the table, collection or store; for the name of the function that owns it and every caller of that function; for the route or command string and its other versions; then jobs, scripts, exports and other clients. List the searches you ran. Do not start from the diff: the path that matters is usually one the diff did not touch. For each path, cite where the rule is enforced on it, or write `open`. Then say where the rule lives: at the owner, so every path passes it; copied into some callers (name the ones without it); or `surface only`. Use the signatures you were given. An `open` path to something the ask governs is a Blocker, whether this build created it or found it that way. A rule that is `surface only` is a Blocker. A rule copied into callers instead of living at the owner is a Major.

### correctness

> Assume the diff is wrong and find where. For each changed function: which input, state, order of events or failure makes it return a wrong answer, lose data or leave work half-done? Which branch that worked before now behaves differently? What comes back when the thing it reads is empty, missing or malformed — a named failure, or a value that reads like a result? Then, for every change the plan does not name — a fix, a refactor, a workaround added along the way — say what it is, whether it is right, and whether it removes a cause or hides a symptom. A wrong answer, lost data or a security hole is a Blocker. A hidden symptom or an unhandled failure is a Major.

### impact

> The diff shows what changed. Find what changes with it. For every modified function, type, route, query, stored shape or setting: search the repository for every caller and consumer — tests, scripts, other packages, front ends — and say whether the build accounts for each. For data already stored in the old shape, caches already filled and sessions already open: what happens to them now? An unaccounted caller or consumer is a Major. Existing data the change makes wrong or exposes is a Blocker.

### lean (XL)

The `lean` prompt from `goldfish-lenses.md`, with "the plan builds" read as "the build added", under this file's preamble.

### critic on what was held (XL, after the coverage check)

> Here are rules and, for each, the code said to enforce it. Assume each one is wrong. For each: find a way to reach the governed thing that this code does not stand in front of, or an input for which it lets through what it should refuse. Cite the path. A row you cannot break, say so in one line.

It receives the `held` rows only — the reviewers' citations, never the builder's account.

## 4. Coverage check — before any synthesis

Assemble two tables from the reviewers' returns (`tracing.md › 5` is the model):

- **The obligation table.** One row per obligation, duplicates across lanes merged: the instruction it comes from · the kind · the rule · the place · which lanes examined it · state · citation or searches · check.
- **The change table.** One row per changed file: which reviewers opened it.

Gaps, each of which gets a **targeted pass** (a fresh reviewer, the one lane prompt, the one target):

- an instruction or answer with no obligation rows;
- a place its kind puts weight on (§2) that no reviewer opened;
- a way in that Reverse listed and did not open;
- a changed file no reviewer opened;
- two lanes that disagree on a row's state.

Repeat until no remaining gap could hide an unmet obligation. What is still unexamined is written into the verdict as **Not examined**, by name. A reviewer that failed, timed out or returned `INCOMPLETE` is retried once, fresh; after that it is `not run`. Not run is never zero findings, and its rows are `not examined`. Each reviewer's return — the paraphrase, the rows, the coverage statement — goes to the detail file as returned; a summary that keeps only the findings loses the evidence for everything that was held.

Then merge the findings as `goldfish-lenses.md › Synthesis before resolution` says: one finding per gap, credited to every lane that found it; ordered by severity, then confidence; Lows as a count.

## 5. Reconcile — now, and only now, the builder's account

Read `## Build findings`, `## Decisions`, `## Changes`, `## Realign` and `## Verification`, and set them against what the reviewers found:

| The reviewers found | The account says | Result |
| --- | --- | --- |
| A deviation from the plan or the ask | Recorded, and the user decided it | Settled; cite the decision. (It should also have reached the reviewers through `## Clarifications`; if it did not, add the missing line there) |
| A deviation | Recorded, never decided | A decision for the user, in decision shape |
| A deviation, or a reading of an ambiguous point | Nothing | The finding stands, tagged **silent**. A `DRIFT` line in the event log; the lesson ladder decides what it becomes (`logging.md › Drift and lessons`) |
| An obligation `not held` | "done", "verified", "enforced" | The finding stands, tagged **claimed, not true**. A step marked done whose done-condition the code does not meet is a Blocker |
| Nothing | A change the reviewers did not see | A coverage gap: back to step 4 for that file |

A shortcut marked in the code with its ceiling and upgrade path (`core/SKILL.md › Implement`) is declared, not silent; it is a finding only when its ceiling breaks an obligation. Completion claims are not evidence in either direction: a ticked step proves nothing, and an unticked one is not a finding.

## 6. Confirm — every Blocker, before it reaches the user

Each Blocker carries a **prediction** a person could try, in the shape *doing this, as this caller, gives this result* — the refused request that succeeds, the input that stores the wrong record, the switch that changes nothing. Run it when that needs no change to the project's code and touches no shared environment: an existing test, a throwaway check under `.a/tmp/`, a local call.

| Outcome | Then |
| --- | --- |
| The prediction holds | **CONFIRMED** |
| It cannot be run here | **LIKELY**, with exactly what would confirm it and what that needs |
| It fails | The finding moves to **Considered and dropped**, with what refuted it |

A Blocker without a prediction is not reported as one. Low-confidence Majors are checked against the code the same way before they get a verdict. *Considered and dropped* is shown to the user, so a real finding lost to one wrong refutation can still be caught; it is never given to a later round's reviewers.

## 7. Sort — whose it is, what it shares, where it goes

The review ends by sorting, not by fixing. Three passes over the confirmed findings (`flow.md › Whose finding is it`):

**Origin.** *Ours* — the build added it or broke it: it is in the diff, or the diff made it wrong. *Exposed* — it was there before and the build never touched it, but an instruction cannot be true without it. *Pre-existing* — it was there before, and every instruction holds without it. Origin is read from the diff and the obligation table, never from the builder's account.

**Group.** Findings that share an owner or a mechanism are one group, with one line saying what they share. A group is the sign that the cause sits upstream of the individual gaps.

**Exit.** Each finding or group leaves by exactly one:

| Exit | When | Next |
| --- | --- | --- |
| **Fix** | Ours, or exposed at an owner the build already changed; the cause is plain from the finding; one right place for it | A fix item at the owner |
| **Decide** | It comes from a design choice or from words that carry two needs; or a group shares one origin; or it is exposed and lies outside what the build touched | A decision for the user; the plan changes only if they choose a different design |
| **Diagnose** | The cause cannot be seen from the code: work that vanished, something that cannot happen | `/A.rootcause` on that finding or group, and nothing else |
| **Later** | Pre-existing; and everything under *noticed, not ours* | One line on the board, shown at Close. Never in this feature's fixes. One that loses data or opens access is raised to the user at once as its own proposed feature |

The review names the exit; it does not design the fix. What a fix is, exactly where it goes and what else it touches is the plan stage's work, done on the fix item with the callers read.

## 8. Verdict and report

One verdict, in these words, so two runs on the same build can be compared:

| Verdict | When |
| --- | --- |
| **Sound** | Every obligation is `held` where it is owned, with a check; no Blocker or Major is open |
| **Sound once fixed** | Every obligation is `held`; there are defects from the lenses, and the FIX list closes them |
| **Shallow** | One or more obligations are `not held`, or held with no check: it looks finished and is not |
| **Off target** | What was built answers a different ask than the user's. Goes to the user first, alone, as a decision; nothing else is resolved until they answer (`goldfish-lenses.md › A premise finding stops the round`) |

Only obligations whose origin is *ours* or *exposed* count toward the verdict; pre-existing ones are listed and change nothing. The verdict always carries **Not examined**, even when that line says "nothing".

The review is an item of the feature (`7.n · Build review (review)`), written with the report schema's headings and these in place of *Proposed change*:

- **What you asked** — the instructions, answers and decisions in force, quoted.
- **What was built, read cold** — the intent reviewer's paraphrase of the build, unedited, directly under the user's words, so the two can be compared at a glance.
- **Verdict** — one of the four, and one plain sentence of why.
- **Where each rule stands** — the obligation rows that are not `held`, in plain words with how, and the count that are; the full table goes to the detail file.
- **Decided without you** — every silent decision, each in decision shape: what was unclear, the reading the build took, the other reading, what each means for you, suggested. The user confirms or changes each one; a confirmed one becomes a decision (dual write), a line in `## Clarifications` and an instruction in the ledger.
- **Findings** — Blockers and Majors with CONFIRMED or LIKELY, each with its origin; groups shown as one; Lows as a count.
- **Considered and dropped** — one line each.
- **Not examined.**
- **Where each finding goes** — four short lists by exit: ours to fix now · yours to decide · needs its cause found · older problems noted for later. No fix is designed here.

In chat, plain language first (`communication.md`): what it means for the user, in terms of what they can see or do — "it looks finished from the screen, but underneath it is only hidden, not prevented" — then the decisions, then where the detail is.

## Gate

The review changes no code and writes no plan. It ends:

- **Sound** → "Next: Verify. Say *go*."
- **Sound once fixed** or **Shallow** → by exit (§7). *Fix*: one item of the feature holding only ours and exposed findings, entering the spine at Evaluate — the callers read, each fix at the owner with a check seen to go red before it and green after, its quality stated (robust, tactical or quick fix), its tier from `sizing.md` over the fix set: S gets no plan review, M and above get `/A.review`. What the build added that it should not have — duplication, dead code — is a second item, built after the first is verified. *Decide*: to the user now. *Diagnose*: `/A.rootcause`; its cause then joins the fix item. *Later*: the board. A fix set that is feature-sized (`hierarchy.md`) is proposed as its own feature.
- **Off target** → one decision to the user, alone, before anything else is resolved: keep and adjust, or go back to the plan (`/A.plan.realign`).

At L and XL a build is not verified or closed without this review; the user may stop at the round cap, in their own words, with what is unreviewed stated.

## Without a plan

Code with no feature behind it (a diff in the chat, a branch, a pull request) is reviewed the same way with what exists: the user's request in this conversation is the ask — quoted into the report, and asked for in one line if there is none; "the plan" is absent and said to be absent; Reconcile has only the commit messages. At the end, offer once to record it as a feature (`record_chat_work`).

## Resolution and rounds

Findings are answered with `resolve-protocol.md`. Three rules are tighter here, because the session resolving the findings is usually the one that wrote the code:

- **The author does not rule on their own review.** A CONTEST needs `path:line` evidence the reviewer could have read. A contested or declined Blocker or Major is settled only with the user's agreement, shown with both sides.
- **Severity is the reviewer's.** The author may contest a finding; it may not lower one.
- **The review changes nothing and plans nothing.** Fix items are planned by the plan stage, go through the gate, and are built by `/A.build`.

After the fixes are built, two things happen. Every earlier Blocker's prediction is run again and must now fail — a fix is checked on purpose, not by the luck of a later reviewer raising it. And the review runs again on the new diff — fresh reviewers, told nothing of the earlier round — for the lanes whose obligation rows the fixes touched; a fix to an owner re-runs Reverse in full. Rounds, the clean-round rule, the cap and churn are as `goldfish-lenses.md › Rounds`. Stopping at the cap is the user's decision, stated with what is still unreviewed. What keeps this from becoming a loop is stated once, in `flow.md › What ends the loop`.

## Depth

The feature's tier, recomputed with `sizing.md` over what the build actually touched (not what the plan expected to touch). Plain `/A.build.review` chooses from those signals. `/A.build.review.s`, `.m`, `.l`, `.xl` force the depth, as does "quick", "at L" or "xl" in the request (`Tier: L (user)`). In the flow after a build, tier S is not a stage — small changes carry no ceremony, and the build check and Validate cover them; run by name on a small build, it is the quick check.

| Tier | Runs |
| --- | --- |
| **S** — the quick check | One fresh reviewer runs `intent`, then Forward, then Reverse, writing each before starting the next, on the places each instruction's kind puts weight on (§2, step one) and no others. No lenses, no targeted passes, no rounds. Checks first, reconcile and confirm still apply. The verdict is labelled `quick check`, and *Not examined* names what this depth leaves out: the correctness and impact lenses, and every place outside the weighted ones |
| **M** | `intent` · one **depth** reviewer running Forward then Reverse, writing the first before starting the second · `correctness`. Coverage check, reconcile, confirm |
| **L** | `intent` · `forward` · `reverse` · `correctness` · `impact`, in parallel. Coverage check with targeted passes, reconcile, confirm; rounds |
| **XL** | L, plus `lean`, plus the critic on what was held; rounds |

`review.xl_engine: egm` does not apply: that engine reviews documents.

## Who reviews

Fresh reviewers as `hosts.md` says, one per lane or lens, read-only, each given: its prompt with the preamble; the three tables of §2; the signatures, for Forward and Reverse; the paths of the `## Instructions`, `## Clarifications` and approved `## Report` sections; the diff and changed-paths files; the constitution — every path absolute. Nothing from the fourth row of §1, nothing about earlier rounds, no summary of the conversation, and never the answer to a question the code is supposed to answer.

Where the host has no fresh reviewer, the honest substitute is a **new conversation**: the review reads only files, so a session that did not build the code is a fresh reviewer. In the conversation that built it, the cold self-review protocol (`hosts.md`) applies with one more sentence to the user — "the author is reviewing their own work; run `/A.build.review` in a new chat for an independent read" — and the verdict is labelled `cold self-review`.

**Reviewers leave drops.** The Forward hops and the Reverse path lists are flow fragments and relations; at the write point after the coverage check they are appended to the registry (`elements.md › Every pass leaves a drop`).
