# Changelog

Version numbers follow the scale of the change, decided per release. **Third digit:** iteration on an existing capability — wording, rules, fixes, a redesign of something that already exists (a new layout for the map is still the map). **Second digit:** a new capability, or anything an installed copy must re-learn — a new or removed command or stage, a new script, a format change that breaks old files. **First digit:** a restructure that breaks existing projects (not before 1.0).

## 0.9.2 — 15 Nov 26

- **Observed layer** on the map: an element's `Events:` patterns (`scout.*`, `agent.invoke@Key`, notes in parentheses ignored) and a generic contract file `docs/map/observed.jsonl` (`turn, ts, name, kind, status, ms, tag`) written by a project-owned exporter; the map shows turns, errors and median duration per element, traffic on relations, observed paths with their share of turns beside the declared flows, and the unmapped-events list as the registry's gaps. The skill never reads a project's telemetry store.
- Map page: pan by dragging, Ctrl+wheel and ± zoom, foldable side panel, multi-visit step badges, labels only on selection or an active flow, dotted container boundaries, compact placement of branches under their branch point, no-flow parts as a grid.
- Flow naming rule (actor and action; one per agent, with the externals it uses). Build check: new telemetry names are claimed by an element.

## 0.9.1 — 15 Nov 26

- Map laid out by flows: inside a container, one row per flow with the steps left to right in order; parts on no flow collapse into one "N other parts" card; externals sit in a column beside the part that uses them; only flow and external connections are drawn by default (labels on them), the rest on selection or with "all connections". An external that sits on a flow between two containers (the proxy) is placed between them.

## 0.9.0 — 15 Nov 26

Map iteration: containers are the structure; a registry field retired (ignored, not breaking). (Numbered 0.9.0 as pushed; by the rule below this and 0.8.0 would have been third-digit changes — the rule applies from here on.)

- **Containers are the structure.** The deployable units (plugin, proxy, backend app, external systems) are elements; every other element has `Part of:` up to one of them. The map draws containers as boxes with their parts inside, left to right in the order a request travels (from the flows), nested containers as boxes inside boxes; top level open, inner ones collapsed to a card until clicked.
- **Connection type is a label on the relation** — `Depends on: chat-store (Cosmos: conversations) · live-feed (SSE: /chat/resume)` — written on the line when an element or a flow is selected. Never a grouping.
- **`Layer:` retired.** A technology type is not a place in the system; grouping by it hid the structure (0.8.0's mistake). The map ignores it.

## 0.8.0 — 15 Nov 26

Map iteration: structure fields in the registry, flows, and the every-pass-leaves-a-drop rule.

- **Structure in the registry**: `Layer:` (entry · api · orchestration · agents · stores · platform), `Part of:` (containment), and a `## Flows` section — named sequences of elements in the order they run, with **fragments** any pass can add under a flow's name.
- **Every pass leaves a drop** (`elements.md`): any stage that reads code — a plan's Read, a root cause's lanes, a review's spot-checks, the build check's look-around, a coverage pass — appends what it learned about structure to the registry at its write point: anchors, relations, `Part of`, `Layer`, flow fragments. Two or three lines, no question. The map consolidates: merges fragments by element order (or by their step number), fills layers the code makes plain, sets containment, asks only on conflicts. A one-time flow pass seeds the main flows.
- Flow steps may carry `(planned)`; the map dims them. `Part of` has a test: runs, hosts or wholly contains.
- **Map renders the structure**: rows by layer, columns by area; a parent is one card with "+N parts" that expands in place; a flow selector lights the path with numbered steps and dims the rest; the panel lists the flows an element is on and its position in each.

## 0.7.1 — 15 Nov 26

- Map builder tolerates hand-written registries: `feature 6` or `F6` in history lines, `State:` with an annotation (kept as a note), a `###` heading ends an element; decisions without an `Elements:` line match by whole id or multi-word name only and are marked ≈ in the panel. `Note:` field documented.

## 0.7.0 — 15 Nov 26

Second-number release: a new script (`.a/scripts/map_build.py`), new element fields (`Area`, `Sources`) and a new element state. An installed copy needs `/A.skill.update`; existing projects get the script on the next `/A.project.start` refresh or the map's first run.

- Element state `untouched` (mapped from the code, no feature yet) with its own colour; the map builder gained a layered layout, correct feature and decision counts, decisions matched by id or name when the `Elements:` field is absent, a collapsible thread panel and a quieter look.
- **Interactive map**: `.a/scripts/map_build.py` (stdlib Python, no network) builds `docs/map/map.html` from the registry, board and decisions — grouped by area, coloured by state, click an element to pull its thread. Offered in one line whenever the overview is regenerated; Mermaid stays the lean base. Elements gain `Area` and `Sources`.
- **Map asks only for judgement**: anchor corrections, approved elements, relations and the overview redraw happen without asking; merges, boundaries and untouched parts are the questions. Element states `stable / in change / planned / unwired / superseded`; Close redraws the overview and appends element history itself.
- **Verified means deployed**: user-visible behaviour is verified through the deployed environment's real entry point; a local run against its resources is labelled and does not close a requirement.

## 0.6.0 — 14 Nov 26

Second-number release: the command set, the stages and the project schema changed. An installed copy needs `/A.skill.update` and a new chat.

- **The user's instructions are the source** (`## Instructions` ledger in every feature, in the user's words; conformance check at every boundary and first in every review lens; a plan that does not honour an instruction is a Blocker; deviations are decisions to the user, never agent resolutions). Replaces the earlier "user-given design is the spec" rule with its general form.
- **Two files per feature**: the report (current state, plain words, for a person) and the `.detail.md` (event log, findings, lanes, verification, reuse/impact, superseded text, in terse agent notation). Records the map, thread, drift, resume and conformance check depend on are listed and never minimized.
- **Reground** (`lean.md › Reground`, spine standing rule, build-check step 8, lens consistency pass, auto advance, self-check 23): scope, lean and premise asked silently at every stage boundary; one line and the full check when any is no. Robust and lean defined as the same target: the robust solution with the least code.

