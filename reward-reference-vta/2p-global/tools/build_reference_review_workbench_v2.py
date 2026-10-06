from pathlib import Path
import argparse, json, re
import pandas as pd

def js_safe(s):
    return json.dumps(str(s),ensure_ascii=False)

def build(bundle_root, animal_label=None, storage_key=None):
    root=Path(bundle_root).resolve()
    cp=root/"identity_review_candidates.csv"
    if not cp.exists():
        raise SystemExit(f"Missing {cp}")
    c=pd.read_csv(cp)
    aliases={"source_session":"src_session","source_roi":"src_roi","target_session":"tgt_session","target_roi":"tgt_roi"}
    for canon,ref in aliases.items():
        if ref not in c.columns and canon in c.columns:
            c=c.rename(columns={canon:ref})
    need=["candidate_id","src_session","src_roi","tgt_session","tgt_roi"]
    miss=[x for x in need if x not in c.columns]
    if miss:
        raise SystemExit("Missing candidate columns: "+",".join(miss))
    label=animal_label or root.name.split("_")[0]
    key=storage_key or re.sub(r"[^a-z0-9]+","_",label.lower())+"_identity_review"
    rows=[]
    for _,r in c.iterrows():
        rec={k:(None if pd.isna(v) else (float(v) if isinstance(v,float) else int(v) if isinstance(v,int) else str(v))) for k,v in r.to_dict().items()}
        rec["pair"]=f"{r.src_session} → {r.tgt_session}"
        rows.append(rec)
    review=root/"identity_review"; review.mkdir(parents=True,exist_ok=True)
    (review/"identity_review_data.js").write_text("window.CARMA_IDENTITY_CANDIDATES="+json.dumps(rows,separators=(",",":"),ensure_ascii=False)+";",encoding="utf-8")

    js=r'''const ALL=window.CARMA_IDENTITY_CANDIDATES||[];
let V=ALL.slice(),i=0;
const KEY=document.body.dataset.key;
let D=JSON.parse(localStorage.getItem(KEY)||'{}');
const $=id=>document.getElementById(id);
const f=(v,d=3)=>v==null?'—':typeof v==='number'?(Number.isFinite(v)?v.toFixed(d):'—'):String(v);
function reviewed(){return Object.values(D).filter(x=>['ACCEPT','REJECT','UNCERTAIN'].includes(x)).length}
function pairs(){return [...new Set(ALL.map(x=>x.pair))].sort()}
function grades(){return [...new Set(ALL.map(x=>x.source_grade||'').filter(Boolean))].sort()}
function authorities(){return [...new Set(ALL.map(x=>x.authority||'').filter(Boolean))].sort()}
function initFilters(){
  $('pair').innerHTML='<option value="">All session pairs</option>'+pairs().map(x=>'<option>'+x+'</option>').join('');
  $('grade').innerHTML='<option value="">All grades</option>'+grades().map(x=>'<option>'+x+'</option>').join('');
  $('authority').innerHTML='<option value="">All authorities</option>'+authorities().map(x=>'<option>'+x+'</option>').join('');
}
function decision(c){return D[c.candidate_id]||'UNREVIEWED'}
function apply(){
  const pair=$('pair').value,grade=$('grade').value,auth=$('authority').value,state=$('state').value,sort=$('sort').value;
  V=ALL.filter(c=>(!pair||c.pair===pair)&&(!grade||(c.source_grade||'')===grade)&&(!auth||(c.authority||'')===auth)&&(!state||(state==='UNREVIEWED'?decision(c)==='UNREVIEWED':decision(c)!=='UNREVIEWED')));
  if(sort==='corr') V.sort((a,b)=>(Number(b.local_corr)||-9)-(Number(a.local_corr)||-9));
  if(sort==='distance') V.sort((a,b)=>(Number(a.distance_px)||999)-(Number(b.distance_px)||999));
  if(sort==='area') V.sort((a,b)=>Math.abs(Math.log(Number(a.area_ratio)||999))-Math.abs(Math.log(Number(b.area_ratio)||999)));
  i=0; show();
}
function imgPath(c,side){
  const sid=side==='src'?c.src_session:c.tgt_session,rid=side==='src'?c.src_roi:c.tgt_roi;
  return '../sessions/'+sid+'/roi/'+rid+'_mask.png';
}
function show(){
  $('globalProgress').textContent=reviewed()+' / '+ALL.length+' reviewed';
  $('visibleCount').textContent=V.length+' visible';
  if(!V.length){$('app').innerHTML="<div class='card'><h2>No candidates match the current filters.</h2></div>";return}
  i=Math.max(0,Math.min(i,V.length-1)); const c=V[i],dec=decision(c);
  let h="<div class='card'><div class='review-head'><div><div class='small'>"+(i+1)+" / "+V.length+" visible · "+reviewed()+" / "+ALL.length+" reviewed</div><h2>"+c.candidate_id+"</h2><div class='small'>"+c.pair+"</div></div><div class='decision-chip "+dec+"'>"+dec+"</div></div>";
  h+="<div class='reviewpair'><div><b>"+c.src_session+" ROI "+c.src_roi+"</b><br><img src='"+imgPath(c,'src')+"'></div><div><b>"+c.tgt_session+" ROI "+c.tgt_roi+"</b><br><img src='"+imgPath(c,'tgt')+"'></div></div>";
  const metrics=[['plane',c.plane],['distance_px',c.distance_px],['local_corr',c.local_corr],['area_ratio',c.area_ratio],['source_grade',c.source_grade],['authority',c.authority],['source_status',c.review_status]];
  h+="<div class='review-bottom'><table><tbody>"+metrics.map(x=>"<tr><th>"+x[0]+"</th><td>"+f(x[1],4)+"</td></tr>").join('')+"</tbody></table>";
  h+="<div class='decision-panel'><div class='buttons'><button onclick=\"setd('ACCEPT')\">1 · Accept</button><button onclick=\"setd('REJECT')\">2 · Reject</button><button onclick=\"setd('UNCERTAIN')\">3 · Uncertain</button><button onclick=\"clearDecision()\">Clear</button></div><div class='navbuttons'><button onclick='nav(-1)'>← Previous</button><button onclick='nextUnreviewed()'>Next unreviewed</button><button onclick='nav(1)'>Next →</button></div><p class='small'>Keyboard: ←/→ navigate · 1 Accept · 2 Reject · 3 Uncertain · 0 Clear</p></div></div></div>";
  $('app').innerHTML=h;
}
function setd(v){if(!V.length)return;D[V[i].candidate_id]=v;localStorage.setItem(KEY,JSON.stringify(D));show()}
function clearDecision(){if(!V.length)return;delete D[V[i].candidate_id];localStorage.setItem(KEY,JSON.stringify(D));show()}
function nav(d){if(!V.length)return;i=Math.max(0,Math.min(V.length-1,i+d));show()}
function nextUnreviewed(){
  if(!V.length)return;
  for(let k=1;k<=V.length;k++){let j=(i+k)%V.length;if(decision(V[j])==='UNREVIEWED'){i=j;show();return}}
}
function exp(){
  const reviewer=$('reviewer').value.trim(); if(!reviewer){alert('Enter reviewer');return}
  const out={reviewer,timestamp:new Date().toISOString(),bundle:document.body.dataset.bundle,decisions:ALL.map(c=>({candidate_id:c.candidate_id,decision:D[c.candidate_id]||'UNREVIEWED'}))};
  const b=new Blob([JSON.stringify(out,null,2)],{type:'application/json'}),a=document.createElement('a');
  a.href=URL.createObjectURL(b);a.download=document.body.dataset.bundle+'_identity_review_'+reviewer+'.json';a.click();
}
function importReview(input){
  const file=input.files&&input.files[0];if(!file)return;
  file.text().then(t=>{const x=JSON.parse(t);if(!Array.isArray(x.decisions))throw new Error('decisions[] missing');const valid=new Set(ALL.map(c=>c.candidate_id));for(const q of x.decisions){if(valid.has(String(q.candidate_id))&&['ACCEPT','REJECT','UNCERTAIN','UNREVIEWED'].includes(String(q.decision).toUpperCase())){if(String(q.decision).toUpperCase()==='UNREVIEWED')delete D[String(q.candidate_id)];else D[String(q.candidate_id)]=String(q.decision).toUpperCase()}}localStorage.setItem(KEY,JSON.stringify(D));if(x.reviewer)$('reviewer').value=x.reviewer;apply()}).catch(e=>alert('Could not import review: '+e.message));
}
document.addEventListener('keydown',e=>{
  if(['INPUT','SELECT'].includes(document.activeElement.tagName))return;
  if(e.key==='ArrowLeft')nav(-1); else if(e.key==='ArrowRight')nav(1); else if(e.key==='1')setd('ACCEPT'); else if(e.key==='2')setd('REJECT'); else if(e.key==='3')setd('UNCERTAIN'); else if(e.key==='0')clearDecision();
});
initFilters();['pair','grade','authority','state','sort'].forEach(x=>$(x).addEventListener('change',apply));apply();
'''
    (review/"review.js").write_text(js,encoding="utf-8")
    page=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{label} Stage08 review</title><link rel="stylesheet" href="../style.css"><style>
