"""The A Skill: which projects need /A.project.repair. Read-only: never changes a file.

Usage:  python project_check.py <method folder>                 every project in <method>/projects.md
        python project_check.py <method folder> <project> ...    only these folders
<method folder> holds templates/ (and projects.md): ~/.a on a global install.

Prints one line per project that needs repair, nothing for a healthy one. Checks, against the installed templates:
- the folder still holds .a/project.md;
- every top-level config key in templates/project.md is in the project's .a/project.md;
- an always-on block exists in one of the project's always_on_files, sits at the top of that file, and matches
  the current templates/always-on.md (the method path may differ);
- no old copies of the A Skill's helper scripts in <project>/.a/scripts/ (they now run from the install).
install.ps1 carries the same checks in PowerShell (Windows may have no Python); keep the two in step.
"""
import re
import sys
from pathlib import Path

DEFAULT_FILES = ["CLAUDE.md", "AGENTS.md", ".github/copilot-instructions.md"]


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def block_pattern(method: Path) -> "re.Pattern":
    tpl = squash((method / "templates" / "always-on.md").read_text(encoding="utf-8"))
    return re.compile(re.escape(tpl).replace(re.escape("{{skills_root}}"), ".+?"))


def check(path: Path, method: Path) -> list:
    cfg_file = path / ".a" / "project.md"
    if not cfg_file.is_file():
        return ["no .a/project.md there any more (moved or deleted?); see /A.project.list"]
    cfg = cfg_file.read_text(encoding="utf-8", errors="replace")
    found = []
    keys = dict.fromkeys(re.findall(r"(?m)^([a-z_]+):", (method / "templates" / "project.md").read_text(encoding="utf-8")))
    missing = [k for k in keys if not re.search(rf"(?m)^{k}\s*:", cfg)]
    if missing:
        found.append("config lacks " + ", ".join(missing))
    m = re.search(r"(?m)^always_on_files\s*:\s*(.+)$", cfg)
    names = [n.strip() for n in m.group(1).split(",")] if m else DEFAULT_FILES
    pattern = block_pattern(method)
    with_block = [path / n for n in names if (path / n).is_file() and "A-skill: begin" in (path / n).read_text(encoding="utf-8", errors="replace")]
    if not with_block:
        found.append("no always-on block in " + ", ".join(names))
    for f in with_block:
        text = f.read_text(encoding="utf-8", errors="replace")
        body = re.sub(r"(?s)\A---\r?\n.*?\r?\n---\r?\n", "", text).lstrip()
        if not body.startswith("<!-- A-skill: begin"):
            found.append(f"always-on block not at the top of {f.name}")
        span = re.search(r"(?s)<!-- A-skill: begin.*?A-skill: end -->", text)
        if span and not pattern.fullmatch(squash(span.group(0))):
            found.append(f"always-on block in {f.name} is from an older version")
    old = [n for n in ("page_build.py", "map_build.py") if (path / ".a" / "scripts" / n).is_file()]
    if old:
        found.append("old copies of the A Skill's helper scripts in .a/scripts/ (" + ", ".join(old) + "; they now run from the install)")
    return found


def projects(method: Path) -> list:
    index = method / "projects.md"
    rows = []
    if index.is_file():
        for line in index.read_text(encoding="utf-8", errors="replace").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if line.startswith("|") and len(cells) > 1 and re.match(r"^([A-Za-z]:[\\/]|/|~)", cells[1]):
                rows.append((cells[0], Path(cells[1]).expanduser()))
    return rows


def main() -> int:
    method = Path(sys.argv[1]).expanduser()
    targets = [(Path(p).name, Path(p)) for p in sys.argv[2:]] or projects(method)
    for name, path in targets:
        found = check(path, method)
        if found:
            print(f"  {name} ({path}): " + "; ".join(found))
    return 0


if __name__ == "__main__":
    sys.exit(main())
