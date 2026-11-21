#!/usr/bin/env sh
# Install The A Skill. Default: once per machine (global). Then run /A.project.start in each folder you want as a project.
#   sh install.sh                 global: method in ~/.a, commands in ~/.claude/commands and ~/.a/commands/copilot
#   sh install.sh --project DIR   project-level: everything inside DIR (for a repository that must carry the method)
# Idempotent: re-running updates the method and commands, never a project's documents or config.
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
if [ "${1:-}" = "--project" ]; then
  DEST="$(cd "$2" && pwd)"; GLOBAL=0
  SKILLS_ROOT=".a/skills"; COPILOT_DIR="$DEST/.github/prompts"
else
  DEST="$HOME"; GLOBAL=1
  SKILLS_ROOT="$HOME/.a/skills"; COPILOT_DIR="$HOME/.a/commands/copilot"
fi
mkdir -p "$DEST/.a/skills" "$DEST/.a/templates" "$DEST/.claude/commands" "$COPILOT_DIR"
echo "Installing The A Skill from $SRC into $DEST"

cp -R "$SRC/skills/." "$DEST/.a/skills/"
cp -R "$SRC/templates/." "$DEST/.a/templates/"
cp "$SRC/install.sh" "$SRC/install.ps1" "$SRC/uninstall.sh" "$SRC/uninstall.ps1" "$DEST/.a/templates/" 2>/dev/null || true
cp "$SRC/registry.md" "$DEST/.a/registry.md"
cp "$SRC/VERSION" "$DEST/.a/VERSION"
COMMIT="$(git -C "$SRC" rev-parse HEAD 2>/dev/null || echo unknown)"
printf "repository: https://github.com/AdarshK95/The-A-Skill\ninstalled: %s\nscope: %s\ncommit: %s\n" "$(date '+%d %b %y, %I:%M %p')" "$([ "$GLOBAL" = 1 ] && echo global || echo project)" "$COMMIT" > "$DEST/.a/SOURCE"
[ -f "$DEST/.a/projects.md" ] || [ "$GLOBAL" = 0 ] || cp "$SRC/templates/projects.md" "$DEST/.a/projects.md"
SETTINGS_MD="$DEST/.a/settings.md"
[ -f "$SETTINGS_MD" ] || cp "$SRC/templates/settings.md" "$SETTINGS_MD"
# Settings a newer version adds reach an existing settings.md: each missing top-level key is inserted with its default and
# comment lines before the closing ---; a value the user set is never changed.
# ponytail: top-level keys only; a key added later under an existing block (review:) is not merged. A YAML-aware merge is the upgrade.
awk 'NR==FNR { if ($0 ~ /^[a-z_]+[ \t]*:/) { k=$0; sub(/[ \t]*:.*/, "", k); have[k]=1 } next }
     /^[a-z_]+[ \t]*:/ { k=$0; sub(/[ \t]*:.*/, "", k); take=!(k in have); if (take) print; next }
     /^[ \t]+(#|[a-z_]+[ \t]*:)/ { if (take) print; next }
     { take=0 }' "$SETTINGS_MD" "$SRC/templates/settings.md" > "$SETTINGS_MD.add"
NEW_KEYS="$(grep -E '^[a-z_]+[[:space:]]*:' "$SETTINGS_MD.add" | sed 's/[[:space:]]*:.*//' | tr '\n' ' ')"
if [ -s "$SETTINGS_MD.add" ]; then
  { echo "# Added by the installer ($(cat "$SRC/VERSION")): new settings with their defaults"; cat "$SETTINGS_MD.add"; } > "$SETTINGS_MD.ins"
  awk -v ins="$SETTINGS_MD.ins" '/^---[ \t]*$/ { n++; if (n == 2) while ((getline l < ins) > 0) print l } { print }
       END { if (n < 2) while ((getline l < ins) > 0) print l }' "$SETTINGS_MD" > "$SETTINGS_MD.new" && mv "$SETTINGS_MD.new" "$SETTINGS_MD"
fi
rm -f "$SETTINGS_MD.add" "$SETTINGS_MD.ins"
ALWAYS_ON=1; grep -Eq '^always_on[[:space:]]*:[[:space:]]*off' "$SETTINGS_MD" && ALWAYS_ON=0
rm -f "$DEST/.claude/commands"/A.*.md "$COPILOT_DIR"/A.*.prompt.md
for f in "$SRC"/commands/claude/A.*.md; do sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$f" > "$DEST/.claude/commands/$(basename "$f")"; done
for f in "$SRC"/commands/copilot/A.*.prompt.md; do sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$f" > "$COPILOT_DIR/$(basename "$f")"; done

if grep -rl "{{SKILLS_ROOT}}" "$DEST/.claude/commands" "$COPILOT_DIR" >/dev/null 2>&1; then echo "ERROR: a command file still has an unfilled {{SKILLS_ROOT}}; install incomplete."; exit 1; fi

# On by default (global only): a pointer every message starts with, so a message with no /A.* command runs auto mode.
# ponytail: project-level installs get no hook (no path that works for every clone); their always-on block stays at the top of CLAUDE.md instead.
HOOK_NOTE="not added (project-level install)"
if [ "$GLOBAL" = 1 ]; then
  POINTER="$DEST/.a/auto-pointer.md"
  # The pointer is printed by a shell before every message; plain ASCII survives every shell's output encoding.
  if LC_ALL=C grep -q '[^[:print:][:space:]]' "$SRC/templates/auto-pointer.md"; then echo "ERROR: templates/auto-pointer.md has non-ASCII characters; the hook output would be garbled on some shells."; exit 1; fi
  sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$SRC/templates/auto-pointer.md" > "$POINTER"
  mkdir -p "$DEST/.copilot/instructions"
  if [ "$ALWAYS_ON" = 1 ]; then { printf -- "---\napplyTo: '**'\ndescription: The A Skill is the default workflow\n---\n\n"; cat "$POINTER"; } > "$DEST/.copilot/instructions/a-skill.instructions.md"
  else rm -f "$DEST/.copilot/instructions/a-skill.instructions.md"; fi
  PY=""; for c in python3 python; do "$c" -c "" 2>/dev/null && PY="$c" && break; done   # skips stubs that exist but do not run
  # The hook names its shell (bash: this installer runs in it) and exits 0 either way; a missing pointer says so on every message.
  HOOK_CMD="cat \"$POINTER\" 2>/dev/null || echo \"The A Skill: pointer file missing ($POINTER). Run /A.skill.repair.\""
  if [ -n "$PY" ]; then HOOK_NOTE="$("$PY" "$SRC/templates/settings_hook.py" "$DEST/.claude/settings.json" "$([ "$ALWAYS_ON" = 1 ] && echo "$HOOK_CMD")" bash || echo "NOT added: settings.json could not be updated; add it by hand (SETUP.md)")"
  else HOOK_NOTE="NOT added: no working Python (python3 or python) to merge settings.json; add it by hand (SETUP.md)"; fi
  [ "$ALWAYS_ON" = 1 ] || HOOK_NOTE="removed: always_on is off in $SETTINGS_MD ($HOOK_NOTE)"
  DETECTED="sh; Python: ${PY:-none}; hook shell: bash"
  # Projects that need /A.project.repair - only those are named; a healthy project is not mentioned.
  if [ -n "$PY" ]; then REPAIR="$("$PY" "$DEST/.a/templates/project_check.py" "$DEST/.a" 2>/dev/null)"
  else REPAIR="  (project check skipped: no working Python; run /A.project.repair in each project to check it)"; fi
else DETECTED="sh; no hook (project-level install)"; fi
n_skills=$(find "$DEST/.a/skills" -type f -name '*.md' | wc -l | tr -d ' ')
n_claude=$(ls "$DEST/.claude/commands"/A.*.md 2>/dev/null | wc -l | tr -d ' ')
n_copilot=$(ls "$COPILOT_DIR"/A.*.prompt.md 2>/dev/null | wc -l | tr -d ' ')
echo "Installed (version $(cat "$DEST/.a/VERSION"), commit $(echo "$COMMIT" | cut -c1-7)):"
echo "  $DEST/.a/skills                  $n_skills files   (the method)"
echo "  $DEST/.claude/commands/A.*.md    $n_claude files   (Claude Code: /A.plan, /A.show, ...)"
echo "  $COPILOT_DIR/A.*.prompt.md       $n_copilot files   (Copilot in VS Code)"
echo "  On by default (auto mode every message): Claude Code hook $HOOK_NOTE"
echo "  Detected: $DETECTED"
[ "$GLOBAL" = 1 ] && echo "                                   Copilot: $([ "$ALWAYS_ON" = 1 ] && echo "$DEST/.copilot/instructions/a-skill.instructions.md" || echo "off (always_on: off)")"
[ -n "$NEW_KEYS" ] && echo "  New settings added to $SETTINGS_MD with their defaults: $NEW_KEYS"
echo
if [ "$GLOBAL" = 1 ]; then
  echo "INSTALLATION COMPLETE. The A Skill $(cat "$DEST/.a/VERSION") is installed for this machine (global)."
  echo
  echo "To see the /A.* shortcuts in VS Code (Copilot), two steps remain:"
  echo "  1. Settings -> chat.promptFilesLocations -> add: $COPILOT_DIR"
  echo "  2. Developer: Reload Window"
  echo "  3. The IDE will ask before reading the method files (they live in $DEST/.a, outside your workspace)."
  echo "     Agents: follow $DEST/.a/skills/core/references/ide-permissions.md — search the IDE settings for a permanent"
  echo "     allowance first; if none, test the prompt once with the user; if still nothing permanent, offer a local mirror of the method inside the workspace. Ask before each change."
  echo "Claude Code needs nothing. (Agents: ask the user for approval, do 1 and 2, confirm /A.help appears, then do 3.)"
  echo
  echo "The skill remembers work PER PROJECT: in any folder you want to work in, run /A.project.start once."
  echo "Everything done there (board, logs, decisions) becomes that project's memory, separate from every other project. /A.project.list shows them all."
  if [ -n "$REPAIR" ]; then
    echo
    echo "PROJECTS TO BRING UP TO DATE - open each one and run /A.project.repair (it shows what it will change and asks first):"
    echo "$REPAIR"
  fi
else
  echo "This was a PROJECT-LEVEL install into $DEST: the commands are read from this folder, so it must be the workspace root for them to appear (the global install has no such limit)."
  echo "Open this folder, start a new chat, and run /A.project.start (required; nothing is remembered without it)."
fi
