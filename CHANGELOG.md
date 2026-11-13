# Changelog

## 0.5.7 — 13 Nov 26

Seamless setup.

- `/A.start-project` is one confirmation, not an interview: infers name, areas, documentation location, date formats, tracker label and dependencies from the project; shows one summary; asks one question; then does everything. Never installs the method, never writes outside the project, never logs its run in another project. Report lists only what was asked; one optional line at most.
- Rules: *Not done* lists only the user's asks; multi-choice moments are one summary and one confirmation; the agent does its own searching before asking the user; given steps are followed in the given order; never substitute, never assert what was not checked.
- IDE permissions procedure (`ide-permissions.md`): agent searches the IDE first, tests the prompt with the user second, offers a workspace mirror of the method last; wrappers resolve a mirror first; `/A.skill-update` refreshes mirrors.
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