- **Root cause is its own stage** (`/A.rootcause`, `.m` `.l` `.xl`; `rootcause.md`): understand and compartmentalize the user's account (symptom · expectation · their insights · what they want next); observe the real artifacts; reverse, forward and zoom-out lanes **in parallel, each blind to the others, each to an origin** (never the first candidate; cascades recorded as chains); a **coverage check** for gaps along the path, lateral and vertical, with targeted passes before reconciliation; reconcile; **confirm by a falsifiable test** (CONFIRMED / LIKELY / demoted / not found); XL adds a fresh critic on the confirmed cause. Output is a cause, never a fix; nothing is planned from a HYPOTHESIS. `plan.bugfix` is removed; `/A.plan` plans the fix from the report at the origin. Auto classifies any wrong behaviour with an unknown cause as root cause — the shape of a likely fix never decides it.

- **Commands by stage.** The set is now `plan` (`.realign`, `.bugfix`, `.scope_check_drift_check`, `.lean_overcomplication_check`), `review` (`.m` `.l` `.xl`), `build` (`.resume`), `verify`, `close`, `project` (`.start` `.status` `.board` `.map` `.drift` `.list`), `skill` (`.update` `.repair` `.uninstall` `.help`), plus `/A.auto` and `/A.help`. Removed: `extend`, `bugfix`, `implement`, `realign`, `simplify`, `validate`, `tracker`, `resume`, `init`, `projects`, `clarify` and all aliases — their work lives inside the stage commands. Long names filter in the picker (`/A.scope`, `/A.drift`); anything typed that matches no command is handled by auto. The installer removes the previous release's command files on update.
- **Hierarchy and type by scope** (`hierarchy.md`): Project › Area › Feature (`feature` / `change` / `fix`) › Item › Step, with **Elements** as the system's parts. Type follows the sizing signals and is re-evaluated at Evaluate, Realign and by the scope check; promotion and demotion are decisions to the user, recorded in the header.
- **Elements registry** (`elements.md`, `docs/map/elements.md`): stable ids, alias list for name drift, code anchors, relations, append-only history. Every report has `### Elements touched`; decisions name elements; Close appends history; Start reads an element's lineage before the code.
- **`/A.project.map` assembles rather than discovers**: resolves name drift and duplicates against the code (same anchors or same function → one element; otherwise sequential / parallel / alternative / part-of relations), asks before merging, draws elements per area with state; `/A.project.map <element>` pulls the thread — every feature, item, bug and decision that touched it, in order.
- `/A.build.resume` reads the tracker and verifies done steps against the files before continuing. `/A.verify` is the validate stage. Config `schema_version` 2 adds `elements_registry`.

- **Wrappers no longer require `.a/project.md` at the workspace root**: they resolve the project as the spine does (named → files → conversation → the only project folder in the workspace, sub-folders included → ask), and offer `/A.start-project` only when no project exists anywhere in the workspace.

