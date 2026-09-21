"""Schematic: the six tabs of the pSI Localization Atlas and what each draws on.

Tab labels are the `navigation` array in src/App.tsx (lines 13-18), in nav
order; the component per tab is the one rendered in App.tsx (lines 36-41);
asset counts are the `import` statements of each component and of the data
module it uses (src/data/*.ts) in pSI-localization-atlas-v2.17.1-source.zip.

Run from the repository root:  python docs/figures/make_site_map_schematic.py
Requires numpy + matplotlib only.
"""
from __future__ import annotations

import pathlib
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schematic_style import C, apply_style, box, hide_axes, save, stamp  # noqa: E402

INTERACTIVE = C["blue"]
REMOTE = C["orange"]
BUNDLED = C["grey"]
TABLES = C["green"]
MONO = "DejaVu Sans Mono"

# (nav label, component, body text (<= 42 chars per line), badges, interactive?)
TABS = [
    ("CCFv3 Locator", "Locator.tsx + CcfCanvas.tsx",
     "Type or preset a bregma coordinate; see the\n"
     "coronal + sagittal CCFv3 slices with the pSI\n"
     "contour; read structure, hierarchy and\n"
     "neighbours; copy a share URL. Below it:\n"
     "'Representative pSI sections' (3 images).",
     [("remote CCFv3 (live)", REMOTE), ("allenStructures.json", TABLES), ("3 webp", BUNDLED)], True),
    ("Locating pSI", "IdentificationGuide.tsx",
     "Eight-step microscope guide: AP bracket,\n"
     "caudal GP + internal capsule, optic tract,\n"
     "MeA / CeA / CeM / LH, molecular context,\n"
     "tracing, footprint. Landmark stack, four\n"
     "criteria, links to HCN1 and AmgC/M–PAG.",
     [("text only, no data files", BUNDLED)], False),
    ("Anatomy & circuits", "ExperimentalImages.tsx",
     "01 Localization and targeting: PAG-\n"
     "retrograde coronal series AP −0.70 … −1.40\n"
     "(8 PNG + PDF). 02 Input anatomy: VMHvl\n"
     "terminals, human SI atlas, SI volume video.\n"
     "03 Circuit maps. Cards enlarge on click.",
     [("8 png + pdf + mp4 + 10 webp", BUNDLED), ("experimentalImages.ts", TABLES)], False),
    ("Gene expression & spatial profile", "GeneExpression.tsx",
     "Method summary; spatial map and cell-type\n"
     "composition of pSI vs CEAl, CEAm, GPe, GPi,\n"
     "MEA and anterior SI; differential expression\n"
     "at MERFISH-panel and scRNA-seq level.\n"
     "Precomputed; the page runs no analysis.",
     [("10 png", BUNDLED), ("geneExpression.ts", TABLES)], False),
    ("Neural firing (Neuropixels)", "NeuralActivity.tsx",
     "2021 tetrode context; where IBL Brain-Wide\n"
     "Map units sit; event-aligned pSI firing;\n"
     "pSI vs each neighbour; significance and\n"
     "response subtypes; single-unit validation;\n"
     "response manifold. Precomputed figures.",
     [("12 png", BUNDLED), ("neuralActivity.ts", TABLES)], False),
    ("References & other species", "Resources.tsx",
     "Franklin–Paxinos coordinates used in the\n"
     "papers, targeting schematic and histology;\n"
     "Blue Brain Cell Atlas SI statistics; CCFv3\n"
     "and other-species atlas links; the four\n"
     "primary papers.",
     [("4 webp", BUNDLED), ("external links", TABLES)], False),
]


def badge(ax, x, y, text, color, fs=8):
    """Rounded monospace badge; returns its width in inches."""
    w = 0.6 * fs / 72 * len(text) + 0.16
    ax.add_patch(FancyBboxPatch((x, y), w, 0.22, boxstyle="round,pad=0,rounding_size=0.08",
                                fc="#FFFFFF", ec=color, lw=1.0, zorder=4))
    ax.text(x + w / 2, y + 0.11, text, ha="center", va="center", fontsize=fs, color=color, zorder=5, family=MONO)
    return w


def badge_row(ax, x0, y0, width, items):
    """Lay badges left to right, wrapping upward into a second row if needed."""
    x, y = x0, y0
    for text, color in items:
        w = 0.6 * 8 / 72 * len(text) + 0.16
        if x + w > x0 + width and x > x0:
            x, y = x0, y + 0.28
        x += badge(ax, x, y, text, color) + 0.1


def main() -> None:
    apply_style()
    fig = plt.figure(figsize=(9.8, 7.0))
    W, H = 9.8, 6.3
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.9])  # 9.8 x 6.3 in -> 1 unit = 1 inch
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    hide_axes(ax)
    ax.set_title("Site map: the six tabs, what each shows, and the data behind it (schematic)",
                 loc="left", fontsize=12, weight="bold", pad=8)

    ax.text(0.1, 6.15, "Top navigation, left → right (nav labels from src/App.tsx:13-18). "
                       "Blue = interactive, state kept in the URL; grey = static content built into the site.",
            fontsize=8.5, va="center", color="#333333")

    tw, th = 3.1, 2.45
    xs = [0.1, 3.35, 6.6]
    ys = [3.45, 0.8]
    for i, (label, component, body, badges, interactive) in enumerate(TABS):
        x = xs[i % 3]
        y = ys[i // 3]
        ec = INTERACTIVE if interactive else C["black"]
        fc = "#DCEBF6" if interactive else "#F7F7F7"
        box(ax, (x, y), tw, th, fc=fc, ec=ec, lw=1.6 if interactive else 1.0, radius=0.12)
        ax.text(x + 0.12, y + th - 0.13, f"{i + 1}", fontsize=9.5, weight="bold", ha="left", va="top",
                color="#777777", zorder=4)
        ax.text(x + 0.35, y + th - 0.13, label, fontsize=9.5, weight="bold", ha="left", va="top",
                color=INTERACTIVE if interactive else C["black"], zorder=4)
        ax.text(x + 0.12, y + th - 0.40, f"[{component}]", fontsize=8, ha="left", va="top",
                family=MONO, color="#444444", zorder=4)
        ax.text(x + 0.12, y + th - 0.66, body, fontsize=8, ha="left", va="top", linespacing=1.3, zorder=4)
        ax.text(x + 0.12, y + 0.74, "interactive · opens by default · state in URL" if interactive
                else "static · bundled at build time",
                fontsize=8, ha="left", va="bottom", style="italic",
                color=INTERACTIVE if interactive else "#555555", zorder=4)
        badge_row(ax, x + 0.12, y + 0.12, tw - 0.24, badges)

    # legend
    ax.text(0.1, 0.5, "Badges:", fontsize=8.5, weight="bold", va="center")
    lx = 0.75
    for text, color in [("remote CCFv3 (live)", REMOTE), ("bundled figures in assets/", BUNDLED),
                        ("curated tables in src/data/*.ts", TABLES)]:
        lx += badge(ax, lx, 0.39, text, color) + 0.15
    ax.text(0.1, 0.15, "Only the CCFv3 Locator talks to a server (the public 50 µm CCFv3 Zarr mirror). "
                       "The gene-expression and neural-firing\npipelines behind tabs 4 and 5 are not in this repository.",
            fontsize=8, va="center", color="#333333", linespacing=1.3)

    stamp(fig, repo="pSI-atlas", script=__file__)
    save(fig, "docs/img/site_map_schematic.png")


if __name__ == "__main__":
    main()