.review-toolbar{{display:flex;gap:10px;flex-wrap:wrap;align-items:end}} .review-toolbar label{{display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:700}} .review-toolbar select,.review-toolbar input{{min-width:150px;padding:7px}}
.review-head{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}} .decision-chip{{padding:7px 10px;border:1px solid #ccd4df;border-radius:999px;font-weight:800}} .decision-chip.ACCEPT{{background:#e7f7ef}} .decision-chip.REJECT{{background:#fdecec}} .decision-chip.UNCERTAIN{{background:#fff5dc}}
.reviewpair{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:16px}} .reviewpair img{{display:block;width:100%;max-width:420px;aspect-ratio:1/1;object-fit:contain;background:#0b1018;border-radius:10px}}
.review-bottom{{display:grid;grid-template-columns:minmax(280px,.8fr) minmax(320px,1.2fr);gap:24px;margin-top:16px}} .review-bottom table{{width:100%;border-collapse:collapse}} .review-bottom th,.review-bottom td{{padding:7px 9px;border-bottom:1px solid #e3e8ef;text-align:left}}
.buttons,.navbuttons{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}} .small{{font-size:12px;color:#657080}} @media(max-width:820px){{.reviewpair,.review-bottom{{grid-template-columns:1fr}}}}
</style></head><body data-key={js_safe(key)} data-bundle={js_safe(label)}><div class="top"><a href="../index.html">← {label}</a><b>Stage08 independent identity review</b></div><div class="wrap">
<div class="card"><p><strong>Independent review only.</strong> Filters and sorting help navigation; they never auto-assign identity. Decisions remain local until a reviewer exports JSON and the CLI consensus step is run.</p><p>仅用于独立人工复核。筛选和排序只帮助浏览，不会自动判定 same-cell；只有 reviewer 导出 JSON 并经过 CLI consensus 后才能冻结。</p>
<div class="review-toolbar"><label>Reviewer<input id="reviewer"></label><label>Session pair<select id="pair"></select></label><label>Source grade<select id="grade"></select></label><label>Authority<select id="authority"></select></label><label>Review state<select id="state"><option value="">All</option><option value="UNREVIEWED">Unreviewed</option><option value="REVIEWED">Reviewed</option></select></label><label>Sort<select id="sort"><option value="">Original order</option><option value="corr">Local corr ↓</option><option value="distance">Distance ↑</option><option value="area">Area ratio ≈1</option></select></label></div>
<div style="margin-top:12px"><button onclick="exp()">Export decisions JSON</button><label style="margin-left:8px">Import review JSON <input type="file" accept=".json,application/json" onchange="importReview(this)"></label></div>
<p><b id="globalProgress"></b> · <span id="visibleCount"></span></p></div><div id="app"></div></div><script src="identity_review_data.js"></script><script src="review.js"></script></body></html>'''
    (review/"index.html").write_text(page,encoding="utf-8")
    print(json.dumps({"bundle":str(root),"label":label,"n_candidates":len(rows),"review_dir":str(review)},indent=2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("bundle_root")
    ap.add_argument("--label")
    ap.add_argument("--storage-key")
    a=ap.parse_args()
    build(a.bundle_root,a.label,a.storage_key)

if __name__=="__main__":
    main()
