from pathlib import Path
import argparse, json, hashlib, shutil, sys, platform, re, os
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import yaml
import tifffile
from scipy import ndimage, stats
from skimage.registration import phase_cross_correlation
from skimage.measure import regionprops, label
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOOL_VERSION="1.0.0"
STAGES={
"00":{"name":"Intake + staging","deps":[]},
"01":{"name":"Within-trial registration","deps":["00"]},
"02":{"name":"ROI morphology + QC","deps":["01"]},
"03":{"name":"Activity extraction","deps":["02"]},
"04":{"name":"Signal selection","deps":["03"]},
"05":{"name":"Behavior alignment","deps":["00","03"]},
"06":{"name":"Functional metrics","deps":["04","05"]},
"07":{"name":"Cross-day image transform","deps":["01"]},
"08":{"name":"Cross-day cell identity","deps":["02","07"]},
"09":{"name":"Population + remapping inference","deps":["06"]},
"10":{"name":"Freeze + report","deps":["06","09"]},
}
DOWNSTREAM={"00":["01","05"],"01":["02","07"],"02":["03","08"],"03":["04","05"],"04":["06"],"05":["06"],"06":["09","10"],"07":["08"],"08":["09"],"09":["10"],"10":[]}
STATUS_OK={"PASS","WARN","FROZEN","NA","REVIEW_REQUIRED","MIGRATED"}
ROI_SCHEMA=["dataset_id","session_id","animal","day","task","roi_id","plane","x","y","area_px","edge_touch","morphology_pass","trace_snr","bg_corr","final_signal_method","n_trials","n_conditions","cue_effect","cue_p","predictive_effect","predictive_p","outcome_effect","outcome_p","late_effect","late_p","post_effect","post_p","trial_reliability","track_id","identity_status","qc_status","exclusion_flags"]

def now(): return datetime.now(timezone.utc).isoformat()
def sha256(path,block=1024*1024):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        while True:
            b=f.read(block)
            if not b: break
            h.update(b)
    return h.hexdigest()
def jdump(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str),encoding="utf-8")
def jload(path,default=None):
    p=Path(path); return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
def load_yaml(path): return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
def save_yaml(path,obj): Path(path).write_text(yaml.safe_dump(obj,sort_keys=False,allow_unicode=True),encoding="utf-8")
def project_root(path):
    p=Path(path).resolve()
    if p.is_file(): p=p.parent
    if not (p/"dataset.yaml").exists(): raise SystemExit(f"Not a CaRMA project: {p}")
    return p
def cfg(root): return load_yaml(Path(root)/"dataset.yaml")
def sessions_df(root):
    c=cfg(root); return pd.read_csv(Path(root)/c.get("sessions_file","sessions.csv"),dtype={"session_id":str,"animal":str,"day":str})
def session_dir(root,sid): return Path(root)/"sessions"/str(sid)
def stage_dir(root,sid,stage): return session_dir(root,sid)/f"stage_{stage}"
def state_path(root,sid): return session_dir(root,sid)/"state.json"
def read_state(root,sid):
    st=jload(state_path(root,sid),None) or {"session_id":str(sid),"created_at":now(),"tool_version":TOOL_VERSION,"stages":{}}
    for k,v in STAGES.items(): st["stages"].setdefault(k,{"name":v["name"],"status":"PENDING","updated_at":None,"message":""})
    return st
def write_state(root,sid,st): st["updated_at"]=now(); jdump(state_path(root,sid),st)
def log_stage(root,sid,stage,status,message="",metrics=None,outputs=None):
    st=read_state(root,sid); ent=st["stages"][stage]
    ent.update({"status":status,"message":message,"updated_at":now()})
    if metrics is not None: ent["metrics"]=metrics
    if outputs is not None: ent["outputs"]=[str(x) for x in outputs]
    write_state(root,sid,st)
def descendants(stage):
    seen=set(); stack=list(DOWNSTREAM.get(stage,[]))
    while stack:
        x=stack.pop()
        if x in seen: continue
        seen.add(x); stack.extend(DOWNSTREAM.get(x,[]))
    return sorted(seen)
def row_for(root,sid):
    s=sessions_df(root); m=s[s.session_id.astype(str)==str(sid)]
    if len(m)!=1: raise ValueError(f"session_id {sid}: expected 1 row, found {len(m)}")
    return m.iloc[0].to_dict()
def resolve_input(root,row,key):
    v=row.get(key,"")
    if pd.isna(v) or str(v).strip()=="": return None
    p=Path(str(v))
    return p if p.is_absolute() else (Path(root)/p).resolve()
def stage_guard(root,sid,stage,force=False):
    st=read_state(root,sid)
    if not force and st["stages"][stage]["status"] in STATUS_OK: return False,"already satisfied"
    for dep in STAGES[stage]["deps"]:
        s=st["stages"][dep]["status"]
        if s not in STATUS_OK: return False,f"dependency {dep} is {s}"
    return True,""
