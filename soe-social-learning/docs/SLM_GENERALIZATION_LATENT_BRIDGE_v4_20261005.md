# SLM latent → later generalization bridge v4 — 2026-10-05

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
