# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets"
SRC=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da")
POST="DA_Post06_AUCperSec"; BOUT="DA_ActionBout_AUCperSec"
actor=pd.read_csv(SRC/"fp_da_method_common_events_v2"/"actor_common_event_metrics.csv")
credit=pd.read_csv(SRC/"fp_da_method_common_events_v2"/"passive_credit_common_event_metrics.csv")
agree=pd.read_csv(SRC/"fp_da_method_common_events_v2"/"target_agreement_per_animal.csv")
scalar=pd.read_csv(SRC/"scalar_vs_vector_pe_v1"/"loao_animal_metrics.csv")

def gain(frame,target,model,base):
    q=frame[frame.target.eq(target)].pivot(index="animal",columns="model",values="mse")
    return 100*(q[base]-q[model])/q[base]

def credit_gain(target,fixed):
    q=credit[credit.target.eq(target)].pivot(index="animal",columns="model",values="mse")
    return 1000*(q[f"update_{fixed}"]-q["update_selected"])

def vector_inc(target):
    q=scalar[scalar.target.eq(target)].pivot(index="animal",columns="model",values="mse")
    return 1000*(q["scalar_full"]-q["scalar_plus_vector"])

def pair_block(ax,left,right,x0,x1,label0,label1,color0,color1):
    idx=left.index.intersection(right.index)
    l=left.loc[idx].to_numpy(float); r=right.loc[idx].to_numpy(float)
    for a,b in zip(l,r):
        ax.plot([x0,x1],[a,b],color=GRAY_LIGHT,lw=.65,zorder=1)
    means=[np.nanmean(l),np.nanmean(r)]
    errs=[sem(l),sem(r)]
    ax.bar([x0,x1],means,width=.48,color=[color0,color1],edgecolor="none",zorder=2)
    ax.errorbar([x0,x1],means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.8,capsize=2,capthick=.8,zorder=3)
    return idx

apply_rc(False)
fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
gs=fig.add_gridspec(2,2,left=.16,right=.985,bottom=.13,top=.96,wspace=.46,hspace=.54)

# A readout agreement
ax=fig.add_subplot(gs[0,0]); x=np.arange(len(agree))
ax.bar(x,agree.spearman_rho,width=.5,color=CYAN,edgecolor="none")
ax.axhline(agree.spearman_rho.median(),color=RED,lw=1)
ax.set_ylim(0,1.03); ax.set_xticks(x); ax.set_xticklabels(agree.animal.astype(int))
ax.set_xlabel("Animal"); ax.set_ylabel("Readout correlation (rho)")
ax.set_title("Same 1,371 events",pad=3)
ax.text(.03,.95,f"median rho={agree.spearman_rho.median():.3f}",transform=ax.transAxes,va="top",fontsize=5.8)
clean_ax(ax); ax.text(-.13,1.02,"A",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="bottom")

# B same downstream RPE analyses, animal-level mirror
ax=fig.add_subplot(gs[0,1])
models=[("q_signed_unsigned","Q RPE + abs"),("actor_rpe_abs","Actor RPE + abs")]
centers=[.5,3.0]
for (model,label),c in zip(models,centers):
    pair_block(ax,gain(actor,POST,model,"baseline_poly5"),gain(actor,BOUT,model,"baseline_poly5"),c-.32,c+.32,"","",CYAN,RED)
ax.axhline(0,color=GRAY_MID,lw=.7)
ax.set_xticks(centers); ax.set_xticklabels([m[1] for m in models],fontsize=6)
ax.set_ylabel("MSE gain (%)"); ax.set_title("RPE structure is preserved",pad=3)
ax.text(.03,.96,"Fixed 0-6 s",color=CYAN,transform=ax.transAxes,va="top",fontsize=5.5)
ax.text(.98,.96,"Real bout",color=RED,transform=ax.transAxes,ha="right",va="top",fontsize=5.5)
clean_ax(ax); ax.text(-.13,1.02,"B",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="bottom")

# C behavior-selected credit
ax=fig.add_subplot(gs[1,0])
for fixed,c in [("w0p75",.5),("w1p0",3.0)]:
    pair_block(ax,credit_gain(POST,fixed),credit_gain(BOUT,fixed),c-.32,c+.32,"","",CYAN,RED)
ax.axhline(0,color=GRAY_MID,lw=.7)
ax.set_xticks([.5,3.0]); ax.set_xticklabels(["vs fixed 0.75","vs fixed 1.0"],fontsize=6)
ax.set_ylabel("Credit-model gain x1000"); ax.set_title("Social credit replicates",pad=3)
ax.text(.03,.96,"Fixed 0-6 s",color=CYAN,transform=ax.transAxes,va="top",fontsize=5.5)
ax.text(.98,.96,"Real bout",color=RED,transform=ax.transAxes,ha="right",va="top",fontsize=5.5)
clean_ax(ax); ax.text(-.13,1.02,"C",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="bottom")

# D vector added after scalar RPE
ax=fig.add_subplot(gs[1,1])
pair_block(ax,vector_inc(POST),vector_inc(BOUT),0,1,"","",CYAN,RED)
ax.axhline(0,color=GRAY_MID,lw=.7)
ax.set_xticks([0,1]); ax.set_xticklabels(["Fixed 0-6 s","Real bout"],fontsize=6)
ax.set_ylabel("Incremental MSE gain x1000"); ax.set_title("Vector PE adds no gain",pad=3)
clean_ax(ax); ax.text(-.13,1.02,"D",transform=ax.transAxes,fontweight="bold",fontsize=10,ha="left",va="bottom")

for ext in ["png","pdf","svg"]:
    fig.savefig(A/f"SOE_VTA_codex_exact_replication_v96.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)
print("replotted v96 with paired animal-level data")
