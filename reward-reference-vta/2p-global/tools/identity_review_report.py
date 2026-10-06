from pathlib import Path
import html
import json
import math
import numpy as np
import pandas as pd


def _j(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return None if not np.isfinite(v) else float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, float) and not math.isfinite(v):
        return None
    try:
        if pd.isna(v):
            return None
    except Exception:
        pass
    return v


def build_identity_review_pages(root, out, css=""):
    root = Path(root)
    out = Path(out)
    cards = []
    for candp in root.glob("sessions/*/stage_08/identity_candidates.csv"):
        sid = candp.parts[-3]
        if candp.stat().st_size == 0:
            continue
        try:
            c = pd.read_csv(candp)
        except pd.errors.EmptyDataError:
            continue
        if not len(c):
            continue
        aliases = {
            "src_session": "source_session",
            "src_roi": "source_roi",
            "tgt_session": "target_session",
            "tgt_roi": "target_roi",
        }
        for old, new in aliases.items():
            if new not in c.columns and old in c.columns:
                c = c.rename(columns={old: new})
        need = ["candidate_id", "source_session", "source_roi", "target_session", "target_roi"]
        if any(x not in c.columns for x in need):
            continue
        rd = out / "identity-review" / sid
        rd.mkdir(parents=True, exist_ok=True)
        rows = []
        for _, r in c.iterrows():
            rec = {k: _j(v) for k, v in r.to_dict().items()}
            rec["source_img"] = f"../../sessions/{r.source_session}/assets/roi_{int(r.source_roi)}_mask.png"
            rec["target_img"] = f"../../sessions/{r.target_session}/assets/roi_{int(r.target_roi)}_mask.png"
            rows.append(rec)
        payload = json.dumps(rows, separators=(",", ":"))
        (rd / "candidates.js").write_text(
            "window.CARMA_IDENTITY_CANDIDATES=" + payload + ";", encoding="utf-8"
        )
        key = "carma_identity_review_" + sid
        js = r"""
const C=window.CARMA_IDENTITY_CANDIDATES||[];let i=0;
const KEY=document.body.dataset.key;let D=JSON.parse(localStorage.getItem(KEY)||'{}');
const f=(v,d=3)=>v==null||Number.isNaN(+v)?'-':typeof v==='number'?v.toFixed(d):String(v);
function show(){
  if(!C.length)return;
  const c=C[i];
  document.getElementById('pos').textContent=(i+1)+' / '+C.length+' | '+c.candidate_id;
  document.getElementById('src').src=c.source_img;document.getElementById('tgt').src=c.target_img;
  document.getElementById('srcLab').textContent=c.source_session+' ROI '+c.source_roi;
  document.getElementById('tgtLab').textContent=c.target_session+' ROI '+c.target_roi;
  const ks=['distance_px','reciprocal_nearest','area_ratio','local_corr','source_morphology_pass','target_morphology_pass','review_status'];
  document.getElementById('metrics').innerHTML=ks.map(k=>'<tr><th>'+k+'</th><td>'+f(c[k],4)+'</td></tr>').join('');
  document.getElementById('decision').textContent=D[c.candidate_id]||'UNREVIEWED';
}
function setd(v){D[C[i].candidate_id]=v;localStorage.setItem(KEY,JSON.stringify(D));show()}
function nav(d){i=Math.max(0,Math.min(C.length-1,i+d));show()}
function exp(){
  const reviewer=document.getElementById('reviewer').value.trim();
  if(!reviewer){alert('Enter reviewer');return}
  const out={reviewer,timestamp:new Date().toISOString(),decisions:C.map(c=>({candidate_id:c.candidate_id,decision:D[c.candidate_id]||'UNREVIEWED'}))};
  const b=new Blob([JSON.stringify(out,null,2)],{type:'application/json'}),a=document.createElement('a');
  a.href=URL.createObjectURL(b);a.download=C[0].source_session+'_identity_review_'+reviewer+'.json';a.click();
}
show();
"""
        page = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(sid)} identity review</title><style>{css}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;background:#f6f8fb;color:#172033;margin:0}}
.wrap{{max-width:1100px;margin:auto;padding:28px}}.card{{background:#fff;border:1px solid #dfe5ee;border-radius:14px;padding:16px;margin-top:18px}}
.reviewpair{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.reviewpair img{{display:block;width:100%;max-width:360px;aspect-ratio:1/1;object-fit:contain;background:#0b1018;border-radius:10px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}table{{border-collapse:collapse;width:100%}}th,td{{padding:7px 9px;border-bottom:1px solid #e3e8ef;text-align:left}}
button,input{{font:inherit;padding:8px 10px;margin:4px}}@media(max-width:760px){{.reviewpair,.grid2{{grid-template-columns:1fr}}}}
</style></head><body data-key='{html.escape(key)}'><div class='wrap'><a href='../../index.html'>&lt;- dataset</a><h1>Stage08 independent identity review</h1><p>{html.escape(sid)}. Automatic matches are candidates only; two reviewers export decisions independently, then CLI consensus freezes accepted edges.</p>
<div class='card'><label>Reviewer <input id='reviewer'></label><button onclick='exp()'>Export decisions JSON</button></div>
<div class='card'><h2 id='pos'></h2><div class='reviewpair'><div><b id='srcLab'></b><img id='src'></div><div><b id='tgtLab'></b><img id='tgt'></div></div>
<div class='grid2'><div><table><tbody id='metrics'></tbody></table></div><div><button onclick="setd('ACCEPT')">Accept</button><button onclick="setd('REJECT')">Reject</button><button onclick="setd('UNCERTAIN')">Uncertain</button><p>Current: <b id='decision'></b></p><button onclick='nav(-1)'>&lt;- Previous</button><button onclick='nav(1)'>Next -&gt;</button></div></div></div></div>
<script src='candidates.js'></script><script>{js}</script></body></html>"""
        (rd / "index.html").write_text(page, encoding="utf-8")
        cards.append(
            {
                "session_id": sid,
                "n_candidates": len(rows),
                "href": f"identity-review/{sid}/index.html",
            }
        )
    return cards
