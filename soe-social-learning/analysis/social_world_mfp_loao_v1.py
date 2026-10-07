from __future__ import annotations
from pathlib import Path
import json, math, random, sys
from collections import Counter
import numpy as np
import torch
import torch.nn.functional as F
from scipy.io import loadmat
from sklearn.metrics import balanced_accuracy_score
from scipy.stats import wilcoxon

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from social_world_model_v2 import SocialWorldConfig, SocialWorldModelV2

RAWROOT=Path(r"H:\brain_world_model_20261005\external_social_data")
OUT=HERE.parent/"data"/"SOCIAL_WORLD_MFP_LOAO_v1.json"
SEEDS=[20261006,20261007]
torch.set_num_threads(4)

BEH=["Other","Investigate","Attack","Reproductive"]
B2I={x:i for i,x in enumerate(BEH)}
CTX=["Baseline","F","M","Toy"]
C2I={x:i for i,x in enumerate(CTX)}
REPRO={"Attempted_Mount","Mount","Thrust","Ejaculate"}
CONTEXT_MARKERS={
    "Intro_Baseline":("set","Baseline"),"Rmv_Baseline":("remove","Baseline"),
    "Intro_F":("set","F"),"Rmv_F":("remove","F"),
    "Intro_M":("set","M"),"Rmv_M":("remove","M"),
    "Intro_Toy":("set","Toy"),"Rmv_Toy":("remove","Toy")
}

def coarse(x):
    if x=="Other": return "Other"
    if x=="Investigate": return "Investigate"
    if x=="Attack": return "Attack"
    if x in REPRO: return "Reproductive"
    return None

def completed_files():
    out=[]
    for p in sorted(RAWROOT.glob("MFP-ERa-GC*.mat")):
        if p.stat().st_size < 1_000_000: continue
        try:
            d=loadmat(p,squeeze_me=True,struct_as_record=False)
            raw=d["Raw"]
            regs=[str(x) for x in np.asarray(raw.regions).tolist()]
            days=[x for x in (getattr(raw,"_fieldnames",[]) or []) if x.startswith("r") and x[1:].isdigit()]
            if days: out.append((p,d,raw,regs,days))
        except Exception as e:
            print("SKIP",p.name,repr(e),flush=True)
    return out

FILES=completed_files()
animals=[p.stem.replace("MFP-ERa-","") for p,_,_,_,_ in FILES]
common=sorted(set.intersection(*[set(regs) for _,_,_,regs,_ in FILES]))
# Deliberately exact-name only. PAGl/lPAG is not harmonized here.
if len(common)<10: raise RuntimeError(common)
print("ANIMALS",animals,"COMMON",common,flush=True)

def build_sequences():
    seqs=[]
    for p,d,raw,regs,days in FILES:
        animal=p.stem.replace("MFP-ERa-","")
        ridx=[regs.index(r) for r in common]
        for day in days:
            q=getattr(raw,day)
            sig=np.asarray(q.Lfold,dtype=np.float32)[ridx]
            fs=np.asarray(q.Fstart).astype(int)
            fe=np.asarray(q.Fstop).astype(int)
            labs=[str(x) for x in np.asarray(q.behaviors).tolist()]
            order=np.argsort(fs); fs=fs[order]; fe=fe[order]; labs=[labs[i] for i in order]
            fps=float(q.FL); nframes=sig.shape[1]
            ctx="Baseline"; rows=[]
            for a,b,lab in zip(fs,fe,labs):
                if lab in CONTEXT_MARKERS:
                    typ,val=CONTEXT_MARKERS[lab]
                    if typ=="set": ctx=val
                    elif typ=="remove" and ctx==val: ctx="Baseline"
                    continue
                cc=coarse(lab)
                if cc is None: continue
                a=max(0,min(int(a),nframes-1)); b=max(a,min(int(b),nframes-1))
                neu=np.nanmean(sig[:,a:b+1],axis=1)
                rows.append({
                    "behavior":B2I[cc],"ctx":C2I[ctx],
                    "duration":(b-a+1)/fps,
                    "progress":a/max(1,nframes-1),
                    "neural":neu.astype(np.float32)
                })
            if len(rows)<8: continue
            seqs.append({"animal":animal,"day":day,"rows":rows})
    return seqs

SEQS=build_sequences()
print("SEQS",len(SEQS),"EVENTS",sum(len(s["rows"]) for s in SEQS),flush=True)

def train_stats(train):
    neu=np.concatenate([[r["neural"] for r in s["rows"]] for s in train],axis=0).astype(np.float64)
    neu=np.nan_to_num(neu,nan=0.0,posinf=0.0,neginf=0.0)
    dur=np.concatenate([[r["duration"] for r in s["rows"]] for s in train],axis=0)
    mu=np.mean(neu,0)
    sd=np.std(neu,0)
    sd=np.where(np.isfinite(sd) & (sd>1e-3),sd,1.0)
    return mu.astype(np.float32),sd.astype(np.float32),float(np.mean(np.log1p(dur))),float(max(np.std(np.log1p(dur)),1e-3))

