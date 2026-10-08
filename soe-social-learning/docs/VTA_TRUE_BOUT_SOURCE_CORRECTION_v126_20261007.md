# VTA time-window authority correction and next analysis gates — 2026-10-07 (v126)

## What was wrong
The older file `fp_da_method_common_events_v2` named `DA_ActionBout_AUCperSec` a real action-bout readout. Source field `ActionBoutStart_FP` is exactly `AnchorStart_FP` across 1,371 matched records. However, `ActionBoutEnd_FP` marks a long *post-anchor event-defined interval*, not an explicitly measured real observation bout. The historical median of **28.8507 s**, Q25=12.8169 and Q75=64.1213, and the fraction >6 s of **94.3837%** therefore apply to this long model interval, **not** genuine observation or licking episodes. Fifty-seven records have `ActionBoutDur_FP` approximately 100 seconds. Extended intervals include **550 no-observation events**.

The genuine observable `ObsBoutDur_FP` is present for **821 of the 1,371 events**, with median **2.3980 s**, Q25=1.1990, Q75=5.1957 s. Of these, **730/821** real observation bouts end **before** `AnchorStart_FP`, and 91 end later. Hence `DA_ObsBout_AUCperSec` often measures *pre-anchor sampling*, `DA_Post06_AUCperSec` measures *post-anchor 0–6 seconds*, and the old `DA_ActionBout_AUCperSec` averages an extended post-anchor interval. These are not interchangeable neural readouts or isolated execution-versus-post-execution measures.

## Exact triple-target common-event reanalysis, n=821 / nine animals
Animal-level two-sided Wilcoxon with identical event keys, behavior-derived credit hypotheses and nested leave-one-animal-out model pipeline, time residualization before common-event restriction:

| Test | Extended post-anchor interval | Genuine observation bout | Fixed post-anchor 0–6 s |
|---|---:|---:|---:|
| Selected Passive credit vs fixed 0.75 | 8/9, P=.0078125 | 4/9, P=.8203125 | 5/9, P=.1640625 |
| Selected Passive credit vs fixed 1.0 | 8/9, P=.01171875 | 3/9, P=.8203125 | 7/9, P=.07421875 |
| Selected credit vs no-credit/history baseline | 6/9, P=.5703125 | 2/9, P=.0390625 (negative direction) | 6/9, P=.42578125 |

Crucial logic: winning against two specified nonzero credit *weights* does not imply improvement over a no-credit baseline. The genuine observation bout negative Post-credit model result **does not disprove outcome-stage social credit** because this real observation bout normally occurs *before the anchor/outcome period*. No independent post-bout offset-locked DA analysis has yet established whether teaching signals continue after actual behavior termination.

The older nine-of-nine P=.00390625 is retained as **historical extended-interval vs fixed-weight comparison on 1,371 events**; it is not an independently replicated biological action-bout result. Neither this corrected audit nor a small P value licenses the original claim that genuine observed behavior itself is encoding a particular social-credit coefficient.

## What is still valid
Frozen Early sampling-policy and Middle APE results, including strict raw-photometry reconstruction, are **separate estimation contracts** and have not been invalidated by this post-readout source correction. The frozen post-anchor 0–6 s RPE analysis remains a legitimate time-defined comparison. The VTA JAWS Active credit causal contrast is a distinct experiment and does not establish identity with neural Passive-credit coefficients.

## Gated next work
1. **Behavioral event authority:** derive a per-event table explicitly containing observation onset/offset, each feeder/lick bout onset/offset, trial outcome time, stimulation state and true animal/day/condition; lock units and event provenance. Zero assumption that model `ActionBoutEnd_FP` equals actual offset.
2. **Separate temporal hypotheses:** pre-observation baseline, genuine observation AUC/s, event/post-outcome 0–2/2–6 s, 6 s onward, and *independent true behavior-offset-locked* DA. Apply each window only to events where it exists and keep event identities matched within a specific comparison. Check duration, overlap, next-event contamination and photometry temporal autocorrelation.
3. **Models and controls:** compare selected credit to no-credit/history as the primary incremental test, then to each fixed-credit weight. Run RPE, APE, simple reward, motion/location, event density and smooth-duration covariates, with animal-level cross-validation; split learner/non-learner and early/middle/post only using frozen training authority.
4. **OXT inhibition:** use the restored condition registry (contingent D21 normal vs D50/51 ON/OFF; noncontingent D60 normal vs D52/53), keep all-source normal→full and within-stimulation ON/OFF estimands distinct, and stratify old OXT learners 118/119/121/126 from nonlearners 122/125/129. Old MATLAB MAT with N_days=1..23 is not the intervention SRI/PRI source.
5. **NAc/DMS:** lock actual recording site and sensor per animal with histology and later Codex 2.5 learning labels; the five original NAc-legacy animals 132/133/134/141/144 are **nonlearners**, so previously presented 5/5 change is not learner-specific learning. Exclude DMS3 site conflicts until resolved; enforce FP/event source-clock synchronization before outcome-aligned DA.

### Reproducible outputs
`../assets/SOE_VTA_true_obs_interval_audit_v126.png` (also SVG/PDF); `../data/SOE_VTA_real_obs_interval_audit_v126.json`; `../data/SOE_VTA_true_obs_post_action_credit_comparisons_v126.csv`; `../data/SOE_VTA_true_obs_event_outcome_counts_v126.csv`; source script `audit_fp_da_TRIPLE_MATCHED_v4.py` retained in the workstation Codex frozen model directory.

**Public communications:** mark all original action-bout evidence panels as historical explorations, not primary real-bout encoding evidence. Preserve frozen results for transparent scientific correction.

## 2026-10-07 strict neural-to-next-choice gate (v131)

This gate tests the article's *learning affects future behavior* link; it is not the primary demonstration of Observe→Feed conversion. In the raw FP event table, next event timing overlaps **315/1706 (18.5%)** valid fixed 0–6 s DA windows and **738/1363 (54.1%)** historical extended-interval windows. Thus neither naive DA readout is inherently a pre-next-choice predictor. Source [event-overlap CSV](../data/SOE_VTA_next_choice_event_overlap_v131.csv).

With the identical nested leave-animal-out behavior baseline and only an additional current DA residual: (a) fixed post-anchor 0–6 s with next-event gap ≥6 s gives **1391 events, 5/9 improving, two-sided P=.5703125**; (b) extended interval not crossing the next event (but possibly touching its onset boundary) gives **625 events, 1/9 improving, P=.12890625**. The latter is explicitly boundary-touch exploratory, NOT a strict 0.1-s separated prospective test; only two events pass that stronger interval gap gate. Source [recomputed model contrasts](../data/SOE_VTA_next_choice_timing_QC_v131.csv). Neither result establishes independent neural teaching-to-future-choice prediction, but neither disproves circuit-level causal teaching measured separately using JAWS. Prioritize actual content→native Feed and correctly timed intervention endpoints rather than rescuing a DA significance claim.
