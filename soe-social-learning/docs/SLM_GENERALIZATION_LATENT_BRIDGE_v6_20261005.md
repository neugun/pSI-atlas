# SLM latent → later generalization bridge v5 — 2026-10-05

## Main update: cross-domain double mapping

Two SOE latent coordinates were tested against two later behavioral domains in the same six Social-trained mice.

Primary 2×2 Spearman mapping:
- credit → novel-food initiation: rho=.886
- credit → fear shock reactivity: rho=.143
- APE → novel-food initiation: rho=−.086
- APE → fear shock reactivity: rho=.943

Matched-mapping contrast:
(credit→food + APE→fear) − (credit→fear + APE→food) = 1.771.

Exact null:
- food and fear mouse identities are permuted independently;
- 720 × 720 = 518,400 exact domain permutations;
- exact P=.00672.

Definition/window sensitivity:
- 2-, 3-, and 4-day early/late windows;
- Active−mean(other), Active−Unrewarded, Active−Passive credit definitions;
- 9/9 contrasts are positive;
- 8/9 are P<.05; the remaining 4-day Active−Unrewarded definition is P=.0553.

## Biological interpretation

The result favors a modular computational phenotype rather than one scalar social-learning strength.

- Social-credit maintenance maps onto the threshold/timing of later novel-food engagement.
- Action-prediction-error sensitivity maps onto later shock-locked reactivity.
- The mismatched cross-domain links are weak.

This changes the biological statement from “some SLM latent predicts some later behavior” to “distinct learned computations map onto distinct future social-behavioral domains.”

## Relation to nested prediction

Food:
- SLM credit family lowers held-out absolute error versus the simple behavior family in 6/6 mice.
- median absolute error: 43.83→12.43 s.
- paired r_rb=1.00, P=.015625.
- full nested model-comparison permutation P=.04861.

Fear:
- late |APE|→shock velocity rho=.943, exact P=.0167.
- four-endpoint fear-family BH q=.0333.
- strongest in the middle 10 shocks; within-timecourse q=.0417.
- nested APE predicted↔observed rho=.829, exact P=.0111.
- simple SOE behavior still explains some fear variance.

## Guardrail

The same-animal cohort remains n=6. The double mapping is strong mechanistic evidence, not a substitute for prospective replication. The next confirmatory cohort should freeze both latent families and both later endpoints before analysis.


## Additional specificity checks

The modular mapping is not explained by redundant latent axes or correlated later outcomes:
- credit vs APE: rho=.257, exact two-sided P=.658;
- food vs fear phenotypes: rho=−.143, exact two-sided P=.803.

Matched links remain strong after controlling the other latent in rank space:
- credit→food | APE: partial rho=.943, exact P=.02778;
- APE→fear | credit: partial rho=.947, exact P=.01111.

Thus the diagonal 2×2 mapping is not a trivial consequence of collinear SLM latents or correlated later phenotypes.

## Selection-aware simple-behavior challenge

A stricter post hoc audit asked whether the 2×2 latent double mapping is itself unique to SLM coordinates. The comparator family contained four simple SOE behavioral phenotypes: late SRI, ΔSRI, late Observe→Active conversion, and Δconversion. All 16 ordered behavior-feature pairs were evaluated under the same independent food × fear identity permutations, and the null selected the best behavior pair on every permutation.

Results:
- fixed latent mapping (Δcredit→food, late |APE|→fear): double-mapping score = 1.771; exact P=.00672;
- best simple-behavior pair in the observed data: late SRI→food plus late conversion→fear; score = 2.000;
- after correcting for selection over the 16 behavior pairs, the behavior-family mapping is not significant (P=.1123);
- the latent mapping does not exceed the selection-optimized behavior family (latent−best behavior = −.229; selection-corrected exact P=.1846).

This audit changes the allowed claim. The significant latent double mapping supports a modular computational phenotype, but it is **not evidence that SLM latents uniquely contain all cross-domain predictive information**. The strongest behavior-independent result remains the nested Δcredit→novel-food prediction (6/6 held-out mice lower absolute error; model-comparison P=.0486). The late |APE|→fear relationship should be described as a strong domain-matched mechanistic association, not as demonstrated superiority over simple behavioral phenotypes.

## Preferred wording

Distinct SOE computations map onto distinct later behavioral domains. Social-credit maintenance provides incremental prediction of later novel-food initiation beyond simple SOE behavior, whereas late action-prediction-error sensitivity is strongly associated with later shock-locked reactivity but does not yet show behavior-independent predictive superiority. The 2×2 double mapping is robust to latent collinearity and definition/window choices, but prospective replication in a larger cohort is required.