def tensorize(s,stats,use_neural):
    mu,sd,dm,ds=stats; rows=s["rows"]; L=len(rows)-1
    cur=rows[:-1]; nxt=rows[1:]
    y=np.array([r["behavior"] for r in nxt],np.int64)
    one=np.eye(len(BEH),dtype=np.float32)[[r["behavior"] for r in cur]]
    dur=(np.log1p([r["duration"] for r in cur])-dm)/ds
    prog=np.array([r["progress"] for r in cur],np.float32)
    ss=np.concatenate([one,np.asarray(dur,np.float32)[:,None],prog[:,None]],axis=1)
    cidx=np.array([r["ctx"] for r in cur],int)
    ctx=np.eye(len(CTX),dtype=np.float32)[cidx]
    ctx=np.concatenate([ctx,prog[:,None],np.sin(2*np.pi*prog)[:,None],np.cos(2*np.pi*prog)[:,None]],axis=1)
    neu=np.stack([r["neural"] for r in cur]).astype(np.float32)
    neun=np.stack([r["neural"] for r in nxt]).astype(np.float32)
    neu=np.nan_to_num((neu-mu)/sd,nan=0.0,posinf=8.0,neginf=-8.0)
    neun=np.nan_to_num((neun-mu)/sd,nan=0.0,posinf=8.0,neginf=-8.0)
    neu=np.clip(neu,-8.0,8.0); neun=np.clip(neun,-8.0,8.0)
    batch={
      "self_state":torch.from_numpy(ss[None,:,None,:]),
      "pair_state":torch.zeros(1,L,1,1,4,dtype=torch.float32),
      "agent_mask":torch.ones(1,L,1,dtype=torch.bool),
      "identity_id":torch.full((1,L,1),-1,dtype=torch.long),
      "context":torch.from_numpy(ctx[None].astype(np.float32)),
      "intervention_id":torch.zeros(1,L,dtype=torch.long),
      "focal_agent":torch.zeros(1,L,dtype=torch.long),
      "neural_state":torch.from_numpy(neu[None]) if use_neural else None
    }
    return batch,torch.from_numpy(y),torch.from_numpy(neun)

