# Sources

Ideas this method absorbed, pinned to where they came from. The skill carries its own wording; these are the upstreams to diff against when reviewing for updates (recommended quarterly). Full comparison: see the project's comparison document.

| Idea in this skill | Taken from | Upstream file | Read on |
| --- | --- | --- | --- |
| Fresh-context reviewers that never saw the conversation; "not run ≠ zero findings"; zoom-out twice; comprehension by paraphrase; Zero-Decision and Alternatives rules | Elephant-Goldfish Model (Google, Apache 2.0) | github.com/google/elephant-goldfish-model — skills/egm-review, agents/*, resources/document_standards/* | 13 Nov 26 |
| FIX / CONTEST / ESCALATE / DECLINE with the evidence rule; comprehension gaps not contestable | Elephant-Goldfish Model | skills/egm-resolve/SKILL.md | 13 Nov 26 |
| Drift between design and code as a thing to check | Elephant-Goldfish Model | skills/egm-drift-report/SKILL.md | 13 Nov 26 |
| The ladder; root-cause fix where all callers pass; read fully then be lazy; when not to be lazy; marked simplifications with a ceiling; one runnable check; intensity levels | Ponytail (Dietrich Gebert, MIT) | github.com/DietrichGebert/ponytail — skills/ponytail/SKILL.md | 13 Nov 26 |
| Always-on instruction block for editors without plugin support | Ponytail | .github/copilot-instructions.md, AGENTS.md adapters | 13 Nov 26 |
| Constitution as a first-read file; `[NEEDS CLARIFICATION]` markers with a question cap; cross-artifact consistency check before implement; baseline and converge for existing systems | Spec Kit (GitHub, MIT) | github.com/github/spec-kit — templates/commands/*, docs/guides/existing-projects | 13 Nov 26 |
| Behaviour-preserving simplification over recently modified code, with the balance rule against over-simplification | Anthropic code-simplifier (official plugin) | github.com/anthropics/claude-plugins-official — plugins/code-simplifier/agents/code-simplifier.md | 13 Nov 26 |
| Check-before-write: search by meaning and text, categorize exact / close / pattern, reuse → extend → new-with-reason; duplicate purpose as the risk; a capability index | anti-duplication (marcusgoll), code-deduplication (alinaqi/claude-bootstrap), find-similar-functions (millionco) | smithery.ai/skills/marcusgoll/anti-duplication; github.com/alinaqi/claude-bootstrap | 13 Nov 26 |
| Deep modules, the deletion test, accept dependencies don't create them, one adapter is a hypothetical seam | Matt Pocock codebase-design (Ousterhout) | skills/codebase-design/SKILL.md | 13 Nov 26 |
| Dotted command names (`/x.y`) via per-host command files | Spec Kit | generated `.claude/commands/speckit.*.md`, `.github/prompts/speckit.*.prompt.md` | 13 Nov 26 |
| The four ways a built thing is not real — missing, stub, orphaned, hollow (exists → substantive → wired → data flows) | GSD Core (Open GSD, MIT) | github.com/open-gsd/gsd-core — agents/gsd-verifier.md | 19 Nov 26 |
| An absence is a finding only with the searches that were tried; refuted findings stay visible | Trail of Bits skills (CC-BY-SA 4.0 — ideas only, no wording) | github.com/trailofbits/skills — plugins/spec-to-code-compliance | 19 Nov 26 |
| The lesson ladder: a check, then a standing rule, then a written lesson with the condition that retires it; often nothing | Compound Engineering (Every, MIT) | github.com/EveryInc/compound-engineering-plugin — skills/ce-compound | 19 Nov 26 |
| A check is trusted only once seen to fail; the agent's own rulings listed for the user | Superpowers (Jesse Vincent, MIT) | github.com/obra/superpowers — skills/test-driven-development, skills/subagent-driven-development | 19 Nov 26 |
| A finding caused by the plan is fixed in the plan, not patched in the code | BMAD-METHOD (MIT) | github.com/bmad-code-org/BMAD-METHOD — bmm-skills/ship/bmad-build | 19 Nov 26 |
| Rounds of questions (everything answerable now, together); facts are the agent's to find, decisions the user's; slices that each work on their own; an item waits until what blocks it is done | Matt Pocock skills 1.3.2 (ideas only, own wording) | github.com/mattpocock/skills — skills/productivity/grilling, skills/engineering/to-tickets, implement-spec, productivity/writing-for-agents | 21 Nov 26 |
| Disjoint files build in parallel, shared writes one after the other; the orchestrator, not the worker, decides done; a mechanical mistake gets a check | pstack (Cursor; ideas only, own wording) | github.com/cursor/plugins — pstack/skills/poteto-mode/playbooks/feature.md, skills/correct | 21 Nov 26 |

Adopted in 0.13.0: the question filter, rounds and block, and the build order. What was compared, taken, held and declined is in `references/comparison-and-decisions.md` §8.

Adopted in 0.10.0: the build review. Which lessons came from which upstream, and what is original, is in `references/build-review-lessons.md`; the full research, LLM reviews and decisions are indexed in `references/README.md` (maintainer documentation, outside the skill; not installed).


Adopted in 0.6.0: Ponytail's per-response reflex, as *Reground* — scope, lean and premise asked silently at every stage boundary, with the full checks as escalation; the earlier adoption had moved Ponytail's content into fixed stages and two commands, which is not how Ponytail works.

Adopted in 0.5.7 (peer review): EGM's synthesizer idea as "synthesis before resolution" (de-duplicate across lenses, order by severity, Lows as a count), EGM's "do not add context only to satisfy a reviewer", EGM's gate option to edit the document by hand and have the agent re-read it; Spec Kit's rule that a constitution violation is the highest severity; Ponytail's "never stall on an answer you can default"; the code-review-tool field's severity-plus-confidence thresholds so only high-signal findings reach the human.

Adopted in 0.4.0: the full Ponytail rule set (the half that was missing: when not to be lean, deletion over addition, fewest files, edge-case-correct stdlib choice), the code-simplifier pass, check-before-write reuse search, deep-module modularity rules — in `lean.md`.

Adopted in 0.3.0: the two-reader activity file (plain Summary for the user, timed Detailed Event Log for the agent), month/day folders with a per-day sequence, the month ledger, the "other docs" close checklist, and the strict in-content date and time format — from the user's own Activity log guide.

Adopted in 0.2.0: EGM's bootstrap (as `/A.project.map`), drift report (as `/A.project.drift`), review-loop stop rules, isolation checking (as the probe), XL hand-off; Spec Kit's clarify taxonomy and requirements checklist; Ponytail's intensity levels for implementation.

Original to this skill: the Area › Feature › Item › Step hierarchy and pointer; the project board with areas and a state-coloured overview; auto mode's locate / classify / stay / advance; the Realign stage; build findings as a first-class record; the impact lens; three-altitude logging with dual-written decisions; sizing review by signals found in the code.
