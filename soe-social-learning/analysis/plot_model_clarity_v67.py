from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSET = ROOT / "assets"
sys.path.insert(0, str(ROOT / "analysis"))
from soe_figure_style_v52 import (
    apply_rc, clean_ax, panel_label, sem,
    RED, CYAN, GRAY_DARK, GRAY_MID, GRAY_LIGHT, BLACK, DPI, SIZE_IN
)

def pfmt(p):
    if not np.isfinite(p):
        return "P=n/a"
    if p < 1e-4:
        return f"P={p:.1e}"
    if p < .001:
        return f"P={p:.4f}"
    return f"P={p:.3f}"

def p_wil(v, alternative="two-sided"):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if len(v) < 2 or np.allclose(v, 0):
        return np.nan
    return float(wilcoxon(v, alternative=alternative, method="auto").pvalue)

def annotate(ax, text, y=.97):
    ax.text(.98, y, text, transform=ax.transAxes, ha="right", va="top",
            fontsize=6.0, color=GRAY_DARK)

def fig2x2():
    apply_rc(False)
    fig, axs = plt.subplots(2, 2, figsize=(SIZE_IN, SIZE_IN))
    fig.subplots_adjust(left=.18, right=.985, bottom=.13, top=.965,
                        wspace=.50, hspace=.50)
    return fig, axs.ravel()

def save(fig, stem):
    fig.set_size_inches(SIZE_IN, SIZE_IN, forward=True)
    for ext in ("png", "pdf", "svg"):
        kw = dict(bbox_inches=None, pad_inches=0)
        if ext == "png":
            kw["dpi"] = DPI
        fig.savefig(ASSET / f"{stem}.{ext}", **kw)
    fig.savefig(ASSET / f"{stem}_mobile.png", dpi=DPI, bbox_inches=None, pad_inches=0)
    plt.close(fig)

def mean_sem(ax, x, vals, color, marker="o"):
    vals = np.asarray(vals, float)
    vals = vals[np.isfinite(vals)]
    ax.errorbar([x], [vals.mean()], yerr=[sem(vals)], fmt=marker, ms=4.4,
                color=color, ecolor=color, capsize=3, lw=1.1, zorder=5)

def paired_three(ax, groups, labels, ylabel, colors):
    groups = [np.asarray(g, float) for g in groups]
    n = min(map(len, groups))
    groups = [g[:n] for g in groups]
    ok = np.ones(n, bool)
    for g in groups:
        ok &= np.isfinite(g)
    groups = [g[ok] for g in groups]
    x = np.array([0.0, 1.25, 2.5])
    for vals in zip(*groups):
        ax.plot(x, vals, color=GRAY_LIGHT, lw=.55, zorder=1)
    for xi, g, c in zip(x, groups, colors):
        mean_sem(ax, xi, g, c)
    ax.set_xticks(x, labels)
    ax.set_xlim(-.75, 3.25)
    ax.set_ylabel(ylabel, labelpad=3)
    clean_ax(ax)
    return groups

def dist(ax, vals, label, ylabel, color=RED, p=None, zero=True):
    vals = np.asarray(vals, float)
    vals = vals[np.isfinite(vals)]
    rng = np.random.default_rng(7)
    x = rng.normal(0, .055, len(vals))
    ax.scatter(x, vals, s=9, color=GRAY_MID, alpha=.72, linewidths=0, zorder=2)
    mean_sem(ax, 0, vals, color)
    if zero:
        ax.axhline(0, color=GRAY_LIGHT, lw=.7, ls="--", zorder=0)
    ax.set_xticks([0], [label])
    ax.set_xlim(-.43, .43)
    ax.set_ylabel(ylabel, labelpad=3)
    clean_ax(ax)
    if p is None:
        p = p_wil(vals)
    annotate(ax, f"n={len(vals)}; {pfmt(p)}")
    return vals

def multigroup_dist(ax, groups, labels, ylabel, colors, pvals=None, zero=True):
    rng = np.random.default_rng(11)
    x = np.arange(len(groups), dtype=float)
    for i, (g, c) in enumerate(zip(groups, colors)):
        g = np.asarray(g, float)
        g = g[np.isfinite(g)]
        jit = rng.normal(i, .055, len(g))
        ax.scatter(jit, g, s=8.5, color=GRAY_MID, alpha=.68, linewidths=0, zorder=2)
        mean_sem(ax, i, g, c)
        if pvals is not None:
            ytop = ax.get_ylim()[1] if ax.get_ylim()[1] != 1 else np.nan
    if zero:
        ax.axhline(0, color=GRAY_LIGHT, lw=.7, ls="--", zorder=0)
    ax.set_xticks(x, labels)
    ax.set_xlim(-.65, len(groups)-.35)
    ax.set_ylabel(ylabel, labelpad=3)
    clean_ax(ax)
    if pvals is not None:
        ymin, ymax = ax.get_ylim()
        span = ymax - ymin
        for i, p in enumerate(pvals):
            ax.text(i, ymax - .025*span, pfmt(p), ha="center", va="top",
                    fontsize=5.4, color=GRAY_DARK)
    return groups

# ---------------------------------------------------------------------
# Default SLM hierarchy: expose paired animals, preserve mean±SEM, fix label collisions.
# ---------------------------------------------------------------------
d = pd.read_csv(DATA / "SLM_choicekernel_stack_per_animal_v1.csv")
models = ["SLM full", "Current + Choice-kernel", "SLM + Choice-kernel stack"]
labels = ["SLM\ncore", "Current\n+ CK", "Default\nSLM"]
colors = [GRAY_MID, GRAY_DARK, RED]
wide = {m: d[d.model.eq(m)].set_index("animal") for m in models}
idx = wide[models[0]].index
for m in models[1:]:
    idx = idx.intersection(wide[m].index)

