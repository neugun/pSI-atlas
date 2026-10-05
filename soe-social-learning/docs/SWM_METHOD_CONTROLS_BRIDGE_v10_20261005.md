# Social World Model (SWM) — checkpoint v10
Date: 2026-10-05
Status: authority for prospective information-gain control, visible-state increment, in-distribution social dependence, SLM↔SWM bridge, and learning-stage boundary.

## Naming
- SWM = Social World Model.
- SLM = interpretable Social Learning Model.
- Retire "SLM World Model" terminology.

## Main mechanistic claim
SWM learns a prospective relational-efficacy state. Mice preferentially sample social information when that sampling is predicted to improve future Active feeding, not simply when expected information gain is high.

### Prospective ΔActive
DeltaActive(z_t) = P(Active | z_t, Observe) - P(Active | z_t, Other)
- actual Observe AUC = 0.60718; 25/27 > .5; P=1.02e-6.
- actual Observe efficacy (Active vs Unrewarded among Observe) AUC = 0.61957; 27/27 > .5; P=7.45e-9.

## 1. Prospective expected information gain — replaces realized/post-hoc IG as decision control
Held-out animals never use the actually observed future social content.
Training labels for realized update are generated with inner animal cross-fitting; the held-out EIG predictor receives current z_t only.

Results:
- ΔActive Observe AUC = 0.60718.
- prospective EIG Ridge Observe AUC = 0.48042, NS.
- prospective EIG nonlinear HGB Observe AUC = 0.49182, NS.
- ΔActive − Ridge EIG AUC = +0.12676; 24/27; P=4.80e-5.
- ΔActive − nonlinear EIG AUC = +0.11537; 23/27; P=1.33e-4.
- Observe vs non-Observe EIG difference ~0 for both predictors.

Interpretation:
Information may be available without being selected. Goal-related prospective efficacy, not generic expected information gain, is the better predictor of Observe.

Old realized/post-hoc information-gain analysis may remain descriptive but cannot support a decision-stage claim.

## 2. ΔActive exceeds simple visible-state cues
Strict LOAO logistic readouts on actual Observe events, Active vs Unrewarded.

Mean held-animal AUC:
- ΔActive alone: 0.61957.
- observer-spout distance + demonstrator feeding: 0.53504.
- visible2 + ΔActive: 0.62332.
  gain +0.08827; 26/27; P=2.24e-8.
- visible4 (observer distance, demonstrator feeding, demonstrator distance, demonstrator facing): 0.57141.
- visible4 + ΔActive: 0.62421.
  gain +0.05280; 24/27; P=2.29e-6.
- all 13 current social cues: 0.61520.
- all current social cues + ΔActive: 0.63605.
  gain +0.02085; 22/27; P=2.68e-4.
Brier and logloss also improve for all three incremental contrasts.

Interpretation:
ΔActive is not a restatement of demonstrator feeding or spatial proximity. It compresses current cues plus temporally integrated/history-dependent information relevant to efficacy.

## 3. In-distribution social dependence — replaces zero-channel gate authority

### Coherent social-trajectory replacement
For each held-out session, replace the complete 13-D social trajectory with a coherent training-animal trajectory selected from the nearest 24 donor sessions by training day and duration; 10 donor replicates are averaged.
No held-out animal is used as a donor.

Results:
- efficacy AUC: 0.61957 -> 0.56090.
  drop +0.05867; 26/27; P=1.49e-8.
- Observe action AUC: 0.77118 -> 0.75575.
  drop +0.01543; 23/27; P=2.29e-6.
- motif accuracy: 0.30950 -> 0.29729.
  drop +0.01221; 19/27; P=7.83e-4.
- outcome accuracy does not reliably decline.

### No-social SWM retrain
Same architecture family and same train/val/test folds as original SWM, retrained from scratch after removing all 13 social channels.

Results:
- efficacy AUC: 0.61957 -> 0.57150.
  drop +0.04806; 26/27; P=2.29e-6.
- action AUC: 0.71748 -> 0.70178.
  drop +0.01570; 22/27; P=9.40e-6.
- action Brier worsens +0.00259; 19/27; P=.01495.
- outcome NLL worsens +0.00801; 22/27; P=.00162.
- motif NLL: no reliable loss.
- motif accuracy: no reliable loss.

Interpretation:
Correct social content is specifically required for the relational efficacy state and contributes to Observe/outcome prediction. Broad motif dynamics are comparatively preserved without social channels.
The old zero-gate −0.063 AUC result is retired as primary evidence.

## 4. Learning-stage controls
Equal-event matching:
- learner policy–ΔActive rho late−early = +0.18355; 23/27; P=3.2e-5.
- learner Observe-vs-Other ΔActive contrast late−early = +0.00756; 20/27; P=6.26e-4.

