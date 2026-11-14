---
# The A Skill — machine-wide settings (~/.a/settings.md)
# Defaults are what the skill does on its own. Change any value; a project's .a/project.md may override any key for that project.
# Precedence: project.md > this file > skill defaults.

verbosity: quiet          # quiet: decisions, stop points, answers only; everything else in the event log
                          # normal: plus one line at each stage boundary
                          # verbose: plus progress every few steps (for debugging the skill)
progress_interrupts: blockers   # blockers: interrupt a running stage only for a blocking finding
                                # findings: also for any Major
solution_mode: balanced   # balanced: recommend the robust path, name quick fixes as such, follow the chat's theme when the user states one
                          # robust: always recommend the robust path   |   quick: prefer the quick fix, offer the robust one as follow-up
record_chat_work: ask     # when a command runs on work done in the chat that is not on the board:
                          # ask: offer once, afterwards, to record it as a feature
                          # always: record it   |   never: don't offer
review:
  auto_tier: on           # off: every feature is reviewed at `default_tier` unless the user sets a tier at the gate
  default_floor: S        # lowest tier a project may get
  max_tier: XL            # highest tier the rubric may choose on its own (S, M, L or XL); the user can still ask for more
  fresh_context: auto     # auto | always | never (see config-schema.md)
dates:
  date_format: DD MMM YY
  time_format: 12h
---

# About this file

Everything here is a default the skill applies unless a project says otherwise. `/A.project.start` copies `dates` and `review` into a new project's config so each project can diverge. Nothing in this file is project data; deleting it restores the skill's defaults.
