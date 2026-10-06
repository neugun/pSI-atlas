from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import wilcoxon, mannwhitneyu
import sys

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/"assets"
SRC=Path(r"H:\soe_github_publish\soe_v25_work\soe-social-learning\data")
RES=Path(r"H:\soe_social_inference_20260928\results")

sys.path.insert(0,str(Path(r"H:\soe_github_publish\soe_v25_work\soe-social-learning\analysis")))
from soe_figure_style_v52 import apply_rc, clean_ax, panel_label, sem, RED, CYAN, GRAY_DARK, GRAY_MID, GRAY_LIGHT, BLACK, DPI, SIZE_IN

def pfmt(p):
    if not np.isfinite(p): return "P=n/a"
    if p<1e-4: return f"P={p:.1e}"
    if p<.001: return f"P={p:.4f}"
    return f"P={p:.3f}"

def p_wil(a,b=None,alternative="two-sided"):
    a=np.asarray(a,float)
    if b is None:
        a=a[np.isfinite(a)]
        if len(a)<2 or np.allclose(a,0): return np.nan
        return float(wilcoxon(a,alternative=alternative,method="auto").pvalue)
    b=np.asarray(b,float); ok=np.isfinite(a)&np.isfinite(b); a,b=a[ok],b[ok]
    if len(a)<2 or np.allclose(a,b): return np.nan
    return float(wilcoxon(a,b,alternative=alternative,method="auto").pvalue)

def annotate_p(ax,p,text=None,y=.96):
    s=(text+"; " if text else "")+pfmt(p)
    ax.text(.98,y,s,transform=ax.transAxes,ha="right",va="top",fontsize=6.2,color=GRAY_DARK)

def paired_panel(ax,a,b,labels,ylabel,colors=(GRAY_DARK,RED),p=None,ylim=None):
    a=np.asarray(a,float); b=np.asarray(b,float); ok=np.isfinite(a)&np.isfinite(b); a,b=a[ok],b[ok]
    x=np.array([0.,1.])
    for aa,bb in zip(a,b):
        ax.plot(x,[aa,bb],color=GRAY_LIGHT,lw=.7,zorder=1)
    means=[a.mean(),b.mean()]; errs=[sem(a),sem(b)]
    ax.bar(x,means,width=.48,color=colors,edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.85,capsize=2.3,capthick=.85,zorder=3)
    ax.set_xticks(x,labels)
    ax.set_ylabel(ylabel,labelpad=3)
    ax.set_xlim(-.68,1.68)
    if ylim: ax.set_ylim(*ylim)
    clean_ax(ax)
    if p is None: p=p_wil(a,b)
    annotate_p(ax,p,f"n={len(a)}")
    return p

def dist_panel(ax,vals,label,ylabel,color=RED,p=None,zero=False):
    v=np.asarray(vals,float);v=v[np.isfinite(v)]
    rng=np.random.default_rng(1); x=rng.normal(0,.055,len(v))
    ax.scatter(x,v,s=9,color=GRAY_MID,alpha=.75,linewidths=0,zorder=2)
    m=v.mean(); e=sem(v)
    ax.errorbar([0],[m],yerr=[e],fmt="o",ms=4.2,color=color,ecolor=color,capsize=3,lw=1.1,zorder=4)
    if zero: ax.axhline(0,color=GRAY_LIGHT,lw=.7,ls="--",zorder=0)
    ax.set_xticks([0],[label]); ax.set_xlim(-.45,.45); ax.set_ylabel(ylabel,labelpad=3);clean_ax(ax)
    if p is None: p=p_wil(v)
    annotate_p(ax,p,f"n={len(v)}")
    return p

def multigroup_points(ax,groups,labels,ylabel,colors,paired=False):
    x=np.arange(len(groups),dtype=float); rng=np.random.default_rng(2)
    if paired:
        n=min(len(g) for g in groups)
        arr=[np.asarray(g,float)[:n] for g in groups]
        ok=np.ones(n,dtype=bool)
        for g in arr: ok&=np.isfinite(g)
        arr=[g[ok] for g in arr]
        for vals in zip(*arr): ax.plot(x,vals,color=GRAY_LIGHT,lw=.55,zorder=1)
        groups=arr
    for i,(g,c) in enumerate(zip(groups,colors)):
        g=np.asarray(g,float);g=g[np.isfinite(g)]
        jit=rng.normal(i,.045,len(g))
        if not paired: ax.scatter(jit,g,s=7.5,color=GRAY_MID,alpha=.55,linewidths=0,zorder=2)
        ax.errorbar([i],[g.mean()],yerr=[sem(g)],fmt="o",ms=4.2,color=c,ecolor=c,capsize=3,lw=1.05,zorder=4)
    ax.set_xticks(x,labels); ax.set_ylabel(ylabel,labelpad=3); ax.set_xlim(-.65,len(groups)-.35); clean_ax(ax)

