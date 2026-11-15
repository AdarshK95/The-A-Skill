#!/usr/bin/env python3
"""Build the interactive map (one self-contained HTML file) from the project's elements registry.

Source of truth: docs/map/elements.md (the registry), plus the board (feature titles and states) and the
decisions and deferred-decisions logs (entries that name an element). The Mermaid overview in the board is
another view of the same registry; this script never reads it.

Usage:  python .a/scripts/map_build.py            (reads .a/project.md for paths; writes docs/map/map.html)
        python .a/scripts/map_build.py --out path/to/map.html

Standard library only. No network. Safe to re-run; the output is regenerated in full.
"""
from __future__ import annotations
import argparse, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # <project>/.a/scripts/map_build.py → <project>

def read_config():
    cfg = {"elements_registry": "docs/map/elements.md", "board_file": "docs/activity/BOARD.md", "observed_file": "docs/map/observed.jsonl", "trace_link": "",
           "decisions_log": "docs/decisions.md", "deferred_decisions_log": "docs/deferred-decisions.md",
           "activity_folder": "docs/activity/", "project_name": ROOT.name, "areas": []}
    p = ROOT / ".a" / "project.md"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([a-z_]+):\s*(.+?)\s*$", line)
            if m and m.group(1) in cfg and m.group(1) != "areas":
                cfg[m.group(1)] = m.group(2).strip("`\"' ")
        m = re.search(r"^areas:\s*\n((?:\s+-\s+.+\n)+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            cfg["areas"] = [re.sub(r"^\s+-\s+", "", a).strip() for a in m.group(1).splitlines() if a.strip()]
    return cfg

LAYERS = ["entry", "api", "orchestration", "agents", "stores", "platform"]

def parse_flows(block):
    """The `## Flows` block: '### name · title' then numbered steps 'N. element · note', then 'Sources:'. Fragments: '### name (fragment, F7) · …'."""
    flows = {}
    for sec in re.split(r"^### ", block, flags=re.M)[1:]:
        lines = sec.splitlines()
        head = lines[0].strip()
        m = re.match(r"^([A-Za-z0-9_-]+)\s*(\(fragment[^)]*\))?\s*(?:·\s*(.*))?$", head)
        if not m: continue
        name, frag, title = m.group(1), bool(m.group(2)), (m.group(3) or "").strip()
        steps, sources = [], ""
        for ln in lines[1:]:
            sm = re.match(r"^\s*(\d+[a-z]?)\.\s+([A-Za-z0-9_-]+)\s*(?:·\s*(.*))?$", ln)
            if sm: steps.append({"n": sm.group(1), "el": sm.group(2), "note": (sm.group(3) or "").strip()}); continue
            src = re.match(r"^Sources:\s*(.*)$", ln)
            if src: sources = src.group(1).strip()
        f = flows.setdefault(name, {"name": name, "title": "", "steps": [], "fragments": [], "sources": []})
        if frag: f["fragments"].append({"steps": steps, "sources": sources})
        else:
            f["steps"] = steps
            if title: f["title"] = title
        if sources: f["sources"].append(sources)
    # merge fragments: a step whose element is absent is inserted after its predecessor in the fragment;
    # a step numbered like "4a" with no predecessor goes after the flow's step 4; otherwise at the end
    for f in flows.values():
        order = [st["el"] for st in f["steps"]]
        for fr in f["fragments"]:
            prev = None
            for st in fr["steps"]:
                if st["el"] not in order:
                    if prev in order:
                        i = order.index(prev) + 1
                    else:
                        m = re.match(r"^(\d+)", st["n"]); k = int(m.group(1)) if m else None
                        i = min(k, len(order)) if k else len(order)
                    order.insert(i, st["el"]); f["steps"].insert(i, {**st, "fragment": True})
                prev = st["el"]
        for i, st in enumerate(f["steps"]): st["n"] = str(i + 1)
    return list(flows.values())

def parse_relations(val):
    """'chat-store (Cosmos: conversations) · agent-pipeline (call: run)' → ids and {id: label}."""
    ids, labels = [], {}
    for item in re.split(r"\s·\s", val):
        item = item.strip().strip("`")
        if not item or item.lower() in ("none", "(none)", "-", "—"): continue
        m = re.match(r"^([A-Za-z0-9_-]+)\s*(?:\((.*)\))?\s*$", item)
        if not m:
            m2 = re.match(r"^([A-Za-z0-9_-]+)", item)
            if not m2: continue
            ids.append(m2.group(1)); continue
        ids.append(m.group(1))
        if m.group(2): labels[m.group(1)] = m.group(2).strip()
    return ids, labels

def parse_elements(text):
    els = []
    flows = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        lines = block.splitlines()
        eid = lines[0].strip()
        if eid.lower().startswith("flows"):
            flows = parse_flows(block); continue
        if not eid or " " in eid or eid.startswith("<") or eid.startswith("!"):  # element ids have no spaces; prose headings are skipped
            continue
        el = {"id": eid, "names": [], "purpose": "", "code": [], "interfaces": [], "depends_on": [],
              "used_by": [], "dep_labels": {}, "events": [], "state": "stable", "state_note": "", "area": "", "layer": "", "part_of": "", "sources": [], "history": []}
        cur = None
        for ln in lines[1:]:
            if ln.startswith("#"):  # a sub-heading (###) ends the element; nothing below it belongs to it
                break
            m = re.match(r"^([A-Za-z ]+):\s*(.*)$", ln)
            if m and m.group(1).strip() in ("Names", "Purpose", "Code", "Interfaces", "Depends on", "Used by", "State", "Note", "Area", "Layer", "Part of", "Events", "Sources", "History"):
                key, val = m.group(1).strip(), m.group(2).strip()
                cur = key
                if key == "Names": el["names"] = [x.strip() for x in re.split(r"\s·\s|,", val) if x.strip()]
                elif key == "Purpose": el["purpose"] = val
                elif key == "Code": el["code"] = [x.strip() for x in re.split(r"\s·\s", val) if x.strip()]
                elif key == "Interfaces": el["interfaces"] = [x.strip() for x in re.split(r"\s·\s|,", val) if x.strip()]
                elif key == "Depends on": el["depends_on"], el["dep_labels"] = parse_relations(val)
                elif key == "Used by": el["used_by"], _ = parse_relations(val)
                elif key == "State":
                    v = val.lower().strip("`")
                    el["state"] = next((st for st in ("in change", "untouched", "superseded", "unwired", "planned", "stable") if v.startswith(st)), "stable")
                    note = v[len(el["state"]):].strip(" ()-—·")
                    if note: el["state_note"] = note
                elif key == "Note": el["state_note"] = val
                elif key == "Area": el["area"] = val
                elif key == "Layer":
                    v = val.lower().strip("`")
                    el["layer"] = next((L for L in LAYERS if v.startswith(L)), "")
                elif key == "Events": el["events"] = [x.strip().strip("`") for x in re.split(r"\s·\s|,", val) if x.strip() and x.strip().lower() not in ("none", "(none)")]
                elif key == "Part of":
                    v = val.strip().strip("`")
                    el["part_of"] = "" if v.lower() in ("", "none", "(none)", "-", "—") else v.split()[0].strip(",·")
                elif key == "Sources": el["sources"] = [x.strip() for x in re.split(r"\s·\s", val) if x.strip()]
                continue
            if cur == "History" and ln.strip().startswith("- "):
                h = ln.strip()[2:]
                parts = [x.strip() for x in h.split(" · ")]
                feat = re.search(r"\b(?:F|[Ff]eature\s+)(\d+)\b", h)
                el["history"].append({"date": parts[0] if parts else "", "text": h, "feature": int(feat.group(1)) if feat else None})
        els.append(el)
    parse_elements.flows = flows
    return els

def parse_board(text):
    feats = {}
    section = ""
    for ln in text.splitlines():
        m = re.match(r"^## (.+)$", ln)
        if m: section = m.group(1).strip(); continue
        m = re.match(r"^### (\d+) · (.+?) · (\w+) · (\w+) · pointer (.+?) · updated (.+?) · (\S+)", ln)
        if m:
            feats[int(m.group(1))] = {"n": int(m.group(1)), "title": m.group(2), "type": m.group(3), "phase": m.group(4),
                                      "pointer": m.group(5), "updated": m.group(6), "file": m.group(7), "section": section}
            continue
        m = re.match(r"^\| \w+ \| (\d+) \| (.+?) \| (\w+) \| (\w+) \| (.+?) \| (.+?) \| (\S+) \|", ln)
        if m and section.startswith("Finished"):
            feats[int(m.group(1))] = {"n": int(m.group(1)), "title": m.group(2), "type": m.group(3), "phase": "Closed",
                                      "pointer": "", "updated": m.group(5), "file": m.group(7), "section": "Finished"}
    return feats

def parse_decisions(text, kind, elements=None):
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head = block.splitlines()[0].strip()
        m = re.search(r"^Elements:\s*(.+)$", block, re.M)
        els = [x.strip().strip("`") for x in re.split(r"\s·\s|,", m.group(1))] if m else []
        if not els and elements:  # older entries without an Elements field: match an element's id or any of its names in the text
            low = block.lower()
            def hit(e):
                if re.search(r"(?<![\w-])" + re.escape(e["id"].lower()) + r"(?![\w-])", low): return True
                return any(" " in n and re.search(r"\b" + re.escape(n.lower()) + r"\b", low) for n in e["names"])
            els = [e["id"] for e in elements if hit(e)]
        dec = re.search(r"^Decision:\s*(.+)$", block, re.M)
        reopen = re.search(r"^Reopen when:\s*(.+)$", block, re.M)
        out.append({"kind": kind, "head": head, "elements": els, "decision": dec.group(1).strip() if dec else "",
                    "reopen": reopen.group(1).strip() if reopen else "", "by_name": not bool(m) and bool(els)})
    return out

HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — map</title>
<style>
:root{--bg:#fafafa;--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--card:#fff;--box:#f3f5f7;--panel:#f6f8fa;--hi:#d97706;--flow:#0969da;
 --stable:#1a7f37;--inchange:#0969da;--planned:#6e7781;--unwired:#9a6700;--untouched:#8250df;--superseded:#afb8c1}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#8b949e;--line:#30363d;--card:#161b22;--box:#11161d;--panel:#161b22;--flow:#58a6ff;
 --stable:#3fb950;--inchange:#58a6ff;--planned:#8b949e;--unwired:#d29922;--untouched:#bc8cff;--superseded:#6e7681}}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;font:13px/1.45 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);display:grid;grid-template-rows:auto 1fr auto}
header{display:flex;gap:8px;align-items:center;padding:8px 14px;border-bottom:1px solid var(--line);flex-wrap:wrap;background:var(--card)}
header h1{font-size:15px;font-weight:600;margin:0 10px 0 0}header input,header select,header button{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
header button{cursor:pointer}header button.on{background:var(--flow);color:#fff;border-color:var(--flow)}.legend{margin-left:auto;display:flex;gap:12px;color:var(--muted);font-size:12px}.legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
main{display:grid;grid-template-columns:1fr 0;min-height:0;transition:grid-template-columns .2s;position:relative}main.open{grid-template-columns:1fr 390px}main.open.folded{grid-template-columns:1fr 0}
#handle{position:absolute;right:0;top:50%;transform:translateY(-50%);z-index:3;display:none;width:22px;height:48px;border:1px solid var(--line);border-right:0;border-radius:8px 0 0 8px;background:var(--card);color:var(--muted);cursor:pointer;font-size:16px;line-height:46px;text-align:center}
main.open #handle{display:block;right:390px}main.open.folded #handle{right:0}
#zoom{position:absolute;left:12px;bottom:12px;z-index:3;display:flex;gap:4px}#zoom button{width:28px;height:28px;padding:0;font-size:16px}
#canvas{cursor:grab}#canvas.panning{cursor:grabbing}
#canvas{overflow:auto;position:relative;padding:10px}svg{display:block}
aside{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:14px 16px;display:none}main.open aside{display:block}
aside h2{font-size:16px;margin:0 0 2px;font-weight:600}aside h3{font-size:11px;margin:16px 0 4px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
aside .muted{color:var(--muted)}aside ul,aside ol{padding-left:18px;margin:4px 0}aside li{margin:2px 0}aside code{font-size:12px;background:var(--bg);padding:1px 5px;border-radius:4px;border:1px solid var(--line)}
aside a{color:var(--inchange);text-decoration:none;cursor:pointer}aside a:hover{text-decoration:underline}
.close{float:right;background:none;border:0;color:var(--muted);font-size:18px;cursor:pointer;line-height:1}
.node{cursor:pointer}.node .card{fill:var(--card);stroke:var(--line);rx:8}.node .stripe{rx:2}.node .name{font-size:12.5px;font-weight:600;fill:var(--fg)}.node .sub{font-size:11px;fill:var(--muted)}
.node .parts{font-size:11px;fill:var(--inchange);font-weight:600}.node:hover .card{stroke:var(--fg)}.hi>.card,.hi>.boxrect{stroke:var(--hi)!important;stroke-width:2}.dim{opacity:.38}
.node.others .card{stroke-dasharray:4 3;fill:none}
.box .boxrect{fill:none;stroke:var(--line);stroke-dasharray:4 5;rx:10}.box .boxtitle{font-size:12.5px;font-weight:600;fill:var(--fg)}.box .boxsub{font-size:10.5px;fill:var(--muted)}.box .collapse{font-size:12px;fill:var(--inchange);font-weight:600;cursor:pointer}
.rowlabel{font-size:10px;fill:var(--muted);text-transform:uppercase;letter-spacing:.08em}.rowline{stroke:var(--line);stroke-dasharray:2 4}
.node.onflow>.card,.box.onflow>.boxrect{stroke:var(--flow)!important;stroke-width:2}.step{font-size:11px;font-weight:700;fill:#fff}.stepbg{fill:var(--flow)}
.edge{stroke:var(--muted);stroke-width:1.2;fill:none;opacity:.55;marker-end:url(#arrow)}.edge.hidden{display:none}.edge.hi{stroke:var(--hi);opacity:1;stroke-width:1.8;display:block}
.edge.flow{stroke:var(--flow);opacity:.9;stroke-width:2;marker-end:url(#arrowflow)}.edge.ext{opacity:.5}
.node .err{font-size:10.5px;font-weight:700;fill:#d1242f}.node .obs{font-size:10.5px;fill:var(--muted)}.edge.obs{opacity:.75}
.elabel{font-size:10.5px;fill:var(--fg)}.elabelbg{fill:var(--bg);stroke:var(--line);rx:4}
footer{padding:4px 14px;border-top:1px solid var(--line);color:var(--muted);font-size:11px;background:var(--card)}
.timeline li{margin-bottom:8px}.timeline .d{color:var(--muted);font-size:11px}
</style></head><body>
<header><h1>__TITLE__</h1>
<input id="q" placeholder="search" size="20">
<select id="state"><option value="">all states</option><option>stable</option><option>in change</option><option>planned</option><option>unwired</option><option>untouched</option><option>superseded</option></select>
<select id="flow"><option value="">all flows</option></select>
<button id="unmapped" title="event names in the observed data that no element claims" style="display:none"></button>
<button id="allEdges" title="show every dependency, not only flows and externals">all connections</button>
<button id="expandAll" title="open or close every container">expand all</button><button id="reset">clear</button>
<span class="legend"><span><i style="background:var(--stable)"></i>stable</span><span><i style="background:var(--inchange)"></i>in change</span><span><i style="background:var(--planned)"></i>planned</span><span><i style="background:var(--unwired)"></i>unwired</span><span><i style="background:var(--untouched)"></i>untouched</span></span></header>
<main id="main"><div id="canvas"></div><div id="handle" title="hide or show the panel">›</div><div id="zoom"><button id="zin" title="zoom in">+</button><button id="zout" title="zoom out">−</button><button id="zfit" title="fit width">⤢</button></div><aside id="panel"></aside></main>
<footer><span id="meta"></span> · inside a box, one row per flow, steps left to right · externals beside the part that uses them · lines shown: flows and externals, all on selection</footer>
<script>
const DATA=__DATA__;
const OBS=DATA.observed;const obsEl=id=>OBS&&OBS.elements[id];
// observed stats for a drawn box: itself, or the sum over the parts it stands for
const obsFor=id=>{if(!OBS)return null;const ids=[id,...DATA.elements.filter(e=>ancestorsOf(e.id).includes(id)).map(e=>e.id)];let t=0,er=0,ms=[];ids.forEach(x=>{const o=OBS.elements[x];if(o){t=Math.max(t,o.turns);er+=o.errors;if(o.ms!=null)ms.push(o.ms)}});return t||er?{turns:t,errors:er,ms:ms.length?Math.round(ms.reduce((a,b)=>a+b,0)/ms.length):null}:null};
const ancestorsOf=id=>{const a=[];let k=DATA.elements.find(e=>e.id===id);const map=Object.fromEntries(DATA.elements.map(e=>[e.id,e]));while(k&&k.part_of&&map[k.part_of]){a.push(k.part_of);k=map[k.part_of]}return a};
if(OBS)DATA.flows=DATA.flows.concat(OBS.flows);
const colors={stable:'var(--stable)','in change':'var(--inchange)',planned:'var(--planned)',unwired:'var(--unwired)',untouched:'var(--untouched)',superseded:'var(--superseded)'};
const byId=Object.fromEntries(DATA.elements.map(e=>[e.id,e]));
const kidsOf={};DATA.elements.forEach(e=>{if(e.part_of&&byId[e.part_of])(kidsOf[e.part_of]=kidsOf[e.part_of]||[]).push(e)});
const children=id=>kidsOf[id]||[];
const roots=DATA.elements.filter(e=>!e.part_of||!byId[e.part_of]);
const isContainer=e=>children(e.id).length>0;
const featCount=e=>e.history.filter(h=>h.feature!=null).length;
const decsFor=id=>DATA.decisions.filter(d=>d.elements.includes(id));
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ancestors=id=>{const a=[];let k=byId[id];while(k&&k.part_of&&byId[k.part_of]){a.push(k.part_of);k=byId[k.part_of]}return a};
const within=(id,cont)=>ancestors(id).includes(cont);
// flow position: first appearance (first flow listed wins)
const flowPos={};DATA.flows.forEach((f,fi)=>f.steps.forEach((st,si)=>{if(flowPos[st.el]==null)flowPos[st.el]=fi*1000+si}));
const orderOf=id=>{const own=flowPos[id];const ks=children(id).map(k=>orderOf(k.id)).filter(v=>v<1e9);const m=ks.length?Math.min(...ks):1e9;return Math.min(own==null?1e9:own,m)};
const byOrder=(a,b)=>orderOf(a.id)-orderOf(b.id)||a.id.localeCompare(b.id);
const open=new Set(roots.filter(isContainer).map(r=>r.id));const othersOpen=new Set(DATA.elements.filter(isContainer).map(e=>e.id));
let selected=null,activeFlow=null,allEdges=false;
const isOpen=id=>open.has(id);
// the visible node standing for an element: itself, or its first closed ancestor, or its container's "others" card
const repRaw=id=>{const e=byId[id];if(!e)return null;const chain=ancestors(id).reverse();for(const anc of chain){if(!isOpen(anc))return anc}return id};
const rep=id=>{const r=repRaw(id);if(r==null)return id;if(r!==id)return r;const e=byId[id];if(e.part_of&&byId[e.part_of]&&!onAnyFlowRow(id)&&!othersOpen.has(e.part_of))return 'others:'+e.part_of;return id};
function onAnyFlowRow(id){return flowPos[id]!=null||children(id).some(k=>onAnyFlowRow(k.id))}
const W=200,H=54,GX=26,GY=30,PAD=18,TITLE=36,LABELW=86,OTHCOLS=4;
// --- layout ---
const geo={};
function measure(e){const kids=children(e.id);if(!kids.length||!isOpen(e.id)){geo[e.id]={w:W,h:H,leaf:true};return geo[e.id]}const nested=!!(e.part_of&&byId[e.part_of]);const LW=nested?0:LABELW,PD=nested?12:PAD;
  kids.forEach(measure);
  const kidFor=id=>kids.find(c=>c.id===id||within(id,c.id));
  // cells: {row,col} per child. Row 0 = the first flow that touches this container, left to right in step order.
  // Each later flow adds only the children it introduces, in the row below, in the column of the step it branched from.
  const cell={},rowsMeta=[];const taken=new Set();let ncols=0;
  const flowsHere=DATA.flows.filter(f=>f.steps.some(st=>kidFor(st.el)));
  flowsHere.forEach((f,fi)=>{let col=-1,added=false;const rowIdx=rowsMeta.length;
    f.steps.forEach(st=>{const k=kidFor(st.el);if(!k)return;if(cell[k.id]){col=cell[k.id].col;return}
      if(rowIdx===0){col=col+1}else{col=Math.max(0,col)}
      while(taken.has(rowIdx+':'+col))col++;
      cell[k.id]={row:rowIdx,col};taken.add(rowIdx+':'+col);ncols=Math.max(ncols,col+1);added=true});
    if(added)rowsMeta.push({label:f.name})});
  const others=kids.filter(k=>!cell[k.id]).sort(byOrder);
  let othersRows=0;
  if(others.length){if(othersOpen.has(e.id)){const cols=Math.max(ncols,OTHCOLS);others.forEach((k,i)=>{const r=rowsMeta.length+Math.floor(i/cols),c=i%cols;cell[k.id]={row:r,col:c};ncols=Math.max(ncols,c+1)});othersRows=Math.ceil(others.length/cols);for(let i=0;i<othersRows;i++)rowsMeta.push({label:i===0?'other parts':'',others:true})}
    else{cell['others:'+e.id]={row:rowsMeta.length,col:0,othersCard:true,count:others.length,of:e.id};rowsMeta.push({label:'',othersCard:true});ncols=Math.max(ncols,1)}}
  if(!ncols)ncols=1;
  // row heights from the tallest child in the row
  const rowH=rowsMeta.map(()=>H);for(const id in cell){const c=cell[id];const h=c.othersCard?H:geo[id].h;rowH[c.row]=Math.max(rowH[c.row],h)}
  // column widths from the widest child in the column (an open sub-container is wider than a card)
  const colW=Array.from({length:ncols},()=>W);for(const id in cell){const c=cell[id];const w=c.othersCard?W:geo[id].w;colW[c.col]=Math.max(colW[c.col],w)}
  const w=colW.reduce((a,b)=>a+b,0)+GX*(ncols-1),h=rowH.reduce((a,b)=>a+b,0)+GY*(rowsMeta.length-1);
  geo[e.id]={w:w+PD*2+LW,h:TITLE+PD+h+PD,leaf:false,cell,rowsMeta,rowH,colW,nested,PD,LW};return geo[e.id]}
function place(e,x,y){const g=geo[e.id];g.x=x;g.y=y;if(g.leaf)return;
  const rowY=[];let cy=y+TITLE+g.PD;g.rowsMeta.forEach((r,i)=>{rowY[i]=cy;r.y=cy;cy+=g.rowH[i]+GY});
  const colX=[];let cx=x+g.PD+g.LW;g.colW.forEach((w,i)=>{colX[i]=cx;cx+=w+GX});
  for(const id in g.cell){const c=g.cell[id];if(c.othersCard){geo[id]={x:colX[c.col],y:rowY[c.row],w:W,h:H,leaf:true,othersCard:true,count:c.count,of:c.of};continue}place(byId[id],colX[c.col],rowY[c.row])}}
function layout(){for(const k in geo)delete geo[k];
  const conts=roots.filter(isContainer).sort(byOrder),exts=roots.filter(r=>!isContainer(r)).sort(byOrder);
  // containers left to right in flow order; an external with a flow position between two containers goes between them, others into the right-hand column
  let x=16,maxH=0;const seq=[];const inline=exts.filter(x=>flowPos[x.id]!=null&&conts.some(c=>orderOf(c.id)>flowPos[x.id])&&conts.some(c=>orderOf(c.id)<flowPos[x.id]));
  const all=[...conts,...inline].sort(byOrder);all.forEach(r=>{measure(r);place(r,x,16);x+=geo[r.id].w+44;maxH=Math.max(maxH,geo[r.id].h)});
  const col=exts.filter(x=>!inline.includes(x));let ey=16;col.forEach(ex=>{measure(ex);
    // align to the first drawn part that connects to it
    const users=DATA.elements.filter(e=>e.depends_on.includes(ex.id)).map(e=>geo[rep(e.id)]).filter(Boolean);const ty=users.length?Math.min(...users.map(g=>g.y)):ey;const y=Math.max(ey,ty);place(ex,x,y);ey=y+H+GY;maxH=Math.max(maxH,y+H)});
  return {width:x+W+30,height:maxH+40}}
// --- render ---
let render=function(){
  const filter=window.filter;const Lo=layout(),ns='http://www.w3.org/2000/svg';const svg=document.createElementNS(ns,'svg');svg.setAttribute('width',Lo.width);svg.setAttribute('height',Lo.height);
  svg.innerHTML=`<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L9 5L0 9z" fill="var(--muted)"/></marker><marker id="arrowflow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L9 5L0 9z" fill="var(--flow)"/></marker></defs>`;
  const el=(t,a)=>{const n=document.createElementNS(ns,t);for(const k in a)n.setAttribute(k,a[k]);return n};
  const edgeLayer=el('g',{});svg.appendChild(edgeLayer);
  const visible=e=>(!filter.state||e.state===filter.state)&&(!filter.q||(e.id+' '+e.names.join(' ')+' '+e.code.join(' ')+' '+e.purpose).toLowerCase().includes(filter.q));
  const flow=activeFlow?DATA.flows.find(f=>f.name===activeFlow):null;const flowIds=flow?flow.steps.map(s=>rep(s.el)):[];
  const drawNode=(e)=>{const g=geo[e.id];if(!g)return;const kids=children(e.id);const onflow=flow&&flowIds.includes(e.id);
    if(!g.leaf){const grp=el('g',{class:'box'+(onflow?' onflow':'')});grp.dataset.id=e.id;grp.appendChild(el('rect',{class:'boxrect',x:g.x,y:g.y,width:g.w,height:g.h}));
      grp.appendChild(el('rect',{x:g.x,y:g.y+11,width:4,height:TITLE-16,rx:2,fill:colors[e.state]||colors.stable}));
      const t=el('text',{class:'boxtitle',x:g.x+14,y:g.y+23});t.textContent=e.names[0]||e.id;grp.appendChild(t);
      const st=el('text',{class:'boxsub',x:g.x+14+((e.names[0]||e.id).length*7.4),y:g.y+23});st.textContent=`${kids.length} parts`;grp.appendChild(st);
      const c=el('text',{class:'collapse',x:g.x+g.w-12,y:g.y+23,'text-anchor':'end'});c.textContent='−';c.addEventListener('click',ev=>{ev.stopPropagation();open.delete(e.id);render()});grp.appendChild(c);
      grp.querySelector('.boxrect').addEventListener('click',()=>select(e.id));grp.querySelector('.boxtitle').addEventListener('click',()=>select(e.id));svg.appendChild(grp);
      if(!g.nested)g.rowsMeta.forEach(r=>{if(r.label){const l=el('text',{class:'rowlabel',x:g.x+PAD,y:r.y+16});l.textContent=r.label.slice(0,13);svg.appendChild(l)}});
      for(const id in g.cell){const c=g.cell[id];if(c.othersCard){const og=geo[id];const n=el('g',{class:'node others',transform:`translate(${og.x},${og.y})`});n.dataset.id=id;n.appendChild(el('rect',{class:'card',width:W,height:H}));const tt=el('text',{class:'name',x:14,y:22});tt.textContent=`${c.count} other parts`;n.appendChild(tt);const ss=el('text',{class:'sub',x:14,y:42});ss.textContent='not on any flow · click to open';n.appendChild(ss);n.addEventListener('click',()=>{othersOpen.add(c.of);render()});svg.appendChild(n)}else drawNode(byId[id])}
      if(othersOpen.has(e.id)){const oc=el('text',{class:'collapse',x:g.x+g.w-34,y:g.y+23,'text-anchor':'end'});oc.textContent='hide others';oc.addEventListener('click',ev=>{ev.stopPropagation();othersOpen.delete(e.id);render()});grp.appendChild(oc)}
      return}
    const g2=el('g',{class:'node'+((flow?flowIds.includes(e.id):visible(e))?'':' dim')+(onflow?' onflow':''),transform:`translate(${g.x},${g.y})`});g2.dataset.id=e.id;
    g2.appendChild(el('rect',{class:'card',width:W,height:H}));g2.appendChild(el('rect',{class:'stripe',x:0,y:8,width:4,height:H-16,fill:colors[e.state]||colors.stable}));
    const t=el('text',{class:'name',x:14,y:22});t.textContent=(e.names[0]||e.id).slice(0,24);g2.appendChild(t);
    const fc=featCount(e),dc=decsFor(e.id).length;const sub=el('text',{class:'sub',x:14,y:41});sub.textContent=`${fc} feat · ${dc} dec`;g2.appendChild(sub);
    const ob=obsFor(e.id);if(ob){const ot=el('text',{class:ob.errors?'err':'obs',x:W-10,y:41,'text-anchor':'end'});ot.textContent=(ob.errors?`⚠ ${ob.errors} err · `:'')+`${ob.turns} turns`+(ob.ms!=null?` · ${ob.ms}ms`:'');g2.appendChild(ot)}
    if(kids.length){const pt=el('text',{class:'parts',x:W-10,y:22,'text-anchor':'end'});pt.textContent='+'+kids.length;pt.addEventListener('click',ev=>{ev.stopPropagation();open.add(e.id);render()});g2.appendChild(pt)}
    if(flow){const idx=flowIds.map((v,i)=>v===e.id?i:-1).filter(i=>i>=0);if(idx.length){const planned=idx.every(i=>/\(planned\)/i.test(flow.steps[i].note||''));const txt=idx.map(i=>i+1).join('·');const bw=Math.max(20,txt.length*7+10);g2.appendChild(el('rect',{class:'stepbg',x:W-bw-6,y:H-24,width:bw,height:18,rx:9,opacity:planned?.35:1}));const s2=el('text',{class:'step',x:W-bw/2-6,y:H-11,'text-anchor':'middle'});s2.textContent=txt;g2.appendChild(s2);if(planned)g2.classList.add('dim')}}
    g2.addEventListener('click',()=>select(e.id));svg.appendChild(g2)};
  roots.slice().sort(byOrder).forEach(drawNode);
  // edges
  const seen=new Set();const flowPairs=new Set();DATA.flows.forEach(f=>{if(flow&&f!==flow)return;const ids=f.steps.map(s=>rep(s.el));for(let i=0;i<ids.length-1;i++)flowPairs.add(ids[i]+'>'+ids[i+1])});
  const anchor=(a,b)=>{const ax=a.x+a.w/2,ay=a.y+a.h/2,bx=b.x+b.w/2,by=b.y+b.h/2;const dx=bx-ax,dy=by-ay;if(Math.abs(dx)*a.h>Math.abs(dy)*a.w)return {x:ax+Math.sign(dx)*a.w/2,y:ay};return {x:ax,y:ay+Math.sign(dy)*a.h/2}};
  const isExt=id=>{const e=byId[id];return e&&!e.part_of&&!isContainer(e)};
  for(const e of DATA.elements){for(const d0 of e.depends_on){const from=rep(e.id),to=rep(d0);if(from===to||!geo[from]||!geo[to]||seen.has(from+'>'+to))continue;seen.add(from+'>'+to);
    const A=geo[from],B=geo[to];const p1=anchor(A,B),p2=anchor(B,A);const mx=(p1.x+p2.x)/2,my=(p1.y+p2.y)/2;const horiz=Math.abs(p2.x-p1.x)>Math.abs(p2.y-p1.y);
    const d=horiz?`M${p1.x} ${p1.y} C ${mx} ${p1.y}, ${mx} ${p2.y}, ${p2.x} ${p2.y}`:`M${p1.x} ${p1.y} C ${p1.x} ${my}, ${p2.x} ${my}, ${p2.x} ${p2.y}`;
    const onFlow=flowPairs.has(from+'>'+to)||flowPairs.has(to+'>'+from);const ext=isExt(to)||isExt(from);
    const cls='edge'+(onFlow?' flow':'')+(ext&&!onFlow?' ext':'')+((onFlow||ext||allEdges)?'':' hidden')+(flow&&!onFlow?' dim':'');
    const traffic=OBS?(OBS.edges[from+'>'+to]||0)+(OBS.edges[to+'>'+from]||0):0;
    const path=el('path',{class:cls+(traffic?' obs':''),d});if(traffic)path.setAttribute('stroke-width',(1.2+Math.min(3,Math.log10(traffic+1)*1.5)).toFixed(1));path.dataset.from=from;path.dataset.to=to;path.dataset.label=(e.dep_labels[d0]||'')+(traffic?(e.dep_labels[d0]?' · ':'')+traffic+' turns':'');const tt=el('title',{});tt.textContent=`${byId[e.id].names[0]||e.id} → ${byId[d0]?.names[0]||d0}${path.dataset.label?' · '+path.dataset.label:''}`;path.appendChild(tt);edgeLayer.appendChild(path)}}
  const c=document.getElementById('canvas');c.innerHTML='';c.appendChild(svg);
  if(selected&&byId[selected])highlight(selected);else labelEdges(p=>!!flow&&p.classList.contains('flow'));
}
function labelEdges(pred){const svg=document.querySelector('#canvas svg');if(!svg)return;const ns='http://www.w3.org/2000/svg';document.querySelectorAll('.elabel,.elabelbg').forEach(n=>n.remove());document.querySelectorAll('.edge').forEach(p=>{if(!pred(p)||!p.dataset.label||p.classList.contains('hidden'))return;const len=p.getTotalLength();const m=p.getPointAtLength(len/2);const t=document.createElementNS(ns,'text');t.setAttribute('class','elabel');t.setAttribute('x',m.x);t.setAttribute('y',m.y+4);t.setAttribute('text-anchor','middle');t.textContent=p.dataset.label;svg.appendChild(t);const bb=t.getBBox();const r=document.createElementNS(ns,'rect');r.setAttribute('class','elabelbg');r.setAttribute('x',bb.x-5);r.setAttribute('y',bb.y-2);r.setAttribute('width',bb.width+10);r.setAttribute('height',bb.height+4);svg.insertBefore(r,t)})}
function highlight(id){const r=rep(id);const e=byId[id];const nb=new Set([r,...e.depends_on.map(rep),...e.used_by.map(rep),...children(id).map(k=>rep(k.id))]);
  document.querySelectorAll('.node,.box').forEach(n=>{n.classList.toggle('hi',n.dataset.id===r);if(!activeFlow&&n.classList.contains('node'))n.classList.toggle('dim',!nb.has(n.dataset.id))});
  document.querySelectorAll('.edge').forEach(p=>{const on=p.dataset.from===r||p.dataset.to===r;p.classList.toggle('hi',on);if(!activeFlow)p.classList.toggle('dim',!on)});
  labelEdges(p=>p.classList.contains('hi'))}
function clear(){selected=null;document.querySelectorAll('.node,.box,.edge').forEach(n=>n.classList.remove('hi'));if(!activeFlow)document.querySelectorAll('.node,.edge').forEach(n=>n.classList.remove('dim'));labelEdges(p=>!!activeFlow&&p.classList.contains('flow'));document.getElementById('main').classList.remove('open')}
function select(id){
  if(selected===id){clear();return}
  selected=id;const e=byId[id];highlight(id);
  const feats=e.history.filter(h=>h.feature!=null).slice().sort((a,b)=>(a.date>b.date?1:-1));const notes=e.history.filter(h=>h.feature==null);
  const feat=h=>{const f=DATA.features[h.feature];return f?` — <a href="${esc(DATA.activity+f.file)}">${esc(f.title)}</a> <span class="muted">(${esc(f.type)}, ${esc(f.phase)})</span>`:` — F${h.feature}`};
  const decs=decsFor(id);const kids=children(id).slice().sort(byOrder);const flows=DATA.flows.filter(f=>f.steps.some(s=>s.el===id));
  const rel=(d)=>`<li><a data-go="${esc(d)}">${esc(byId[d]?.names[0]||d)}</a>${e.dep_labels[d]?` <span class="muted">(${esc(e.dep_labels[d])})</span>`:''}</li>`;
  document.getElementById('panel').innerHTML=`<button class="close" id="close" title="close">×</button><h2>${esc(e.names[0]||e.id)}</h2><div class="muted"><code>${esc(e.id)}</code> · <span style="color:${colors[e.state]||'inherit'}">●</span> ${esc(e.state)}${e.part_of?` · in <a data-go="${esc(e.part_of)}">${esc(byId[e.part_of]?.names[0]||e.part_of)}</a>`:''}</div>
   ${e.state_note?`<div class="muted" style="margin-top:2px">${esc(e.state_note)}</div>`:''}
   ${e.names.length>1?`<div class="muted" style="margin-top:4px">also: ${e.names.slice(1).map(esc).join(' · ')}</div>`:''}
   <p style="margin:10px 0 0">${esc(e.purpose)}</p>
   ${kids.length?`<h3>Parts · ${kids.length}</h3><ol>${kids.map(k=>`<li><a data-go="${esc(k.id)}">${esc(k.names[0]||k.id)}</a> <span class="muted">${esc(k.state)}</span></li>`).join('')}</ol>`:''}
   ${flows.length?`<h3>On flows</h3><ul>${flows.map(f=>{const i=f.steps.findIndex(s=>s.el===id);return `<li><a data-flow="${esc(f.name)}">${esc(f.title||f.name)}</a> <span class="muted">step ${i+1} of ${f.steps.length}${f.steps[i].note?' — '+esc(f.steps[i].note):''}</span></li>`}).join('')}</ul>`:''}
   ${(()=>{const o=obsFor(id);if(!o)return OBS?'<h3>Observed</h3><div class="muted">no events mapped to this element in the window'+(e.events.length?'':' — it lists no Events: patterns')+'</div>':'';return `<h3>Observed · ${esc(OBS.window.from.slice(0,10))} → ${esc(OBS.window.to.slice(0,10))}</h3><div>${o.turns} turns${o.ms!=null?` · median ${o.ms} ms`:''}${o.errors?` · <span style="color:#d1242f;font-weight:600">${o.errors} errors</span>`:' · no errors'}</div>${e.events.length?`<div class="muted">events: ${e.events.map(esc).join(' · ')}</div>`:''}${DATA.trace_link?`<div><a href="${esc(DATA.trace_link.replace('{id}',encodeURIComponent(e.id)).replace('{events}',encodeURIComponent(e.events.join(','))))}" target="_blank">open traces</a></div>`:''}`})()}
   <h3>Code</h3><ul>${e.code.map(c=>`<li><code>${esc(c)}</code></li>`).join('')||'<li class="muted">none recorded</li>'}</ul>
   ${e.interfaces.length?`<h3>Interfaces</h3><ul>${e.interfaces.map(c=>`<li><code>${esc(c)}</code></li>`).join('')}</ul>`:''}
   <h3>Depends on</h3><ul>${e.depends_on.map(rel).join('')||'<li class="muted">nothing</li>'}</ul>
   <h3>Used by</h3><ul>${e.used_by.map(d=>`<li><a data-go="${esc(d)}">${esc(byId[d]?.names[0]||d)}</a></li>`).join('')||'<li class="muted">nothing</li>'}</ul>
   <h3>Thread · ${feats.length} feature${feats.length===1?'':'s'}</h3><ul class="timeline">${feats.map(h=>`<li><div class="d">${esc(h.date)}</div>${esc(h.text.replace(/^[^·]+·\s*/,''))}${feat(h)}</li>`).join('')||'<li class="muted">no feature has touched this yet</li>'}</ul>
   ${notes.length?`<h3>Notes</h3><ul>${notes.map(h=>`<li><span class="d">${esc(h.date)}</span> ${esc(h.text.replace(/^[^·]+·\s*/,''))}</li>`).join('')}</ul>`:''}
   <h3>Decisions · ${decs.length}</h3><ul>${decs.map(d=>`<li><span class="d">${esc(d.head)}${d.by_name?' <span title="matched by element name in the text; add an Elements: line to make it exact">≈</span>':''}</span>${d.decision?`<br>${esc(d.decision)}`:''}${d.reopen?`<br><span class="muted">reopen when: ${esc(d.reopen)}</span>`:''}</li>`).join('')||'<li class="muted">none name this element</li>'}</ul>
   ${e.sources.length?`<h3>Sources</h3><ul>${e.sources.map(s=>`<li>${esc(s)}</li>`).join('')}</ul>`:''}`;
  document.getElementById('main').classList.add('open');document.getElementById('main').classList.remove('folded');document.getElementById('handle').textContent='›';
  document.getElementById('close').addEventListener('click',clear);
  document.querySelectorAll('#panel a[data-go]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();const t=a.dataset.go;ancestors(t).forEach(x=>open.add(x));const k=byId[t];if(k&&k.part_of&&!onAnyFlowRow(t))othersOpen.add(k.part_of);render();select(t)}));
  document.querySelectorAll('#panel a[data-flow]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();document.getElementById('flow').value=a.dataset.flow;setFlow(a.dataset.flow)}));
}
function setFlow(name){activeFlow=name||null;if(activeFlow){const f=DATA.flows.find(x=>x.name===activeFlow);f.steps.forEach(s=>ancestors(s.el).forEach(x=>open.add(x)))}render();
  if(activeFlow){const f=DATA.flows.find(x=>x.name===activeFlow);document.getElementById('panel').innerHTML=`<button class="close" id="close" title="close">×</button><h2>${esc(f.title||f.name)}</h2><div class="muted"><code>${esc(f.name)}</code> · ${f.steps.length} steps</div><ol>${f.steps.map(s=>`<li${/\(planned\)/i.test(s.note||'')?' class="muted"':''}><a data-go="${esc(s.el)}">${esc(byId[s.el]?.names[0]||s.el)}</a>${s.note?` <span class="muted">— ${esc(s.note)}</span>`:''}${s.fragment?' <span class="muted" title="added from a pass fragment">≈</span>':''}</li>`).join('')}</ol>${f.sources.length?`<h3>Sources</h3><ul>${f.sources.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}`;
    document.getElementById('main').classList.add('open');document.getElementById('close').addEventListener('click',()=>{document.getElementById('flow').value='';setFlow('');clear()});
    document.querySelectorAll('#panel a[data-go]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.go)}))}}
window.filter={q:'',state:''};
const flowSel=document.getElementById('flow');const grpD=document.createElement('optgroup');grpD.label='declared';const grpO=document.createElement('optgroup');grpO.label='observed';DATA.flows.forEach(f=>{const o=document.createElement('option');o.value=f.name;o.textContent=f.title||f.name;(f.observed?grpO:grpD).appendChild(o)});flowSel.appendChild(grpD);if(grpO.children.length)flowSel.appendChild(grpO);
if(OBS){const ub=document.getElementById('unmapped');ub.style.display='';ub.textContent=`${OBS.unmapped.length} unmapped events`;ub.addEventListener('click',()=>{document.getElementById('panel').innerHTML=`<button class="close" id="close">×</button><h2>Unmapped events</h2><div class="muted">names in the observed data that no element claims in its Events: line — each is a gap in the map</div><ul>${OBS.unmapped.map(u=>`<li><code>${esc(u.name)}</code> <span class="muted">× ${u.count}</span></li>`).join('')||'<li class="muted">none — every observed event maps to an element</li>'}</ul>`;document.getElementById('main').classList.add('open');document.getElementById('main').classList.remove('folded');document.getElementById('close').addEventListener('click',clear)})}
document.getElementById('q').addEventListener('input',ev=>{window.filter.q=ev.target.value.toLowerCase();render()});
document.getElementById('state').addEventListener('change',ev=>{window.filter.state=ev.target.value;render()});
flowSel.addEventListener('change',ev=>setFlow(ev.target.value));
document.getElementById('allEdges').addEventListener('click',ev=>{allEdges=!allEdges;ev.target.classList.toggle('on',allEdges);render()});
document.getElementById('expandAll').addEventListener('click',()=>{const parents=DATA.elements.filter(isContainer);if(parents.every(p=>open.has(p.id))&&othersOpen.size){open.clear();othersOpen.clear();roots.filter(isContainer).forEach(r=>open.add(r.id))}else{parents.forEach(p=>open.add(p.id));parents.forEach(p=>othersOpen.add(p.id))}render()});
document.getElementById('reset').addEventListener('click',()=>{window.filter.q=window.filter.state='';document.getElementById('q').value='';document.getElementById('state').value='';flowSel.value='';activeFlow=null;allEdges=false;document.getElementById('allEdges').classList.remove('on');clear();render()});
// pan by dragging empty canvas; zoom with Ctrl+wheel or the buttons; the panel folds with the handle
(()=>{const c=document.getElementById('canvas');let drag=null;
 c.addEventListener('mousedown',ev=>{if(ev.button!==0)return;const t=ev.target;if(t.closest&&t.closest('.node,.box .boxtitle,.box .collapse,.edge,.elabel'))return;drag={x:ev.clientX,y:ev.clientY,sl:c.scrollLeft,st:c.scrollTop};c.classList.add('panning');ev.preventDefault()});
 window.addEventListener('mousemove',ev=>{if(!drag)return;c.scrollLeft=drag.sl-(ev.clientX-drag.x);c.scrollTop=drag.st-(ev.clientY-drag.y)});
 window.addEventListener('mouseup',()=>{drag=null;c.classList.remove('panning')});
 window.zoom=1;const applyZoom=()=>{const svg=c.querySelector('svg');if(!svg)return;if(!svg.dataset.w){svg.dataset.w=svg.getAttribute('width');svg.dataset.h=svg.getAttribute('height');svg.setAttribute('viewBox',`0 0 ${svg.dataset.w} ${svg.dataset.h}`)}svg.setAttribute('width',svg.dataset.w*window.zoom);svg.setAttribute('height',svg.dataset.h*window.zoom)};
 window.applyZoom=applyZoom;
 c.addEventListener('wheel',ev=>{if(!ev.ctrlKey)return;ev.preventDefault();window.zoom=Math.min(3,Math.max(.25,window.zoom*(ev.deltaY<0?1.1:1/1.1)));applyZoom()},{passive:false});
 document.getElementById('zin').addEventListener('click',()=>{window.zoom=Math.min(3,window.zoom*1.2);applyZoom()});
 document.getElementById('zout').addEventListener('click',()=>{window.zoom=Math.max(.25,window.zoom/1.2);applyZoom()});
 document.getElementById('zfit').addEventListener('click',()=>{const svg=c.querySelector('svg');if(!svg)return;window.zoom=Math.min(1,(c.clientWidth-24)/(svg.dataset.w||svg.getAttribute('width')));applyZoom()});
 const h=document.getElementById('handle');h.addEventListener('click',()=>{const m=document.getElementById('main');m.classList.toggle('folded');h.textContent=m.classList.contains('folded')?'‹':'›'});
})();
const _render=render;render=function(){_render();if(window.applyZoom)window.applyZoom()};
document.getElementById('meta').textContent=`${DATA.elements.length} elements · ${DATA.flows.length} flows · ${Object.keys(DATA.features).length} features · ${DATA.decisions.length} decisions`+(OBS?` · observed ${OBS.window.turns} turns, ${OBS.window.events} events`:'')+` · built ${DATA.built}`;
render();
</script></body></html>"""

def observe(path, els):
    """Read the observed-events contract (JSONL: turn, ts, name, kind, status, ms) and derive what the map shows:
    per element: turns, errors, mean ms; per edge: traffic; the most common element paths as observed flows; unmapped names."""
    import fnmatch, collections, statistics
    if not path.exists(): return None
    # a pattern is a glob on the event name; "name@tag" also requires the event's tag (any discriminator the exporter sends,
    # e.g. the agent name) to match the glob after "@"; "(unverified)" or other parenthesised notes on a pattern are ignored
    pats = []
    for e in els:
        for pat in e["events"]:
            pat = re.sub(r"\s*\(.*?\)\s*$", "", pat).strip()
            if not pat: continue
            n, _, t = pat.partition("@")
            pats.append((e["id"], n.strip(), t.strip()))
    def owner(name, tag=""):
        for eid, pn, pt in pats:
            if fnmatch.fnmatchcase(name, pn) and (not pt or fnmatch.fnmatchcase(str(tag or ""), pt)): return eid
        return None
    turns = collections.OrderedDict(); unmapped = collections.Counter(); kinds = {}
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln: continue
        try: r = json.loads(ln)
        except Exception: continue
        name = str(r.get("name", "")); tag = str(r.get("tag", "") or ""); eid = owner(name, tag)
        if not eid: unmapped[name + ("@" + tag if tag else "")] += 1
        turns.setdefault(str(r.get("turn", "")), []).append({"ts": r.get("ts", ""), "name": name, "el": eid, "kind": r.get("kind", ""), "status": str(r.get("status", "")).lower(), "ms": r.get("ms")})
        if eid and r.get("kind"): kinds[eid] = r.get("kind")
    el_stats = collections.defaultdict(lambda: {"turns": set(), "errors": 0, "ms": []}); edges = collections.Counter(); paths = collections.Counter()
    for tid, evs in turns.items():
        evs.sort(key=lambda x: str(x["ts"]))
        seq = []
        for ev in evs:
            if not ev["el"]: continue
            st = el_stats[ev["el"]]; st["turns"].add(tid)
            if ev["status"] in ("error", "failed", "fail", "exception"): st["errors"] += 1
            if isinstance(ev["ms"], (int, float)) and ev["ms"] > 0: st["ms"].append(ev["ms"])
            if not seq or seq[-1] != ev["el"]: seq.append(ev["el"])
        for a, b in zip(seq, seq[1:]): edges[a + ">" + b] += 1
        if seq: paths[" > ".join(seq)] += 1
    tss = [ev["ts"] for evs in turns.values() for ev in evs if ev["ts"]]
    # observed paths: group turns by their first four elements, keep the most common full path of each group, report the share
    total = sum(paths.values()) or 1
    groups = collections.defaultdict(collections.Counter)
    for sig, n in paths.items():
        groups[" > ".join(sig.split(" > ")[:4])][sig] += n
    ranked = sorted(groups.items(), key=lambda kv: -sum(kv[1].values()))
    flows = []
    for i, (prefix, variants) in enumerate(ranked[:6]):
        gn = sum(variants.values()); sig, _ = variants.most_common(1)[0]; share = round(100 * gn / total)
        if share < 2 and i >= 3: break
        flows.append({"name": "observed-%d" % (i + 1), "title": "observed · %d%% of turns · %d variant%s" % (share, len(variants), "" if len(variants) == 1 else "s"), "observed": True, "turns": gn,
                      "steps": [{"n": str(j + 1), "el": e, "note": ""} for j, e in enumerate(sig.split(" > "))], "fragments": [], "sources": ["observed: %d turns in this group of %d; the most common full path is shown" % (gn, len(turns))]})
    return {"window": {"from": min(tss) if tss else "", "to": max(tss) if tss else "", "turns": len(turns), "events": sum(len(v) for v in turns.values())},
            "elements": {k: {"turns": len(v["turns"]), "errors": v["errors"], "ms": round(statistics.median(v["ms"])) if v["ms"] else None, "kind": kinds.get(k, "")} for k, v in el_stats.items()},
            "edges": dict(edges), "flows": flows, "unmapped": [{"name": n, "count": c} for n, c in unmapped.most_common(50)]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    cfg = read_config()
    reg = ROOT / cfg["elements_registry"]
    if not reg.exists():
        sys.exit(f"elements registry not found: {reg}")
    els = parse_elements(reg.read_text(encoding="utf-8"))
    flows = getattr(parse_elements, "flows", [])
    board = ROOT / cfg["board_file"]
    feats = parse_board(board.read_text(encoding="utf-8")) if board.exists() else {}
    decs = []
    for key, kind in (("decisions_log", "decision"), ("deferred_decisions_log", "deferred")):
        p = ROOT / cfg[key]
        if p.exists():
            decs += parse_decisions(p.read_text(encoding="utf-8"), kind, els)
    # area from the board's feature rows when the element has none: the area of the first feature that touched it
    for e in els:
        if not e["area"]:
            for h in e["history"]:
                f = feats.get(h["feature"]) if h["feature"] is not None else None
                if f and f.get("area"): e["area"] = f["area"]; break
    # element states: in change when an open feature touched it
    open_feats = {n for n, f in feats.items() if f["section"] in ("In progress",)}
    for e in els:
        if e["state"] in ("stable", "untouched") and any(h["feature"] in open_feats for h in e["history"]):
            e["state"] = "in change"
    import datetime
    obs = observe(ROOT / cfg["observed_file"], els)
    data = {"elements": els, "flows": flows, "observed": obs, "trace_link": cfg.get("trace_link", ""), "features": feats, "decisions": decs, "activity": "../activity/",
            "built": datetime.datetime.now().strftime("%d %b %y, %I:%M %p")}
    out = Path(args.out) if args.out else (reg.parent / "map.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    page = HTML.replace("__TITLE__", html.escape(cfg["project_name"])).replace("__DATA__", json.dumps(data))
    out.write_text(page, encoding="utf-8")
    extra = f", observed {obs['window']['turns']} turns / {len(obs['unmapped'])} unmapped names" if obs else ""
    print(f"map written: {out}  ({len(els)} elements, {len(feats)} features, {len(decs)} decisions{extra})")

if __name__ == "__main__":
    main()
