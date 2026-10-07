# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import wilcoxon

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
ASSET=ROOT/"assets"
EXPORT=Path(r"C:\Users\Public\fp_psth_v80\FP_PSTH_ALL_EVENTS_v80.csv")
GRID=Path(r"C:\Users\Public\fp_psth_v80\FP_PSTH_GRID_v80.csv")
COMMON=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da\fp_da_method_common_events_v1\method_difference_events.csv.gz")
LATENT=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da\dudman_policy_update_v1\analysis_events_with_policy_latents.csv.gz")
CREDIT=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da\passive_credit_robustness_v1\trajectory_source.csv.gz")

COLORS={"active":"#C94F46","passive":"#4C78A8","unrewarded":"#7A7A7A","observe_all":"#6C5FA7"}
TRACE_COLS=[f"z{i:03d}" for i in range(1,91)]
times=pd.read_csv(GRID).iloc[0].to_numpy(float)
d=pd.read_csv(EXPORT)
d["anchor6"]=pd.to_numeric(d.AnchorStart_FP).round(6)
common=pd.read_csv(COMMON)
common["anchor6"]=pd.to_numeric(common.AnchorStart_FP).round(6)
lat=pd.read_csv(LATENT,low_memory=False)
lat["anchor6"]=pd.to_numeric(lat.AnchorStart_FP).round(6)
credit=pd.read_csv(CREDIT,low_memory=False)
credit["anchor6"]=pd.to_numeric(credit.AnchorStart_FP).round(6)

# Outcome rows: use the RL event table as the authority for Active/Passive/Unrewarded identity.
# The legacy row-4 export contains 33 duplicate copies of Active anchors; matching the
# authoritative model_outcome removes those duplicates without discarding any true outcomes.
raw_out=d[d.event_type.isin(["active","passive","unrewarded"])].copy()
lat_keep=lat[["SessionANM","anchor6","model_outcome","actor_rpe","actor_abs_rpe","actor_signed_update","actor_abs_update","actor_p_internal","fast_rpe","fast_abs_rpe"]].drop_duplicates(["SessionANM","anchor6"])
out=raw_out.merge(lat_keep,on=["SessionANM","anchor6"],how="inner",validate="many_to_one")
out=out[out.event_type.eq(out.model_outcome)].copy()
common_keys=common[["SessionANM","anchor6","model_outcome"]].drop_duplicates()
ck=set(zip(common_keys.SessionANM.astype(str),common_keys.anchor6,common_keys.model_outcome.astype(str)))
out["is_common"]=[(str(s),a,str(o)) in ck for s,a,o in zip(out.SessionANM,out.anchor6,out.model_outcome)]
out=out.merge(credit[["SessionANM","anchor6","passive_weight","rpe_selected","absrpe_selected","qdiff_selected"]].drop_duplicates(["SessionANM","anchor6"]),
              on=["SessionANM","anchor6"],how="left")

# Authoritative counts.
count_rows=[]
for scope,sub in [("all",out),("common",out[out.is_common])]:
    for typ,g in sub.groupby("event_type"):
        count_rows.append(dict(scope=scope,event_type=typ,n_events=len(g),n_animals=g.AnmID.nunique(),
                               median_duration=float(g.ActionBoutDur_FP.median()),
                               q25_duration=float(g.ActionBoutDur_FP.quantile(.25)),
                               q75_duration=float(g.ActionBoutDur_FP.quantile(.75))))
counts=pd.DataFrame(count_rows)
counts.to_csv(DATA/"SOE_FP_PSTH_EVENT_COUNTS_v82.csv",index=False)

def animal_curves(frame, group_col="event_type"):
    rows=[]
    for (grp,an),g in frame.groupby([group_col,"AnmID"]):
        arr=g[TRACE_COLS].to_numpy(float)
        m=np.nanmean(arr,axis=0)
        for j,t in enumerate(times):
            rows.append({group_col:grp,"AnmID":an,"time_s":t,"mean_da":m[j],"n_events":len(g)})
    return pd.DataFrame(rows)

