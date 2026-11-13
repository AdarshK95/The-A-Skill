---
name: start-project
description: Make this folder a project of The A Skill: config, documentation files, board, shared folder, the always-on block, and a row in the machine-wide projects index.
disable-model-invocation: true
---

# /A.start-project — make this folder a project

**Place in the flow:** needs an installed skill and a folder; produces a project; next: describe what to build, or `/A.plan`. See `../core/references/flow.md`.

Aliases: `/A.init`, `/A.setup`, `/A.initialize`. Safe to run again: existing files are kept and reported, never overwritten; the index row is refreshed.

The method is installed once per machine; this command gives *one folder* its own memory. A workspace can hold many such folders. Everything the user does here afterwards — board, activity files, decisions, lessons — lives here and nowhere else (`../core/references/projects.md`).

**Setup is one confirmation, not an interview.** Infer what can be inferred, default the rest, show one summary, ask one question, then do everything. This command never installs or copies the method, never writes outside the chosen project folder, and never logs its own run in any other project.

## Step 1 — look (no questions yet)

1. **Folder.** Candidates: the folder the user named, else the folder containing the files they are working in, else the workspace root. Search for existing projects: `.a/project.md` at the root and up to three levels below (skipping dependency, build and VCS folders), and rows in `~/.a/projects.md` under the workspace. A `.a/project.md` in a parent of the candidate → nesting; the parent is the project; say so and stop.
2. **Infer the config** from what is there:
   - `project_name`: the folder name.
   - `areas`: top-level folders that hold code, named after their role (frontend, ui, web, backend, api, server, services, mcp, connectors, data, infra, tests…). None recognisable → `General`.
   - documentation: an existing docs folder (`docs`, `documentation`, `z_Documentation`, anything holding a decisions/implementation/API file) and its files, pointed at rather than duplicated; otherwise `docs/` with the defaults.
   - `date_format` / `time_format`: the format already used in the existing docs if any; else the values in `~/.a/settings.md`.
   - `tracker_label`: `ADO` when `AB#` patterns appear in docs or commits, `Jira` for `[A-Z]+-\d+` keys, `Issue` when a `.github` folder exists, else `Work item`.
   - `depends_on` / `provides`: empty unless the index lists other projects **and** this folder's code references one of them (imports, URLs, package names); then propose the dependency.
   - `gitignore`: on; paths already tracked by git are excluded from the block.

## Step 2 — one summary, one question

Show, in plain words, one block:

> I'll make **<folder>** a project named *<name>*. Areas: <list>. Documentation: <existing folder found and reused | new `docs/` folder>. Dates `<format>`, times `<format>`. Work items: <label>. Depends on: <none | proposed list>. I'll add the always-on block to <files>, ignore `.a/` <and the new docs paths> in git, and register the project in the machine index. **Proceed, or tell me what to change?**

If several folders could be the project (step 1 found siblings, or none at the root), the same block lists the choice: "Create it at <root>, or in <sub-folder A> / <sub-folder B>?" — still one question.

## Step 3 — on yes, do all of it, silently

1. Write `.a/project.md` from `../../templates/project.md` with the inferred values.
2. Create what the config names and does not exist, from `../../templates/`: constitution, decisions log, deferred-decisions log, implementation log, API docs, lessons log, activity folder with `_template.md`, board with one `### Area:` heading per area and one `subgraph` per area. Existing files are kept untouched. Numbered central docs (`01.…`) get the next numbers.
3. Create `shared_folder` from `../../templates/shared/`.
4. Append `../../templates/always-on.md` to each `always_on_files` entry (create if missing), `{{skills_root}}` filled with the real method path; skip files that already carry the marker.
5. `.gitignore`: the marked block, unless `gitignore: off`.
6. Add or refresh the row in `~/.a/projects.md`; redraw its dependency diagram.
7. Write `E1` in a new activity file **only if the user asked for the setup to be logged**; otherwise the project's history starts with its first feature. Nothing is written in any other project's logs, ever.

## Step 4 — report, in the standard shape

> **<name> is a project now.** Done: <files created, one line each, grouped>. Not done: <only something the user asked for that could not be done, else "everything you asked for is in place">. Your next step: start a new chat and describe what you want to build, or `/A.plan <idea>`.

One optional line after the block, and only one: "When you want the overview drawn from your code: `/A.map`." Nothing about placeholders, other projects' logs, or things nobody asked for. If a command wrapper is found to be broken (an unfilled `{{SKILLS_ROOT}}`), the install is defective: say "the install looks incomplete; run `/A.skill-repair`" in one line and nothing more.

## Re-running

Safe. Existing files are kept and reported; the index row is refreshed; the summary says "refresh" instead of "make".
