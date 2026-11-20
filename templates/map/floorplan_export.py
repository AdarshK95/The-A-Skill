#!/usr/bin/env python3
"""Turn the elements registry into Floorplan's input: nodes, edges, flows and the open features as "recent work".

Reads the same sources as map_build.py (it imports its parser, so the two views cannot disagree) and prints ONE JSON
document on stdout. It writes nothing into the project.

  python floorplan_export.py --project <project folder> --prefix <folder name on the Floorplan map> [--code-root <folder>]

--prefix   Floorplan paths start with the repo folder, so a relative Code anchor `agent/main.py` becomes `<prefix>/agent/main.py`.
--code-root  an absolute anchor (D:\\Code\\Other\\x.py) becomes relative to this folder (the folder the map's repos sit in).

Output: {"nodes": [...], "edges": [...], "flows": [...], "tasks": [...], "unresolved": [...]}  (Floorplan's architecture@1 fields).
Standard library only. No network.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import map_build as mb  # the registry parser lives there; one parser, two views

EDGE_KIND = [  # first word of "(type: name)" -> Floorplan edge kind
    (r"^(api|http|https|rest|webhook)", "http"), (r"^(sse|event|stream|pubsub|eventgrid)", "event"), (r"^(queue|servicebus|kafka)", "queue"),
    (r"^(mcp|rpc|grpc)", "rpc"), (r"^(cosmos|search|blob|db|sql|storage|index|redis|snowflake|keyvault|data)", "data"), (r"^(config|env|setting)", "config"),
]

def edge_kind(label: str) -> str:
    t = label.split(":")[0].strip().lower()
    return next((k for rx, k in EDGE_KIND if re.match(rx, t)), "call")

def anchors(code: list[str], prefix: str, code_root: str, unresolved: list) -> list[str]:
    """Code anchors are prose-ish: 'path (symbols)', 'path:182', 'D:\\abs\\dir\\ (a.tsx, b.tsx)', 'agent/main.py and the agent/ package'.
    Take every path-looking token, drop symbols and line numbers, make it relative to the map's repo root."""
    out = []
    root = code_root.replace("\\", "/").rstrip("/").lower()
    for entry in code:
        entry = re.sub(r"\([^)]*\)", " ", entry).replace("`", " ").replace("\\", "/")
        found = False
        for tok in re.findall(r"(?:[A-Za-z]:)?[\w.@\-/\[\]]*[/.][\w.@\-/\[\]]*", entry):
            tok = re.sub(r":\d+(-\d+)?$", "", tok).strip(".,;")
            if not tok or tok in (".", "..") or ("/" not in tok and not re.search(r"\.\w{1,5}$", tok)): continue
            if re.match(r"^[A-Za-z]:/", tok):
                if tok.lower().startswith(root + "/"): tok = tok[len(root) + 1:]
                else: continue  # outside the map's folders: nothing to point at
            else:
                tok = tok.lstrip("./")
                tok = f"{prefix}/{tok}" if prefix else tok
            out.append(tok.rstrip("/") + "/**" if (entry.strip().endswith("/") or tok.endswith("/") or "." not in tok.rsplit("/", 1)[-1]) else tok)
            found = True
        if not found and entry.strip(): unresolved.append(entry.strip()[:100])
    return list(dict.fromkeys(out))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--prefix", default="")
    ap.add_argument("--code-root", default="")
    a = ap.parse_args()
    mb.ROOT = Path(a.project).resolve()  # ponytail: map_build reads its root from a module global; reuse it instead of forking the parser
    cfg = mb.read_config()
    reg = mb.ROOT / cfg["elements_registry"]
    if not reg.exists():
        print(json.dumps({"nodes": [], "edges": [], "flows": [], "tasks": [], "unresolved": []})); return 0
    els = mb.parse_elements(reg.read_text(encoding="utf-8"))
    flows = getattr(mb.parse_elements, "flows", [])
    board = mb.ROOT / cfg["board_file"]
    feats = mb.parse_board(board.read_text(encoding="utf-8")) if board.exists() else {}
    ids = {e["id"] for e in els if e["state"] != "superseded"}
    parents = {e["part_of"] for e in els if e["part_of"]}
    unresolved: list[str] = []
    nodes, edges, seen = [], [], set()
    for e in els:
        if e["id"] not in ids: continue  # superseded: kept for history in the registry, not drawn
        paths = anchors(e["code"], a.prefix, a.code_root, unresolved)
        ui = any(re.search(r"\.(tsx|jsx|vue|svelte)\b|/(plugins?|frontend|web|ui)/", p) for p in paths)
        kind = "external" if not paths and e["id"] not in parents else "ui" if ui else "service"
        n = {"id": e["id"], "label": (e["names"] or [e["id"]])[0], "kind": kind, "summary": e["purpose"],
             "tags": [t for t in (e["state"], e["area"]) if t]}
        if e["part_of"] in ids: n["parent"] = e["part_of"]
        if paths and kind != "external": n["paths"] = paths
        extra = [f"Also called: {', '.join(e['names'][1:])}." if len(e["names"]) > 1 else "", f"Interfaces: {', '.join(e['interfaces'])}." if e["interfaces"] else "",
                 f"State: {e['state']}" + (f" ({e['state_note']})" if e["state_note"] else "") + "."]
        n["details"] = "\n\n".join(x for x in extra if x)
        nodes.append(n)
        for d in e["depends_on"]:  # "Depends on" -> a connection e → d, typed from "(API: /chat)"
            if d in ids and (e["id"], d) not in seen:
                seen.add((e["id"], d)); lab = e["dep_labels"].get(d, "")
                edges.append({"from": e["id"], "to": d, "kind": edge_kind(lab), "label": lab})
    for e in els:  # "Used by" says the same thing from the other side; add it when the other element did not
        for u in e["used_by"]:
            if e["id"] in ids and u in ids and (u, e["id"]) not in seen:
                seen.add((u, e["id"])); edges.append({"from": u, "to": e["id"], "kind": "call", "label": ""})
    out_flows = []
    for f in flows:
        steps = [{"node": s["el"], "note": s["note"] + (" (planned)" if "(planned)" in s["note"] else "")} for s in f["steps"] if s["el"] in ids]
        if len(steps) >= 2: out_flows.append({"id": f["name"], "title": f["title"] or f["name"], "steps": steps})
    # open features -> "recent work": the elements their history lines name, marked changed; closed work is not highlighted
    tasks = []
    for n, f in sorted(feats.items()):
        if f["section"] != "In progress": continue
        items = [{"ref": e["id"], "change": "changed", "note": h["text"][:240]} for e in els if e["id"] in ids for h in e["history"] if h["feature"] == n]
        if items: tasks.append({"title": f["title"][:60], "request": f["title"], "summary": f"Feature {n}, {f['type']}, {f['phase']}.", "items": items})
    print(json.dumps({"nodes": nodes, "edges": edges, "flows": out_flows, "tasks": tasks, "unresolved": unresolved}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
