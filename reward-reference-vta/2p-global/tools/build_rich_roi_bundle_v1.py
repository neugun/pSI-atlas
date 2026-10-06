from __future__ import annotations
import argparse, base64, hashlib, io, json, os, re
from pathlib import Path
import numpy as np
import pandas as pd
import tifffile
from PIL import Image, ImageDraw

SCHEMA="CARMA_RICH_ROI_BUNDLE_V1"

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()

def png_uri(arr, mask=None, box=None):
    a=np.asarray(arr, float)
    lo,hi=np.nanpercentile(a,[1,99.5])
    if not np.isfinite(lo): lo=0.0
    if not np.isfinite(hi) or hi<=lo: hi=lo+1.0
    g=np.clip((a-lo)/(hi-lo)*255,0,255).astype(np.uint8)
    im=Image.fromarray(g,"L").convert("RGB")
    if mask is not None:
        m=np.asarray(mask,bool)
        edge=m.copy()
        edge[1:-1,1:-1] &= ~(
            m[:-2,1:-1] & m[2:,1:-1] & m[1:-1,:-2] & m[1:-1,2:]
        )
        pix=np.asarray(im).copy()
        pix[edge]=[210,45,45]
        im=Image.fromarray(pix)
    if box is not None:
        x0,y0,x1,y1=box
        im=im.crop((x0,y0,x1,y1))
    buf=io.BytesIO(); im.save(buf,format="PNG",optimize=True)
    return "data:image/png;base64,"+base64.b64encode(buf.getvalue()).decode("ascii")

def find_labels(session_dir: Path, explicit: str|None):
    if explicit: return Path(explicit)
    cands=sorted(session_dir.glob("*population_labels.tif"))
    if not cands: cands=sorted(session_dir.glob("*labels*.tif"))
    if not cands: raise FileNotFoundError("population labels TIFF not found")
    return cands[0]

def find_csv(session_dir: Path, explicit: str|None, pats):
    if explicit: return Path(explicit)
    for pat in pats:
        cands=sorted(session_dir.glob(pat))
        if cands: return cands[0]
    return None

def ref_for_plane(refs_dir: Path|None, plane_1based: int):
    if refs_dir is None or not refs_dir.exists(): return None
    pats=[f"*S{plane_1based}_Avg.tif",f"*S{plane_1based}*.tif"]
    for pat in pats:
        c=sorted(refs_dir.glob(pat))
        if c: return c[0]
    return None

def down(v, n=192):
    v=np.asarray(v,float)
    if len(v)<=n: return v
    idx=np.linspace(0,len(v)-1,n).round().astype(int)
    return v[idx]

