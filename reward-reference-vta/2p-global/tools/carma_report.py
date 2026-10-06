from __future__ import annotations
from pathlib import Path
import html, json, os, math
import numpy as np
import pandas as pd
import yaml
from PIL import Image

def _load_json(p, default=None):
    p=Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def _jsonable(v):
    if isinstance(v,(np.integer,)): return int(v)
    if isinstance(v,(np.floating,)): return None if not np.isfinite(v) else float(v)
    if isinstance(v,(np.bool_,)): return bool(v)
    if isinstance(v,float) and not math.isfinite(v): return None
    if pd.isna(v): return None
    return v

def _norm_u8(a):
    a=np.asarray(a,float)
    lo,hi=np.nanpercentile(a,[1,99.5])
    if not np.isfinite(lo): lo=0
    if not np.isfinite(hi) or hi<=lo: hi=lo+1
    return np.clip((a-lo)/(hi-lo)*255,0,255).astype(np.uint8)

def _mask_crop(mean,mask,out):
    y,x=np.nonzero(mask)
    if not len(x): return None
    cy,cx=float(y.mean()),float(x.mean()); pad=44
    x0=max(0,int(round(cx))-pad); x1=min(mean.shape[1],int(round(cx))+pad)
    y0=max(0,int(round(cy))-pad); y1=min(mean.shape[0],int(round(cy))+pad)
    g=_norm_u8(mean[y0:y1,x0:x1])
    rgb=np.repeat(g[...,None],3,axis=2)
    m=np.asarray(mask[y0:y1,x0:x1],bool)
    edge=m.copy()
    if edge.shape[0]>2 and edge.shape[1]>2:
        edge[1:-1,1:-1] &= ~(m[:-2,1:-1]&m[2:,1:-1]&m[1:-1,:-2]&m[1:-1,2:])
    rgb[edge]=[205,45,45]
    out.parent.mkdir(parents=True,exist_ok=True)
    Image.fromarray(rgb).save(out)
    return out.name

def _down(v,n=600):
    v=np.asarray(v,float)
    if len(v)<=n: return v
    ix=np.linspace(0,len(v)-1,n).round().astype(int)
    return v[ix]

def _finite_list(v,nd=5):
    return [None if not np.isfinite(float(x)) else round(float(x),nd) for x in np.asarray(v).ravel()]

def _rel_link(src,from_dir):
    try: return Path(os.path.relpath(src,from_dir)).as_posix()
    except Exception: return None

