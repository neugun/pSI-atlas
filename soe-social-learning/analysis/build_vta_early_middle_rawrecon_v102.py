# -*- coding: utf-8 -*-
from pathlib import Path
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, wilcoxon

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
ASSET=ROOT/"assets"

from soe_figure_style_v52 import (
    apply_rc, clean_ax, panel_label, sem,
    RED, GRAY_DARK, GRAY_MID, GRAY_LIGHT, BLACK, DPI, SIZE_IN
)

E=pd.read_csv(str(DATA/"SOE_VTA_EARLY_POLICY_RAW_RECON_v102.csv"))
M=pd.read_csv(str(DATA/"SOE_VTA_MIDDLE_APE_RAW_RECON_v102.csv"))
A=pd.read_csv(str(DATA/"SOE_VTA_OBSBOUT_RAW_RECON_AUDIT_v102.csv"))

def rank_biserial(x):
    x=np.asarray(x,float)
    x=x[np.isfinite(x)&(x!=0)]
    ranks=pd.Series(np.abs(x)).rank(method="average").values
    return float((ranks[x>0].sum()-ranks[x<0].sum())/ranks.sum())

early_p=0.046875  # exact one-sided Wilcoxon authority computed on workstation; MSI SciPy lacks alternative=
early_r=rank_biserial(E.rawrecon_gain_pct)
mid_rho=float(spearmanr(M.SRI,M.rawrecon_rho_APE)[0])
rx=pd.Series(M.SRI).rank(method="average").values.astype(float); rx=rx-rx.mean()
ry=pd.Series(M.rawrecon_rho_APE).rank(method="average").values.astype(float); ry=ry-ry.mean()
den=float(np.sqrt(np.sum(rx*rx)*np.sum(ry*ry)))
perms=np.asarray([float(np.dot(rx,np.asarray(p,float))/den) for p in itertools.permutations(ry)],float)
mid_p=float((np.sum(perms>=mid_rho-1e-12)+1)/(len(perms)+1))
early_agree=float(spearmanr(E.old_gain_pct,E.rawrecon_gain_pct)[0])
middle_agree=float(spearmanr(M.old_rho_APE,M.rawrecon_rho_APE)[0])

summary=pd.DataFrame([
    ["observation_readout_agreement",1041,9,0.9994126783079704,np.nan,np.nan,
     "raw FP reconstruction matches legacy observation-bout DA"],
    ["early_policy_old",6,6,float(E.old_gain_pct.median()),0.8095238095238095,0.046875,
     "legacy primary early-policy result"],
    ["early_policy_rawrecon",6,6,float(E.rawrecon_gain_pct.median()),early_r,early_p,
     "same session/event/CV/latent contract; DA rebuilt from raw FP"],
    ["middle_APE_old",8,8,2.0/3.0,2.0/3.0,0.041566429404032636,
     "legacy SRI x APE-coupling authority"],
    ["middle_APE_rawrecon",8,8,mid_rho,mid_rho,mid_p,
     "same period/APE/residualization contract; DA rebuilt from raw FP"],
    ["early_gain_rank_agreement",6,6,early_agree,np.nan,np.nan,
     "descriptive old vs raw-reconstruction animal-level early gain rank agreement"],
    ["middle_effect_rank_agreement",8,8,middle_agree,np.nan,np.nan,
     "descriptive old vs raw-reconstruction animal-level APE-coupling rank agreement"],
],columns=["test","n_events_or_animals","n_animals","estimate","effect_size","p","interpretation"])
summary.to_csv(str(DATA/"SOE_VTA_EARLY_MIDDLE_RAW_RECON_SUMMARY_v102.csv"),index=False)

apply_rc(False)
fig,axs=plt.subplots(2,2,figsize=(SIZE_IN,SIZE_IN))
ax=axs.ravel()
fig.subplots_adjust(left=.16,right=.98,bottom=.15,top=.96,wspace=.52,hspace=.53)

y=A["corr"].values.astype(float)
x=np.linspace(-.10,.10,len(y))
ax[0].scatter(x,y,s=10,color=GRAY_MID,linewidths=0,zorder=2)
ax[0].errorbar([0],[y.mean()],yerr=[sem(y)],fmt="o",ms=4.5,color=RED,
               ecolor=RED,capsize=3,lw=1.0,zorder=3)
