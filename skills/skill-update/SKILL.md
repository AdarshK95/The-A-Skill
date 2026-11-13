---
name: skill-update
description: Check whether a newer release of The A Skill exists and, only after the user confirms, install it. Not a project command — it updates the skill itself.
disable-model-invocation: true
---

# /A.skill-update — update The A Skill itself

This command is about the skill, not the user's code. Nothing in the project's files, config or documents is touched. **No action is taken without the user's explicit yes.**

## Step 1 — check, then ask. Nothing else first.

Releases are not always numbered: the version can stay the same while the repository gains fixes. So the check is on the **commit**, with the version as a label.

1. Read `.a/SOURCE` (global: `~/.a/SOURCE`): `repository:`, `commit:` (the commit installed from; may be `unknown` on old installs) and `.a/VERSION`.
2. Ask the repository for its current `main` commit without cloning: `git ls-remote <repository> HEAD` (first field). Fetch its `VERSION` too.
3. Compare the two commits. Say exactly one of these, then **stop and wait**:

   - Commits differ (version may or may not differ):
     > `/A.skill-update` checks for a newer release of The A Skill — the workflow tooling, not your project code. You have **<installed version>** (commit <short>); the repository is at **<latest version>** (commit <short>), **<n> commits newer**. What changed: <one line per commit message in between — from `git log --oneline <installed>..<latest>` on a shallow fetch, or from the repository's commit page; the CHANGELOG where it has an entry>. Do you want to update now? (yes / no)

   - Commits equal:
     > `/A.skill-update` checks for a newer release of The A Skill — the workflow tooling, not your project code. You have **<version>** (commit <short>), which is exactly what the repository has. Nothing to do.

   - `commit:` is `unknown` (installed before commits were recorded):
     > I can't tell which commit your copy came from, so I can't say whether anything changed. Updating is safe and takes a few seconds: it refreshes the method and commands and touches none of your projects. Do you want to update now? (yes / no)

   - Repository unreachable:
     > I couldn't reach <repository> to check (reason). Nothing was changed. Try again later or check the address in `.a/SOURCE`.

## Step 2 — only after "yes"

1. Fetch the release to a temporary folder (`git clone --depth 1`, or the archive when git is unavailable).
2. Show the user the fetched `install.ps1` / `install.sh` if it differs from the one in `.a/templates` (or in one line say it is unchanged), then run it against this project (`powershell -ExecutionPolicy Bypass -File install.ps1` on Windows — or, when Group Policy refuses even that, from inside the fetched folder: `& ([scriptblock]::Create((Get-Content .\install.ps1 -Raw)))`, `sh install.sh` elsewhere). It writes only `.a/skills`, `.a/templates`, `.a/registry.md`, `.a/VERSION`, `.a/SOURCE`, `.claude/commands/A.*`, `.github/prompts/A.*`. No installer possible → copy exactly those paths by hand.
3. If `.a/project.md` exists and its `schema_version` is older than the one `../core/references/config-schema.md` expects: list the keys added or renamed with their defaults and **ask again** before writing any of them.
4. **Find and refresh every mirror.** Build the list from three sources: `## Mirrors` in `~/.a/projects.md`; every registered project's path and the current workspace root, checked for `.a/mirror/MIRROR`; and, for registered projects, their parent folder (a workspace block there means a mirror may sit beside it). Any mirror found that is not in `## Mirrors` is added to it. Then for each mirror: copy `skills` and `templates` again, update its `MIRROR` file's commit, and list it in the report with before → after commit. A mirror whose folder no longer exists is marked `missing` in the list and left for the user to remove; nothing is deleted.
5. Remove the temporary folder.
6. Report: `<old version> (<old commit>) → <new version> (<new commit>)`, the installer's file counts, any config keys the user should set, and that a **new chat** is needed before the updated commands load.

"No" or anything other than a clear yes → "Not updated. You're still on <installed>." and stop.
