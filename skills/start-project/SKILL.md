---
name: start-project
description: Make this folder a project of The A Skill: config, documentation files, board, shared folder, the always-on block, and a row in the machine-wide projects index.
disable-model-invocation: true
---

# /A.start-project — make this folder a project

Aliases: `/A.init`, `/A.setup`, `/A.initialize`. Safe to run again: existing files are kept and reported, never overwritten; the index row is refreshed.

The method is installed once per machine; this command gives *this folder* its own memory. Everything the user does here afterwards — board, activity files, decisions, lessons — lives here and nowhere else (`../core/references/projects.md`).

0. **Scope check.** The project is the current workspace root. A `.a/project.md` deeper in the tree or in a parent folder is reported, not merged. Find the method: the folder this skill file lives in is `skills_root` (global: `~/.a/skills`; project-level: `.a/skills`); if both exist, say which one is active and recommend removing the other. Read `~/.a/projects.md` if it exists: if this path is already registered, this is a refresh, say so.
1. **Look first.** List what the project already has: a docs folder, a decisions or ADR file, a changelog or implementation log, an architecture doc, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`. Propose config values that point at what exists rather than creating duplicates.
2. **Ask, one at a time, only what you could not infer:** the project's areas (sections: for example UI, Backend, API, Data); where documentation should live if nothing exists; date and time format if the project already uses one. Everything else takes the defaults in `../core/references/config-schema.md`.
3. **Write `.a/project.md`** from `../../templates/project.md` with the agreed values. Show it.
4. **Create what the config names and does not yet exist**, from `../../templates/`: constitution, decisions log, implementation log, API docs, lessons log, the activity folder with `_template.md`, and the board with one `### Area:` heading per area under Planned and In progress and one `subgraph` per area in the overview. When the project numbers its central docs (`01.…`, `02.…`), offer to give the new ones the next numbers and point the config at them. Month folders and ledgers are created on demand by the first feature, not now.
5. **Shared folder.** Create `shared_folder` from `../../templates/shared/` (README, claims, handoffs, notes).
6. **Always-on block.** Append `../../templates/always-on.md` to each file in `always_on_files`, creating the file if missing, with `{{skills_root}}` replaced by the real path found in step 0. Skip a file that already contains the `A-skill: begin` marker.
6a. **Git ignore.** If the project is a git repository and `gitignore: on` (default), add to its `.gitignore` (create it if missing) a marked block ignoring `.a/` and every documentation path the config names that did not already exist and is not already tracked by git (`docs_root`, the activity folder, the board, the map folder, the lessons log): working notes and agent metadata are usually not committed. Paths that git already tracks are left alone and reported. Tell the user at the end exactly which lines were added, that it is safe to remove them if they want the documentation committed, and that nothing already committed was changed.
6b. **Register.** Add or refresh this project's row in `~/.a/projects.md` (create it from `../../templates/projects.md` if missing): name, path, areas, depends on, provides, started, last active. Redraw the dependency diagram from all rows.
7. **Verify.** List every file created or changed. Point out that the commands become available when the host reloads (new chat or reload window).
8. **Existing code?** If the repository already has source files, offer `/A.map` now so the overview starts from the real architecture instead of empty.
9. **Hand over** in three lines: try `/A.help`; start with `/A.plan <idea>` or just describe what you want; `/A.status` any morning. Mention that the first review in this project will run a one-time isolation probe (`../core/references/hosts.md`).
10. **Other projects** (`../core/references/projects.md`): show the project's row in `~/.a/projects.md` and the other projects listed there. Ask: does this project depend on any of them, or provide something they use? If yes, write `depends_on` / `provides` into `.a/project.md` in the user's words and refresh the index. Then say: work in this folder is now this project's memory; any other folder needs its own `/A.start-project`; `/A.projects` shows them all. Repeat the `.gitignore` lines added and how to undo them.

Project-specific rules the user states during setup go into `rules:` in the config, or into the constitution when they are standing principles — ask which.
