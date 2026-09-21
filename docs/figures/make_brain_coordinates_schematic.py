"""Schematic: where pSI sits and how the two coordinate systems relate.

Panel A  side view of a mouse skull/brain with bregma, the AP axis and the
         pSI AP window (PSI_AP_RANGE, -0.7 ... -1.6 mm behind bregma).
Panel B  coronal outline at AP -0.90 mm with ML/DV axes, Allen SI (id 342)
         drawn as pSI, GPe as context, and the 2021 / 2024 preset crosses.
Panel C  Franklin-Paxinos stereotaxic mm  <->  Allen CCFv3 voxel index, with
         the arithmetic exactly as implemented in src/lib/ccfCoordinates.ts.

Shapes are schematic (not traced from the atlas). Numbers come from the site
source: ccfCoordinates.ts (CCF_SHAPE, CCF_BREGMA_UM, PSI_AP_RANGE),
coordinates.ts (viewerBounds, presets). The SI centroid (ML 1.91, DV -5.37)
is the value returned by "Center on Allen SI" at the 2021 preset when the
site's own code was run offline against the public CCFv3 data (README,
"Example result").

Run from the repository root:  python docs/figures/make_brain_coordinates_schematic.py
Requires numpy + matplotlib only.
"""
from __future__ import annotations

import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon, Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schematic_style import C, apply_style, arrow, box, hide_axes, save, stamp  # noqa: E402

# ---- constants copied from src/lib/ccfCoordinates.ts and src/lib/coordinates.ts
CCF_RESOLUTION_MM = 0.05
CCF_SHAPE = {"ml": 228, "dv": 160, "ap": 264}
CCF_BREGMA_UM = {"ml": 5739, "ap": 5400, "dv": 332}
SI_STRUCTURE_ID = 342
PSI_AP_RANGE = {"anterior": -0.7, "posterior": -1.6}
VIEWER_BOUNDS = {"ap": (-3.0, 1.0), "ml": (0.0, 5.6), "dv": (-7.5, 0.3)}
PRESETS = {
    "2021": {"ap": -0.9, "ml": 2.3, "dv": -4.5},
    "2024": {"ap": -0.9, "ml": 2.2, "dv": -4.5},
}
SI_CENTROID_2021 = {"ml": 1.91, "dv": -5.37}  # 'Center on Allen SI' result at AP -0.90

ACCENT = C["blue"]           # the thing the figure is about: pSI / Allen SI
PRESET_COL = C["vermilion"]  # published surgical presets
CTX = C["grey"]
MONO = "DejaVu Sans Mono"


def stereotaxic_to_voxel(ap: float, ml: float, dv: float) -> dict[str, int]:
    """Same arithmetic as stereotaxicToVoxel() in ccfCoordinates.ts (lines 23-29)."""
    def clamp(axis: str, value: float) -> int:
        return int(min(CCF_SHAPE[axis] - 1, max(0, round(value))))
    return {
        "ml": clamp("ml", (CCF_BREGMA_UM["ml"] + ml * 1000) / 50),
        "dv": clamp("dv", (CCF_BREGMA_UM["dv"] - dv * 1000) / 50),
        "ap": clamp("ap", (CCF_BREGMA_UM["ap"] - ap * 1000) / 50),
    }


def title(ax, letter, text):
    ax.set_title(f"{letter}   {text}", loc="left", fontsize=12, weight="bold", pad=6)


