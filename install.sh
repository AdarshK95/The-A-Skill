#!/usr/bin/env sh
# Install the The A Skill into a project.
# Usage:  sh install.sh [path/to/project]        (default: current directory)
# Idempotent: re-running updates the method and commands, never your project's documents or config.
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-.}"
DEST="$(cd "$DEST" && pwd)"

echo "Installing The A Skill from $SRC into $DEST"

mkdir -p "$DEST/.a/skills" "$DEST/.a/templates" "$DEST/.claude/commands" "$DEST/.github/prompts"
cp -R "$SRC/skills/." "$DEST/.a/skills/"
cp -R "$SRC/templates/." "$DEST/.a/templates/"
cp "$SRC/registry.md" "$DEST/.a/registry.md"
cp "$SRC/VERSION" "$DEST/.a/VERSION"
cp "$SRC"/commands/claude/A.*.md "$DEST/.claude/commands/"
cp "$SRC"/commands/copilot/A.*.prompt.md "$DEST/.github/prompts/"

n_skills=$(find "$DEST/.a/skills" -type f -name '*.md' | wc -l | tr -d ' ')
n_claude=$(ls "$DEST/.claude/commands"/A.*.md 2>/dev/null | wc -l | tr -d ' ')
n_copilot=$(ls "$DEST/.github/prompts"/A.*.prompt.md 2>/dev/null | wc -l | tr -d ' ')
echo "Installed (version $(cat "$DEST/.a/VERSION")):"
echo "  .a/skills                     $n_skills files   (the method)"
echo "  .claude/commands/A.*.md       $n_claude files   (Claude Code: /A.plan, /A.bugfix, ...)"
echo "  .github/prompts/A.*.prompt.md $n_copilot files   (Copilot in VS Code: /A.plan, /A.bugfix, ...)"
echo
echo "Open THIS project folder as the workspace root (not a parent folder), start a new chat."
if [ ! -f "$DEST/.a/project.md" ]; then
  echo "REQUIRED before first use: run /A.init  (creates .a/project.md; nothing works without it)"
else
  echo "Config .a/project.md already present; method updated. Run /A.help to check."
fi
