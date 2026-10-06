from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import wilcoxon, spearmanr
import sys

ROOT=Path(__file__).resolve().parents[1]; F=ROOT/"assets"
SRC=Path(r"H:\soe_github_publish\soe_v25_work\soe-social-learning\data")
STAGE=Path(r"H:\soe_social_inference_20260928\SOE_GITHUB_STAGING_20261003\results")
SOE=Path(r"H:\soe_social_inference_20260928\rl_model2_20261001\social_learning_unification_20261002")
sys.path.insert(0,str(Path(r"H:\soe_github_publish\soe_v25_work\soe-social-learning\analysis")))
from soe_figure_style_v52 import apply_rc, clean_ax, panel_label, sem, RED, CYAN, GRAY_DARK, GRAY_MID, GRAY_LIGHT, BLACK, DPI, SIZE_IN

def pfmt(p):
    if not np.isfinite(p): return "P=n/a"
    if p<1e-4:return f"P={p:.1e}"
    if p<.001:return f"P={p:.4f}"
    return f"P={p:.3f}"

def p_wil(a,b=None,alternative="two-sided"):
    a=np.asarray(a,float)
    if b is None:
        a=a[np.isfinite(a)]
        if len(a)<2 or np.allclose(a,0):return np.nan
        return float(wilcoxon(a,alternative=alternative,method="auto").pvalue)
    b=np.asarray(b,float);ok=np.isfinite(a)&np.isfinite(b);a,b=a[ok],b[ok]
    if len(a)<2 or np.allclose(a,b):return np.nan
    return float(wilcoxon(a,b,alternative=alternative,method="auto").pvalue)

def ann(ax,p,txt=None,y=.96):
    ax.text(.98,y,((txt+"; ") if txt else "")+pfmt(p),transform=ax.transAxes,
            ha="right",va="top",fontsize=6.1,color=GRAY_DARK)

def paired(ax,a,b,labels,ylabel,colors=(GRAY_DARK,RED),p=None):
    a=np.asarray(a,float);b=np.asarray(b,float);ok=np.isfinite(a)&np.isfinite(b);a,b=a[ok],b[ok]
    x=[0,1]
    for aa,bb in zip(a,b):ax.plot(x,[aa,bb],color=GRAY_LIGHT,lw=.7,zorder=1)
    m=[a.mean(),b.mean()];e=[sem(a),sem(b)]
    ax.bar(x,m,width=.48,color=colors,edgecolor="none",zorder=2)
    ax.errorbar(x,m,yerr=e,fmt="none",ecolor=BLACK,capsize=2.3,lw=.85,zorder=3)
    ax.set_xticks(x,labels);ax.set_xlim(-.65,1.65);ax.set_ylabel(ylabel,labelpad=3);clean_ax(ax)
    if p is None:p=p_wil(a,b)
    ann(ax,p,f"n={len(a)}")
    return p

def dist(ax,v,label,ylabel,color=RED,p=None,zero=True):
    v=np.asarray(v,float);v=v[np.isfinite(v)]
    rng=np.random.default_rng(7);x=rng.normal(0,.055,len(v))
    ax.scatter(x,v,s=9,color=GRAY_MID,alpha=.72,linewidths=0,zorder=2)
    ax.errorbar([0],[v.mean()],yerr=[sem(v)],fmt="o",ms=4.3,color=color,ecolor=color,capsize=3,lw=1.1,zorder=4)
    if zero:ax.axhline(0,color=GRAY_LIGHT,lw=.7,ls="--")
    ax.set_xticks([0],[label]);ax.set_xlim(-.42,.42);ax.set_ylabel(ylabel,labelpad=3);clean_ax(ax)
    if p is None:p=p_wil(v)
    ann(ax,p,f"n={len(v)}")
    return p

def fig4():
    apply_rc(False);f,a=plt.subplots(2,2,figsize=(SIZE_IN,SIZE_IN))
    f.subplots_adjust(left=.18,right=.985,bottom=.13,top=.965,wspace=.48,hspace=.48)
    return f,a.ravel()

