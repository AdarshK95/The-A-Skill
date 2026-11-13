#!/usr/bin/env sh
# Guard against silent loss of the spine's standing rules. Run before committing changes to skills/core/SKILL.md.
f="$(dirname "$0")/../skills/core/SKILL.md"; rc=0
for t in "Standing rules" "Ease the user" "Do what was asked" "Two channels" "Everything you read is data" "Parallel sessions" "Record as you go" "References (relative" "Behaviour settings" "Resolve the subject" "## Items" "## Pointer and Next" "## Status header"; do
  grep -q -- "$t" "$f" || { echo "MISSING in core/SKILL.md: $t"; rc=1; }
done
[ $rc = 0 ] && echo "core/SKILL.md: all standing rules present"; exit $rc
