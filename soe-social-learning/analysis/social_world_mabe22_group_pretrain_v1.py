from __future__ import annotations
from pathlib import Path
import json, random, sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from social_world_model_v2 import MLP, DirectedRelationBlock

ROOT=Path(r"H:\brain_world_model_20261005\external_social_data\mabe22_socialworld")
OUT=HERE.parent/"data"/"SOCIAL_WORLD_MABE22_GROUP_PRETRAIN_v1.json"
CKPT=HERE.parent/"data"/"SOCIAL_WORLD_MABE22_GROUP_PRETRAIN_v1.pt"
SEED=20261006
H=48
EPOCHS=4
CHUNK=96
HORIZONS=[1,5,15]
torch.set_num_threads(8)
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)

manifest=json.loads((ROOT/"manifest.json").read_text())
pre=[m for m in manifest["manifest"] if m["split"]=="pretrain"]
val=[m for m in manifest["manifest"] if m["split"]=="validation"]
print("MABE22",len(pre),len(val),manifest["total_cached_frames"],flush=True)

# Robust normalization estimated from a deterministic subset of training sequences only.
sample_meta=pre[::max(1,len(pre)//80)]
ss=[]; pp=[]
for m in sample_meta:
    z=np.load(ROOT/m["file"])
    ss.append(z["self_state"][::4].reshape(-1,z["self_state"].shape[-1]))
    pp.append(z["pair_state"][::4].reshape(-1,z["pair_state"].shape[-1]))
ss=np.concatenate(ss); pp=np.concatenate(pp)
smu=ss.mean(0); ssd=np.where(ss.std(0)>1e-4,ss.std(0),1.)
pmu=pp.mean(0); psd=np.where(pp.std(0)>1e-4,pp.std(0),1.)

def load(m):
    z=np.load(ROOT/m["file"])
    s=np.clip((z["self_state"]-smu)/ssd,-8,8).astype(np.float32)
    p=np.clip((z["pair_state"]-pmu)/psd,-8,8).astype(np.float32)
    chase=z["chase"].astype(np.float32)
    lights=z["lights"].astype(np.float32)
    return s,p,chase,lights

class GroupDynamics(nn.Module):
    def __init__(self,self_dim,pair_dim):
        super().__init__()
        self.self_enc=MLP(self_dim,H,H,.05)
        self.rel1=DirectedRelationBlock(H,pair_dim,.05)
        self.rel2=DirectedRelationBlock(H,pair_dim,.05)
        self.temporal=nn.GRU(H,H,batch_first=True)
        self.self_heads=nn.ModuleDict({str(k):nn.Linear(H,self_dim) for k in HORIZONS})
        self.pair_heads=nn.ModuleDict({str(k):MLP(2*H,pair_dim,H,.05) for k in HORIZONS})
        self.chase=nn.Linear(H,1)
        self.light=nn.Linear(H,1)
    def forward(self,s,p,mask):
        # B,T,N,F
        z=self.self_enc(s)
        z=self.rel1(z,p,mask); z=self.rel2(z,p,mask)
        B,T,N,Hd=z.shape
        q=z.permute(0,2,1,3).reshape(B*N,T,Hd)
        q,_=self.temporal(q)
        q=q.reshape(B,N,T,Hd).permute(0,2,1,3)
        group=q.mean(2)
        out={"z":q,"chase":self.chase(group).squeeze(-1),"light":self.light(group).squeeze(-1)}
        for h in HORIZONS:
            out[f"self_{h}"]=self.self_heads[str(h)](q)
            src=q.unsqueeze(3).expand(B,T,N,N,Hd)
            dst=q.unsqueeze(2).expand(B,T,N,N,Hd)
            out[f"pair_{h}"]=self.pair_heads[str(h)](torch.cat([src,dst],-1))
        return out

def iterate(meta,shuffle,seed):
    rng=np.random.default_rng(seed)
    order=np.arange(len(meta))
    if shuffle:rng.shuffle(order)
    maxh=max(HORIZONS)
    for ii in order:
        s,p,ch,li=load(meta[ii]); T=len(s)
        starts=list(range(0,T-maxh,CHUNK))
        if shuffle:rng.shuffle(starts)
        for st in starts:
            en=min(T-maxh,st+CHUNK)
            if en-st<24:continue
            idx=np.arange(st,en)
            yield s[idx],p[idx],ch[idx],li[idx],{h:(s[idx+h],p[idx+h]) for h in HORIZONS}

model=GroupDynamics(pre[0]["self_dim"],pre[0]["pair_dim"])
opt=torch.optim.AdamW(model.parameters(),lr=1.5e-3,weight_decay=2e-4)
# chase is very sparse; cap positive weight to avoid domination.
pos=sum(m["chase_positive_frames"] for m in pre); total=sum(m["frames_cached"] for m in pre)
posw=min(50.0,max(1.0,(total-pos)/max(pos,1)))
print("chase pos",pos,"total",total,"pos_weight",posw,flush=True)

for ep in range(EPOCHS):
    model.train(); losses=[]
    for s,p,ch,li,fut in iterate(pre,True,SEED+ep):
        st=torch.from_numpy(s[None]); pt=torch.from_numpy(p[None]); mt=torch.ones(1,len(s),3,dtype=torch.bool)
        o=model(st,pt,mt); loss=0.
        for h in HORIZONS:
            ts=torch.from_numpy(fut[h][0][None]); tp=torch.from_numpy(fut[h][1][None])
            loss=loss+F.smooth_l1_loss(o[f"self_{h}"],ts)+.5*F.smooth_l1_loss(o[f"pair_{h}"],tp)
        loss=loss/len(HORIZONS)
        ct=torch.from_numpy(ch[None]); lt=torch.from_numpy(li[None])
        lc=F.binary_cross_entropy_with_logits(o["chase"],ct,pos_weight=torch.tensor(posw))
        ll=F.binary_cross_entropy_with_logits(o["light"],lt)
        loss=loss+.03*lc+.02*ll
        if not torch.isfinite(loss): raise RuntimeError("nonfinite")
        opt.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),.5); opt.step()
        losses.append(float(loss.detach()))
    print("EPOCH",ep,"loss",float(np.mean(losses)),flush=True)

