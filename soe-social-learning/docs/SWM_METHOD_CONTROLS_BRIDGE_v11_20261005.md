# Social World Model (SWM) — method, controls and SLM bridge v11
Date: 2026-10-05

## Central question
SLM supplies an interpretable mechanistic state for social learning. SWM is a flexible recurrent future-prediction model trained without SLM equations. The bridge analysis asks which task coordinates are shared between the two models and which predictive state is added by SWM.

## 1. Prospective efficacy adds beyond SLM state and current social cues
Target: Active vs Unrewarded outcome among actual Observe events.

Strict leave-one-animal-out baseline uses the same held-animal events throughout:
- SLM pre-outcome state: policy probability, Active/Passive/Unrewarded belief-pre, Q-difference-pre, previous Observe persistence;
- all 13 current social cues;
- their combined model;
- the same combined model plus prospective efficacy, DeltaActive.

Mean held-animal AUC:
- SLM prestate: 0.55350
- 13 current social cues: 0.61520
- SLM prestate + current13: 0.62466
- SLM prestate + current13 + prospective efficacy: 0.63907

Primary incremental test:
- Delta AUC = +0.01441
- 21/27 animals improve
- rank-biserial = .667
- one-sided Wilcoxon P=.000843

Secondary proper scores are directionally improved:
- Brier gain +.00362; 18/27; P=.0707
- logloss gain +.00743; 18/27; P=.0674

Interpretation: prospective efficacy contains held-animal outcome-ranking information beyond both the interpretable SLM pre-event state and the complete current-social-cue readout. The strongest claim is AUC/ranking; Brier and logloss remain supporting directional results.

## 2. Prospective efficacy depends on correct social content
Coherent held-out social-trajectory replacement:
- efficacy AUC .61957 -> .56090
- drop .05867
- 26/27 lower
- P=1.49e-8

No-social SWM retraining:
- efficacy AUC .61957 -> .57150
- drop .04806
- 26/27 lower
- P=2.29e-6

Broad motif dynamics are much less affected by no-social retraining. This localizes social-content dependence to efficacy / Observe-related computations.

## 3. Decoder accessibility is a boundary, not the mechanistic result
SLM coordinates are decodable from SWM latent in held animals:
- policy Spearman .833
- Q/all-reward .886
- belief/critic .885
- actor-state-value .886

Raw encoder and PCA32 encoder decode the same coordinates as well or better. No-social SWM decoding is only slightly lower and does not differ significantly.

Therefore decoder performance alone establishes common-task coordinate accessibility. It does not establish SWM-specific emergence of SLM coordinates.

## 4. SLM-aligned subspace is functionally used for Observe policy
A four-dimensional SLM-aligned subspace is fitted on training animals, removed from held-animal SWM latents, and compared against 32 matched random subspaces.

Observe action AUC:
- SLM-subspace scrub loss .01396
- matched-random loss .00330
- specific loss +.01065
- 26/27 positive
- P vs random = 5.22e-7

Prospective efficacy AUC:
- no specific loss from SLM-subspace scrub
- specific difference = -.01064
- P vs random ~1

Interpretation: SLM-aligned coordinates contribute specifically to Observe policy. Prospective efficacy is functionally separable from that SLM-aligned policy subspace.

## 5. Full SWM contains future dynamics beyond SLM-coordinate readout
Held-animal future-motif prediction:
- full SWM NLL 1.83470; accuracy .30950
- SLM-coordinate readout NLL 1.97097; accuracy .24621
- action+outcome baseline NLL 2.03029; accuracy .21962

Full SWM beats the SLM-coordinate readout in 27/27 animals for both NLL and accuracy (P=7.45e-9).

## 6. Prospective efficacy vs generic expected information gain
Prospective DeltaActive predicts Observe / successful Observe. Cross-fitted prospective expected-information-gain predictors do not:
- DeltaActive Observe AUC .60718
- EIG Ridge .48042
- EIG nonlinear HGB .49182
- DeltaActive exceeds both in held animals.

This supports prospective action efficacy as the relevant decision variable.

## 7. Real Visual Block boundary
In real Visual Block sessions:
- SWM efficacy alone remains informative;
- adding efficacy to the two most obvious visible cues gives about +.09 AUC and is significant;
- adding efficacy to the full current-cue readout gives a smaller, non-significant increment.

The perturbation claim therefore concerns robustness beyond obvious visible cues. The stronger full-current-cue incremental claim is established in the unperturbed learner cohort by the strict held-animal test above.

## Preferred integrated statement
A data-driven SWM separates two components of social-information use. An SLM-aligned latent subspace is functionally required for Observe policy. A distinct prospective-efficacy variable predicts whether an Observe event will become effective Active feeding, adds outcome-ranking information beyond SLM pre-event state plus all current social cues, and depends on correct social content. Full SWM dynamics also retain predictive structure beyond the SLM-coordinate subspace.

## Claims to avoid
- Using decoder performance alone as evidence that SWM uniquely discovers SLM coordinates.
- Saying the SLM-coordinate subspace mediates prospective efficacy.
- Claiming the real Visual Block full-current-cue increment is significant.
- Treating Brier/logloss in the strict SLM+current13 increment as significant.