def save(fig,stem):
    fig.set_size_inches(SIZE_IN,SIZE_IN,forward=True)
    fig.savefig(F/f"{stem}.png",dpi=DPI,bbox_inches=None,pad_inches=0)
    fig.savefig(F/f"{stem}.pdf",bbox_inches=None,pad_inches=0)
    fig.savefig(F/f"{stem}.svg",bbox_inches=None,pad_inches=0)
    fig.savefig(F/f"{stem}_mobile.png",dpi=DPI,bbox_inches=None,pad_inches=0)
    plt.close(fig)

def fig2x2(mobile=False):
    apply_rc(mobile)
    fig,axs=plt.subplots(2,2,figsize=(SIZE_IN,SIZE_IN))
    fig.subplots_adjust(left=.18,right=.985,bottom=.13,top=.965,wspace=.48,hspace=.48)
    return fig,axs.ravel()

# 1 behavioral foundations
d=pd.read_csv(SRC/"training_conversion_animal_stage_v52.csv")
pv=lambda g,col: d[d.group.eq(g)].pivot(index="animal",columns="stage",values=col).dropna()
fig,ax=fig2x2()
q=d.pivot(index="animal",columns="stage",values="sri").dropna()
paired_panel(ax[0],q.early,q.late,["Early","Late"],"SRI",p=p_wil(q.early,q.late));panel_label(ax[0],"A")
qL=pv("learner","active_conversion"); paired_panel(ax[1],qL.early,qL.late,["Early","Late"],"Observe→Active",p=.00297);panel_label(ax[1],"B")
qN=pv("non_learner","active_conversion"); paired_panel(ax[2],qN.early,qN.late,["Early","Late"],"Observe→Active",colors=(GRAY_DARK,GRAY_MID),p=p_wil(qN.early,qN.late));panel_label(ax[2],"C")
dl=(qL.late-qL.early).values; dn=(qN.late-qN.early).values
multigroup_points(ax[3],[dl,dn],["Learner","Non-learner"],"Δ conversion",[RED,GRAY_MID]); ax[3].axhline(0,color=GRAY_LIGHT,lw=.7,ls="--")
pm=.0110;annotate_p(ax[3],pm,f"n={len(dl)}/{len(dn)}");panel_label(ax[3],"D")
save(fig,"SOE_behavioral_foundations_v64")

# 2 adaptive information value
d=pd.read_csv(SRC/"SOE_adaptive_social_information_value_v52_source.csv")
fig,ax=fig2x2()
dist_panel(ax[0],d.overall,"Full social","ΔNLL (nats)",RED,p_wil(d.overall,alternative="greater"),True);panel_label(ax[0],"A")
paired_panel(ax[1],d.early,d.late,["Early","Late"],"ΔNLL (nats)",colors=(GRAY_DARK,RED),p=p_wil(d.early,d.late));panel_label(ax[1],"B")
paired_panel(ax[2],d.nofeed_far,d.nofeed_near,["Far","Near"],"No-feed ΔNLL",colors=(GRAY_DARK,CYAN),p=p_wil(d.nofeed_far,d.nofeed_near));panel_label(ax[2],"C")
paired_panel(ax[3],d.feed_far,d.feed_near,["Far","Near"],"Feed-state ΔNLL",colors=(GRAY_DARK,RED),p=p_wil(d.feed_far,d.feed_near));panel_label(ax[3],"D")
save(fig,"SOE_adaptive_social_information_value_v64")

# 3 default SLM compact hierarchy
d=pd.read_csv(SRC/"SLM_choicekernel_stack_per_animal_v1.csv")
models=["SLM full","Current + Choice-kernel","SLM + Choice-kernel stack"]
labs=["Core","Cur.+CK","Default"]; cols=[GRAY_MID,GRAY_DARK,RED]
wide={m:d[d.model.eq(m)].set_index("animal") for m in models}
idx=wide[models[0]].index
for m in models[1:]: idx=idx.intersection(wide[m].index)
fig,ax=fig2x2()
multigroup_points(ax[0],[wide[m].loc[idx,"brier"].values for m in models],labs,"Held-animal Brier",cols,paired=True)
annotate_p(ax[0],.0016869753599166,f"Default vs Cur.+CK, n={len(idx)}");panel_label(ax[0],"A")
multigroup_points(ax[1],[wide[m].loc[idx,"auc"].values for m in models],labs,"Held-animal AUC",cols,paired=True)
annotate_p(ax[1],p_wil(wide[models[1]].loc[idx,"auc"],wide[models[2]].loc[idx,"auc"]),f"n={len(idx)}");panel_label(ax[1],"B")
db=(wide[models[1]].loc[idx,"brier"]-wide[models[2]].loc[idx,"brier"]).values
dist_panel(ax[2],db,"Default gain","Brier improvement",RED,p_wil(db,alternative="greater"),True);panel_label(ax[2],"C")
da=(wide[models[2]].loc[idx,"auc"]-wide[models[1]].loc[idx,"auc"]).values
dist_panel(ax[3],da,"Default gain","AUC improvement",RED,p_wil(da,alternative="greater"),True);panel_label(ax[3],"D")
save(fig,"SOE_SLM_default_hierarchy_v64")

