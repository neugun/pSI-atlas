# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/"assets"; DATA=ROOT/"data"
CTRL=Path(r"C:\Users\Public\fp_psth_controls_v90\FP_PSTH_CONTROL_EVENTS_v90.csv.gz")
MAIN=Path(r"C:\Users\Public\fp_psth_v80\FP_PSTH_ALL_EVENTS_v80.csv")
GRID=Path(r"C:\Users\Public\fp_psth_v80\FP_PSTH_GRID_v80.csv")
tc=[f"z{i:03d}" for i in range(1,91)]
t=pd.read_csv(GRID).iloc[0].to_numpy(float)
c=pd.read_csv(CTRL)
m=pd.read_csv(MAIN)
keep=m[m.event_type.isin(["observe_inside","observe_outside"])].copy()
d=pd.concat([c,keep],ignore_index=True,sort=False)

def animal_curve(frame):
    rows=[]
    for an,g in frame.groupby("AnmID"):
        x=g[tc].to_numpy(float)
        mu=np.nanmean(x,axis=0)
        rows.append((an,mu,len(g)))
    return rows

def summary(frame):
    ac=animal_curve(frame)
    mat=np.vstack([x[1] for x in ac])
    return np.nanmean(mat,axis=0), np.nanstd(mat,axis=0,ddof=1)/np.sqrt(mat.shape[0]), mat.shape[0], ac

def win_animal(frame,lo,hi):
    mask=(t>=lo)&(t<hi)
    rows=[]
    for an,g in frame.groupby("AnmID"):
        x=np.nanmean(g[tc].to_numpy(float)[:,mask],axis=1)
        rows.append((an,float(np.nanmean(x))))
    return pd.Series(dict(rows),dtype=float)

def safe_p(x):
    x=np.asarray(x,float); x=x[np.isfinite(x)]
    return np.nan if len(x)==0 or np.allclose(x,0) else float(wilcoxon(x).pvalue)

pairs=[
("observe_inside","random_noobserve_inside","Observation inside","Random no-observe inside"),
("observe_outside","random_noobserve_outside","Observation outside","Random no-observe outside"),
("dem_transition_inside","random_noobserve_inside","Demonstrator transition inside","Random no-observe inside"),
("dem_transition_outside","random_noobserve_outside","Demonstrator transition outside","Random no-observe outside"),
("dem_triggered","dem_untriggered","Demonstrator-triggered","Demonstrator-untriggered"),
]
stat=[]
for left,right,ll,rr in pairs:
    for w,lo,hi in [("pre_-1_0",-1,0),("post_0_2",0,2),("post_0_6",0,6)]:
        a=win_animal(d[d.event_type.eq(left)],lo,hi)
        b=win_animal(d[d.event_type.eq(right)],lo,hi)
        idx=a.index.intersection(b.index)
        z=(a.loc[idx]-b.loc[idx]).to_numpy(float)
        stat.append(dict(window=w,left=left,right=right,n=len(idx),mean_diff=np.nanmean(z),
                         median_diff=np.nanmedian(z),positive=int(np.sum(z>0)),p=safe_p(z)))
# observer feeding change from its own pre-state
for w,lo,hi in [("post_0_2",0,2),("post_0_6",0,6)]:
    post=win_animal(d[d.event_type.eq("observer_feeding")],lo,hi)
    pre=win_animal(d[d.event_type.eq("observer_feeding")],-1,0)
    idx=post.index.intersection(pre.index); z=(post.loc[idx]-pre.loc[idx]).to_numpy(float)
    stat.append(dict(window=w,left="observer_feeding",right="own_pre_-1_0",n=len(idx),mean_diff=np.nanmean(z),
                     median_diff=np.nanmedian(z),positive=int(np.sum(z>0)),p=safe_p(z)))
stats=pd.DataFrame(stat)
stats.to_csv(DATA/"SOE_FP_EVENT_CONTROL_STATS_v90.csv",index=False)

# compact animal-level source curves
src=[]
for typ,g in d.groupby("event_type"):
    for an,mu,n in animal_curve(g):
        for tt,v in zip(t,mu): src.append(dict(event_type=typ,AnmID=an,time_s=tt,mean_da=v,n_events=n))
pd.DataFrame(src).to_csv(DATA/"SOE_FP_EVENT_CONTROL_ANIMAL_CURVES_v90.csv",index=False)

colors={"observe_inside":CYAN,"observe_outside":RED,"random_noobserve_inside":GRAY_DARK,
        "random_noobserve_outside":GRAY_DARK,"dem_transition_inside":CYAN,"dem_transition_outside":RED,
        "dem_triggered":RED,"dem_untriggered":CYAN,"observer_feeding":RED}
panels=[
("observe_inside","random_noobserve_inside","Observation inside"),
("observe_outside","random_noobserve_outside","Observation outside"),
("dem_transition_inside","random_noobserve_inside","Dem transition inside"),
("dem_transition_outside","random_noobserve_outside","Dem transition outside"),
("dem_triggered","dem_untriggered","Demonstrator events"),
("observer_feeding",None,"Observer feeding"),
]
fig=plt.figure(figsize=(7.0,7.0))
gs=fig.add_gridspec(3,2,left=.12,right=.985,bottom=.10,top=.965,wspace=.34,hspace=.48)
letters="ABCDEF"
for k,(a,b,title) in enumerate(panels):
    ax=fig.add_subplot(gs[k//2,k%2])
    for typ,lab in [(a,a.replace("_"," ")),(b,b.replace("_"," ") if b else None)]:
        if typ is None: continue
        g=d[d.event_type.eq(typ)]
        y,e,n,_=summary(g)
        ax.plot(t,y,lw=1.45,color=colors.get(typ,GRAY_DARK),label=f"{lab} (n={len(g)})")
        ax.fill_between(t,y-e,y+e,color=colors.get(typ,GRAY_DARK),alpha=.15,lw=0)
    ax.axvline(0,color=GRAY_MID,lw=.8,ls="--"); ax.axhline(0,color=GRAY_LIGHT,lw=.7)
    ax.set_xlim(-3,5.9); ax.set_title(title,fontsize=8,pad=3)
    ax.set_xlabel("Time from event (s)",fontsize=7); ax.set_ylabel("DA z-score",fontsize=7)
    ax.legend(frameon=False,fontsize=5.5,loc="upper right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(False)
    ax.tick_params(labelsize=6.5); panel_label(ax,letters[k])
    if b:
        q=stats[(stats.window=="post_0_2")&(stats.left==a)&(stats.right==b)].iloc[0]
        ax.text(.02,.03,f"0–2 s: {int(q.positive)}/{int(q.n)} positive, P={q.p:.3f}",
                transform=ax.transAxes,ha="left",va="bottom",fontsize=5.3,color=GRAY_DARK)
    else:
        q=stats[(stats.window=="post_0_2")&(stats.left=="observer_feeding")].iloc[0]
        ax.text(.02,.03,f"post vs pre: {int(q.positive)}/{int(q.n)}, P={q.p:.3f}",
                transform=ax.transAxes,ha="left",va="bottom",fontsize=5.3,color=GRAY_DARK)
fig.tight_layout()
for ext in ["png","pdf","svg"]:
    fig.savefig(ASSET/f"SOE_FP_PSTH_event_controls_v90.{ext}",dpi=250,bbox_inches="tight")
plt.close(fig)

print(stats.to_string(index=False))
print("events",d.groupby("event_type").size().to_dict())
