from __future__ import annotations
from pathlib import Path
import argparse, json, zipfile
import numpy as np

IMAGE_W, IMAGE_H = 1024.0, 570.0
KEYPOINTS = ["nose","left_ear","right_ear","neck","left_hip","right_hip","tail_base"]

def _norm(v, eps=1e-6):
    return v/np.maximum(np.linalg.norm(v,axis=-1,keepdims=True),eps)

def canonicalize(kp, scores, fps=30.0):
    # Official CalMS21: [F, mouse, xy, bodypart] -> [F,N,K,2]
    kp=np.asarray(kp,np.float32).transpose(0,1,3,2)
    sc=np.asarray(scores,np.float32)
    F,N,K,_=kp.shape
    body=kp[:,:,[3,4,5,6]].mean(2)
    nose=kp[:,:,0]
    neck=kp[:,:,3]
    tail=kp[:,:,6]
    heading=_norm(nose-neck)
    perp=np.stack([-heading[...,1],heading[...,0]],axis=-1)
    rel=kp-body[:,:,None,:]
    ego_x=(rel*heading[:,:,None,:]).sum(-1)
    ego_y=(rel*perp[:,:,None,:]).sum(-1)
    scale=np.linalg.norm(nose-tail,axis=-1)
    scale_safe=np.maximum(scale,1.0)
    ego=np.stack([ego_x/scale_safe[:,:,None],ego_y/scale_safe[:,:,None]],axis=-1)
    vel=np.diff(body,axis=0,prepend=body[:1])*fps
    speed=np.linalg.norm(vel,axis=-1)
    conf_mean=sc.mean(-1)
    center_norm=np.stack([body[...,0]/IMAGE_W,body[...,1]/IMAGE_H],axis=-1)
    self_state=np.concatenate([
        ego.reshape(F,N,-1),
        center_norm,
        vel/100.0,
        speed[...,None]/100.0,
        heading,
        (scale/100.0)[...,None],
        conf_mean[...,None]
    ],axis=-1).astype(np.float32)

    # directed source i -> target j
    src=body[:,:, :,None] if False else None
    pair=np.zeros((F,N,N,12),np.float32)
    for i in range(N):
        for j in range(N):
            relc=body[:,j]-body[:,i]
            dist=np.linalg.norm(relc,axis=-1)
            u=_norm(relc)
            approach=np.r_[0, -np.diff(dist)]*fps
            nn=np.linalg.norm(nose[:,i]-nose[:,j],axis=-1)
            nt=np.linalg.norm(nose[:,i]-tail[:,j],axis=-1)
            pair[:,i,j]=np.column_stack([
                dist/100.0,u,
                (heading[:,i]*u).sum(-1),
                (heading[:,j]*(-u)).sum(-1),
                approach/100.0,
                nn/100.0,nt/100.0,
                speed[:,j]/100.0,
                conf_mean[:,i],conf_mean[:,j],
                np.ones(F,np.float32)
            ])
    return self_state,pair,kp,sc

def load_json_from_zip(zpath):
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist()
        cal=[n for n in names if Path(n).name.startswith("calms21_") and n.endswith(".json")]
        if not cal: raise RuntimeError("No calms21_*.json found")
        for name in cal:
            with z.open(name) as f:
                yield name,json.load(f)

def iter_sequences(tree):
    for group,seqs in tree.items():
        for sid,d in seqs.items():
            yield group,sid,d

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--zip",type=Path,required=True)
    ap.add_argument("--outdir",type=Path,required=True)
    ap.add_argument("--fps",type=float,default=30.0)
    args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for source,tree in load_json_from_zip(args.zip):
        for group,sid,d in iter_sequences(tree):
            self_state,pair,kp,sc=canonicalize(d["keypoints"],d["scores"],args.fps)
            ann=np.asarray(d.get("annotations",np.full(len(self_state),-1)),np.int64)
            safe=sid.replace("/","__").replace("\\","__")
            out=args.outdir/(safe+".npz")
            np.savez_compressed(out,self_state=self_state,pair_state=pair,
              agent_mask=np.ones(self_state.shape[:2],bool),
              identity_id=np.tile(np.arange(self_state.shape[1],dtype=np.int64),(self_state.shape[0],1)),
              annotations=ann,keypoint_confidence=sc)
            manifest.append({
              "source_file":source,"group":group,"sequence_id":sid,"file":out.name,
              "frames":int(len(self_state)),"n_agents":int(self_state.shape[1]),
              "self_dim":int(self_state.shape[-1]),"pair_dim":int(pair.shape[-1]),
              "annotator_id":d.get("metadata",{}).get("annotator_id",None),
              "vocab":d.get("metadata",{}).get("vocab",None)
            })
    summary={"schema":"social-world-v1","dataset":"CalMS21","n_sequences":len(manifest),
             "total_frames":int(sum(x["frames"] for x in manifest)),"sequences":manifest}
    (args.outdir/"manifest.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="sequences"},indent=2))

if __name__=="__main__":
    main()
