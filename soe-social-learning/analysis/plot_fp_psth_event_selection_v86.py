# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; A=ROOT/"assets"
ALL=pd.read_csv(D/"SOE_FP_PSTH_OUTCOME_ALL_ANIMAL_MEAN_v82.csv")
COM=pd.read_csv(D/"SOE_FP_PSTH_OUTCOME_COMMON_ANIMAL_MEAN_v82.csv")
CNT=pd.read_csv(D/"SOE_FP_PSTH_EVENT_COUNTS_v82.csv")
events=["active","passive","unrewarded"]
labels={"active":"Active","passive":"Passive","unrewarded":"Unrewarded"}
colors={"active":CYAN,"passive":RED,"unrewarded":GRAY_DARK}

def n_for(scope,event):
    q=CNT[(CNT.scope.eq(scope))&(CNT.event_type.eq(event))]
    return int(q.iloc[0].n_events)

def render():
    apply_rc(False)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(2,3,left=.14,right=.985,bottom=.13,top=.96,wspace=.40,hspace=.48)
    for i,(scope,df) in enumerate([("all",ALL),("common",COM)]):
        for j,e in enumerate(events):
            ax=fig.add_subplot(gs[i,j])
            q=df[df.event_type.eq(e)].sort_values("time_s")
            x=q.time_s.to_numpy(); y=q.mean_da.to_numpy(); se=q.sem_da.to_numpy()
            y=gaussian_filter1d(y,sigma=1.5,mode="nearest")
            se=gaussian_filter1d(se,sigma=1.5,mode="nearest")
            ax.plot(x,y,color=colors[e],lw=1.35)
            ax.fill_between(x,y-se,y+se,color=colors[e],alpha=.16,lw=0)
            ax.axvline(0,color=GRAY_MID,lw=.7,ls="--"); ax.axhline(0,color=GRAY_LIGHT,lw=.6)
            ax.set_xlim(-3,5.9); ax.set_title(f"{labels[e]} · n={n_for(scope,e)}",fontsize=6.7,pad=2)
            ax.set_xlabel("Time from outcome (s)",fontsize=6.2)
            if j==0:
                ax.set_ylabel(("All valid outcomes\n" if i==0 else "Same 1,371 events\n")+"DA z-score",fontsize=6.4)
            clean_ax(ax); ax.tick_params(labelsize=5.8)
            if j==0: panel_label(ax,"A" if i==0 else "B")
    return fig

fig=render()
save_square(fig,A/"SOE_FP_PSTH_event_selection_v86",mobile=False)
plt.close(fig)
print("event-selection PSTH v86 done")
