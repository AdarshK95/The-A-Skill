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
printf "repository: https://github.com/AdarshK95/The-A-Skill\ninstalled: %s\nscope: %s\n" "$(date '+%d %b %y, %I:%M %p')" "$([ "$GLOBAL" = 1 ] && echo global || echo project)" > "$DEST/.a/SOURCE"
[ -f "$DEST/.a/projects.md" ] || [ "$GLOBAL" = 0 ] || cp "$SRC/templates/projects.md" "$DEST/.a/projects.md"
for f in "$SRC"/commands/claude/A.*.md; do sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$f" > "$DEST/.claude/commands/$(basename "$f")"; done
for f in "$SRC"/commands/copilot/A.*.prompt.md; do sed "s|{{SKILLS_ROOT}}|$SKILLS_ROOT|g" "$f" > "$COPILOT_DIR/$(basename "$f")"; done

n_skills=$(find "$DEST/.a/skills" -type f -name '*.md' | wc -l | tr -d ' ')
n_claude=$(ls "$DEST/.claude/commands"/A.*.md 2>/dev/null | wc -l | tr -d ' ')
n_copilot=$(ls "$COPILOT_DIR"/A.*.prompt.md 2>/dev/null | wc -l | tr -d ' ')
echo "Installed (version $(cat "$DEST/.a/VERSION")):"
echo "  $DEST/.a/skills                  $n_skills files   (the method)"
echo "  $DEST/.claude/commands/A.*.md    $n_claude files   (Claude Code: /A.plan, /A.bugfix, ...)"
echo "  $COPILOT_DIR/A.*.prompt.md       $n_copilot files   (Copilot in VS Code)"
echo
if [ "$GLOBAL" = 1 ]; then
  echo "This was a GLOBAL install: the /A.* commands are available in every folder on this machine."
  echo "Copilot in VS Code needs one setting once: add \"$COPILOT_DIR\" to chat.promptFilesLocations, then Reload Window."
  echo
  echo "Nothing is remembered until a folder is made a project. In the folder you want to work in, open a new chat and run:"
  echo "    /A.start-project"
  echo "Everything you do there becomes that project's memory (board, logs, decisions), separate from every other project."
  echo "Start as many projects as you like in different folders. /A.projects shows them all and how they depend on each other."
else
  echo "This was a PROJECT-LEVEL install into $DEST: the commands work only when this folder is the workspace root."
  echo "Open this folder, start a new chat, and run /A.start-project (required; nothing is remembered without it)."
fi
