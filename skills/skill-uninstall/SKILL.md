---
name: skill-uninstall
description: Remove The A Skill's own installed files — and nothing the user made with it. Asks before acting.
disable-model-invocation: true
---

# /A.skill-uninstall — remove the skill, keep the work

**Guard, before anything else.** This command removes only what the installer put on the machine. Everything created *while using* the skill — every project's `.a/project.md`, `.a/shared/`, documentation, board, activity files, decisions, lessons, the always-on blocks in instruction files, and `~/.a/projects.md` — is the user's work. It is not yours to delete, and this command never does. Deleting any of it is a violation, even if the user seems to ask for it in passing; a user who wants their documentation gone deletes it themselves, knowingly.

The removal is done by the installer's own uninstall script, which can only remove a fixed list of paths. Do not substitute your own `rm` or `Remove-Item` commands.

## Step 1 — show, then ask. Nothing else first.

1. Read `.a/SOURCE` from the global install (`~/.a/SOURCE`) or the project (`.a/SOURCE`) to learn the scope.
2. Run the uninstall script in dry-run mode: `~/.a/templates/uninstall.ps1` (Windows) or `sh ~/.a/templates/uninstall.sh` — project-level: the same with `-Project <folder>` / `--project <folder>`. It prints exactly what would be removed and what is kept.
3. Say:
   > `/A.skill-uninstall` removes The A Skill's own files — the method and the `/A.*` commands — from <scope>. It will remove: <the list the script printed>. It keeps everything you made: your projects' config, documentation, boards, activity logs, decisions, and the projects index. Those stay exactly as they are; delete them yourself later if you ever want to. Do you want to uninstall? (yes / no)
4. **Stop and wait.**

## Step 2 — only after "yes"

1. Run the same script with `-Yes` / `--yes`.
2. Offer one optional extra, as a separate question: remove the `A-skill: begin … end` block from this project's instruction files (`CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`) so agents stop being pointed at files that no longer exist. Only the text between the markers; only after a second yes; only in the current project unless the user names others.
3. Report what was removed (the script's list), what was deliberately kept, and that a new chat is needed for the commands to disappear.

"No" → "Nothing removed." and stop.
