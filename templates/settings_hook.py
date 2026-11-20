"""Add or remove The A Skill's UserPromptSubmit hook in a Claude Code settings.json (used by install.sh / uninstall.sh).

Usage:  python3 settings_hook.py <settings.json> '<command>'   add (replaces an older A Skill hook)
        python3 settings_hook.py <settings.json> ''            remove
Only hooks whose command mentions auto-pointer.md are touched; every other key is kept. A backup is written first.
Never prints the file's contents (it can hold tokens).
"""
import json, os, shutil, sys

path, cmd = sys.argv[1], sys.argv[2]
settings = {}
if not os.path.exists(path) and not cmd:
    sys.exit(0)  # nothing to remove
if os.path.exists(path):
    raw = open(path, encoding="utf-8-sig").read()
    try:
        settings = json.loads(raw) if raw.strip() else {}
    except ValueError:
        print(f"NOTE: {path} is not plain JSON; left untouched. Add the A Skill hook by hand (see SETUP.md).")
        sys.exit(0)
    shutil.copyfile(path, path + ".bak-a-skill")
hooks = settings.setdefault("hooks", {})
groups = hooks.setdefault("UserPromptSubmit", [])
for g in groups:
    g["hooks"] = [h for h in g.get("hooks", []) if "auto-pointer.md" not in h.get("command", "")]
groups[:] = [g for g in groups if g["hooks"]]
if cmd:
    groups.append({"hooks": [{"type": "command", "command": cmd}]})
if not groups:
    del hooks["UserPromptSubmit"]
if not hooks:
    del settings["hooks"]
os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")
print(f"added (UserPromptSubmit in {path}; backup {path}.bak-a-skill)" if cmd else f"removed the A Skill hook from {path}")
