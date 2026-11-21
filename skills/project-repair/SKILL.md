---
name: project-repair
description: Bring this project up to the installed version of The A Skill — missing config keys, the always-on block, old helper-script copies, the page server setting. Reports first; changes nothing until the user says yes.
disable-model-invocation: true
---

# /A.project.repair — bring this project up to the installed version

**Place in the flow:** independent; needs a started project; produces a project that matches the installed version. The installer names the projects that need it; `/A.skill.update` relays that list. See `../core/references/flow.md`.

This command changes only **the A Skill's own files inside the project** — `.a/project.md`, the always-on block between its markers, the A Skill's helper-script copies under `.a/scripts/`, the docs the config names when they are missing. It never touches the user's own code, scripts or documents, and never deletes a document. Everything it reports was checked in this run (`../core/references/communication.md › Only verified facts reach the user`).

## Step 1 — inspect (read-only), then report and stop

1. **Project.** Resolve it as the spine's Start says. None → say so in one line and offer `/A.project.start`; stop.
2. **The deterministic checks.** Run `<python> <method>/templates/project_check.py <method> <project>` (`<method>` is the folder holding `skills/` and `templates/`, `~/.a` on a global install). It prints nothing for a healthy project, else one line listing what it found: config keys the installed template has and the project lacks; an always-on block missing, not at the top of its file, or from an older version; old copies of the A Skill's helper scripts in `.a/scripts/`. No Python → make the same checks by reading the files (the script's docstring lists them).
3. **The checks only an agent can make**, each against the files:
   - `simplification_markers` missing → search the code for shortcut-marker comment prefixes already in use (at least `lean:` and `ponytail:`), with their counts.
   - Every document and folder the config names exists (`/A.project.start › Step 3`, items 2–3).
   - Old helper-script copies: for each one, whether the page server answers now (`<method>/templates/pages/page_build.py --root <project> --status`) and whether a Windows login entry exists (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\a-skill-pages-<name>.vbs`, where `<name>` is the project folder's name in lower case with every run of other characters turned into `-`) and which script it names.
   - `pages_server` in force (`.a/project.md`, else `~/.a/settings.md`) against reality: `login` with no login entry, or a login entry with anything else.
4. **Report and stop.** One block, each finding naming whose file it is, its full path and what will change; then one question:

> `/A.project.repair` checks the A Skill's own files in **<project>** (<path>) against the installed version <v>. It never touches your code. Found: <one line per finding, in plain words, with the full path>. I'll <one line per fix>. **Proceed? (yes / no)**

Nothing found → "**<project>** matches the installed version <v>. Nothing to repair." and stop.

## Step 2 — only after "yes"

In this order:

1. **Config keys:** add each missing key to `.a/project.md` with the template's default value and comment, next to its neighbours in the template; `simplification_markers` gets `lean:` first, then the prefixes found in step 1.3. No existing value changes.
2. **Missing documents and folders:** create them from the templates exactly as `/A.project.start › Step 3` items 2–3 do; existing files are kept.
3. **Always-on block:** refresh and move it to the top exactly as `/A.project.start › Step 3` item 4 does; nothing outside the markers changes.
4. **Old helper-script copies**, in this order so nothing breaks: if the server answers, stop it (`... --stop`) and start it again from the install (`... --serve`) when `pages_server` is `session` or `login`; if a login entry names a copy, replace it from the install (`... --install-startup`); then delete each copy, and the `.a/scripts/` folder if it is left empty.
5. **`pages_server: login`** without an entry → install it (`... --install-startup`); an entry with any other value → remove it (`... --remove-startup`). Not Windows → say login start is Windows only and that `session` applies.
6. **Check:** run `project_check.py` again; it must print nothing. Anything left → say what and why.

## Step 3 — report

> **<project> is up to date with version <v>.** Done: <one line per change, with the full path>. Not done: <anything that could not be done, with the reason, else "everything found is fixed">. Your next step: <usually `/A.show` to see the pages>.
