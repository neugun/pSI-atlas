# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from soe_figure_style_v52 import *

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; A=ROOT/"assets"
S=pd.read_csv(D/"SOE_FP_PSTH_ANIMAL_CURVES_v82.csv")

def window(analysis,lo,hi):
    q=S[S.analysis.eq(analysis) & S.x.between(lo,hi,inclusive="both")]
    return q.groupby(["AnmID","condition"]).DA_z.mean().unstack()

F=window("outcome_fixed",0,5.9)
B=window("outcome_bout_phase",0,100)
pairs=[
    ("active","unrewarded","Active success − Unrewarded"),
    ("passive","unrewarded","Passive outcome − Unrewarded"),
    ("passive","active","Passive − Active"),
]
rows=[]
for left,right,title in pairs:
    f=(F[left]-F[right]).dropna()
    b=(B[left]-B[right]).dropna()
    idx=f.index.intersection(b.index); f=f.loc[idx]; b=b.loc[idx]
    rows += [
        ["fixed_0_6",left,right,len(f),float(f.mean()),float(f.median()),int((f>0).sum()),float(wilcoxon(f).pvalue)],
        ["bout_duration",left,right,len(b),float(b.mean()),float(b.median()),int((b>0).sum()),float(wilcoxon(b).pvalue)],
        ["fixed_minus_bout",left,right,len(idx),float((f-b).mean()),float((f-b).median()),int(((f-b)>0).sum()),float(wilcoxon(f-b).pvalue)],
    ]
T=pd.DataFrame(rows,columns=["comparison_scope","left","right","n","mean_diff","median_diff","positive","p"])
T.to_csv(D/"SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv",index=False)

def p(scope,left,right):
    return float(T[(T.comparison_scope.eq(scope))&(T.left.eq(left))&(T.right.eq(right))].iloc[0].p)

def render(mobile=False):
    apply_rc(mobile)
    fig=plt.figure(figsize=(SIZE_IN,SIZE_IN))
    gs=fig.add_gridspec(2,2,left=.17,right=.985,bottom=.13,top=.96,wspace=.46,hspace=.52)
    axes=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1]),fig.add_subplot(gs[1,0])]
    short_titles=["Active − Unrewarded","Passive − Unrewarded","Passive − Active"]
    letters=["A","B","C"]
    direct=[]
    for ax,(left,right,_),title,letter in zip(axes,pairs,short_titles,letters):
        f=(F[left]-F[right]).dropna(); b=(B[left]-B[right]).dropna()
        idx=f.index.intersection(b.index); f=f.loc[idx]; b=b.loc[idx]
        x=np.array([0.,1.]); means=[f.mean(),b.mean()]; errs=[sem(f),sem(b)]
        for an in idx:
            ax.plot(x,[f.loc[an],b.loc[an]],color=GRAY_LIGHT,lw=.75,zorder=1)
        ax.bar(x,means,width=.48,color=[CYAN,RED],edgecolor="none",zorder=2)
        ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.8,capsize=2,capthick=.8,zorder=3)
        ax.axhline(0,color=GRAY_MID,lw=.65)
        ax.set_xticks(x); ax.set_xticklabels(["Outcome\n0–6 s","Actual\nbout"])
        ax.set_title(title,fontsize=7.0,pad=3)
        ax.text(.03,.97,
                f"0–6 s P={p('fixed_0_6',left,right):.3f}\n"
                f"Bout P={p('bout_duration',left,right):.3f}\n"
                f"readout Δ P={p('fixed_minus_bout',left,right):.3f}",
                transform=ax.transAxes,ha="left",va="top",fontsize=5.0)
        clean_ax(ax); ax.tick_params(axis="both",labelsize=6); panel_label(ax,letter)
        direct.append((f-b).to_numpy(float))
    axes[0].set_ylabel("DA contrast (z)",fontsize=7)
    axes[2].set_ylabel("DA contrast (z)",fontsize=7)

    ax=fig.add_subplot(gs[1,1])
    x=np.arange(3,dtype=float)
    mat=np.vstack(direct).T
    for row in mat:
        ax.plot(x,row,color=GRAY_LIGHT,lw=.65,zorder=1)
    means=np.nanmean(mat,axis=0); errs=[sem(mat[:,i]) for i in range(3)]
    ax.bar(x,means,width=.48,color=[CYAN,RED,GRAY_DARK],edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=.8,capsize=2,capthick=.8,zorder=3)
    ax.axhline(0,color=GRAY_MID,lw=.65)
    ax.set_xticks(x); ax.set_xticklabels(["A − U","P − U","P − A"])
    ax.set_ylabel("0–6 s minus bout",fontsize=7)
    ax.set_title("Readout difference",fontsize=7.0,pad=3)
    ax.text(.03,.97,
            f"P={p('fixed_minus_bout','active','unrewarded'):.3f}\n"
            f"P={p('fixed_minus_bout','passive','unrewarded'):.3f}\n"
            f"P={p('fixed_minus_bout','passive','active'):.3f}",
            transform=ax.transAxes,ha="left",va="top",fontsize=5.0)
    clean_ax(ax); ax.tick_params(axis="both",labelsize=6); panel_label(ax,"D")
    return fig

fig=render(False); save_square(fig,A/"SOE_FP_DA_outcome_contrasts_v85",mobile=False); plt.close(fig)
fig=render(True); save_square(fig,A/"SOE_FP_DA_outcome_contrasts_v85_mobile",mobile=True,also_vector=False); plt.close(fig)
print(T.to_string(index=False))
