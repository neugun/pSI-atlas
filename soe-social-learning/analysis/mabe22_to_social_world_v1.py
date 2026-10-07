from pathlib import Path
import numpy as np, json, hashlib

SRC=Path(r"H:\brain_world_model_20261005\external_social_data\mabe22_mouse_user_train.npy")
OUT=Path(r"H:\brain_world_model_20261005\external_social_data\mabe22_socialworld")
OUT.mkdir(parents=True,exist_ok=True)
STEP=3

x=np.load(SRC,allow_pickle=True).item()
seqs=x["sequences"]
vocab=x["vocabulary"]

def norm(v,eps=1e-6):
    return v/np.maximum(np.linalg.norm(v,axis=-1,keepdims=True),eps)

def features(kp):
    # kp [T,N,K,2]. Avoid assuming keypoint identity/order beyond consistent indexing.
    kp=np.asarray(kp,np.float32)
    center=kp.mean(2)
    rel=kp-center[:,:,None,:]
    size=np.sqrt(np.mean(np.sum(rel**2,axis=-1),axis=-1))
    scale=np.maximum(size,1.0)
    reln=rel/scale[:,:,None,None]
    vel=np.diff(center,axis=0,prepend=center[:1])
    speed=np.linalg.norm(vel,axis=-1)
    # Full centered shape + translation/dynamics. Coordinates are further standardized during training.
    self_state=np.concatenate([
        reln.reshape(len(kp),kp.shape[1],-1),
        center/1000.0,
        vel/100.0,
        speed[...,None]/100.0,
        (size/100.0)[...,None]
    ],axis=-1).astype(np.float32)
    T,N,_=center.shape
    pair=np.zeros((T,N,N,8),np.float32)
    for i in range(N):
        for j in range(N):
            d=center[:,j]-center[:,i]
            dist=np.linalg.norm(d,axis=-1)
            u=norm(d)
            rv=vel[:,j]-vel[:,i]
            approach=np.r_[0,-np.diff(dist)]
            pair[:,i,j]=np.column_stack([
                dist/100.0,u,rv/100.0,approach/100.0,
                speed[:,i]/100.0,speed[:,j]/100.0
            ])
    return self_state,pair

manifest=[]
for n,(sid,s) in enumerate(seqs.items()):
    kp=np.asarray(s["keypoints"])[::STEP]
    ann=np.asarray(s["annotations"])[:,::STEP]
    ss,pp=features(kp)
    chase=ann[0].astype(np.float32)
    lights=ann[1].astype(np.float32)
    fn=f"{sid}.npz"
    np.savez_compressed(OUT/fn,self_state=ss,pair_state=pp,
        agent_mask=np.ones(ss.shape[:2],bool),
        identity_id=np.tile(np.arange(ss.shape[1],dtype=np.int64),(len(ss),1)),
        chase=chase,lights=lights)
    # stable sequence-level pretraining split; NOT an animal-level inference split
    h=int(hashlib.sha1(sid.encode()).hexdigest()[:8],16)%10
    split="validation" if h==0 else "pretrain"
    manifest.append({"sequence_id":sid,"file":fn,"frames_original":int(len(s["keypoints"])),
      "frames_cached":int(len(ss)),"n_agents":int(ss.shape[1]),"self_dim":int(ss.shape[-1]),
      "pair_dim":int(pp.shape[-1]),"split":split,"chase_positive_frames":int(np.nansum(chase>0)),
      "lights_on_frames":int(np.nansum(lights>0))})
    if (n+1)%100==0: print("converted",n+1,flush=True)

out={"schema":"social-world-v1","dataset":"MABe22 mouse triplets","source":str(SRC),
     "vocabulary":vocab,"downsample_step_frames":STEP,
     "timing_guardrail":"Frame rate is not assumed in this adapter; horizons remain in cached-frame units until source timing metadata are explicitly verified.",
     "n_sequences":len(manifest),"total_original_frames":int(sum(m["frames_original"] for m in manifest)),
     "total_cached_frames":int(sum(m["frames_cached"] for m in manifest)),
     "pretrain_sequences":int(sum(m["split"]=="pretrain" for m in manifest)),
     "validation_sequences":int(sum(m["split"]=="validation" for m in manifest)),
     "manifest":manifest,
     "split_guardrail":"The source user-train bundle does not establish independent animal identities here. This split is only for representation pretraining/validation and must not be reported as held-animal generalization."}
(OUT/"manifest.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in out.items() if k!="manifest"},indent=2))
