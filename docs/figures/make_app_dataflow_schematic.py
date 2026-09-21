"""Schematic: what the CCFv3 Locator does with a coordinate, module by module.

Left to right: user input / URL -> clamp + convert -> fetch exactly two planes
from the public CCFv3 Zarr mirror -> draw the two canvases -> readout ->
shareable URL. Boxes carry the real file and function names from
src/lib and src/components of pSI-localization-atlas-v2.17.1-source.zip.

Numbers: array shape 228x160x264 and chunk size 64^3 come from the mirror's
.zarray metadata (also CCF_SHAPE in ccfCoordinates.ts); the example voxel is
stereotaxicToVoxel() applied to the 2021 preset; the 0.5 mm radius is
radiusVoxels = 10 in collectNearbyStructures().

Run from the repository root:  python docs/figures/make_app_dataflow_schematic.py
Requires numpy + matplotlib only.
"""
from __future__ import annotations

import pathlib
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schematic_style import C, apply_style, arrow, box, hide_axes, save, stamp  # noqa: E402

ACCENT = C["blue"]      # pSI / Allen SI
DATA = C["orange"]      # remote data
OUT = C["green"]        # outputs the user sees
FILL_IN = "#F2F2F2"
MONO = "DejaVu Sans Mono"
LINE = 0.148            # inches per 8-pt line at linespacing 1.3


def tbox(ax, xy, w, h, title, body, ec=C["black"], fc=FILL_IN, title_color=None, lw=1.1):
    """Box (inch units) with a bold title line and an 8-pt body."""
    box(ax, xy, w, h, fc=fc, ec=ec, lw=lw, radius=0.1)
    x, y = xy
    ax.text(x + w / 2, y + h - 0.16, title, ha="center", va="center", fontsize=9, weight="bold",
            color=title_color or C["black"], zorder=4)
    ax.text(x + 0.12, y + h - 0.34, body, ha="left", va="top", fontsize=8, linespacing=1.3, zorder=4)