def _build_viewer(root,sid,row,cfg,session_report_dir):
    sdir=root/"sessions"/sid
    need=[
        sdir/"stage_01"/"mean_image.npy",sdir/"stage_02"/"roi_masks.npy",
        sdir/"stage_03"/"traces.npz",sdir/"stage_04"/"final_signal.npz",
        sdir/"stage_05"/"aligned_trials.csv",sdir/"stage_06"/"per_roi.csv"
    ]
    if not all(p.exists() for p in need): return None
    mean=np.load(need[0]); masks=np.load(need[1]).astype(bool)
    z3=np.load(need[2]); raw=np.asarray(z3["raw"],float); bg=np.asarray(z3["bg"],float)
    z4=np.load(need[3]); final=np.asarray(z4["signal"],float)
    trials=pd.read_csv(need[4]); per=pd.read_csv(need[5])
    nroi,nframes=final.shape
    fr=float(row.get("frame_rate",cfg.get("frame_rate",10.0)))
    windows=cfg.get("windows",{"cue":[-3,-1],"predictive":[-1,0],"outcome":[0,2],"late":[2,6],"post":[6,9]})
    lo=min(float(v[0]) for v in windows.values()); hi=max(float(v[1]) for v in windows.values())
    offs=np.arange(int(round(lo*fr)),int(round(hi*fr))+1,dtype=int)
    rt=offs/fr
    condcol=cfg.get("condition_column","condition")
    conds=trials[condcol].astype(str).tolist() if condcol in trials.columns else ["all"]*len(trials)
    event=trials["event_frame"].astype(int).to_numpy()
    valid=np.array([(e+offs[0]>=0 and e+offs[-1]<nframes) for e in event],bool)
    eventv=event[valid]; condv=[c for c,k in zip(conds,valid) if k]
    assets=session_report_dir/"assets"; assets.mkdir(parents=True,exist_ok=True)
    roi_items=[]
    for i in range(min(nroi,len(masks),len(per))):
        rid=int(per.iloc[i]["roi_id"])
        mask_name=_mask_crop(mean,masks[i],assets/f"roi_{rid}_mask.png")
        ix=np.linspace(0,nframes-1,min(nframes,600)).round().astype(int)
        mat=np.stack([final[i,e+offs] for e in eventv]) if len(eventv) else np.empty((0,len(offs)))
        zmat=mat.copy()
        pre=rt<0
        if len(mat) and pre.any():
            mu=np.nanmean(mat[:,pre],axis=1,keepdims=True)
            sd=np.nanstd(mat[:,pre],axis=1,keepdims=True)+1e-9
            zmat=(mat-mu)/sd
        aligned_raw=np.stack([raw[i,e+offs] for e in eventv]) if len(eventv) else np.empty((0,len(offs)))
        aligned_bg=np.stack([bg[i,e+offs] for e in eventv]) if len(eventv) else np.empty((0,len(offs)))
        metrics={k:_jsonable(v) for k,v in per.iloc[i].to_dict().items()}
        roi_items.append({
            "roi_id":rid,"mask_png":"assets/"+mask_name if mask_name else None,"metrics":metrics,
            "continuous_time_s":_finite_list(ix/fr),
            "continuous_raw":_finite_list(raw[i,ix]),
            "continuous_bg":_finite_list(bg[i,ix]),
            "continuous_final":_finite_list(final[i,ix]),
            "aligned_time_s":_finite_list(rt),
            "mean_aligned_raw":_finite_list(np.nanmean(aligned_raw,axis=0)) if len(aligned_raw) else [],
            "mean_aligned_bg":_finite_list(np.nanmean(aligned_bg,axis=0)) if len(aligned_bg) else [],
            "mean_aligned_final":_finite_list(np.nanmean(mat,axis=0)) if len(mat) else [],
            "trial_heatmap_z":[_finite_list(x) for x in zmat],
        })
    obj={
        "schema":"CARMA_PROJECT_ROI_EXPLORER_V1","session_id":sid,
        "frame_rate":fr,"n_frames":nframes,"n_roi":len(roi_items),
        "n_trials_total":len(trials),"n_trials_heatmap":int(valid.sum()),
        "conditions":condv,"windows":windows,"rois":roi_items
    }
    payload=json.dumps(obj,separators=(",",":"))
    p=session_report_dir/"roi_explorer_data.json"
    p.write_text(payload,encoding="utf-8")
    (session_report_dir/"roi_explorer_data.js").write_text("window.CARMA_VIEWER="+payload+";",encoding="utf-8")
    return obj

