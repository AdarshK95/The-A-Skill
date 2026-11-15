# <nn> · <feature title> — detail

_Agent notation (`core/references/logging.md › Agent notation`): one record per line, fields ` · `-separated, refs `path:symbol:line`, no sentences. Append-only except the Reuse and Impact tables, which are current-state. The report (`<nn>-<slug>.md`) points here; nothing here repeats the report._

## Event log
- E1 · <DD MMM YY, hh:mm AM/PM> · <what> · <refs>

## Findings
- F1 · round <n> · <lens> · <Blocker|Major|Low> · <high|medium|low> · <path:symbol:line> · <gap> · <FIX|ESCALATE D<n>|CONTEST <evidence>|DECLINE <where>>

## Root cause (when run)
- L-reverse · <chain origin → … → symptom> · <refs> · coverage <segments>
- L-forward · <candidates with conditions> · <refs> · coverage <segments>
- L-zoom · <kind: design|regression|data|config|misuse> · <refs>
- C · <segment> · <layer> · <lanes that examined it> · <could carry error y/n>
- V<n> · <candidate> · <prediction> · <test> · <result CONFIRMED|LIKELY|demoted>

## Build findings (resolved)
- BF1 · <step> · <what> · <path:symbol:line> · <handling> · <date>

## Verification
- V<n> · <requirement> · <command> · <result> · <date>

## Reuse (current)
| need | candidate path:symbol | match | decision |
| --- | --- | --- | --- |

## Impact (current)
| boundary | path:symbol | risk if wrong |
| --- | --- | --- |

## Superseded
- <date> · <section> · <one line what changed and why> · old text ↓
