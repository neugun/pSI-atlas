from pathlib import Path
import json, numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, balanced_accuracy_score
from scipy.stats import wilcoxon

ROOT=Path(r"H:\brain_world_model_20261005\external_social_data\calms21_task1_socialworld")
OUT=Path(r"H:\brain_world_model_20261005\push_stage23_clean\soe-social-learning\data\SOCIAL_WORLD_CALMS21_FAST_INFORMATION_GATE_v1.json")
man=json.loads((ROOT/"manifest.json").read_text())
train=[m for m in man["sequences"] if "__train__" in m["file"]]
test=[m for m in man["sequences"] if "__test__" in m["file"]]
STEP=12; H=[1,2,5]

def load(m):
 z=np.load(ROOT/m["file"]); return z["self_state"][::STEP],z["pair_state"][::STEP],z["annotations"][::STEP].astype(int)

def feat(s,p,mode):
 focal=s[:,0]
 if mode=="self_only": return focal
 if mode=="relational": return np.concatenate([focal,s[:,1],p[:,0,1]],1)
 if mode=="partner_shuffle":
  k=max(7,len(s)//3)
  return np.concatenate([focal,np.roll(s[:,1],k,0),np.roll(p[:,0,1],k,0)],1)

modes=["self_only","relational","partner_shuffle"]
results={}
for h in H:
 results[h]={}
 for mode in modes:
  X=[];Y=[]
  for m in train:
   s,p,y=load(m); X.append(feat(s,p,mode)[:-h]);Y.append(y[h:])
  X=np.concatenate(X);Y=np.concatenate(Y)
  model=make_pipeline(StandardScaler(),LogisticRegression(C=.5,max_iter=500,class_weight="balanced",solver="lbfgs"))
  model.fit(X,Y)
  rows=[]
  for m in test:
   s,p,y=load(m); xt=feat(s,p,mode)[:-h]; yt=y[h:]
   pr=model.predict_proba(xt)
   # Ensure columns map to 0..3.
   nll=float(log_loss(yt,pr,labels=model[-1].classes_))
   ba=float(balanced_accuracy_score(yt,model.predict(xt)))
   rows.append({"animal":m["sequence_id"],"n":len(yt),"nll":nll,"balanced_accuracy":ba})
  results[h][mode]=rows

paired={}
for h in H:
 paired[h]={}
 for comp in ["self_only","partner_shuffle"]:
  gain=np.array([results[h][comp][i]["nll"]-results[h]["relational"][i]["nll"] for i in range(len(test))])
  bag=np.array([results[h]["relational"][i]["balanced_accuracy"]-results[h][comp][i]["balanced_accuracy"] for i in range(len(test))])
  try:p=float(wilcoxon(gain,alternative="greater").pvalue)
  except:p=None
  paired[h][comp]={"n":len(gain),"mean_nll_gain":float(gain.mean()),"median_nll_gain":float(np.median(gain)),
    "positive":int((gain>0).sum()),"wilcoxon_one_sided_p":p,
    "mean_balanced_accuracy_gain":float(bag.mean()),"median_ba_gain":float(np.median(bag))}
out={"generated_at":"2026-10-06","status":"FAST_INFORMATION_GATE_NOT_FINAL_MODEL",
 "n_train_animals":len(train),"n_test_animals":len(test),"downsample":STEP,
 "horizons":{"1":"~0.4 s","2":"~0.8 s","5":"~2.0 s"},
 "paired_animal_level":paired,"per_animal":results,
 "guardrail":"Official identity split; fast multinomial gate only. It tests whether partner/relation channels contain transferable incremental information before deep-model confirmation."}
OUT.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(paired,indent=2))