CSS="""body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;margin:0;background:#f6f8fb;color:#172033}a{color:#2468d8;text-decoration:none}.wrap{max-width:1240px;margin:auto;padding:28px}.top{background:white;border-bottom:1px solid #dfe5ee}.top .wrap{padding-top:18px;padding-bottom:18px}.eyebrow{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#2468d8}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{background:white;border:1px solid #dfe5ee;border-radius:14px;padding:16px;box-shadow:0 7px 20px rgba(20,35,60,.06)}h1{margin:4px 0 10px}h2{margin-top:32px}.PASS,.FROZEN,.MIGRATED{color:#087a55;font-weight:800}.WARN,.REVIEW_REQUIRED,.REVIEW{color:#a56800;font-weight:800}.FAIL,.INVALID{color:#a52f36;font-weight:800}.NA{color:#707782;font-weight:800}table{border-collapse:collapse;width:100%;background:white}th,td{padding:7px 9px;border-bottom:1px solid #e3e8ef;text-align:left;font-size:13px;vertical-align:top}th{background:#eef3f8}.scroll{overflow:auto;max-height:560px;border:1px solid #dfe5ee;border-radius:12px}.stage{border-left:4px solid #dfe5ee}.stage.PASS,.stage.FROZEN,.stage.MIGRATED{border-left-color:#16835d}.stage.WARN,.stage.REVIEW_REQUIRED,.stage.REVIEW{border-left-color:#bf7b08}.stage.FAIL,.stage.INVALID{border-left-color:#b33d42}.small{font-size:12px;color:#677285}.viewer{display:grid;grid-template-columns:280px 1fr;gap:18px}.mask{width:100%;aspect-ratio:1/1;object-fit:contain;background:#0b1018;border-radius:10px}.plot svg{display:block;width:100%;height:auto}.heat{display:block;width:100%;height:260px;image-rendering:pixelated;border:1px solid #dfe5ee;border-radius:8px}.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:12px 0}select{padding:7px 9px}.metric{font-size:29px;font-weight:800}@media(max-width:850px){.grid,.grid2,.viewer{grid-template-columns:1fr}}"""

JS=r"""let V=null;
const $=x=>document.getElementById(x);
const f=(v,d=3)=>v==null||Number.isNaN(+v)?'—':typeof v==='number'?v.toFixed(d):String(v);
function q(a,p){a=a.filter(Number.isFinite).sort((x,y)=>x-y);if(!a.length)return 0;let x=(a.length-1)*p,l=Math.floor(x),h=Math.ceil(x);return a[l]*(h-x)+a[h]*(x-l)}
function traceSvg(t,ss){const W=800,H=250,L=52,R=15,T=15,B=35,A=ss.flatMap(s=>s.v).map(Number).filter(Number.isFinite),lo=q(A,.02),hi=q(A,.98),mn=lo===hi?lo-1:lo,mx=lo===hi?hi+1:hi,x=v=>L+(v-t[0])/(t.at(-1)-t[0])*(W-L-R),y=v=>T+(mx-v)/(mx-mn)*(H-T-B),cs=['#111827','#9ca3af','#2563eb'];let z='<svg viewBox="0 0 '+W+' '+H+'"><line x1="'+L+'" y1="'+(H-B)+'" x2="'+(W-R)+'" y2="'+(H-B)+'" stroke="#111"/><line x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(H-B)+'" stroke="#111"/>';ss.forEach((s,k)=>{let p='';s.v.forEach((v,i)=>{if(v==null)return;p+=(p?'L':'M')+x(t[i]).toFixed(1)+','+y(+v).toFixed(1)});z+='<path d="'+p+'" fill="none" stroke="'+cs[k]+'" stroke-width="'+(k===2?2.2:1.4)+'"/>'});z+='<text x="'+W/2+'" y="'+(H-4)+'" text-anchor="middle" font-size="12">time (s)</text></svg>';return z}
function heat(c,m){if(!m.length)return;c.width=m[0].length;c.height=m.length;let x=m.flat().map(Number).filter(Number.isFinite),lim=Math.max(Math.abs(q(x,.02)),Math.abs(q(x,.98)))||1,ctx=c.getContext('2d'),im=ctx.createImageData(c.width,c.height),k=0;for(let r=0;r<c.height;r++)for(let j=0;j<c.width;j++){let v=Number(m[r][j])||0;v=Math.max(-lim,Math.min(lim,v))/lim;let R,G,B;if(v>=0){R=255;G=Math.round(255*(1-v));B=G}else{v=-v;R=Math.round(255*(1-v));G=R;B=255}im.data[k++]=R;im.data[k++]=G;im.data[k++]=B;im.data[k++]=255}ctx.putImageData(im,0,0)}
function show(i){let r=V.rois[i];$('roiPick').value=i;$('mask').src=r.mask_png||'';$('cont').innerHTML=traceSvg(r.continuous_time_s,[{v:r.continuous_raw},{v:r.continuous_bg},{v:r.continuous_final}]);$('aligned').innerHTML=traceSvg(r.aligned_time_s,[{v:r.mean_aligned_raw},{v:r.mean_aligned_bg},{v:r.mean_aligned_final}]);heat($('heat'),r.trial_heatmap_z);let m=r.metrics;$('metrics').innerHTML=Object.keys(m).map(k=>'<tr><th>'+k+'</th><td>'+f(m[k],4)+'</td></tr>').join('');$('roiTitle').textContent='ROI '+r.roi_id;$('heatcap').textContent=V.n_trials_heatmap+' aligned trials · z-scored to pre-event baseline';}
function initViewer(v){V=v;$('viewerBlock').hidden=false;$('roiPick').innerHTML=v.rois.map((r,i)=>'<option value="'+i+'">ROI '+r.roi_id+'</option>').join('');$('roiPick').onchange=()=>show(+$('roiPick').value);show(0)}
if(window.CARMA_VIEWER){initViewer(window.CARMA_VIEWER)}else{fetch('roi_explorer_data.json').then(r=>r.json()).then(initViewer).catch(()=>{})}
"""

