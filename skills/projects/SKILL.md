---
name: projects
description: Show the projects on this machine that use The A Skill and how they depend on each other; rebuild the index from each project's own config.
disable-model-invocation: true
---

# /A.projects — all projects on this machine

Reads `~/.a/projects.md`. Missing → no project has been started yet; say so and point to `/A.start-project`.

1. **Rebuild.** For every row, open that path's `.a/project.md` and refresh name, areas, `depends_on`, `provides`, and last active (the newest `Updated:` in its activity files). A path that no longer exists is marked `missing` and left in the table for the user to remove. Redraw the dependency diagram: one node per project, one edge per `depends_on` line.
2. **Show** the table and the diagram, with the projects that lie under the current workspace listed first and marked.
3. **Say in plain words**: how many projects, which depend on which, which are independent — "no documented dependency" is reported as independent, not as unknown. If the current folder is one of them, say which, and what it depends on.
4. **With input** ("A depends on B for the auth contract", "remove the missing one", "rename X") → edit the relevant project's `.a/project.md` (never only the index), then rebuild. A dependency is written in the dependent project's config; the index follows.

The index is never the source of truth; the projects' own config files are. Anything the user wants remembered about how projects relate goes into those files.
