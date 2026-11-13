#!/usr/bin/env sh
# Install The A Skill. Default: once per machine (global). Then run /A.start-project in each folder you want as a project.
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
[ -f "$DEST/.a/settings.md" ] || cp "$SRC/templates/settings.md" "$DEST/.a/settings.md"
for f in "$SRC"/commands/claude/A.*.md; do sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$f" > "$DEST/.claude/commands/$(basename "$f")"; done
for f in "$SRC"/commands/copilot/A.*.prompt.md; do sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$f" > "$COPILOT_DIR/$(basename "$f")"; done

if grep -rl "{{SKILLS_ROOT}}" "$DEST/.claude/commands" "$COPILOT_DIR" >/dev/null 2>&1; then echo "ERROR: a command file still has an unfilled {{SKILLS_ROOT}}; install incomplete."; exit 1; fi
n_skills=$(find "$DEST/.a/skills" -type f -name '*.md' | wc -l | tr -d ' ')
n_claude=$(ls "$DEST/.claude/commands"/A.*.md 2>/dev/null | wc -l | tr -d ' ')
n_copilot=$(ls "$COPILOT_DIR"/A.*.prompt.md 2>/dev/null | wc -l | tr -d ' ')
echo "Installed (version $(cat "$DEST/.a/VERSION"), commit $(echo "$COMMIT" | cut -c1-7)):"
echo "  $DEST/.a/skills                  $n_skills files   (the method)"
echo "  $DEST/.claude/commands/A.*.md    $n_claude files   (Claude Code: /A.plan, /A.bugfix, ...)"
echo "  $COPILOT_DIR/A.*.prompt.md       $n_copilot files   (Copilot in VS Code)"
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
  echo "The skill remembers work PER PROJECT: in any folder you want to work in, run /A.start-project once."
  echo "Everything done there (board, logs, decisions) becomes that project's memory, separate from every other project. /A.projects shows them all."
else
  echo "This was a PROJECT-LEVEL install into $DEST: the commands are read from this folder, so it must be the workspace root for them to appear (the global install has no such limit)."
  echo "Open this folder, start a new chat, and run /A.start-project (required; nothing is remembered without it)."
fi
