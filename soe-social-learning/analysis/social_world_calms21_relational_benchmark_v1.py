from __future__ import annotations
from pathlib import Path
import json, math, random, sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.stats import wilcoxon
from sklearn.metrics import balanced_accuracy_score

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from social_world_model_v2 import SocialWorldConfig, SocialWorldModelV2

ROOT=Path(r"H:\brain_world_model_20261005\external_social_data\calms21_task1_socialworld")
OUT=HERE.parent/"data"/"SOCIAL_WORLD_CALMS21_RELATIONAL_BENCHMARK_v1.json"
SEEDS=[20261006,20261007]
MODES=["relational","self_only","partner_shuffle"]
HORIZONS=[1,3,10]  # after 6x downsample from ~30 fps => ~0.2, 0.6, 2.0 s
DOWNSAMPLE=6
CHUNK=96
EPOCHS=7
torch.set_num_threads(4)

manifest=json.loads((ROOT/"manifest.json").read_text())
meta=manifest["sequences"]
train_meta=[x for x in meta if "__train__" in x["file"]]
test_meta=[x for x in meta if "__test__" in x["file"]]
assert train_meta and test_meta
print("CALMS train/test",len(train_meta),len(test_meta),"frames",manifest["total_frames"],flush=True)

def load_seq(m):
    z=np.load(ROOT/m["file"])
    self_state=z["self_state"][::DOWNSAMPLE].astype(np.float32)
    pair=z["pair_state"][::DOWNSAMPLE].astype(np.float32)
    y=z["annotations"][::DOWNSAMPLE].astype(np.int64)
    return {"id":m["sequence_id"],"self":self_state,"pair":pair,"y":y}

train=[load_seq(m) for m in train_meta]
test=[load_seq(m) for m in test_meta]

# train-only normalization, channel-wise; preserve masks and categorical targets.
self_all=np.concatenate([s["self"].reshape(-1,s["self"].shape[-1]) for s in train])
pair_all=np.concatenate([s["pair"].reshape(-1,s["pair"].shape[-1]) for s in train])
smu=self_all.mean(0); ssd=self_all.std(0); ssd=np.where(ssd>1e-4,ssd,1.)
pmu=pair_all.mean(0); psd=pair_all.std(0); psd=np.where(psd>1e-4,psd,1.)
for s in train+test:
    s["self"]=np.clip((s["self"]-smu)/ssd,-8,8).astype(np.float32)
    s["pair"]=np.clip((s["pair"]-pmu)/psd,-8,8).astype(np.float32)

counts=np.bincount(np.concatenate([s["y"] for s in train]),minlength=4).astype(float)
weights=(counts.sum()/np.maximum(counts,1)); weights=weights/weights.mean()
CLASS_W=torch.tensor(weights,dtype=torch.float32)
print("class_counts",counts.tolist(),"weights",weights.tolist(),flush=True)

