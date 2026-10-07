# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.ndimage import gaussian_filter1d
from soe_figure_style_v52 import *

R=Path(__file__).resolve().parents[1]
A=R/"assets"; D=R/"data"
main=pd.read_csv(r"C:\Users\Public\fp_psth_v80\FP_PSTH_ALL_EVENTS_v80.csv")
ctrl=pd.read_csv(r"C:\Users\Public\fp_psth_controls_v90\FP_PSTH_CONTROL_EVENTS_v90.csv.gz")
phase=pd.read_csv(r"C:\Users\Public\fp_psth_v80\FP_BOUT_PHASE_TRACES_v81.csv.gz")
tc=[f"z{i:03d}" for i in range(1,91)]
pc=[f"p{i:03d}" for i in range(101)]
t=np.arange(-3,6,.1); ph=np.linspace(0,100,101)

def wp(x):
    x=np.asarray(x,float); x=x[np.isfinite(x)]
    return np.nan if len(x)==0 or np.allclose(x,0) else float(wilcoxon(x).pvalue)
def ac(frame,cols):
    out={}
    for an,g in frame.groupby("AnmID"): out[an]=np.nanmean(g[cols].to_numpy(float),axis=0)
    return out
def summ(curves):
    x=np.vstack(list(curves.values())); return np.nanmean(x,axis=0),np.nanstd(x,axis=0,ddof=1)/np.sqrt(x.shape[0])
def scalar(frame,cols):
    return frame.groupby("AnmID")[cols].mean().mean(axis=1)
def pair_stat(left,right):
    idx=left.index.intersection(right.index); z=(left.loc[idx]-right.loc[idx]).to_numpy(float)
    return len(z),int((z>0).sum()),float(np.mean(z)),wp(z)
def add_curve(ax,x,frame,cols,color,label):
    curves=ac(frame,cols)
    mat=np.vstack(list(curves.values()))
    sigma=1.5 if x[0] < 0 else 2.0
    sm=gaussian_filter1d(mat,sigma=sigma,axis=1,mode="nearest")
    m=np.nanmean(sm,axis=0); e=np.nanstd(sm,axis=0,ddof=1)/np.sqrt(sm.shape[0])
    ax.plot(x,m,color=color,lw=1.4,label=label); ax.fill_between(x,m-e,m+e,color=color,alpha=.16,lw=0)
def finish(ax,xlabel):
    ax.axhline(0,color=GRAY_LIGHT,lw=.7); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(False)
    ax.set_xlabel(xlabel); ax.set_ylabel("DA z-score"); ax.tick_params(labelsize=6.5)

inside=main[main.event_type.eq("observe_inside")]
outside=main[main.event_type.eq("observe_outside")]
rin=ctrl[ctrl.event_type.eq("random_noobserve_inside")]
rout=ctrl[ctrl.event_type.eq("random_noobserve_outside")]
tin=ctrl[ctrl.event_type.eq("dem_transition_inside")]
tout=ctrl[ctrl.event_type.eq("dem_transition_outside")]
pin=phase[phase.event_type.eq("observe_inside")]
pout=phase[phase.event_type.eq("observe_outside")]

mask02=(t>=0)&(t<2); mask06=(t>=0)&(t<6)
stats=[]
for name,l,r in [("observe_inside_vs_random_inside",inside,rin),("observe_inside_vs_observe_outside",inside,outside),
                 ("dem_transition_inside_vs_random_inside",tin,rin),("dem_transition_outside_vs_random_outside",tout,rout)]:
    for win,mask in [("post_0_2",mask02),("post_0_6",mask06)]:
        n,pos,eff,p=pair_stat(scalar(l,list(np.array(tc)[mask])),scalar(r,list(np.array(tc)[mask])))
        stats.append([name,win,n,pos,eff,p])
for win,cols in [("phase_0_25",pc[:26]),("phase_whole",pc)]:
    n,pos,eff,p=pair_stat(scalar(pin,cols),scalar(pout,cols)); stats.append(["observe_inside_vs_observe_outside",win,n,pos,eff,p])
S=pd.DataFrame(stats,columns=["comparison","window","n","positive","mean_diff","p"])
S.to_csv(D/"SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv",index=False)

apply_rc(False)
fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
gs=fig.add_gridspec(2,2,left=.16,right=.985,bottom=.13,top=.96,wspace=.48,hspace=.52)

