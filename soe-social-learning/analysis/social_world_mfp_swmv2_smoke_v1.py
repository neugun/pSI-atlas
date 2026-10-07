from __future__ import annotations
from pathlib import Path
import json, math, sys, random
import numpy as np
import torch
import torch.nn.functional as F
from scipy.io import loadmat

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from social_world_model_v2 import SocialWorldConfig, SocialWorldModelV2

DATA=Path(r"H:\brain_world_model_20261005\external_social_data\MFP-ERa-GC18.mat")
OUT=HERE.parent/"data"/"SOCIAL_WORLD_MFP_GC18_SWMV2_SMOKE_v1.json"

torch.set_num_threads(4)
SEED=20261006
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)

raw=loadmat(DATA,squeeze_me=True,struct_as_record=False)["Raw"]
day=raw.r200911
regions=[str(x) for x in np.asarray(raw.regions).tolist()]
beh=[str(x) for x in np.asarray(day.behaviors).tolist()]
fs=np.asarray(day.Fstart).astype(int)
fe=np.asarray(day.Fstop).astype(int)
sig=np.asarray(day.Lfold,dtype=np.float32)
FL=float(day.FL)
labels=sorted(set(beh))
lab2i={x:i for i,x in enumerate(labels)}
n=len(beh)

# MATLAB annotations are treated as frame indices; clamp robustly and average each bout.
event_neural=[]
duration=[]
for a,b in zip(fs,fe):
    a=max(0,min(int(a),sig.shape[1]-1))
    b=max(a,min(int(b),sig.shape[1]-1))
    event_neural.append(np.nanmean(sig[:,a:b+1],axis=1))
    duration.append((b-a+1)/FL)
event_neural=np.asarray(event_neural,np.float32)
duration=np.asarray(duration,np.float32)
y=np.array([lab2i[x] for x in beh],np.int64)

# Each current event predicts next event and next event neural state.
Xbeh=np.eye(len(labels),dtype=np.float32)[y]
progress=np.linspace(0,1,n,dtype=np.float32)
logdur=np.log1p(duration).astype(np.float32)
self_state=np.concatenate([Xbeh,logdur[:,None],progress[:,None]],axis=1)

split=int(round(.70*(n-1)))
tr_idx=np.arange(0,split)
te_idx=np.arange(split,n-1)

# Train-only standardization.
mu=event_neural[tr_idx].mean(0); sd=event_neural[tr_idx].std(0)+1e-6
neural=(event_neural-mu)/sd
dmu=logdur[tr_idx].mean(); dsd=logdur[tr_idx].std()+1e-6
self_state[:,-2]=(self_state[:,-2]-dmu)/dsd

def make_batch(idx,use_neural=True):
    T=len(idx)
    ss=torch.from_numpy(self_state[idx][None,:,None,:])
    pair=torch.zeros(1,T,1,1,4,dtype=torch.float32)
    mask=torch.ones(1,T,1,dtype=torch.bool)
    ident=torch.zeros(1,T,1,dtype=torch.long)
    ctx=np.column_stack([progress[idx], np.sin(2*np.pi*progress[idx]), np.cos(2*np.pi*progress[idx]), np.ones(T,dtype=np.float32)])
    batch={
      "self_state":ss,
      "pair_state":pair,
      "agent_mask":mask,
      "identity_id":ident,
      "context":torch.from_numpy(ctx[None].astype(np.float32)),
      "intervention_id":torch.zeros(1,T,dtype=torch.long),
      "focal_agent":torch.zeros(1,T,dtype=torch.long),
      "neural_state":torch.from_numpy(neural[idx][None].astype(np.float32)) if use_neural else None
    }
    ta=torch.from_numpy(y[idx+1][None])
    tn=torch.from_numpy(neural[idx+1][None].astype(np.float32))
    return batch,ta,tn