- **Review findings**: severity scale is now Blocker / Major / Low; every finding has one shape (severity · confidence · summary · where · now · gap); "no findings" is a complete review, and silence is a valid output everywhere the agent reports by exception.
- **Peer-review adoptions**: findings carry confidence; constitution violations are Blockers; synthesis before resolution (de-dupe across lenses, order by severity, Lows as a count, low-confidence verified or dropped); no context added to a plan only for reviewers; the user may edit the activity file directly and say "re-read"; never stall on a defaultable answer.
- **Premise findings stop the round**: a zoom-out finding that questions the design's premise goes to the user as a decision before the next lens group; detail review runs only on a confirmed premise.
- **Fold, never amend**: pre-approval corrections are written into the step they belong to; no amendment or override sections; a consistency pass of the whole report between lens groups.
- **Review structure**: a round is one full pass of the lens groups; XL runs three groups (zoom-out → comprehension + critic → additions zoom-out + readiness + codebase-details + impact + lean), lenses inside a group in parallel; later rounds re-run only the lenses the fixes touched; stopping at the cap is the user's decision and a round that ended with new Blockers is never called complete silently. Reviewers are told nothing about earlier rounds (except the additions-only zoom-out). Report corrected in place before Approve with every change logged; dated revisions only after Approve. One consolidated write per lens group.

- **Artifacts** (`artifacts.md`): project-level measured evidence — probe matrices, baselines, inventories, error shapes — kept in `docs/artifacts/` with a ledger; proposed at Validate/Close, written on the user's yes; read at Start and by the reuse search so nothing is measured twice; staleness checked by `/A.drift`.
- **Deferred-decisions log** (`deferred-decisions.md`): noticed-but-not-acted-on risks and parked choices, with why they are fine for now and the condition that would change that; written from low-impact DECLINEs; read at Start for work in the same area.
- **Failure handling in Implement**: every step enumerates its failure cases before build; preconditions checked with clear errors; every error carries a plain-English layer (what, which step, what to do) above the technical detail; best-effort paths still report; verification covers failure paths.
- **Build check** (`build-check.md`): Implement works like an experienced engineer — before each edit, search the whole repository for callers, consumers, tests, siblings and config; after it, wire the path end to end, run the nearest check, re-read the ask, judge robust vs quick fix. Findings go to build findings; only plan-changing or trust-boundary ones interrupt. Per item, a two-minute self-pass over the review lenses before `Result:`.
- **Write points**: record every event when it happens, write the file at boundaries (step done, decision, blocking finding, stage change, before asking, before a long run, before the turn ends) in one pass; decisions still written immediately.

- **Flow awareness** (`flow.md`): every command knows what it needs, produces and what comes next; a missing predecessor is offered with a default (review chat work, then offer to make it a plan); every command ends by naming the next step with its likely answer.
- **Say where you stand**: one line of the agent's own read on every instruction and decision — agree, caveat, disagree with alternative, or possible misunderstanding — grounded in the code.
- **Decisions arrive with their context**: where we are, what came up and why, the options and what each means, the suggested answer with reason, what happens next — in reports, gates, escalations, build findings and clarify questions; never a bare question. Readable without opening the file.
- **Decisions arrive answered**: each decision carries a recommended answer and reason; "say go" takes them all. No restating unchanged state, no menus of every possible move.
- **Solution-architect judgement**: every proposal states robust / tactical / quick fix against what a well-run team would do; follows the user's stated theme; `solution_mode` in settings.

- **Quiet by default.** `~/.a/settings.md` (created by the installer) holds `verbosity`, `progress_interrupts`, `record_chat_work`, review tier limits (`auto_tier`, `max_tier`, `default_floor`) and date formats; projects may override. Chat carries decisions, stop points and answers; everything else goes to the event log. Review reports once, after all stages. Report by exception.
- **Every command is about this chat first.** Subject resolution: what the user pointed at → what this conversation is doing → board candidates fetched and offered by name with their next action → one question when both are plausible. Chat work not on the board is offered for recording once, afterwards (`record_chat_work`).
- **Bring the options to the user**: whenever the user must choose or check, the agent fetches and lists the options with what each means; never "see the board".