def transformed(s,mode):
    x=s["self"].copy(); p=s["pair"].copy()
    mask=np.ones((len(x),2),bool)
    if mode=="self_only":
        x[:,1]=0; p[:]=0; mask[:,1]=False
    elif mode=="partner_shuffle":
        # Keep focal trajectory exactly intact while breaking moment-by-moment partner/relation correspondence.
        shift=max(17,len(x)//3)
        x[:,1]=np.roll(x[:,1],shift,axis=0)
        p=np.roll(p,shift,axis=0)
    return x,p,mask

def chunks(s,mode,shuffle=False,rng=None):
    x,p,mask=transformed(s,mode)
    starts=list(range(0,max(1,len(x)-max(HORIZONS)),CHUNK))
    if shuffle and rng is not None: rng.shuffle(starts)
    for st in starts:
        en=min(len(x)-max(HORIZONS),st+CHUNK)
        if en-st<12: continue
        idx=np.arange(st,en)
        yield x[idx],p[idx],mask[idx],{h:s["y"][idx+h] for h in HORIZONS}

class HorizonModel(nn.Module):
    def __init__(self):
        super().__init__()
        cfg=SocialWorldConfig(self_dim=23,pair_dim=12,context_dim=4,neural_dim=1,
            hidden=48,relation_hidden=48,slow_hidden=24,n_actions=4,n_outcomes=4,
            n_social_contents=4,n_interventions=2,n_identity_slots=4,max_agents=2,dropout=.05)
        self.core=SocialWorldModelV2(cfg)
        self.heads=nn.ModuleDict({str(h):nn.Linear(cfg.hidden,4) for h in HORIZONS})
    def forward(self,x,p,mask):
        B,T,N,_=x.shape
        batch={
          "self_state":x,"pair_state":p,"agent_mask":mask,
          "identity_id":torch.full((B,T,N),-1,dtype=torch.long,device=x.device),
          "context":torch.zeros(B,T,4,device=x.device),
          "intervention_id":torch.zeros(B,T,dtype=torch.long,device=x.device),
          "focal_agent":torch.zeros(B,T,dtype=torch.long,device=x.device),
          "neural_state":None
        }
        z=self.core(batch)["behavior_latent"]
        return {h:self.heads[str(h)](z) for h in HORIZONS}

def train_one(mode,seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    m=HorizonModel()
    opt=torch.optim.AdamW(m.parameters(),lr=1.5e-3,weight_decay=2e-4)
    rng=np.random.default_rng(seed)
    for ep in range(EPOCHS):
        order=rng.permutation(len(train))
        m.train(); running=[]
        for ii in order:
            for x,p,mask,ys in chunks(train[ii],mode,shuffle=True,rng=rng):
                xt=torch.from_numpy(x[None]); pt=torch.from_numpy(p[None]); mt=torch.from_numpy(mask[None])
                o=m(xt,pt,mt)
                loss=0
                for h in HORIZONS:
                    yt=torch.from_numpy(ys[h])
                    loss=loss+F.cross_entropy(o[h].reshape(-1,4),yt,weight=CLASS_W)
                loss=loss/len(HORIZONS)
                if not torch.isfinite(loss): raise RuntimeError(f"nonfinite {mode} {seed}")
                opt.zero_grad(set_to_none=True); loss.backward()
                torch.nn.utils.clip_grad_norm_(m.parameters(),0.5); opt.step()
                running.append(float(loss.detach()))
        print("TRAIN",mode,seed,"ep",ep,"loss",round(float(np.mean(running)),4),flush=True)

    m.eval(); animals=[]
    with torch.no_grad():
        for s in test:
            prob={h:[] for h in HORIZONS}; yy={h:[] for h in HORIZONS}
            for x,p,mask,ys in chunks(s,mode):
                o=m(torch.from_numpy(x[None]),torch.from_numpy(p[None]),torch.from_numpy(mask[None]))
                for h in HORIZONS:
                    prob[h].append(torch.softmax(o[h],-1).squeeze(0).numpy()); yy[h].append(ys[h])
            row={"animal":s["id"]}
            for h in HORIZONS:
                P=np.concatenate(prob[h]); Y=np.concatenate(yy[h])
                nll=float(-np.log(np.clip(P[np.arange(len(Y)),Y],1e-7,1)).mean())
                ba=float(balanced_accuracy_score(Y,P.argmax(1)))
                row[f"h{h}_nll"]=nll; row[f"h{h}_balanced_accuracy"]=ba; row[f"h{h}_n"]=int(len(Y))
            animals.append(row)
    return {"mode":mode,"seed":seed,"params":sum(p.numel() for p in m.parameters()),"animals":animals}

runs=[]
for mode in MODES:
    for seed in SEEDS:
        runs.append(train_one(mode,seed))

# Average seeds per test animal, then paired animal-level inference.
ids=[x["sequence_id"] for x in test_meta]
summary={}
for mode in MODES:
    rs=[r for r in runs if r["mode"]==mode]
    rows=[]
    for i,aid in enumerate(ids):
        q={"animal":aid}
        for h in HORIZONS:
            q[f"h{h}_nll"]=float(np.mean([r["animals"][i][f"h{h}_nll"] for r in rs]))
            q[f"h{h}_balanced_accuracy"]=float(np.mean([r["animals"][i][f"h{h}_balanced_accuracy"] for r in rs]))
        rows.append(q)
    summary[mode]=rows

paired={}
for comp in ["self_only","partner_shuffle"]:
    paired[comp]={}
    for h in HORIZONS:
        gain=np.array([summary[comp][i][f"h{h}_nll"]-summary["relational"][i][f"h{h}_nll"] for i in range(len(ids))])
        bagain=np.array([summary["relational"][i][f"h{h}_balanced_accuracy"]-summary[comp][i][f"h{h}_balanced_accuracy"] for i in range(len(ids))])
        try:p=float(wilcoxon(gain,alternative="greater").pvalue)
        except Exception:p=None
        paired[comp][f"h{h}"]={
          "n_animals":len(ids),"nll_gain_relational":float(gain.mean()),"median_nll_gain":float(np.median(gain)),
          "positive_nll_gain":int((gain>0).sum()),"wilcoxon_one_sided_p":p,
          "balanced_accuracy_gain":float(bagain.mean()),"median_ba_gain":float(np.median(bagain))
        }

out={
 "generated_at":"2026-10-06",
 "status":"CALMS21_HELD_ANIMAL_RELATIONAL_BENCHMARK",
 "dataset":{"n_train_animals":len(train),"n_test_animals":len(test),"total_original_frames":manifest["total_frames"],
            "downsample":DOWNSAMPLE,"approx_hz":5.0,"self_dim":23,"pair_dim":12},
 "horizons":{"h1":"~0.2 s","h3":"~0.6 s","h10":"~2.0 s"},
 "modes":{
   "relational":"both mice + true directed pair state",
   "self_only":"resident only; partner masked and pair state removed",
   "partner_shuffle":"resident intact; partner and pair channels shifted in time within each animal"
 },
 "paired_animal_level":paired,
 "per_animal_seed_averaged":summary,
 "guardrail":"Official CalMS21 train/test identity split is preserved. Test animals never contribute to normalization, training or model selection. Frame counts are not treated as independent inferential units; paired inference is over the 19 held-out test animals."
}
OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(paired,indent=2))
