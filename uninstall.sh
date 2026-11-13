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
  TARGETS="$DEST/.a/skills $DEST/.a/templates $DEST/.a/commands $DEST/.a/registry.md $DEST/.a/VERSION $DEST/.a/SOURCE"
  GLOBS="$DEST/.claude/commands/A.*.md"
else
  TARGETS="$DEST/.a/skills $DEST/.a/templates $DEST/.a/registry.md $DEST/.a/VERSION $DEST/.a/SOURCE"
  GLOBS="$DEST/.claude/commands/A.*.md $DEST/.github/prompts/A.*.prompt.md"
fi
echo "The A Skill uninstall ($([ "$GLOBAL" = 1 ] && echo global || echo "project: $DEST")) — would remove:"
for t in $TARGETS; do [ -e "$t" ] && echo "  $t"; done
for g in $GLOBS; do [ -e "$g" ] && echo "  $g"; done
echo "Kept (yours): every project's .a/project.md, .a/shared/, documentation, board, activity files, instruction-file blocks; ~/.a/projects.md"
[ "$MODE" = yes ] || { echo "Nothing removed (dry run). Re-run with --yes to remove the paths above."; exit 0; }
for t in $TARGETS; do [ -e "$t" ] && rm -rf "$t"; done
for g in $GLOBS; do [ -e "$g" ] && rm -f "$g"; done
echo "Removed. Start a new chat for the commands to disappear."
