---
name: skill-repair
description: Check the installed files of The A Skill against the release they came from, report what is missing or altered, and — only after the user confirms — restore them. Not a project command.
disable-model-invocation: true
---

# /A.skill.repair — check and restore The A Skill's own files

For when a command fails to load, a file was deleted or edited by mistake, or an install looks incomplete. Touches only the skill's own files; never the project's config, documents, board or shared folder. **No action without the user's explicit yes.**

## Step 1 — inspect and report. Nothing else first.

1. Read `.a/VERSION` and `.a/SOURCE` (missing SOURCE → `https://github.com/AdarshK95/The-A-Skill`). Missing VERSION → the skill is not installed; say so and offer the install sentence from the repository's SETUP.md instead.
2. Fetch the **same commit** recorded in `.a/SOURCE` (`commit:`) from the repository to a folder under the operating system's temp directory (`$env:TEMP` on Windows, `/tmp` elsewhere) — never inside the workspace or a user folder —; if it is `unknown`, fetch the latest and say that differences may include genuine updates.
3. Find every mirror the same way `/A.skill.update` does (`## Mirrors` in the index, plus `.a/mirror/MIRROR` under registered projects and the current workspace); register any that are missing from the index. Compare each mirror's `skills` and `templates` against the global install's, and the global install against the fetched release. For the global install compare, file by file, these locations against the fetched release: `.a/skills` ↔ `skills`, `.a/templates` ↔ `templates`, `.a/registry.md`, `.claude/commands/A.*.md` ↔ `commands/claude`, `.github/prompts/A.*.prompt.md` ↔ `commands/copilot`. Classify each as **present and identical**, **missing**, **altered** (content differs), or **extra** (an `A.*` file not in the release).
4. Say, then **stop and wait**:

   - Nothing wrong:
     > `/A.skill.repair` checks The A Skill's own files, not your project. All <n> files match version <v>; <m> mirror(s) match the install. Nothing to repair.

   - Problems found:
     > `/A.skill.repair` checks The A Skill's own files, not your project. Version <v>. Missing: <list>. Altered: <list>. Extra: <list>. I can restore the missing and altered files from the release (extra files are left alone unless you say otherwise). Your `.a/project.md`, documents and board are not touched. Proceed? (yes / no)

## Step 2 — only after "yes"

1. Copy the missing and altered files from the fetched release into place, then refresh every mirror from the repaired install. If more than half the files are missing, re-run the installer instead (same effect, one step) and say so.
2. Remove that temp folder before reporting; if the host refuses, ask for one approval to delete it and do it in the same turn — the user is never left to clean it up.
3. Report what was restored, file by file, and that a **new chat** is needed before commands reload.

An altered file the user says they changed on purpose is left as is and listed as "kept by user"; suggest they move the change into `.a/project.md › rules` or the constitution so the next update does not lose it.
