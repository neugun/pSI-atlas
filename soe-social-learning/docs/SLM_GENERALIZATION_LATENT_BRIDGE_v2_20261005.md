# SLM latent → later generalization bridge v2 — 2026-10-05

## Biological question
Does the computational phenotype acquired during SOE forecast how the same animal later uses social information in another behavioral domain?

The same six Social-trained mice were later tested in novel-food/SAFN and observational-fear assays. Because n=6 is small, this analysis separates:
1. same-animal mechanistic association;
2. endpoint-family correction within each biological domain;
3. a stricter nested leave-one-mouse-out prediction test in which latent-family selection is repeated using only the five training animals.

## Food-related transfer: source-specific social credit
Primary matched coordinate: early→late change in Active-versus-other credit separation.

Novel-food acceptance (− latency to feed):
- n=6 same animals
- Spearman rho=.886
- exact two-sided P=.0333
- one-sided P=.0167
- across four food endpoints, family BH q=.0667

Other food endpoints are directionally concordant for total feeding duration and feeding fraction (rho=.600 for both) but do not independently clear correction.

Nested leave-one-mouse-out family selection:
- candidates: credit_sep_late, credit_sep_delta
- credit_sep_delta is selected in all six held-out folds
- LOOCV R²=.713 versus leave-one-out train-mean baseline
- exact outcome-permutation P(R²)=.0625
- predicted↔observed rho=.543, exact P=.10

Interpretation: source-specific social-credit maintenance is a strong same-animal correlate of later food acceptance, but the stringent nested prediction test is currently borderline rather than confirmatory.

## Observational-fear transfer: action-prediction error
Primary matched coordinate: late SOE |APE|.

Shock-locked velocity:
- n=6 same animals
- Spearman rho=.943
- exact two-sided P=.0167
- one-sided P=.00833
- across four fear endpoints, family BH q=.0333

The other fear endpoints do not show the same strength, indicating that the relation is specifically tied to shock-locked reactivity rather than a generic fear composite.

Nested leave-one-mouse-out family selection:
- candidates: ape_abs_late, ape_abs_delta
- ape_abs_late is selected in all six held-out folds
- LOOCV R²=.307
- exact outcome-permutation P(R²)=.0514
- predicted↔observed rho=.829, exact P=.0111

Interpretation: late action-prediction-error sensitivity forecasts the rank ordering of later shock reactivity, while variance-explained validation remains just above .05.

## Biological framing
The pattern argues against one scalar “social learning strength” controlling every later assay. Instead, different components of the learned SOE computation may transfer into different future behaviors:
- source-specific Active credit → food-related social transfer;
- action-prediction-error sensitivity → reaction to unexpected socially observed threat.

This is a modular generalization phenotype.

## Boundary and next decisive test
The same-animal cohort is n=6. The next decisive experiment should freeze:
- the SLM fit,
- the two latent families,
- endpoint definitions,
- and prediction direction
before later-task data are analyzed in an independent cohort.
