---
name: init
description: Set a project up for the /A.* workflow: config, documentation files, board, and the always-on block in the agent instruction files.
disable-model-invocation: true
---

# /A.init — set up this project

Aliases: `/A.setup`, `/A.initialize`. Safe to run again: existing files are kept and reported, never overwritten.

1. **Look first.** List what the project already has: a docs folder, a decisions or ADR file, a changelog or implementation log, an architecture doc, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`. Propose config values that point at what exists rather than creating duplicates.
2. **Ask, one at a time, only what you could not infer:** the project's areas (sections: for example UI, Backend, API, Data); where documentation should live if nothing exists; date and time format if the project already uses one. Everything else takes the defaults in `../core/references/config-schema.md`.
3. **Write `.a/project.md`** from `../../templates/project.md` with the agreed values. Show it.
4. **Create what the config names and does not yet exist**, from `../../templates/`: constitution, decisions log, implementation log, API docs, lessons log, the activity folder with `_template.md`, and the board with one `### Area:` heading per area under Planned and In progress and one `subgraph` per area in the overview. When the project numbers its central docs (`01.…`, `02.…`), offer to give the new ones the next numbers and point the config at them. Month folders and ledgers are created on demand by the first feature, not now.
5. **Shared folder.** Create `shared_folder` from `../../templates/shared/` (README, claims, handoffs, notes).
6. **Always-on block.** Append `../../templates/always-on.md` to each file in `always_on_files`, creating the file if missing. Skip a file that already contains the `A-skill: begin` marker.
7. **Verify.** List every file created or changed. Point out that the commands become available when the host reloads (new chat or reload window).
8. **Existing code?** If the repository already has source files, offer `/A.map` now so the overview starts from the real architecture instead of empty.
9. **Hand over** in three lines: try `/A.help`; start with `/A.plan <idea>` or just describe what you want; `/A.status` any morning. Mention that the first review in this project will run a one-time isolation probe (`../core/references/hosts.md`).

Project-specific rules the user states during setup go into `rules:` in the config, or into the constitution when they are standing principles — ask which.