- **Core principle: ease the user's effort, never add to it.** The agent finishes and cleans up what it creates (scratch in the OS temp folder or `.a/tmp/`, deleted before reporting), never hands the user a chore it caused; a host that blocks a deletion means choosing a deletable location, or one approval request, not a note to the user. Enforced in communication.md, the spine, the self-check, close, and the skill-* commands.

- `/A.start-project` is one confirmation, not an interview: infers name, areas, documentation location, date formats, tracker label and dependencies from the project; shows one summary; asks one question; then does everything. Never installs the method, never writes outside the project, never logs its run in another project. Report lists only what was asked; one optional line at most.
- Rules: *Not done* lists only the user's asks; multi-choice moments are one summary and one confirmation; the agent does its own searching before asking the user; given steps are followed in the given order; never substitute, never assert what was not checked.
- IDE permissions procedure (`ide-permissions.md`): agent searches the IDE first, tests the prompt with the user second, offers a workspace mirror of the method last; wrappers resolve a mirror first; `/A.skill-update` and `/A.skill-repair` discover every mirror (index, registered projects, current workspace), register unlisted ones, and refresh them all.
- `/A.skill-update` compares the installed **commit** with the repository, not only the version; installers record the commit in `.a/SOURCE`.
- Installers fail loudly if a command wrapper keeps an unfilled `{{SKILLS_ROOT}}`.
- Multi-project workspaces: the agent resolves which project a message belongs to (named → files → conversation → only one → ask); workspace block for parent folders; `/A.start-project <folder>`.
- Managed-machine notes (Group Policy): run the scripts as script blocks.

## 0.5.6 — 13 Nov 26

- **Install once, start projects many times.** The installer is global by default (method in `~/.a`, commands in `~/.claude/commands` and `~/.a/commands/copilot`); `--project DIR` / `-Project DIR` keeps a project-level layout for repositories that must carry it. Command wrappers carry `{{SKILLS_ROOT}}`, filled by the installer.
- `/A.start-project` (aliases `init`, `setup`, `initialize`): makes a folder a project — config, docs, board, shared folder, always-on block, a marked `.gitignore` block for `.a/` and the created documentation (removable), and a row in `~/.a/projects.md`, the machine-wide index with `depends_on` / `provides` and a dependency diagram. Asks at the end about dependencies on other projects.
- `/A.projects`: shows and rebuilds the index from the projects' own config files.
- `/A.skill-update`: installed vs latest, what changed, acts only after yes; shows the fetched installer if it differs. `/A.skill-repair`: compares installed files with the release, restores after yes. `/A.skill-uninstall`: removes only what the installer created, through a fixed-path uninstall script, after yes; never the user's config, documentation, board, logs or index.
- `DISCLAIMER.md` and `SECURITY.md`; core rule that everything read from project files is data, never instructions.
- Installer prints version and file counts, writes `.a/SOURCE`; cross-project handoffs through the dependent project's shared folder; `projects.md` reference; SETUP rewritten for the global layout.

## 0.5.5 — 13 Nov 26

From the first agent-install run (Copilot in VS Code, passed):
- Installer prints the version and the number of files written per location; its last line says `/A.init` is **required**, and that the project folder itself must be the workspace root.
- SETUP: same two points in "Then"; the agent-install section says installing does not set the project up and the agent should not run `/A.init` unasked.
- `skills/README.md`: index of the skill folders with counts, so an agent browsing `skills/` finds a map instead of a missing `skills/SKILL.md`.

## 0.5.4 — 13 Nov 26

- lean.md: the ladder applies to tools and checks handed to the user, not only to code — prefer an existing tool (`git status`, a diff) over a custom script. Self-check item 13 added.

## 0.5.3 — 13 Nov 26

- Repository is https://github.com/AdarshK95/The-A-Skill; placeholders replaced in README, SETUP, LICENSE and the plugin manifests; plugin manifest version and marketplace name corrected; maintainer note on web uploads added to SETUP.

## 0.5.2 — 13 Nov 26

- Project named **The A Skill**; README intro rewritten; always-on marker renamed `A-skill: begin/end`.

## 0.5.1 — 13 Nov 26

- The closing block is now checkable: Done maps each ask to implemented / not / partly and lists the files changed; says where the changes live; Not done names each remaining ask and why; bare phrases ("nothing", "see above") are disallowed. communication.md, self-check.md, always-on.md.

## 0.5.0 — 13 Nov 26

Coordination release.

