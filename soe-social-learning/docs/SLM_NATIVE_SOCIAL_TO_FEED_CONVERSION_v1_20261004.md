# Native social-to-feed conversion authority v1 — 2026-10-04

## Biological question

Can the Artificial-SLM framework be extended beyond Observe / No-observe so that feeding is a native future action, and what social signal actually couples observation to later feeding?

The answer is now more specific than a generic shared-controller hypothesis.

A native Feed action is robustly predictable from the observer's own pre-action state. Current social/dyadic state adds a small held-animal increment. Merely having observed recently is not sufficient. The strongest conversion signal is the content of the preceding observation: whether the demonstrator was feeding.

## 1. Native Feed action is real and reproducible

Strict future-action contract:
- 1-s decision grid;
- current observer Feeding and Social Observation are OFF immediately before the decision;
- Feed = observer Feeding onset in the next 1 s;
- Observe = Social Observation onset in the next 1 s;
- Other = neither;
- Observe+Feed conflicts excluded;
- no current event-outcome label is used to define Feed.

Pooled first + second session, both sessions held out together by animal, n=40:
- observer-only Feed AUC = 0.82531;
- observer-only macro AUC = 0.68096;
- Feed AUC exceeds prevalence in 40/40 animals;
- adding current social/dyadic state gives Feed AUC = 0.82665;
- social-state Feed AUC increment: 30/40 improve, r_rb=0.407, P=0.0120;
- Feed-specific social log predictive gain: 28/40 positive, mean +0.01728 nats / Feed decision, r_rb=0.471, P=0.00431.

Boundary: only 20/38 animals show positive Feed social gain in both individual sessions. The pooled held-animal signal is real, but the generic current-social increment is not sufficiently individually stable to be the mechanism headline.

## 2. Directly carrying old SLM scalar state into Feed is not sufficient

A conservative controller carried forward the most recent strictly previous event-PRE SLM state onto the native action grid.

Coverage:
- 160,108 / 163,758 grid decisions;
- 40 animals, 80 sessions;
- median SLM-state age 23.5 s; 95th percentile 308.2 s.

Adding Active/Passive/Unrewarded belief and Q difference beyond current state + simple previous-event history did not reliably improve native Feed:
- Feed AUC gain: 21/40 positive, r_rb=0.0024, P=0.497;
- Feed-specific log predictive gain: 16/40 positive, P=0.602.

Among 27 learners, short-latency SLM state gives a small overall action log-probability gain within ~10–30 s, but not a significant Feed-specific gain.

Conclusion:
do not implement the richer agent as a single shared scalar-belief readout controlling both Observe and Feed.

## 3. Recent observation alone is not the conversion signal

A held-animal Feed-hazard ladder compared:
self state -> + current social state -> + time since the last actual Observe -> + PRE-outcome SLM state at that Observe.

Learners, n=27:
- current social state vs self state: Feed AUC improves in 19/27, r_rb=0.434, P=0.0246;
- adding recent-Observe recency does not improve Feed AUC and does not reliably improve log loss;
- adding SLM scalar state after recency also does not improve Feed-specific prediction.

Thus "an Observe happened recently" is not enough.

## 4. What was observed matters

For the 27 formal learners, formal_oof_latents and the held-animal real-mouse event replay were aligned within session:
- 68,624 events;
- action identity alignment = 100%;
- outcome identity alignment = 100%;
- event-frame recovery = 100%.

This permits a strict pre-action bridge from each actual Observe event to the subsequent native Feed grid.

Adding content from the most recent Observe — demonstrator-feeding and observer-near-spout state at that observation, with recency interactions — improves held-animal Feed calibration beyond generic observation recency:
- log loss: 17/27 improve, mean gain +0.00237, r_rb=0.392, P=0.0386;
- Brier: 21/27 improve, mean gain +0.000627, r_rb=0.492, P=0.0123.

This does not improve global Feed AUC. The value is conditional conversion, not a globally better Feed classifier.

## 5. Demonstrator feeding is the content-specific signal

Ablation separates:
- demonstrator feeding at the preceding Observe;
- observer near-spout at the preceding Observe.

