from __future__ import annotations
from pathlib import Path
import argparse, json, math
import numpy as np

def _safe_norm(v, eps=1e-6):
    n=np.linalg.norm(v,axis=-1,keepdims=True)
    return v/np.maximum(n,eps)

def egocentric_features(keypoints, fps=30.0):
    """
    keypoints: [T,N,K,2], assumed K contains at least nose, ears/body center/tailbase when dataset mapping supplies them.
    Returns simple self centers + velocities; dataset-specific adapters should append mapped body features.
    """
    x=np.asarray(keypoints,float)
    center=np.nanmean(x,axis=2)
    vel=np.diff(center,axis=0,prepend=center[:1])*fps
    speed=np.linalg.norm(vel,axis=-1)
    return {"center":center,"velocity":vel,"speed":speed}

def pair_geometry(center, heading=None):
    """Directed i->j geometry: [T,N,N,F]."""
    c=np.asarray(center,float)
    rel=c[:,:,None,:]-c[:,None,:,:]      # target? construct source i -> target j below
    rel=-rel
    dist=np.linalg.norm(rel,axis=-1)
    unit=_safe_norm(rel)
    feats=[dist[...,None],unit]
    if heading is not None:
        h=_safe_norm(np.asarray(heading,float))
        hi=h[:,:,None,:]
        hj=h[:,None,:,:]
        facing=(hi*unit).sum(-1)[...,None]
        mutual=(hj*(-unit)).sum(-1)[...,None]
        feats += [facing,mutual]
    return np.concatenate(feats,axis=-1)

def build_soelike_event_contract(action_observe, outcome, demfeed=None):
    outcome=np.asarray(outcome).astype(str)
    action=np.asarray(action_observe).astype(int)
    names=np.array(["other","observe","unrewarded","active","passive"],object)
    pre=np.where(action>0,1,0)
    post=np.where(outcome=="active",3,np.where(outcome=="passive",4,2))
    content=np.zeros(len(action),dtype=np.int64)
    if demfeed is not None:
        content=np.where(np.asarray(demfeed).astype(float)>0,1,0)
    return {"pre_event":pre,"post_event":post,"event_names":names.tolist(),"social_content":content}

def inspect_multifiber_mat(path: Path):
    """
    Supports either HDF5 MAT v7.3 or classic MAT. It intentionally returns structure/QC first;
    data-specific flattening is performed only after verifying actual field layout.
    """
    report={"path":str(path),"size_bytes":path.stat().st_size}
    try:
        import h5py
        if h5py.is_hdf5(path):
            report["mat_format"]="hdf5/v7.3"
            with h5py.File(path,"r") as f:
                report["root_keys"]=list(f.keys())
                def walk(g,prefix="",depth=0):
                    rows=[]
                    if depth>3:return rows
                    for k in g.keys():
                        o=g[k]; name=f"{prefix}/{k}"
                        if hasattr(o,"shape"): rows.append({"path":name,"shape":list(o.shape),"dtype":str(o.dtype)})
                        if hasattr(o,"keys"): rows += walk(o,name,depth+1)
                    return rows
                report["datasets"]=walk(f)[:500]
            return report
    except Exception as e:
        report["h5_error"]=repr(e)
    try:
        from scipy.io import whosmat, loadmat
        report["mat_format"]="classic"
        report["variables"]=[{"name":n,"shape":list(s),"class":c} for n,s,c in whosmat(path)]
        # Load only after whosmat succeeds; Raw is expected from the data authority.
        d=loadmat(path,squeeze_me=True,struct_as_record=False)
        report["loaded_keys"]=[k for k in d.keys() if not k.startswith("__")]
        raw=d.get("Raw")
        if raw is not None:
            report["raw_fields"]=list(getattr(raw,"_fieldnames",[]) or [])
        return report
    except Exception as e:
        report["classic_error"]=repr(e)
    return report

def validate_canonical(batch):
    req=["time","agent_mask","identity_id","self_state","pair_state","context","intervention_id","focal_agent"]
    missing=[k for k in req if k not in batch]
    if missing: raise ValueError(f"missing required keys: {missing}")
    B,T,N=batch["agent_mask"].shape
    assert batch["self_state"].shape[:3]==(B,T,N)
    assert batch["pair_state"].shape[:4]==(B,T,N,N)
    assert batch["time"].shape==(B,T)
    assert batch["identity_id"].shape==(B,T,N)
    assert batch["context"].shape[:2]==(B,T)
    assert batch["intervention_id"].shape==(B,T)
    assert batch["focal_agent"].shape==(B,T)
    return {"B":B,"T":T,"N":N,"self_dim":batch["self_state"].shape[-1],"pair_dim":batch["pair_state"].shape[-1]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--inspect-multifiber",type=Path)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()
    if args.inspect_multifiber:
        r=inspect_multifiber_mat(args.inspect_multifiber)
        text=json.dumps(r,indent=2,ensure_ascii=False)
        if args.out:
            args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(text,encoding="utf-8")
        print(text)

if __name__=="__main__":
    main()