def _session_html(root,sid,row,cfg,state,report_dir,viewer):
    stages=[]
    for sg in [f"{i:02d}" for i in range(11)]:
        ent=state.get("stages",{}).get(sg,{"status":"PENDING","name":sg})
        sd=root/"sessions"/sid/f"stage_{sg}"
        qc=_load_json(sd/"qc.json",{}) or {}
        outs=_load_json(sd/"outputs.json",[]) or []
        metrics=qc.get("metrics",ent.get("metrics",{})) or {}
        outlinks=[]
        for x in outs:
            p=Path(str(x.get("path","")))
            if p.exists():
                rel=_rel_link(p,report_dir)
                outlinks.append(f"<a href='{html.escape(rel)}'>{html.escape(p.name)}</a>")
            elif x.get("path"): outlinks.append(html.escape(Path(str(x["path"])).name))
        metric_text=" · ".join(f"{html.escape(str(k))}={html.escape(str(v))}" for k,v in list(metrics.items())[:8])
        status=str(ent.get("status","PENDING"))
        stages.append(f"<div class='card stage {status}'><div class='eyebrow'>Stage {sg}</div><b>{html.escape(str(ent.get('name',sg)))}</b><div class='{status}'>{status}</div><div class='small'>{metric_text}</div><div class='small'>{' · '.join(outlinks) or 'no outputs'}</div></div>")
    per=root/"sessions"/sid/"stage_06"/"per_roi.csv"
    pt=""
    if per.exists():
        df=pd.read_csv(per)
        pt="<div class='scroll'>"+df.head(300).to_html(index=False,escape=True)+"</div>"
    overlay=root/"sessions"/sid/"stage_02"/"roi_overlay.png"
    overlay_html=f"<img src='{html.escape(_rel_link(overlay,report_dir))}' style='max-width:100%;border-radius:10px'>" if overlay.exists() else ""
    viewer_html=""
    if viewer and viewer.get("rois"):
        viewer_html="""<h2>Single-ROI explorer</h2><div id='viewerBlock' class='card' hidden><div class='controls'><label>ROI <select id='roiPick'></select></label><b id='roiTitle'></b></div><div class='viewer'><div><img id='mask' class='mask'><div id='metrics' class='scroll'><table><tbody></tbody></table></div></div><div><h3>Continuous raw / background / final</h3><div id='cont' class='plot'></div><h3>Event-aligned mean raw / background / final</h3><div id='aligned' class='plot'></div><h3>Trial × time heatmap · final signal z</h3><canvas id='heat' class='heat'></canvas><p id='heatcap' class='small'></p></div></div></div><script src='roi_explorer_data.js'></script><script>"""+JS+"""</script>"""
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(sid)} · CaRMA</title><style>{CSS}</style></head><body><div class='top'><div class='wrap'><a href='../../index.html'>← dataset</a><div class='eyebrow'>CaRMA session report</div><h1>{html.escape(sid)}</h1><div>{html.escape(str(row.get('animal','')))} · {html.escape(str(row.get('day','')))} · {html.escape(str(row.get('task','')))}</div></div></div><main class='wrap'><h2>Stage ledger</h2><div class='grid'>{''.join(stages)}</div><h2>ROI morphology / registration context</h2>{overlay_html}{viewer_html}<h2>Per-ROI authority</h2>{pt or '<p>Stage06 per_roi.csv not available.</p>'}</main></body></html>"""

def build_project_report(root):
    root=Path(root).resolve()
    cfg=yaml.safe_load((root/"dataset.yaml").read_text(encoding="utf-8"))
    sess=pd.read_csv(root/cfg.get("sessions_file","sessions.csv"),dtype={"session_id":str,"animal":str,"day":str})
    out=root/"reports"; out.mkdir(parents=True,exist_ok=True)
    index_rows=[]
    all_per=[]
    for _,r in sess.iterrows():
        sid=str(r.session_id)
        state=_load_json(root/"sessions"/sid/"state.json",{}) or {}
        rd=out/"sessions"/sid; rd.mkdir(parents=True,exist_ok=True)
        viewer=_build_viewer(root,sid,r.to_dict(),cfg,rd)
        (rd/"index.html").write_text(_session_html(root,sid,r.to_dict(),cfg,state,rd,viewer),encoding="utf-8")
        statuses={k:v.get("status","PENDING") for k,v in state.get("stages",{}).items()}
        index_rows.append({"session_id":sid,"animal":r.get("animal",""),"day":r.get("day",""),"task":r.get("task",""),**{f"stage_{k}":v for k,v in statuses.items()}})
        p=root/"sessions"/sid/"stage_06"/"per_roi.csv"
        if p.exists(): all_per.append(pd.read_csv(p))
    idx=pd.DataFrame(index_rows)
    idx.to_csv(out/"stage_status_matrix.csv",index=False)
    if all_per: pd.concat(all_per,ignore_index=True).to_csv(out/"per_roi_all.csv",index=False)
    cards=[]
    for rec in index_rows:
        ss=rec["session_id"]; st=[v for k,v in rec.items() if k.startswith("stage_")]
        done=sum(x in {"PASS","WARN","FROZEN","MIGRATED","NA","REVIEW_REQUIRED"} for x in st)
        cards.append(f"<div class='card'><a href='sessions/{html.escape(ss)}/index.html'><b>{html.escape(ss)}</b></a><div>{html.escape(str(rec['task']))}</div><div class='metric'>{done}/11</div><div class='small'>stages recorded</div></div>")
    index=f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(str(cfg.get('dataset_id','CaRMA')))}</title><style>{CSS}</style></head><body><div class='top'><div class='wrap'><div class='eyebrow'>CaRMA 00→10 project report</div><h1>{html.escape(str(cfg.get('dataset_id','CaRMA dataset')))}</h1><p>Every session links to its stage ledger, provenance, QC, and—when Stage06 is complete—a real per-ROI mask/trace/trial-heatmap explorer.</p></div></div><main class='wrap'><div class='grid'>{''.join(cards)}</div><h2>Stage status matrix</h2><div class='scroll'>{idx.to_html(index=False,escape=True)}</div></main></body></html>"""
    (out/"index.html").write_text(index,encoding="utf-8")
    return out/"index.html"
