# Projects — scope, setup, and where the skill is installed

## Which project is this message about?

A project is any folder that holds `.a/project.md`. A workspace may hold one project, several (a parent folder such as `D:\Code` with projects under it, or a multi-root workspace), or none. The commands are installed globally, so they work in all of these; what the agent must do is **resolve the project** before Start, in this order:

1. **The user named it** — `/A.plan in api-backend …`, or the project is named in the message → that project, by its row in `~/.a/projects.md` or by folder name.
2. **The files point to it** — the message mentions or the editor has open a file; walk up from that file's folder until a `.a/project.md` is found → that project.
3. **The conversation is already in one** — a project was resolved earlier in this conversation → stay in it (auto's Stay rule).
4. **Exactly one project in the workspace** — one folder in the workspace holds `.a/project.md` (or exactly one registered path in `~/.a/projects.md` lies under the workspace) → that one.
5. **Several** → ask, one question, listing them by name: "Which project is this for: api-backend, frontend, mcp-server?" Never guess between projects.
6. **None** → say that no folder here is a project yet and offer `/A.start-project <folder>`.

Say the resolved project in one phrase at the start of the reply ("In *api-backend*:"). All paths in config are relative to **that project's folder**, not the workspace root. Nested projects (a `.a/project.md` inside another project's folder) are not supported; the nearest one up from the file wins and `/A.start-project` warns.

## Workspaces that hold several projects

Keep working from the parent folder or the multi-root workspace; there is no need to open each project separately. `/A.start-project` first looks for existing projects at the root and up to three levels below, reports them, and asks where the new project should be created before writing anything; `/A.start-project <folder>` names the folder directly but is checked the same way. When run at a folder that is not itself a project but contains projects, it writes a short **workspace block** into that folder's instruction files (`templates/always-on-workspace.md`): the list of projects under it with their paths, and the resolution rule above, so every agent opening the workspace knows which projects exist and how to pick one. `/A.projects` lists the projects in the current workspace first.

## One project or several?

| Situation | Set up as | Why |
| --- | --- | --- |
| One repository, several parts worked on in parallel (UI, backend, API, data) | **One** `.a/` at the repository root, one **area** per part | The board, overview and shared folder keep topics separate by area while sessions coordinate; one install, one history |
| Several repositories that belong to one product | One `.a/` **per repository** | Each is its own workspace root; contexts stay separate, each has its own board |
| A parent folder or multi-root workspace holding several repositories | One `.a/` per repository; a workspace block in the parent's instruction file | Work from the parent; the agent resolves the project from the files or asks |
| A main project plus throwaway experiments | `.a/` in the main project; experiments without it unless they will outlive the week | Install where history is worth keeping |

If a user describes a main project with parallel pieces under it, the question is whether the pieces share one history or need their own: one repository worked on as one thing → one project with areas; separate repositories or separately shipped parts → one project each, all under the same workspace if the user likes.

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

After an install, lead with **"Installation complete"** and the version and counts — never with what is missing. Then, if VS Code Copilot is in use, say the two remaining steps (add the commands folder to `chat.promptFilesLocations`, reload the window) and **ask for approval to do them**; on yes, do them and confirm `/A.help` appears. Then one idea, in one line: the skill remembers work per project — run `/A.start-project` once in any folder you want to work in; everything done there is that project's memory, separate from every other project; `/A.projects` shows them all. The exact wording is in the repository's `SETUP.md › A — ask your agent`.

Whenever a command runs in a folder with no `.a/project.md`: say the skill is installed but this folder is not a project yet, so nothing done here is remembered, and offer `/A.start-project`.

At the end of `/A.start-project`: confirm the project is registered, show the index row, and ask whether this project depends on, or provides something to, any other project in the index.