def panel_a(ax):
    """Side view: anterior to the left, AP in mm from bregma on the x axis."""
    ax.set_xlim(5.9, -7.6)  # anterior (+) left, posterior (-) right
    ax.set_ylim(-8.3, 2.3)
    hide_axes(ax)
    ax.set_aspect("equal")
    ax.set_anchor("N")
    title(ax, "A", "Side view with bregma (schematic)")

    # brain outline (cerebrum + olfactory bulb + cerebellum), grey context
    t = np.linspace(0, 2 * np.pi, 200)
    cerebrum = np.c_[-1.4 + 4.6 * np.cos(t), -3.0 + 3.1 * np.sin(t)]
    ax.add_patch(Polygon(cerebrum, closed=True, fc="#F2F2F2", ec=CTX, lw=1.2, zorder=1))
    ax.add_patch(Ellipse((4.2, -3.6), 2.6, 1.9, fc="#F2F2F2", ec=CTX, lw=1.2, zorder=1))
    ax.add_patch(Ellipse((-6.4, -4.2), 2.6, 2.4, fc="#F2F2F2", ec=CTX, lw=1.2, zorder=1))
    ax.text(4.2, -3.6, "OB", ha="center", va="center", fontsize=8, color=CTX)
    ax.text(-6.4, -4.2, "CB", ha="center", va="center", fontsize=8, color=CTX)

    # skull: a curved line above the brain, bregma marked at AP 0
    xs = np.linspace(5.4, -7.4, 100)
    skull = 0.35 - 0.045 * (xs + 1.4) ** 2 * 0.25
    ax.plot(xs, skull, color=C["black"], lw=1.6, zorder=3)
    ax.text(5.3, 0.55, "skull", fontsize=9, color=C["black"], ha="left", va="bottom")
    y_b = float(np.interp(0.0, xs[::-1], skull[::-1]))
    ax.plot([0], [y_b], marker="o", ms=6, color=C["black"], zorder=5)
    ax.text(0.15, y_b + 0.45, "bregma\nAP 0 · ML 0 · DV 0", fontsize=9, weight="bold",
            ha="right", va="bottom", zorder=5, linespacing=1.2)

    # Allen SI as an elongated band at the ventral forebrain; posterior part = pSI
    si_x0, si_x1 = 0.8, -1.9          # schematic AP extent of SI
    ax.add_patch(Rectangle((si_x1, -5.7), si_x0 - si_x1, 1.0, fc="#DDDDDD", ec=CTX, lw=1.0, zorder=2))
    ax.text(1.05, -5.2, "Allen SI\n(id 342)", fontsize=8.5, color="#555555", ha="right", va="center", linespacing=1.2)
    ax.add_patch(Rectangle((PSI_AP_RANGE["posterior"], -5.7),
                           PSI_AP_RANGE["anterior"] - PSI_AP_RANGE["posterior"], 1.0,
                           fc="#CFE5F5", ec=ACCENT, lw=1.6, zorder=3))
    ax.text(-1.15, -5.2, "pSI", fontsize=9.5, weight="bold", color=ACCENT, ha="center", va="center", zorder=4)

    # pSI AP window projected up to the skull and down to the axis
    for x in (PSI_AP_RANGE["anterior"], PSI_AP_RANGE["posterior"]):
        ax.plot([x, x], [-7.0, y_b], color=ACCENT, lw=0.9, ls=":", zorder=2)
    ax.add_patch(Rectangle((PSI_AP_RANGE["posterior"], -7.0),
                           PSI_AP_RANGE["anterior"] - PSI_AP_RANGE["posterior"], y_b + 7.0,
                           fc=ACCENT, alpha=0.07, ec="none", zorder=1))
    ax.text(-1.85, 0.9, "pSI AP window [PSI_AP_RANGE]\n−0.7 … −1.6 mm behind bregma", fontsize=8.5,
            color=ACCENT, ha="left", va="bottom", linespacing=1.25)

    # injection track at AP -0.90 down to DV -4.5 (2021 preset depth)
    ax.plot([-0.9, -0.9], [y_b + 0.05, -4.5], color=PRESET_COL, lw=1.4, zorder=4)
    ax.plot([-0.9], [-4.5], marker="x", ms=7, mew=1.8, color=PRESET_COL, zorder=5)
    ax.text(-2.0, -3.3, "preset track\nAP −0.90\nDV −4.50", fontsize=8, color=PRESET_COL, ha="left",
            va="center", linespacing=1.2)

    # AP axis with ticks (viewer bounds -3 ... +1)
    y_ax = -7.5
    arrow(ax, (1.9, y_ax), (-3.7, y_ax), color=C["black"], lw=1.2)
    for tick in (1, 0, -1, -2, -3):
        ax.plot([tick, tick], [y_ax - 0.12, y_ax + 0.12], color=C["black"], lw=1)
        ax.text(tick, y_ax - 0.3, f"{tick:+d}" if tick else "0", fontsize=8, ha="center", va="top")
    ax.text(-3.9, y_ax, "AP (mm)\nviewer −3.0 … +1.0", fontsize=8.5, ha="left", va="center", linespacing=1.2)
    ax.text(2.1, y_ax, "anterior", fontsize=8, ha="right", va="center", color="#555555")


