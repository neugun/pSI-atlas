# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np,pandas as pd,json,matplotlib,os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import sem
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; ASSETS=ROOT/"assets"
SRC=Path(os.environ["SOE_FROZEN_RL_ROOT"]).expanduser()  # Set to the local frozen Codex model root.
raw=pd.read_csv(SRC/"neural_da/dudman_policy_update_v1/analysis_events_with_policy_latents.csv.gz",low_memory=False)
old=raw[np.isfinite(raw.DA_Post06_AUCperSec)&np.isfinite(raw.DA_ActionBout_AUCperSec)&(raw.ActionBoutDur_FP>=.05)].copy()
obs=old[old.ObsBoutDur_FP.notna() & old.DA_ObsBout_AUCperSec.notna() & (old.action_observe==1)].copy()
assert len(old)==1371 and len(obs)==821
base=SRC/"neural_da/fp_da_TRIPLE_MATCHED_QC_v4"
m=pd.read_csv(base/"passive_credit_common_event_contrasts.csv")
sumtab=m[m.comparison.isin(["update_selected_vs_w0p75","update_selected_vs_w1p0","update_selected_vs_baseline"])].copy()
sumtab.to_csv(DATA/"SOE_VTA_true_obs_post_action_credit_comparisons_v126.csv",index=False)
outcomes=obs.groupby(["model_outcome","action_observe"],dropna=False).size().reset_index(name="n")
outcomes.to_csv(DATA/"SOE_VTA_true_obs_event_outcome_counts_v126.csv",index=False)
meta=dict(n_action_interval=1371,n_real_obs=821,n_no_observe=550,med_extended_s=float(old.ActionBoutDur_FP.median()),
med_real_obs_s=float(obs.ObsBoutDur_FP.median()),real_obs_q25=float(obs.ObsBoutDur_FP.quantile(.25)),real_obs_q75=float(obs.ObsBoutDur_FP.quantile(.75)),
fraction_action_gt6=float((old.ActionBoutDur_FP>6).mean()),n_obs_ending_before_anchor=int((obs.ObsBoutEnd_FP<obs.AnchorStart_FP).sum()),n_obs_ending_after_anchor=int((obs.ObsBoutEnd_FP>obs.AnchorStart_FP).sum()),
n_action_fixed100=int(np.isclose(old.ActionBoutDur_FP,100.,atol=.05).sum()),no_baseline_improvement_n=int(sumtab[(sumtab.target=="DA_ActionBout_AUCperSec")&(sumtab.comparison=="update_selected_vs_baseline")].wins_selected.iloc[0]))
(DATA/"SOE_VTA_real_obs_interval_audit_v126.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":False,"pdf.fonttype":42,"svg.fonttype":"none"})
red="#B32C32";cyan="#1597A6";gray="#8F99A2";ink="#222222"
fig,axes=plt.subplots(2,2,figsize=(8.3,8.3))
ax=axes[0,0]
bins=np.logspace(np.log10(.3),np.log10(550),200)
for vals,lab,color in [(old.ActionBoutDur_FP,"Extended interval (1371)",gray),(obs.ObsBoutDur_FP,"True observation (821)",red)]:
 a=np.sort(vals.to_numpy(float)); ax.plot(a,np.arange(1,len(a)+1)/len(a),lw=1.8,color=color,label=lab)
ax.set_xscale("log");ax.set(xlim=(.3,550),ylim=(0,1),xlabel="Interval duration (seconds)",ylabel="Cumulative fraction",title="A · Duration is not the same")
ax.legend(frameon=False,loc="lower right",fontsize=7)
ax=axes[0,1]
anchor=13.005440
parts=[("True Obs",8.827277,11.922119,red),("Fixed 0-6",anchor,anchor+6,cyan),("Extended",anchor,43.531708,gray)]
for i,(label,st,en,col) in enumerate(parts):
 ax.broken_barh([(st-anchor,en-st)],(2-i-.30,.60),facecolors=col,edgecolors="none")
ax.axvline(0,lw=.85,color=ink)
ax.set(xlim=(-5,33),ylim=(-.5,2.9),xlabel="Seconds relative to outcome anchor",title="B · Real event (ANM18, session D16)")
ax.set_yticks([0,1,2],["Extended","Fixed 0–6","True Obs"]);ax.tick_params(axis="y",length=0)
ax=axes[1,0]
names=[("DA_ActionBout_AUCperSec","Extended"),("DA_ObsBout_AUCperSec","True Obs"),("DA_Post06_AUCperSec","Fixed 0–6")]
values=[0.75,1.0];width=.22
for k,(key,lab) in enumerate(names):
 points=[]
 for w in ["w0p75","w1p0"]:
  q=sumtab[(sumtab.target==key)&(sumtab.comparison=="update_selected_vs_"+w)].iloc[0]
  points.append((int(q.wins_selected),float(q.p)))
 x=np.arange(2)+(k-1)*width
 ax.bar(x,[a[0] for a in points],width=width*.9,color=[gray,red,cyan][k],edgecolor="none",label=lab)
 for xx,(n,p) in zip(x,points):ax.text(xx,n+.24,f"{n}/9",ha="center",fontsize=6.6)
ax.set(xlim=(-.65,1.65),ylim=(0,10),ylabel="Animals favoring selected credit (of 9)",title="C · Same 821 events / 9 animals")
ax.set_xticks([0,1],["vs fixed 0.75","vs fixed 1.0"]);ax.legend(frameon=False,fontsize=7)
ax=axes[1,1]
sub=sumtab[sumtab.comparison=="update_selected_vs_baseline"]
n=[int(sub[sub.target==key].wins_selected.iloc[0]) for key,_ in names]
ax.bar(np.arange(3),n,width=.42,color=[gray,red,cyan],edgecolor="none")
for i,(key,lab) in enumerate(names):
 p=float(sub[sub.target==key].p.iloc[0])
 ax.text(i,n[i]+.22,f"{n[i]}/9\nP={p:.3f}"+("\n7/9 worse" if key=="DA_ObsBout_AUCperSec" else ""),ha="center",fontsize=7)
ax.set(xlim=(-.6,2.6),ylim=(0,10),ylabel="Animals improved vs history baseline",title="D · Selected credit vs no-credit baseline")
ax.set_xticks(range(3),["Extended","True Obs","Fixed 0–6"])
fig.suptitle("VTA DA: actual observation versus extended action interval",fontsize=11,y=.985)
fig.subplots_adjust(left=.12,right=.985,top=.94,bottom=.09,wspace=.34,hspace=.40)
for ext in ["png","svg","pdf"]:fig.savefig(ASSETS/("SOE_VTA_true_obs_interval_audit_v126."+ext),dpi=260)
print("AUDIT",meta)
print("CREDIT",sumtab.to_string(index=False))
print("FIGURE",ASSETS/"SOE_VTA_true_obs_interval_audit_v126.png")
