# Projects — scope, setup, and where the skill is installed

## One workspace root = one project context

The A Skill is installed into a folder and is available only when that folder is the agent's workspace root. Everything it knows — `.a/project.md`, the board, activity files, decisions, lessons, the shared folder — lives in that folder. Opening a parent folder, a different repository, or a multi-root workspace does not carry it along.

Nested `.a/` folders are not supported. The agent uses the `.a/` at the workspace root; a `.a/` deeper in the tree is ignored, and `/A.start-project` warns if it finds one.

## One project or several?

| Situation | Set up as | Why |
| --- | --- | --- |
| One repository, several parts worked on in parallel (UI, backend, API, data) | **One** `.a/` at the repository root, one **area** per part | The board, overview and shared folder keep topics separate by area while sessions coordinate; one install, one history |
| Several repositories that belong to one product | One `.a/` **per repository** | Each is its own workspace root; contexts stay separate, each has its own board |
| A monorepo where teams open sub-folders as separate workspaces | One `.a/` per sub-folder that is opened as a root | Install where the workspace root is, not where the code is |
| A main project plus throwaway experiments | `.a/` in the main project; experiments without it unless they will outlive the week | Install where history is worth keeping |

If a user describes a main project with parallel pieces under it, the question to ask is: **do you open them as one folder or as separate folders?** One folder → one install with areas. Separate folders → one install each.

## Install once, start projects many times

The skill is installed **once per machine** (`~/.a/skills`, with the commands where each host reads user-level commands). It is then available in every folder. A folder becomes a **project** when the user runs `/A.start-project` in it: that creates `.a/project.md`, the documentation set, the board and the shared folder *inside that folder*, and registers the project in `~/.a/projects.md`. Work done in a folder that has not been started is not remembered anywhere; the commands still answer, but they say so and offer `/A.start-project`.

A project-level install (`install.ps1 -Dest <folder>` / `install.sh <folder>`) is still possible for a repository that must carry the method with it (teammates, pinning). Not both in one folder: duplicate `/A.*` entries, and the wrong version may run. `/A.start-project` checks and says which copy is active.

## Projects that work together

Three projects can be one product: an MCP server, a frontend, a multi-agent backend. Each is its own project with its own context. They are connected only by what they **document**:

- In `.a/project.md`, `depends_on:` lists the projects this one uses and, in one line each, what it uses from them; `provides:` lists what this one offers. Both empty means independent — and that is the statement, not an omission. Nothing is inferred from folder names or imports.
- `/A.start-project` mirrors these into `~/.a/projects.md`, the machine-wide index: one row per project (name, path, areas, depends on, provides, started, last active) and a diagram of the dependencies. `/A.projects` shows it and rebuilds it from the projects' own config files.
- At Start, a session reads the index and, if this project depends on others, the `provides` lines of those projects. When a feature touches a provided thing, the report says so under *Impact* and `## Links` names the other project; the user decides whether that project needs a feature of its own.
- Two projects talk through handoffs: a session in project A that needs something from project B writes a `waiting on` row in **B's** shared folder (path from the index), naming A's feature file; B's next session reports it at Start like any other handoff. Nothing is logged about the conversation itself — only the dependency and the handoff.

No dependency documented → the agent assumes none and does not go looking.

## After install — what to tell the user

At the end of the installer's output, and whenever a command runs in a folder with no `.a/project.md`:

1. The skill is installed globally; the commands work in every folder on this machine.
2. But nothing is remembered until a folder is made a project: **run `/A.start-project` in the folder you want to work in.** Everything done there is then that project's memory — board, logs, decisions — and stays separate from every other project.
3. Start as many projects as you like, in different folders, so their contexts never mix. If projects work together, declare it in each one's `.a/project.md` (`depends_on`, `provides`); `/A.projects` shows how they connect.

At the end of `/A.start-project`: confirm the project is registered, show the index row, and ask whether this project depends on, or provides something to, any other project in the index.