def write_stage_provenance(root,sid,stage,inputs,params,outputs,status,metrics=None,message=""):
    d=stage_dir(root,sid,stage); d.mkdir(parents=True,exist_ok=True)
    inp=[]
    for p in inputs:
        if p is None: continue
        p=Path(p); ex=p.exists()
        inp.append({"path":str(p),"exists":ex,"size":p.stat().st_size if ex and p.is_file() else None,"sha256":sha256(p) if ex and p.is_file() and p.stat().st_size<2_000_000_000 else None})
    out=[]
    for p in outputs:
        p=Path(p); ex=p.exists()
        out.append({"path":str(p),"exists":ex,"size":p.stat().st_size if ex and p.is_file() else None,"sha256":sha256(p) if ex and p.is_file() and p.stat().st_size<2_000_000_000 else None})
    jdump(d/"inputs.json",inp); jdump(d/"params.json",params); jdump(d/"outputs.json",out)
    jdump(d/"qc.json",{"status":status,"metrics":metrics or {},"message":message})
    jdump(d/"software_environment.json",{"tool_version":TOOL_VERSION,"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"pandas":pd.__version__,"timestamp":now()})
def get_registered_path(root,sid):
    p=stage_dir(root,sid,"01")/"registered.tif"
    if p.exists(): return p
    meta=jload(stage_dir(root,sid,"01")/"registered_authority.json",{})
    if meta.get("path"): return Path(meta["path"])
    raise FileNotFoundError(f"No registered movie for {sid}")
def read_movie(path):
    a=np.asarray(tifffile.imread(str(path)))
    if a.ndim==2: a=a[None,...]
    if a.ndim!=3: raise ValueError(f"Only 2D frame stacks supported in V1, got {a.shape}")
    return a.astype(np.float32,copy=False)
def frame_corrs(movie,ref):
    r=ref.ravel().astype(float); r-=r.mean(); rn=np.linalg.norm(r)+1e-12; out=[]
    for fr in movie:
        x=fr.ravel().astype(float); x-=x.mean(); out.append(float(np.dot(x,r)/(np.linalg.norm(x)*rn+1e-12)))
    return np.asarray(out)

def run_00(root,sid,row):
    d=stage_dir(root,sid,"00"); d.mkdir(parents=True,exist_ok=True)
    keys=["raw_tiff","registered_tiff","evt_file","behavior_file","roi_source"]; files={k:resolve_input(root,row,k) for k in keys}
    if not files["raw_tiff"] and not files["registered_tiff"]: raise ValueError("Need raw_tiff or registered_tiff")
    missing=[k for k in ["evt_file","behavior_file","roi_source"] if files[k] is None or not files[k].exists()]
    if missing: raise ValueError("Missing required inputs: "+",".join(missing))
    for k,p in files.items():
        if p is not None and not p.exists(): raise FileNotFoundError(f"{k}: {p}")
    manifest={"session_id":sid,"animal":str(row.get("animal","")),"day":str(row.get("day","")),"task":str(row.get("task","")),"analysis_role":str(row.get("analysis_role","MAIN")),"capability":str(row.get("capability","AUTO")),"files":{k:(str(v) if v else None) for k,v in files.items()},"created_at":now()}
    jdump(d/"intake_manifest.json",manifest); metrics={"required_fields_ok":True,"input_files_present":sum(p is not None for p in files.values())}
    write_stage_provenance(root,sid,"00",[p for p in files.values() if p],{},[d/"intake_manifest.json"],"PASS",metrics)
    return "PASS",metrics,[d/"intake_manifest.json"]

def run_01(root,sid,row):
    d=stage_dir(root,sid,"01"); d.mkdir(parents=True,exist_ok=True)
    raw=resolve_input(root,row,"raw_tiff"); reg=resolve_input(root,row,"registered_tiff"); rp=cfg(root).get("registration",{})
    if reg and reg.exists():
        movie=read_movie(reg); ref=movie.mean(0); cor=frame_corrs(movie,ref); np.save(d/"mean_image.npy",ref)
        jdump(d/"registered_authority.json",{"path":str(reg),"source":"provided_registered_tiff","frozen":True})
        metrics={"n_frames":int(movie.shape[0]),"height":int(movie.shape[1]),"width":int(movie.shape[2]),"frame_corr_median":float(np.median(cor)),"frame_corr_p05":float(np.quantile(cor,.05)),"shift_median_px":None,"shift_p95_px":None}
        write_stage_provenance(root,sid,"01",[reg],{"mode":"provided_registered_tiff"},[d/"mean_image.npy",d/"registered_authority.json"],"FROZEN",metrics)
        return "FROZEN",metrics,[d/"mean_image.npy",d/"registered_authority.json"]
    movie=read_movie(raw); ref=np.mean(movie[:min(len(movie),100)],axis=0); regmov=np.empty_like(movie); shifts=[]; rejected=[]
    max_shift=float(rp.get("max_shift_px",8.0)); prev=np.array([0.0,0.0])
    for i,fr in enumerate(movie):
        sh,_,_=phase_cross_correlation(ref,fr,upsample_factor=int(rp.get("upsample_factor",10)))
        sh=np.asarray(sh,dtype=float)
        bad=(not np.all(np.isfinite(sh))) or (np.linalg.norm(sh)>max_shift)
        if bad:
            sh=prev.copy()
        else:
            prev=sh.copy()
        rejected.append(bool(bad)); shifts.append(sh)
        regmov[i]=ndimage.shift(fr,shift=sh,order=1,mode="nearest",prefilter=False)
    shifts=np.asarray(shifts,float); tifffile.imwrite(str(d/"registered.tif"),regmov.astype(np.float32)); ref2=regmov.mean(0); np.save(d/"mean_image.npy",ref2)
    mag=np.linalg.norm(shifts,axis=1); cor=frame_corrs(regmov,ref2)
    metrics={"n_frames":int(len(movie)),"height":int(movie.shape[1]),"width":int(movie.shape[2]),"frame_corr_median":float(np.median(cor)),"frame_corr_p05":float(np.quantile(cor,.05)),"shift_median_px":float(np.median(mag)),"shift_p95_px":float(np.quantile(mag,.95)),"shift_p99_px":float(np.quantile(mag,.99)),"shift_max_px":float(np.max(mag)),"max_shift_gate_px":max_shift,"rejected_large_shift_fraction":float(np.mean(rejected))}
    pd.DataFrame({"frame":np.arange(len(movie)),"dy":shifts[:,0],"dx":shifts[:,1],"shift_px":mag,"phase_candidate_rejected":rejected,"frame_corr":cor}).to_csv(d/"registration_qc.csv",index=False)
    reg_status="WARN" if metrics["rejected_large_shift_fraction"]>float(rp.get("warn_rejected_fraction",0.20)) or metrics["frame_corr_median"]<float(rp.get("warn_frame_corr_median",0.50)) else "PASS"
    write_stage_provenance(root,sid,"01",[raw],rp,[d/"registered.tif",d/"mean_image.npy",d/"registration_qc.csv"],reg_status,metrics)
    return reg_status,metrics,[d/"registered.tif",d/"mean_image.npy",d/"registration_qc.csv"]

def roi_masks_from_source(path,shape,params):
    h,w=shape; p=Path(path)
    if p.suffix.lower()==".csv":
        df=pd.read_csv(p)
        if not {"x","y"}.issubset(df.columns): raise ValueError("ROI CSV requires x,y")
        if "roi_id" not in df.columns: df["roi_id"]=np.arange(1,len(df)+1)
        radius=df["radius"].to_numpy() if "radius" in df.columns else np.full(len(df),params.get("default_radius_px",5))
        yy,xx=np.mgrid[0:h,0:w]; masks=[(xx-float(r.x))**2+(yy-float(r.y))**2<=float(rad)**2 for (_,r),rad in zip(df.iterrows(),radius)]
        return np.asarray(masks,bool),df[["roi_id","x","y"]].copy()
    if p.suffix.lower()==".npy":
        obj=np.load(p,allow_pickle=True)
        if obj.dtype==object and obj.ndim==1:
            masks=[]; rows=[]
            for i,s in enumerate(obj):
                m=np.zeros((h,w),bool); yp=np.asarray(s["ypix"],int); xp=np.asarray(s["xpix"],int); ok=(yp>=0)&(yp<h)&(xp>=0)&(xp<w); m[yp[ok],xp[ok]]=True
                masks.append(m); rows.append({"roi_id":i+1,"x":float(xp[ok].mean()),"y":float(yp[ok].mean())})
            return np.asarray(masks,bool),pd.DataFrame(rows)
        if obj.ndim==3 and obj.shape[1:]==(h,w):
            rows=[]
            for i,m in enumerate(obj.astype(bool)):
                y,x=np.nonzero(m); rows.append({"roi_id":i+1,"x":float(x.mean()),"y":float(y.mean())})
            return obj.astype(bool),pd.DataFrame(rows)
    raise ValueError("roi_source must be CSV(x,y[,radius]) or NPY masks/Suite2p stat.npy")

def run_02(root,sid,row):
    d=stage_dir(root,sid,"02"); d.mkdir(parents=True,exist_ok=True); movie=read_movie(get_registered_path(root,sid)); mean=movie.mean(0)
    source=resolve_input(root,row,"roi_source"); params=cfg(root).get("roi_qc",{}); masks,coords=roi_masks_from_source(source,mean.shape,params)
    min_area=float(params.get("min_area_px",20)); max_area=float(params.get("max_area_px",1000)); records=[]; accepted=[]
    for i,m in enumerate(masks):
        area=int(m.sum()); edge=bool(m[0].any() or m[-1].any() or m[:,0].any() or m[:,-1].any()); rp=regionprops(label(m.astype(np.uint8))); ecc=float(rp[0].eccentricity) if rp else np.nan; solid=float(rp[0].solidity) if rp else np.nan
        ok=(area>=min_area and area<=max_area and not edge and np.isfinite(ecc)); accepted.append(ok)
        records.append({"roi_id":int(coords.iloc[i].roi_id),"x":float(coords.iloc[i].x),"y":float(coords.iloc[i].y),"area_px":area,"edge_touch":edge,"eccentricity":ecc,"solidity":solid,"morphology_pass":bool(ok)})
    q=pd.DataFrame(records); q.to_csv(d/"per_roi_qc.csv",index=False); np.save(d/"roi_masks.npy",masks); np.save(d/"accepted.npy",np.asarray(accepted,bool))
    fig,ax=plt.subplots(figsize=(6,6)); ax.imshow(mean,cmap="gray")
    for i,m in enumerate(masks):
        ys,xs=np.nonzero(m)
        if len(xs): ax.plot(xs.mean(),ys.mean(),"o",ms=3,mec="none",color=("lime" if accepted[i] else "red"))
    ax.set_axis_off(); fig.tight_layout(); fig.savefig(d/"roi_overlay.png",dpi=180); plt.close(fig)
    metrics={"n_roi":len(masks),"n_accepted":int(np.sum(accepted)),"accepted_fraction":float(np.mean(accepted))}; status="PASS" if np.sum(accepted)>0 else "FAIL"
    write_stage_provenance(root,sid,"02",[source,get_registered_path(root,sid)],params,[d/"per_roi_qc.csv",d/"roi_masks.npy",d/"accepted.npy",d/"roi_overlay.png"],status,metrics)
    return status,metrics,[d/"per_roi_qc.csv",d/"roi_masks.npy",d/"accepted.npy",d/"roi_overlay.png"]

def run_03(root,sid,row):
    d=stage_dir(root,sid,"03"); d.mkdir(parents=True,exist_ok=True); movie=read_movie(get_registered_path(root,sid))
    masks=np.load(stage_dir(root,sid,"02")/"roi_masks.npy"); accepted=np.load(stage_dir(root,sid,"02")/"accepted.npy").astype(bool); params=cfg(root).get("extraction",{})
    inner=int(params.get("neuropil_inner_px",2)); outer=int(params.get("neuropil_outer_px",7)); alpha=float(params.get("alpha",0.7)); union=np.any(masks,axis=0)
    raw=[]; bg=[]; snr=[]; bgcorr=[]
    for m,ok in zip(masks,accepted):
        if not ok: raw.append(np.full(movie.shape[0],np.nan)); bg.append(np.full(movie.shape[0],np.nan)); snr.append(np.nan); bgcorr.append(np.nan); continue
        r=movie[:,m].mean(1); ring=ndimage.binary_dilation(m,iterations=outer)&~ndimage.binary_dilation(m,iterations=inner)&~union
        b=movie[:,ring].mean(1) if ring.sum()>=10 else np.nanmedian(movie.reshape(movie.shape[0],-1),axis=1); s=r-alpha*b; med=np.nanmedian(s); mad=np.nanmedian(np.abs(s-med))*1.4826+1e-9
        snr.append(float((np.nanpercentile(s,95)-med)/mad)); bgcorr.append(float(np.corrcoef(r,b)[0,1]) if np.std(r)>0 and np.std(b)>0 else np.nan); raw.append(r); bg.append(b)
    raw=np.asarray(raw); bg=np.asarray(bg); sub=raw-alpha*bg; np.savez_compressed(d/"traces.npz",raw=raw,bg=bg,sub=sub,accepted=accepted,alpha=alpha)
    roi_ids=pd.read_csv(stage_dir(root,sid,"02")/"per_roi_qc.csv")["roi_id"].astype(int).to_numpy()
    if len(roi_ids)!=len(masks): raise ValueError("Stage02 ROI ID count does not match mask count")
    q=pd.DataFrame({"roi_id":roi_ids,"accepted":accepted,"trace_snr":snr,"bg_corr":bgcorr}); q.to_csv(d/"extraction_qc.csv",index=False)
    metrics={"n_roi":len(masks),"n_accepted":int(accepted.sum()),"median_snr":float(np.nanmedian(snr)),"median_bg_corr":float(np.nanmedian(bgcorr))}
    write_stage_provenance(root,sid,"03",[get_registered_path(root,sid),stage_dir(root,sid,"02")/"roi_masks.npy"],params,[d/"traces.npz",d/"extraction_qc.csv"],"PASS",metrics)
    return "PASS",metrics,[d/"traces.npz",d/"extraction_qc.csv"]

def run_04(root,sid,row):
    d=stage_dir(root,sid,"04"); d.mkdir(parents=True,exist_ok=True); z=np.load(stage_dir(root,sid,"03")/"traces.npz"); raw=z["raw"]; bg=z["bg"]; accepted=z["accepted"].astype(bool)
    params=cfg(root).get("signal_selection",{}); alphas=[float(x) for x in params.get("candidate_alphas",[0.0,0.5,0.7,1.0])]; rows=[]
    for a in alphas:
        s=raw-a*bg; vals=[abs(np.corrcoef(s[i],bg[i])[0,1]) for i in np.where(accepted)[0] if np.std(s[i])>0 and np.std(bg[i])>0]
        rows.append({"method":f"raw_minus_{a:g}bg","alpha":a,"median_abs_bg_corr":float(np.nanmedian(vals)) if vals else np.inf})
    # Primary extraction coefficient is prespecified: Suite2p-style α=0.7.
    # Diagnostics may compare other coefficients but must never silently override the default.
    a=float(params.get("default_alpha",cfg(root).get("extraction",{}).get("alpha",0.7)))
    if not np.isfinite(a) or a<0: raise ValueError("Invalid default neuropil alpha")
    if not any(np.isclose(a,x) for x in alphas):
        vals=[abs(np.corrcoef(raw[i]-a*bg[i],bg[i])[0,1]) for i in np.where(accepted)[0]
              if np.std(raw[i]-a*bg[i])>0 and np.std(bg[i])>0]
        rows.append({"method":f"raw_minus_{a:g}bg","alpha":a,"median_abs_bg_corr":float(np.nanmedian(vals)) if vals else np.inf})
    tab=pd.DataFrame(rows).sort_values(["alpha"])
    chosen=tab.loc[np.isclose(tab.alpha,a)].iloc[0]
    final=raw-a*bg
    np.savez_compressed(d/"final_signal.npz",signal=final,alpha=a,accepted=accepted)
    tab["is_default"]=[bool(np.isclose(x,a)) for x in tab.alpha]
    tab.to_csv(d/"signal_selection.csv",index=False)
    jdump(d/"final_signal_method.json",{"method":"prespecified_suite2p_style_neuropil",
          "alpha":a,"selection_rule":"fixed prespecified coefficient (default 0.7); alternative candidates are QC only"})
    metrics={"chosen_method":"prespecified_suite2p_style_neuropil","chosen_alpha":a,
             "median_abs_bg_corr":float(chosen.median_abs_bg_corr)}
    write_stage_provenance(root,sid,"04",[stage_dir(root,sid,"03")/"traces.npz"],params,[d/"final_signal.npz",d/"signal_selection.csv",d/"final_signal_method.json"],"PASS",metrics)
    return "PASS",metrics,[d/"final_signal.npz",d/"signal_selection.csv",d/"final_signal_method.json"]

def normalize_event_table(evt,frame_rate):
    if "trial_id" not in evt.columns: raise ValueError("evt_file requires trial_id")
    e=evt.copy()
    if "event_name" in e.columns:
        anchor=e[e.event_name.astype(str).str.lower().isin(["anchor","outcome","reward","event"])]
        if len(anchor): e=anchor
    if "event_frame" in e.columns: out=e[["trial_id","event_frame"]].copy()
    elif "event_time_s" in e.columns:
        out=e[["trial_id","event_time_s"]].copy(); out["event_frame"]=np.rint(out.event_time_s.astype(float)*frame_rate).astype(int)
    else: raise ValueError("evt_file requires event_frame or event_time_s")
    return out.drop_duplicates("trial_id")

def run_05(root,sid,row):
    d=stage_dir(root,sid,"05"); d.mkdir(parents=True,exist_ok=True); evtp=resolve_input(root,row,"evt_file"); behp=resolve_input(root,row,"behavior_file"); evt=pd.read_csv(evtp); beh=pd.read_csv(behp)
    if "trial_id" not in beh.columns: raise ValueError("behavior_file requires trial_id")
    if beh.trial_id.duplicated().any(): raise ValueError("behavior trial_id must be unique")
    fr=float(row.get("frame_rate",cfg(root).get("frame_rate",10.0))); ev=normalize_event_table(evt,fr)
    if ev.trial_id.duplicated().any(): raise ValueError("event trial_id must be unique")
    aligned=beh.merge(ev,on="trial_id",how="inner",validate="one_to_one")
    if len(aligned)==0: raise ValueError("No trial IDs joined between behavior and EVT")
    aligned.to_csv(d/"aligned_trials.csv",index=False); metrics={"n_behavior_trials":len(beh),"n_event_trials":len(ev),"n_aligned":len(aligned),"missing_behavior_join":int(len(beh)-len(aligned)),"missing_event_join":int(len(ev)-len(aligned))}
    status="PASS" if len(aligned)>=max(1,int(.8*min(len(beh),len(ev)))) else "WARN"; write_stage_provenance(root,sid,"05",[evtp,behp],{"join":"explicit trial_id","frame_rate":fr},[d/"aligned_trials.csv"],status,metrics)
    return status,metrics,[d/"aligned_trials.csv"]

def window_response(sig,event_frame,lo_s,hi_s,fr):
    a=event_frame+int(round(lo_s*fr)); b=event_frame+int(round(hi_s*fr))
    if a<0 or b>sig.shape[1] or b<=a: return np.full(sig.shape[0],np.nan)
    return np.nanmean(sig[:,a:b],axis=1)

def run_06(root,sid,row):
    d=stage_dir(root,sid,"06"); d.mkdir(parents=True,exist_ok=True); z=np.load(stage_dir(root,sid,"04")/"final_signal.npz"); sig=z["signal"]; accepted=z["accepted"].astype(bool)
    qroi=pd.read_csv(stage_dir(root,sid,"02")/"per_roi_qc.csv"); qext=pd.read_csv(stage_dir(root,sid,"03")/"extraction_qc.csv").set_index("roi_id"); trials=pd.read_csv(stage_dir(root,sid,"05")/"aligned_trials.csv")
    fr=float(row.get("frame_rate",cfg(root).get("frame_rate",10.0))); windows=cfg(root).get("windows",{"cue":[-3,-1],"predictive":[-1,0],"outcome":[0,2],"late":[2,6],"post":[6,9]}); resp={name:np.vstack([window_response(sig,int(f),float(lo),float(hi),fr) for f in trials.event_frame]) for name,(lo,hi) in windows.items()}
    condcol=cfg(root).get("condition_column","condition"); conds=list(pd.unique(trials[condcol])) if condcol in trials.columns else ["all"]; rows=[]
    method=jload(stage_dir(root,sid,"04")/"final_signal_method.json")["method"]
    for i in range(sig.shape[0]):
        base=qroi.iloc[i].to_dict(); r={"dataset_id":cfg(root)["dataset_id"],"session_id":sid,"animal":str(row.get("animal","")),"day":str(row.get("day","")),"task":str(row.get("task","")),"roi_id":int(base["roi_id"]),"plane":int(row.get("plane",0) if not pd.isna(row.get("plane",0)) else 0),"x":float(base["x"]),"y":float(base["y"]),"area_px":float(base["area_px"]),"edge_touch":bool(base["edge_touch"]),"morphology_pass":bool(base["morphology_pass"]),"trace_snr":float(qext.loc[int(base["roi_id"]),"trace_snr"]),"bg_corr":float(qext.loc[int(base["roi_id"]),"bg_corr"]),"final_signal_method":method,"n_trials":int(len(trials)),"n_conditions":int(len(conds)),"track_id":"","identity_status":"NA","qc_status":"PASS" if accepted[i] else "FAIL","exclusion_flags":"" if accepted[i] else "ROI_QC_FAIL"}
        for name in ["cue","predictive","outcome","late","post"]:
            rr=resp.get(name); effect=np.nan; p=np.nan
            if rr is not None:
                if len(conds)==2:
                    a=rr[trials[condcol]==conds[0],i]; b=rr[trials[condcol]==conds[1],i]; effect=float(np.nanmean(b)-np.nanmean(a))
                    if np.isfinite(a).sum()>=2 and np.isfinite(b).sum()>=2: p=float(stats.ttest_ind(a,b,equal_var=False,nan_policy="omit").pvalue)
                else: effect=float(np.nanmean(rr[:,i]))
            r[f"{name}_effect"]=effect; r[f"{name}_p"]=p
        ol=np.c_[resp.get("outcome")[:,i],resp.get("late")[:,i]] if "outcome" in resp and "late" in resp else np.empty((0,2))
        if len(trials)>=4:
            odd=np.nanmean(ol[::2],axis=0); even=np.nanmean(ol[1::2],axis=0); r["trial_reliability"]=float(1.0-abs(np.nanmean(odd)-np.nanmean(even))/(np.nanstd(ol)+1e-9))
        else: r["trial_reliability"]=np.nan
        rows.append(r)
    per=pd.DataFrame(rows)
    for col in ROI_SCHEMA:
        if col not in per.columns: per[col]=np.nan
    per=per[ROI_SCHEMA]; per.to_csv(d/"per_roi.csv",index=False)
    try: per.to_parquet(d/"per_roi.parquet",index=False)
    except Exception: pass
    long=[]
    for name,arr in resp.items():
        for ti,tr in trials.reset_index(drop=True).iterrows():
            for i in range(sig.shape[0]):
                if accepted[i]: long.append({"session_id":sid,"trial_id":tr.trial_id,"condition":tr.get(condcol,"all"),"window":name,"roi_id":int(per.iloc[i].roi_id),"response":arr[ti,i]})
    pd.DataFrame(long).to_parquet(d/"trial_roi.parquet",index=False)
    metrics={"n_roi_total":len(per),"n_roi_pass":int((per.qc_status=="PASS").sum()),"n_trials":len(trials),"n_conditions":len(conds)}; write_stage_provenance(root,sid,"06",[stage_dir(root,sid,"04")/"final_signal.npz",stage_dir(root,sid,"05")/"aligned_trials.csv"],{"windows":windows,"condition_column":condcol},[d/"per_roi.csv",d/"trial_roi.parquet"],"PASS",metrics)
    return "PASS",metrics,[d/"per_roi.csv",d/"trial_roi.parquet"]

def run_07(root,sid,row):
    d=stage_dir(root,sid,"07"); d.mkdir(parents=True,exist_ok=True); s=sessions_df(root); peers=s[s.animal.astype(str)==str(row.get("animal",""))]
    if len(peers)<2:
        metrics={"reason":"single session for animal"}; write_stage_provenance(root,sid,"07",[],{},[],"NA",metrics); return "NA",metrics,[]
    cur=np.load(stage_dir(root,sid,"01")/"mean_image.npy"); rows=[]
    for _,pr in peers.iterrows():
        psid=str(pr.session_id)
        if psid==sid: continue
        pp=stage_dir(root,psid,"01")/"mean_image.npy"
        if not pp.exists(): continue
        ref=np.load(pp); sh,err,_=phase_cross_correlation(ref,cur,upsample_factor=10)
        moved=ndimage.shift(cur,shift=sh,order=1,mode="nearest",prefilter=False)
        a=ref.ravel().astype(float); b=moved.ravel().astype(float)
        image_corr=float(np.corrcoef(a,b)[0,1]) if np.std(a)>0 and np.std(b)>0 else np.nan
        rows.append({"source_session":sid,"target_session":psid,"dy":float(sh[0]),"dx":float(sh[1]),"phase_error":float(err),"registered_image_corr":image_corr})
    pd.DataFrame(rows).to_csv(d/"crossday_transforms.csv",index=False)
    metrics={"n_peer_transforms":len(rows),"median_registered_image_corr":float(np.nanmedian([x["registered_image_corr"] for x in rows])) if rows else None}
    status="PASS" if rows else "NA"
    write_stage_provenance(root,sid,"07",[stage_dir(root,sid,"01")/"mean_image.npy"],{"method":"phase_cross_correlation; all peer sessions must have Stage01 first"},[d/"crossday_transforms.csv"] if rows else [],status,metrics)
    return status,metrics,[d/"crossday_transforms.csv"] if rows else []

def local_patch_corr(a,b,ax,ay,bx,by,radius=10):
    ax=int(round(ax)); ay=int(round(ay)); bx=int(round(bx)); by=int(round(by)); r=int(radius)
    def crop(x,cx,cy):
        y0=max(0,cy-r); y1=min(x.shape[0],cy+r+1); x0=max(0,cx-r); x1=min(x.shape[1],cx+r+1)
        return x[y0:y1,x0:x1]
    pa=crop(a,ax,ay); pb=crop(b,bx,by)
    h=min(pa.shape[0],pb.shape[0]); w=min(pa.shape[1],pb.shape[1])
    if h<5 or w<5: return np.nan
    x=pa[:h,:w].ravel().astype(float); y=pb[:h,:w].ravel().astype(float)
    return float(np.corrcoef(x,y)[0,1]) if np.std(x)>0 and np.std(y)>0 else np.nan

def run_08(root,sid,row):
    d=stage_dir(root,sid,"08"); d.mkdir(parents=True,exist_ok=True); tr=stage_dir(root,sid,"07")/"crossday_transforms.csv"
    if not tr.exists():
        metrics={"reason":"no cross-day transforms"}; write_stage_provenance(root,sid,"08",[],{},[],"NA",metrics); return "NA",metrics,[]
    sess=sessions_df(root); order={str(x):i for i,x in enumerate(sess.session_id.astype(str))}
    cur=pd.read_csv(stage_dir(root,sid,"02")/"per_roi_qc.csv"); curim=np.load(stage_dir(root,sid,"01")/"mean_image.npy")
    params=cfg(root).get("identity",{}); maxdist=float(params.get("max_distance_px",12.0)); patch_radius=int(params.get("patch_radius_px",10))
    cand=[]
    for _,t in pd.read_csv(tr).iterrows():
        tsid=str(t.target_session)
        if order.get(tsid,-1)<=order.get(sid,-1): continue
        tp=stage_dir(root,tsid,"02")/"per_roi_qc.csv"; tip=stage_dir(root,tsid,"01")/"mean_image.npy"
        if not tp.exists() or not tip.exists(): continue
        tar=pd.read_csv(tp); tarim=np.load(tip)
        sx=cur.x.to_numpy(float)+float(t.dx); sy=cur.y.to_numpy(float)+float(t.dy)
        tx=tar.x.to_numpy(float); ty=tar.y.to_numpy(float)
        D=np.sqrt((sy[:,None]-ty[None,:])**2+(sx[:,None]-tx[None,:])**2)
        src_near=np.argmin(D,axis=1); tgt_near=np.argmin(D,axis=0)
        for i,r in cur.reset_index(drop=True).iterrows():
            j=int(src_near[i]); dd=float(D[i,j])
            if not np.isfinite(dd) or dd>maxdist: continue
            q=tar.iloc[j]; sr=int(r.roi_id); trgt=int(q.roi_id)
            reciprocal=bool(tgt_near[j]==i)
            ar=float(q.area_px)/float(r.area_px) if float(r.area_px)>0 else np.nan
            lc=local_patch_corr(curim,tarim,float(r.x),float(r.y),float(q.x),float(q.y),patch_radius)
            cand.append({"candidate_id":f"{sid}:{sr}->{tsid}:{trgt}","source_session":sid,"source_roi":sr,"target_session":tsid,"target_roi":trgt,
                         "distance_px":dd,"reciprocal_nearest":reciprocal,"area_ratio":ar,"local_corr":lc,
                         "source_morphology_pass":bool(r.morphology_pass),"target_morphology_pass":bool(q.morphology_pass),
                         "review_status":"REVIEW_REQUIRED"})
    out=pd.DataFrame(cand)
    if len(out): out=out.sort_values(["target_session","distance_px","source_roi"]).reset_index(drop=True)
    out.to_csv(d/"identity_candidates.csv",index=False)
    if not len(out):
        metrics={"reason":"no forward candidate within distance gate","max_distance_px":maxdist}
        write_stage_provenance(root,sid,"08",[tr],params,[d/"identity_candidates.csv"],"NA",metrics)
        return "NA",metrics,[d/"identity_candidates.csv"]
    metrics={"n_candidates":len(out),"n_reciprocal":int(out.reciprocal_nearest.sum()),"max_distance_px":maxdist,"independent_review_required":True}
    write_stage_provenance(root,sid,"08",[tr],{"rule":"forward-session nearest centroid + reciprocal/area/local-corr evidence; candidate only",**params},[d/"identity_candidates.csv"],"REVIEW_REQUIRED",metrics,"Automatic candidates are not frozen identity.")
    return "REVIEW_REQUIRED",metrics,[d/"identity_candidates.csv"]

def run_09(root,sid,row):
    d=stage_dir(root,sid,"09"); d.mkdir(parents=True,exist_ok=True); per=pd.read_csv(stage_dir(root,sid,"06")/"per_roi.csv"); trial=pd.read_parquet(stage_dir(root,sid,"06")/"trial_roi.parquet"); conds=list(pd.unique(trial.condition)); metrics={"n_roi":int((per.qc_status=="PASS").sum()),"n_conditions":len(conds)}
    if len(conds)==2:
        w="late" if "late" in trial.window.unique() else trial.window.iloc[0]; x=trial[trial.window==w].pivot(index="trial_id",columns="roi_id",values="response"); c=trial[trial.window==w].drop_duplicates("trial_id").set_index("trial_id").loc[x.index,"condition"]; a=x[c==conds[0]].to_numpy(); b=x[c==conds[1]].to_numpy(); d2=float(np.nansum((np.nanmean(b,0)-np.nanmean(a,0))**2)); metrics["centroid_d2"]=d2; data={"window":w,"condition_a":str(conds[0]),"condition_b":str(conds[1]),"centroid_d2":d2,"n_roi":x.shape[1]}
    else: data={"n_conditions":len(conds),"note":"generic population inference skipped: need two conditions"}
    jdump(d/"population_summary.json",data); write_stage_provenance(root,sid,"09",[stage_dir(root,sid,"06")/"per_roi.csv",stage_dir(root,sid,"06")/"trial_roi.parquet"],{"generic_analysis":"centroid geometry"},[d/"population_summary.json"],"PASS",metrics); return "PASS",metrics,[d/"population_summary.json"]

def run_10(root,sid,row):
    d=stage_dir(root,sid,"10"); d.mkdir(parents=True,exist_ok=True); st=read_state(root,sid); files=[]
    for sg in STAGES:
        sd=stage_dir(root,sid,sg)
        if sd.exists(): files.extend([p for p in sd.rglob("*") if p.is_file() and p.name!="release_manifest.csv"])
    rows=[{"path":str(p.relative_to(root)),"size":p.stat().st_size,"sha256":sha256(p) if p.stat().st_size<2_000_000_000 else ""} for p in files]; pd.DataFrame(rows).to_csv(d/"release_manifest.csv",index=False)
    stage_status={k:v["status"] for k,v in st["stages"].items()}; stage_status["10"]="PASS"
    jdump(d/"session_report.json",{"dataset_id":cfg(root)["dataset_id"],"session_id":sid,"animal":str(row.get("animal","")),"day":str(row.get("day","")),"task":str(row.get("task","")),"tool_version":TOOL_VERSION,"frozen_at":now(),"stage_status":stage_status})
    metrics={"n_hashed_files":len(rows)}; write_stage_provenance(root,sid,"10",[stage_dir(root,sid,"06")/"per_roi.csv"],{},[d/"release_manifest.csv",d/"session_report.json"],"PASS",metrics); return "PASS",metrics,[d/"release_manifest.csv",d/"session_report.json"]

RUNNERS={"00":run_00,"01":run_01,"02":run_02,"03":run_03,"04":run_04,"05":run_05,"06":run_06,"07":run_07,"08":run_08,"09":run_09,"10":run_10}

def run_stage(root,sid,stage,force=False):
    row=row_for(root,sid); ok,msg=stage_guard(root,sid,stage,force)
    if not ok: print(f"{sid} stage {stage}: SKIP {msg}"); return
    log_stage(root,sid,stage,"RUNNING")
    try:
        status,metrics,outputs=RUNNERS[stage](root,sid,row); log_stage(root,sid,stage,status,"",metrics,outputs); print(f"{sid} stage {stage} {STAGES[stage]['name']}: {status}")
    except Exception as e:
        log_stage(root,sid,stage,"FAIL",f"{type(e).__name__}: {e}"); sd=stage_dir(root,sid,stage); sd.mkdir(parents=True,exist_ok=True); (sd/"error.txt").write_text(f"{type(e).__name__}: {e}\n",encoding="utf-8"); print(f"{sid} stage {stage}: FAIL {e}"); raise
def run_pipeline(root,sessions=None,from_stage="00",to_stage="10",force=False):
    ids=list(sessions_df(root).session_id.astype(str)) if sessions is None else sessions; stages=list(STAGES); a=stages.index(from_stage); b=stages.index(to_stage)
    # Stage-major scheduling is required for cross-day work: every peer must finish Stage01/02
    # before any session attempts Stage07/08.
    for stage in stages[a:b+1]:
        for sid in ids: run_stage(root,sid,stage,force)
def invalidate(root,sid,stage,reason):
    st=read_state(root,sid); affected=[stage]+descendants(stage)
    for sg in affected: st["stages"][sg].update({"status":"INVALID","message":f"invalidated from {stage}: {reason}","updated_at":now()})
    write_state(root,sid,st); d=session_dir(root,sid); d.mkdir(parents=True,exist_ok=True)
    with (d/"invalidation_log.jsonl").open("a",encoding="utf-8") as f: f.write(json.dumps({"timestamp":now(),"from_stage":stage,"affected":affected,"reason":reason},ensure_ascii=False)+"\n")
    print(sid,"invalidated",",".join(affected))
def status(root,sid=None):
    ids=[sid] if sid else list(sessions_df(root).session_id.astype(str)); rows=[]
    for x in ids:
        st=read_state(root,x)
        for sg in STAGES: rows.append({"session_id":x,"stage":sg,"name":STAGES[sg]["name"],"status":st["stages"][sg]["status"],"message":st["stages"][sg].get("message","")})
    df=pd.DataFrame(rows)
    if sid: print(df.to_string(index=False))
    else: print(df.pivot(index="session_id",columns="stage",values="status").to_string())
    return df
def export_roi(root,out=None):
    pieces=[]
    for sid in sessions_df(root).session_id.astype(str):
        p=stage_dir(root,sid,"06")/"per_roi.csv"
        if p.exists(): pieces.append(pd.read_csv(p))
    if not pieces: raise SystemExit("No stage 06 per_roi.csv files")
    allroi=pd.concat(pieces,ignore_index=True); out=Path(out) if out else Path(root)/"exports"/"per_roi_all.csv"; out.parent.mkdir(parents=True,exist_ok=True); allroi.to_csv(out,index=False)
    try: allroi.to_parquet(out.with_suffix(".parquet"),index=False)
    except Exception: pass
    print(out,len(allroi),"ROIs"); return out
def doctor(root):
    rows=[]
    for sid in sessions_df(root).session_id.astype(str):
        st=read_state(root,sid); next_stage=None; blocker=None
        for sg in STAGES:
            s=st["stages"][sg]["status"]
            if s in ("FAIL","INVALID"):
                next_stage=sg; blocker=s+": "+st["stages"][sg].get("message",""); break
            if s=="PENDING":
                deps=STAGES[sg]["deps"]; unmet=[d for d in deps if st["stages"][d]["status"] not in STATUS_OK]
                next_stage=sg; blocker=("waiting for "+",".join(unmet)) if unmet else "ready"; break
        if next_stage is None:
            review=[sg for sg in STAGES if st["stages"][sg]["status"]=="REVIEW_REQUIRED"]
            blocker=("manual review required at "+",".join(review)) if review else "complete"
        rows.append({"session_id":sid,"next_stage":next_stage or "NONE","state":blocker})
    df=pd.DataFrame(rows); print(df.to_string(index=False))
    out=Path(root)/"reports"; out.mkdir(parents=True,exist_ok=True); df.to_csv(out/"doctor.csv",index=False)
    return df

def report(root):
    df=status(root)
    out=Path(root)/"reports"; out.mkdir(parents=True,exist_ok=True)
    df.groupby(["stage","status"]).size().reset_index(name="n").to_csv(out/"stage_status_summary.csv",index=False)
    if any((stage_dir(root,s,"06")/"per_roi.csv").exists() for s in sessions_df(root).session_id.astype(str)):
        export_roi(root,out/"per_roi_all.csv")
    from carma_report import build_project_report
    page=build_project_report(root)
    print(page)
def init_project(dataset_yaml,dest):
    src=Path(dataset_yaml); c=load_yaml(src); dest=Path(dest); dest.mkdir(parents=True,exist_ok=True); sf=(src.parent/Path(c.get("sessions_file","sessions.csv"))).resolve(); shutil.copy2(sf,dest/"sessions.csv"); c["sessions_file"]="sessions.csv"; save_yaml(dest/"dataset.yaml",c)
    for sid in pd.read_csv(dest/"sessions.csv").session_id.astype(str): session_dir(dest,sid).mkdir(parents=True,exist_ok=True); write_state(dest,sid,read_state(dest,sid))
    print("Initialized",dest)

def migrate_existing(outroot):
    base=Path(os.environ.get("CARMA_MASTER_SUMMARY", str(Path(__file__).resolve().parent.parent)))
    wf=base/"CARMA_STANDARDIZED_WORKFLOW_20260926"; authority=wf/"CANONICAL_SESSION_AUTHORITY.csv"; stages=wf/"CURRENT_SESSION_STAGE_STATUS_V2.csv"; cell=base/"GLOBAL_RESULTS_ATLAS_20260924"/"CELL_ACTIVITY_AUTHORITY_20260925"/"CELL_ACTIVITY_AUTHORITY.csv"
    if not authority.exists() or not stages.exists() or not cell.exists():
        raise SystemExit("migrate-existing needs the legacy authority tree; set CARMA_MASTER_SUMMARY to its root")
    outroot=Path(outroot); outroot.mkdir(parents=True,exist_ok=True); a=pd.read_csv(authority,dtype={"animal":str,"day":str}); dup=a.session_id.duplicated(keep=False); a["session_key"]=a.session_id.astype(str); a.loc[dup,"session_key"]=a.loc[dup].session_id.astype(str)+"__"+a.loc[dup].task.astype(str)
    sess=pd.DataFrame({"session_id":a.session_key,"animal":a.animal,"day":a.day,"task":a.task,"analysis_role":a.analysis_tier,"capability":"MIGRATED_AUTHORITY","raw_tiff":"","registered_tiff":"","evt_file":"","behavior_file":"","roi_source":"","frame_rate":np.nan,"legacy_session_id":a.session_id}); sess.to_csv(outroot/"sessions.csv",index=False)
    save_yaml(outroot/"dataset.yaml",{"dataset_id":"current_vta_authority_2026","sessions_file":"sessions.csv","condition_column":"condition","windows":{"cue":[-3,-1],"predictive":[-1,0],"outcome":[0,2],"late":[2,6],"post":[6,9]},"note":"Migrated frozen authority; stage ledger records provenance, not rerun."})
    stold=pd.read_csv(stages,dtype=str); ca=pd.read_csv(cell,dtype={"animal":str,"day":str})
    for _,r in sess.iterrows():
        sid=str(r.session_id); session_dir(outroot,sid).mkdir(parents=True,exist_ok=True); st=read_state(outroot,sid); m=stold[stold.session_key==sid]
        for _,x in m.iterrows():
            sg=str(x.stage).zfill(2); st["stages"][sg]={"name":STAGES[sg]["name"],"status":"MIGRATED","updated_at":now(),"message":str(x.status),"legacy_status":str(x.status)}
        write_state(outroot,sid,st); aa=a[a.session_key==sid].iloc[0]; c=ca[(ca.animal.astype(str)==str(aa.animal))&(ca.day.astype(str)==str(aa.day))&(ca.task.astype(str)==str(aa.task))].copy()
        if len(c):
            d=stage_dir(outroot,sid,"06"); d.mkdir(parents=True,exist_ok=True); out=pd.DataFrame(index=c.index.copy()); out["dataset_id"]="current_vta_authority_2026"; out["session_id"]=sid; out["animal"]=c.animal.astype(str); out["day"]=c.day.astype(str); out["task"]=c.task.astype(str); out["roi_id"]=c.cell_id; out["plane"]=c.get("plane",0); out["x"]=c.get("x",np.nan); out["y"]=c.get("y",np.nan); out["area_px"]=c.get("roi_area",c.get("area",np.nan)); out["edge_touch"]=~c.get("edge_qc_pass",pd.Series(True,index=c.index)).astype(bool); out["morphology_pass"]=c.get("strict",pd.Series(True,index=c.index)).astype(bool); out["trace_snr"]=c.get("median_snr",c.get("roi_snr",np.nan)); out["bg_corr"]=c.get("median_roi_bg_corr",np.nan); out["final_signal_method"]=c.get("final_signal_method",""); out["n_trials"]=c.get("n_trials",np.nan); out["n_conditions"]=np.where(c.task.astype(str).str.contains("_vs_"),2,1)
            mapping={"cue":"cue_z_csplus_minus_csminus","predictive":"trace_beta_trace_5_6","outcome":"outcome_z_csplus_minus_csminus","late":"late_z_csplus_minus_csminus","post":"post_z_csplus_minus_csminus"}
            for k,col in mapping.items(): out[f"{k}_effect"]=c[col] if col in c.columns else np.nan; out[f"{k}_p"]=np.nan
            out["trial_reliability"]=c.get("trial_sign_consistency",np.nan); out["track_id"]=c.get("track_id",""); out["identity_status"]=c.get("identity_layer","NA"); out["qc_status"]=np.where(out["morphology_pass"],"PASS","WARN"); out["exclusion_flags"]=""
            for col in ROI_SCHEMA:
                if col not in out.columns: out[col]=np.nan
            out=out[ROI_SCHEMA]; out.to_csv(d/"per_roi.csv",index=False)
            try: out.to_parquet(d/"per_roi.parquet",index=False)
            except Exception: pass
    export_roi(outroot); report(outroot); print("Migrated",len(sess),"sessions to",outroot)

def make_fixture(dest):
    dest=Path(dest); dest.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(1); n=140; h=w=64; fr=10.0; yy,xx=np.mgrid[0:h,0:w]; centers=[(18,18),(45,20),(32,44),(50,48)]; masks=np.array([((xx-x)**2+(yy-y)**2<=4**2) for x,y in centers]); base=rng.normal(100,2,(n,h,w)).astype(np.float32); event_frames=[25,50,75,100,120]; cond=["A","B","A","B","A"]
    for ri,m in enumerate(masks):
        base[:,m]+=18+ri*3
    for ef,c in zip(event_frames,cond):
        for ri,m in enumerate(masks):
            amp=(2+ri*.7)+(4 if c=="B" and ri in (0,2) else 0)
            for f in range(max(0,ef),min(n,ef+15)): base[f,m]+=amp*np.exp(-(f-ef)/7)
    mov=np.empty_like(base)
    for i,fr0 in enumerate(base): mov[i]=ndimage.shift(fr0,(1.4*np.sin(i/15),1.1*np.cos(i/19)),order=1,mode="nearest",prefilter=False)
    tifffile.imwrite(dest/"raw.tif",mov); pd.DataFrame({"trial_id":np.arange(1,6),"event_frame":event_frames,"event_name":"outcome"}).to_csv(dest/"events.csv",index=False); pd.DataFrame({"trial_id":np.arange(1,6),"condition":cond}).to_csv(dest/"behavior.csv",index=False); pd.DataFrame({"roi_id":[11,24,37,58],"x":[c[0] for c in centers],"y":[c[1] for c in centers],"radius":4}).to_csv(dest/"roi.csv",index=False)
    pd.DataFrame([{"session_id":"SYN_D1","animal":"SYN","day":"D1","task":"A_vs_B","raw_tiff":str((dest/"raw.tif").resolve()),"registered_tiff":"","evt_file":str((dest/"events.csv").resolve()),"behavior_file":str((dest/"behavior.csv").resolve()),"roi_source":str((dest/"roi.csv").resolve()),"analysis_role":"MAIN","capability":"RAW_MOVIE","frame_rate":fr}]).to_csv(dest/"sessions.csv",index=False)
    save_yaml(dest/"dataset.yaml",{"dataset_id":"synthetic_cold_start","sessions_file":"sessions.csv","frame_rate":fr,"condition_column":"condition","registration":{"upsample_factor":10},"roi_qc":{"min_area_px":20,"max_area_px":500,"default_radius_px":4},"extraction":{"neuropil_inner_px":2,"neuropil_outer_px":7,"alpha":0.7},"signal_selection":{"candidate_alphas":[0.0,0.5,0.7,1.0]},"windows":{"cue":[-2,-1],"predictive":[-1,0],"outcome":[0,1],"late":[1,2],"post":[2,3]}})
    print("Fixture",dest)
def cold_test(work):
    work=Path(work)
    if work.exists(): shutil.rmtree(work)
    src=work/"source"; proj=work/"project"; make_fixture(src); init_project(src/"dataset.yaml",proj); run_pipeline(proj,to_stage="10"); export_roi(proj); report(proj)
    per=pd.read_csv(proj/"sessions"/"SYN_D1"/"stage_06"/"per_roi.csv")
    tri=pd.read_parquet(proj/"sessions"/"SYN_D1"/"stage_06"/"trial_roi.parquet")
    expected={11,24,37,58}
    assert len(per)==4 and {"outcome_effect","late_effect","qc_status"}.issubset(per.columns)
    assert set(per.roi_id.astype(int))==expected, f"per_roi ID drift: {set(per.roi_id)}"
    assert set(tri.roi_id.astype(int))==expected, f"trial_roi ID drift: {set(tri.roi_id)}"
    assert (proj/"sessions"/"SYN_D1"/"stage_10"/"release_manifest.csv").exists()
    assert (proj/"reports"/"sessions"/"SYN_D1"/"roi_explorer_data.js").exists()
    print("COLD_TEST_PASS",proj,"ROI_IDS",sorted(expected))

def make_crossday_fixture(dest):
    dest=Path(dest); dest.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(7); n=140; h=w=64; fr=10.0; yy,xx=np.mgrid[0:h,0:w]
    centers1=[(18,18),(45,20),(32,44),(50,48)]; ids1=[11,24,37,58]
    dx,dy=-3,2; centers2=[(x+dx,y+dy) for x,y in centers1]; ids2=[101,205,309,444]
    masks=np.array([((xx-x)**2+(yy-y)**2<=4**2) for x,y in centers1])
    base=rng.normal(100,1.6,(n,h,w)).astype(np.float32); event_frames=[25,50,75,100,120]; cond=["A","B","A","B","A"]
    for ri,m in enumerate(masks): base[:,m]+=22+ri*4
    for ef,c in zip(event_frames,cond):
        for ri,m in enumerate(masks):
            amp=(2.5+ri*.8)+(4.5 if c=="B" and ri in (0,2) else 0)
            for f in range(max(0,ef),min(n,ef+15)): base[f,m]+=amp*np.exp(-(f-ef)/7)
    mov1=np.empty_like(base)
    for i,fr0 in enumerate(base): mov1[i]=ndimage.shift(fr0,(1.2*np.sin(i/15),.9*np.cos(i/19)),order=1,mode="nearest",prefilter=False)
    mov2=np.empty_like(base)
    for i,fr0 in enumerate(base):
        q=ndimage.shift(fr0,(dy+1.0*np.sin(i/17),dx+.8*np.cos(i/21)),order=1,mode="nearest",prefilter=False)
        mov2[i]=q+rng.normal(0,.35,q.shape)
    tifffile.imwrite(dest/"raw_D1.tif",mov1.astype(np.float32)); tifffile.imwrite(dest/"raw_D2.tif",mov2.astype(np.float32))
    pd.DataFrame({"trial_id":np.arange(1,6),"event_frame":event_frames,"event_name":"outcome"}).to_csv(dest/"events.csv",index=False)
    pd.DataFrame({"trial_id":np.arange(1,6),"condition":cond}).to_csv(dest/"behavior.csv",index=False)
    pd.DataFrame({"roi_id":ids1,"x":[c[0] for c in centers1],"y":[c[1] for c in centers1],"radius":4}).to_csv(dest/"roi_D1.csv",index=False)
    pd.DataFrame({"roi_id":ids2,"x":[c[0] for c in centers2],"y":[c[1] for c in centers2],"radius":4}).to_csv(dest/"roi_D2.csv",index=False)
    rows=[]
    for sid,day,movie,roi in [("SYN_D1","D1","raw_D1.tif","roi_D1.csv"),("SYN_D2","D2","raw_D2.tif","roi_D2.csv")]:
        rows.append({"session_id":sid,"animal":"SYN","day":day,"task":"A_vs_B","raw_tiff":str((dest/movie).resolve()),"registered_tiff":"","evt_file":str((dest/"events.csv").resolve()),"behavior_file":str((dest/"behavior.csv").resolve()),"roi_source":str((dest/roi).resolve()),"analysis_role":"MAIN","capability":"RAW_MOVIE","frame_rate":fr})
    pd.DataFrame(rows).to_csv(dest/"sessions.csv",index=False)
    save_yaml(dest/"dataset.yaml",{"dataset_id":"synthetic_crossday","sessions_file":"sessions.csv","frame_rate":fr,"condition_column":"condition","registration":{"upsample_factor":10},"roi_qc":{"min_area_px":20,"max_area_px":500,"default_radius_px":4},"extraction":{"neuropil_inner_px":2,"neuropil_outer_px":7,"alpha":0.7},"signal_selection":{"candidate_alphas":[0.0,0.5,0.7,1.0]},"identity":{"max_distance_px":6.0,"patch_radius_px":10},"windows":{"cue":[-2,-1],"predictive":[-1,0],"outcome":[0,1],"late":[1,2],"post":[2,3]}})
    return {"expected_pairs":list(zip(ids1,ids2)),"expected_shift":[dy,dx]}

def crossday_test(work):
    work=Path(work)
    if work.exists(): shutil.rmtree(work)
    src=work/"source"; proj=work/"project"; truth=make_crossday_fixture(src); init_project(src/"dataset.yaml",proj); run_pipeline(proj,to_stage="10")
    tr=pd.read_csv(proj/"sessions"/"SYN_D1"/"stage_07"/"crossday_transforms.csv")
    c=pd.read_csv(proj/"sessions"/"SYN_D1"/"stage_08"/"identity_candidates.csv")
    got={(int(r.source_roi),int(r.target_roi)) for _,r in c.iterrows()}
    expected=set(tuple(x) for x in truth["expected_pairs"])
    assert got==expected, f"cross-day candidate mismatch: got={got} expected={expected}"
    assert c.reciprocal_nearest.astype(bool).all(), "expected reciprocal-nearest candidates"
    assert float(c.distance_px.max())<3.0, f"candidate distance too large: {c.distance_px.max()}"
    assert read_state(proj,"SYN_D1")["stages"]["08"]["status"]=="REVIEW_REQUIRED"
    assert read_state(proj,"SYN_D2")["stages"]["08"]["status"]=="NA"
    decisions={"timestamp":now(),"decisions":[{"candidate_id":x,"decision":"ACCEPT"} for x in c.candidate_id.astype(str)]}
    a=work/"reviewA.json"; b=work/"reviewB.json"; jdump(a,decisions); jdump(b,decisions)
    identity_review_import(proj,"SYN_D1","reviewerA",a); identity_review_import(proj,"SYN_D1","reviewerB",b); identity_consensus(proj,"SYN_D1",2)
    cons=pd.read_csv(proj/"sessions"/"SYN_D1"/"stage_08"/"identity_consensus.csv")
    assert len(cons)==4 and (cons.consensus=="ACCEPT").all() and not cons.one_to_one_conflict.astype(bool).any()
    assert read_state(proj,"SYN_D1")["stages"]["09"]["status"]=="INVALID" and read_state(proj,"SYN_D1")["stages"]["10"]["status"]=="INVALID"
    run_pipeline(proj,["SYN_D1"],from_stage="09",to_stage="10")
    assert read_state(proj,"SYN_D1")["stages"]["09"]["status"]=="PASS" and read_state(proj,"SYN_D1")["stages"]["10"]["status"]=="PASS"
    report(proj)
    print("CROSSDAY_TEST_PASS","transform",tr[["dy","dx","registered_image_corr"]].to_dict("records"),"pairs",sorted(got),"release_refrozen",True)

def canonical_identity_candidates(cand):
    cand=cand.copy()
    aliases={"src_session":"source_session","src_roi":"source_roi","tgt_session":"target_session","tgt_roi":"target_roi"}
    for old,new in aliases.items():
        if new not in cand.columns and old in cand.columns: cand=cand.rename(columns={old:new})
    need=["source_session","source_roi","target_session","target_roi"]
    miss=[x for x in need if x not in cand.columns]
    if miss: raise SystemExit("Identity candidate table missing columns: "+",".join(miss))
    if "candidate_id" not in cand.columns:
        cand["candidate_id"]=cand.apply(lambda r:f"{r.source_session}:{int(r.source_roi)}->{r.target_session}:{int(r.target_roi)}",axis=1)
    return cand

def identity_review_import(root,sid,reviewer,decisions_file):
    d=stage_dir(root,sid,"08"); candp=d/"identity_candidates.csv"
    if not candp.exists(): raise SystemExit(f"No Stage08 candidates for {sid}")
    cand=canonical_identity_candidates(pd.read_csv(candp))
    cand.to_csv(candp,index=False)
    obj=jload(decisions_file,{})
    if not isinstance(obj,dict) or "decisions" not in obj: raise SystemExit("Review JSON requires decisions[]")
    reviewer=str(reviewer).strip()
    if not reviewer: raise SystemExit("reviewer cannot be empty")
    allowed={"ACCEPT","REJECT","UNCERTAIN","UNREVIEWED"}
    dec={str(x["candidate_id"]):str(x.get("decision","UNREVIEWED")).upper() for x in obj["decisions"]}
    unknown=set(dec)-set(cand.candidate_id.astype(str))
    if unknown: raise SystemExit("Unknown candidate IDs: "+",".join(sorted(unknown)[:10]))
    out=cand[["candidate_id","source_session","source_roi","target_session","target_roi"]].copy()
    out["decision"]=out.candidate_id.astype(str).map(dec).fillna("UNREVIEWED")
    bad=sorted(set(out.decision)-allowed)
    if bad: raise SystemExit("Invalid decisions: "+",".join(bad))
    out["reviewer"]=reviewer; out["reviewed_at"]=obj.get("timestamp",now())
    rd=d/"reviews"; rd.mkdir(parents=True,exist_ok=True)
    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",reviewer)
    path=rd/f"{safe}.csv"; out.to_csv(path,index=False)
    print("IMPORTED",reviewer,len(out),"decisions ->",path)
    return path

def identity_consensus(root,sid,min_reviewers=2):
    d=stage_dir(root,sid,"08"); candp=d/"identity_candidates.csv"
    if not candp.exists(): raise SystemExit(f"No Stage08 candidates for {sid}")
    cand=canonical_identity_candidates(pd.read_csv(candp))
    reviews=list((d/"reviews").glob("*.csv")) if (d/"reviews").exists() else []
    if len(reviews)<min_reviewers: raise SystemExit(f"Need >= {min_reviewers} independent reviewer files; found {len(reviews)}")
    R=pd.concat([pd.read_csv(p) for p in reviews],ignore_index=True)
    if R.reviewer.astype(str).nunique()<min_reviewers: raise SystemExit("Reviewer names are not independent")
    rows=[]
    for _,c in cand.iterrows():
        q=R[R.candidate_id.astype(str)==str(c.candidate_id)]
        useful=q[q.decision.isin(["ACCEPT","REJECT","UNCERTAIN"])]
        counts=useful.decision.value_counts().to_dict()
        na=int(counts.get("ACCEPT",0)); nr=int(counts.get("REJECT",0)); nu=int(counts.get("UNCERTAIN",0))
        nrev=int(useful.reviewer.astype(str).nunique())
        if nrev<min_reviewers: cons="UNRESOLVED"
        elif na>=min_reviewers and nr==0: cons="ACCEPT"
        elif nr>=min_reviewers and na==0: cons="REJECT"
        else: cons="CONFLICT"
        rec=c.to_dict(); rec.update({"n_reviewers":nrev,"n_accept":na,"n_reject":nr,"n_uncertain":nu,"consensus":cons})
        rows.append(rec)
    out=pd.DataFrame(rows)
    # one-to-one integrity within each source-target session pair
    out["one_to_one_conflict"]=False
    acc=out[out.consensus=="ACCEPT"].copy()
    for (ss,ts),g in acc.groupby(["source_session","target_session"]):
        bad_src=set(g.loc[g.source_roi.duplicated(keep=False),"source_roi"])
        bad_tgt=set(g.loc[g.target_roi.duplicated(keep=False),"target_roi"])
        m=(out.source_session==ss)&(out.target_session==ts)&((out.source_roi.isin(bad_src))|(out.target_roi.isin(bad_tgt)))&(out.consensus=="ACCEPT")
        out.loc[m,"one_to_one_conflict"]=True
        out.loc[m,"consensus"]="CONFLICT"
    outp=d/"identity_consensus.csv"; out.to_csv(outp,index=False)
    frozen=out[out.consensus=="ACCEPT"].copy()
    frozen.to_csv(d/"identity_edges_frozen.csv",index=False)
    unresolved=int(out.consensus.isin(["UNRESOLVED","CONFLICT"]).sum())
    status08="PASS" if unresolved==0 else "REVIEW_REQUIRED"
    metrics={"n_candidates":len(out),"n_accepted":int((out.consensus=="ACCEPT").sum()),"n_rejected":int((out.consensus=="REJECT").sum()),"n_unresolved":unresolved,"n_reviewers":int(R.reviewer.astype(str).nunique()),"one_to_one_conflicts":int(out.one_to_one_conflict.sum())}
    log_stage(root,sid,"08",status08,"independent reviewer consensus",metrics,[outp,d/"identity_edges_frozen.csv"])
    # Stage09/10 may have been produced before manual review; refresh downstream release state.
    st=read_state(root,sid)
    for sg in ["09","10"]:
        if st["stages"][sg]["status"] in STATUS_OK:
            st["stages"][sg].update({"status":"INVALID","message":"Stage08 reviewer consensus changed; rerun downstream","updated_at":now()})
    write_state(root,sid,st)
    print("CONSENSUS",sid,status08,metrics)
    return outp


def main():
    ap=argparse.ArgumentParser(prog="carma",description="CaRMA 2P Tool V1"); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("init"); p.add_argument("dataset_yaml"); p.add_argument("dest")
    p=sp.add_parser("run"); p.add_argument("project"); p.add_argument("--session",action="append"); p.add_argument("--from-stage",default="00"); p.add_argument("--to-stage",default="10"); p.add_argument("--force",action="store_true")
    p=sp.add_parser("resume"); p.add_argument("project"); p.add_argument("--session",action="append")
    p=sp.add_parser("status"); p.add_argument("project"); p.add_argument("--session")
    p=sp.add_parser("invalidate"); p.add_argument("project"); p.add_argument("--session",required=True); p.add_argument("--stage",required=True); p.add_argument("--reason",required=True)
    p=sp.add_parser("report"); p.add_argument("project")
    p=sp.add_parser("doctor"); p.add_argument("project")
    p=sp.add_parser("export-roi"); p.add_argument("project"); p.add_argument("--out")
    p=sp.add_parser("migrate-existing"); p.add_argument("dest")
    p=sp.add_parser("make-fixture"); p.add_argument("dest")
    p=sp.add_parser("cold-test"); p.add_argument("work")
    p=sp.add_parser("crossday-test"); p.add_argument("work")
    p=sp.add_parser("identity-review-import"); p.add_argument("project"); p.add_argument("--session",required=True); p.add_argument("--reviewer",required=True); p.add_argument("--decisions",required=True)
    p=sp.add_parser("identity-consensus"); p.add_argument("project"); p.add_argument("--session",required=True); p.add_argument("--min-reviewers",type=int,default=2)
    a=ap.parse_args()
    if a.cmd=="init": init_project(a.dataset_yaml,a.dest)
    elif a.cmd=="run": run_pipeline(project_root(a.project),a.session,a.from_stage.zfill(2),a.to_stage.zfill(2),a.force)
    elif a.cmd=="resume": run_pipeline(project_root(a.project),a.session)
    elif a.cmd=="status": status(project_root(a.project),a.session)
    elif a.cmd=="invalidate": invalidate(project_root(a.project),a.session,a.stage.zfill(2),a.reason)
    elif a.cmd=="report": report(project_root(a.project))
    elif a.cmd=="doctor": doctor(project_root(a.project))
    elif a.cmd=="export-roi": export_roi(project_root(a.project),a.out)
    elif a.cmd=="migrate-existing": migrate_existing(a.dest)
    elif a.cmd=="make-fixture": make_fixture(a.dest)
    elif a.cmd=="cold-test": cold_test(a.work)
    elif a.cmd=="crossday-test": crossday_test(a.work)
    elif a.cmd=="identity-review-import": identity_review_import(project_root(a.project),a.session,a.reviewer,a.decisions)
    elif a.cmd=="identity-consensus": identity_consensus(project_root(a.project),a.session,a.min_reviewers)
if __name__=="__main__": main()
