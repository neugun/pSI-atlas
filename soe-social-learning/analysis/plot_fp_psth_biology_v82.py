# -*- coding: utf-8 -*-
from pathlib import Path
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
SRC=Path(r"C:\Users\Public\fp_psth_v80")
OUT=ROOT/"assets"; DATA=ROOT/"data"
d=pd.read_csv(SRC/"FP_PSTH_ALL_EVENTS_v80.csv")
phase_df=pd.read_csv(SRC/"FP_BOUT_PHASE_TRACES_v81.csv.gz")
common=pd.read_csv(ROOT/"data"/"fp_da_common_event_v1"/"method_difference_events.csv.gz")
trace_cols=[c for c in d.columns if c.startswith("z")]
phase_cols=[c for c in phase_df.columns if c.startswith("p") and c[1:].isdigit()]
t=np.arange(-3,6,0.1); phase=np.linspace(0,100,len(phase_cols))
events=["active","passive","unrewarded"]
labels={"active":"Active","passive":"Passive","unrewarded":"Unrewarded"}
colors={"active":CYAN,"passive":RED,"unrewarded":GRAY_DARK}
d["key"]=d.SessionANM.astype(str)+"|"+d.AnchorStart_FP.round(6).astype(str)+"|"+d.event_type.astype(str)
common["key"]=common.SessionANM.astype(str)+"|"+common.AnchorStart_FP.round(6).astype(str)+"|"+common.model_outcome.astype(str)
d["common"]=d.key.isin(set(common.key))
d["event_index"]=d.groupby(["SessionANM","event_type"]).cumcount()

# Rebuild the next-observation trace table from the corrected outcome authority.
# The legacy event export contains 33 duplicate Active anchors in the passive row;
# SOE_FP_NEXT_OBSERVE_AFTER_OUTCOME_v82.csv was rebuilt after removing those duplicates.
nextmeta=pd.read_csv(DATA/"SOE_FP_NEXT_OBSERVE_AFTER_OUTCOME_v82.csv")
nextmeta["anchor6"]=nextmeta.next_observe_start.round(6)
obs=d[d.event_type.eq("observe_all")].copy()
obs["anchor6"]=obs.AnchorStart_FP.round(6)
nextobs=nextmeta.rename(columns={"previous_outcome":"prev_outcome"}).merge(
    obs[["SessionANM","anchor6","event_index"]+trace_cols],
    on=["SessionANM","anchor6"],how="inner",validate="many_to_one")

def animal_curves(frame, event_col, event_value, cols):
    g=frame[frame[event_col].eq(event_value)]
    rows=[]
    for an,z in g.groupby("AnmID"):
        rows.append((int(an),z[cols].mean(axis=0).to_numpy(float)))
    return rows

def ms(rows):
    x=np.vstack([v for _,v in rows])
    return np.nanmean(x,axis=0),np.nanstd(x,axis=0,ddof=1)/np.sqrt(x.shape[0]),x

def plot_curve(ax,x,rows,color,label):
    m,s,_=ms(rows)
    ax.plot(x,m,color=color,lw=1.35,label=label)
    ax.fill_between(x,m-s,m+s,color=color,alpha=.16,lw=0)

def finish_time(ax,title):
    ax.axvline(0,color=GRAY_MID,lw=.75,ls="--")
    ax.axhline(0,color=GRAY_LIGHT,lw=.6)
    ax.set_xlim(-3,5.9); ax.set_xlabel("Time from event (s)"); ax.set_ylabel("DA z-score")
    ax.set_title(title,pad=2); clean_ax(ax)

def finish_phase(ax,title):
    ax.axhline(0,color=GRAY_LIGHT,lw=.6)
    ax.set_xlim(0,100); ax.set_xlabel("Bout phase (%)"); ax.set_ylabel("DA z-score")
    ax.set_title(title,pad=2); clean_ax(ax)

# Long-form animal-average source table
source_rows=[]
for event in events:
    for an,v in animal_curves(d[d.common],"event_type",event,trace_cols):
        for ti,val in zip(t,v): source_rows.append(["outcome_fixed",event,an,ti,val])
    q=phase_df[(phase_df.event_type.eq(event))&phase_df.common]
    for an,v in animal_curves(q,"event_type",event,phase_cols):
        for ti,val in zip(phase,v): source_rows.append(["outcome_bout_phase",event,an,ti,val])

# Link duration-normalized observation bouts back to previous outcome
obs_phase=phase_df[phase_df.event_type.eq("observe_all")].merge(
    nextobs[["SessionANM","event_index","prev_outcome"]].drop_duplicates(),
    on=["SessionANM","event_index"],how="inner")
for event in events:
    for an,v in animal_curves(nextobs,"prev_outcome",event,trace_cols):
        for ti,val in zip(t,v): source_rows.append(["next_observe_fixed",event,an,ti,val])
    for an,v in animal_curves(obs_phase,"prev_outcome",event,phase_cols):
        for ti,val in zip(phase,v): source_rows.append(["next_observe_bout_phase",event,an,ti,val])
