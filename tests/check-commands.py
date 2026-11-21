"""Every /A.* command file has a one-line description that a picker can show whole.

Checks both hosts (commands/claude/*.md, commands/copilot/*.prompt.md):
- the front matter parses as YAML (an unquoted "word: word" breaks it, and the host then shows the
  file's first body line instead of the description - 11 commands did this before 0.14.0);
- description is a string of 1-60 characters (Copilot's picker cut longer ones at about 65);
- the same command has the same description in both hosts.
Needs PyYAML (pip install pyyaml).   python tests/check-commands.py   Exit 0 = all good.
"""
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
bad, seen = [], {}
for host, ext in (("claude", ".md"), ("copilot", ".prompt.md")):
    files = sorted((REPO / "commands" / host).glob("A.*" + ext))
    if not files:
        bad.append(f"no command files in commands/{host}")
    for f in files:
        name = f.name[: -len(ext)]
        try:
            fm = yaml.safe_load(f.read_text(encoding="utf-8").split("---")[1])
        except Exception as e:
            bad.append(f"{host}/{f.name}: front matter is not valid YAML ({str(e).splitlines()[0]})")
            continue
        d = fm.get("description") if isinstance(fm, dict) else None
        if not isinstance(d, str) or not 1 <= len(d) <= 60:
            bad.append(f"{host}/{f.name}: description missing or not 1-60 characters ({len(d) if isinstance(d, str) else d!r})")
            continue
        if name in seen and seen[name] != d:
            bad.append(f"{name}: description differs between hosts")
        seen[name] = d
for b in bad:
    print("FAIL " + b)
print(f"{len(seen)} commands checked; " + ("all descriptions parse and fit" if not bad else f"{len(bad)} problem(s)"))
sys.exit(1 if bad else 0)
