from pathlib import Path
from scipy.io import loadmat
from scipy.stats import wilcoxon
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import log_loss, balanced_accuracy_score
import numpy as np, json

ROOT=Path(r"H:\brain_world_model_20261005\external_social_data")
OUT=Path(r"H:\brain_world_model_20261005\push_stage23_clean\soe-social-learning\data\SOCIAL_WORLD_MFP_FAST_INFORMATION_GATE_v1.json")
BEH=["Other","Investigate","Attack","Reproductive"]; B2I={x:i for i,x in enumerate(BEH)}
CTX=["Baseline","F","M","Toy"]; C2I={x:i for i,x in enumerate(CTX)}
REPRO={"Attempted_Mount","Mount","Thrust","Ejaculate"}
MARK={"Intro_Baseline":("set","Baseline"),"Rmv_Baseline":("remove","Baseline"),
"Intro_F":("set","F"),"Rmv_F":("remove","F"),"Intro_M":("set","M"),"Rmv_M":("remove","M"),
"Intro_Toy":("set","Toy"),"Rmv_Toy":("remove","Toy")}

def coarse(x):
 if x in B2I:return x
 if x in REPRO:return "Reproductive"
 return None

files=[]
for p in sorted(ROOT.glob("MFP-ERa-GC*.mat")):
 if p.stat().st_size<1e6:continue
 try:
  d=loadmat(p,squeeze_me=True,struct_as_record=False); raw=d["Raw"]
  regs=[str(x) for x in np.asarray(raw.regions).tolist()]
  days=[x for x in (getattr(raw,"_fieldnames",[]) or []) if x.startswith("r") and x[1:].isdigit()]
  if days:files.append((p,raw,regs,days))
 except:pass
common=sorted(set.intersection(*[set(r) for _,_,r,_ in files]))
seqs=[]
for p,raw,regs,days in files:
 animal=p.stem.replace("MFP-ERa-",""); ridx=[regs.index(r) for r in common]
 for day in days:
  q=getattr(raw,day); sig=np.asarray(q.Lfold,float)[ridx]; fs=np.asarray(q.Fstart).astype(int); fe=np.asarray(q.Fstop).astype(int)
  labs=[str(x) for x in np.asarray(q.behaviors).tolist()]; order=np.argsort(fs); fs=fs[order];fe=fe[order];labs=[labs[i] for i in order]
  ctx="Baseline"; rows=[]; nf=sig.shape[1]; fps=float(q.FL)
  for a,b,lab in zip(fs,fe,labs):
   if lab in MARK:
    typ,val=MARK[lab]
    if typ=="set":ctx=val
    elif typ=="remove" and ctx==val:ctx="Baseline"
    continue
   cc=coarse(lab)
   if cc is None:continue
   a=max(0,min(int(a),nf-1));b=max(a,min(int(b),nf-1))
   neu=np.nanmean(sig[:,a:b+1],1)
   if not np.all(np.isfinite(neu)):continue
   rows.append((B2I[cc],C2I[ctx],np.log1p((b-a+1)/fps),a/max(1,nf-1),neu))
  if len(rows)>=8:seqs.append({"animal":animal,"day":day,"rows":rows})

animals=sorted(set(s["animal"] for s in seqs))
folds=[]
for held in animals:
 tr=[s for s in seqs if s["animal"]!=held]; te=[s for s in seqs if s["animal"]==held]
 def stack(ss):
  X=[];N=[];Y=[];NY=[]
  for s in ss:
   r=s["rows"]
   for a,b in zip(r[:-1],r[1:]):
    beh,ctx,dur,prog,neu=a; y,_,_,_,nneu=b
    base=np.r_[np.eye(4)[beh],np.eye(4)[ctx],dur,prog]
    X.append(base);N.append(neu);Y.append(y);NY.append(nneu)
  return np.asarray(X,float),np.asarray(N,float),np.asarray(Y,int),np.asarray(NY,float)
 Xtr,Ntr,Ytr,NYtr=stack(tr); Xte,Nte,Yte,NYte=stack(te)
 # behavior models
 base=make_pipeline(StandardScaler(),LogisticRegression(C=.5,max_iter=1000,class_weight="balanced",solver="lbfgs"))
 neural=make_pipeline(StandardScaler(),LogisticRegression(C=.5,max_iter=1000,class_weight="balanced",solver="lbfgs"))
 base.fit(Xtr,Ytr); neural.fit(np.c_[Xtr,Ntr],Ytr)
 pb=base.predict_proba(Xte);pn=neural.predict_proba(np.c_[Xte,Nte])
 nllb=float(log_loss(Yte,pb,labels=base[-1].classes_));nlln=float(log_loss(Yte,pn,labels=neural[-1].classes_))
 # future neural models, target normalized using training animals only
 ym=NYtr.mean(0);ys=np.where(NYtr.std(0)>1e-6,NYtr.std(0),1.)
 ztr=(NYtr-ym)/ys;zte=(NYte-ym)/ys
 rb=make_pipeline(StandardScaler(),Ridge(alpha=10.0));rn=make_pipeline(StandardScaler(),Ridge(alpha=10.0))
 rb.fit(Xtr,ztr);rn.fit(np.c_[Xtr,Ntr],ztr)
 pred_b=rb.predict(Xte);pred_n=rn.predict(np.c_[Xte,Nte])
 mse_b=float(np.mean((pred_b-zte)**2));mse_n=float(np.mean((pred_n-zte)**2))
 # standardized persistence from current neural
 p_persist=(Nte-ym)/ys; mse_p=float(np.mean((p_persist-zte)**2))
 folds.append({"held_out_animal":held,"n":len(Yte),
   "behavior_base_nll":nllb,"behavior_neural_nll":nlln,"behavior_nll_gain":nllb-nlln,
   "behavior_base_ba":float(balanced_accuracy_score(Yte,base.predict(Xte))),
   "behavior_neural_ba":float(balanced_accuracy_score(Yte,neural.predict(np.c_[Xte,Nte]))),
   "future_neural_base_mse":mse_b,"future_neural_with_current_neural_mse":mse_n,
   "future_neural_mse_gain":mse_b-mse_n,"persistence_mse":mse_p})

def stat(key):
 x=np.array([r[key] for r in folds],float)
 try:p=float(wilcoxon(x,alternative="greater").pvalue)
 except:p=None
 return {"n":len(x),"mean":float(x.mean()),"median":float(np.median(x)),"positive":int((x>0).sum()),"negative":int((x<0).sum()),"wilcoxon_one_sided_p":p,"values":x.tolist()}

out={"generated_at":"2026-10-06","status":"MFP_FAST_INFORMATION_GATE_NOT_FINAL_MODEL",
 "n_animals":len(animals),"n_days":len(seqs),"n_events":int(sum(len(s["rows"]) for s in seqs)),
 "common_regions_exact_name":common,"behavior_ontology":BEH,"context_ontology":CTX,
 "summary":{"behavior_nll_gain_from_neural":stat("behavior_nll_gain"),"future_neural_mse_gain":stat("future_neural_mse_gain")},
 "folds":folds,
 "guardrail":"Leave-one-animal-out with animal as inferential unit; all normalization/model fitting is training-animal only. This fast linear gate decides whether neural channels contain transferable incremental information before deep-model confirmation."}
OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out["summary"],indent=2))
