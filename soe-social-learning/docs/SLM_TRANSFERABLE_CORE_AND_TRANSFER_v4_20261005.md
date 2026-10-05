# Transferable SLM computations and cross-task model transfer â€” authority update 2026-10-05

## Executive decision

The cross-species story should not be framed as â€œSLM wins in many datasets.â€ The defensible claim is narrower and stronger: **four computations recur across tasks, but the evidence tier differs by dataset.** Direct held-out model comparison, component transfer, neural convergence, and literature-only support must remain separated.

The current four computations are:

1. **Source-tagged credit** â€” distinguish self, social-other, and non-social sources when assigning outcome credit.
2. **State-gated information value** â€” social information changes value as a function of the observerâ€™s own state, role, geometry, or uncertainty.
3. **Task-matched multiscale state** â€” useful history is neither memoryless nor a single universal exponential trace; relevant fast, minute-scale, and longer priors coexist.
4. **Sampling-to-action separation** â€” information sampling and consummatory/action execution are distinct control problems linked by sampled content.

VTA/DA is best treated as an **implementation layer** for policy, APE, RPE, and credit update, not as a fifth transferable computation.

## Comparator audit

### Human

The previous â€œcurrent state vs multiscale historyâ€ comparison was too weak to support a model-selection claim by itself. Under the same held-subject OOF contract, multiscale history was re-compared with the best matched Feature-Q model.

- 10 held-out subjects.
- Multiscale history improves Brier in **8/10** subjects.
- paired rank-biserial **r_rb = .891**.
- exact one-sided **P = .00488**.
- Relative to the Feature-Q -> RNN ceiling gap, the structured state recovers about **90.2%** of the gain.

This is currently the cleanest external behavioral case that a structured SLM-style state clears a stronger matched comparator.

### Macaque DANDI001435

A parallel comparison was run against the best matched Feature-Q model.

- 44 recording-date clusters, nested in **2 monkeys**.
- 41/44 date clusters improve.
- r_rb = .982, one-sided P = 1.88e-12 at the date-cluster level.

This is **sensitivity evidence only**. The 44 dates are not 44 independent animals. The result should not be presented as population-level primate inference.

### Rat DANDI001169

The matched classical-RL gap is now closed under the **same original same-zoo OOF contract**, with classical-family selection confirmed by nested held-rat cross-validation.

- 10 rats; 12,564 violation-filtered trials.
- The exact original 5-fold held-rat split is reused (2 test rats per fold).
- Classical family: WSLS, Q-learning, asymmetric-Q, forgetting-Q, choice-kernel (CK), and Q+CK.
- Inside each outer training set, a 4-fold **held-rat inner CV** compares all six model families by mean held-rat Brier. The best family is then refit on all outer-training rats before testing the two untouched outer rats.
- CK is selected in **5/5 outer folds** by nested CV.
- An independent training-fold BIC sensitivity analysis also selects CK in 5/5 folds and gives the same outer-test result.
- Multiscale history beats the selected classical comparator in **8/10 rats**.
- mean Brier: **0.228778 -> 0.227473** (lower is better).
- mean gain = **+0.001306**; median gain = **+0.001269**.
- paired rank-biserial **r_rb=.891**.
- exact one-sided **P=.00488**.

The effect is modest in absolute Brier but consistent across independent rats. Rat DANDI001169 can therefore be promoted from "component-only support" to a **matched classical-comparator test of task-matched multiscale state**.


### Rat multimetric robustness

The same nested-CV comparator result is robust across three held-rat metrics:

- **Brier:** 8/10 rats favor structured multiscale; mean 0.228778 -> 0.227473; r_rb=.891; exact one-sided P=.00488.
- **NLL:** 8/10 favor structured multiscale; mean 0.649615 -> 0.646780; r_rb=.891; P=.00488.
- **AUC:** 9/10 favor structured multiscale; mean 0.52995 -> 0.54498; r_rb=.927; P=.00293.