def group_summary(ac, group_col):
    z=[]
    for (grp,t),g in ac.groupby([group_col,"time_s"]):
        x=g.mean_da.to_numpy(float)
        z.append({group_col:grp,"time_s":t,"mean_da":np.nanmean(x),
                  "sem_da":np.nanstd(x,ddof=1)/np.sqrt(np.sum(np.isfinite(x))),
                  "n_animals":np.sum(np.isfinite(x))})
    return pd.DataFrame(z)

ac_all=animal_curves(out)
ac_common=animal_curves(out[out.is_common])
group_summary(ac_all,"event_type").to_csv(DATA/"SOE_FP_PSTH_OUTCOME_ALL_ANIMAL_MEAN_v82.csv",index=False)
group_summary(ac_common,"event_type").to_csv(DATA/"SOE_FP_PSTH_OUTCOME_COMMON_ANIMAL_MEAN_v82.csv",index=False)

def set_ax(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.grid(False); ax.tick_params(labelsize=7)
    ax.axvline(0,color="0.25",lw=.8,ls="--",zorder=0)
    ax.set_xlim(-3,5.9)

def plot_outcome_psth(frame, fname, title_suffix):
    fig,axs=plt.subplots(1,3,figsize=(8.4,2.8),sharex=True,sharey=True)
    for ax,typ in zip(axs,["active","passive","unrewarded"]):
        g=frame[frame.event_type.eq(typ)]
        ac=animal_curves(g)
        s=group_summary(ac,"event_type")
        x=s.time_s.to_numpy(); y=s.mean_da.to_numpy(); e=s.sem_da.to_numpy()
        ax.plot(x,y,lw=1.5,color=COLORS[typ])
        ax.fill_between(x,y-e,y+e,alpha=.18,color=COLORS[typ],lw=0)
        dur=float(g.ActionBoutDur_FP.median()); q25=float(g.ActionBoutDur_FP.quantile(.25)); q75=float(g.ActionBoutDur_FP.quantile(.75))
        ax.axvspan(max(0,q25),min(5.9,q75),color="0.5",alpha=.08,lw=0)
        if 0<dur<5.9: ax.axvline(dur,color="0.45",lw=.8)
        ax.set_title(f"{typ.capitalize()}\n{len(g)} events · {g.AnmID.nunique()} animals",fontsize=8)
        ax.set_xlabel("Time from event onset (s)",fontsize=7); set_ax(ax)
    axs[0].set_ylabel("DA z-score",fontsize=7)
    fig.suptitle(title_suffix,fontsize=9,y=.995)
    fig.tight_layout()
    for ext in ["png","pdf","svg"]: fig.savefig(ASSET/f"{fname}.{ext}",dpi=250,bbox_inches="tight")
    plt.close(fig)

plot_outcome_psth(out,"SOE_FP_PSTH_outcomes_all_v82","Outcome-aligned VTA dopamine · all valid events")
plot_outcome_psth(out[out.is_common],"SOE_FP_PSTH_outcomes_common_v82","Outcome-aligned VTA dopamine · same events for both FP→DA readouts")

# Trial heatmaps on common events, sorted within outcome by real bout duration.
fig,axs=plt.subplots(1,3,figsize=(8.4,3.2),sharex=True)
heat_sources=[]
for ax,typ in zip(axs,["active","passive","unrewarded"]):
    g=out[out.is_common & out.event_type.eq(typ)].sort_values("ActionBoutDur_FP").copy()
    X=g[TRACE_COLS].to_numpy(float)
    # robust common scale per outcome, avoid a few extreme trials dominating
    lim=np.nanpercentile(np.abs(X),97)
    im=ax.imshow(X,aspect="auto",interpolation="nearest",extent=[times.min(),times.max(),len(g),0],
                 cmap="RdBu_r",vmin=-lim,vmax=lim)
    ax.axvline(0,color="k",lw=.7,ls="--")
    end=np.clip(g.ActionBoutDur_FP.to_numpy(float),0,times.max())
    ax.plot(end,np.arange(len(g))+.5,color="k",lw=.55)
    ax.set_title(f"{typ.capitalize()} · {len(g)} common events",fontsize=8)
    ax.set_xlabel("Time (s)",fontsize=7); ax.set_ylabel("Trials sorted by bout duration",fontsize=7)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(False)
    heat_sources.append(g[["SessionANM","AnmID","AnchorStart_FP","ActionBoutDur_FP","event_type"]])
fig.tight_layout()
for ext in ["png","pdf","svg"]: fig.savefig(ASSET/f"SOE_FP_PSTH_outcome_heatmaps_common_v82.{ext}",dpi=250,bbox_inches="tight")
plt.close(fig)
pd.concat(heat_sources).to_csv(DATA/"SOE_FP_PSTH_COMMON_HEATMAP_INDEX_v82.csv",index=False)

# Build next-observation table: first observe_all after an outcome, only if it occurs before the next outcome.
obs=d[d.event_type.eq("observe_all")].copy()
next_rows=[]
for sid,go in out.groupby("SessionANM"):
    go=go.sort_values("AnchorStart_FP")
    oo=obs[obs.SessionANM.eq(sid)].sort_values("AnchorStart_FP")
    ot=oo.AnchorStart_FP.to_numpy(float)
    oidx=oo.index.to_numpy()
    starts=go.AnchorStart_FP.to_numpy(float)
    for pos,(idx,row) in enumerate(go.iterrows()):
        t=float(row.AnchorStart_FP)
        j=np.searchsorted(ot,t,side="right")
        if j>=len(ot): continue
        tobs=float(ot[j])
        tnext=float(starts[pos+1]) if pos+1<len(starts) else np.inf
        if tobs>=tnext: continue
        rr=oo.loc[oidx[j]]
        next_rows.append(dict(SessionANM=sid,AnmID=row.AnmID,previous_outcome=row.event_type,
                              outcome_start=t,next_observe_start=tobs,latency_s=tobs-t,
                              observe_index=rr.name))
nextobs=pd.DataFrame(next_rows)
nextobs.to_csv(DATA/"SOE_FP_NEXT_OBSERVE_AFTER_OUTCOME_v82.csv",index=False)

if len(nextobs):
    om=obs.reset_index().rename(columns={"index":"observe_index"})
    no=nextobs.merge(om[["observe_index"]+TRACE_COLS],on="observe_index",how="left")
    no_ac=animal_curves(no.rename(columns={"previous_outcome":"grp"}),group_col="grp")
    no_sum=group_summary(no_ac,"grp")
    no_sum.to_csv(DATA/"SOE_FP_PSTH_NEXT_OBSERVE_BY_PREV_OUTCOME_v82.csv",index=False)
    fig,ax=plt.subplots(figsize=(3.3,3.3))
    for typ in ["active","passive","unrewarded"]:
        s=no_sum[no_sum.grp.eq(typ)]
        if s.empty: continue
        x=s.time_s.to_numpy(); y=s.mean_da.to_numpy(); e=s.sem_da.to_numpy()
        ax.plot(x,y,lw=1.4,color=COLORS[typ],label=f"{typ} (n={int((nextobs.previous_outcome==typ).sum())})")
        ax.fill_between(x,y-e,y+e,color=COLORS[typ],alpha=.15,lw=0)
    ax.set_xlabel("Time from next Observe onset (s)",fontsize=7); ax.set_ylabel("DA z-score",fontsize=7)
    ax.legend(frameon=False,fontsize=6); set_ax(ax); fig.tight_layout()
    for ext in ["png","pdf","svg"]: fig.savefig(ASSET/f"SOE_FP_PSTH_next_observe_by_previous_outcome_v82.{ext}",dpi=250,bbox_inches="tight")
    plt.close(fig)

# Model variables are tested with held-animal prediction and temporal adjudication elsewhere.
# We intentionally do not publish naive high/low latent PSTHs here: an unbalanced split is
# confounded by outcome identity, while within-animal × outcome-balanced splits do not show
# an independent amplitude effect. The raw event PSTHs below remain model-free.

# Brief machine-readable summary.
summary={
    "all_events_exported":int(len(d)),
    "outcome_events":int(len(out)),
    "common_outcome_events":int(out.is_common.sum()),
    "animals":int(d.AnmID.nunique()),
    "next_observe_events":int(len(nextobs)),
}
pd.Series(summary).to_csv(DATA/"SOE_FP_PSTH_PIPELINE_SUMMARY_v82.csv",header=["value"])
print(summary)
print(counts.to_string(index=False))
print("DONE v82")