def finite_list(v, nd=5):
    out=[]
    for x in np.asarray(v).ravel():
        xf=float(x)
        out.append(None if not np.isfinite(xf) else round(xf,nd))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--session-dir", required=True)
    ap.add_argument("--session-id", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--checkpoints-dir")
    ap.add_argument("--roi-qc")
    ap.add_argument("--trial-metrics")
    ap.add_argument("--cell-models")
    ap.add_argument("--refs-dir")
    ap.add_argument("--out", required=True)
    a=ap.parse_args()

    sd=Path(a.session_dir)
    labels_p=find_labels(sd,a.labels)
    ck=Path(a.checkpoints_dir) if a.checkpoints_dir else sd/"population_checkpoints"
    roi_p=find_csv(sd,a.roi_qc,["*population_roi_qc.csv","*roi_qc.csv"])
    tr_p=find_csv(sd,a.trial_metrics,["*population_trial_metrics.csv","*trial_metrics.csv"])
    model_p=find_csv(sd,a.cell_models,["*population_cell_models.csv","*cell_models.csv"])
    refs=Path(a.refs_dir) if a.refs_dir else (sd/"refs")

    files=sorted(ck.glob("T*.npz"), key=lambda p:int(re.findall(r"\d+",p.stem)[-1]))
    if not files: raise FileNotFoundError(f"no T*.npz in {ck}")
    zs=[np.load(f,allow_pickle=True) for f in files]
    ids=np.asarray(zs[0]["ids"]).astype(int)
    for f,z in zip(files,zs):
        if not np.array_equal(np.asarray(z["ids"]).astype(int),ids):
            raise RuntimeError(f"ROI ids differ in {f.name}")
    labels=tifffile.imread(labels_p)
    if labels.ndim==2: labels=labels[None,...]
    roi_qc=pd.read_csv(roi_p) if roi_p else pd.DataFrame()
    trials=pd.read_csv(tr_p) if tr_p else pd.DataFrame()
    models=pd.read_csv(model_p) if model_p else pd.DataFrame()

    idcol=next((c for c in roi_qc.columns if c.lower().endswith("_id") or c.lower()=="roi_id"),None)
    tidcol=next((c for c in trials.columns if c.lower().endswith("_id") or c.lower()=="roi_id"),None)
    midcol=next((c for c in models.columns if c.lower().endswith("_id") or c.lower()=="roi_id"),None)

    plane_items=[]
    for pi in range(labels.shape[0]):
        rp=ref_for_plane(refs,pi+1)
        ref=tifffile.imread(rp) if rp else (labels[pi]>0).astype(np.uint8)
        if ref.ndim>2: ref=np.squeeze(ref)
        plane_items.append({
            "plane":pi+1,
            "roi_count":int(len(np.unique(labels[pi]))-1),
            "reference_name":rp.name if rp else None,
            "image_png":png_uri(ref,labels[pi]>0),
        })

    common_t=np.nanmedian(np.stack([np.asarray(z["time_s"],float) for z in zs]),axis=(0,1))
    roi_items=[]
    for j,rid in enumerate(ids):
        loc=np.argwhere(labels==rid)
        if len(loc):
            pi=int(np.median(loc[:,0])); yy=loc[:,1]; xx=loc[:,2]
            cx=float(np.mean(xx)); cy=float(np.mean(yy))
            pad=48
            x0=max(0,int(round(cx))-pad); x1=min(labels.shape[2],int(round(cx))+pad)
            y0=max(0,int(round(cy))-pad); y1=min(labels.shape[1],int(round(cy))+pad)
            rp=ref_for_plane(refs,pi+1)
            ref=tifffile.imread(rp) if rp else (labels[pi]>0).astype(np.uint8)
            ref=np.squeeze(ref)
            mask=labels[pi]==rid
            crop_png=png_uri(ref,mask,(x0,y0,x1,y1))
            plane=pi+1
        else:
            crop_png=None; plane=None; cx=cy=None

        raw=np.stack([np.asarray(z["raw"],float)[j] for z in zs])
        bg=np.stack([np.asarray(z["bg"],float)[j] for z in zs])
        sub=np.stack([np.asarray(z["sub"],float)[j] for z in zs])
        q={}
        if idcol:
            rr=roi_qc.loc[roi_qc[idcol].astype(str)==str(rid)]
            if len(rr): q={k:(None if pd.isna(v) else (float(v) if isinstance(v,(np.floating,float)) else int(v) if isinstance(v,(np.integer,int)) else str(v))) for k,v in rr.iloc[0].items()}
        tm=[]
        if tidcol:
            rr=trials.loc[trials[tidcol].astype(str)==str(rid)]
            for _,row in rr.iterrows():
                tm.append({k:(None if pd.isna(v) else (float(v) if isinstance(v,(np.floating,float)) else int(v) if isinstance(v,(np.integer,int)) else str(v))) for k,v in row.items()})
        mm=[]
        if midcol:
            rr=models.loc[models[midcol].astype(str)==str(rid)]
            for _,row in rr.iterrows():
                mm.append({k:(None if pd.isna(v) else (float(v) if isinstance(v,(np.floating,float)) else int(v) if isinstance(v,(np.integer,int)) else str(v))) for k,v in row.items()})
        roi_items.append({
            "roi_id":int(rid),"plane":plane,"x":cx,"y":cy,
            "mask_png":crop_png,"qc":q,"models":mm,"trial_metrics":tm,
            "mean_raw":finite_list(np.nanmean(raw,axis=0)),
            "mean_bg":finite_list(np.nanmean(bg,axis=0)),
            "mean_sub":finite_list(np.nanmean(sub,axis=0)),
            "heatmap_sub":[finite_list(r) for r in sub],
        })

    trial_meta=[]
    if len(trials):
        cols=[c for c in ["trial","condition","cond100","nlick","trial_z"] if c in trials.columns]
        if "trial" in cols:
            for trial,g in trials.groupby("trial",sort=True):
                row=g.iloc[0]
                trial_meta.append({c:(None if pd.isna(row[c]) else (float(row[c]) if isinstance(row[c],(np.floating,float)) else int(row[c]) if isinstance(row[c],(np.integer,int)) else str(row[c]))) for c in cols})

    src=[labels_p]+files
    for p in [roi_p,tr_p,model_p]:
        if p: src.append(p)
    bundle={
        "schema":SCHEMA,"session_id":a.session_id,
        "n_roi":int(len(ids)),"n_trials":int(len(files)),"n_timepoints":int(len(common_t)),
        "time_s":finite_list(common_t),
        "trial_meta":trial_meta,"planes":plane_items,"rois":roi_items,
        "source_manifest":[{"name":p.name,"bytes":p.stat().st_size,"sha256":sha256(p)} for p in src],
        "privacy":"LOCAL_PRIVATE_BUNDLE_DO_NOT_COMMIT_RAW_TRACES_OR_MASKS"
    }
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(bundle,separators=(",",":")),encoding="utf-8")
    print(json.dumps({"out":str(out),"schema":SCHEMA,"session_id":a.session_id,"n_roi":len(ids),"n_trials":len(files),"bytes":out.stat().st_size},indent=2))

if __name__=="__main__":
    main()
