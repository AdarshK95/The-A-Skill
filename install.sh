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

echo "Installed:"
echo "  .a/skills, .a/templates, .a/registry.md         (the method)"
echo "  .claude/commands/A.*.md                          (Claude Code: /A.plan, /A.bugfix, ...)"
echo "  .github/prompts/A.*.prompt.md                    (Copilot in VS Code: /A.plan, /A.bugfix, ...)"
echo
if [ ! -f "$DEST/.a/project.md" ]; then
  echo "Next: open the project in your agent, start a new chat, and run /A.init"
else
  echo "Config .a/project.md already present; method updated. Run /A.help to check."
fi
