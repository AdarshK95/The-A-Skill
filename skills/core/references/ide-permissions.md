# IDE permissions — stopping the "Allow reading external files?" prompt

With a global install the method lives under the user's home folder, outside the workspace, so VS Code Copilot asks for permission to read it. The agent resolves this; the user is asked only to approve. Follow the steps in order; stop at the first that works.

## 1. Look in the IDE first — no question to the user yet

Before asking the user anything, find out whether the IDE can be told to trust the method folder permanently:

- Search the IDE's settings (settings UI and the user `settings.json`) for a way to trust a folder or auto-approve file reads. Names to search, in this order: `chat.tools`, `autoApprove`, `external files`, `trusted`, `promptFiles`, `workspace trust`. Read each candidate's description.
- Check the IDE's own documentation or release notes if the settings are unclear (the host's help command or docs search).

Found one that allows a folder or path pattern → show the user the exact setting and value, explain in one line what it does, and ask approval to set it. On yes: set it, Reload Window, read a method file to confirm the prompt is gone, report. Stop here.

Found nothing → go to step 2.

## 2. Test the prompt once, with the user

Say: "I couldn't find a setting that allows this permanently. I'll trigger the prompt once so we can see what your IDE offers." Read one method file (for example `core/SKILL.md`). Ask the user what the prompt shows — the button labels and the options in the arrow menu next to the first button — or ask for a screenshot. Record the labels.

- An option that persists beyond the session is offered ("Always Allow", "Allow in this Workspace") → tell the user that choosing it once ends the prompts. Stop here.
- Only session-scoped options ("Allow Once", "Allow in this Session") → go to step 3.

## 3. Last resort: a local mirror in the workspace

Only when steps 1 and 2 found nothing permanent. Propose this and wait for approval:

> Your IDE can only allow this for one session at a time. The way around it is a copy of the method inside this workspace — a mirror of `~/.a/skills` and `~/.a/templates` at `<workspace root>/.a/mirror/`. Commands then read from the mirror, which is inside the workspace, and the prompt stops. The global install stays as it is; `/A.skill.update` refreshes mirrors too. Shall I create it?

On yes:

1. Copy `~/.a/skills` → `<root>/.a/mirror/skills` and `~/.a/templates` → `<root>/.a/mirror/templates`. Write `<root>/.a/mirror/MIRROR` with: `mirror_of: <global .a path>`, `commit: <from ~/.a/SOURCE>`, `created: <date time>`.
2. Add the mirror path to `~/.a/projects.md` under `## Mirrors`. `/A.skill.update` and `/A.skill.repair` refresh every mirror after every update — those in the list and any they discover under registered projects or the current workspace — so a mirror never silently falls behind.
3. Add `.a/mirror/` to the workspace's `.gitignore` (marked block) unless the user wants it committed, and say so.
4. Test with the same read; confirm the prompt is gone.

Command wrappers already prefer a mirror: each wrapper first looks for `<workspace root>/.a/mirror/skills/<name>/SKILL.md` and reads that if present, else the global path. A mirror older than the global install is reported by `/A.skill.update` and `/A.project.status`.

## What never happens here

Asking the user before the agent has searched the IDE itself (step 1 is the agent's work). Telling the user to click something the agent has not seen the IDE offer. Changing an IDE setting without showing it and getting a yes. Touching the global install. Copying anything other than `skills` and `templates` into the mirror. Running the steps in any other order.