pd.DataFrame(source_rows,columns=["analysis","condition","AnmID","x","DA_z"]).to_csv(
    DATA/"SOE_FP_PSTH_ANIMAL_CURVES_v82.csv",index=False)

# Animal-level window statistics for next observation
stats=[]
mask02=(t>=0)&(t<2)
for event in events:
    g=nextobs[nextobs.prev_outcome.eq(event)].copy()
    g["value"]=g[np.array(trace_cols)[mask02]].mean(axis=1)
    a=g.groupby("AnmID").value.mean()
    for an,v in a.items(): stats.append([event,int(an),float(v)])
sv=pd.DataFrame(stats,columns=["condition","AnmID","post0_2_DA"])
sv.to_csv(DATA/"SOE_FP_NEXT_OBSERVE_POST02_PER_ANIMAL_v82.csv",index=False)
wide=sv.pivot(index="AnmID",columns="condition",values="post0_2_DA")
test_rows=[]
for left,right in [("active","unrewarded"),("passive","unrewarded"),("active","passive")]:
    q=wide[[left,right]].dropna(); diff=q[left]-q[right]
    pval=float(wilcoxon(diff).pvalue)
    test_rows.append([left,right,len(q),float(diff.mean()),float(diff.median()),pval,int((diff>0).sum())])
test_df=pd.DataFrame(test_rows,columns=["left","right","n","mean_diff","median_diff","p","positive"])
test_df.to_csv(DATA/"SOE_FP_NEXT_OBSERVE_POST02_STATS_v82.csv",index=False)
def p_post(left,right):
    return float(test_df[(test_df.left.eq(left))&(test_df.right.eq(right))].iloc[0].p)

def render_main(mobile=False):
    apply_rc(mobile)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(2,2,left=.18,right=.985,bottom=.13,top=.965,wspace=.46,hspace=.50)
    ax=fig.add_subplot(gs[0,0])
    for event in events:
        rows=animal_curves(d[d.common],"event_type",event,trace_cols)
        plot_curve(ax,t,rows,colors[event],f"{labels[event]}")
    finish_time(ax,"Outcome window")
    ax.legend(frameon=False,fontsize=5.8); panel_label(ax,"A")

    ax=fig.add_subplot(gs[0,1])
    for event in events:
        q=phase_df[(phase_df.event_type.eq(event))&phase_df.common]
        rows=animal_curves(q,"event_type",event,phase_cols)
        plot_curve(ax,phase,rows,colors[event],f"{labels[event]}")
    finish_phase(ax,"Actual bout")
    ax.legend(frameon=False,fontsize=5.8); panel_label(ax,"B")

    ax=fig.add_subplot(gs[1,0])
    for event in events:
        rows=animal_curves(nextobs,"prev_outcome",event,trace_cols)
        plot_curve(ax,t,rows,colors[event],f"after {labels[event]}")
    finish_time(ax,"Next-observe state")
    ax.legend(frameon=False,fontsize=5.4); panel_label(ax,"C")

    ax=fig.add_subplot(gs[1,1])
    order=["active","passive","unrewarded"]; x=np.arange(3,dtype=float)
    vals=[wide[e].dropna().to_numpy(float) for e in order]
    for an,row in wide[order].dropna().iterrows():
        ax.plot(x,row.to_numpy(float),color=GRAY_LIGHT,lw=.7,zorder=1)
    means=[np.mean(v) for v in vals]; errs=[sem(v) for v in vals]
    ax.bar(x,means,width=.50,color=[colors[e] for e in order],edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.8,capsize=2,capthick=.8,zorder=3)
    ax.axhline(0,color=GRAY_LIGHT,lw=.6)
    ax.set_xticks(x); ax.set_xticklabels(["Active\nprior","Passive\nprior","Unrewarded\nprior"])
    ax.set_ylabel("DA z-score, 0–2 s"); ax.set_title("Next-observe VTA state",pad=2)
    ymax=max(means[i]+errs[i] for i in range(3)); ax.set_ylim(min(-.45,min(means)-.2),ymax+.34)
    ax.text(.03,.97,f"Active vs Unrewarded  P={p_post('active','unrewarded'):.3f}\nPassive vs Unrewarded  P={p_post('passive','unrewarded'):.3f}",transform=ax.transAxes,ha="left",va="top",fontsize=5.3)
    clean_ax(ax); panel_label(ax,"D")
    return fig

fig=render_main(False); save_square(fig,OUT/"SOE_FP_PSTH_biological_story_v82",mobile=False); plt.close(fig)
fig=render_main(True); save_square(fig,OUT/"SOE_FP_PSTH_biological_story_v82_mobile",mobile=True,also_vector=False); plt.close(fig)

# Observation-context figure: where observation occurs and what preceded the next sampling bout.
obs_conditions=["observe_inside","observe_outside","observe_all"]
obs_labels={"observe_inside":"Inside","observe_outside":"Outside","observe_all":"All obs."}
obs_colors={"observe_inside":CYAN,"observe_outside":RED,"observe_all":GRAY_DARK}