def panel_b(ax):
    """Coronal outline at AP -0.90 with real ML/DV axes (mm from bregma)."""
    ax.set_xlim(VIEWER_BOUNDS["ml"][0] - 0.1, VIEWER_BOUNDS["ml"][1] + 0.1)
    ax.set_ylim(-7.0, VIEWER_BOUNDS["dv"][1] + 0.3)
    ax.set_aspect("equal")
    ax.set_anchor("N")
    ax.set_xlabel("ML (mm from midline)", fontsize=9)
    ax.set_ylabel("DV (mm from bregma)", fontsize=9)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_yticks([0, -1, -2, -3, -4, -5, -6, -7])
    ax.tick_params(labelsize=8.5)
    ax.grid(True, color="#EEEEEE", lw=0.6)
    ax.set_axisbelow(True)
    title(ax, "B", "Coronal at AP −0.90 mm (schematic)")

    # right hemisphere outline (schematic dome), midline dashed at ML 0
    t = np.linspace(-np.pi / 2, np.pi / 2, 120)
    outer = np.c_[5.3 * np.cos(t) * 0.98, -3.1 + 3.25 * np.sin(t)]
    outer[:, 0] = np.clip(outer[:, 0], 0, None)
    ax.add_patch(Polygon(outer, closed=True, fc="#F5F5F5", ec=CTX, lw=1.2, zorder=1))
    ax.plot([0, 0], [-6.35, 0.15], color=CTX, lw=1.0, ls="--", zorder=2)
    ax.text(0.1, 0.0, "midline", fontsize=8, color=CTX, va="bottom")

    # context structures (grey)
    ax.add_patch(Ellipse((2.45, -4.1), 1.5, 1.6, angle=25, fc="#E3E3E3", ec=CTX, lw=1.0, zorder=2))
    ax.text(3.1, -4.75, "GPe\n(id 1022)", fontsize=8, color="#555555", ha="left", va="center", zorder=3,
            linespacing=1.15)
    ax.add_patch(Ellipse((3.65, -3.2), 0.7, 2.4, angle=20, fc="#EBEBEB", ec=CTX, lw=0.8, zorder=2))
    ax.text(4.15, -3.0, "int.\ncapsule", fontsize=8, color="#666666", ha="left", va="center", linespacing=1.15)
    ax.add_patch(Ellipse((3.0, -5.9), 1.3, 0.75, fc="#EBEBEB", ec=CTX, lw=0.8, zorder=2))
    ax.text(3.0, -5.9, "MeA", fontsize=8, color="#666666", ha="center", va="center")
    ax.add_patch(Ellipse((0.9, -5.6), 1.3, 1.0, fc="#EBEBEB", ec=CTX, lw=0.8, zorder=2))
    ax.text(0.9, -5.6, "LH", fontsize=8, color="#666666", ha="center", va="center")

    # Allen SI (id 342): at AP -0.90 the whole cross-section is inside the pSI window
    si = Ellipse((SI_CENTROID_2021["ml"], SI_CENTROID_2021["dv"]), 1.45, 0.85, angle=-12,
                 fc="#CFE5F5", ec=ACCENT, lw=1.8, zorder=3)
    ax.add_patch(si)
    ax.plot(SI_CENTROID_2021["ml"], SI_CENTROID_2021["dv"], marker="o", ms=6, color=ACCENT, zorder=5)
    ax.text(0.1, -6.85, "Allen SI (id 342) at AP −0.90 = pSI", fontsize=8.5, color=ACCENT, ha="left",
            va="bottom", zorder=4)

    # preset crosses
    for p in PRESETS.values():
        ax.plot(p["ml"], p["dv"], marker="x", ms=8, mew=2.0, color=PRESET_COL, zorder=6, ls="none")
    ax.annotate("× 2021 (2.30, −4.50)\n× 2024 (2.20, −4.50)\nCCFv3 label: GPe",
                xy=(PRESETS["2021"]["ml"] + 0.08, PRESETS["2021"]["dv"] + 0.1), xytext=(2.2, -1.3),
                fontsize=8.5, color=PRESET_COL, ha="left", va="center", linespacing=1.25,
                arrowprops=dict(arrowstyle="-|>", color=PRESET_COL, lw=1.0, shrinkA=0, shrinkB=3), zorder=6)
    ax.annotate("● 'Center on Allen SI'\n   ML 1.91 · DV −5.37",
                xy=(SI_CENTROID_2021["ml"] - 0.55, SI_CENTROID_2021["dv"] + 0.2), xytext=(0.15, -3.1),
                fontsize=8.5, color=ACCENT, ha="left", va="center", linespacing=1.25,
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.0, shrinkA=0, shrinkB=3), zorder=6)


