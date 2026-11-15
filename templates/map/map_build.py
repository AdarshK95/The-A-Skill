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
    cfg = {"elements_registry": "docs/map/elements.md", "board_file": "docs/activity/BOARD.md",
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

def parse_elements(text):
    els = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        lines = block.splitlines()
        eid = lines[0].strip()
        if not eid or eid.startswith("<") or eid.startswith("!"):
            continue
        el = {"id": eid, "names": [], "purpose": "", "code": [], "interfaces": [], "depends_on": [],
              "used_by": [], "state": "stable", "area": "", "sources": [], "history": []}
        cur = None
        for ln in lines[1:]:
            m = re.match(r"^([A-Za-z ]+):\s*(.*)$", ln)
            if m and m.group(1).strip() in ("Names", "Purpose", "Code", "Interfaces", "Depends on", "Used by", "State", "Area", "Sources", "History"):
                key, val = m.group(1).strip(), m.group(2).strip()
                cur = key
                if key == "Names": el["names"] = [x.strip() for x in re.split(r"\s·\s|,", val) if x.strip()]
                elif key == "Purpose": el["purpose"] = val
                elif key == "Code": el["code"] = [x.strip() for x in re.split(r"\s·\s", val) if x.strip()]
                elif key == "Interfaces": el["interfaces"] = [x.strip() for x in re.split(r"\s·\s|,", val) if x.strip()]
                elif key == "Depends on": el["depends_on"] = [x.strip().strip("`") for x in re.split(r"\s·\s|,", val) if x.strip()]
                elif key == "Used by": el["used_by"] = [x.strip().strip("`") for x in re.split(r"\s·\s|,", val) if x.strip()]
                elif key == "State": el["state"] = val.lower().strip("`")
                elif key == "Area": el["area"] = val
                elif key == "Sources": el["sources"] = [x.strip() for x in re.split(r"\s·\s", val) if x.strip()]
                continue
            if cur == "History" and ln.strip().startswith("- "):
                h = ln.strip()[2:]
                parts = [x.strip() for x in h.split(" · ")]
                feat = re.search(r"\bF(\d+)\b", h)
                el["history"].append({"date": parts[0] if parts else "", "text": h, "feature": int(feat.group(1)) if feat else None})
        els.append(el)
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

def parse_decisions(text, kind):
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head = block.splitlines()[0].strip()
        m = re.search(r"^Elements:\s*(.+)$", block, re.M)
        els = [x.strip().strip("`") for x in re.split(r"\s·\s|,", m.group(1))] if m else []
        dec = re.search(r"^Decision:\s*(.+)$", block, re.M)
        reopen = re.search(r"^Reopen when:\s*(.+)$", block, re.M)
        out.append({"kind": kind, "head": head, "elements": els, "decision": dec.group(1).strip() if dec else "",
                    "reopen": reopen.group(1).strip() if reopen else ""})
    return out

HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — map</title>
<style>
:root{--bg:#fff;--fg:#1b1b1b;--muted:#666;--line:#ccc;--panel:#f6f6f6;--stable:#43a047;--inchange:#1e88e5;--planned:#9e9e9e;--unwired:#8d6e63;--superseded:#bdbdbd;--hi:#ff9800}
@media(prefers-color-scheme:dark){:root{--bg:#141414;--fg:#e8e8e8;--muted:#aaa;--line:#444;--panel:#1f1f1f}}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg);display:grid;grid-template-rows:auto 1fr;height:100vh}
header{display:flex;gap:10px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
header h1{font-size:16px;margin:0 8px 0 0}header input,header select{font:inherit;padding:4px 6px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--fg)}
.legend span{display:inline-block;margin-right:10px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:middle}
main{display:grid;grid-template-columns:1fr 360px;min-height:0}
#canvas{overflow:auto;position:relative}svg{display:block;min-width:100%}
aside{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:12px}
aside h2{font-size:15px;margin:0 0 4px}aside h3{font-size:13px;margin:14px 0 4px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
aside .muted{color:var(--muted)}aside ul{padding-left:18px;margin:4px 0}aside code{font-size:12px;background:var(--bg);padding:1px 4px;border-radius:3px}
.node{cursor:pointer}.node rect{stroke:var(--line);stroke-width:1.2;rx:6}.node text{font-size:12px;fill:#fff;pointer-events:none}
.node .badge{font-size:10px;fill:#fff;opacity:.9}.area-box{fill:none;stroke:var(--line);stroke-dasharray:4 3}.area-label{font-size:12px;fill:var(--muted)}
.edge{stroke:var(--muted);stroke-width:1.2;fill:none;marker-end:url(#arrow)}.dim{opacity:.18}.hi rect{stroke:var(--hi);stroke-width:3}
.timeline li{margin-bottom:6px}.timeline .d{color:var(--muted);font-size:12px}
button{font:inherit;padding:4px 8px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--fg);cursor:pointer}
</style></head><body>
<header><h1>__TITLE__</h1>
<input id="q" placeholder="search element, name, file…" size="28">
<select id="area"><option value="">all areas</option></select>
<select id="state"><option value="">all states</option><option>stable</option><option>in change</option><option>planned</option><option>unwired</option><option>superseded</option></select>
<button id="reset">clear</button>
<span class="legend"><span><i style="background:var(--stable)"></i>stable</span><span><i style="background:var(--inchange)"></i>in change</span><span><i style="background:var(--planned)"></i>planned</span><span><i style="background:var(--unwired)"></i>unwired</span></span>
<span class="muted" id="meta"></span></header>
<main><div id="canvas"></div><aside id="panel"><p class="muted">Click an element to pull its thread: purpose, code, relations, every feature and decision that touched it, in order. Click again to clear. Edges point from an element to what it depends on.</p></aside></main>
<script>
const DATA=__DATA__;
const colors={stable:'var(--stable)','in change':'var(--inchange)',planned:'var(--planned)',unwired:'var(--unwired)',superseded:'var(--superseded)'};
const byId=Object.fromEntries(DATA.elements.map(e=>[e.id,e]));
const touches=id=>DATA.elements.find(e=>e.id===id)?.history||[];
const decsFor=id=>DATA.decisions.filter(d=>d.elements.includes(id));
function layout(){
  const areas={};DATA.elements.forEach(e=>{(areas[e.area||'Other']=areas[e.area||'Other']||[]).push(e)});
  const W=250,H=56,GX=40,GY=22,PAD=28;let x=20;const pos={},boxes=[];
  for(const [area,list] of Object.entries(areas)){
    // rank by dependency depth inside the area: things nothing depends on go to the top
    const depth={};const dep=id=>{if(depth[id]!=null)return depth[id];depth[id]=0;const e=byId[id];if(!e)return 0;let d=0;for(const u of e.used_by){if(byId[u]&&byId[u].area===e.area)d=Math.max(d,dep(u)+1)}return depth[id]=d};
    list.forEach(e=>dep(e.id));list.sort((a,b)=>depth[a.id]-depth[b.id]||a.id.localeCompare(b.id));
    const cols=Math.max(1,Math.ceil(Math.sqrt(list.length)));let i=0,maxY=0;
    list.forEach(e=>{const c=i%cols,r=Math.floor(i/cols);pos[e.id]={x:x+PAD+c*(W+GX),y:60+PAD+r*(H+GY)};maxY=Math.max(maxY,pos[e.id].y+H);i++});
    const bw=PAD*2+cols*(W+GX)-GX;boxes.push({area,x,y:60,w:bw,h:maxY-60+PAD});x+=bw+40;
  }
  return {pos,boxes,W,H,width:x,height:Math.max(...boxes.map(b=>b.y+b.h))+40};
}
function render(filter){
  const L=layout(),ns='http://www.w3.org/2000/svg';const svg=document.createElementNS(ns,'svg');svg.setAttribute('width',L.width);svg.setAttribute('height',L.height);
  svg.innerHTML=`<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>`;
  for(const b of L.boxes){const r=document.createElementNS(ns,'rect');r.setAttribute('class','area-box');r.setAttribute('x',b.x);r.setAttribute('y',b.y);r.setAttribute('width',b.w);r.setAttribute('height',b.h);svg.appendChild(r);
    const t=document.createElementNS(ns,'text');t.setAttribute('class','area-label');t.setAttribute('x',b.x+10);t.setAttribute('y',b.y-8);t.textContent=b.area;svg.appendChild(t)}
  const visible=e=>(!filter.area||e.area===filter.area)&&(!filter.state||e.state===filter.state)&&(!filter.q||(e.id+' '+e.names.join(' ')+' '+e.code.join(' ')+' '+e.purpose).toLowerCase().includes(filter.q));
  for(const e of DATA.elements){for(const d of e.depends_on){if(!L.pos[d])continue;const a=L.pos[e.id],b=L.pos[d];const p=document.createElementNS(ns,'path');p.setAttribute('class','edge'+((visible(e)&&visible(byId[d]))?'':' dim'));
    const x1=a.x+L.W/2,y1=a.y+L.H,x2=b.x+L.W/2,y2=b.y;p.setAttribute('d',`M${x1} ${y1} C ${x1} ${(y1+y2)/2}, ${x2} ${(y1+y2)/2}, ${x2} ${y2}`);p.dataset.from=e.id;p.dataset.to=d;svg.appendChild(p)}}
  for(const e of DATA.elements){const g=document.createElementNS(ns,'g');g.setAttribute('class','node'+(visible(e)?'':' dim'));g.dataset.id=e.id;const p=L.pos[e.id];g.setAttribute('transform',`translate(${p.x},${p.y})`);
    const r=document.createElementNS(ns,'rect');r.setAttribute('width',L.W);r.setAttribute('height',L.H);r.setAttribute('fill',colors[e.state]||colors.stable);g.appendChild(r);
    const t=document.createElementNS(ns,'text');t.setAttribute('x',10);t.setAttribute('y',22);t.textContent=(e.names[0]||e.id).slice(0,34);g.appendChild(t);
    const b=document.createElementNS(ns,'text');b.setAttribute('class','badge');b.setAttribute('x',10);b.setAttribute('y',42);const dc=decsFor(e.id).length;b.textContent=`${e.history.length} feature${e.history.length===1?'':'s'} · ${dc} decision${dc===1?'':'s'} · ${e.depends_on.length}↓ ${e.used_by.length}↑`;g.appendChild(b);
    g.addEventListener('click',()=>select(e.id));svg.appendChild(g)}
  const c=document.getElementById('canvas');c.innerHTML='';c.appendChild(svg);
}
let selected=null;
function select(id){
  if(selected===id){selected=null;document.querySelectorAll('.node,.edge').forEach(n=>n.classList.remove('hi','dim'));document.getElementById('panel').innerHTML='<p class="muted">Click an element to pull its thread.</p>';return}
  selected=id;const e=byId[id];const nb=new Set([id,...e.depends_on,...e.used_by]);
  document.querySelectorAll('.node').forEach(n=>{n.classList.toggle('hi',n.dataset.id===id);n.classList.toggle('dim',!nb.has(n.dataset.id))});
  document.querySelectorAll('.edge').forEach(p=>p.classList.toggle('dim',!(p.dataset.from===id||p.dataset.to===id)));
  const feats=e.history.slice().sort((a,b)=>(a.date>b.date?1:-1));
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const feat=h=>{const f=h.feature!=null?DATA.features[h.feature]:null;return f?` — <a href="${esc(DATA.activity+f.file)}">${esc(f.title)}</a> <span class="muted">(${esc(f.type)}, ${esc(f.phase)})</span>`:''};
  const decs=decsFor(id);
  document.getElementById('panel').innerHTML=`<h2>${esc(e.names[0]||e.id)}</h2><div class="muted"><code>${esc(e.id)}</code> · ${esc(e.state)} · ${esc(e.area||'')}</div>
   ${e.names.length>1?`<div class="muted">also called: ${e.names.slice(1).map(esc).join(' · ')}</div>`:''}
   <p>${esc(e.purpose)}</p>
   <h3>Code</h3><ul>${e.code.map(c=>`<li><code>${esc(c)}</code></li>`).join('')||'<li class="muted">none recorded</li>'}</ul>
   ${e.interfaces.length?`<h3>Interfaces</h3><ul>${e.interfaces.map(c=>`<li><code>${esc(c)}</code></li>`).join('')}</ul>`:''}
   <h3>Depends on</h3><ul>${e.depends_on.map(d=>`<li><a href="#" data-go="${esc(d)}">${esc(byId[d]?.names[0]||d)}</a></li>`).join('')||'<li class="muted">nothing</li>'}</ul>
   <h3>Used by</h3><ul>${e.used_by.map(d=>`<li><a href="#" data-go="${esc(d)}">${esc(byId[d]?.names[0]||d)}</a></li>`).join('')||'<li class="muted">nothing</li>'}</ul>
   <h3>Thread — ${feats.length} feature${feats.length===1?'':'s'}</h3><ul class="timeline">${feats.map(h=>`<li><div class="d">${esc(h.date)}</div>${esc(h.text.replace(/^[^·]+·\s*/,''))}${feat(h)}</li>`).join('')||'<li class="muted">no feature has touched this yet</li>'}</ul>
   <h3>Decisions — ${decs.length}</h3><ul>${decs.map(d=>`<li><span class="d">${esc(d.head)}</span>${d.decision?`<br>${esc(d.decision)}`:''}${d.reopen?`<br><span class="muted">reopen when: ${esc(d.reopen)}</span>`:''}</li>`).join('')||'<li class="muted">none name this element</li>'}</ul>
   ${e.sources.length?`<h3>Sources</h3><ul>${e.sources.map(s=>`<li>${esc(s)}</li>`).join('')}</ul>`:''}`;
  document.querySelectorAll('#panel a[data-go]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.go)}));
}
const filter={q:'',area:'',state:''};
const areaSel=document.getElementById('area');[...new Set(DATA.elements.map(e=>e.area||'Other'))].forEach(a=>{const o=document.createElement('option');o.textContent=a;areaSel.appendChild(o)});
document.getElementById('q').addEventListener('input',ev=>{filter.q=ev.target.value.toLowerCase();render(filter)});
areaSel.addEventListener('change',ev=>{filter.area=ev.target.value;render(filter)});
document.getElementById('state').addEventListener('change',ev=>{filter.state=ev.target.value;render(filter)});
document.getElementById('reset').addEventListener('click',()=>{filter.q=filter.area=filter.state='';document.getElementById('q').value='';areaSel.value='';document.getElementById('state').value='';selected=null;render(filter);document.getElementById('panel').innerHTML='<p class="muted">Click an element to pull its thread.</p>'});
document.getElementById('meta').textContent=`${DATA.elements.length} elements · ${Object.keys(DATA.features).length} features · built ${DATA.built}`;
render(filter);
</script></body></html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    cfg = read_config()
    reg = ROOT / cfg["elements_registry"]
    if not reg.exists():
        sys.exit(f"elements registry not found: {reg}")
    els = parse_elements(reg.read_text(encoding="utf-8"))
    board = ROOT / cfg["board_file"]
    feats = parse_board(board.read_text(encoding="utf-8")) if board.exists() else {}
    decs = []
    for key, kind in (("decisions_log", "decision"), ("deferred_decisions_log", "deferred")):
        p = ROOT / cfg[key]
        if p.exists():
            decs += parse_decisions(p.read_text(encoding="utf-8"), kind)
    # area from the board's feature rows when the element has none: the area of the first feature that touched it
    for e in els:
        if not e["area"]:
            for h in e["history"]:
                f = feats.get(h["feature"]) if h["feature"] is not None else None
                if f and f.get("area"): e["area"] = f["area"]; break
    # element states: in change when an open feature touched it
    open_feats = {n for n, f in feats.items() if f["section"] in ("In progress",)}
    for e in els:
        if e["state"] == "stable" and any(h["feature"] in open_feats for h in e["history"]):
            e["state"] = "in change"
    import datetime
    data = {"elements": els, "features": feats, "decisions": decs, "activity": "../activity/",
            "built": datetime.datetime.now().strftime("%d %b %y, %I:%M %p")}
    out = Path(args.out) if args.out else (reg.parent / "map.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    page = HTML.replace("__TITLE__", html.escape(cfg["project_name"])).replace("__DATA__", json.dumps(data))
    out.write_text(page, encoding="utf-8")
    print(f"map written: {out}  ({len(els)} elements, {len(feats)} features, {len(decs)} decisions)")

if __name__ == "__main__":
    main()
