# Changelog

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