def fit(use_neural,seed):
    torch.manual_seed(seed)
    cfg=SocialWorldConfig(
      self_dim=self_state.shape[1],pair_dim=4,context_dim=4,neural_dim=len(regions),
      hidden=64,relation_hidden=64,slow_hidden=32,n_actions=len(labels),n_outcomes=4,
      n_social_contents=8,n_interventions=2,n_identity_slots=4,max_agents=1,dropout=.05
    )
    m=SocialWorldModelV2(cfg)
    opt=torch.optim.AdamW(m.parameters(),lr=3e-3,weight_decay=1e-4)
    b,ytr,ntr=make_batch(tr_idx,use_neural)
    for ep in range(120):
        m.train(); o=m(b)
        loss_a=F.cross_entropy(o["next_action_logits"].reshape(-1,len(labels)),ytr.reshape(-1))
        loss_am=F.cross_entropy(o["next_action_logits_multimodal"].reshape(-1,len(labels)),ytr.reshape(-1))
        loss_n=F.mse_loss(o["neural_prediction"],ntr)
        loss=loss_a+.50*loss_am+.20*loss_n
        opt.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(),1.0); opt.step()
    m.eval()
    with torch.no_grad():
        bt,yte,nte=make_batch(te_idx,use_neural)
        ot=m(bt)
        pa=torch.softmax(ot["next_action_logits"],-1)
        pam=torch.softmax(ot["next_action_logits_multimodal"],-1)
        nll=float(F.cross_entropy(ot["next_action_logits"].reshape(-1,len(labels)),yte.reshape(-1)))
        nllm=float(F.cross_entropy(ot["next_action_logits_multimodal"].reshape(-1,len(labels)),yte.reshape(-1)))
        acc=float((pa.argmax(-1)==yte).float().mean())
        accm=float((pam.argmax(-1)==yte).float().mean())
        mse=float(F.mse_loss(ot["neural_prediction"],nte))
    return {"test_action_nll_core":nll,"test_action_accuracy_core":acc,
            "test_action_nll_multimodal":nllm,"test_action_accuracy_multimodal":accm,
            "test_next_neural_mse":mse,"params":sum(p.numel() for p in m.parameters())}

def markov():
    counts=np.ones((len(labels),len(labels)),dtype=float)
    for i in tr_idx: counts[y[i],y[i+1]]+=1
    P=counts/counts.sum(1,keepdims=True)
    probs=np.array([P[y[i],y[i+1]] for i in te_idx])
    pred=np.array([P[y[i]].argmax() for i in te_idx])
    return {"test_action_nll":float(-np.log(probs).mean()),"test_action_accuracy":float(np.mean(pred==y[te_idx+1]))}

with_neural=fit(True,SEED)
without_neural=fit(False,SEED)
mk=markov()
out={
 "generated_at":"2026-10-06",
 "status":"EXTERNAL_NEURAL_SOCIAL_PIPELINE_SMOKE_NOT_POPULATION_CLAIM",
 "source":"Zenodo 8128564 / MFP-ERa-GC18.mat",
 "animal":"GC18","day":"r200911","regions":regions,"n_regions":len(regions),
 "n_bouts":n,"n_behavior_labels":len(labels),"behavior_labels":labels,
 "split":{"type":"chronological","train_transitions":int(len(tr_idx)),"test_transitions":int(len(te_idx))},
 "swmv2_with_current_neural":with_neural,
 "swmv2_without_current_neural":without_neural,
 "markov_behavior_baseline":mk,
 "paired_architecture_delta":{
   "core_action_nll_without_minus_with":without_neural["test_action_nll_core"]-with_neural["test_action_nll_core"],
   "multimodal_action_nll_without_minus_with":without_neural["test_action_nll_multimodal"]-with_neural["test_action_nll_multimodal"],
   "next_neural_mse_without_minus_with":without_neural["test_next_neural_mse"]-with_neural["test_next_neural_mse"]
 },
 "guardrail":"One animal/day, chronological smoke test. This validates end-to-end ingestion and neural/social forecasting only; it is not evidence of population generalization or superiority until multi-animal held-out evaluation is run."
}
OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