# 4 feed conversion
d=pd.read_csv(SRC/"SLM_native_feed_demfeed_direct_hazard_per_animal_v1.csv")
d=d[d.window.eq("age_le_3s")].copy()
fig,ax=fig2x2()
paired_panel(ax[0],d.feed_rate_nodem,d.feed_rate_demfeed,["No dem-feed","Dem-feed"],"Feed probability",p=p_wil(d.feed_rate_nodem,d.feed_rate_demfeed));panel_label(ax[0],"A")
paired_panel(ax[1],d.residual_nodem,d.residual_demfeed,["No dem-feed","Dem-feed"],"State-residual Feed",p=p_wil(d.residual_nodem,d.residual_demfeed));panel_label(ax[1],"B")
dist_panel(ax[2],d.feed_rate_delta,"Raw Δ","Feed probability Δ",RED,p_wil(d.feed_rate_delta,alternative="greater"),True);panel_label(ax[2],"C")
dist_panel(ax[3],d.residual_delta,"Residual Δ","State-controlled Δ",RED,p_wil(d.residual_delta,alternative="greater"),True);panel_label(ax[3],"D")
save(fig,"SOE_feed_conversion_learning_v64")

# 5 artificial lesion correspondence
d=pd.read_csv(SRC/"SLM_autonomous_lesions_per_animal_v1.csv")
d=d[d.analysis_group.eq("learner")]
def modepair(metric,mode):
    a=d[d["mode"].eq("control")].set_index("analysis_animal_key")[metric]
    b=d[d["mode"].eq(mode)].set_index("analysis_animal_key")[metric]
    idx=a.index.intersection(b.index); return a.loc[idx].values,b.loc[idx].values
fig,ax=fig2x2()
a,b=modepair("obs_rate","sensory_mask");paired_panel(ax[0],a,b,["Intact","VB-like"],"Generated Observe",colors=(GRAY_DARK,CYAN),p=p_wil(a,b));panel_label(ax[0],"A")
a,b=modepair("active_contingency","sensory_mask");paired_panel(ax[1],a,b,["Intact","VB-like"],"Active contingency",colors=(GRAY_DARK,CYAN),p=p_wil(a,b));panel_label(ax[1],"B")
a,b=modepair("active_belief_mean","jaws50");paired_panel(ax[2],a,b,["Intact","JAWS-like"],"Active social credit",colors=(GRAY_DARK,RED),p=p_wil(a,b));panel_label(ax[2],"C")
a,b=modepair("abs_dA","jaws50");paired_panel(ax[3],a,b,["Intact","JAWS-like"],"|Active update|",colors=(GRAY_DARK,RED),p=p_wil(a,b));panel_label(ax[3],"D")
save(fig,"SOE_ArtificialSLM_causal_double_dissociation_v64")

# 6 JAWS multiscale causal
conv=pd.read_csv(SRC/"panel_e_jaws_conversion.csv")
alt=pd.read_csv(SRC/"JAWS_SLM_continuous_replay_animal_state_deltas_v2.csv")
sess=pd.read_csv(SRC/"JAWS_SLM_crossday_normal_vs_fulljaws_animal_v1.csv")
fig,ax=fig2x2()
q=conv[conv.condition.eq("contingent")];paired_panel(ax[0],q.off_conversion,q.on_conversion,["OFF","ON"],"Observe→Active",p=p_wil(q.off_conversion,q.on_conversion));panel_label(ax[0],"A")
q=conv[conv.condition.eq("noncontingent")];paired_panel(ax[1],q.off_conversion,q.on_conversion,["OFF","ON"],"Timing control",colors=(GRAY_DARK,CYAN),p=p_wil(q.off_conversion,q.on_conversion));panel_label(ax[1],"B")
q=alt[(alt.condition.eq("contingent"))&(alt.metric.eq("active_belief"))&(alt.normalization.eq("per_episode"))]
paired_panel(ax[2],q.off,q.on,["OFF","ON"],"Active credit / episode",p=p_wil(q.off,q.on));panel_label(ax[2],"C")
q=sess[(sess.condition.eq("contingent"))&(sess.metric.eq("final_belief_active_diff"))]
paired_panel(ax[3],q.normal,q.full_jaws,["Normal","Full JAWS"],"Accumulated Active credit",p=p_wil(q.normal,q.full_jaws));panel_label(ax[3],"D")
save(fig,"SOE_JAWS_credit_logic_v64")