def fit_eval(train,test,use_neural,seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    st=train_stats(train)
    cfg=SocialWorldConfig(
      self_dim=6,pair_dim=4,context_dim=7,neural_dim=len(common),
      hidden=48,relation_hidden=48,slow_hidden=24,n_actions=len(BEH),
      n_outcomes=4,n_social_contents=8,n_interventions=2,n_identity_slots=4,dropout=.05)
    m=SocialWorldModelV2(cfg)
    opt=torch.optim.AdamW(m.parameters(),lr=1.0e-3,weight_decay=2e-4)
    # sequence-wise training: preserves each day's recurrent continuity, never crosses animal/day boundaries
    for ep in range(55):
        order=np.random.default_rng(seed+ep).permutation(len(train))
        m.train()
        for ii in order:
            b,y,yn=tensorize(train[ii],st,use_neural)
            o=m(b)
            lc=F.cross_entropy(o["next_action_logits"].reshape(-1,len(BEH)),y)
            lm=F.cross_entropy(o["next_action_logits_multimodal"].reshape(-1,len(BEH)),y)
            ln=F.mse_loss(o["neural_prediction"].reshape(-1,len(common)),yn)
            loss=lc + .5*lm + .05*ln
            if not torch.isfinite(loss):
                raise RuntimeError(f"non-finite training loss held-seed={seed} seq={train[ii]['animal']}:{train[ii]['day']} lc={float(lc)} lm={float(lm)} ln={float(ln)}")
            opt.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(m.parameters(),0.5); opt.step()
    m.eval(); all_y=[]; core_p=[]; multi_p=[]; neu_y=[]; neu_p=[]
    with torch.no_grad():
        for s in test:
            b,y,yn=tensorize(s,st,use_neural); o=m(b)
            all_y.append(y.numpy())
            core_p.append(torch.softmax(o["next_action_logits"],-1).squeeze(0).numpy())
            multi_p.append(torch.softmax(o["next_action_logits_multimodal"],-1).squeeze(0).numpy())
            neu_y.append(yn.numpy()); neu_p.append(o["neural_prediction"].squeeze(0).numpy())
    y=np.concatenate(all_y); pc=np.concatenate(core_p); pm=np.concatenate(multi_p)
    ny=np.concatenate(neu_y); npred=np.concatenate(neu_p)
    def nll(p): return float(-np.log(np.clip(p[np.arange(len(y)),y],1e-7,1)).mean())
    return {
      "n_test_transitions":int(len(y)),
      "core_nll":nll(pc),
      "core_balanced_accuracy":float(balanced_accuracy_score(y,pc.argmax(1))),
      "multimodal_nll":nll(pm),
      "multimodal_balanced_accuracy":float(balanced_accuracy_score(y,pm.argmax(1))),
      "next_neural_mse":float(np.mean((npred-ny)**2)),
      "params":int(sum(p.numel() for p in m.parameters()))
    }

def markov(train,test):
    counts=np.ones((len(BEH),len(BEH)),float)
    for s in train:
        yy=[r["behavior"] for r in s["rows"]]
        for a,b in zip(yy[:-1],yy[1:]): counts[a,b]+=1
    P=counts/counts.sum(1,keepdims=True)
    ys=[]; ps=[]
    for s in test:
        yy=[r["behavior"] for r in s["rows"]]
        for a,b in zip(yy[:-1],yy[1:]): ys.append(b); ps.append(P[a])
    y=np.asarray(ys); p=np.asarray(ps)
    return {"nll":float(-np.log(np.clip(p[np.arange(len(y)),y],1e-7,1)).mean()),
            "balanced_accuracy":float(balanced_accuracy_score(y,p.argmax(1)))}

folds=[]
for held in sorted(set(s["animal"] for s in SEQS)):
    train=[s for s in SEQS if s["animal"]!=held]; test=[s for s in SEQS if s["animal"]==held]
    if not train or not test: continue
    row={"held_out_animal":held,"n_test_days":len(test),"markov":markov(train,test),"seeds":[]}
    for seed in SEEDS:
        a=fit_eval(train,test,True,seed)
        b=fit_eval(train,test,False,seed)
        row["seeds"].append({"seed":seed,"with_neural":a,"without_neural":b})
        print("FOLD",held,"SEED",seed,"N",a["n_test_transitions"],
              "multi dNLL",round(b["multimodal_nll"]-a["multimodal_nll"],4),
              "neural dMSE",round(b["next_neural_mse"]-a["next_neural_mse"],4),flush=True)
    def mean(path,mode):
        return float(np.mean([z[mode][path] for z in row["seeds"]]))
    row["ensemble_summary"]={
      "with_neural_multimodal_nll":mean("multimodal_nll","with_neural"),
      "without_neural_multimodal_nll":mean("multimodal_nll","without_neural"),
      "neural_behavior_nll_gain":mean("multimodal_nll","without_neural")-mean("multimodal_nll","with_neural"),
      "with_neural_next_neural_mse":mean("next_neural_mse","with_neural"),
      "without_neural_next_neural_mse":mean("next_neural_mse","without_neural"),
      "neural_future_mse_gain":mean("next_neural_mse","without_neural")-mean("next_neural_mse","with_neural"),
      "with_neural_balanced_accuracy":mean("multimodal_balanced_accuracy","with_neural"),
      "without_neural_balanced_accuracy":mean("multimodal_balanced_accuracy","without_neural")
    }
    folds.append(row)

def stat(key,alt="greater"):
    x=np.array([r["ensemble_summary"][key] for r in folds],float)
    try:p=float(wilcoxon(x,alternative=alt).pvalue)
    except Exception:p=None
    return {"n_animals":len(x),"mean":float(x.mean()),"median":float(np.median(x)),
            "positive":int((x>0).sum()),"negative":int((x<0).sum()),
            "wilcoxon_one_sided_p":p,"values":x.tolist()}

out={
 "generated_at":"2026-10-06",
 "status":"MULTI_ANIMAL_EXTERNAL_NEURAL_SOCIAL_BENCHMARK",
 "animals":sorted(set(s["animal"] for s in SEQS)),
 "n_animals":len(set(s["animal"] for s in SEQS)),
 "n_days":len(SEQS),"n_events":sum(len(s["rows"]) for s in SEQS),
 "common_regions_exact_name":common,
 "region_guardrail":"PAG excluded because GC2 uses PAGl whereas other animals use lPAG; no synonym mapping is assumed in v1.",
 "behavior_ontology":BEH,
 "context_ontology":CTX,
 "split":"leave-one-animal-out; all preprocessing statistics fit on training animals only",
 "summary":{
   "neural_behavior_nll_gain":stat("neural_behavior_nll_gain","greater"),
   "neural_future_mse_gain":stat("neural_future_mse_gain","greater")
 },
 "folds":folds,
 "interpretation":"Tests whether current 12-region neural state adds cross-animal information beyond event/context history for future social behavior, while separately testing future neural-state prediction.",
 "guardrail":"Animal is the inferential unit. This is an external multifiber dataset and not SOE; behavioral labels are deliberately coarsened before model fitting using a fixed ontology."
}
OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps({"summary":out["summary"],"n_animals":out["n_animals"],"n_days":out["n_days"],"n_events":out["n_events"]},indent=2))