Thus the rat advantage is not confined to one probability-calibration metric. The absolute effect remains modest, but it is directionally consistent across independent rats and appears in proper-scoring and discrimination metrics.

## Primate RPE circularity correction

The Noritake/Isoda public release contains preselected positive/negative O-RPE and S-RPE population objects. Our earlier replot estimated slopes from those same preselected RPE populations. That does not remove the original selection circularity.

Therefore:

- the primate RPE replot is removed from the quantitative cross-species main figure;
- neuron-level slope P values are not used in the evidence count;
- the dataset is currently **literature / audit support** for source-tagged credit;
- promotion back to quantitative evidence requires trial-resolved data allowing split-half classification/test or another held-out source-selectivity analysis.

The public MAT files currently expose condition-averaged population arrays rather than the trial-resolved table needed for that split-half test.

## Marmoset inference correction

The marmoset dataset has **2 animals**. Cell/unit-level P values are therefore not used as population inference. The main panel now displays the effect direction separately in animals K and D.

The correct current use is architectural convergence:

- active gaze gates partner evidence;
- partner variability changes evidence accumulation;
- dmPFC activity tracks social evidence / decision variables;
- outcome history shifts policy bias.

This is a close analogue of sampling -> evidence -> decision, but it is not a full replication of the SOE Observe-policy / Feed-policy decomposition.

## Four-computation evidence map

### 1. Source-tagged credit

**SOE:** Active / Passive credit; VTA JAWS selectively disrupts Active-belief updating.

**External behavior:** rat observational maze shows demonstrator-source information that is not reproduced by a moving object; macaque source-aware state improves behavior prediction.

**External neural:** published primate self/other RPE remains literature support pending non-circular reanalysis.

### 2. State-gated information value

**SOE:** social information value changes with observer state, including distance from the observerâ€™s own spout.

**External behavior:** cooperative foraging shows follower-specific uncertainty gating and a role-by-uncertainty interaction; Aeon shows value of recent partner history.

**External neural:** marmoset partner variability changes evidence accumulation in both recorded animals.

### 3. Task-matched multiscale state

**SOE:** immediate outcome-conditioned switching, minute-scale history, and transient cross-day prior coexist.

**External behavior:** human, rat DANDI001169, and macaque structured states clear stronger matched classical/Feature-Q comparators; mouse DANDI001632 provides component-level timing support.

**External neural:** macaque ACC encoding improves when multiscale state is added.

### 4. Sampling-to-action separation

**SOE:** the direct evidence is strongest here. Recent Observe alone and the old scalar SLM state do not explain native Feed. What was sampled â€” especially demonstrator feeding â€” predicts short-latency Feed conversion.

**External analogues:** marmoset gaze gates partner evidence before decision; rat maze observed source predicts later choice.

Current status: **directly established in SOE; externally analogous, not yet fully replicated.**

## Using the SOE-trained model across tasks

A direct weight-transfer test has now been run. A recurrent core is pretrained on SOE and then fine-tuned on external tasks under held-out target-unit evaluation.

### SOE -> external fine-tuning, seed-averaged at the true held-out unit

**Macaque DANDI001435**
- 20% target training data: 6/10 sessions improve; mean NLL gain +.00275; r_rb=.345; P=.188.
- 50% target training data: 6/10 improve; mean +.00678; r_rb=.455; P=.116.
- 100% target training data: 5/10 improve; mean -.00100; no benefit.
- At 50%, both monkeys have positive mean gain, but this remains descriptive because sessions are nested within only two animals.

**Aeon**
- no robust benefit at 20%, 50%, or 100% target data after averaging the three seeds within each of five experiments.

**Cooperative foraging**
- no positive average benefit; this is one dyad and is treated as within-dyad transfer only.

Conclusion: **raw recurrent weight transfer is not broadly task-general.** The current evidence favors transfer of computational motifs/coordinates over a universal pretrained network.

### External -> SOE pretraining

The existing reverse-transfer experiment is asymmetric and concentrated in the low-data regime.