def render_obs(mobile=False):
    apply_rc(mobile)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(2,2,left=.18,right=.985,bottom=.13,top=.965,wspace=.46,hspace=.50)
    ax=fig.add_subplot(gs[0,0])
    for e in obs_conditions:
        plot_curve(ax,t,animal_curves(d,"event_type",e,trace_cols),obs_colors[e],obs_labels[e])
    finish_time(ax,"Observation onset\nfixed time")
    ax.legend(frameon=False,fontsize=5.3); panel_label(ax,"A")
    ax=fig.add_subplot(gs[0,1])
    for e in obs_conditions:
        plot_curve(ax,phase,animal_curves(phase_df,"event_type",e,phase_cols),obs_colors[e],obs_labels[e])
    finish_phase(ax,"Observation bout\nnormalized duration")
    ax.legend(frameon=False,fontsize=5.3); panel_label(ax,"B")
    ax=fig.add_subplot(gs[1,0])
    for e in events:
        plot_curve(ax,t,animal_curves(nextobs,"prev_outcome",e,trace_cols),colors[e],f"after {labels[e]}")
    finish_time(ax,"First re-observation\n≤60 s")
    ax.legend(frameon=False,fontsize=5.1); panel_label(ax,"C")
    ax=fig.add_subplot(gs[1,1])
    for e in events:
        plot_curve(ax,phase,animal_curves(obs_phase,"prev_outcome",e,phase_cols),colors[e],f"after {labels[e]}")
    finish_phase(ax,"Same re-observation\nbout-normalized")
    ax.legend(frameon=False,fontsize=5.1); panel_label(ax,"D")
    return fig

fig=render_obs(False); save_square(fig,OUT/"SOE_FP_PSTH_observation_context_v82",mobile=False); plt.close(fig)
fig=render_obs(True); save_square(fig,OUT/"SOE_FP_PSTH_observation_context_v82_mobile",mobile=True,also_vector=False); plt.close(fig)

# Trial-level heatmaps for the same common events under the two temporal views.
fixed_pool=d[d.common & d.event_type.isin(events)][trace_cols].to_numpy(float)
phase_pool=phase_df[phase_df.common & phase_df.event_type.isin(events)][phase_cols].to_numpy(float)
fv=(np.nanpercentile(fixed_pool,5),np.nanpercentile(fixed_pool,95))
pv=(np.nanpercentile(phase_pool,5),np.nanpercentile(phase_pool,95))
fig,axs=plt.subplots(2,3,figsize=(8.2,5.4),constrained_layout=True)
for j,e in enumerate(events):
    g=d[d.common & d.event_type.eq(e)].sort_values("ActionBoutDur_FP")
    if len(g)>300: g=g.iloc[np.linspace(0,len(g)-1,300).astype(int)]
    heat=g[trace_cols].to_numpy(float)
    lim=max(abs(fv[0]),abs(fv[1]))
    im=axs[0,j].imshow(heat,aspect="auto",origin="lower",extent=[-3,5.9,0,len(heat)],
                       cmap="RdBu_r",vmin=-lim,vmax=lim)
    axs[0,j].axvline(0,color="w",lw=.7,ls="--")
    axs[0,j].set_title(labels[e],fontsize=8); axs[0,j].set_xlabel("Time (s)")
    axs[0,j].set_ylabel("Events" if j==0 else "")
    g=phase_df[phase_df.common & phase_df.event_type.eq(e)].sort_values("duration_s")
    if len(g)>300: g=g.iloc[np.linspace(0,len(g)-1,300).astype(int)]
    heat=g[phase_cols].to_numpy(float)
    lim2=max(abs(pv[0]),abs(pv[1]))
    im2=axs[1,j].imshow(heat,aspect="auto",origin="lower",extent=[0,100,0,len(heat)],
                        cmap="RdBu_r",vmin=-lim2,vmax=lim2)
    axs[1,j].set_xlabel("Bout phase (%)"); axs[1,j].set_ylabel("Events" if j==0 else "")
axs[0,0].text(-.24,1.08,"A",transform=axs[0,0].transAxes,fontweight="bold",fontsize=10)
axs[1,0].text(-.24,1.08,"B",transform=axs[1,0].transAxes,fontweight="bold",fontsize=10)
fig.text(.015,.73,"Fixed 0–6 s view",rotation=90,va="center",ha="center",fontsize=8)
fig.text(.015,.27,"Bout-normalized view",rotation=90,va="center",ha="center",fontsize=8)
fig.colorbar(im,ax=axs[0,:],fraction=.025,pad=.02,label="DA z-score")
fig.colorbar(im2,ax=axs[1,:],fraction=.025,pad=.02,label="DA z-score")
fig.savefig(OUT/"SOE_FP_PSTH_trial_heatmaps_v82.png",dpi=600)
fig.savefig(OUT/"SOE_FP_PSTH_trial_heatmaps_v82.pdf")
fig.savefig(OUT/"SOE_FP_PSTH_trial_heatmaps_v82.svg")
plt.close(fig)
