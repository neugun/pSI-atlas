from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; F=ROOT/"assets"
S=pd.read_csv(D/"SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv")
Q=pd.read_csv(D/"SLM_FP_DA_CROSS_READOUT_PER_ANIMAL_v1.csv")
R=pd.read_csv(D/"fp_da_common_event_v1"/"target_agreement_per_animal.csv")

def paired(ax,post,bout,ylabel,title,ann):
    post=np.asarray(post,float); bout=np.asarray(bout,float)
    x=np.array([0.,1.]); means=[post.mean(),bout.mean()]; errs=[sem(post),sem(bout)]
    ax.bar(x,means,width=.50,color=[CYAN,RED],edgecolor="none",zorder=1)
    for a,b in zip(post,bout): ax.plot(x,[a,b],color=GRAY_LIGHT,lw=.65,zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.8,capsize=2,capthick=.8,zorder=3)
    ax.axhline(0,color=GRAY_MID,lw=.6); ax.set_xticks(x); ax.set_xticklabels(["0-6 s","Bout"])
    ax.set_xlim(-.75,1.75); ax.set_ylabel(ylabel,labelpad=3); ax.set_title(title,pad=2)
    ax.text(.03,.97,ann,transform=ax.transAxes,ha="left",va="top",fontsize=5.6,color=GRAY_DARK)
    clean_ax(ax)

def pair(fam,comp):
    q=Q[(Q.family==fam)&(Q.comparison==comp)].sort_values("animal")
    s=S[(S.family==fam)&(S.comparison==comp)].iloc[0]
    return q,s

def render(mobile=False):
    apply_rc(mobile)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(2,2,left=.17,right=.985,bottom=.13,top=.96,wspace=.44,hspace=.50)
    ax=fig.add_subplot(gs[0,0]); r=R.sort_values("animal"); x=np.arange(len(r),dtype=float)
    ax.bar(x,r.spearman_rho,width=.50,color=CYAN,edgecolor="none"); med=float(r.spearman_rho.median()); ax.axhline(med,color=RED,lw=1)
    ax.set_ylim(0,1.04); ax.set_xticks(x); ax.set_xticklabels([str(int(v)) for v in r.animal]); ax.set_xlabel("Animal"); ax.set_ylabel("Spearman rho"); ax.set_title("Same 1,371 events",pad=2)
    ax.text(.03,.96,f"median={med:.3f}\nrange={r.spearman_rho.min():.2f}-{r.spearman_rho.max():.2f}",transform=ax.transAxes,ha="left",va="top",fontsize=5.6,color=GRAY_DARK)
    clean_ax(ax); panel_label(ax,"A")
    ax=fig.add_subplot(gs[0,1]); q,s=pair("actor","actor_abs_rpe"); paired(ax,q.post06_pct,q.actionbout_pct,"MSE gain (%)","Actor |RPE|",f"positive in both {int(s.positive_both)}/9\ngain rho={s.gain_rho:.2f}\nreadout delta P={s.direct_delta_p:.3f}"); panel_label(ax,"B")
    ax=fig.add_subplot(gs[1,0]); q,s=pair("passive_credit","update_selected_vs_w0p75"); paired(ax,q.post06_pct,q.actionbout_pct,"Credit gain (%)","Credit vs fixed 0.75",f"positive in both {int(s.positive_both)}/9\ngain rho={s.gain_rho:.2f}\nreadout delta P={s.direct_delta_p:.3f}"); panel_label(ax,"C")
    ax=fig.add_subplot(gs[1,1]); q,s=pair("passive_credit","update_selected_vs_w1p0"); paired(ax,q.post06_pct,q.actionbout_pct,"Credit gain (%)","Credit vs fixed 1.0",f"positive in both {int(s.positive_both)}/9\ngain rho={s.gain_rho:.2f}\nreadout delta P={s.direct_delta_p:.3f}"); panel_label(ax,"D")
    return fig

fig=render(False); save_square(fig,F/"SOE_FP_DA_cross_readout_consensus_v78",mobile=False); plt.close(fig)
fig=render(True); save_square(fig,F/"SOE_FP_DA_cross_readout_consensus_v78_mobile",mobile=True,also_vector=False); plt.close(fig)
print("done")
