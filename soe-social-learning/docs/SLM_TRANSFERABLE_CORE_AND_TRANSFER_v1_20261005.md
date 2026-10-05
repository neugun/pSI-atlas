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

The present same-zoo contract still compares multiscale state mainly with a current baseline and TinyRNN. A matched classical RL family is still absent. This dataset supports a multiscale-state component but does **not yet** establish SLM superiority over the best classical RL comparator.

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

**External behavior:** human and macaque structured states clear stronger Feature-Q comparators; rat DANDI001169 and mouse DANDI001632 provide component-level timing/history support.

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

The six Social-trained mice with later observational-fear and food-neophobia assays were linked back to their held-animal SOE latent trajectories.

A prespecified exploratory grid tested late-state values and early-to-late changes in policy, credit separation, Q difference, |RPE|, and |APE| against food latency, shock response, shock observation, cue quieting, and a cross-assay composite.

- n = 6 animals.
- exact 720-permutation Spearman tests.
- 50 exploratory associations corrected together by BH.
- **No association survives BH correction.**
- strongest nominal signal: late policy vs later shock velocity, rho = -1.0, exact P=.00278, q=.139.

This analysis is hypothesis-generating only. The present data do not support a headline claim that a single SOE latent magnitude predicts later generalization.

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