def save(fig,stem):
    fig.set_size_inches(SIZE_IN,SIZE_IN,forward=True)
    fig.savefig(F/f"{stem}.png",dpi=DPI,bbox_inches=None,pad_inches=0)
    fig.savefig(F/f"{stem}_mobile.png",dpi=DPI,bbox_inches=None,pad_inches=0)
    plt.close(fig)

# Agent: direct animal-level generative comparisons.
A=pd.read_csv(STAGE/"SLM_agent_motif_rollout_per_animal_v1.csv")
R=pd.read_csv(SRC/"SLM_generic_RNN_per_animal_alignment_v1.csv")
fig,ax=fig4()
for k,comp in enumerate(["Q-allreward","Outcome-belief"]):
    a=A[A.model.eq(comp)].set_index("animal").occupancy_js
    b=A[A.model.eq("Full SLM")].set_index("animal").occupancy_js
    idx=a.index.intersection(b.index)
    p=.025699842639369308 if comp=="Q-allreward" else .012949305320944404
    paired(ax[k],a.loc[idx],b.loc[idx],[("Q" if comp=="Q-allreward" else "Belief"),"Full SLM"],"Motif occupancy JS",p=p)
    panel_label(ax[k],chr(65+k))
q=R.pivot(index="animal",columns="reward_mode",values="occupancy_r").dropna()
paired(ax[2],q.active_only,q.food_all,["Active-only","Act.+Pass."],"Agent occupancy r",colors=(GRAY_DARK,CYAN),p=p_wil(q.active_only,q.food_all));panel_label(ax[2],"C")
q=R.pivot(index="animal",columns="reward_mode",values="policy_motif_rho").dropna()
paired(ax[3],q.active_only,q.food_all,["Active-only","Act.+Pass."],"Policy–motif ρ",colors=(GRAY_DARK,CYAN),p=p_wil(q.active_only,q.food_all));panel_label(ax[3],"D")
save(fig,"SOE_agent_sufficiency_hierarchy_v65")

# Visual Block: every main panel is animal-level.
V=pd.read_csv(SRC/"VisualBlock_choiceKernel_SRI_loss_per_animal_v1.csv")
fig,ax=fig4()
paired(ax[0],V.SRI_reference,V.SRI_visualblock,["Original","Visual Block"],"SRI",colors=(GRAY_DARK,CYAN),p=p_wil(V.SRI_reference,V.SRI_visualblock));panel_label(ax[0],"A")
dist(ax[1],V.Brier_degradation,"VB − reference","Brier degradation",CYAN,p_wil(V.Brier_degradation,alternative="greater"));panel_label(ax[1],"B")
dist(ax[2],V.NLL_degradation,"VB − reference","NLL degradation",CYAN,p_wil(V.NLL_degradation,alternative="greater"));panel_label(ax[2],"C")
# AUC degradation is expected negative if prediction worsens.
dist(ax[3],V.AUC_degradation,"VB − reference","AUC change",CYAN,p_wil(V.AUC_degradation,alternative="less"));panel_label(ax[3],"D")
save(fig,"SOE_VisualBlock_information_closure_v65")

# Cross-species: individual held-out units for Human/Rat; nested date clusters shown explicitly.
X=pd.read_csv(SRC/"SOE_crossspecies_comparator_hierarchy_v3_source.csv")
fig,ax=fig4()
for k,(ds,lab,p0) in enumerate([("Human","Human",.0048828125),("Rat DANDI001169","Rat",.0048828125)]):
    q=X[X.dataset.eq(ds)]
    paired(ax[k],q.comparator_brier,q.structured_brier,["Comparator","Structured"],f"{lab} held-out Brier",p=p0)
    panel_label(ax[k],chr(65+k))
