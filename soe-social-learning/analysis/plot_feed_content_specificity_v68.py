from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
ASSET=ROOT/"assets"
sys.path.insert(0,str(ROOT/"analysis"))
from soe_figure_style_v52 import (
    apply_rc,clean_ax,panel_label,sem,RED,CYAN,GRAY_DARK,GRAY_MID,GRAY_LIGHT,BLACK,DPI,SIZE_IN
)

def pfmt(p):
    if not np.isfinite(p): return "P=n/a"
    if p < 1e-4: return f"P={p:.1e}"
    if p < .001: return f"P={p:.4f}"
    return f"P={p:.3f}"

def pwil(a,b=None,alternative="two-sided"):
    a=np.asarray(a,float)
    if b is None:
        a=a[np.isfinite(a)]
        if len(a)<2 or np.allclose(a,0): return np.nan
        return float(wilcoxon(a,alternative=alternative,method="auto").pvalue)
    b=np.asarray(b,float)
    ok=np.isfinite(a)&np.isfinite(b)
    a,b=a[ok],b[ok]
    if len(a)<2 or np.allclose(a,b): return np.nan
    return float(wilcoxon(a,b,alternative=alternative,method="auto").pvalue)

def annotate(ax,text,y=.97):
    ax.text(.98,y,text,transform=ax.transAxes,ha="right",va="top",fontsize=6.0,color=GRAY_DARK)

def paired_bar(ax,a,b,labels,ylabel,colors=(GRAY_DARK,RED),p=None):
    a=np.asarray(a,float); b=np.asarray(b,float)
    ok=np.isfinite(a)&np.isfinite(b); a,b=a[ok],b[ok]
    x=np.array([0.,1.])
    for aa,bb in zip(a,b):
        ax.plot(x,[aa,bb],color=GRAY_LIGHT,lw=.65,zorder=1)
    means=[a.mean(),b.mean()]; errs=[sem(a),sem(b)]
    ax.bar(x,means,width=.48,color=colors,edgecolor="none",zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,capsize=2.4,lw=.9,zorder=3)
    ax.set_xticks(x,labels); ax.set_xlim(-.68,1.68); ax.set_ylabel(ylabel,labelpad=3)
    clean_ax(ax)
    if p is None: p=pwil(a,b)
    annotate(ax,f"n={len(a)}; {pfmt(p)}")
    return a,b

def dist(ax,v,label,ylabel,color=RED,p=None,zero=True):
    v=np.asarray(v,float); v=v[np.isfinite(v)]
    rng=np.random.default_rng(23)
    x=rng.normal(0,.055,len(v))
    ax.scatter(x,v,s=9,color=GRAY_MID,alpha=.72,linewidths=0,zorder=2)
    ax.errorbar([0],[v.mean()],yerr=[sem(v)],fmt="o",ms=4.4,color=color,ecolor=color,capsize=3,lw=1.1,zorder=4)
    if zero: ax.axhline(0,color=GRAY_LIGHT,lw=.7,ls="--",zorder=0)
    ax.set_xticks([0],[label]); ax.set_xlim(-.42,.42); ax.set_ylabel(ylabel,labelpad=3)
    clean_ax(ax)
    if p is None: p=pwil(v)
    annotate(ax,f"n={len(v)}; {pfmt(p)}")
    return v

def grouped(ax,groups,labels,ylabel,colors,pvals):
    rng=np.random.default_rng(31)
    x=np.arange(len(groups),dtype=float)*1.35
    for i,(g,c,p) in enumerate(zip(groups,colors,pvals)):
        g=np.asarray(g,float); g=g[np.isfinite(g)]
        jit=rng.normal(i,.055,len(g))
        ax.scatter(jit,g,s=8.5,color=GRAY_MID,alpha=.68,linewidths=0,zorder=2)
        ax.errorbar([i],[g.mean()],yerr=[sem(g)],fmt="o",ms=4.3,color=c,ecolor=c,capsize=3,lw=1.05,zorder=4)
    ax.axhline(0,color=GRAY_LIGHT,lw=.7,ls="--",zorder=0)
    ax.set_xticks(x,labels); ax.set_xlim(-.68,x[-1]+.68); ax.set_ylabel(ylabel,labelpad=3)
    clean_ax(ax)
    ymin,ymax=ax.get_ylim(); span=ymax-ymin
    for i,p in enumerate(pvals):
        lab="P<1e-7" if p < 1e-7 else pfmt(p)
        ax.text(x[i],ymax-.025*span,lab,ha="center",va="top",fontsize=4.8,color=GRAY_DARK)

