# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; A=ROOT/"assets"
SRC=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da")

actor=pd.read_csv(SRC/"fp_da_method_common_events_v2"/"actor_common_event_contrasts.csv")
credit=pd.read_csv(SRC/"fp_da_method_common_events_v2"/"passive_credit_common_event_contrasts.csv")
agree=pd.read_csv(SRC/"fp_da_method_common_events_v2"/"target_agreement_per_animal.csv")
scalar=pd.read_csv(SRC/"scalar_vs_vector_pe_v1"/"baseline_contrasts.csv")
pairs=pd.read_csv(SRC/"scalar_vs_vector_pe_v1"/"direct_pairs.csv")
core=pd.read_csv(SRC/"corev2_strict_neural_v1"/"baseline_contrasts.csv")

def get(df,target,col,val):
    q=df[(df.target==target)&(df[col]==val)]
    if len(q)!=1: raise RuntimeError((target,col,val,len(q)))
    return q.iloc[0]

POST="DA_Post06_AUCperSec"
BOUT="DA_ActionBout_AUCperSec"
rows=[]

def add_pair(test,label,src_df,col,val,effect_col,wins_col,p_col,interpretation):
    a=get(src_df,POST,col,val); b=get(src_df,BOUT,col,val)
    rows.append(dict(test=test,label=label,
        post_effect=float(a[effect_col]),bout_effect=float(b[effect_col]),
        post_wins=int(a[wins_col]),bout_wins=int(b[wins_col]),
        post_p=float(a[p_col]),bout_p=float(b[p_col]),
        n=int(a.get("n",a.get("n_animals",9))),
        replication=interpretation))

add_pair("q_signed_unsigned","Signed + unsigned RPE",actor,"model","q_signed_unsigned",
         "median_pct_gain","wins","p","same_direction_weaker_duration")
add_pair("actor_rpe_abs","Actor RPE + |RPE|",actor,"model","actor_rpe_abs",
         "median_pct_gain","wins","p","same_direction_weaker_duration")
add_pair("scalar_full","Scalar RPE family",scalar,"model","scalar_full",
         "median_pct_gain","wins","p","same_direction")
add_pair("vector_signed","Outcome-vector PE",scalar,"model","vector_signed",
         "median_pct_gain","wins","p","same_direction_but_weaker_than_scalar")

for comp,label in [("update_selected_vs_w0p75","Behavior-selected credit vs fixed 0.75"),
                   ("update_selected_vs_w1p0","Behavior-selected credit vs fixed 1.0")]:
    a=get(credit,POST,"comparison",comp); b=get(credit,BOUT,"comparison",comp)
    rows.append(dict(test=comp,label=label,
        post_effect=float(a["median_mse_gain_selected"]),
        bout_effect=float(b["median_mse_gain_selected"]),
        post_wins=int(a["wins_selected"]),bout_wins=int(b["wins_selected"]),
        post_p=float(a["p"]),bout_p=float(b["p"]),n=int(a["n"]),
        replication="full_replication"))

# Incremental vector after scalar: positive means vector adds beyond scalar.
for target,name in [(POST,"fixed_0_6"),(BOUT,"real_bout")]:
    q=pairs[(pairs.target==target)&(pairs.left=="scalar_plus_vector")&(pairs.right=="scalar_full")].iloc[0]
    rows.append(dict(test="vector_after_scalar_"+name,label="Vector PE added after scalar RPE",
        post_effect=float(q["mean_mse_gain_left"]) if target==POST else np.nan,
        bout_effect=float(q["mean_mse_gain_left"]) if target==BOUT else np.nan,
        post_wins=int(q["wins_left"]) if target==POST else -1,
        bout_wins=int(q["wins_left"]) if target==BOUT else -1,
        post_p=float(q["p"]) if target==POST else np.nan,
        bout_p=float(q["p"]) if target==BOUT else np.nan,
        n=int(q["n"]),replication="no_increment_in_both"))

R=pd.DataFrame(rows)
# collapse incremental pair into one row
p0=R[R.test=="vector_after_scalar_fixed_0_6"].iloc[0]
p1=R[R.test=="vector_after_scalar_real_bout"].iloc[0]
R=R[~R.test.str.startswith("vector_after_scalar_")].copy()
R.loc[len(R)]=dict(test="vector_after_scalar",label="Vector PE added after scalar RPE",
    post_effect=p0.post_effect,bout_effect=p1.bout_effect,
    post_wins=p0.post_wins,bout_wins=p1.bout_wins,
    post_p=p0.post_p,bout_p=p1.bout_p,n=9,replication="no_increment_in_both")

R.to_csv(D/"SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv",index=False)
agree.to_csv(D/"SOE_VTA_CODEX_READOUT_AGREEMENT_v96.csv",index=False)

