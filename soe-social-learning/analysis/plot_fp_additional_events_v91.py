from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; A=ROOT/"assets"
fix=pd.read_csv(r"C:\Users\Public\fp_psth_controls_v90\FP_PSTH_CONTROL_EVENTS_v90.csv.gz")
phase=pd.read_csv(r"C:\Users\Public\fp_psth_controls_v91\FP_CONTROL_BOUT_PHASE_v91.csv.gz")
phase_stats=pd.read_csv(r"C:\Users\Public\fp_psth_controls_v91\FP_CONTROL_BOUT_PHASE_STATS_v91.csv")
fixed_stats=pd.read_csv(D/"SOE_FP_EVENT_CONTROL_STATS_v90.csv")
tc=[f"z{i:03d}" for i in range(1,91)]
pc=[f"p{i:03d}" for i in range(101)]
t=np.arange(-3,6,.1); ph=np.linspace(0,100,101)

def curves(frame,cols):
    out=[]
    for an,g in frame.groupby("AnmID"):
        out.append(np.nanmean(g[cols].to_numpy(float),axis=0))
    x=np.vstack(out)
    return np.nanmean(x,axis=0),np.nanstd(x,axis=0,ddof=1)/np.sqrt(x.shape[0]),x.shape[0]

def add(ax,x,frame,cols,color,label):
    m,e,n=curves(frame,cols)
    ax.plot(x,m,color=color,lw=1.4,label=label)
    ax.fill_between(x,m-e,m+e,color=color,alpha=.16,lw=0)

def finish(ax,xlab):
    ax.axhline(0,color=GRAY_LIGHT,lw=.7)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(False)
    ax.set_xlabel(xlab); ax.set_ylabel("DA z-score"); ax.tick_params(labelsize=6.5)

apply_rc(False)
fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
gs=fig.add_gridspec(2,2,left=.16,right=.985,bottom=.13,top=.96,wspace=.47,hspace=.52)

ax=fig.add_subplot(gs[0,0])
add(ax,t,fix[fix.event_type.eq("dem_triggered")],tc,RED,"Triggered")
add(ax,t,fix[fix.event_type.eq("dem_untriggered")],tc,CYAN,"Untriggered")
ax.axvline(0,color=GRAY_MID,lw=.8,ls="--"); ax.set_xlim(-3,5.9); ax.set_title("Demonstrator - fixed",pad=3)
q=fixed_stats[(fixed_stats.left=="dem_triggered")&(fixed_stats.right=="dem_untriggered")&(fixed_stats.window=="post_0_2")].iloc[0]
ax.text(.03,.05,f"0-2 s: {int(q.positive)}/{int(q.n)}, P={q.p:.3f}",transform=ax.transAxes,fontsize=5.5)
ax.legend(frameon=False,fontsize=5.5,loc="upper right"); finish(ax,"Time from event onset (s)"); panel_label(ax,"A")

ax=fig.add_subplot(gs[0,1])
add(ax,ph,phase[phase.event_type.eq("dem_triggered")],pc,RED,"Triggered")
add(ax,ph,phase[phase.event_type.eq("dem_untriggered")],pc,CYAN,"Untriggered")
ax.set_xlim(0,100); ax.set_title("Demonstrator - real bout",pad=3)
q=phase_stats[(phase_stats.left=="dem_triggered")&(phase_stats.window=="phase_whole")].iloc[0]
ax.text(.03,.05,f"whole bout: {int(q.positive)}/{int(q.n)}, P={q.p:.3f}",transform=ax.transAxes,fontsize=5.5)
ax.legend(frameon=False,fontsize=5.5,loc="upper right"); finish(ax,"Bout phase (%)"); panel_label(ax,"B")

ax=fig.add_subplot(gs[1,0])
g=fix[fix.event_type.eq("observer_feeding")]
add(ax,t,g,tc,RED,"Observer feeding")
ax.axvline(0,color=GRAY_MID,lw=.8,ls="--"); ax.set_xlim(-3,5.9); ax.set_title("Own feeding - fixed",pad=3)
q=fixed_stats[(fixed_stats.left=="observer_feeding")&(fixed_stats.window=="post_0_2")].iloc[0]
ax.text(.03,.05,f"post vs pre: {int(q.positive)}/{int(q.n)}, P={q.p:.3f}",transform=ax.transAxes,fontsize=5.5)
finish(ax,"Time from feeding onset (s)"); panel_label(ax,"C")

ax=fig.add_subplot(gs[1,1])
g=phase[phase.event_type.eq("observer_feeding")]
add(ax,ph,g,pc,RED,"Observer feeding")
ax.set_xlim(0,100); ax.set_title("Own feeding - real bout",pad=3)
q=phase_stats[(phase_stats.left=="observer_feeding")&(phase_stats.window=="phase_whole")].iloc[0]
ax.text(.03,.05,f"above zero: {int(q.positive)}/{int(q.n)}, P={q.p:.4f}",transform=ax.transAxes,fontsize=5.5)
finish(ax,"Feeding-bout phase (%)"); panel_label(ax,"D")

for ext in ["png","pdf","svg"]:
    fig.savefig(A/f"SOE_FP_PSTH_additional_events_v91.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)
phase_stats.to_csv(D/"SOE_FP_ADDITIONAL_BOUT_EVENT_STATS_v91.csv",index=False)

rows=[]
for typ,g in fix[fix.event_type.isin(["dem_triggered","dem_untriggered","observer_feeding"])].groupby("event_type"):
    for an,q in g.groupby("AnmID"):
        v=np.nanmean(q[tc].to_numpy(float),axis=0)
        for tt,x in zip(t,v): rows.append(dict(view="fixed",event_type=typ,AnmID=an,x=tt,mean_da=x))
for typ,g in phase.groupby("event_type"):
    for an,q in g.groupby("AnmID"):
        v=np.nanmean(q[pc].to_numpy(float),axis=0)
        for tt,x in zip(ph,v): rows.append(dict(view="bout_phase",event_type=typ,AnmID=an,x=tt,mean_da=x))
pd.DataFrame(rows).to_csv(D/"SOE_FP_ADDITIONAL_EVENT_CURVES_v91.csv",index=False)
print(phase_stats.to_string(index=False))
