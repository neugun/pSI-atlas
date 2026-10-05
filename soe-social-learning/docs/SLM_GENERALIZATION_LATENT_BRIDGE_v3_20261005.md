# SLM latent → later generalization bridge v3 — 2026-10-05

## Biological question

Does the computational phenotype acquired during SOE forecast how the same mouse later uses social information in a different behavioral domain?

The same six Social-trained mice were later tested in social-related novelty-suppressed feeding (SAFN / novel-food engagement) and observational fear. The analysis now separates three levels of evidence:

1. same-animal mechanistic association;
2. strict leave-one-mouse-out prediction with feature-family selection repeated inside each training fold;
3. comparison against simple SOE behavioral readouts (late SRI, ΔSRI, late Observe→Active conversion, Δconversion).

The goal is not to construct one generic “social score.” The hypothesis is modular: distinct latent computations should forecast distinct later phenotypes.

## 1. Food-related transfer: social-credit maintenance

### Same-animal association

Primary coordinate: early→late change in Active-versus-other social-credit separation.

Novel-food initiation (− latency to feed):
- n=6 same mice
- Spearman ρ=.886
- exact two-sided P=.0333
- one-sided P=.0167
- leave-one-mouse influence: 6/6 jackknife subsets remain positive; ρ range .80–.90

Across four food endpoints:
- initiation latency: ρ=.886, P=.0333
- total feeding duration: ρ=.600, P=.2417
- feeding fraction: ρ=.600, P=.2417
- first-bout duration: ρ=.314, P=.5639
- one-sided BH across the four food endpoints: q=.0667 for the initiation effect

The biological specificity is important: the latent is most strongly related to *when the mouse commits to novel-food engagement*, not to how much it consumes after engagement begins.

### Strict nested leave-one-mouse-out prediction

SLM latent family:
- candidate coordinates: late credit separation and Δ credit separation
- feature selection repeated using only the five training mice
- Δ credit separation selected in all 6 folds
- LOOCV R²=.713
- exact permutation P(R²)=.0625
- predicted-versus-observed rank ρ=.543, P=.10

Simple SOE behavior family:
- candidates: late SRI, ΔSRI, late Observe→Active conversion, Δconversion
- feature selection repeated inside each training fold
- LOOCV R²=−3.053
- P=.8889

Direct held-out error comparison:
- SLM latent family has lower absolute prediction error in 6/6 mice
- median absolute error: 43.83 s → 12.43 s
- paired rank-biserial=1.00
- exact one-sided Wilcoxon P=.015625
- full permutation comparison of model MSE: P=.04861

Interpretation: the social-credit latent carries information about later novel-food initiation that is not captured by simple SOE behavioral learning measures.

## 2. Observational-fear transfer: action-prediction-error sensitivity

Primary coordinate: late SOE absolute action-prediction error (|APE|).

### Same-animal association

All-shock velocity:
- ρ=.943
- exact two-sided P=.0167
- one-sided P=.00833
- four-endpoint fear-family BH q=.0333

The association is not a generic fear/arousal score. Across the shock-velocity timecourse:
- first 10 shocks: ρ=.771, P=.1028
- middle 10 shocks: ρ=.943, P=.0167
- last 10 shocks: ρ=.543, P=.2972
- within-target five-timecourse-test BH q=.0417 for the middle-10 effect

Jackknife influence for middle-10 shock velocity:
- 6/6 leave-one-mouse subsets remain positive
- ρ range .90–1.00

Late-window sensitivity:
- using the last 2, 3, or 4 SOE training days gives the same rank relation for APE→middle-shock velocity: ρ=.943, exact P=.0167 in each definition

Biological interpretation: SOE action-prediction-error sensitivity forecasts a later *shock-reactivity* phenotype rather than a generic increase in social monitoring or immobility.

### Nested prediction and simple behavioral comparison

APE family:
- candidates: late |APE| and Δ|APE|
- for all-shock velocity, late |APE| is selected in all 6 folds
- nested LOOCV R²=.307, P=.0514
- predicted-versus-observed ρ=.829, exact P=.0111

Simple SOE behavior family:
- nested LOOCV R²=.548, P=.0333 for all-shock velocity

For the middle-10 shock epoch:
- behavior family: R²=.643, P=.0208; predicted↔observed ρ=.543, P=.0806
- APE family: R²=.576, P=.0361; predicted↔observed ρ=.829, P=.025

Interpretation: later fear reactivity retains both a gross behavioral-training signature and a more specific APE rank-order signature. The APE result should be framed as computational specificity, not as universally outperforming simple behavior.

## 3. The latent space is grounded in SOE learning across all 40 animals

Independent of the later assays, several SLM dimensions track within-SOE learning across the full cohort:
- Δ|RPE| → Δ Observe→Active conversion: ρ=.615, P=2.4×10⁻⁵
- late credit separation → late conversion: ρ=.558, P=.000181
- ΔQ → ΔSRI: ρ=.556, P=.000192
- Δpolicy → ΔSRI: ρ=.453, P=.00337

This establishes that the generalization analysis is operating in a latent space already grounded in the original SOE learning process rather than arbitrary post hoc variables.

## 4. Current biological synthesis

The current data favor a **modular computational phenotype**:

- social-credit maintenance → threshold/timing of later food engagement;
- action-prediction-error sensitivity → later shock-reactivity rank and its middle-epoch expression;
- simple behavioral learning measures still explain part of observational-fear variance;
- SLM credit latents add clear held-out value for novel-food prediction beyond simple SOE behavior.

This is stronger than a generic “SLM score predicts everything” story because each latent maps onto a biologically matched later phenotype.

## 5. Remaining decisive test

The same-animal cohort remains n=6. The next confirmatory experiment should freeze before the later assays:
- the SLM fit;
- the credit and APE coordinate families;
- endpoint definitions;
- prediction direction;
- and model-comparison contract.

The cleanest prospective prediction is:
1. stronger preservation of Active social credit during SOE should predict earlier novel-food engagement;
2. larger late SOE |APE| should predict stronger middle-epoch shock reactivity in later observational fear.
