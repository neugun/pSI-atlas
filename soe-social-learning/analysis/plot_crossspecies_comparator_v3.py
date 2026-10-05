from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"data"; F=ROOT/"assets"
SRC=pd.read_csv(D/"SOE_crossspecies_comparator_hierarchy_v3_source.csv")
AUD=pd.read_csv(D/"SOE_crossspecies_classical_comparator_audit_v3.csv")
RATL=pd.read_csv(D/"rat001169_classical_RL_samecontract_summary_v5.csv")

GRAY="#9a9a9a"; LIGHT="#d2d2d2"; DARK="#333333"; BLUE="#2f4b7c"
plt.rcParams.update({"font.family":"Arial","font.size":9.2,"axes.titlesize":10.2,
                     "axes.labelsize":9.2,"xtick.labelsize":8.3,"ytick.labelsize":8.3,
                     "svg.fonttype":"none"})

def clean(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(False)

def paired(ax,df,labels,title,note):
    left=df.comparator_brier.to_numpy(float); right=df.structured_brier.to_numpy(float)
    x=np.array([0.,1.])
    for a,b in zip(left,right): ax.plot(x,[a,b],color=LIGHT,lw=.8,zorder=1)
    means=[left.mean(),right.mean()]
    sems=[left.std(ddof=1)/np.sqrt(len(left)),right.std(ddof=1)/np.sqrt(len(right))]
    ax.bar(x,means,width=.28,color=[GRAY,BLUE],edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=sems,fmt="none",ecolor=DARK,lw=1,capsize=2.5,zorder=3)
    ax.set_xticks(x,labels); ax.set_ylabel("Held-out Brier"); ax.set_title(title,loc="left",weight="bold")
    ax.text(.02,.98,note,transform=ax.transAxes,ha="left",va="top",fontsize=8.1); clean(ax)

ha=AUD[AUD.dataset.eq("Human exp/obs")].iloc[0]
ra=AUD[AUD.dataset.eq("Rat DANDI001169")].iloc[0]
ma=AUD[AUD.dataset.eq("Macaque global")].iloc[0]
h=SRC[SRC.dataset.eq("Human")]; r=SRC[SRC.dataset.eq("Rat DANDI001169")]; m=SRC[SRC.dataset.eq("Macaque")]

fig,axs=plt.subplots(2,2,figsize=(8.2,8.2),constrained_layout=True)
paired(axs[0,0],h,["Best Feature-Q","Structured"],"A  Human: structured state clears Feature-Q",
       f"8/10 held-out subjects\nr_rb={ha.rrb:.3f}, P={ha.p_one_sided:.4g}")
paired(axs[0,1],r,["Best classical","Structured"],"B  Rat: structured state clears nested-CV RL",
       f"Nested held-rat CV selects CK in 5/5 outer folds\n8/10 rats, r_rb={ra.rrb:.3f}, P={ra.p_one_sided:.4g}")
paired(axs[1,0],m,["Best Feature-Q","Structured"],"C  Macaque: nested sensitivity",
       f"41/44 date clusters\nr_rb={ma.rrb:.3f}, P={ma.p_one_sided:.2e}\n2 monkeys; not population-level inference")

ax=axs[1,1]
order=["wsls","q","asymq","forgetq","qck","ck"]; names={"wsls":"WSLS","q":"Q","asymq":"asym-Q","forgetq":"forget-Q","qck":"Q+CK","ck":"CK"}
v=RATL.set_index("model")
vals=[float(v.loc[k,"mean_brier"]) for k in order]+[float(r.structured_brier.mean())]
labs=[names[k] for k in order]+["Structured"]; x=np.arange(len(labs))
ax.bar(x,vals,width=.56,color=[GRAY]*6+[BLUE],edgecolor="none")
ax.set_xticks(x,labs,rotation=32,ha="right"); ax.set_ylabel("Mean held-rat Brier")
ax.set_title("D  Rat outer-test family ladder",loc="left",weight="bold")
ax.text(.02,.98,"Same 12,564 trials and original 5-fold split\nLower is better; nested CV selects CK",
        transform=ax.transAxes,ha="left",va="top",fontsize=8.1)
ax.set_ylim(min(vals)-.0035,max(vals)+.004); clean(ax)
fig.suptitle("Structured multiscale state versus strong matched comparators",fontsize=12.5,weight="bold")
for ext in ["png","pdf","svg"]: fig.savefig(F/f"SOE_crossspecies_comparator_hierarchy_v3.{ext}",dpi=450,bbox_inches="tight")
plt.close(fig)

fig,axs=plt.subplots(4,1,figsize=(5.4,11.8),constrained_layout=True)
paired(axs[0],h,["Best Feature-Q","Structured"],"A  Human",f"8/10; r_rb={ha.rrb:.3f}; P={ha.p_one_sided:.4g}")
paired(axs[1],r,["Best classical","Structured"],"B  Rat",f"Nested CV: CK 5/5; 8/10; r_rb={ra.rrb:.3f}; P={ra.p_one_sided:.4g}")
paired(axs[2],m,["Best Feature-Q","Structured"],"C  Macaque sensitivity",f"41/44 dates; r_rb={ma.rrb:.3f}; P={ma.p_one_sided:.2e}\n2 monkeys nested")
ax=axs[3]; ax.bar(x,vals,width=.56,color=[GRAY]*6+[BLUE],edgecolor="none")
ax.set_xticks(x,labs,rotation=28,ha="right"); ax.set_ylabel("Mean held-rat Brier"); ax.set_title("D  Rat outer-test family ladder",loc="left",weight="bold")
ax.set_ylim(min(vals)-.0035,max(vals)+.004); clean(ax)
fig.savefig(F/"SOE_crossspecies_comparator_hierarchy_v3_mobile.png",dpi=350,bbox_inches="tight")
plt.close(fig)
print("wrote comparator hierarchy v3")