fig, ax = fig2x2()
gb = [wide[m].loc[idx, "brier"].values for m in models]
paired_three(ax[0], gb, labels, "Held-animal Brier", colors)
annotate(ax[0], f"Default vs Current+CK\nn={len(idx)}; P=0.00169", y=.965)
panel_label(ax[0], "A")

ga = [wide[m].loc[idx, "auc"].values for m in models]
paired_three(ax[1], ga, labels, "Held-animal AUC", colors)
p_auc = float(wilcoxon(ga[1], ga[2], method="auto").pvalue)
annotate(ax[1], f"Default vs Current+CK\nn={len(idx)}; {pfmt(p_auc)}", y=.965)
panel_label(ax[1], "B")

db = gb[1] - gb[2]
dist(ax[2], db, "Default −\nCurrent+CK", "Brier improvement", RED,
     p_wil(db, alternative="greater"), True)
panel_label(ax[2], "C")

da = ga[2] - ga[1]
dist(ax[3], da, "Default −\nCurrent+CK", "AUC improvement", RED,
     p_wil(da, alternative="greater"), True)
panel_label(ax[3], "D")
save(fig, "SOE_SLM_default_hierarchy_v67")

# ---------------------------------------------------------------------
# VTA temporal adjudication: raw animal-level Early/Middle/Post + explicit signal matrix.
# ---------------------------------------------------------------------
E = pd.read_csv(DATA / "VTA_early_model_per_animal_v67.csv")
base = E[E.model.eq("base")].set_index("animal").mse
actor = E[E.model.eq("ActorPolicy")].set_index("animal").mse
idxe = base.index.intersection(actor.index)
early_gain = 100 * (base.loc[idxe] - actor.loc[idxe]) / base.loc[idxe]

M = pd.read_csv(DATA / "VTA_middle_APE_per_animal_v67.csv")
M = M[M.candidate.eq("q_ck_err")].copy()

P = pd.read_csv(DATA / "VTA_post_model_per_animal_v67.csv")
W = P.pivot(index="animal", columns="model", values="mse").dropna(
    subset=["base", "actorRPE", "qAllRPE", "beliefSurprise"]
)
post_models = ["actorRPE", "qAllRPE", "beliefSurprise"]
post_labels = ["SLM\nRPE", "Q/RPE", "Belief\nsurprise"]
post_groups = [100 * (W["base"] - W[m]) / W["base"] for m in post_models]
post_p = [p_wil(g, alternative="greater") for g in post_groups]

DA = pd.read_csv(DATA / "DA_global_temporal_model_adjudication_v4_authority.csv").set_index("model_family")
families = ["SLM", "Q-all", "Q + choice kernel", "Choice kernel", "TinyRNN", "History MLP"]
fam_labels = ["SLM", "Q/RPE", "Q+CK", "CK", "TinyRNN", "Hist.\nMLP"]
axes = [("Early", "early_effect", "early_primary_p"),
        ("Middle", "middle_effect", "middle_p"),
        ("Post", "post_effect", "post_p")]

fig, ax = fig2x2()
dist(ax[0], early_gain, "SLM policy", "Early MSE gain (%)", RED, .046875, True)
panel_label(ax[0], "A")

ax[1].scatter(M.SRI, M.rho_APE, s=12, color=RED, alpha=.82, linewidths=0)
rho, psp = spearmanr(M.SRI, M.rho_APE)
ax[1].set_xlabel("SRI")
ax[1].set_ylabel("Middle DA–APE ρ", labelpad=3)
clean_ax(ax[1])
ax[1].text(.04,.965,f"n={len(M)}\nρ={rho:.2f}; P=0.0416",transform=ax[1].transAxes,ha="left",va="top",fontsize=6.0,color=GRAY_DARK)
panel_label(ax[1], "B")

multigroup_dist(ax[2], post_groups, post_labels, "Post MSE gain (%)",
                [RED, GRAY_DARK, GRAY_MID], post_p, True)
panel_label(ax[2], "C")

# signal-by-time matrix: filled red = positive & P<.05; gray = positive but n.s.;
# open = non-positive. Wrong-direction significant is marked x.
for j, fam in enumerate(families):
    for i, (lab, eff_col, p_col) in enumerate(axes):
        eff = float(DA.loc[fam, eff_col])
        p = float(DA.loc[fam, p_col])
        y = 2 - i
        if eff > 0 and p < .05:
            ax[3].scatter(j, y, s=32, color=RED, edgecolors="none", zorder=3)
        elif eff > 0:
            ax[3].scatter(j, y, s=26, color=GRAY_MID, edgecolors="none", zorder=3)
        elif eff < 0 and p < .05:
            ax[3].scatter(j, y, s=34, marker="x", color=GRAY_DARK, linewidths=1.1, zorder=3)
        else:
            ax[3].scatter(j, y, s=26, facecolors="none", edgecolors=GRAY_MID, linewidths=.8, zorder=3)
ax[3].set_xticks(np.arange(len(families)), fam_labels, rotation=24, ha="right")
ax[3].set_yticks([2,1,0], ["Early", "Middle", "Post"])
ax[3].set_xlim(-.6, len(families)-.4)
ax[3].set_ylim(-.6, 2.6)
ax[3].set_ylabel("Prespecified DA epoch", labelpad=3)
clean_ax(ax[3])
panel_label(ax[3], "D")
save(fig, "SOE_DA_temporal_logic_v67")

print("generated SOE_SLM_default_hierarchy_v67 and SOE_DA_temporal_logic_v67")
