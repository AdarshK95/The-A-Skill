---
name: show
description: Open the project's pages live — build them, start the page server, open the browser. One command, nothing to set up.
disable-model-invocation: true
---

# /A.show — open the project pages

**Place in the flow:** independent; needs a project; produces the pages open in the browser, following the agent. See `../core/references/flow.md`.

Also what "show me the dashboard", "open the pages", "where is the html", "start the page server" mean.

The page script is the A Skill's own, run from the install — `<method>/templates/pages/page_build.py`, where `<method>` is the folder holding `skills/` and `templates/` (`~/.a` on a global install) — with `--root <project>`. It is never copied into the project (`../core/references/logging.md › The pages`).

## Steps

1. **Project.** Resolve it as the spine's Start says. None → say so in one line and offer `/A.project.start`; stop.
2. **Python.** `python --version`, else `py -3 --version`, else `python3 --version`; use the first that runs. None → say: "The pages need Python 3 (free, from python.org or the Microsoft Store). Without it I can't build or serve them." If `<pages_folder>/index.html` already exists, open it as a file (`start` / `open` / `xdg-open`) and say it is not live. Stop.
3. **Start and open.** Run `<python> <method>/templates/pages/page_build.py --root <project> --serve --open`. It builds the pages, starts the server hidden (or says `already running`), and opens the page in the default browser. The address is fixed per project and printed by the command.
4. **Server would not start** (the command says so — usually the port is taken): run the same command without `--serve` (`--root <project> --open`), which builds the pages and opens them as a file, and say that the page is not live and why, quoting the command's own message.
5. **Report**, in this shape:

> **Pages open:** <address> — live: it follows the agent by itself, and **Resync** rebuilds on demand. **Stop the server:** `<python> <method>/templates/pages/page_build.py --root <project> --stop`. **Starts by itself:** <the `pages_server` value in force and where it is set — `.a/project.md` or `~/.a/settings.md`> (`off`, `session` or `login`; the page's **Help** section explains each).

Every path in the report is the real one for this machine, checked by running the command — never a placeholder.

## What this command never does

Copy the script into the project. Install a login startup entry (only `pages_server: login`, applied by `/A.project.repair`, does that). Edit any project file.