Macaque-only pretraining before SOE fine-tuning:
- 2 SOE training animals: 5/5 folds improve, mean Brier gain +.00482, P=.03125.
- 4 SOE training animals: 5/5 folds improve, mean +.01365, P=.03125.
- 8 SOE training animals: only 1/5 improves; mean gain becomes slightly negative.

Mouse DANDI001632 and Aeon show a similar pattern in some low-data settings, with the advantage disappearing when more SOE animals are available.

Interpretation: there is evidence for **sample-efficiency transfer**, not a universal asymptotic foundation model.

## Same-animal bridge to later fear / neophobia

The same six Social-trained mice later entered novel-food and observational-fear assays. The current analysis no longer asks whether one global "SLM score" predicts everything. It tests whether distinct SOE computations map onto functionally matched later domains.

Primary 2x2 mapping:
- Delta social-credit -> novel-food initiation: rho=.886.
- Delta social-credit -> fear shock reactivity: rho=.143.
- late |APE| -> novel-food initiation: rho=-.086.
- late |APE| -> fear shock reactivity: rho=.943.
- matched-minus-mismatched double mapping = 1.771; exact independent food x fear identity permutation **P=.00672**.

The strongest behavior-independent result is the food branch:
- nested leave-one-mouse-out credit family lowers held-out absolute error versus the simple-behavior family in **6/6 mice**;
- median absolute error **43.83 -> 12.43 s**;
- paired P=.0156;
- full nested model-comparison permutation **P=.0486**.

The fear branch is strong but must be stated more narrowly:
- late |APE| -> shock velocity rho=.943, exact P=.0167;
- nested predicted-observed rho=.829, exact P=.0111;
- however simple SOE behavior also explains part of fear variance.

A selection-aware challenge over all 16 ordered pairs made from late/Delta SRI and late/Delta conversion does **not** show that the latent double mapping uniquely beats the best simple-behavior pairing (latent-minus-best-behavior corrected P=.185). Thus the double mapping supports a modular computational phenotype, not unique latent sufficiency.

This cohort remains **n=6**. Prospective replication should freeze both latent definitions and both later endpoints before analysis. Detailed authority: SLM_GENERALIZATION_LATENT_BRIDGE_v6_20261005.md.

## Current model-level conclusion

The most defensible cross-task statement is:

> **SLM generalizes primarily as a compact set of computations, not yet as a universally transferable set of trained network weights.**

The strongest transferable components are source tagging, state-gated information value, and task-matched multiscale state. Sampling-to-action separation is a major SOE result with promising architectural analogues but still needs a second direct task-level demonstration.

## Frozen-core representation transfer — completed

A stricter representation-transfer test froze the recurrent core and trained only the target adapter/head. The comparator was an equally frozen random recurrent core, so any advantage comes from the SOE-learned recurrent dynamics rather than target-task fine-tuning of the core.

**Macaque DANDI001435**
- 20% target data: 6/10 held-out sessions improve; mean NLL gain +.00501; r_rb=.345; P=.188.
- 50% target data: 8/10 improve; mean +.01491; r_rb=.745; P=.0186.
- 100% target data: **10/10 improve**; mean +.01284; median +.01452; r_rb=1.00; session-level P=.000977.
- At 100%, both Lalo and Offenbach are positive in all 5/5 held-out sessions; mean gains are +.01445 and +.01124 respectively.
- Inference remains nested in **2 monkeys**, so the session-level P value is a within-dataset sensitivity statistic, not a population-level primate P value.

**Aeon**
- 20%: 3/5 experiments positive, P=.156.
- 50%: 1/5 positive, P=.781.
- 100%: 4/5 positive, P=.0938.
- therefore no robust frozen-core transfer claim.

This sharpens the model-level conclusion: **SOE does contain reusable recurrent dynamics for the macaque task under a frozen-core test, but transfer is not universal across every social task.** This result is stronger than the fine-tuning-initialization result and should be shown as cross-species representation transfer with the two-monkey nesting caveat.

