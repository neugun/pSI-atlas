# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
SRC=Path(r"C:\Users\Public\fp_psth_v80")
DOUT=ROOT/"data"; AOUT=ROOT/"assets"
TRACE=SRC/"FP_PSTH_ALL_EVENTS_v80.csv"
PHASE=SRC/"FP_BOUT_PHASE_TRACES_v81.csv.gz"
LAT=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da\dudman_policy_update_v1\analysis_events_with_policy_latents.csv.gz")
CREDIT=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da\passive_credit_robustness_v1\trajectory_source.csv.gz")

events=["active","passive","unrewarded"]
trace_cols=[f"z{i:03d}" for i in range(1,91)]
phase_cols=[f"p{i:03d}" for i in range(101)]
t=np.arange(-3,6,0.1); ph=np.linspace(0,100,101)

d=pd.read_csv(TRACE)
d["event_index"]=d.groupby(["SessionANM","event_type"]).cumcount()
d["anchor6"]=pd.to_numeric(d.AnchorStart_FP).round(6)
lat=pd.read_csv(LAT,low_memory=False)
lat["anchor6"]=pd.to_numeric(lat.AnchorStart_FP).round(6)
keep=lat[["SessionANM","anchor6","model_outcome","actor_abs_rpe","actor_abs_update","actor_p_internal"]].drop_duplicates(["SessionANM","anchor6"])
x=d[d.event_type.isin(events)].merge(keep,on=["SessionANM","anchor6"],how="inner",validate="many_to_one")
x=x[x.event_type.eq(x.model_outcome)].copy()

credit=pd.read_csv(CREDIT,low_memory=False)
credit["anchor6"]=pd.to_numeric(credit.AnchorStart_FP).round(6)
ck=credit[["SessionANM","anchor6","absrpe_selected","qdiff_selected"]].drop_duplicates(["SessionANM","anchor6"])
x=x.merge(ck,on=["SessionANM","anchor6"],how="left")

# Only events valid for both DA readouts; preserve the event_index needed for the phase table.
common=pd.read_csv(ROOT/"data"/"fp_da_common_event_v1"/"method_difference_events.csv.gz")
common["anchor6"]=pd.to_numeric(common.AnchorStart_FP).round(6)
keys=set(zip(common.SessionANM.astype(str),common.anchor6,common.model_outcome.astype(str)))
x=x[[(str(s),a,str(o)) in keys for s,a,o in zip(x.SessionANM,x.anchor6,x.model_outcome)]].copy()

phase=pd.read_csv(PHASE,low_memory=False)
phase=phase[phase.common & phase.event_type.isin(events)].copy()

vars=[
    ("actor_p_internal","Sampling policy"),
    ("actor_abs_rpe","Actor |RPE|"),
    ("actor_abs_update","Actor update"),
]
# within-animal median split to avoid between-animal amplitude confounds
for var,_ in vars:
    x[var]=pd.to_numeric(x[var],errors="coerce")
    x[var+"_group"]=x.groupby("AnmID")[var].transform(lambda s: np.where(s>=s.median(),"high","low"))

# carry groups into phase table
phase=phase.merge(
    x[["SessionANM","event_type","event_index","AnmID"]+[v+"_group" for v,_ in vars]].drop_duplicates(["SessionANM","event_type","event_index"]),
    on=["SessionANM","event_type","event_index","AnmID"],how="inner",validate="many_to_one")

def animal_mean(frame, group_col, cols):
    rows=[]
    for (grp,an),g in frame.groupby([group_col,"AnmID"]):
        rows.append((grp,int(an),np.nanmean(g[cols].to_numpy(float),axis=0),len(g)))
    return rows

source=[]
def plot_pair(ax, fixed, group_col, cols, xx, title):
    colors={"high":RED,"low":CYAN}
    for grp in ["high","low"]:
        rows=[r for r in animal_mean(fixed,group_col,cols) if r[0]==grp]
        arr=np.vstack([r[2] for r in rows])
        sigma=1.5 if xx[0] < 0 else 2.0
        arr_display=gaussian_filter1d(arr,sigma=sigma,axis=1,mode="nearest")
        m=np.nanmean(arr_display,axis=0); e=np.nanstd(arr_display,axis=0,ddof=1)/np.sqrt(arr_display.shape[0])
        ax.plot(xx,m,color=colors[grp],lw=1.3,label=f"{grp} (n={arr.shape[0]} animals)")
        ax.fill_between(xx,m-e,m+e,color=colors[grp],alpha=.16,lw=0)
        for j,(tt,val) in enumerate(zip(xx,m)):
            source.append([title,grp,"fixed" if xx[0]<0 else "bout_phase",float(tt),float(val),float(e[j]),arr.shape[0]])
    ax.axhline(0,color=GRAY_LIGHT,lw=.6)
    if xx[0]<0:
        ax.axvline(0,color=GRAY_MID,lw=.75,ls="--"); ax.set_xlim(-3,5.9); ax.set_xlabel("Time from outcome (s)")
    else:
        ax.set_xlim(0,100); ax.set_xlabel("Bout phase (%)")
    ax.set_ylabel("DA z-score"); ax.set_title(title,pad=2); clean_ax(ax)

def render(mobile=False):
    apply_rc(mobile)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(3,2,left=.18,right=.985,bottom=.12,top=.97,wspace=.45,hspace=.58)
    for i,(var,label) in enumerate(vars):
        ax=fig.add_subplot(gs[i,0]); plot_pair(ax,x,var+"_group",trace_cols,t,label); panel_label(ax,chr(65+2*i))
        ax=fig.add_subplot(gs[i,1]); plot_pair(ax,phase,var+"_group",phase_cols,ph,label); panel_label(ax,chr(66+2*i))
        if i==0:
            ax.legend(frameon=False,fontsize=4.8,loc="best")
    return fig

fig=render(False); save_square(fig,AOUT/"SOE_FP_PSTH_model_variables_v88",mobile=False); plt.close(fig)
fig=render(True); save_square(fig,AOUT/"SOE_FP_PSTH_model_variables_v88_mobile",mobile=True,also_vector=False); plt.close(fig)
pd.DataFrame(source,columns=["model_axis","group","view","x","mean_da","sem_da","n_animals"]).to_csv(DOUT/"SOE_FP_PSTH_MODEL_VARIABLES_v88.csv",index=False)
print("events",len(x),"phase rows",len(phase),"animals",x.AnmID.nunique())
print("done v88")