For Feed decisions whose preceding Observe occurred while the demonstrator was feeding:
- demfeed-only content model improves held-out log probability in 26/26 informative animals;
- mean gain +0.15998 nats / decision;
- median +0.15071;
- r_rb=1.0;
- P=1.49e-8.

For Feed decisions after an Observe without demonstrator feeding:
- demfeed content decreases the predicted probability, 27/27 animals;
- mean log-probability change -0.05044 nats.

For non-Feed decisions after observing demonstrator feeding:
- demfeed content also lowers Feed probability, 26/26 animals.

Near-spout alone does not reproduce the Feed-after-demfeed effect:
- 14/26 positive;
- r_rb=0.140;
- P=0.274.

Therefore the conditional signal is specifically tied to observed demonstrator feeding, not simply where the observer happened to be during the preceding observation.

## 6. Direct biological hazard supports a short conversion window

Using the actual future Feed onset rather than the content model, and treating animal as the unit of inference:

Within 3 s of the previous Observe:
- mean Feed hazard after observing demonstrator feeding = 0.2273 per 1-s decision;
- after observing no demonstrator feeding = 0.1519;
- mean within-animal difference = +0.0754 (7.54 percentage points);
- 17/26 animals positive;
- r_rb=0.409;
- P=0.0377.

A frozen held-out self + current-social model already predicts some moment-to-moment Feed propensity. Residualizing against that model:
- residual Feed hazard difference within 3 s = +0.0609;
- 17/26 animals positive;
- r_rb=0.385;
- P=0.0445.

At 10–60 s the raw difference remains directionally positive, but current behavioral state increasingly carries the same information. Therefore the preferred biological statement is a short-latency conversion window, not an indefinitely persistent feeding drive.

## 7. Architecture implied by the data

The richer Artificial-SLM should be hierarchical rather than forcing one latent to control every action.

Preferred architecture:

social/dyadic state
-> SLM Observe / information-sampling controller
-> observed content (especially demonstrator feeding)
-> short eligibility / conversion bridge
-> native Feed hazard on top of the observer's strong self-state feeding controller

In parallel:
Observe outcome
-> contingency-specific belief / Q update
-> future sampling policy and longer-timescale social-learning organization.

This preserves the established role of SLM in sampling and social reward-credit while allowing Feed to have its own dominant self-state controller plus a transient social-content input.

## 8. Relation to Visual Block and JAWS

This architecture strengthens the existing perturbation logic.

Visual Block:
- does not simply abolish Observe;
- disrupts access to useful social content and Observe-to-Active conversion;
- artificial sensory masking leaves gross observation approximately intact while reducing Active contingency and Active social value.

JAWS:
- selectively weakens Active-belief teaching / reward-credit organization;
- does not behave like a visual-information lesion;
- therefore need not directly suppress the native motor act of feeding.

The two perturbations act at distinct positions in a larger social-information-to-action chain.

## Promotion status

PASS:
- native future Feed action is feasible and replicated across two sessions;
- current social state has a small held-animal increment for Feed;
- recent Observe alone is not sufficient;
- preceding observed demonstrator feeding is a highly specific predictor of subsequent Feed;
- an acute <=3 s actual Feed-hazard increase survives a held-out current-state residual control.

PROVISIONAL:
- exact parameterization of the short eligibility kernel;
- whether the conversion bridge should use raw demonstrator-feeding state or a learned content encoder;
- autonomous rollout with native Feed feeding back into subsequent state.

FAIL / do not claim:
- one old SLM scalar belief directly controls native Feed;
- global Feed AUC is improved by observed-content features;
- the association proves demonstrator feeding causally triggers observer feeding;
- the current extension already reconstructs canonical SRI in a fully autonomous mouse.

## Immediate next build

Implement a two-policy Artificial-SLM:
1. preserve the current SLM Observe policy and belief/Q updates;
2. add a native Feed hazard dominated by observer self-state;
3. add a short-latency demonstrator-feeding content eligibility term;
4. let generated Observe content feed that eligibility term;
5. run held-animal autonomous rollouts and test:
   - Observe trajectory fidelity;
   - native Feed timing;
   - Observe->Feed conversion;
   - Visual Block analogue;
   - JAWS analogue;
   - whether a non-circular virtual SOE phenotype emerges.