def panel_c(ax):
    """Two coordinate systems and the conversion arithmetic. Axes units = inches."""
    W, H = 9.6, 3.85
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    hide_axes(ax)
    title(ax, "C", "Two coordinate systems and the conversion as implemented [ccfCoordinates.ts]")

    # left: Franklin-Paxinos
    box(ax, (0.1, 2.05), 4.0, 1.7, fc="#FBEFD9", ec=PRESET_COL, lw=1.4, radius=0.12)
    ax.text(2.1, 3.57, "Franklin–Paxinos stereotaxic (surgery)", ha="center", va="center", fontsize=9.5,
            weight="bold", color=PRESET_COL)
    ax.text(0.25, 3.32, "unit: mm from bregma (skull landmark)\nAP: + anterior, − posterior\n"
                        "ML: distance from the midline\nDV: − below bregma",
            ha="left", va="top", fontsize=8.5, linespacing=1.35)
    ax.text(0.25, 2.25, "2021 preset: AP −0.90 · ML 2.30 · DV −4.50", ha="left", va="center", fontsize=8.5,
            family=MONO)

    # right: Allen CCFv3 voxel
    box(ax, (5.5, 2.05), 4.0, 1.7, fc="#DCEBF6", ec=ACCENT, lw=1.4, radius=0.12)
    ax.text(7.5, 3.57, "Allen CCFv3 voxel index (annotation)", ha="center", va="center", fontsize=9.5,
            weight="bold", color=ACCENT)
    ax.text(5.65, 3.32,
            f"unit: 50 µm voxel [CCF_RESOLUTION_MM]\n"
            f"array (ML, DV, AP) = ({CCF_SHAPE['ml']}, {CCF_SHAPE['dv']}, {CCF_SHAPE['ap']}) [CCF_SHAPE]\n"
            f"bregma landmark [CCF_BREGMA_UM], µm:\n"
            f"ML {CCF_BREGMA_UM['ml']} · AP {CCF_BREGMA_UM['ap']} · DV {CCF_BREGMA_UM['dv']}",
            ha="left", va="top", fontsize=8.5, linespacing=1.35)
    v = stereotaxic_to_voxel(**PRESETS["2021"])
    ax.text(5.65, 2.25, f"→ voxel ML {v['ml']} · DV {v['dv']} · AP {v['ap']}  (label: GPe)", ha="left",
            va="center", fontsize=8.5, family=MONO)

    # arrows between the two
    arrow(ax, (4.1, 3.15), (5.5, 3.15), color=C["black"], lw=1.4, mutation_scale=16)
    arrow(ax, (5.5, 2.55), (4.1, 2.55), color=C["black"], lw=1.4, mutation_scale=16)
    ax.text(4.8, 3.23, "stereotaxicToVoxel", ha="center", va="bottom", fontsize=8, family=MONO)
    ax.text(4.8, 2.47, "voxelToStereotaxic", ha="center", va="top", fontsize=8, family=MONO)

    # the arithmetic, as implemented (lines 23-37)
    box(ax, (0.1, 0.1), 9.4, 1.8, fc="#F7F7F7", ec=C["black"], lw=1.0, radius=0.12)
    ax.text(0.25, 1.75, "Arithmetic in src/lib/ccfCoordinates.ts:23-37 — round, then clamp to 0 … shape − 1",
            ha="left", va="center", fontsize=9, weight="bold")
    code = (
        "ml_vox = round((5739 + ML_mm·1000) / 50)        ML_mm = (ml_vox·50 − 5739) / 1000\n"
        "dv_vox = round(( 332 − DV_mm·1000) / 50)        DV_mm = ( 332 − dv_vox·50) / 1000\n"
        "ap_vox = round((5400 − AP_mm·1000) / 50)        AP_mm = (5400 − ap_vox·50) / 1000"
    )
    ax.text(0.25, 1.52, code, ha="left", va="top", fontsize=8.5, family=MONO, linespacing=1.55)
    ax.text(0.25, 0.8,
            "Scale + shift + axis flip only; no warping. The site does not register Franklin–Paxinos to CCFv3,\n"
            "so a preset that is right for surgery can sit on a different Allen label (2021 preset → GPe, id 1022).\n"
            "pSI rule [isPosteriorSi]: Allen id = 342 AND −1.6 ≤ AP ≤ −0.7 mm.   "
            "Viewer limits [viewerBounds]: AP −3.0…+1.0, ML 0…5.6, DV −7.5…+0.3 mm.",
            ha="left", va="top", fontsize=8.5, linespacing=1.4)


def main() -> None:
    apply_style()
    fig = plt.figure(figsize=(9.8, 9.3))
    # axes placed in figure fractions so that panel C has 1 data unit = 1 inch
    ax_a = fig.add_axes([0.02, 0.545, 0.46, 0.43])
    ax_b = fig.add_axes([0.56, 0.555, 0.42, 0.41])
    ax_c = fig.add_axes([0.02, 0.035, 0.96, 0.414])  # 9.6 x 3.85 in
    panel_a(ax_a)
    panel_b(ax_b)
    panel_c(ax_c)
    stamp(fig, repo="pSI-atlas", script=__file__)
    save(fig, "docs/img/brain_coordinates_schematic.png")


if __name__ == "__main__":
    main()
