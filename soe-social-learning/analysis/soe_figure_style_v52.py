from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# SOE manuscript plotting authority V52 (2026-10-05)
SIZE_IN = 3.35
DPI = 600
RED = "#B2232E"
CYAN = "#87CDD4"
GRAY_DARK = "#555555"
GRAY_MID = "#999999"
GRAY_LIGHT = "#D7D7D7"
BLACK = "#222222"

def apply_rc(mobile=False):
    base = 7.4 if mobile else 7.0
    mpl.rcParams.update({
        "font.family": "Arial",
        "font.size": base,
        "axes.titlesize": base,
        "axes.labelsize": base,
        "xtick.labelsize": base - 0.5,
        "ytick.labelsize": base - 0.5,
        "legend.fontsize": base - 0.5,
        "axes.linewidth": 0.75,
        "xtick.major.width": 0.75,
        "ytick.major.width": 0.75,
        "xtick.major.size": 2.4,
        "ytick.major.size": 2.4,
        "lines.linewidth": 1.25,
        "patch.linewidth": 0.0,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })

def clean_ax(ax):
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.75)
    ax.spines["bottom"].set_linewidth(0.75)
    ax.tick_params(width=0.75, length=2.4, pad=2.0)
    return ax

def panel_label(ax, letter):
    ax.text(-0.13, 1.01, letter, transform=ax.transAxes,
            ha="left", va="bottom", fontsize=9, fontweight="bold",
            color=BLACK, clip_on=False)

def compact_label(label):
    label=str(label)
    if "\n" in label:
        return label
    explicit={
        "Nested-CV CK":"Nested-CV\nCK",
        "Not feeding":"Not\nfeeding",
        "Dem feeding":"Dem\nfeeding",
        "Expected info":"Expected\ninfo",
        "Current social":"Current\nsocial",
        "Full history":"Full\nhistory",
        "History MLP":"History\nMLP",
        "Current + CK":"Current\n+ CK",
        "Choice kernel":"Choice\nkernel",
        "Global uncertainty":"Global\nuncertainty",
        "Uncertainty state":"Uncertainty\nstate",
    }
    if label in explicit:
        return explicit[label]
    if len(label)>11 and " " in label:
        parts=label.split()
        if len(parts)==2:
            return parts[0]+"\n"+parts[1]
    return label

def categorical_geometry(n):
    x = np.arange(n, dtype=float)
    width = 0.5
    xlim = (-0.75, n - 0.25)
    return x, width, xlim

def sem(a):
    a=np.asarray(a,float)
    a=a[np.isfinite(a)]
    return np.nan if len(a)<2 else float(np.std(a,ddof=1)/np.sqrt(len(a)))

def paired_bars(ax, left, right, left_color=GRAY_DARK, right_color=RED,
                labels=("Comparator","Structured"), ylabel=None):
    left=np.asarray(left,float); right=np.asarray(right,float)
    ok=np.isfinite(left)&np.isfinite(right)
    left,right=left[ok],right[ok]
    x,w,xlim=categorical_geometry(2)
    for a,b in zip(left,right):
        ax.plot(x,[a,b],color=GRAY_LIGHT,lw=0.75,zorder=1)
    means=[float(np.mean(left)),float(np.mean(right))]
    errs=[sem(left),sem(right)]
    ax.bar(x,means,width=w,color=[left_color,right_color],edgecolor="none",linewidth=0,zorder=2)
    ax.errorbar(x,means,yerr=errs,fmt="none",ecolor=BLACK,elinewidth=0.8,capsize=2.0,capthick=0.8,zorder=3)
    ax.set_xlim(*xlim)
    ax.set_xticks(x,[compact_label(v) for v in labels])
    if ylabel: ax.set_ylabel(ylabel,labelpad=3)
    clean_ax(ax)
    return ax

def categorical_bars(ax, values, labels, colors, errors=None, ylabel=None, rotation=0):
    values=np.asarray(values,float)
    n=len(values)
    x,w,xlim=categorical_geometry(n)
    ax.bar(x,values,width=w,color=colors,edgecolor="none",linewidth=0,
           yerr=errors,ecolor=BLACK,capsize=2.0,error_kw={"elinewidth":0.8,"capthick":0.8})
    ax.set_xlim(*xlim)
    ax.set_xticks(x,[compact_label(v) for v in labels],rotation=rotation,ha="right" if rotation else "center")
    if ylabel: ax.set_ylabel(ylabel,labelpad=3)
    clean_ax(ax)
    return ax


def horizontal_bars(ax, values, labels, colors, errors=None, xlabel=None):
    values=np.asarray(values,float)
    n=len(values)
    y=np.arange(n,dtype=float)[::-1]
    height=0.5
    ax.barh(y,values,height=height,color=colors,edgecolor="none",linewidth=0,
            xerr=errors,ecolor=BLACK,capsize=2.0,error_kw={"elinewidth":0.8,"capthick":0.8})
    ax.set_ylim(-0.75,n-0.25)
    ax.set_yticks(y,[compact_label(v) for v in labels])
    if xlabel: ax.set_xlabel(xlabel,labelpad=3)
    clean_ax(ax)
    return ax

def square_figure(nrows=1,ncols=1,mobile=False):
    apply_rc(mobile=mobile)
    fig,axs=plt.subplots(nrows,ncols,figsize=(SIZE_IN,SIZE_IN),squeeze=False)
    # Compact manuscript geometry: small outer margin and panel gaps.
    if nrows==1 and ncols==1:
        fig.subplots_adjust(left=.19,right=.97,bottom=.18,top=.96)
    else:
        fig.subplots_adjust(left=.15,right=.985,bottom=.13,top=.965,
                            wspace=.42 if mobile else .34,
                            hspace=.48 if mobile else .38)
    return fig,axs

def save_square(fig, stem: Path, mobile=False, also_vector=True):
    stem=Path(stem)
    fig.set_size_inches(SIZE_IN,SIZE_IN,forward=True)
    # No bbox_inches='tight': physical size must remain 3.35 x 3.35 in.
    fig.savefig(stem.with_suffix(".png"),dpi=DPI,bbox_inches=None,pad_inches=0)
    if also_vector and not mobile:
        fig.savefig(stem.with_suffix(".pdf"),bbox_inches=None,pad_inches=0)
        fig.savefig(stem.with_suffix(".svg"),bbox_inches=None,pad_inches=0)
