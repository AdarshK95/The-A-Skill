#!/usr/bin/env sh
# Remove ONLY what install.sh created. Never touches any project's .a/project.md, .a/shared, documentation,
# board, activity files, or the always-on block in instruction files. ~/.a/projects.md (the user's index) is kept.
#   sh uninstall.sh --list                 show what would be removed, remove nothing
#   sh uninstall.sh --yes                  global uninstall
#   sh uninstall.sh --project DIR --yes    project-level uninstall inside DIR
set -e
MODE=list; GLOBAL=1; DEST="$HOME"
while [ $# -gt 0 ]; do case "$1" in
  --yes) MODE=yes;; --list) MODE=list;; --project) GLOBAL=0; DEST="$(cd "$2" && pwd)"; shift;; *) echo "unknown option $1"; exit 2;; esac; shift; done
if [ "$GLOBAL" = 1 ]; then
  TARGETS="$DEST/.a/skills $DEST/.a/templates $DEST/.a/commands $DEST/.a/registry.md $DEST/.a/VERSION $DEST/.a/SOURCE $DEST/.a/auto-pointer.md $DEST/.copilot/instructions/a-skill.instructions.md"
  GLOBS="$DEST/.claude/commands/A.*.md"
else
  TARGETS="$DEST/.a/skills $DEST/.a/templates $DEST/.a/registry.md $DEST/.a/VERSION $DEST/.a/SOURCE"
  GLOBS="$DEST/.claude/commands/A.*.md $DEST/.github/prompts/A.*.prompt.md"
fi
echo "The A Skill uninstall ($([ "$GLOBAL" = 1 ] && echo global || echo "project: $DEST")) — would remove:"
for t in $TARGETS; do [ -e "$t" ] && echo "  $t"; done
for g in $GLOBS; do [ -e "$g" ] && echo "  $g"; done
SETTINGS="$DEST/.claude/settings.json"; HAS_HOOK=0
[ "$GLOBAL" = 1 ] && [ -f "$SETTINGS" ] && grep -q "auto-pointer\.md" "$SETTINGS" && HAS_HOOK=1
[ "$HAS_HOOK" = 1 ] && echo "  the A Skill hook in $SETTINGS (only that entry; backup first)"
echo "Kept (yours): every project's .a/project.md, .a/shared/, documentation, board, activity files, instruction-file blocks; ~/.a/projects.md"
[ "$MODE" = yes ] || { echo "Nothing removed (dry run). Re-run with --yes to remove the paths above."; exit 0; }
if [ "$HAS_HOOK" = 1 ]; then   # before the templates folder (which holds settings_hook.py) is removed
  PY=""; for c in python3 python; do "$c" -c "" 2>/dev/null && PY="$c" && break; done   # skips stubs that exist but do not run
  if [ -n "$PY" ]; then "$PY" "$DEST/.a/templates/settings_hook.py" "$SETTINGS" ""
  else echo "NOTE: Python not found; remove the UserPromptSubmit entry mentioning auto-pointer.md from $SETTINGS by hand."; fi
fi
for t in $TARGETS; do [ -e "$t" ] && rm -rf "$t"; done
for g in $GLOBS; do [ -e "$g" ] && rm -f "$g"; done
echo "Removed. Start a new chat for the commands to disappear."
