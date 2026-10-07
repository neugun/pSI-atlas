# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.ndimage import gaussian_filter1d
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; A=ROOT/"assets"
S=pd.read_csv(D/"SOE_FP_PSTH_ANIMAL_CURVES_v82.csv")
events=["active","passive","unrewarded"]
labels={"active":"Active","passive":"Passive","unrewarded":"Unrewarded"}
colors={"active":CYAN,"passive":RED,"unrewarded":GRAY_DARK}

fixed=S[S.analysis.eq("next_observe_fixed")].copy()
phase=S[S.analysis.eq("next_observe_bout_phase")].copy()

def wide_window(frame,lo,hi):
    q=frame[(frame.x>=lo)&(frame.x<hi)].groupby(["AnmID","condition"]).DA_z.mean().unstack()
    return q

pre=wide_window(fixed,-1,0)
post=wide_window(fixed,0,2)
early=wide_window(phase,0,25)
whole=wide_window(phase,0,101)

stats=[]
for name,w in [("pre_-1_0",pre),("post_0_2",post),("phase_0_25",early),("phase_whole",whole)]:
    for left,right in [("active","unrewarded"),("passive","unrewarded"),("active","passive")]:
        q=w[[left,right]].dropna(); diff=q[left]-q[right]
        stats.append([name,left,right,len(q),float(diff.mean()),float(diff.median()),float(wilcoxon(diff).pvalue),int((diff>0).sum())])
stats_df=pd.DataFrame(stats,columns=["window","left","right","n","mean_diff","median_diff","p","positive"])
stats_df.to_csv(D/"SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv",index=False)
def pval(window,left,right):
    return float(stats_df[(stats_df.window.eq(window))&(stats_df.left.eq(left))&(stats_df.right.eq(right))].iloc[0].p)

def curve(frame,condition):
    q=frame[frame.condition.eq(condition)].pivot(index="AnmID",columns="x",values="DA_z").sort_index(axis=1)
    x=q.columns.to_numpy(float); arr=q.to_numpy(float)
    sigma=1.5 if x[0] < 0 else 2.0
    arr=gaussian_filter1d(arr,sigma=sigma,axis=1,mode="nearest")
    m=np.nanmean(arr,axis=0); s=np.nanstd(arr,axis=0,ddof=1)/np.sqrt(arr.shape[0])
    return x,m,s

def bar3(ax,w,title,ylabel,ann):
    order=events; x=np.arange(3,dtype=float)
    q=w[order].dropna()
    for _,r in q.iterrows():
        ax.plot(x,r.to_numpy(float),color=GRAY_LIGHT,lw=.7,zorder=1)
    vals=[q[e].to_numpy(float) for e in order]
    means=[v.mean() for v in vals]; errs=[sem(v) for v in vals]
    ax.bar(x,means,width=.50,color=[colors[e] for e in order],edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.8,capsize=2,capthick=.8,zorder=3)
    ax.axhline(0,color=GRAY_LIGHT,lw=.6)
    ax.set_xticks(x); ax.set_xticklabels(["Active\nprev.","Passive\nprev.","Unrewarded\nprev."],rotation=0); ax.tick_params(axis="x",labelsize=5.8)
    ax.set_ylabel(ylabel); ax.set_title(title,pad=2)
    ax.text(.03,.97,ann,transform=ax.transAxes,ha="left",va="top",fontsize=5.2)
    clean_ax(ax)

def render(mobile=False):
    apply_rc(mobile)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(2,2,left=.18,right=.985,bottom=.13,top=.965,wspace=.46,hspace=.52)
    ax=fig.add_subplot(gs[0,0])
    for e in events:
        x,m,s=curve(fixed,e)
        ax.plot(x,m,color=colors[e],lw=1.35,label=f"after {labels[e]}")
        ax.fill_between(x,m-s,m+s,color=colors[e],alpha=.16,lw=0)
    ax.axvline(0,color=GRAY_MID,lw=.75,ls="--"); ax.axhline(0,color=GRAY_LIGHT,lw=.6)
    ax.set_xlim(-3,5.9); ax.set_xlabel("Time from observation (s)"); ax.set_ylabel("DA z-score")
    ax.set_title("Previous outcome persists",pad=2); ax.legend(frameon=False,fontsize=5.0); clean_ax(ax); panel_label(ax,"A")

    ax=fig.add_subplot(gs[0,1])
    bar3(ax,pre,"Before next observation","DA z-score, −1–0 s",
         f"Active vs Unrewarded  P={pval('pre_-1_0','active','unrewarded'):.3f}\nPassive vs Unrewarded  P={pval('pre_-1_0','passive','unrewarded'):.3f}\nPassive vs Active  P={pval('pre_-1_0','active','passive'):.3f}")
    panel_label(ax,"B")

    ax=fig.add_subplot(gs[1,0])
    bar3(ax,post,"After next observation","DA z-score, 0–2 s",
         f"Active vs Unrewarded  P={pval('post_0_2','active','unrewarded'):.3f}\nPassive vs Unrewarded  P={pval('post_0_2','passive','unrewarded'):.3f}")
    panel_label(ax,"C")

    ax=fig.add_subplot(gs[1,1])
    for e in events:
        x,m,s=curve(phase,e)
        ax.plot(x,m,color=colors[e],lw=1.35,label=f"after {labels[e]}")
        ax.fill_between(x,m-s,m+s,color=colors[e],alpha=.16,lw=0)
    ax.axhline(0,color=GRAY_LIGHT,lw=.6); ax.set_xlim(0,100)
    ax.set_xlabel("Observation-bout phase (%)"); ax.set_ylabel("DA z-score")
    ax.set_title("Across observation bout",pad=2)
    ax.text(.03,.97,f"Early 25%:\nActive > Unrewarded  P={pval('phase_0_25','active','unrewarded'):.3f}\nPassive > Unrewarded  P={pval('phase_0_25','passive','unrewarded'):.3f}",
            transform=ax.transAxes,ha="left",va="top",fontsize=5.0)
    clean_ax(ax); panel_label(ax,"D")
    return fig

fig=render(False); save_square(fig,A/"SOE_FP_next_observe_memory_v83",mobile=False); plt.close(fig)
fig=render(True); save_square(fig,A/"SOE_FP_next_observe_memory_v83_mobile",mobile=True,also_vector=False); plt.close(fig)