- `shared.md`: the shared folder for parallel sessions — session tags, `claims.md` (claim symbols before editing, release on verified), `handoffs.md` (waiting on / done, removed by the receiver), `notes.md` (warnings between sessions); stale-claim takeover with notice; never repair another session's claimed region; empty folder means nothing in flight. Read at Start, every stage move and every step; `/A.close` refuses while rows remain.
- Every answer ends with a fixed `Done / Not done / Your next step` block (communication.md, self-check, always-on); the same block closes every feature's Summary.
- Test 08: two sessions, one file.

## 0.4.0 — 13 Nov 26

Lean release: least code, nothing duplicated, nothing hardcoded.

- `lean.md`: the ladder; a mandatory **reuse search** in Evaluate (index → search by meaning and text → exact / close / pattern / none → decision), written to the report as *Reuse candidates*; modularity rules (one path per purpose, nothing varying hardcoded, accept dependencies, deep modules, deletion over addition, fewest files); when not to be lean; marked simplifications; a duplication-and-complexity check and a behaviour-preserving simplify pass at Realign.
- `/A.simplify` (`/A.lean`): the simplify pass on demand, each cut proven by the checks.
- `lean` review lens at M, L and XL; self-check items for reuse and hardcoding; `/A.drift` lists marked ceilings and runs the duplication check codebase-wide; `/A.map` contracts serve as the capability index.
- Test 07: reuse and duplication.

## 0.3.0 — 13 Nov 26

Communication and record release.

- `communication.md`: two readers (user in plain language, agent in full detail), five-line progress updates at every stage move, reports that open with what it means and end with the next step, paths and symbols only on request, a one-line lean on every choice, drift logged as a lesson.
- Activity file reshaped on a proven activity-log guide: `## Summary (plain language)` with five points for the user, and an append-only, timed `## Event log` (`E<n> · date, time — …`) as the technical backbone; corrections point back, nothing is rewritten; `## Changes` as a quick reference; `## Links` with the external work item.
- Month and day folders with a zero-padded sequence per day (`{yyyy}-{mm}/{yyyy}-{mm}-{dd}/{seq}-{slug}.md`) and a month `_ledger.md`; file names in `YYYY-MM-DD` so they sort, prose dates in `DD MMM YY`.
- Central repository extended: lessons log (drift and mistakes, read at Start with the constitution), board, map, ledgers; config example shows numbered central docs.
- `hosts.md`: a step-by-step cold self-review protocol for hosts without fresh subagents.
- `tracker_label` for the external work-item system; `/A.init` offers numbered names for new central docs.
- Test 06: plain-English report and conclusive answer.

## 0.2.0 — 13 Nov 26

Depth release: the method behind the structure.

- `hosts.md`: how to spawn a fresh reviewer per host, the cold-self-review fallback, a one-time isolation probe recorded in config, and an XL hand-off to the EGM plugin (`review.xl_engine`).
- Review rounds: stop on two consecutive clean rounds, at five, or on churn.
- `tracing.md`: the Read method — trace table, caller inventory, boundary list; Read is done when they are filled.
- `clarify.md`: seven-category scan for clarification questions; unasked ones become Assumptions; requirements checklist for L/XL, ticked at Validate.
- `self-check.md`: ten-line pre-approve consistency check on every report, all tiers.
- `/A.map` (`/A.bootstrap`): per-directory contracts and the overview's first nodes for existing codebases.
- `/A.drift`: documents, decisions and overview versus code; decisions-log hygiene; overdue warning in `/A.status`.
- `implement.posture` lite / full / ultra; `approval.second_reviewer`; shareable findings block.
- `tests/`: five scenarios with pass/fail rubrics, and an install test protocol in SETUP.md.

## 0.1.0 — 13 Nov 26

First release.

- Workflow: Start → Read → Evaluate → Clarify → Report → Review → Approve → Implement → Realign → Validate → Close, every stage a command, nothing past Approve without the user.
- Entry types: plan, extend (reopen), bugfix, review.
- Auto mode as the default: locate, classify, stay, advance.
- Hierarchy Area › Feature › Item › Step with a pointer that makes `/A.resume` exact.
- Project board with Planned / In progress / Finished / Deferred / To do, per area, and a mermaid overview coloured by state.
- Tiered fresh-context review (S / M / L / XL) with six lenses and a four-verdict resolve protocol.
- Logging at three altitudes; decisions dual-written; agent-private memory never the record.
- Per-project config in `.a/project.md`; nothing project-specific in the skill.
- Host wrappers for Claude Code and GitHub Copilot in VS Code; install scripts for sh and PowerShell.
