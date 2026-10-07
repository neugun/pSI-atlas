# Figure 5: Bout survival and held-mouse sensitivity (2026-10-07)

**Goal.** Audit the emergence of relative-value DA during consumption without silently replacing the original Fig. 5 estimand.

## Source and population

The existing local `authority11_transition_local_features.csv` contains **402 bouts from 11 animals**. Of these, 387 are post-initial-block; 192 satisfy both post-initial-block and duration >=5 seconds. Across all bouts, 203 last <5 seconds and 109 last <2 seconds. A nonmissing 2–5 s DA field on a shorter bout does not imply continuous feeding throughout that window.

Among post-initial-block bouts, quality=0 has 65/197 (33.0%) surviving 5 seconds, while quality=1 has 127/190 (66.8%). Per-mouse retained counts range from 4 to 32.

## Methods and estimand

The prespecified proxy `C_lick_a0.1` is used in this new analysis; this **does not re-estimate the original +1.458 temporal interaction**. Outcome is 2–5 s DA minus 0–2 s DA, with the component windows also fitted separately. OLS includes reward quality, session fraction, time within block, log prior licks, log prior licks in current block, and animal fixed effects; SEs are clustered by animal. Additional log bout duration is a sensitivity analysis, not a causal adjustment. Thresholds of 7/10/15/20 seconds are exploratory.

For out-of-sample tests, an entire mouse is held out; ridge hyperparameters are selected solely by inner leave-mouse-out validation among the training mice, comparing identical covariates with versus without the contrast proxy.

## Main results

| Threshold / model | n bouts (11 mice) | β history, 2–5 s minus 0–2 s | Mouse-clustered P |
|---|---:|---:|---:|
| >=5 seconds | 192 | +1.305 | 0.00536 |
| >=7 seconds | 154 | +1.664 | 0.000084 |
| >=10 seconds | 116 | +1.563 | 0.000920 |
| >=20 seconds | 69 | +0.258 | 0.665 |
| >=5 seconds, additional duration covariate | 192 | +1.148 | 0.0327 |
| >=20 seconds, additional duration covariate | 69 | −0.304 | 0.609 |

The adjusted odds of reaching 5 seconds are greater at higher current reward quality (OR=3.80, clustered P=0.042); the contrast proxy itself is not significant in this selection model (P=0.601), which **does not prove absence of selection bias**.

**Held-mouse prediction of sustained-minus-early DA**, incremental contrast signal:

| Threshold | Relative MSE improvement | Mouse wins | One-sided paired mouse Wilcoxon |
|---|---:|---:|---:|
| >=5 s | +2.50% | 7/11 | P=0.207 |
| >=5 s, duration adjusted | +2.48% | 8/11 | P=0.139 |
| >=7 s | +2.07% | 7/11 | P=0.183 |
| >=10 s | +6.86% | 9/11 | P=0.0122 |
| >=10 s, duration adjusted | +1.04% | 5/11 | P=0.382 |

The >=10 s unadjusted P value is an **exploratory, threshold-selected finding** and does not survive the interpretive sensitivity to duration adjustment; it must not be promoted as confirmatory.

## Interpretation

Within bouts long enough to observe a true 2–5 s feeding window, a contrast proxy positively tracks sustained-minus-early DA under several survival thresholds. However, current reward strongly determines who enters this sample, and **the out-of-animal predictive increment at the primary 5-second threshold is not significant by paired animal-level testing**. These audit results supplement rather than replace the original Fig. 5 interactions. Available covariates do not fully substitute for frame-level DA, moment-to-moment licking, and motion artifact controls.

Next: recover the raw event-aligned signal, distinguish valid feeding frames from post-termination windows, inspect local action trajectories, and test survival weighting/shared time windows in a held-animal framework.

## Reproduction

`tools/audit_fig5_bout_survival_v1.py` and `tools/audit_fig5_nested_oof_v1.py`, producing only aggregate CSVs: `FIG5_bout_sample_accounting_v1.csv`, `FIG5_survival_selection_logit_v1.csv`, `FIG5_bout_duration_sensitivity_v1.csv`, `FIG5_nested_LOAO_contrast_gain_v1.csv`. The local bout-level input was not published.
