from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; F=ROOT/"assets"
P=pd.read_csv(D/"rat001169_nestedCV_multimetric_paired_v7.csv")
S=pd.read_csv(D/"rat001169_nestedCV_multimetric_summary_v7.csv").set_index("metric")
FAM=pd.read_csv(D/"rat001169_nestedCV_family_scores_v6.csv")

GRAY="#9a9a9a"; LIGHT="#d2d2d2"; DARK="#333333"; BLUE="#2f4b7c"
plt.rcParams.update({"font.family":"Arial","font.size":9.2,"axes.titlesize":10.2,
                     "axes.labelsize":9.2,"xtick.labelsize":8.3,"ytick.labelsize":8.3,
                     "svg.fonttype":"none"})

def clean(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(False)

def paired(ax,metric,ylab,title,higher=False):
    a=P[f"{metric}_classical"].to_numpy(float)
    b=P[f"{metric}_multiscale"].to_numpy(float)
    x=np.array([0.,1.])
    for u,v in zip(a,b):
        ax.plot(x,[u,v],color=LIGHT,lw=.8,zorder=1)
    means=[a.mean(),b.mean()]
    sems=[a.std(ddof=1)/np.sqrt(len(a)),b.std(ddof=1)/np.sqrt(len(b))]
    ax.bar(x,means,width=.28,color=[GRAY,BLUE],edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=sems,fmt="none",ecolor=DARK,lw=1,capsize=2.5,zorder=3)
    ax.set_xticks(x,["Nested-CV CK","Structured"])
    ax.set_ylabel(ylab)
    ax.set_title(title,loc="left",weight="bold")
    r=S.loc[metric]
    direction="higher" if higher else "lower"
    ax.text(.02,.98,f"{int(r.wins)}/10 favor structured; r_rb={r.rank_biserial:.3f}\nP={r.p_one_sided:.4g}; {direction} is better",
            transform=ax.transAxes,ha="left",va="top",fontsize=8.1)
    clean(ax)

fig,axs=plt.subplots(2,2,figsize=(8.2,8.2),constrained_layout=True)
paired(axs[0,0],"brier","Brier","A  Held-rat probability error")
paired(axs[0,1],"nll","NLL","B  Held-rat log loss")
paired(axs[1,0],"auc","AUC","C  Held-rat discrimination",higher=True)

ax=axs[1,1]
order=["wsls","q","asymq","forgetq","qck","ck"]
names={"wsls":"WSLS","q":"Q","asymq":"asym-Q","forgetq":"forget-Q","qck":"Q+CK","ck":"CK"}
g=FAM.groupby("model").inner_mean_rat_brier.agg(["mean","sem"]).reindex(order)
x=np.arange(len(order))
ax.bar(x,g["mean"],yerr=g["sem"],width=.56,color=[GRAY]*5+[DARK],edgecolor="none",
       ecolor=DARK,capsize=2.5)
ax.set_xticks(x,[names[k] for k in order],rotation=30,ha="right")
ax.set_ylabel("Inner held-rat CV Brier")
ax.set_title("D  Comparator family selection",loc="left",weight="bold")
ax.text(.02,.98,"CK has the lowest mean inner-CV error\nand is selected in 5/5 outer folds",
        transform=ax.transAxes,ha="left",va="top",fontsize=8.1)
ax.set_ylim(float(g["mean"].min())-.002,float(g["mean"].max())+.004)
clean(ax)

fig.suptitle("Rat DANDI001169: structured multiscale state clears nested-CV classical RL",fontsize=12.4,weight="bold")
for ext in ["png","pdf","svg"]:
    fig.savefig(F/f"SOE_rat001169_nestedCV_multimetric_v1.{ext}",dpi=450,bbox_inches="tight")
plt.close(fig)

fig,axs=plt.subplots(4,1,figsize=(5.4,11.8),constrained_layout=True)
paired(axs[0],"brier","Brier","A  Brier")
paired(axs[1],"nll","NLL","B  NLL")
paired(axs[2],"auc","AUC","C  AUC",higher=True)
ax=axs[3]
ax.bar(x,g["mean"],yerr=g["sem"],width=.56,color=[GRAY]*5+[DARK],edgecolor="none",
       ecolor=DARK,capsize=2.5)
ax.set_xticks(x,[names[k] for k in order],rotation=28,ha="right")
ax.set_ylabel("Inner CV Brier"); ax.set_title("D  Classical family selection",loc="left",weight="bold")
ax.text(.02,.98,"CK selected in 5/5 outer folds",transform=ax.transAxes,ha="left",va="top",fontsize=8.1)
ax.set_ylim(float(g["mean"].min())-.002,float(g["mean"].max())+.004); clean(ax)
fig.savefig(F/"SOE_rat001169_nestedCV_multimetric_v1_mobile.png",dpi=350,bbox_inches="tight")
plt.close(fig)
print("wrote rat multimetric figure")