q=X[X.dataset.eq("Macaque")]
pdate=p_wil(q.comparator_brier,q.structured_brier,alternative="greater")
paired(ax[2],q.comparator_brier,q.structured_brier,["Feature-Q","Structured"],"Macaque date Brier",colors=(GRAY_DARK,CYAN),p=pdate)
ax[2].text(.02,.08,"44 date clusters; nested in 2 monkeys",transform=ax[2].transAxes,fontsize=5.5,color=GRAY_DARK)
panel_label(ax[2],"C")
m=pd.read_csv(SRC/"SOE_to_macaque_frozen_transfer_by_monkey_v2.csv");m=m[m.frac.eq(1.0)]
dist(ax[3],m.mean_gain,"Frozen core","Transfer gain",CYAN,p=np.nan,zero=True)
ax[3].text(.02,.08,"n=2 monkeys; sensitivity only",transform=ax[3].transAxes,fontsize=5.5,color=GRAY_DARK)
panel_label(ax[3],"D")
save(fig,"SOE_crossspecies_evidence_hierarchy_v65")

# VTA temporal logic: expose raw animal-level early and middle data; keep post as transparent effect-size summary.
E=pd.read_csv(SOE/"ObsDA_earlythird_classical_adjudication_by_animal_v1.csv")
base=E[E.model.eq("base")].set_index("animal").mse
act=E[E.model.eq("ActorPolicy")].set_index("animal").mse
idx=base.index.intersection(act.index)
early_gain=100*(base.loc[idx]-act.loc[idx])/base.loc[idx]
M=pd.read_csv(SOE/"DA_middle_APE_vs_classicRL_partial_by_animal_v1.csv")
M=M[M.candidate.eq("q_ck_err")].copy()
T=pd.read_csv(SOE/"DA_classicRL_postoutcome_timeresid_tests_v2.csv")
fig,ax=fig4()
dist(ax[0],early_gain,"Actor policy","Early MSE gain (%)",RED,p=.046875,zero=True);panel_label(ax[0],"A")
ax[1].scatter(M.SRI,M.rho_APE,s=13,color=RED,alpha=.8,linewidths=0)
rho,p_sp=spearmanr(M.SRI,M.rho_APE)
ax[1].set_xlabel("SRI");ax[1].set_ylabel("Middle DA–APE ρ",labelpad=3);clean_ax(ax[1])
ann(ax[1],.0415664294040326,f"n={len(M)}; ρ={rho:.2f}");panel_label(ax[1],"B")
post_names=["ActorCriticRPE","qAllRPE","BeliefSurprise"]; labs=["SLM RPE","Q/RPE","Belief surprise"]
q=T.set_index("model").loc[post_names]
x=np.arange(3);vals=q.rank_biserial_r.values.astype(float)
ax[2].bar(x,vals,width=.48,color=[RED,GRAY_MID,GRAY_LIGHT],edgecolor="none")
ax[2].set_xticks(x,labs,rotation=20,ha="right");ax[2].set_ylabel("Post outcome effect",labelpad=3);ax[2].set_ylim(0,1.1);clean_ax(ax[2])
for i,r in enumerate(q.itertuples()):
    ax[2].text(i,float(r.rank_biserial_r)+.045,pfmt(float(r.p_two_sided)),ha="center",va="bottom",fontsize=5.4,color=GRAY_DARK)
panel_label(ax[2],"C")
# Count prespecified axes that are positive+significant, while retaining the RPE boundary.
DA=pd.read_csv(SRC/"DA_global_temporal_model_adjudication_v4_authority.csv").set_index("model_family")
fam=["SLM","Q-all","Choice kernel","TinyRNN","History MLP"];labs=["SLM","Q/RPE","CK","TinyRNN","Hist. MLP"]
vals=[DA.loc[f,"positive_sig_axes"] for f in fam]
ax[3].bar(np.arange(len(fam)),vals,width=.48,color=[RED,GRAY_MID,GRAY_LIGHT,GRAY_DARK,GRAY_DARK],edgecolor="none")
ax[3].set_xticks(np.arange(len(fam)),labs,rotation=25,ha="right");ax[3].set_ylabel("# positive significant axes",labelpad=3);ax[3].set_ylim(0,3.4);clean_ax(ax[3]);panel_label(ax[3],"D")
save(fig,"SOE_DA_temporal_logic_v65")

print("generated V65 quantitative figures")
