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

def parse_decisions(text, kind, elements=None):
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head = block.splitlines()[0].strip()
        m = re.search(r"^Elements:\s*(.+)$", block, re.M)
        els = [x.strip().strip("`") for x in re.split(r"\s·\s|,", m.group(1))] if m else []
        if not els and elements:  # older entries without an Elements field: match an element's id or any of its names in the text
            low = block.lower()
            els = [e["id"] for e in elements if e["id"].lower() in low or any(n.lower() in low for n in e["names"] if len(n) > 4)]
        dec = re.search(r"^Decision:\s*(.+)$", block, re.M)
        reopen = re.search(r"^Reopen when:\s*(.+)$", block, re.M)
        out.append({"kind": kind, "head": head, "elements": els, "decision": dec.group(1).strip() if dec else "",
                    "reopen": reopen.group(1).strip() if reopen else ""})
    return out

HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — map</title>
<style>
:root{--bg:#fafafa;--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--card:#fff;--panel:#f6f8fa;--hi:#d97706;
 --stable:#1a7f37;--inchange:#0969da;--planned:#6e7781;--unwired:#9a6700;--untouched:#8250df;--superseded:#afb8c1}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#8b949e;--line:#30363d;--card:#161b22;--panel:#161b22;
 --stable:#3fb950;--inchange:#58a6ff;--planned:#8b949e;--unwired:#d29922;--untouched:#bc8cff;--superseded:#6e7681}}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;font:13px/1.45 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);display:grid;grid-template-rows:auto 1fr auto}
header{display:flex;gap:8px;align-items:center;padding:8px 14px;border-bottom:1px solid var(--line);flex-wrap:wrap;background:var(--card)}
header h1{font-size:15px;font-weight:600;margin:0 10px 0 0}header input,header select,header button{font:inherit;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
header button{cursor:pointer}.legend{margin-left:auto;display:flex;gap:12px;color:var(--muted);font-size:12px}.legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
main{display:grid;grid-template-columns:1fr 0;min-height:0;transition:grid-template-columns .2s}main.open{grid-template-columns:1fr 380px}
#canvas{overflow:auto;position:relative;padding:8px}svg{display:block}
aside{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:14px 16px;display:none}main.open aside{display:block}
aside h2{font-size:16px;margin:0 0 2px;font-weight:600}aside h3{font-size:11px;margin:16px 0 4px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
aside .muted{color:var(--muted)}aside ul{padding-left:16px;margin:4px 0}aside li{margin:2px 0}aside code{font-size:12px;background:var(--bg);padding:1px 5px;border-radius:4px;border:1px solid var(--line)}
aside a{color:var(--inchange);text-decoration:none}aside a:hover{text-decoration:underline}
.close{float:right;background:none;border:0;color:var(--muted);font-size:18px;cursor:pointer;line-height:1}
.node{cursor:pointer}.node .card{fill:var(--card);stroke:var(--line);rx:8}.node .stripe{rx:2}.node .name{font-size:12.5px;font-weight:600;fill:var(--fg)}.node .sub{font-size:11px;fill:var(--muted)}
.node:hover .card{stroke:var(--fg)}.hi .card{stroke:var(--hi);stroke-width:2}.dim{opacity:.22}
.area-box{fill:none;stroke:var(--line);stroke-dasharray:3 4;rx:10}.area-label{font-size:11px;fill:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.edge{stroke:var(--muted);stroke-width:1.1;fill:none;opacity:.55;marker-end:url(#arrow)}.edge.hi{stroke:var(--hi);opacity:1;stroke-width:1.6}
footer{padding:4px 14px;border-top:1px solid var(--line);color:var(--muted);font-size:11px;background:var(--card)}
.timeline li{margin-bottom:8px}.timeline .d{color:var(--muted);font-size:11px}
</style></head><body>
<header><h1>__TITLE__</h1>
<input id="q" placeholder="search" size="22"><select id="area"><option value="">all areas</option></select>
<select id="state"><option value="">all states</option><option>stable</option><option>in change</option><option>planned</option><option>unwired</option><option>untouched</option><option>superseded</option></select>
<button id="reset">clear</button>
<span class="legend"><span><i style="background:var(--stable)"></i>stable</span><span><i style="background:var(--inchange)"></i>in change</span><span><i style="background:var(--planned)"></i>planned</span><span><i style="background:var(--unwired)"></i>unwired</span><span><i style="background:var(--untouched)"></i>untouched</span></span></header>
<main id="main"><div id="canvas"></div><aside id="panel"></aside></main>
<footer><span id="meta"></span> · arrow = depends on · click an element for its thread</footer>
<script>
const DATA=__DATA__;
const colors={stable:'var(--stable)','in change':'var(--inchange)',planned:'var(--planned)',unwired:'var(--unwired)',untouched:'var(--untouched)',superseded:'var(--superseded)'};
const byId=Object.fromEntries(DATA.elements.map(e=>[e.id,e]));
const featCount=e=>e.history.filter(h=>h.feature!=null).length;
const decsFor=id=>DATA.decisions.filter(d=>d.elements.includes(id));
const W=230,H=58,GX=36,GY=46,PAD=26,AREAGAP=36,TOP=56;
function layout(){
  // level = 1 + max(level of dependencies); dependencies sit lower. Computed over all elements, then grouped by area.
  const lvl={};const L=id=>{if(lvl[id]!=null)return lvl[id];lvl[id]=0;const e=byId[id];if(!e)return 0;let d=0;for(const dep of e.depends_on){if(byId[dep])d=Math.max(d,L(dep)+1)}return lvl[id]=d};
  DATA.elements.forEach(e=>L(e.id));const maxL=Math.max(0,...Object.values(lvl));
  const areas={};DATA.elements.forEach(e=>{(areas[e.area||'Other']=areas[e.area||'Other']||[]).push(e)});
  const pos={},boxes=[];let x=16;
  for(const [area,list] of Object.entries(areas)){
    // rows by level (top = depends on most things), columns ordered by barycenter of neighbours to cut crossings
    const rows={};list.forEach(e=>{(rows[lvl[e.id]]=rows[lvl[e.id]]||[]).push(e)});
    const order=Object.keys(rows).map(Number).sort((a,b)=>b-a);let cols=1;
    const colIdx={};
    order.forEach((lv,ri)=>{const row=rows[lv];const bary=e=>{const nb=[...e.depends_on,...e.used_by].map(n=>colIdx[n]).filter(v=>v!=null);return nb.length?nb.reduce((a,b)=>a+b,0)/nb.length:0};
      row.sort((a,b)=>bary(a)-bary(b)||a.id.localeCompare(b.id));row.forEach((e,ci)=>{colIdx[e.id]=ci});cols=Math.max(cols,row.length)});
    order.forEach((lv,ri)=>{const row=rows[lv];const offset=(cols-row.length)*(W+GX)/2;row.forEach((e,ci)=>{pos[e.id]={x:x+PAD+offset+ci*(W+GX),y:TOP+PAD+ri*(H+GY)}})});
    const bw=PAD*2+cols*(W+GX)-GX,bh=PAD*2+order.length*(H+GY)-GY;boxes.push({area,x,y:TOP,w:bw,h:bh});x+=bw+AREAGAP;
  }
  return {pos,boxes,width:x+8,height:TOP+Math.max(...boxes.map(b=>b.h))+30};
}
function render(filter){
  const Lo=layout(),ns='http://www.w3.org/2000/svg';const svg=document.createElementNS(ns,'svg');svg.setAttribute('width',Lo.width);svg.setAttribute('height',Lo.height);
  svg.innerHTML=`<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L9 5L0 9z" fill="var(--muted)"/></marker></defs>`;
  const el=(t,a)=>{const n=document.createElementNS(ns,t);for(const k in a)n.setAttribute(k,a[k]);return n};
  for(const b of Lo.boxes){svg.appendChild(el('rect',{class:'area-box',x:b.x,y:b.y,width:b.w,height:b.h}));const t=el('text',{class:'area-label',x:b.x+12,y:b.y-10});t.textContent=b.area;svg.appendChild(t)}
  const visible=e=>(!filter.area||(e.area||'Other')===filter.area)&&(!filter.state||e.state===filter.state)&&(!filter.q||(e.id+' '+e.names.join(' ')+' '+e.code.join(' ')+' '+e.purpose).toLowerCase().includes(filter.q));
  for(const e of DATA.elements){for(const d of e.depends_on){if(!Lo.pos[d])continue;const a=Lo.pos[e.id],b=Lo.pos[d];const x1=a.x+W/2,y1=a.y+H,x2=b.x+W/2,y2=b.y;const my=y1+(y2-y1)/2;
    const p=el('path',{class:'edge'+((visible(e)&&visible(byId[d]))?'':' dim'),d:y2>y1?`M${x1} ${y1} C ${x1} ${my}, ${x2} ${my}, ${x2} ${y2}`:`M${x1} ${a.y} C ${x1} ${a.y-40}, ${x2} ${b.y+H+40}, ${x2} ${b.y+H}`});p.dataset.from=e.id;p.dataset.to=d;svg.appendChild(p)}}
  for(const e of DATA.elements){const g=el('g',{class:'node'+(visible(e)?'':' dim'),transform:`translate(${Lo.pos[e.id].x},${Lo.pos[e.id].y})`});g.dataset.id=e.id;
    g.appendChild(el('rect',{class:'card',width:W,height:H}));g.appendChild(el('rect',{class:'stripe',x:0,y:8,width:4,height:H-16,fill:colors[e.state]||colors.stable}));
    const t=el('text',{class:'name',x:14,y:23});t.textContent=(e.names[0]||e.id).slice(0,30);g.appendChild(t);
    const fc=featCount(e),dc=decsFor(e.id).length;const s=el('text',{class:'sub',x:14,y:43});s.textContent=`${fc} feature${fc===1?'':'s'} · ${dc} decision${dc===1?'':'s'} · ${e.depends_on.length}↓ ${e.used_by.length}↑`;g.appendChild(s);
    g.addEventListener('click',()=>select(e.id));svg.appendChild(g)}
  const c=document.getElementById('canvas');c.innerHTML='';c.appendChild(svg);
}
let selected=null;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function clear(){selected=null;document.querySelectorAll('.node,.edge').forEach(n=>n.classList.remove('hi','dim'));document.getElementById('main').classList.remove('open')}
function select(id){
  if(selected===id){clear();return}
  selected=id;const e=byId[id];const nb=new Set([id,...e.depends_on,...e.used_by]);
  document.querySelectorAll('.node').forEach(n=>{n.classList.toggle('hi',n.dataset.id===id);n.classList.toggle('dim',!nb.has(n.dataset.id))});
  document.querySelectorAll('.edge').forEach(p=>{const on=p.dataset.from===id||p.dataset.to===id;p.classList.toggle('hi',on);p.classList.toggle('dim',!on)});
  const feats=e.history.filter(h=>h.feature!=null).slice().sort((a,b)=>(a.date>b.date?1:-1));const notes=e.history.filter(h=>h.feature==null);
  const feat=h=>{const f=DATA.features[h.feature];return f?` — <a href="${esc(DATA.activity+f.file)}">${esc(f.title)}</a> <span class="muted">(${esc(f.type)}, ${esc(f.phase)})</span>`:` — F${h.feature}`};
  const decs=decsFor(id);
  document.getElementById('panel').innerHTML=`<button class="close" id="close" title="close">×</button><h2>${esc(e.names[0]||e.id)}</h2><div class="muted"><code>${esc(e.id)}</code> · <span style="color:${colors[e.state]||'inherit'}">●</span> ${esc(e.state)} · ${esc(e.area||'')}</div>
   ${e.names.length>1?`<div class="muted" style="margin-top:4px">also: ${e.names.slice(1).map(esc).join(' · ')}</div>`:''}
   <p style="margin:10px 0 0">${esc(e.purpose)}</p>
   <h3>Code</h3><ul>${e.code.map(c=>`<li><code>${esc(c)}</code></li>`).join('')||'<li class="muted">none recorded</li>'}</ul>
   ${e.interfaces.length?`<h3>Interfaces</h3><ul>${e.interfaces.map(c=>`<li><code>${esc(c)}</code></li>`).join('')}</ul>`:''}
   <h3>Depends on</h3><ul>${e.depends_on.map(d=>`<li><a href="#" data-go="${esc(d)}">${esc(byId[d]?.names[0]||d)}</a></li>`).join('')||'<li class="muted">nothing</li>'}</ul>
   <h3>Used by</h3><ul>${e.used_by.map(d=>`<li><a href="#" data-go="${esc(d)}">${esc(byId[d]?.names[0]||d)}</a></li>`).join('')||'<li class="muted">nothing</li>'}</ul>
   <h3>Thread · ${feats.length} feature${feats.length===1?'':'s'}</h3><ul class="timeline">${feats.map(h=>`<li><div class="d">${esc(h.date)}</div>${esc(h.text.replace(/^[^·]+·\s*/,''))}${feat(h)}</li>`).join('')||'<li class="muted">no feature has touched this yet</li>'}</ul>
   ${notes.length?`<h3>Notes</h3><ul>${notes.map(h=>`<li><span class="d">${esc(h.date)}</span> ${esc(h.text.replace(/^[^·]+·\s*/,''))}</li>`).join('')}</ul>`:''}
   <h3>Decisions · ${decs.length}</h3><ul>${decs.map(d=>`<li><span class="d">${esc(d.head)}</span>${d.decision?`<br>${esc(d.decision)}`:''}${d.reopen?`<br><span class="muted">reopen when: ${esc(d.reopen)}</span>`:''}</li>`).join('')||'<li class="muted">none name this element</li>'}</ul>
   ${e.sources.length?`<h3>Sources</h3><ul>${e.sources.map(s=>`<li>${esc(s)}</li>`).join('')}</ul>`:''}`;
  document.getElementById('main').classList.add('open');
  document.getElementById('close').addEventListener('click',clear);
  document.querySelectorAll('#panel a[data-go]').forEach(a=>a.addEventListener('click',ev=>{ev.preventDefault();select(a.dataset.go)}));
}
const filter={q:'',area:'',state:''};
const areaSel=document.getElementById('area');[...new Set(DATA.elements.map(e=>e.area||'Other'))].forEach(a=>{const o=document.createElement('option');o.textContent=a;areaSel.appendChild(o)});
document.getElementById('q').addEventListener('input',ev=>{filter.q=ev.target.value.toLowerCase();render(filter)});
areaSel.addEventListener('change',ev=>{filter.area=ev.target.value;render(filter)});
document.getElementById('state').addEventListener('change',ev=>{filter.state=ev.target.value;render(filter)});
document.getElementById('reset').addEventListener('click',()=>{filter.q=filter.area=filter.state='';document.getElementById('q').value='';areaSel.value='';document.getElementById('state').value='';clear();render(filter)});
document.getElementById('meta').textContent=`${DATA.elements.length} elements · ${Object.keys(DATA.features).length} features · ${DATA.decisions.length} decisions · built ${DATA.built}`;
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
    data = {"elements": els, "features": feats, "decisions": decs, "activity": "../activity/",
            "built": datetime.datetime.now().strftime("%d %b %y, %I:%M %p")}
    out = Path(args.out) if args.out else (reg.parent / "map.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    page = HTML.replace("__TITLE__", html.escape(cfg["project_name"])).replace("__DATA__", json.dumps(data))
    out.write_text(page, encoding="utf-8")
    print(f"map written: {out}  ({len(els)} elements, {len(feats)} features, {len(decs)} decisions)")

if __name__ == "__main__":
    main()