Observe/Other-stratified matching:
- learner delta rho = +0.17358; 23/27; P=5.5e-5.
- learner delta contrast = +0.00757; 20/27; P=5.66e-4.

Thus the learner early→late effect is not explained by more late-stage events.

Boundary:
13 non-learners also increase:
- delta rho +0.21906; 12/13; P=.00305.
- delta contrast +0.00896; 11/13; P=.0107.
Learner delta is not greater than non-learner:
- rho interaction P=.696.
- contrast interaction P=.642.
Action-stratified results are the same.

Therefore do NOT claim learner-specific emergence of policy–value alignment. Treat it as an experience/training-dependent computation shared across groups; learner phenotype must be defined elsewhere by successful SOE acquisition/conversion.

## 5. SLM ↔ SWM bridge

### Observe policy comparison
Same held-animal events:
- SWM vs SLM mean AUC advantage = +0.01067.
- SWM AUC higher in 25/27 animals; P=1.54e-6 one-sided.
- Brier advantage +0.00136, NS.
- logloss advantage +0.00383, borderline/NS.

Interpretation:
SLM already captures most decision-relevant structure; SWM is modestly stronger on ranking Observe choice.

### Decode SLM coordinates from SWM latent
Decoder trained only on non-test animals; evaluation is held-animal.
Mean Spearman:
- SLM policy: 0.83252.
- SLM Q/all-reward: 0.88576.
- belief/value coordinate: 0.88476.
- actor-state-value coordinate: 0.88568.
All 27/27 positive for all targets, P=7.45e-9.

Important boundary:
Raw encoder and PCA32 encoder decode the same coordinates as well or better.
No-social SWM decoding is only slightly lower and not significantly different.
Therefore decoding alone shows representational accessibility/common task coordinates, not social-specific emergence.

### SLM-coordinate subspace scrub
A 4-D subspace fitted on training animals from SWM latent to SLM-derived coordinates is removed from held-out latents; perturbation magnitude is compared with 32 matched random subspaces.
- Observe action AUC loss under SLM-coordinate scrub = 0.01396.
- matched random loss = 0.00330.
- specific loss = +0.01065; 26/27 positive; P=5.22e-7.
- efficacy AUC is NOT specifically reduced.
- outcome NLL is NOT specifically reduced.
- motif NLL worsens 0.02531; random 0.01802; specific P=.067.
- motif accuracy loss is not specific vs random.

Interpretation:
The SLM-like latent subspace contributes selectively to Observe policy. It is not the same thing as the SWM relational efficacy dimension.
This supports:
"A data-driven SWM trained without SLM structure recovers SLM-like decision coordinates and uses that subspace for Observe policy."
Do NOT say the SLM-like subspace itself mediates ΔActive efficacy.

### Future motif dynamics beyond SLM coordinates
Held-animal next-motif prediction:
- SWM NLL = 1.83470; accuracy = 0.30950.
- SLM-coordinate readout NLL = 1.97097; accuracy = 0.24621.
- action+outcome baseline NLL = 2.03029; accuracy = 0.21962.
SWM > SLM-coordinate readout:
- NLL gain +0.13627; 27/27; P=7.45e-9.
- accuracy gain +0.06329; 27/27; P=7.45e-9.

Interpretation:
SLM and SWM are complementary:
- SLM-like coordinates account for much of decision policy.
- full SWM contains additional predictive dynamics and a distinct relational-efficacy component.

## Preferred integrated statement
A data-driven SWM trained without SLM structure recovers SLM-like decision coordinates, uses that subspace for Observe policy, and additionally learns a prospective relational-efficacy state that predicts when social sampling will improve future Active feeding.

## Retired / downgraded claims
- "SLM World Model" naming.
- zeroing social channels as primary social-dependence evidence.
- realized/post-hoc information gain as a decision-stage comparator.
- learner-specific emergence of policy–value alignment.
- claiming decoded SLM coordinates are uniquely emergent in SWM.
- claiming SLM-coordinate scrub specifically disrupts efficacy.

## Authority result paths
H:/soe_social_inference_20260928/results/prospective_expected_info_gain_v2/
H:/soe_social_inference_20260928/results/delta_active_incremental_visible_state_v1/
H:/soe_social_inference_20260928/results/policy_value_learning_controls_v2/
H:/soe_social_inference_20260928/results/social_replacement_control_v1/
H:/soe_social_inference_20260928/results/social_world_model_nosocial_v1/
H:/soe_social_inference_20260928/results/compare_slm_swm_observe_v1/
H:/soe_social_inference_20260928/results/decode_slm_coordinates_from_swm_v1/
H:/soe_social_inference_20260928/results/decode_slm_coordinates_nosocial_control_v1/
H:/soe_social_inference_20260928/results/scrub_slm_coordinate_subspace_v1/
H:/soe_social_inference_20260928/results/slm_coordinate_motif_readout_vs_swm_v1/
