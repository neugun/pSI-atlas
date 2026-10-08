# SOE/SLM: prior positive findings and latest-model reconciliation (2026-10-08, v179)

## Biological target
Demonstrator feeding content → information-sampling Observe → self-state-dominated native Feed → Active/Passive/Unrewarded evaluation → multiscale learning-state update → future social sampling. Model scores alone do not establish neural teaching or causality.

## 27 held-animal behavioral SLM comparison, 68,624 Observe decisions
SLM full Brier .170824, AUC .823320; Feature-Q .170891, Actor-Critic .171063; Current nonlinear .185812. Stronger prediction-only benchmarks include Current+Choice-kernel .166401, SLM+Choice-kernel .165411, History MLP+formal-all .163722. Thus SLM is a useful mechanistic model, NOT a top-1 all-purpose decoder.
Previous generator recovery: 35/36 six-family tests; 59/60 conditional tests. This is algorithm recovery under synthetic schedules, not proof that the real mouse uniquely executes one model or that continuous parameters are identifiable.

## Social observation content predicts ACTUAL future Feed
The recovered source script builds a strict 1-second future Feed-onset target, excluding simultaneous ongoing observation/feeding, and backward-asof-attaches only past real Observe events; the content features are demonstrator feeding and observer near-spout AT that prior Observe, without injecting the later event outcome.
27 formal learner animals, animal-held-out OOF: adding mere observation recency to current self/social state improves only 11/27, Brier gain -0.000028, two-sided P=.4846. Adding preceding observed content after recency improves 21/27, Brier gain +0.000627, two-sided Wilcoxon P=.02454. The original directional one-sided report P=.0123 is consistent, not contradicted. Content vs self/social state: 21/27, gain +0.000599, P=.04356.
Adding old SLM policy/APE/belief/Q variables beyond actual observed content improves only 13/27, incremental Brier gain -0.0000085, P=.8223. This diagnoses an unsuccessful extra latent-to-Feed interface, not a negative result about demonstrator-feeding content.
Separate previously published actual-behavior evidence: within 3 s of observing demonstrator feeding, real Feed hazard increased +7.54 percentage points (17/26, original P=.0377); after self/current-social residualization +6.09 pp (17/26, original P=.0445). These prior frame-level outputs were not rerun in this audit.

## The original Post DA positives survive their original statistical contract
Frozen Post 0–6 s: nine animals, 1,714 events. Raw newer Post FP event counts match OLD per-animal numbers exactly for ANM 1,3,4,5,6,18,19,27,35. Equal counts do not yet prove row-level event IDs match.
Original v67 uses each animal's relative MSE reduction, 100*(base-model)/base, and one-sided exact signed-rank Wilcoxon; independent audit also reports a distinct two-sided sign-flip of absolute MSE changes.
| Latent | Improving animals | Old average relative MSE gain | Original one-sided P | Independent two-sided P |
|---|---:|---:|---:|---:|
| Belief surprise | 8/9 | +5.78% | .005859 | .0078125 |
| Actor-Critic RPE | 7/9 | +5.79% | .019531 | .019531 |
| Q-all RPE | 7/9 | +5.80% | .019531 | .019531 |
| Actor RPE + belief | 8/9 | +6.16% | .009766 | .015625 |
| Q-all RPE + belief | 8/9 | +6.19% | .009766 | .015625 |
These are valid original model-vs-its-baseline positives. They do NOT establish that a unique RPE/credit latent beats a later best outcome-history, motion/time or context baseline.

## New tests are different questions, not retrospective deletion
Early SLM policy effect original directional P=.046875, two-sided P=.09375; Middle APE-SRI rho=.667, original directional P=.04157; Post old neural baseline gain P=.01953. The axes have distinct timing and inferential tests.
Later outcome-based FP model: prior observation×Active/Passive improves 7/9, P=.03125, but discovery BH q≈.0703 and animal influence make it exploratory.
True real social Obs bout vs fixed Post0–6s on identical 695 events: Active minus Unrewarded becomes more separated after the outcome, 9/9 P=.003906; Passive minus Unrewarded 8/9 P=.0078125. This supports distinct observation acquisition vs result-evaluation DA epochs, not proof of teaching. Synthetic 28.85 s ActionBout is not the real 2.40 s median observation bout.
The recent next-Observe prediction test uses a different target (future all-choice prediction) and rejects outcome-window contamination; no independent residual DA prediction under the strong behavior baseline (5/9 P=.5703). Its non-significance cannot cancel old outcome-related positive neural fits.

## Generativity and causal limitations
Codex-trained SLM produced Observe and native Feed in 27 held-out learners/54 sessions, but physical state and dyad context remained recorded replay. In 3s, generated Feed response at generated Observe opportunities +.04275 vs REAL Feed at those same generated opportunities +.000447; direct paired P=.1074. Cannot yet claim autonomous biological SOE reproduction.
VTA JAWS evidence is an independent causal branch; OXT original 7 contingent OFF→ON SRI 7/7 decrease P=.015625, direct noncontingent interaction P=.25. SF15 Aug-Sep 2026 records are different animals and pseudo-day parity groups without independently verified hardware ON/OFF; do not pool. NAc/DMS need true recording-site, learner-status and FP clock QC.

## Decisive remaining tests
Use exactly matched 1,714 Post event IDs and same neural baseline to compare old RPE/belief versus best later alternative. Test actual Feed onset and actual subsequent Observe decisions with independent animal folds, correct pre-event timestamps, and no next-event contamination. Connect observation content→Feed, outcome-dependent neural change and causal perturbations without equating their statistical estimands. Train two-policy SLM with generated actions fed back to physical state, and judge it on held-animal observed-content-to-native-Feed phenotypes, not a synthetic positive alone.

## Links to source documents
[Canonical behavioral model zoo](../data/SLM_behavior_model_comparison_canonical_v5.csv) · [nine-animal old Post DA](../data/VTA_post_model_per_animal_v67.csv) · [27-animal native Feed OOF](../data/SLM_native_feed_observed_content_per_animal_v1.csv) · [actual Feed conversion](SLM_NATIVE_SOCIAL_TO_FEED_CONVERSION_v1_20261004.md) · [context-dependent DA](VTA_SOURCE_OUTCOME_INTERACTION_EXPLORATORY_v148.md) · [matched real Obs vs Post DA](VTA_REAL_BOUT_TO_OUTCOME_EPOCH_AUDIT_v157.md) · [generator calibration](SLM_NATIVE_FEED_SAMPLING_FIDELITY_AUDIT_v159.md) · [OXT newer cohort](OXT_SF15_EXPANDED_STIM_PROVENANCE_v166.md) · [independent matched-animal comparison figure](../assets/SOE_SLM_legacy_positive_independent_audit_v179.png).

Source declaration: this audit reads the authorized workstation's original archived Codex files and current SOE source tables. Connected Dropbox searches for SLM/SOE/dopamine returned no matching files; it does not claim direct verification of unlocated Dropbox-native artifacts.
