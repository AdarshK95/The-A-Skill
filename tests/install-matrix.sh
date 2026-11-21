#!/usr/bin/env sh
# Installer matrix for the on-by-default hook (install.sh / uninstall.sh). Runs the real scripts against throwaway
# home folders: settings.json missing, empty, full (other hook, token, non-English text), not plain JSON; and a
# machine with no working Python. Needs a working Python itself (to read the results).  sh tests/install-matrix.sh
# Exit code 0 = every check passed. Never touches the real ~/.claude.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(mktemp -d)"; FAIL=0
PY=""; for c in python3 python; do "$c" -c "" 2>/dev/null && PY="$c" && break; done
[ -n "$PY" ] || { echo "this test needs a working python3 or python"; exit 2; }
native() { command -v cygpath >/dev/null 2>&1 && cygpath -m "$1" || echo "$1"; }   # Windows Python cannot read /d/... paths
check() { if [ "$2" = 1 ]; then echo "ok   $1"; else echo "FAIL $1"; FAIL=$((FAIL+1)); fi; }
q() { "$PY" -c "import json,sys; s=json.load(open(sys.argv[1],encoding='utf-8')); $1" "$(native "$2")"; }   # q '<expr printing 1/0>' file
UNI='café 日本 —'
STUB="$ROOT/no-python-bin"; mkdir -p "$STUB"; for c in python3 python; do printf '#!/bin/sh\nexit 9009\n' > "$STUB/$c"; chmod +x "$STUB/$c"; done
echo "install-matrix on sh ($PY for reading results)"
for case in missing empty full notjson nopython; do
  H="$ROOT/$case"; S="$H/.claude/settings.json"; mkdir -p "$H/.claude"
  case $case in
    empty) : > "$S";;
    full|nopython) printf '{"env":{"FAKE_TOKEN":"keep-me","NOTE":"%s"},"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"echo other"}]}]}}' "$UNI" > "$S";;
    notjson) printf '// a comment\n{"env":{}}' > "$S";;
  esac
  before="$(cat "$S" 2>/dev/null)"
  if [ $case = nopython ]; then LOG="$(HOME="$H" PATH="$STUB:$PATH" sh "$REPO/install.sh" 2>&1)"
  else LOG="$(HOME="$H" sh "$REPO/install.sh" 2>&1; HOME="$H" sh "$REPO/install.sh" 2>&1)"; fi   # twice: must not duplicate
  P="$H/.a/auto-pointer.md"
  check "[$case] pointer is plain ASCII" "$(LC_ALL=C grep -q '[^[:print:][:space:]]' "$P" && echo 0 || echo 1)"
  check "[$case] Copilot instructions file written" "$([ -f "$H/.copilot/instructions/a-skill.instructions.md" ] && echo 1 || echo 0)"
  if [ $case = notjson ] || [ $case = nopython ]; then
    check "[$case] settings left byte-for-byte untouched" "$([ "$(cat "$S")" = "$before" ] && echo 1 || echo 0)"
    check "[$case] installer says NOT added" "$(echo "$LOG" | grep -q "NOT added" && echo 1 || echo 0)"
    continue
  fi
  ours='[h for g in s["hooks"]["UserPromptSubmit"] for h in g["hooks"] if "auto-pointer.md" in h["command"]]'
  check "[$case] exactly one A Skill hook after two installs" "$(q "print(int(len($ours)==1))" "$S")"
  check "[$case] hook names its shell" "$(q "print(int($ours[0].get('shell')=='bash'))" "$S")"
  CMD="$(q "print($ours[0]['command'])" "$S")"
  OUT="$(bash -c "$CMD")"; CODE=$?
  check "[$case] hook prints the pointer, exit 0" "$(echo "$OUT" | head -1 | grep -q '^The A Skill is the default workflow' && [ $CODE = 0 ] && echo 1 || echo 0)"
  if [ $case = full ]; then
    check "[$case] other hook, token, non-English text kept" "$(q "print(int(s['env']['FAKE_TOKEN']=='keep-me' and s['env']['NOTE']=='café 日本 —' and any(h['command']=='echo other' for g in s['hooks']['UserPromptSubmit'] for h in g['hooks'])))" "$S")"
  fi
  mv "$P" "$P.hidden"; OUT="$(bash -c "$CMD")"; CODE=$?; mv "$P.hidden" "$P"
  check "[$case] pointer missing: hook says so, exit 0" "$(echo "$OUT" | grep -q 'pointer file missing' && [ $CODE = 0 ] && echo 1 || echo 0)"
  HOME="$H" sh "$H/.a/templates/uninstall.sh" --yes >/dev/null 2>&1
  check "[$case] uninstall removes the hook" "$(q "print(int(not [h for g in s.get('hooks',{}).get('UserPromptSubmit',[]) for h in g['hooks'] if 'auto-pointer.md' in h['command']]))" "$S")"
  check "[$case] uninstall removes pointer and Copilot file" "$([ ! -e "$P" ] && [ ! -e "$H/.copilot/instructions/a-skill.instructions.md" ] && echo 1 || echo 0)"
  [ $case = full ] && check "[$case] after uninstall: other hook, token, non-English text intact" "$(q "print(int(s['env']['FAKE_TOKEN']=='keep-me' and s['env']['NOTE']=='café 日本 —' and len(s['hooks']['UserPromptSubmit'])==1))" "$S")"
