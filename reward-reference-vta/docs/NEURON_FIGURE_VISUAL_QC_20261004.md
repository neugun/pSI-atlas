# NEURON Figure Visual QC — 2026-10-04

## Scope

Current main-figure set:
- Fig1 identical current reward / history effect
- Fig2 sampled consumption vs passive time
- Fig3 continuous history / deeper path
- Fig4 model room
- Fig5 temporal construction
- Fig6 cross-context generalization
- Fig7 persistence / causal dopamine

Additional reviewer-facing figure:
- Extended Data value-vs-action adjudication

The current vector-PDF build audit passes:
- 7/7 main PDFs exist;
- 7/7 are single-page;
- 7/7 contain vector graphics rather than embedded raster panels;
- all review PNGs are rendered at >=300 dpi equivalent.

## Fig1 — PASS after repair

Issue found:
- panel A table used insufficient width for the first column; "current" approached clipping/truncation.
- B/C animal-count and significance labels were dense but readable.

Repair:
- first table column widened;
- history column slightly reduced;
- table font reduced minimally without changing scientific content.

Current status:
- table headers fully readable;
- no obvious text/line collision in the current review raster.

## Fig2 — PASS after scientific and visual revision

Issue found:
- earlier panel D used only early licking / lick-rate controls and did not expose the stronger current-action adjudication.
- long action-control tick labels collided.

Repair:
- panel D now shows:
  1. base,
  2. 0–2 s action,
  3. 0–5 s early+concurrent action,
  4. whole-bout action over-control.
- panel uses conditional-permutation null ticks and P values.
- labels shortened to two-line forms.

Current status:
- panel directly addresses the reviewer-level "value vs lick count" confound;
- labels are readable without overlap.

## Fig3 — PASS after repair; remains intentionally information-dense

Issues found:
- panel B four model labels visually concatenated;
- panel E ΔR²/P annotation competed with the error bar;
- panel F null annotation sat too near the x-axis.

Repairs:
- figure width and inter-panel spacing increased;
- model labels shortened and font size reduced locally;
- panel E annotation given a white-backed inset position;
- panel F null note moved upward.

Current status:
- labels are separable;
- no critical overlap remains.
- watchlist: Fig3 is still the densest main figure and should not accumulate further annotations.

## Fig4 — PASS after repair

Issues found:
- panel C negative competitor values were written to the left of their error bars and collided with y-axis category labels.
- small-value annotations were crowded around zero.

Repair:
- positive annotations remain beyond the error-bar endpoint;
- negative numeric annotations are placed just inside the plotting field on the positive side of the zero axis while retaining their signed value.

Current status:
- category labels are clean;
- negative values remain explicit;
- panel D unique-information labels remain readable.

## Fig5 — PASS

Review findings:
- main trajectory, matched-epoch summary and U/R decomposition are visually coherent.
- legend/title area is dense but does not materially overlap.

No major source-level geometry change required in this round.

Watchlist:
- avoid adding additional statistical text to panel A.

## Fig6 — PASS after repair

Issues found:
- panel C combined a long title with a long vertical y-axis label;
- panel D used a long "frozen natural value axis" label that added unnecessary density.

Repair:
- panel C title shortened to "Orthogonal value manipulations align";
- y label shortened to "Cosine with natural value axis";
- panel D y label shortened to "Projection on natural value axis".

Current status:
- no major title/axis collision.

## Fig7 — PASS after repair

Issues found:
- panel D carried four OR rows, directional interpretation, numeric OR/P labels and the contingent-vs-noncontingent interaction in a narrow forest plot.
- bottom interaction text was close to the axis boundary.

Repair:
- x range expanded;
- right-side OR/P text moved outward;
- panel title shortened;
- directional header and interaction note separated vertically;
- bottom margin increased inside the plotting range.

Current status:
- forest plot is readable;
- borderline timing interaction remains visible but is not visually promoted.

## Extended Data — value vs action — PASS after repair

Issues found in first render:
- panel letters overlapped titles;
- panel A/B tick labels collided;
- panel D low-power note overlapped the x-axis.

Repair:
- larger figure width and panel spacing;
- panel letters moved upward/outward;
- action labels shortened;
- low-power note moved below the plotting field.

Current status:
- four-panel figure cleanly separates:
  A. temporal coupling of action/reference/DA,
  B. conditional action controls,
  C. joint reference+action coefficients,
  D. exact action-matched pair sensitivity.

## Scientific visual consistency check

Color semantics currently remain stable:
- teal: history/reference or high-state natural effect;
- blue: dopamine activation / positive neural readout;
- orange: conservative/action/value-context comparison where applicable;
- gray: baseline/control/null;
- red: inhibition/termination-promoting manipulation.

No panel should use color alone to encode statistical significance.

## Remaining watchlist

1. Figure 3 is near the acceptable information-density ceiling.
2. Figure 5 panel A should not receive additional legends or significance layers.
3. Figure 7 panel D should remain a summary forest; do not add more causal conditions without moving them to Extended Data.
4. Any future site figure replacement should be regenerated from vector PDF/SVG source and re-reviewed at both page width and mobile width.
5. Main figures should not inherit website-specific annotations; scientific figure source remains authoritative.

## Current source-level repair scripts

- scripts/make_science_rebuild_fig1_4_v2.py
- scripts/make_science_rebuild_fig3_v3.py
- scripts/make_science_rebuild_round2_v1.py
- scripts/make_science_rebuild_fig5_7_v2.py
- scripts/make_value_vs_action_figure_v1.py
- scripts/build_science_rebuild_current_v1.py

## Overall status

**PASS with minor density watchlist.**

The previously visible clipping/overlap problems in Fig1, Fig3, Fig4, Fig6, Fig7 and the new action/value Extended Data figure have been repaired at source level rather than patched in exported images.
