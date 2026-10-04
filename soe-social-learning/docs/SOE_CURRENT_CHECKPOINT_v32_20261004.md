# SOE current checkpoint v32 — 2026-10-04

## Authority chain

Global integrated authority:
- provenance/SOE_CURRENT_CHECKPOINT_v31_20261004.md
- analysis/SOE_LATEST_ANALYSIS_MASTER_v23_20261004.md

New autonomous Observe -> native Feed closure:
- docs/SLM_AUTONOMOUS_OBSERVE_NATIVE_FEED_BRIDGE_v1_20261004.md
- docs/SLM_NATIVE_SOCIAL_TO_FEED_CONVERSION_v1_20261004.md
- figures/SOE_native_social_to_feed_conversion_v2.png/pdf/svg

## What changed after v31

v31 established a content-specific real-mouse bridge:
actual Observe -> observed demonstrator feeding -> short-latency native Feed hazard.

v32 asks the next mechanistic question:

Does the Artificial SLM itself choose observation moments whose social content can be translated into native feeding behavior?

This is tested before allowing Feed to alter the artificial transition world.

## Hybrid autonomous contract

The Artificial-SLM Observe schedule/outcomes are autonomous and held-animal / OOF.

The physical 1-s state grid and future Feed labels remain replayed from the real held-out animal.

The Feed conversion model is fit only on training animals using REAL previous-Observe timing/content.

On each held-out animal the same learned conversion is evaluated with:
1. previous REAL Observe timing/content;
2. previous AUTONOMOUS-SLM generated Observe timing/content.

At an autonomous generated Observe, demonstrator-feeding content is read from the physical environment state at that sampling opportunity.

No held-out Feed label is used to choose the generated Observe schedule.

Coverage:
- 105,994 common native decisions;
- 27 formal learners;
- 54 first/second sessions.

## Main autonomous-bridge result

Replacing generic generated-Observe recency with content available at the generated Observe improves future native-Feed calibration:

auto_content vs auto_recency:
- log loss: 18/27 animals improve;
- mean improvement +0.000585;
- median +0.000154;
- r_rb=.370;
- P=.0477.

- Brier: 18/27 improve;
- mean improvement +0.000115;
- median +0.000127;
- r_rb=.402;
- P=.0346.

- Feed AUC: 17/27 improve;
- mean +0.000544;
- r_rb=.249;
- P=.134.

Thus the main signal is improved conditional probability / calibration rather than a large global rank-order change.

Relative to real-observation recency alone, autonomous content also improves:
- log loss: 19/27, r_rb=.540, P=.00650;
- Brier: 19/27, r_rb=.524, P=.00810;
- Feed AUC: 16/27, r_rb=.397, P=.0366.

Do not interpret this comparison as autonomous observations being biologically better than real observations; the timing distributions and common-decision restriction differ. It shows that content sampled by the Artificial SLM remains behaviorally informative under the independently learned Feed-conversion rule.

## Direct hazard after autonomous generated observation

The previous autonomous generated Observe is labeled by whether the demonstrator was feeding at that sampling opportunity.

Within 3 s:
- no reliable native Feed hazard increase;
- feed-rate delta +0.10 percentage points;
- P=.539.

Within 10 s:
- feed-rate delta +3.13 percentage points;
- 17/25 animals positive;
- r_rb=.391;
- P=.0452.
- residual beyond the held-out recency Feed baseline is directional but not significant.

Within 30 s:
- feed-rate delta +2.44 percentage points;
- 19/25 positive;
- r_rb=.557;
- P=.00678.
- residual Feed delta +1.24 percentage points;
- 15/25 positive;
- r_rb=.385;
- P=.0479.

Within 60 s:
- feed-rate delta +2.65 percentage points;
- 18/25 positive;
- r_rb=.557;
- P=.00678.
- residual +1.60 percentage points, P=.0567.

## Biological interpretation of the Artificial SLM agent

The strongest current interpretation is no longer merely:

"the agent mimics mouse Observe trajectories."

It is:

The Artificial SLM is a generative social-information-sampling controller. Its autonomous sampling choices preferentially expose the agent to social content that a separately learned native action system can convert into feeding.

This gives the agent a biologically meaningful role in social foraging:
- it decides when information is worth sampling;
- the sampled content carries action relevance;
- reward/contingency updates reorganize future sampling;
- a separate native feeding controller converts useful social content into food-directed action.

This is stronger than trajectory imitation and weaker than a complete autonomous mouse.

## Important timing boundary

Real-mouse conversion:
- strongest acute excess Feed hazard within <=3 s after observing demonstrator feeding;
- residual current-state-controlled delta +6.09 percentage points, P=.0445.

Artificial-SLM generated sampling:
- does not recover the <=3 s peak;
- useful-content signal appears over ~10–30 s;
- at 30 s the current-state residual is +1.24 percentage points, P=.0479.

Therefore:

PASS:
- the agent samples behaviorally useful social content.

PROVISIONAL:
- exact timing of content-to-action conversion.

FAIL / do not claim:
- the current hybrid agent reproduces the mouse's acute Observe-to-Feed timing.

## Next engineering target

Full two-policy closed-loop integration should specifically optimize temporal coupling, not merely add more SLM scalar variables.

Required architecture:
1. frozen/validated SLM Observe policy;
2. generated Observe content captured online;
3. short eligibility trace tied to demonstrator-feeding content;
4. native Feed hazard dominated by observer self-state plus that eligibility;
5. sampled Feed action feeds back into the transition world / future observer state;
6. Evaluate both:
   - content relevance;
   - latency distribution from Observe(demfeed) -> Feed.

Primary success criteria:
- preserve existing Observe trajectory / local-kernel / motif fidelity;
- preserve VB/JAWS lesion logic;
- native Feed rate/calibration held out by animal;
- generated Observe(demfeed) -> Feed latency moves toward the real <=3 s peak without sacrificing global world fidelity.\n