def main() -> None:
    apply_style()
    fig = plt.figure(figsize=(9.8, 6.4))
    W, H = 9.8, 5.7
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.89])  # 9.8 x 5.7 in -> 1 unit = 1 inch
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    hide_axes(ax)
    ax.set_title("CCFv3 Locator data flow (schematic; file and function names are real)",
                 loc="left", fontsize=12, weight="bold", pad=8)

    # --- column 1: inputs ------------------------------------------------------
    tbox(ax, (0.1, 3.6), 2.0, 2.1, "Input  [Locator.tsx]",
         "• type AP, ML, DV in mm\n"
         "  (− / + steps of 0.05)\n"
         "• hemisphere Left / Right\n"
         "• AP slider −1.6 … −0.7\n"
         "• presets 2021 / 2024\n"
         "  [presets, coordinates.ts]\n"
         "• click in a canvas\n"
         "  [pickCoronal, pickSagittal]")
    tbox(ax, (0.1, 2.3), 2.0, 1.0, "URL  [parseAtlasState]",
         "?ap=-0.90&ml=2.30\n&dv=-4.50&side=right\n(missing → 2021 preset)")
    arrow(ax, (0.7, 3.3), (0.7, 3.6), style="<|-|>")
    ax.text(0.8, 3.45, "same state", fontsize=8, color="#555555", va="center")

    # --- column 2: clamp + convert, centre-on-SI -------------------------------
    tbox(ax, (2.4, 3.6), 2.0, 2.1, "Clamp + convert",
         "[clampCoordinate,\n coordinates.ts]\n"
         "AP −3.0…+1.0, ML 0…5.6,\n"
         "DV −7.5…+0.3 mm\n"
         "[stereotaxicToVoxel,\n ccfCoordinates.ts]\n"
         "AP −0.90 ML 2.30 DV −4.50\n"
         "→ voxel ML 161 DV 97 AP 126")
    arrow(ax, (2.1, 4.65), (2.4, 4.65))
    tbox(ax, (2.4, 2.3), 2.0, 1.0, "Center on Allen SI",
         "[findStructureCentroid,\n ccfSelection.ts]\n"
         "centroid of id 342 in this\ncoronal plane → new ML, DV",
         ec=ACCENT, fc="#DCEBF6", title_color=ACCENT)
    arrow(ax, (3.4, 3.3), (3.4, 3.6), color=ACCENT)
    ax.text(3.5, 3.45, "re-enter", fontsize=8, color=ACCENT, va="center")

    # --- column 3: remote data + plane fetch ----------------------------------
    tbox(ax, (4.7, 4.45), 2.3, 1.25, "Public CCFv3 Zarr mirror",
         "thewtex.github.io/\n  allen-ccf-itk-vtk-zarr\n"
         "template + annotation, uint16\n"
         "(ML, DV, AP) = 228×160×264\n"
         "chunks 64³ · label_to_allen_id",
         ec=DATA, fc="#FBEFD9", title_color=C["vermilion"])
    tbox(ax, (4.7, 2.95), 2.3, 1.25, "Fetch 2 planes  [ccfData.ts]",
         "loadCoronalSlice(ap=126)\n"
         "loadSagittalSlice(ml=161)\n"
         "template + annotation each;\n"
         "remapAnnotationLabels;\n"
         "cache per (orientation, index)")
    arrow(ax, (5.85, 4.45), (5.85, 4.2), color=DATA)
    arrow(ax, (4.4, 4.0), (4.7, 3.7))
    arrow(ax, (4.7, 3.05), (4.4, 2.9), color=ACCENT)

    # small volume glyph: top view (AP x ML) with the two selected planes
    gx, gy, gw, gh = 4.75, 2.1, 0.95, 0.6
    ax.add_patch(Rectangle((gx, gy), gw, gh, fc="#FFFFFF", ec=DATA, lw=1.0, zorder=3))
    for i in range(1, 5):
        ax.plot([gx + gw * i / 5] * 2, [gy, gy + gh], color="#E8D2A8", lw=0.6, zorder=3)
    for j in range(1, 4):
        ax.plot([gx, gx + gw], [gy + gh * j / 4] * 2, color="#E8D2A8", lw=0.6, zorder=3)
    ax.plot([gx + gw * 126 / 264] * 2, [gy, gy + gh], color=ACCENT, lw=2.2, zorder=4)
    ax.plot([gx, gx + gw], [gy + gh * 161 / 228] * 2, color=C["purple"], lw=2.2, zorder=4)
    ax.text(gx + gw / 2, gy - 0.05, "AP →  (ML ↑)", fontsize=8, ha="center", va="top", color="#555555")
    ax.text(gx + gw + 0.1, gy + gh - 0.02, "coronal [null, null, ap]", fontsize=8, color=ACCENT, va="top")
    ax.text(gx + gw + 0.1, gy + 0.28, "sagittal [ml, null, null]", fontsize=8, color=C["purple"], va="top")
    ax.text(4.7, 1.9, "only the 64³ chunks cut by\nthese two planes are fetched",
            fontsize=8, ha="left", va="top", color="#555555", style="italic", linespacing=1.3)

    # --- column 4: draw + readout ---------------------------------------------
    tbox(ax, (7.3, 4.3), 2.2, 1.4, "Draw  [CcfCanvas.tsx]",
         "renderCcfPixels: Histology /\nAnnotation / Overlay\n"
         "pSI mask [pixelIsPosteriorSi]:\n"
         "id 342 AND AP in −1.6…−0.7\n"
         "→ 2-px cyan contour + fill\n"
         "crosshair at the voxel")
    tbox(ax, (7.3, 2.45), 2.2, 1.6, "Readout  [structures.ts]",
         "lookupStructure → acronym,\nname, Allen ID\n"
         "resolveDisplayStructure →\npSI / SI outside / other\n"
         "getStructureHierarchy\n"
         "collectNearbyStructures:\n10 vox = 0.5 mm, ≤ 6 hits")
    arrow(ax, (7.0, 3.9), (7.3, 4.7))
    arrow(ax, (7.0, 3.4), (7.3, 3.25))

    # --- outputs (bottom row) -------------------------------------------------
    tbox(ax, (2.4, 0.15), 2.0, 1.4, "Output: share link",
         "[buildShareUrl,\n coordinates.ts]\n"
         "Copy view URL →\n"
         "?ap=-0.90&ml=2.30\n&dv=-4.50&side=right",
         ec=OUT, fc="#DDF2EA", title_color=OUT)
    tbox(ax, (4.7, 0.15), 2.3, 1.4, "Output: readout panel",
         "exact Allen structure (2021\npreset → GPe, Allen ID 1022)\n"
         "crosshair mm + voxel\n"
         "posterior SI interpretation\n"
         "hierarchy · nearby ≤ 0.5 mm",
         ec=OUT, fc="#DDF2EA", title_color=OUT)
    tbox(ax, (7.3, 0.15), 2.2, 1.4, "Output: two canvases",
         "Coronal (ML × DV) at AP −0.90\n"
         "Sagittal (AP × DV) at ML 2.30\n"
         "cyan = posterior Allen SI\n"
         "white = crosshair",
         ec=OUT, fc="#DDF2EA", title_color=OUT)
    # state -> share link
    arrow(ax, (0.7, 2.3), (0.7, 0.85), color=OUT, style="-")
    arrow(ax, (0.7, 0.85), (2.4, 0.85), color=OUT)
    ax.text(0.8, 1.55, "state", fontsize=8, color=OUT, va="center")
    # readout -> readout panel
    arrow(ax, (7.5, 2.45), (6.9, 1.55), color=OUT, connectionstyle="arc3,rad=0.1")
    # draw -> canvases, routed along the right margin
    arrow(ax, (9.5, 4.9), (9.5, 0.9), color=OUT, connectionstyle="arc3,rad=-0.13")
    ax.text(9.62, 2.9, "pixels", fontsize=8, color=OUT, va="center", rotation=90)

    stamp(fig, repo="pSI-atlas", script=__file__)
    save(fig, "docs/img/app_dataflow_schematic.png")


if __name__ == "__main__":
    main()
