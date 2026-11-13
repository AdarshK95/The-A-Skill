---
name: skill-update
description: Check whether a newer release of The A Skill exists and, only after the user confirms, install it. Not a project command — it updates the skill itself.
disable-model-invocation: true
---

# /A.skill-update — update The A Skill itself

This command is about the skill, not the user's code. Nothing in the project's files, config or documents is touched. **No action is taken without the user's explicit yes.**

## Step 1 — check, then ask. Nothing else first.

1. Read `.a/VERSION` (installed) and `.a/SOURCE` (repository URL; missing → `https://github.com/AdarshK95/The-A-Skill`).
2. Fetch the repository's `VERSION` (and `CHANGELOG.md`) without cloning anything yet.
3. Say exactly one of these, then **stop and wait**:

   - Versions differ:
     > `/A.skill-update` checks for a newer release of The A Skill — the workflow tooling, not your project code. You have **<installed>**; the latest is **<latest>**. What changed: <one line per changelog entry in between, plain words>. Do you want to update now? (yes / no)

   - Versions equal:
     > `/A.skill-update` checks for a newer release of The A Skill — the workflow tooling, not your project code. You have **<installed>**, which is the latest. Nothing to do.

   - Repository unreachable:
     > I couldn't reach <url> to check (reason). Nothing was changed. Try again later or check the address in `.a/SOURCE`.

## Step 2 — only after "yes"

1. Fetch the release to a temporary folder (`git clone --depth 1`, or the archive when git is unavailable).
2. Show the user the fetched `install.ps1` / `install.sh` if it differs from the one in `.a/templates` (or in one line say it is unchanged), then run it against this project (`install.ps1 -Dest .` on Windows, `install.sh .` elsewhere). It writes only `.a/skills`, `.a/templates`, `.a/registry.md`, `.a/VERSION`, `.a/SOURCE`, `.claude/commands/A.*`, `.github/prompts/A.*`. No installer possible → copy exactly those paths by hand.
3. If `.a/project.md` exists and its `schema_version` is older than the one `../core/references/config-schema.md` expects: list the keys added or renamed with their defaults and **ask again** before writing any of them.
4. Remove the temporary folder.
5. Report: `<old> → <new>`, the installer's file counts, any config keys the user should set, and that a **new chat** is needed before the updated commands load.

"No" or anything other than a clear yes → "Not updated. You're still on <installed>." and stop.