# 7 SWM functional bridge
d=pd.read_csv(RES/"swm_efficacy_vs_slm_current_strict_v1"/"held_animal_metrics.csv")
fig,ax=fig2x2()
a=d[d.model.eq("slm_current13")].set_index("animal"); b=d[d.model.eq("slm_current13_efficacy")].set_index("animal"); idx=a.index.intersection(b.index)
paired_panel(ax[0],a.loc[idx,"auc"],b.loc[idx,"auc"],["SLM+cues","+ efficacy"],"Active-vs-Unrewarded AUC",p=p_wil(a.loc[idx,"auc"],b.loc[idx,"auc"],alternative="less"));panel_label(ax[0],"A")
gain=(b.loc[idx,"auc"]-a.loc[idx,"auc"]).values
dist_panel(ax[1],gain,"AUC gain","Δ AUC",RED,p_wil(gain,alternative="greater"),True);panel_label(ax[1],"B")
r=pd.read_csv(SRC/"swm_social_replacement_animal_v1.csv")
paired_panel(ax[2],r.efficacy_auc_raw,r.efficacy_auc_replacement,["Original","Replace"],"Efficacy AUC",colors=(RED,GRAY_MID),p=p_wil(r.efficacy_auc_raw,r.efficacy_auc_replacement,alternative="greater"));panel_label(ax[2],"C")
e=pd.read_csv(SRC/"swm_prospective_expected_info_gain_animal_v2.csv")
multigroup_points(ax[3],[e.auc_delta,e.auc_eig_ridge,e.auc_eig_hgb],["Efficacy","Ridge","HGB"],"Held-animal AUC",[RED,GRAY_MID,GRAY_LIGHT],paired=True)
annotate_p(ax[3],p_wil(e.auc_delta,e.auc_eig_hgb,alternative="greater"),"Efficacy vs EIG");panel_label(ax[3],"D")
save(fig,"SOE_SWM_functional_bridge_v64")

# 8 generalization comparator
d=pd.read_csv(SRC/"SLM_generalization_nested_latent_vs_behavior_family_peranimal_v1.csv")
fig,ax=fig2x2()
for k,domain in enumerate(["food","fear"]):
    q=d[d.domain.eq(domain)].copy()
    wide={}
    for fam in ["behavior_family","SLM_latent_family"]:
        z=q[q.family.eq(fam)].set_index("animal")
        wide[fam]=(z.observed-z.predicted).abs()
    idx=wide["behavior_family"].index.intersection(wide["SLM_latent_family"].index)
    paired_panel(ax[k],wide["behavior_family"].loc[idx],wide["SLM_latent_family"].loc[idx],["Behavior","SLM latent"],f"{domain.capitalize()} abs. error",p=p_wil(wide["behavior_family"].loc[idx],wide["SLM_latent_family"].loc[idx],alternative="greater"));panel_label(ax[k],chr(65+k))
    gain=(wide["behavior_family"].loc[idx]-wide["SLM_latent_family"].loc[idx]).values
    dist_panel(ax[k+2],gain,f"{domain} gain","Error reduction",RED if domain=="food" else CYAN,p_wil(gain,alternative="greater"),True);panel_label(ax[k+2],chr(67+k))
save(fig,"SOE_generalization_comparator_hierarchy_v64")

# 9 rat strong comparator
d=pd.read_csv(SRC/"rat001169_nestedCV_multimetric_per_rat_v7.csv")
fig,ax=fig2x2()
for k,metric in enumerate(["brier","nll","auc"]):
    a=d[d.model.eq("nestedCV_CK")].set_index("animal")[metric]
    b=d[d.model.eq("multiscale_logit")].set_index("animal")[metric]
    idx=a.index.intersection(b.index)
    if metric in ["brier","nll"]:
        p=p_wil(a.loc[idx],b.loc[idx],alternative="greater")
    else:
        p=p_wil(a.loc[idx],b.loc[idx],alternative="less")
    paired_panel(ax[k],a.loc[idx],b.loc[idx],["Nested CK","Multiscale"],metric.upper(),colors=(GRAY_DARK,RED),p=p);panel_label(ax[k],chr(65+k))
m=pd.read_csv(SRC/"SOE_to_macaque_frozen_transfer_by_monkey_v2.csv");m=m[m.frac.eq(1.0)]
dist_panel(ax[3],m.mean_gain,"Macaque","Frozen-core gain",CYAN,p=np.nan,zero=True)
ax[3].text(.02,.08,"2 monkeys (nested sensitivity)",transform=ax[3].transAxes,fontsize=5.6,color=GRAY_DARK)
panel_label(ax[3],"D")
save(fig,"SOE_crossspecies_comparator_hierarchy_v64")

print("generated V64 quantitative figures")
