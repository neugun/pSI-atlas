> **SOURCE CORRECTION (2026-10-07; v126):** Earlier references below to “real action-bout DA” or genuine real-bout social-credit coding are superseded. The field DA_ActionBout_AUCperSec measures an extended post-anchor model interval (median 28.85 s), not the actual observed 2.40-s observation bout. The historical n=1371 9/9 model-comparator result is preserved solely as a documented prior estimate. See [source-level correction and current 821-event triple-readout results](VTA_TRUE_BOUT_SOURCE_CORRECTION_v126_20261007.md). The frozen Early/Middle estimates and separate JAWS causal experiment have independent statistical contracts.

# VTA Early → Middle → Post → causal authority (v113, 2026-10-07)

## Current narrative authority

The VTA story is organized as one computational sequence rather than three disconnected model fits:

1. **Early — sampling policy.** The frozen Early contract gives 5/6 animals improving, rank-biserial=.810, P=.0469. Rebuilding observation-bout DA directly from raw FP returns the same inference and the same animal ranking.
2. **Middle — action-prediction error.** Middle APE coupling scales with SRI across animals, Spearman ρ=.667, exact one-sided permutation P=.0416. Raw-FP reconstruction again preserves the inference and animal ranking.
3. **Post — source/outcome-specific social credit.** For mechanistic interpretation, the primary display uses real action-bout DA because its neural integration window is aligned to the actual outcome/action episode. On the same 1,371 events, behavior-selected Passive credit is favored over fixed 0.75 and fixed 1.0 in 9/9 animals, both P=.00390625.
4. **Causal — VTA-dependent teaching.** Contingent JAWS after successful Active outcomes reduces the per-episode Active social-credit update in 10/10 animals (P=.001953) and accumulated Active credit in 9/10 (P=.003906).

## Why real-bout DA is promoted without deleting the original result

The real-bout result is **not** promoted simply because its P value is smaller. It is promoted as the main mechanistic Post display because the integration window is matched to the actual behavior/outcome bout.

The frozen 0–6 s analysis remains visible and unchanged as the original statistical authority:
- Passive credit vs fixed 0.75: 7/9, P=.0391.
- Passive credit vs fixed 1.0: 6/9, P=.0547.
- Classical RPE-family effects are often stronger in the broader fixed post-outcome window.

Thus the two readouts have complementary roles:
- **real-bout DA:** best aligned to the behavior-linked social-credit claim;
- **fixed 0–6 s DA:** frozen original reference and a broader readout of post-action evaluation/updating.

## Important branch distinction

The neural Post result uses a **behavior-selected Passive-credit** readout.
The causal JAWS endpoint is the **Active-credit update after successful Active outcomes**.

These are different outcome branches inside the same source/outcome-specific credit-assignment mechanism. The current claim is therefore branch-level: VTA DA expresses outcome-specific credit structure, and VTA activity is required for successful-outcome teaching. It does not claim that the Passive neural coefficient and Active JAWS endpoint are the identical scalar.

## Frozen historical material that must remain

`data/DA_global_temporal_model_adjudication_v4_authority.csv` and the original temporal figure remain unchanged historical authority. The Post column in that frozen signal-zoo table is still the original fixed-window metric and must not be silently relabeled as the real-bout social-credit result.

## Rebuild / QA rule

After any VTA page rebuild, run:

`python analysis/qa_vta_current_authority_v115.py`

The build is current only if the full authority suite passes.