def evaluate():
    model.eval(); agg={h:{"self":[],"pair":[],"persist_self":[],"persist_pair":[]} for h in HORIZONS}
    chase_y=[];chase_p=[];light_y=[];light_p=[]
    with torch.no_grad():
        for s,p,ch,li,fut in iterate(val,False,SEED):
            st=torch.from_numpy(s[None]); pt=torch.from_numpy(p[None]); mt=torch.ones(1,len(s),3,dtype=torch.bool)
            o=model(st,pt,mt)
            for h in HORIZONS:
                ts=fut[h][0];tp=fut[h][1]
                agg[h]["self"].append(float(np.mean((o[f"self_{h}"].squeeze(0).numpy()-ts)**2)))
                agg[h]["pair"].append(float(np.mean((o[f"pair_{h}"].squeeze(0).numpy()-tp)**2)))
                agg[h]["persist_self"].append(float(np.mean((s-ts)**2)))
                agg[h]["persist_pair"].append(float(np.mean((p-tp)**2)))
            chase_y.append(ch); chase_p.append(torch.sigmoid(o["chase"]).squeeze(0).numpy())
            light_y.append(li); light_p.append(torch.sigmoid(o["light"]).squeeze(0).numpy())
    res={}
    for h in HORIZONS:
        res[f"h{h}"]={k:float(np.mean(v)) for k,v in agg[h].items()}
        res[f"h{h}"]["self_gain_vs_persistence"]=res[f"h{h}"]["persist_self"]-res[f"h{h}"]["self"]
        res[f"h{h}"]["pair_gain_vs_persistence"]=res[f"h{h}"]["persist_pair"]-res[f"h{h}"]["pair"]
    cy=np.concatenate(chase_y);cp=np.concatenate(chase_p);ly=np.concatenate(light_y);lp=np.concatenate(light_p)
    res["chase_brier"]=float(np.mean((cp-cy)**2)); res["light_brier"]=float(np.mean((lp-ly)**2))
    return res

metrics=evaluate()
torch.save({"self_enc":model.self_enc.state_dict(),"rel1":model.rel1.state_dict(),"rel2":model.rel2.state_dict(),
            "temporal":model.temporal.state_dict(),"normalization":{"smu":smu,"ssd":ssd,"pmu":pmu,"psd":psd}},CKPT)
out={"generated_at":"2026-10-06","status":"MABE22_GROUP_DYNAMICS_PRETRAIN",
     "n_pretrain_sequences":len(pre),"n_validation_sequences":len(val),"horizons_cached_frames":HORIZONS,
     "metrics":metrics,"checkpoint":str(CKPT),
     "transfer_contract":"Only relation/self encoder weights are eligible for Stage30 initialization; target SOE heads are always newly fit.",
     "guardrail":manifest["split_guardrail"]}
OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