# compact audit summary
summary=pd.DataFrame([
["common_event_contract","1371 events / 9 animals","same events valid for both fixed 0-6 s and strict action-bout AUC/s"],
["readout_agreement",f"median rho={agree.spearman_rho.median():.3f}",f"range {agree.spearman_rho.min():.3f}-{agree.spearman_rho.max():.3f}"],
["social_credit","readout-robust with boundary","vs fixed 0.75: fixed 0-6 s 7/9 P=.0391, real bout 9/9 P=.0039; vs fixed 1.0: fixed 0-6 s 6/9 P=.0547 (borderline), real bout 9/9 P=.0039"],
["scalar_vs_vector","replicated qualitatively","scalar RPE family remains stronger than tested vector PE; vector adds no benefit after scalar"],
["post_RPE_strength","window-sensitive","RPE-family gain keeps the same direction but is weaker under strict action-bout readout"],
],columns=["question","result","meaning"])
summary.to_csv(D/"SOE_VTA_CODEX_REPLICATION_SUMMARY_v96.csv",index=False)

# Main figure: direct old-vs-Codex mirror. Effect is percentage MSE gain where defined.
plot_rows=R[R.test.isin(["q_signed_unsigned","actor_rpe_abs","scalar_full"])].copy()
credit_rows=R[R.test.isin(["update_selected_vs_w0p75","update_selected_vs_w1p0"])].copy()

apply_rc(False)
fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
gs=fig.add_gridspec(2,2,left=.15,right=.985,bottom=.13,top=.96,wspace=.42,hspace=.50)

ax=fig.add_subplot(gs[0,0])
x=np.arange(len(agree))
ax.bar(x,agree.spearman_rho,width=.5,color=CYAN,edgecolor="none")
ax.axhline(agree.spearman_rho.median(),lw=1,color=RED)
ax.set_ylim(0,1.03); ax.set_xticks(x); ax.set_xticklabels(agree.animal.astype(int))
ax.set_xlabel("Animal"); ax.set_ylabel("Readout correlation (rho)")
ax.set_title("Same-event DA agreement",pad=4,fontsize=8)
ax.text(.03,.95,f"median rho={agree.spearman_rho.median():.3f}",transform=ax.transAxes,va="top",fontsize=6)
clean_ax(ax); ax.text(-.15,1.08,"A",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="top")

ax=fig.add_subplot(gs[0,1])
x=np.arange(len(plot_rows)); w=.26
ax.bar(x-w/2,plot_rows.post_effect,width=w,label="Fixed 0-6 s",color=CYAN,edgecolor="none")
ax.bar(x+w/2,plot_rows.bout_effect,width=w,label="Real bout",color=RED,edgecolor="none")
ax.axhline(0,lw=.7)
ax.set_xticks(x); ax.set_xticklabels(["Q RPE\n+ abs","Actor RPE\n+ abs","Scalar\nRPE"],fontsize=6)
ax.set_ylabel("Median MSE gain (%)"); ax.set_title("RPE family: same direction",pad=4,fontsize=8)
ax.legend(frameon=False,fontsize=5.5)
clean_ax(ax); ax.text(-.15,1.08,"B",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="top")

ax=fig.add_subplot(gs[1,0])
x=np.arange(2); w=.26
# credit effect is absolute MSE gain, multiply by 1000 for readable scale.
ax.bar(x-w/2,credit_rows.post_effect.to_numpy()*1000,width=w,label="Fixed 0-6 s",color=CYAN,edgecolor="none")
ax.bar(x+w/2,credit_rows.bout_effect.to_numpy()*1000,width=w,label="Real bout",color=RED,edgecolor="none")
ax.set_xticks(x); ax.set_xticklabels(["vs fixed\n0.75","vs fixed\n1.0"],fontsize=6)
ax.set_ylabel("MSE gain x1000"); ax.set_title("Social credit: replicated",pad=4,fontsize=8)
for i,q in enumerate(credit_rows.itertuples()):
    ax.text(i-w/2,q.post_effect*1000+0.15,f"{q.post_wins}/9",ha="center",fontsize=5.5)
    ax.text(i+w/2,q.bout_effect*1000+0.15,f"{q.bout_wins}/9",ha="center",fontsize=5.5)
clean_ax(ax); ax.text(-.15,1.08,"C",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="top")

ax=fig.add_subplot(gs[1,1])
q=R[R.test=="vector_after_scalar"].iloc[0]
x=np.array([0.,1.])
vals=np.array([q.post_effect,q.bout_effect])*1000
ax.bar(x,vals,width=.50,color=[CYAN,RED],edgecolor="none")
ax.axhline(0,lw=.7)
ax.set_xticks(x); ax.set_xticklabels(["Fixed 0-6 s","Real bout"],fontsize=6)
ax.set_ylabel("Incremental MSE gain x1000")
ax.set_title("Vector PE adds no benefit",pad=4,fontsize=8)
ax.text(0,-0.04,f"P={q.post_p:.3f}",ha="center",va="top",fontsize=5.5)
ax.text(1,-0.04,f"P={q.bout_p:.3f}",ha="center",va="top",fontsize=5.5)
ax.set_ylim(-.68,.06); clean_ax(ax); ax.text(-.15,1.08,"D",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="top")

for ext in ["png","pdf","svg"]:
    fig.savefig(A/f"SOE_VTA_codex_exact_replication_v96.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)
print(R.to_string(index=False))
print(summary.to_string(index=False))
