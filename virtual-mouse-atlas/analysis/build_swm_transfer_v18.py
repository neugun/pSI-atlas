from __future__ import print_function
import csv, json, math, os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
VM = ROOT / "virtual-mouse-atlas"
DATA = VM / "data"
ASSETS = VM / "assets"

ST17 = ROOT / "brain-world-model" / "data" / "stage17_recurrent_memory_paired.json"
FROZEN = ROOT / "soe-social-learning" / "data" / "SOE_to_external_frozen_v2_summary.csv"
FROZEN_MONKEY = ROOT / "soe-social-learning" / "data" / "SOE_to_macaque_frozen_transfer_by_monkey_v2.csv"
RAT = ROOT / "soe-social-learning" / "data" / "rat001169_nestedCV_multimetric_summary_v7.csv"
XSP = ROOT / "soe-social-learning" / "data" / "SOE_crossspecies_classical_comparator_audit_v2.csv"

GRAY = "#9a9a9a"
LIGHT = "#d2d2d2"
DARK = "#333333"
RED = "#b2232e"

def read_csv(path):
    with open(str(path), "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

with open(str(ST17), "r", encoding="utf-8") as f:
    st17 = json.load(f)
frozen = read_csv(FROZEN)
frozen_monkey = read_csv(FROZEN_MONKEY)
rat = read_csv(RAT)
xsp = read_csv(XSP)

rat_by_metric = {r["metric"]: r for r in rat}
xsp_by_dataset = {r["dataset"]: r for r in xsp}
mac_rows = [r for r in frozen if r["target"] == "macaque001435"]
mac_rows.sort(key=lambda r: float(r["frac"]))
mac_monkeys = {}
for r in frozen_monkey:
    mac_monkeys.setdefault(r["monkey"], []).append(r)
for k in list(mac_monkeys):
    mac_monkeys[k].sort(key=lambda r: float(r["frac"]))

audit = {
    "version": "v18",
    "status": "PASS_REPRESENTATIVE_POSITIVE_EXTERNAL_TESTS",
    "framing": "Representative positive external tests of SOE-trained SWM dynamics and shared multiscale state; not a universal-transfer claim.",
    "learned_recurrent_state": {
        "comparison": st17["comparison"],
        "heldout_axis": st17["heldout_axis"],
        "gru4_median_bits_per_trial": 0.17680896818637848,
        "gru4_params": 161,
        "paired_vs_current_plus_prev": st17["tests"]["current_plus_prev_linear_bits_per_trial"],
        "folds": st17["folds"],
    },
    "frozen_core_transfer": {
        "dataset": "Macaque DANDI001435",
        "contract": "Freeze SOE-trained recurrent core; train only target adapter/head; compare with equally frozen random recurrent core.",
        "nested_animals": 2,
        "fractions": mac_rows,
        "by_monkey": mac_monkeys,
        "inference_note": "Session-level sensitivity statistics are nested within two monkeys and are not population-level primate inference.",
    },
    "rat_multiscale_state": {
        "dataset": "Rat DANDI001169",
        "contract": "Outer held-rat CV with classical-family selection only inside training folds; CK selected in 5/5 outer folds.",
        "metrics": rat_by_metric,
    },
    "crossspecies_structured_state": {
        "human": xsp_by_dataset["Human exp/obs"],
        "rat": xsp_by_dataset["Rat DANDI001169"],
        "macaque_sensitivity": xsp_by_dataset["Macaque global"],
    },
    "sources": [
        "../brain-world-model/data/stage17_recurrent_memory_paired.json",
        "../soe-social-learning/data/SOE_to_external_frozen_v2_summary.csv",
        "../soe-social-learning/data/SOE_to_macaque_frozen_transfer_by_monkey_v2.csv",
        "../soe-social-learning/data/rat001169_nestedCV_multimetric_summary_v7.csv",
        "../soe-social-learning/data/SOE_crossspecies_classical_comparator_audit_v2.csv",
    ],
}
with open(str(DATA / "swm_transfer_v18.json"), "w", encoding="utf-8") as f:
    json.dump(audit, f, indent=2, ensure_ascii=False)

def sem(a):
    a = np.asarray(a, dtype=float)
    return float(a.std(ddof=1) / math.sqrt(len(a))) if len(a) > 1 else 0.0

def clean(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    ax.tick_params(width=0.75, length=3)
    for s in ["left", "bottom"]:
        ax.spines[s].set_linewidth(0.75)

def make_plot(lang="en"):
    zh = lang == "zh"
    plt.rcParams.update({
        "font.family": "Microsoft YaHei" if zh else "Arial",
        "font.size": 9.0,
        "axes.titlesize": 10.0,
        "axes.labelsize": 9.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "svg.fonttype": "none",
    })
    fig, axs = plt.subplots(2, 2, figsize=(8.0, 8.0))
    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.09, top=0.92, wspace=0.34, hspace=0.42)

    # A. recurrent memory paired cohort test
    ax = axs[0, 0]
    folds = st17["folds"]
    prev = np.array([float(r["current_plus_prev_linear_bits_per_trial"]) for r in folds])
    gru = np.array([float(r["gru4"]) for r in folds])
    for a, b in zip(prev, gru):
        ax.plot([0, 1], [a, b], color=LIGHT, lw=0.9, zorder=1)
    means = [prev.mean(), gru.mean()]
    errs = [sem(prev), sem(gru)]
    ax.bar([0, 1], means, width=0.28, color=[GRAY, RED], edgecolor="none", zorder=2)
    ax.errorbar([0, 1], means, yerr=errs, fmt="none", ecolor=DARK, lw=1.0, capsize=2.5, zorder=3)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Current+prev", "GRU4"] if not zh else ["当前+前一trial", "GRU4"])
    ax.set_ylabel("Bits / trial" if not zh else "Bits / trial")
    ax.set_title(("A  Learned recurrent memory transfers" if not zh else "A  学到的 recurrent memory 可迁移"), loc="left", fontweight="bold")
    ax.text(0.03, 0.96,
            ("7/7 cohorts; median Δ=+0.0579\nP=0.0078; 161 parameters" if not zh else
             "7/7 cohorts；median Δ=+0.0579\nP=0.0078；161 个参数"),
            transform=ax.transAxes, va="top", ha="left", fontsize=8.1)
    clean(ax)

    # B. frozen core -> macaque
    ax = axs[0, 1]
    fracs = np.array([20, 50, 100], dtype=float)
    monkey_names = sorted(mac_monkeys.keys())
    monkey_curves = []
    for name in monkey_names:
        vals = np.array([float(r["mean_gain"]) for r in mac_monkeys[name]], dtype=float)
        monkey_curves.append(vals)
        ax.plot(fracs, vals, color=LIGHT, lw=1.0, zorder=1)
    pooled = np.array([float(r["mean_gain"]) for r in mac_rows], dtype=float)
    ax.plot(fracs, pooled, color=RED, lw=2.0, zorder=3)
    ax.axhline(0, color=GRAY, lw=0.7, ls="--")
    ax.set_xticks(fracs)
    ax.set_xticklabels(["20%", "50%", "100%"])
    ax.set_ylabel("ΔNLL vs frozen random" if not zh else "ΔNLL（相对冻结随机 core）")
    ax.set_title(("B  Frozen SOE core → macaque" if not zh else "B  冻结 SOE core → 猕猴"), loc="left", fontweight="bold")
    ax.text(0.03, 0.96,
            ("100%: 10/10 sessions improve\nboth monkeys 5/5; nested n=2" if not zh else
             "100%：10/10 sessions 改善\n两只猴均 5/5；嵌套 n=2"),
            transform=ax.transAxes, va="top", ha="left", fontsize=8.1)
    clean(ax)

    # C. rank-biserial effect across external tasks
    ax = axs[1, 0]
    human = float(xsp_by_dataset["Human exp/obs"]["rrb"])
    rat_rrb = float(xsp_by_dataset["Rat DANDI001169"]["rrb"])
    maca = float(xsp_by_dataset["Macaque global"]["rrb"])
    vals = [human, rat_rrb, maca]
    cols = [RED, RED, GRAY]
    xs = np.arange(3)
    ax.bar(xs, vals, width=0.38, color=cols, edgecolor="none")
    ax.set_xticks(xs)
    ax.set_xticklabels(["Human\n10 subj", "Rat\n10 rats", "Macaque\n44 dates"] if not zh
                       else ["Human\n10 人", "Rat\n10 只", "Macaque\n44 dates"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Rank-biserial effect" if not zh else "Rank-biserial effect")
    ax.set_title(("C  Shared structured-state advantage" if not zh else "C  Structured state 跨任务优势"), loc="left", fontweight="bold")
    ax.text(0.03, 0.96,
            ("held-subject / held-rat tests in red\nmacaque = 2-monkey nested sensitivity" if not zh else
             "红色：held-subject / held-rat\n猕猴：2 只猴嵌套 sensitivity"),
            transform=ax.transAxes, va="top", ha="left", fontsize=8.1)
    clean(ax)

    # D. rat multi-metric robustness
    ax = axs[1, 1]
    metrics = ["brier", "nll", "auc"]
    winfrac = [float(rat_by_metric[m]["wins"]) / float(rat_by_metric[m]["n"]) for m in metrics]
    ax.bar(np.arange(3), winfrac, width=0.38, color=RED, edgecolor="none")
    ax.set_xticks(np.arange(3))
    ax.set_xticklabels(["Brier", "NLL", "AUC"])
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("Fraction of held-out rats" if not zh else "留出大鼠中支持比例")
    ax.set_title(("D  Rat result survives metric changes" if not zh else "D  Rat 结果跨指标稳定"), loc="left", fontweight="bold")
    ax.text(0.03, 0.96,
            ("8/10, 8/10, 9/10 favor structured\nnested-CV classical family selection" if not zh else
             "8/10、8/10、9/10 支持 structured\nclassical family 采用 nested-CV 选择"),
            transform=ax.transAxes, va="top", ha="left", fontsize=8.1)
    clean(ax)

    fig.suptitle(("SWM transfer: learned memory, frozen dynamics, and external task support" if not zh
                  else "SWM 迁移：学到的记忆、冻结动力学与外部任务支持"),
                 fontsize=12.2, fontweight="bold", y=0.975)

    suffix = "_zh" if zh else ""
    for ext in ["png", "svg"]:
        fig.savefig(str(ASSETS / ("swm_transfer_v18%s.%s" % (suffix, ext))),
                    dpi=420, bbox_inches="tight")
    plt.close(fig)

make_plot("en")
make_plot("zh")

# Matplotlib 3.2 emits trailing spaces inside SVG path lines; strip them so
# repository whitespace checks remain clean without altering vector geometry.
for svg_name in ["swm_transfer_v18.svg", "swm_transfer_v18_zh.svg"]:
    p = ASSETS / svg_name
    s = p.read_text(encoding="utf-8")
    p.write_text("\n".join(line.rstrip() for line in s.splitlines()) + "\n", encoding="utf-8")

print("WROTE", DATA / "swm_transfer_v18.json")
print("WROTE", ASSETS / "swm_transfer_v18.svg")
print("WROTE", ASSETS / "swm_transfer_v18_zh.svg")