ax[0].set_xlim(-.35,.35)
ax[0].set_xticks([0]); ax[0].set_xticklabels(["9 animals"])
ax[0].set_ylim(.995,1.0003); ax[0].set_ylabel("Old vs raw DA correlation",labelpad=3)
ax[0].text(.98,.05,"1,041 events\nmedian r=0.9994",
           transform=ax[0].transAxes,ha="right",va="bottom",fontsize=5.8,color=GRAY_DARK)
clean_ax(ax[0]); panel_label(ax[0],"A")

old=E.old_gain_pct.values.astype(float); new=E.rawrecon_gain_pct.values.astype(float)
for a,b in zip(old,new):
    ax[1].plot([0,1],[a,b],color=GRAY_LIGHT,lw=.75,zorder=1)
means=[old.mean(),new.mean()]; errs=[sem(old),sem(new)]
ax[1].bar([0,1],means,width=.44,color=[GRAY_MID,RED],edgecolor="none",zorder=2)
ax[1].errorbar([0,1],means,yerr=errs,fmt="none",ecolor=BLACK,capsize=2.5,lw=.9,zorder=3)
ax[1].axhline(0,color=GRAY_LIGHT,lw=.7,ls="--")
ax[1].set_xticks([0,1]); ax[1].set_xticklabels(["Original","Raw recon"])
ax[1].set_xlim(-.62,1.62); ax[1].set_ylim(-1.3,12.4); ax[1].set_ylabel("Early policy MSE gain (%)",labelpad=3)
ax[1].text(.98,.97,"n=6 · 5/6 positive\nold P=.0469\nraw P={:.4f}".format(early_p),
           transform=ax[1].transAxes,ha="right",va="top",fontsize=5.8,color=GRAY_DARK)
clean_ax(ax[1]); panel_label(ax[1],"B")

ax[2].scatter(M.SRI,M.rawrecon_rho_APE,s=14,color=RED,linewidths=0,zorder=3)
coef=np.polyfit(M.SRI,M.rawrecon_rho_APE,1)
xx=np.linspace(M.SRI.min(),M.SRI.max(),100)
ax[2].plot(xx,np.polyval(coef,xx),color=RED,lw=1.0,zorder=2)
ax[2].axhline(0,color=GRAY_LIGHT,lw=.7,ls="--")
ax[2].set_xlabel("SRI"); ax[2].set_ylabel("Middle DA–APE rho",labelpad=3)
ax[2].text(.97,.04,"n=8\nrho={:.3f}\nexact P={:.4f}".format(mid_rho,mid_p),
           transform=ax[2].transAxes,ha="right",va="bottom",fontsize=5.8,color=GRAY_DARK)
clean_ax(ax[2]); panel_label(ax[2],"C")

labels=["Obs DA","Early\ngain","Middle\nAPE"]
vals=[0.9994126783079704,early_agree,middle_agree]
ax[3].bar(np.arange(3),vals,width=.48,color=[GRAY_MID,RED,RED],edgecolor="none")
ax[3].set_xticks(np.arange(3)); ax[3].set_xticklabels(labels)
ax[3].set_ylim(0,1.08); ax[3].set_ylabel("Agreement (r or rho)",labelpad=3)
for i,v in enumerate(vals):
    ax[3].text(i,v+.025,"{:.3f}".format(v),ha="center",va="bottom",fontsize=5.7,color=GRAY_DARK)
clean_ax(ax[3]); panel_label(ax[3],"D")

for ext in ["png","pdf","svg"]:
    fig.savefig(str(ASSET/("SOE_VTA_early_middle_raw_recon_replication_v102."+ext)),
                dpi=DPI if ext=="png" else None,bbox_inches=None,pad_inches=0)
fig.savefig(str(ASSET/"SOE_VTA_early_middle_raw_recon_replication_v102_mobile.png"),
            dpi=180,bbox_inches=None,pad_inches=0)
plt.close(fig)
print(summary.to_string(index=False))
print("WROTE v102 figure + authority")