ax=fig.add_subplot(gs[0,0])
add_curve(ax,t,inside,tc,CYAN,"Observe inside"); add_curve(ax,t,rin,tc,GRAY_DARK,"Random no-observe")
ax.axvline(0,color=GRAY_MID,lw=.8,ls="--"); ax.set_xlim(-3,5.9); ax.set_title("Observation > matched control",pad=3,x=.60,fontsize=6.5)
q=S[(S.comparison=="observe_inside_vs_random_inside")&(S.window=="post_0_6")].iloc[0]
ax.text(.03,.05,f"0–6 s: {int(q.positive)}/{int(q.n)}, P={q.p:.3f}",transform=ax.transAxes,fontsize=5.6)
ax.legend(frameon=False,fontsize=5.5,loc="upper left"); finish(ax,"Time from observation onset (s)"); panel_label(ax,"A")

ax=fig.add_subplot(gs[0,1])
add_curve(ax,t,inside,tc,CYAN,"Inside"); add_curve(ax,t,outside,tc,RED,"Outside")
ax.axvline(0,color=GRAY_MID,lw=.8,ls="--"); ax.set_xlim(-3,5.9); ax.set_title("Inside > outside",pad=3,x=.57,fontsize=6.7)
q=S[(S.comparison=="observe_inside_vs_observe_outside")&(S.window=="post_0_2")].iloc[0]
ax.text(.03,.05,f"0–2 s: {int(q.positive)}/{int(q.n)}, P={q.p:.4f}",transform=ax.transAxes,fontsize=5.6)
ax.legend(frameon=False,fontsize=5.5,loc="upper left"); finish(ax,"Time from observation onset (s)"); panel_label(ax,"B")

ax=fig.add_subplot(gs[1,0])
add_curve(ax,ph,pin,pc,CYAN,"Inside"); add_curve(ax,ph,pout,pc,RED,"Outside")
ax.set_xlim(0,100); ax.set_title("Difference persists through bout",pad=3,x=.60,fontsize=6.4)
q=S[(S.comparison=="observe_inside_vs_observe_outside")&(S.window=="phase_whole")].iloc[0]
ax.text(.03,.05,f"whole bout: {int(q.positive)}/{int(q.n)}, P={q.p:.4f}",transform=ax.transAxes,fontsize=5.6)
ax.legend(frameon=False,fontsize=5.5); finish(ax,"Observation-bout phase (%)"); panel_label(ax,"C")

ax=fig.add_subplot(gs[1,1])
# animal-level transition-minus-random difference curves
for l,r,c,label in [(tin,rin,CYAN,"Inside"),(tout,rout,RED,"Outside")]:
    L=ac(l,tc); RR=ac(r,tc); ids=sorted(set(L)&set(RR)); mat=np.vstack([L[i]-RR[i] for i in ids])
    mat=gaussian_filter1d(mat,sigma=1.5,axis=1,mode="nearest")
    m=np.nanmean(mat,axis=0); e=np.nanstd(mat,axis=0,ddof=1)/np.sqrt(len(ids))
    ax.plot(t,m,color=c,lw=1.4,label=label); ax.fill_between(t,m-e,m+e,color=c,alpha=.16,lw=0)
ax.axvline(0,color=GRAY_MID,lw=.8,ls="--"); ax.set_xlim(-3,5.9); ax.set_title("Transitions ≈ matched control",pad=3,x=.60,fontsize=6.4)
qi=S[(S.comparison=="dem_transition_inside_vs_random_inside")&(S.window=="post_0_2")].iloc[0]
qo=S[(S.comparison=="dem_transition_outside_vs_random_outside")&(S.window=="post_0_2")].iloc[0]
ax.text(.03,.05,f"0–2 s: inside P={qi.p:.3f}; outside P={qo.p:.3f}",transform=ax.transAxes,fontsize=5.4)
ax.legend(frameon=False,fontsize=5.5,loc="upper right"); finish(ax,"Time from demonstrator transition (s)"); ax.set_ylabel("DA difference vs random"); panel_label(ax,"D")

for ext in ["png","pdf","svg"]: fig.savefig(A/f"SOE_FP_social_sampling_specificity_v92.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)
print(S.to_string(index=False))
