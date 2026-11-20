#!/usr/bin/env python3
"""Build the project pages: one HTML page per feature and an index, from the activity files the skill writes.

The pages are for the person. The markdown stays the source of truth and stays what agents read; this script
only draws it. It costs no model tokens: the agent writes the same markdown it always writes, in a fixed shape
(`## User summary`, `## Instructions`, `## Clarifications` first), and this script renders it.

The home page (index.html) is the one to keep open while the agent works:
  - Your next steps: everything waiting on you, across all features, with each open question;
  - Recent activity: what happened, what went wrong, what was decided without you — newest first;
  - Ongoing features, most recently worked on first, each with what is happening now and what is next;
  - Project documents: decisions, lessons, standing rules, deferred decisions, the board, the map.
It reloads itself (the "live" switch), so with --watch running it follows the agent without being asked.

What a feature's page adds that the markdown cannot:
  - the user summary always on top, with Now / Running / Next / Waiting on you as a strip, and the step trail;
  - each instruction with whether it is honoured; each question as a card, open ones first;
  - one tab per file of the feature (plan, reviews, build review, agent detail), agent sections folded;
  - what changed since you last pressed "Mark as read" in green, the batch before that in light blue
    (remembered in the browser; the agent writes nothing for it);
  - format problems (a question with no context, a summary with no next step) shown on the page and printed
    here, so the agent that ran this script fixes them before its turn ends.

Usage:  python .a/scripts/page_build.py              build what changed; writes <pages_folder>/index.html
        python .a/scripts/page_build.py --watch      rebuild whenever an activity file changes (Ctrl+C stops)
        python .a/scripts/page_build.py --root P --out D    another project root / output folder
        python .a/scripts/page_build.py --selftest   build a sample in a temp folder and check it

Standard library only. No network. Safe to re-run.
"""
from __future__ import annotations
import argparse, hashlib, html, json, os, re, sys, tempfile, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # <project>/.a/scripts/page_build.py -> <project>
STEPS = ["Root cause", "Plan", "Plan review", "Approved", "Build", "Build review", "Verify", "Closed"]
PHASE_STEP = {"root cause": 0, "start": 1, "read": 1, "evaluate": 1, "clarify": 1, "gate": 1, "review": 2,
              "approved": 3, "implement": 4, "realign": 4, "build review": 5, "verified": 6, "closed": 7}
SUMMARY_FIELDS = ["What this is", "What you asked, as I understand it", "Now", "Running", "Next", "Waiting on you"]
NOTHING = {"", "nothing", "none", "no", "-", "—", "n/a"}
DOCS = [("project_board", "Board"), ("decisions_log", "Decisions"), ("deferred_decisions_log", "Deferred decisions"),
        ("lessons_log", "Lessons"), ("constitution", "Standing rules"), ("implementation_log", "Implementation log"), ("api_docs", "API")]
TRAILS = {"what happened": "done", "what went wrong": "problem", "decided without": "decided", "changes of direction": "direction"}
MONTHS = {m: n for n, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
WHEN_RE = re.compile(r"(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{2,4})(?:,?\s+(\d{1,2}):(\d{2})\s*([AaPp][Mm])?)?")


def parse_when(text: str):
    """The date an entry starts with ('20 Nov 26, 04:15 PM'), or None."""
    m = WHEN_RE.search(text[:50])
    if not m or m.group(2).lower() not in MONTHS:
        return None, text
    year = int(m.group(3)) + (2000 if int(m.group(3)) < 100 else 0)
    hh, mm, ap = int(m.group(4) or 0), int(m.group(5) or 0), (m.group(6) or "").lower()
    hh = hh + 12 if ap == "pm" and hh < 12 else 0 if ap == "am" and hh == 12 else hh
    try:
        when = datetime(year, MONTHS[m.group(2).lower()], int(m.group(1)), hh, mm)
    except ValueError:
        return None, text
    return when, re.sub(r"^[\s·—–\-:]+", "", text[m.end():])


def events(summary_body: str, fallback: datetime) -> list:
    """The dated lines of the user summary's trails, as (when, kind, text)."""
    out = []
    for sec in re.split(r"^###\s+", summary_body, flags=re.M)[1:]:
        head, _, rest = sec.partition("\n")
        kind = next((v for k, v in TRAILS.items() if head.strip().lower().startswith(k)), None)
        if not kind:
            continue
        for m in re.finditer(r"^[-*]\s+(.+(?:\n(?![-*]\s|\s*$|#).+)*)", rest, re.M):
            text = re.sub(r"\s*\n\s*", " ", m.group(1)).strip()
            if text.startswith("<") and text.endswith(">"):
                continue  # an unfilled template line
            when, body = parse_when(text)
            out.append({"when": when or fallback, "dated": bool(when), "kind": kind, "text": body})
    return out


def read_config(root: Path) -> dict:
    cfg = {"activity_folder": "docs/activity/", "pages_folder": "docs/pages/", "project_name": root.name,
           "project_board": "docs/activity/BOARD.md", "decisions_log": "docs/decisions.md", "lessons_log": "docs/lessons.md",
           "constitution": "docs/constitution.md", "deferred_decisions_log": "docs/deferred-decisions.md",
           "implementation_log": "docs/implementation-log.md", "api_docs": "docs/api.md", "map_folder": "docs/map/"}
    p = root / ".a" / "project.md"
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^([a-z_]+):\s*(.+?)\s*$", line)
            if m and m.group(1) in cfg:
                cfg[m.group(1)] = m.group(2).strip("`\"' ")
    return cfg


# ---------------------------------------------------------------- markdown -> html (the subset agents write)
def h(text: str) -> str:
    return hashlib.sha1(re.sub(r"\s+", " ", text).strip().encode("utf-8")).hexdigest()[:10]


def safe_url(u: str) -> str:
    u = u.strip()
    return u if re.match(r"^(https?://|mailto:|#|\.{0,2}/|[A-Za-z0-9_.-]+[/.#])", u) and not re.match(r"^\s*javascript:", u, re.I) else ""


def inline(s: str) -> str:
    out = []
    for part in re.split(r"(`[^`]+`)", s):
        if len(part) > 1 and part.startswith("`") and part.endswith("`"):
            out.append("<code>" + html.escape(part[1:-1], quote=False) + "</code>")
            continue
        t = html.escape(part, quote=True)
        def link(m):
            u = safe_url(html.unescape(m.group(2)))
            return f'<a href="{html.escape(u, quote=True)}">{m.group(1)}</a>' if u else m.group(1)
        t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"~~(.+?)~~", r"<s>\1</s>", t)
        t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", t)
        t = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"<em>\1</em>", t)
        out.append(t)
    return "".join(out)


LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def render_list(items: list) -> str:
    """items: (indent, ordered, text). Nested by indent."""
    out, stack = [], []  # stack of (indent, tag)
    for indent, ordered, text in items:
        tag = "ol" if ordered else "ul"
        while stack and indent < stack[-1][0]:
            out.append(f"</li></{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            out.append(f"<{tag}>")
            stack.append((indent, tag))
        else:
            out.append("</li>")
        box = ""
        m = re.match(r"^\[( |x|X)\]\s+(.*)$", text, re.S)
        if m:
            box = '<span class="box">' + ("&#9745;" if m.group(1).strip() else "&#9744;") + "</span> "
            text = m.group(2)
        out.append(f'<li data-h="{h(text)}">{box}{inline(text)}')
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out)


def md(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines, out, i = text.splitlines(), [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.lstrip().startswith("```"):
            j, body = i + 1, []
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                body.append(lines[j]); j += 1
            out.append("<pre><code>" + html.escape("\n".join(body), quote=False) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", ln)
        if m:
            n = min(len(m.group(1)) + 1, 6)
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
            continue
        if re.match(r"^\s*([-*_])\s*(\1\s*){2,}$", ln):
            out.append("<hr>"); i += 1
            continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            cells = lambda r: [c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(lines[j]); j += 1
            t = ["<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells(ln)) + "</tr></thead><tbody>"]
            for r in rows:
                t.append(f'<tr data-h="{h(r)}">' + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>")
            out.append("".join(t) + "</tbody></table></div>")
            i = j
            continue
        if ln.lstrip().startswith(">"):
            body = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append("<blockquote>" + md("\n".join(body)) + "</blockquote>")
            continue
        if LIST_RE.match(ln):
            items = []
            while i < len(lines):
                m = LIST_RE.match(lines[i])
                if m:
                    items.append([len(m.group(1).expandtabs(4)), m.group(2)[0].isdigit(), m.group(3)])
                elif lines[i].strip() and lines[i].startswith((" ", "\t")) and items:
                    items[-1][2] += "\n" + lines[i].strip()
                elif not lines[i].strip() and i + 1 < len(lines) and (LIST_RE.match(lines[i + 1]) or lines[i + 1].startswith((" ", "\t"))):
                    pass
                else:
                    break
                i += 1
            out.append(render_list(items))
            continue
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|\s*>|\s*\|)", lines[i]) and not LIST_RE.match(lines[i]):
            para.append(lines[i]); i += 1
        p = "\n".join(para)
        out.append(f'<p data-h="{h(p)}">{inline(p).replace(chr(10), "<br>")}</p>')
    return "\n".join(out)


# ---------------------------------------------------------------- reading one activity file
def parse_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    header, body = {}, text
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            k = re.match(r"^([A-Za-z][A-Za-z /]+):\s*(.*)$", line)
            if k:
                header[k.group(1).strip()] = k.group(2).strip()
        body = text[m.end():]
    title = ""
    t = re.search(r"^#\s+(.+)$", body, re.M)
    if t:
        title = t.group(1).strip()
    parts = re.split(r"^##\s+(.+?)\s*$", body, flags=re.M)
    sections = [(parts[k].strip(), parts[k + 1]) for k in range(1, len(parts) - 1, 2)]
    return {"path": path, "header": header, "title": title, "preamble": parts[0], "sections": sections}


def find(sections, *names):
    for name, body in sections:
        low = name.lower()
        if any(low.startswith(n) for n in names):
            return name, body
    return None, ""


def summary_fields(body: str) -> dict:
    out = {}
    for m in re.finditer(r"^\*\*(.+?):\*\*[ \t]*(.*(?:\n(?!\*\*|###|\s*$).*)*)", body, re.M):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


def parse_questions(body: str) -> list:
    qs = []
    for sec in re.split(r"^###\s+", body, flags=re.M)[1:]:
        head, _, rest = sec.partition("\n")
        m = re.match(r"^(Q\d+)\s*(?:·\s*(.*?))?\s*(?:·\s*(open|answered|parked|unanswered))?\s*$", head.strip(), re.I)
        if not m:
            continue
        f = {k.strip(): v.strip() for k, v in re.findall(r"^\*\*(.+?):\*\*[ \t]*((?:.*)(?:\n(?!\*\*).*)*)", rest, re.M)}
        state = (m.group(3) or ("answered" if f.get("Answer") else "open")).lower()
        qs.append({"id": m.group(1), "when": m.group(2) or "", "state": state, "f": f})
    return qs


def lint(doc: dict) -> list:
    """Format problems a person would otherwise have to ask about. Only for files written in the skill's shape."""
    w, secs = [], doc["sections"]
    name, body = find(secs, "user summary")
    if name:
        f = summary_fields(body)
        for need in ("Now", "Next", "Waiting on you", "What you asked, as I understand it"):
            if not f.get(need):
                w.append(f"User summary has no '{need}' line")
        if "### what happened" not in body.lower():
            w.append("User summary has no 'What happened' trail")
    elif (doc["header"].get("Feature") and not find(secs, "summary")[0]  # an older file with the five-point Summary is left alone
          and not doc["path"].name.endswith(".detail.md") and not re.match(r"^\d+\.\d+-", doc["path"].name)):
        w.append("No '## User summary' section at the top")
    _, cl = find(secs, "clarifications", "questions and answers")
    for q in parse_questions(cl):
        need = ["Question", "Context"] + (["Options", "Suggested"] if q["state"] == "open" else ["Answer"] if q["state"] == "answered" else [])
        for n in need:
            if not q["f"].get(n):
                w.append(f"{q['id']} has no {n}")
    return w


# ---------------------------------------------------------------- grouping files into features
def collect(root: Path, cfg: dict, out_dir: Path) -> list:
    act = (root / cfg["activity_folder"]).resolve()
    if not act.exists():
        return []
    docs = []
    for p in sorted(act.rglob("*.md")):
        if p.name.startswith("_") or p.name.upper() == "BOARD.MD" or out_dir in p.parents:
            continue
        docs.append(parse_file(p))
    groups, by_stem = {}, {}
    for d in docs:
        p = d["path"]
        if p.name.endswith(".detail.md"):
            continue
        feat = re.match(r"^\s*(\d+)", d["header"].get("Feature", ""))
        folder = re.match(r"^(\d+)-", p.parent.name)
        own = re.match(r"^(\d+)(?:\.(\d+))?-", p.name)
        if feat:
            key = "F" + feat.group(1)
        elif folder and own and own.group(1) == folder.group(1):
            key = "F" + folder.group(1)
        else:
            key = str(p.relative_to(act).with_suffix("")).replace("\\", "/")
        groups.setdefault(key, []).append(d)
        by_stem[(p.parent, p.stem)] = key
    for d in docs:
        p = d["path"]
        if p.name.endswith(".detail.md"):
            key = by_stem.get((p.parent, p.name[:-len(".detail.md")])) or str(p.relative_to(act).with_suffix("")).replace("\\", "/")
            groups.setdefault(key, []).append(d)
    feats = []
    for key, ds in groups.items():
        def order(d):
            n = d["path"].name
            item = re.match(r"^\d+\.(\d+)-", n)
            return (2, 0) if n.endswith(".detail.md") else (1, int(item.group(1))) if item else (0, 0)
        ds.sort(key=order)
        main = ds[0]
        hd = main["header"]
        ft = hd.get("Feature", "")
        title = (ft.split("·", 1)[1].strip() if "·" in ft else "") or main["title"] or main["path"].stem
        num = key[1:] if key.startswith("F") and key[1:].isdigit() else ""
        date = re.search(r"(\d{4}-\d{2}-\d{2})", str(main["path"]))
        _, sbody = find(main["sections"], "user summary", "summary")
        _, cl = find(main["sections"], "clarifications", "questions and answers")
        mtime = max(d["path"].stat().st_mtime for d in ds)
        feats.append({"key": key, "num": num, "title": title, "docs": ds, "header": hd, "fields": summary_fields(sbody),
                      "open": [q for q in parse_questions(cl) if q["state"] == "open"],
                      "events": events(sbody, datetime.fromtimestamp(mtime)),
                      "open_q": sum(1 for q in parse_questions(cl) if q["state"] == "open"),
                      "warn": [f"{d['path'].name}: {x}" for d in ds for x in lint(d)],
                      "date": date.group(1) if date else "", "mtime": mtime,
                      "page": "f-" + re.sub(r"[^A-Za-z0-9]+", "-", key).strip("-").lower() + ".html"})
    feats.sort(key=lambda f: (0, -int(f["num"])) if f["num"] else (1, f["date"] and -int(f["date"].replace("-", "")) or 0, f["key"]))
    return feats


# ---------------------------------------------------------------- drawing
def chip(text, cls=""):
    return f'<span class="chip {cls}">{html.escape(text)}</span>' if text else ""


def phase_class(phase: str) -> str:
    p = phase.lower()
    return "done" if p.startswith(("closed", "verified")) else "stop" if p.startswith("stopped") else "wait" if p.startswith(("gate", "clarify")) else "run" if p else ""


def trail(header: dict) -> str:
    phase = header.get("Phase", "").strip()
    idx = next((v for k, v in PHASE_STEP.items() if phase.lower().startswith(k)), None)
    if idx is None:
        return ""
    cells = []
    for n, s in enumerate(STEPS):
        cls = "past" if n < idx else "here" if n == idx else "todo"
        cells.append(f'<li class="{cls}">{html.escape(s)}</li>')
    return '<ol class="trail">' + "".join(cells) + "</ol>"


def draw_summary(body: str, header: dict) -> str:
    f = summary_fields(body)
    rest = re.sub(r"^\*\*(.+?):\*\*[ \t]*(.*(?:\n(?!\*\*|###|\s*$).*)*)\n?", "", body, flags=re.M)
    out = ['<section class="summary">']
    if f.get("What this is"):
        out.append(f'<p class="lead" data-h="{h(f["What this is"])}">{inline(f["What this is"])}</p>')
    out.append(trail(header))
    tiles = []
    for k in ("Now", "Running", "Next", "Waiting on you"):
        v = f.get(k, "")
        cls = "need" if k == "Waiting on you" and v.strip().lower().rstrip(".") not in NOTHING else ""
        tiles.append(f'<div class="tile {cls}" data-h="{h(k + v)}"><b>{k}</b><span>{inline(v) if v else "<i>not stated</i>"}</span></div>')
    out.append('<div class="tiles">' + "".join(tiles) + "</div>")
    asked = f.get("What you asked, as I understand it", "")
    if asked:
        out.append(f'<div class="asked" data-h="{h(asked)}"><b>What you asked, as I understand it</b><p>{inline(asked).replace(chr(10), "<br>")}</p></div>')
    for k, v in f.items():
        if k not in SUMMARY_FIELDS:
            out.append(f'<p data-h="{h(k + v)}"><strong>{html.escape(k)}:</strong> {inline(v)}</p>')
    out.append(md(rest))
    out.append("</section>")
    return "".join(out)


def draw_instructions(body: str, status: dict) -> str:
    rows = []
    for m in re.finditer(r"^\s*[-*]\s+(I\d+)\s*·?\s*(.*)$", body, re.M):
        iid, text = m.group(1), m.group(2)
        sup = "superseded" in text.lower()
        st = "superseded" if sup else status.get(iid, "")
        cls = {"honoured": "ok", "deviation": "bad", "question": "wait", "superseded": "old"}.get(st, "")
        rows.append(f'<li class="{"sup" if sup else ""}" data-h="{h(text)}"><span class="iid">{iid}</span><span class="itext">{inline(text)}</span>{chip(st, cls)}</li>')
    return '<ul class="instr">' + "".join(rows) + "</ul>" if rows else md(body)


def draw_questions(body: str, ref: str = "") -> str:
    qs = parse_questions(body)
    if not qs:
        return md(body)
    out = []
    for q in sorted(qs, key=lambda q: 0 if q["state"] == "open" else 1):
        f = q["f"]
        cls = {"open": "wait", "answered": "ok", "parked": "old", "unanswered": "wait"}.get(q["state"], "")
        whole = q["id"] + json.dumps(f, sort_keys=True)
        copy = (f'<button class="copy" data-copy="{html.escape(ref + " " + q["id"] + " — my answer: ", quote=True)}" title="Copies a line to paste into the chat, so the agent knows which question you are answering">copy reply line</button>'
                if q["state"] == "open" else "")
        card = [f'<div class="q {q["state"]}" id="{q["id"]}" data-h="{h(whole)}"><div class="qh"><span class="iid">{q["id"]}</span>{chip(q["state"], cls)}<span class="when">{html.escape(q["when"])}</span>{copy}</div>']
        card.append(f'<p class="qq">{inline(f.get("Question", "")) or "<i class=miss>no question written</i>"}</p>')
        for k in ("Context", "Options", "Suggested", "Answer"):
            v = f.get(k, "")
            if v:
                inner = md(v) if "\n" in v or v.lstrip().startswith(("-", "*")) else f"<p>{inline(v)}</p>"
                card.append(f'<div class="qf {k.lower()}"><b>{k}</b>{inner}</div>')
            elif (k in ("Context",)) or (q["state"] == "open" and k in ("Options", "Suggested")) or (q["state"] == "answered" and k == "Answer"):
                card.append(f'<div class="qf miss"><b>{k}</b><p><i>missing — the agent should have written this</i></p></div>')
        for k, v in f.items():
            if k not in ("Question", "Context", "Options", "Suggested", "Answer"):
                card.append(f'<div class="qf"><b>{html.escape(k)}</b><p>{inline(v)}</p></div>')
        out.append("".join(card) + "</div>")
    return "".join(out)


def tab_label(d: dict, first: bool) -> str:
    n = d["path"].name
    if n.endswith(".detail.md"):
        return "Agent detail"
    m = re.match(r"^(\d+\.\d+)-(.*)\.md$", n)
    if m:
        return m.group(1) + " · " + m.group(2).replace("-", " ")
    return "Summary and plan" if first else d["path"].stem.replace("-", " ")


def draw_doc(d: dict, first: bool, ref: str = "") -> str:
    secs, out = d["sections"], []
    status = {}
    for _, body in secs:
        for m in re.finditer(r"\b(I\d+)\s*[—–-]\s*(honoured|deviation|question)", body, re.I):
            status[m.group(1)] = m.group(2).lower()
    pre = re.sub(r"^#\s+.+$", "", d["preamble"], count=1, flags=re.M).strip()
    if pre:
        out.append('<section class="pre">' + md(pre) + "</section>")
    front = {"user summary": "u", "summary": "u", "instructions": "i", "clarifications": "q", "questions and answers": "q"}
    for name, body in secs:
        kind = next((v for k, v in front.items() if name.lower().startswith(k)), "")
        if kind == "u":
            out.append(f"<h2>{html.escape(name)}</h2>" + (draw_summary(body, d["header"]) if name.lower().startswith("user") else '<section class="summary">' + md(body) + "</section>"))
        elif kind == "i":
            out.append("<h2>Your instructions</h2>" + draw_instructions(body, status))
        elif kind == "q":
            out.append("<h2>Questions and answers</h2>" + draw_questions(body, ref))
        elif body.strip():
            inner = md(body)
            out.append(f'<details class="sec"><summary>{html.escape(name)}</summary>{inner}</details>')
    return "".join(out)


CSS = """
:root{--bg:#fbfbfa;--fg:#1d1f23;--mut:#6b7280;--line:#e3e5e8;--card:#fff;--acc:#2f6fed;--ok:#1f8a4c;--bad:#c0392b;--wait:#b7791f;
--new:#e6f6ea;--newb:#2e9e55;--prev:#e7f1fd;--prevb:#6aa5ee}
@media (prefers-color-scheme:dark){:root{--bg:#16181c;--fg:#e6e8eb;--mut:#9aa3af;--line:#2c3038;--card:#1d2026;--acc:#7aa7ff;--ok:#4cc27f;--bad:#f0776a;--wait:#e0b050;
--new:#16321f;--newb:#3fbf6c;--prev:#14263d;--prevb:#5b93dd}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,Segoe UI,Roboto,sans-serif}
a{color:var(--acc)}main{max-width:1000px;margin:0 auto;padding:16px}
header.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header.top h1{font-size:17px;margin:0;flex:1;min-width:200px}header.top .meta{color:var(--mut);font-size:12px}
button{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:6px;padding:4px 10px;cursor:pointer}
button.on{border-color:var(--acc);color:var(--acc)}
.chip{display:inline-block;font-size:12px;border:1px solid var(--line);border-radius:999px;padding:0 8px;margin-left:6px;color:var(--mut);white-space:nowrap}
.chip.ok,.chip.done{color:var(--ok);border-color:var(--ok)}.chip.bad,.chip.stop{color:var(--bad);border-color:var(--bad)}.chip.wait{color:var(--wait);border-color:var(--wait)}.chip.run{color:var(--acc);border-color:var(--acc)}.chip.old{opacity:.6}
.tabs{display:flex;gap:4px;flex-wrap:wrap;margin:12px 0;border-bottom:1px solid var(--line)}
.tabs button{border-radius:6px 6px 0 0;border-bottom:none}.tabs button.on{background:var(--card);font-weight:600}
.tab{display:none}.tab.on{display:block}
h2{font-size:16px;margin:22px 0 8px}h3{font-size:14.5px;margin:16px 0 6px}h4,h5,h6{font-size:14px;margin:12px 0 4px}
.summary,.q,.pre,details.sec,.card,.warn{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:8px 0}
.lead{font-size:16px;margin:0 0 8px}
.trail{list-style:none;display:flex;flex-wrap:wrap;gap:4px;padding:0;margin:8px 0;font-size:12.5px}
.trail li{padding:2px 9px;border-radius:999px;border:1px solid var(--line);color:var(--mut)}
.trail li.past{color:var(--ok);border-color:var(--ok)}.trail li.here{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:600}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;margin:8px 0}
.tile{border:1px solid var(--line);border-radius:8px;padding:8px 10px}.tile b{display:block;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}
.tile.need{border-color:var(--wait)}.tile.need b{color:var(--wait)}
.asked{border-left:3px solid var(--acc);padding:2px 10px;margin:10px 0}.asked b{font-size:12px;color:var(--mut)}.asked p{margin:2px 0}
ul.instr{list-style:none;padding:0;margin:0}ul.instr li{display:flex;gap:8px;align-items:baseline;padding:6px 8px;border-bottom:1px solid var(--line)}
.iid{font:600 12px ui-monospace,Consolas,monospace;color:var(--mut);min-width:28px}.itext{flex:1}li.sup .itext{text-decoration:line-through;opacity:.6}
.q.open{border-color:var(--wait)}.qh{display:flex;align-items:center;gap:4px}.when{margin-left:auto;color:var(--mut);font-size:12px}
.qq{font-weight:600;margin:6px 0}.qf{margin:6px 0}.qf>b{font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}.qf p,.qf ul{margin:2px 0}
.qf.answer{border-left:3px solid var(--ok);padding-left:10px}.qf.miss,.miss{color:var(--bad)}
details.sec>summary{cursor:pointer;font-weight:600}details.sec[open]>summary{margin-bottom:8px}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{border:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}th{background:rgba(127,127,127,.08)}
pre{overflow-x:auto;background:rgba(127,127,127,.1);padding:8px 10px;border-radius:6px;font-size:12.5px}code{font-family:ui-monospace,Consolas,monospace;font-size:.92em;background:rgba(127,127,127,.12);padding:0 3px;border-radius:3px}pre code{background:none;padding:0}
blockquote{margin:6px 0;padding:2px 12px;border-left:3px solid var(--line);color:var(--mut)}.box{font-size:1.05em}
.warn{border-color:var(--bad)}.warn b{color:var(--bad)}.warn ul{margin:4px 0}
[data-h].new{background:var(--new);box-shadow:inset 3px 0 0 var(--newb)}[data-h].prev{background:var(--prev);box-shadow:inset 3px 0 0 var(--prevb)}
.legend{font-size:12px;color:var(--mut)}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 3px 0 8px;vertical-align:-1px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}.card{margin:0;display:block;color:inherit;text-decoration:none}
.card:hover{border-color:var(--acc)}.card h3{margin:0 0 4px;font-size:15px}.card .row{font-size:13px;margin:2px 0}.card .row b{color:var(--mut);font-weight:500}
.card.need{border-color:var(--wait)}.badge{background:var(--newb);color:#fff;border-radius:999px;font-size:11.5px;padding:0 7px;margin-left:6px}
.todo{background:var(--card);border:1px solid var(--wait);border-radius:8px;padding:10px 14px;margin:8px 0}.todo h3{margin:0 0 4px}.todo ul{margin:4px 0 0;padding-left:20px}
.todo .nx{color:var(--mut);font-size:13px}.none{color:var(--mut)}
ul.feed{list-style:none;padding:0;margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px}
ul.feed li{display:grid;grid-template-columns:118px 1fr;gap:10px;padding:7px 12px;border-bottom:1px solid var(--line)}ul.feed li:last-child{border-bottom:none}
ul.feed .w{color:var(--mut);font-size:12.5px;white-space:nowrap}ul.feed .f{font-size:12.5px}ul.feed .chip{margin-left:0;margin-right:6px}
.chip.problem{color:var(--bad);border-color:var(--bad)}.chip.decided,.chip.direction{color:var(--wait);border-color:var(--wait)}.chip.done{color:var(--ok);border-color:var(--ok)}
.docs{display:flex;flex-wrap:wrap;gap:8px}.docs a{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:4px 12px;text-decoration:none}
button.copy{margin-left:8px;font-size:12px;padding:1px 8px}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--newb);margin-left:6px}
"""

JS = r"""
(function(){
  var KEY='a-pages:'+document.body.dataset.project+':'+document.body.dataset.page, st;
  try{st=JSON.parse(localStorage.getItem(KEY)||'null')}catch(e){st=null}
  var els=[].slice.call(document.querySelectorAll('[data-h]'));
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
  if(!st){st={batch:0,seen:{}};els.forEach(function(e){st.seen[e.dataset.h]=0});save()}
  function paint(){
    var n=0;els.forEach(function(e){var b=st.seen[e.dataset.h];e.classList.remove('new','prev');
      if(b===undefined){e.classList.add('new');n++}else if(st.batch>0&&b===st.batch){e.classList.add('prev')}});
    var c=document.getElementById('newcount');if(c)c.textContent=n?n+' new since you last marked as read':'nothing new';
    var m=document.getElementById('markread');if(m)m.disabled=!n;
    [].forEach.call(document.querySelectorAll('.tabs button,details.sec>summary'),function(b){
      var host=b.tagName==='BUTTON'?document.getElementById(b.dataset.tab):b.parentNode,d=b.querySelector('.dot');
      var has=host&&host.querySelector('[data-h].new');
      if(has&&!d){d=document.createElement('span');d.className='dot';b.appendChild(d)}else if(!has&&d){d.remove()}});
  }
  var mr=document.getElementById('markread');
  if(mr)mr.onclick=function(){st.batch++;var keep={};els.forEach(function(e){var h=e.dataset.h,b=st.seen[h];keep[h]=(b===undefined)?st.batch:b});st.seen=keep;save();paint()};
  [].forEach.call(document.querySelectorAll('.tabs button'),function(b){b.onclick=function(){
    [].forEach.call(document.querySelectorAll('.tabs button,.tab'),function(x){x.classList.remove('on')});
    b.classList.add('on');document.getElementById(b.dataset.tab).classList.add('on');try{sessionStorage.setItem(KEY+':tab',b.dataset.tab)}catch(e){}}});
  try{var t=sessionStorage.getItem(KEY+':tab'),tb=t&&document.querySelector('.tabs button[data-tab="'+t+'"]');if(tb)tb.click();
      var y=sessionStorage.getItem(KEY+':y');if(y)window.scrollTo(0,+y)}catch(e){}
  var ar=document.getElementById('auto'),AK='a-pages:auto';
  function live(){try{return localStorage.getItem(AK)!=='0'}catch(e){return true}}
  function arm(){if(live()){ar&&ar.classList.add('on');setTimeout(function(){try{sessionStorage.setItem(KEY+':y',window.scrollY)}catch(e){}location.reload()},15000)}}
  if(ar)ar.onclick=function(){try{localStorage.setItem(AK,live()?'0':'1')}catch(e){}location.reload()};
  [].forEach.call(document.querySelectorAll('button.copy'),function(b){b.onclick=function(){
    var t=b.dataset.copy,done=function(){var o=b.textContent;b.textContent='copied';setTimeout(function(){b.textContent=o},1200)};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,function(){})}
    else{var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(e){}a.remove()}}});
  if(location.hash){var tgt=document.getElementById(location.hash.slice(1)),tabEl=tgt&&tgt.closest('.tab');
    if(tabEl){var tb2=document.querySelector('.tabs button[data-tab="'+tabEl.id+'"]');if(tb2)tb2.click();tgt.scrollIntoView()}}
  arm();
  [].forEach.call(document.querySelectorAll('a.card[data-hashes]'),function(a){
    var s;try{s=JSON.parse(localStorage.getItem('a-pages:'+document.body.dataset.project+':'+a.dataset.pagekey)||'null')}catch(e){s=null}
    if(!s)return;var n=a.dataset.hashes.split(',').filter(function(x){return x&&s.seen[x]===undefined}).length;
    if(n){var b=document.createElement('span');b.className='badge';b.textContent=n+' new';a.querySelector('h3').appendChild(b)}});
  paint();
})();
"""


def shell(title: str, project: str, page: str, top: str, body: str) -> str:
    built = datetime.now().strftime("%d %b %y, %I:%M %p")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head>"
            f'<body data-project="{html.escape(project, quote=True)}" data-page="{html.escape(page, quote=True)}">'
            f'<header class="top">{top}'
            f'<span class="legend"><span id="newcount"></span><i style="background:var(--newb)"></i>new<i style="background:var(--prevb)"></i>the time before</span>'
            f'<button id="markread">Mark as read</button>'
            f'<button id="auto" title="Reloads this page every 15 seconds so it follows the agent. Click to switch off.">live</button>'
            f'<span class="meta">built {built}</span></header>'
            f"<main>{body}</main><script>{JS}</script></body></html>")


def feature_page(f: dict, project: str) -> str:
    hd = f["header"]
    top = (f'<a href="index.html">&larr; all</a><h1>{html.escape((f["num"] + " · ") if f["num"] else "")}{html.escape(f["title"])}'
           f'{chip(hd.get("Phase", ""), phase_class(hd.get("Phase", "")))}{chip(("tier " + hd["Tier"].split()[0]) if hd.get("Tier") else "")}</h1>'
           )
    body = []
    if f["warn"]:
        body.append('<div class="warn"><b>Format problems — the agent should fix these</b><ul>' + "".join(f"<li>{html.escape(w)}</li>" for w in f["warn"]) + "</ul></div>")
    checks = [f'<b>{k}:</b> {html.escape(hd[k])}' for k in ("Scope check", "Lean check", "Build review", "Pointer", "Updated") if hd.get(k)]
    if checks:
        body.append('<div class="pre" style="font-size:13px">' + " &nbsp;·&nbsp; ".join(checks) + "</div>")
    docs = f["docs"]
    if len(docs) > 1:
        body.append('<div class="tabs">' + "".join(f'<button data-tab="t{n}" class="{"on" if n == 0 else ""}">{html.escape(tab_label(d, n == 0))}</button>' for n, d in enumerate(docs)) + "</div>")
    for n, d in enumerate(docs):
        src = f'<p class="legend">Source: {html.escape(str(d["path"]))}</p>'
        ref = ("Feature " + f["num"]) if f["num"] else f["title"]
        body.append(f'<div class="tab {"on" if n == 0 else ""}" id="t{n}">{draw_doc(d, n == 0, ref)}{src}</div>')
    return shell(f["title"], project, f["page"], top, "".join(body))


def flabel(f: dict) -> str:
    return html.escape(((f["num"] + " · ") if f["num"] else "") + f["title"])


def index_page(feats: list, project: str, links: list) -> str:
    def closed(f):
        return f["header"].get("Phase", "").lower().startswith(("closed", "verified"))

    def needs(f):
        return not closed(f) and (f["fields"].get("Waiting on you", "").strip().lower().rstrip(".") not in NOTHING or f["open_q"] > 0)

    def card(f):
        fl, hd = f["fields"], f["header"]
        rows = "".join(f'<div class="row"><b>{k}:</b> {inline(fl[k])}</div>' for k in ("Now", "Running", "Next") if fl.get(k) and fl[k].strip().lower() not in NOTHING)
        if not rows and fl.get("What this is"):
            rows = f'<div class="row">{inline(fl["What this is"])}</div>'
        if f["warn"]:
            rows += f'<div class="row miss">{len(f["warn"])} format problem(s)</div>'
        hashes = ",".join(sorted(set(re.findall(r'data-h="([0-9a-f]{10})"', f["html"]))))
        upd = datetime.fromtimestamp(f["mtime"]).strftime("%d %b, %I:%M %p")
        return (f'<a class="card {"need" if needs(f) else ""}" href="{f["page"]}" data-pagekey="{f["page"]}" data-hashes="{hashes}">'
                f'<h3>{flabel(f)}{chip(hd.get("Phase", ""), phase_class(hd.get("Phase", "")))}</h3>'
                f'{rows}<div class="row legend">last changed {upd}</div></a>')

    body = []
    # 1. what is waiting on the user, across everything
    todo = []
    for f in sorted((f for f in feats if needs(f)), key=lambda f: -f["mtime"]):
        wait = f["fields"].get("Waiting on you", "").strip()
        qs = "".join(f'<li><a href="{f["page"]}#{q["id"]}">{q["id"]}</a> — {inline(q["f"].get("Question", "") or "question text missing")}</li>' for q in f["open"])
        nx = f["fields"].get("Next", "")
        todo.append(f'<div class="todo" data-h="{h(f["key"] + wait + qs)}"><h3><a href="{f["page"]}">{flabel(f)}</a></h3>'
                    + (f"<div>{inline(wait)}</div>" if wait.lower().rstrip(".") not in NOTHING else "")
                    + (f"<ul>{qs}</ul>" if qs else "") + (f'<div class="nx">Then: {inline(nx)}</div>' if nx else "") + "</div>")
    body.append(f"<h2>Your next steps ({len(todo)})</h2>" + ("".join(todo) or '<p class="none">Nothing is waiting on you.</p>'))
    # 2. what happened lately, newest first
    feed = []
    for f in feats:
        for e in f["events"]:
            feed.append((e["when"], f, e))
        if not f["events"] and not closed(f) and f["header"].get("Phase"):
            feed.append((datetime.fromtimestamp(f["mtime"]), f, {"kind": "", "text": "files changed (this feature has no dated summary lines yet)", "dated": True}))
    feed.sort(key=lambda x: x[0], reverse=True)
    names = {"done": "done", "problem": "problem", "decided": "decided without you", "direction": "change of direction"}
    rows = "".join(f'<li data-h="{h(f["key"] + e["text"])}"><span class="w">{w.strftime("%d %b, %I:%M %p")}</span>'
                   f'<span>{chip(names.get(e["kind"], ""), e["kind"]) if e["kind"] else ""}{inline(e["text"])} <a class="f" href="{f["page"]}">{flabel(f)}</a></span></li>'
                   for w, f, e in feed[:30])
    body.append("<h2>Recent activity</h2>" + (f'<ul class="feed">{rows}</ul>' if rows else '<p class="none">Nothing recorded yet.</p>'))
    # 3. the features, most recently worked on first
    live = sorted((f for f in feats if f["header"].get("Phase") and not closed(f)), key=lambda f: -f["mtime"])
    done = sorted((f for f in feats if closed(f)), key=lambda f: -f["mtime"])
    other = [f for f in feats if not f["header"].get("Phase")]
    body.append(f"<h2>Ongoing ({len(live)})</h2>" + (f'<div class="grid">{"".join(card(f) for f in live)}</div>' if live else '<p class="none">No feature in progress.</p>'))
    if links:
        body.append('<h2>Project documents</h2><div class="docs">' + "".join(f'<a href="{html.escape(u, quote=True)}">{html.escape(t)}</a>' for t, u in links) + "</div>")
    for name, group in (("Finished", done), ("Other documents", other)):
        if group:
            body.append(f"<details class='sec'><summary>{name} ({len(group)})</summary><div class='grid'>{''.join(card(f) for f in group)}</div></details>")
    top = f"<h1>{html.escape(project)} — where things stand</h1>"
    return shell(project, project, "index.html", top, "".join(body))


def build(root: Path, out: Path, quiet=False) -> int:
    cfg = read_config(root)
    out.mkdir(parents=True, exist_ok=True)
    feats = collect(root, cfg, out.resolve())
    warns = 0
    for f in feats:
        f["html"] = feature_page(f, cfg["project_name"])
        (out / f["page"]).write_text(f["html"], encoding="utf-8", newline="\n")
        for w in f["warn"]:
            warns += 1
            print("WARN " + w)
    links, keep = [], {f["page"] for f in feats} | {"index.html"}
    for key, label in DOCS:
        src = root / cfg[key]
        if src.is_file():
            name = "d-" + key.replace("_", "-") + ".html"
            top = f'<a href="index.html">&larr; all</a><h1>{html.escape(label)}</h1>'
            page = md(src.read_text(encoding="utf-8", errors="replace")) + f'<p class="legend">Source: {html.escape(str(src))}</p>'
            (out / name).write_text(shell(label, cfg["project_name"], name, top, page), encoding="utf-8", newline="\n")
            links.append((label, name)); keep.add(name)
    themap = root / cfg["map_folder"] / "map.html"
    if themap.is_file():
        links.append(("Map", os.path.relpath(themap, out).replace("\\", "/")))
    (out / "index.html").write_text(index_page(feats, cfg["project_name"], links), encoding="utf-8", newline="\n")
    for old in list(out.glob("f-*.html")) + list(out.glob("d-*.html")):
        if old.name not in keep:
            old.unlink()
    if not quiet:
        print(f"pages: {len(feats)} built, {warns} format problem(s) -> {out / 'index.html'}")
    return warns


def signature(root: Path) -> tuple:
    cfg = read_config(root)
    act = root / cfg["activity_folder"]
    files = list(act.rglob("*.md")) if act.exists() else []
    files += [root / cfg[k] for k, _ in DOCS if (root / cfg[k]).is_file()]
    return tuple(sorted((str(p), p.stat().st_mtime_ns) for p in files))


SAMPLE = """---
Feature: 11 · Usage report only for devs
Phase: Gate
Tier: M (signals: permission path)
Scope check: plan 20 Nov 26 — clean
Lean check: plan 20 Nov 26 — clean
---

## User summary

**What this is:** Stop admins opening the usage report; devs keep it.
**What you asked, as I understand it:** Admins must not be able to get the usage report by any route, not only lose the menu entry.
**Now:** Plan written, waiting for your answer to one question.
**Running:** nothing
**Next:** you answer Q1, then the plan review.
**Waiting on you:** 1 question

### What happened
- 20 Nov 26, 03:50 PM · Start — read your request · nothing changed yet
- 20 Nov 26, 04:15 PM · Plan — read the report code · the menu and the API both serve it, so both must change · because hiding the menu alone leaves the data reachable

### Decided without you
- 20 Nov 26, 04:18 PM — kept the export job in scope · it reads the same data · say "leave the export" to drop it

## Instructions

- I1 · 20 Nov 26, 04:10 PM — "Admins should no longer have access to the usage report. Only devs."

## Clarifications

### Q1 · 20 Nov 26, 04:20 PM · open
**Question:** What should an admin with a bookmark see?
**Context:** Some admins have the page bookmarked. After the change the page will refuse them, and you decide how that looks.
**Options:**
- An error message — clearest, one line of code
- A redirect to the home page — quieter, hides why
**Suggested:** An error message — it tells the person what changed.

### Q2 · 20 Nov 26, 04:21 PM · open
**Question:** Keep the nightly export?

## Report

### Instruction check
I1 — honoured (steps 1-3)
"""


def selftest() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        folder = root / "docs" / "activity" / "11-usage-report"
        folder.mkdir(parents=True)
        (folder / "11-usage-report.md").write_text(SAMPLE, encoding="utf-8")
        (folder / "11.1-build-review-usage-report.md").write_text("## In short\n\nShallow: the route is open.\n", encoding="utf-8")
        (folder / "11-usage-report.detail.md").write_text("## Event log\n\n- E1 · asked\n", encoding="utf-8")
        legacy = root / "docs" / "activity" / "2026-11" / "2026-11-19"
        legacy.mkdir(parents=True)
        (legacy / "03-older-work.md").write_text("# Older work\n\n- **Status:** done\n\n## Summary (plain language)\n\n1. **The issue:** x <script>alert(1)</script>\n", encoding="utf-8")
        (root / "docs" / "decisions.md").write_text("# Decisions\n\n## 20 Nov 26 — error, not redirect\nReasons: clearer.\n", encoding="utf-8")
        out = root / "docs" / "pages"
        warns = build(root, out, quiet=True)
        page = (out / "f-f11.html").read_text(encoding="utf-8")
        index = (out / "index.html").read_text(encoding="utf-8")
        checks = {
            "three tabs for the feature": page.count('data-tab="t') == 3,
            "summary tiles drawn": 'class="tile need"' in page and "Plan written" in page,
            "step trail marks Plan as current": '<li class="here">Plan</li>' in page,
            "instruction shows honoured": ">honoured<" in page,
            "open question card with context": "Some admins have the page bookmarked" in page,
            "question without context is flagged": "Q2 has no Context" in page and warns >= 3,
            "legacy file gets its own page": (out / "f-2026-11-2026-11-19-03-older-work.html").exists(),
            "html in markdown is escaped": "<script>alert(1)</script>" not in (out / "f-2026-11-2026-11-19-03-older-work.html").read_text(encoding="utf-8"),
            "home: your next steps lists the open questions": "Your next steps (1)" in index and 'href="f-f11.html#Q1"' in index and "What should an admin with a bookmark see?" in index,
            "home: recent activity, newest first": 0 < index.find("kept the export job") < index.find("read the report code") < index.find("read your request"),
            "home: ongoing features and older documents": "Ongoing (1)" in index and "Other documents (1)" in index,
            "home: project documents linked and built": 'href="d-decisions-log.html"' in index and (out / "d-decisions-log.html").exists(),
            "open question has an anchor and a reply line to copy": 'id="Q1"' in page and "Feature 11 Q1" in page,
            "pages are live unless switched off": "!=='0'" in page,
        }
        bad = [k for k, ok in checks.items() if not ok]
        for k, ok in checks.items():
            print(("ok   " if ok else "FAIL ") + k)
        return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    root = a.root.resolve()
    out = (a.out or root / read_config(root)["pages_folder"]).resolve()
    build(root, out)
    if a.watch:
        print("watching for changes - Ctrl+C to stop")
        sig = signature(root)
        try:
            while True:
                time.sleep(2)
                now = signature(root)
                if now != sig:
                    sig = now
                    build(root, out)
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