def save(fig,stem):
    fig.set_size_inches(SIZE_IN,SIZE_IN,forward=True)
    for ext in ("png","pdf","svg"):
        kw=dict(bbox_inches=None,pad_inches=0)
        if ext=="png": kw["dpi"]=DPI
        fig.savefig(ASSET/f"{stem}.{ext}",**kw)
    fig.savefig(ASSET/f"{stem}_mobile.png",dpi=DPI,bbox_inches=None,pad_inches=0)
    plt.close(fig)

apply_rc(False)
fig,ax=plt.subplots(2,2,figsize=(SIZE_IN,SIZE_IN))
fig.subplots_adjust(left=.18,right=.985,bottom=.13,top=.965,wspace=.50,hspace=.50)
ax=ax.ravel()

D=pd.read_csv(DATA/"SLM_native_feed_observed_content_per_animal_v1.csv")
wide={m:D[D.model.eq(m)].set_index("animal") for m in ["self_social","plus_recency","plus_observed_content"]}
idx=wide["self_social"].index
for m in ["plus_recency","plus_observed_content"]:
    idx=idx.intersection(wide[m].index)

# A: simple recency control
paired_bar(ax[0],wide["self_social"].loc[idx,"logloss"],wide["plus_recency"].loc[idx,"logloss"],
           ["Current\nstate","+ recent\nObserve"],"Held-animal log loss",
           colors=(GRAY_DARK,GRAY_MID),
           p=pwil(wide["self_social"].loc[idx,"logloss"],wide["plus_recency"].loc[idx,"logloss"]))
panel_label(ax[0],"A")

# B: content improves held-animal calibration
paired_bar(ax[1],wide["plus_recency"].loc[idx,"logloss"],wide["plus_observed_content"].loc[idx,"logloss"],
           ["Recency","+ observed\ncontent"],"Held-animal log loss",
           colors=(GRAY_DARK,RED),
           p=pwil(wide["plus_recency"].loc[idx,"logloss"],wide["plus_observed_content"].loc[idx,"logloss"],alternative="greater"))
panel_label(ax[1],"B")

# C: Brier gain, every held animal
brier_gain=(wide["plus_recency"].loc[idx,"brier"]-wide["plus_observed_content"].loc[idx,"brier"]).values
dist(ax[2],brier_gain,"Observed-content\ngain","Brier improvement",RED,
     pwil(brier_gain,alternative="greater"),True)
panel_label(ax[2],"C")

# D: content specificity, now animal-level rather than three summary bars
S=pd.read_csv(DATA/"SOE_feed_content_specificity_per_animal_v68.csv")
order=["feed_after_demfeed","feed_after_no_demfeed","nonfeed_after_demfeed"]
labels=["Feed |\nDem+","Feed |\nDem-","No Feed |\nDem+"]
groups=[S[S.subset.eq(s)].mean_gain.values for s in order]
pvals=[pwil(groups[0],alternative="greater"),pwil(groups[1],alternative="less"),pwil(groups[2],alternative="less")]
grouped(ax[3],groups,labels,"Δ log P(actual outcome)",[RED,GRAY_DARK,GRAY_MID],pvals)
panel_label(ax[3],"D")

save(fig,"SOE_feed_content_specificity_v68")
print("generated SOE_feed_content_specificity_v68")
print("A",pwil(wide["self_social"].loc[idx,"logloss"],wide["plus_recency"].loc[idx,"logloss"]))
print("B",pwil(wide["plus_recency"].loc[idx,"logloss"],wide["plus_observed_content"].loc[idx,"logloss"],alternative="greater"))
print("C",pwil(brier_gain,alternative="greater"),"positive",int((brier_gain>0).sum()),"/",len(brier_gain))
print("D",[(s,len(g),int((g>0).sum()),float(np.mean(g)),p) for s,g,p in zip(order,groups,pvals)])