done
# --- the machine: settings from an older version, always_on, and which projects need /A.project.repair
H="$ROOT/machine"; mkdir -p "$H/.a"; SET="$H/.a/settings.md"
printf -- '---\n# old settings\nverbosity: normal          # the user'"'"'s own value\nreview:\n  auto_tier: on\n---\n\n# About this file\n' > "$SET"
for p in healthy stale; do mkdir -p "$H/$p/.a"; done
cp "$REPO/templates/project.md" "$H/healthy/.a/project.md"
{ sed 's|{{skills_root}}|/x/.a/skills|g' "$REPO/templates/always-on.md"; printf "\n# the project's own rules\n"; } > "$H/healthy/CLAUDE.md"
printf -- '---\nproject_name: stale\ndocs_root: docs/\n---\n' > "$H/stale/.a/project.md"
printf "# the project's own rules\n\n<!-- A-skill: begin (managed by /A.project.start) -->\nan old block\n<!-- A-skill: end -->\n" > "$H/stale/CLAUDE.md"
mkdir -p "$H/stale/.a/scripts"; echo "# old copy" > "$H/stale/.a/scripts/map_build.py"
printf '| Project | Path |\n| --- | --- |\n| healthy | %s |\n| stale | %s |\n| gone | %s |\n' "$(native "$H/healthy")" "$(native "$H/stale")" "$(native "$H/gone")" > "$H/.a/projects.md"
LOG="$(HOME="$H" sh "$REPO/install.sh" 2>&1)"
FRONT="$(awk '/^---[ \t]*$/ { n++; next } n == 1' "$SET")"
check "[machine] new settings keys added inside the front matter" "$(echo "$FRONT" | grep -q '^always_on' && echo "$FRONT" | grep -q '^pages_server' && echo 1 || echo 0)"
check "[machine] the user's own setting value kept" "$(grep -q '^verbosity: normal' "$SET" && echo 1 || echo 0)"
check "[machine] installer says which settings it added" "$(echo "$LOG" | grep -q 'New settings added .*always_on' && echo 1 || echo 0)"
check "[machine] stale project named with its findings" "$(echo "$LOG" | grep 'stale (' | grep -q 'config lacks' && echo "$LOG" | grep -q 'not at the top of CLAUDE.md' && echo "$LOG" | grep -q 'older version' && echo "$LOG" | grep -q "old copies of the A Skill's helper scripts" && echo 1 || echo 0)"
check "[machine] missing project folder named" "$(echo "$LOG" | grep -q 'gone (.*no .a/project.md there any more' && echo 1 || echo 0)"
check "[machine] healthy project not mentioned" "$(echo "$LOG" | grep -q '  healthy (' && echo 0 || echo 1)"
sed -i 's/^always_on:[[:space:]]*on/always_on: off/' "$SET"; HOME="$H" sh "$REPO/install.sh" >/dev/null 2>&1
check "[machine] always_on off: no A Skill hook, no Copilot file" "$(q "print(int(not [h for g in s.get('hooks',{}).get('UserPromptSubmit',[]) for h in g['hooks'] if 'auto-pointer.md' in h['command']]))" "$H/.claude/settings.json" | grep -q 1 && [ ! -e "$H/.copilot/instructions/a-skill.instructions.md" ] && echo 1 || echo 0)"
sed -i 's/^always_on:[[:space:]]*off/always_on: on/' "$SET"; HOME="$H" sh "$REPO/install.sh" >/dev/null 2>&1
check "[machine] always_on back on: hook and Copilot file back" "$(q "print(int(len([h for g in s['hooks']['UserPromptSubmit'] for h in g['hooks'] if 'auto-pointer.md' in h['command']])==1))" "$H/.claude/settings.json" | grep -q 1 && [ -e "$H/.copilot/instructions/a-skill.instructions.md" ] && echo 1 || echo 0)"
LOG="$(HOME="$H" PATH="$STUB:$PATH" sh "$REPO/install.sh" 2>&1)"
check "[machine] no working Python: project check says it was skipped" "$(echo "$LOG" | grep -q 'project check skipped' && echo 1 || echo 0)"
rm -rf "$ROOT"
[ $FAIL = 0 ] && echo "all checks passed on sh" || echo "$FAIL check(s) FAILED on sh"
exit $FAIL
