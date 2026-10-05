# Reward-type memory × expression gate authority v1 — 2026-10-05

## Status

**NEW MECHANISTIC SYNTHESIS**

The cross-reward conclusion is now more specific than “some rewards show contrast and some do not.”

A reward-history effect can fail at at least three separable stages:

1. past reward samples may fail to establish a persistent history state;
2. the stored history may fail to alter the neural response to the current reward;
3. a neural history signal may be present but fail to gain access to the behavioral comparison/readout that changes persistence.

The third possibility is directly supported by the VTA-stimulation history dataset.

---

## 1. New QE same-current-reward test

### Question

Does reward-quality history affect behavior when the current physical reward is held fixed?

The QE dataset is useful because 100E (EE) and quinine-adulterated 100E (QE) were interleaved. We selected current EE bouts only, so the current reward is the same 100E while the frozen alpha=.20 history coordinate varies according to prior EE/QE sampling.

### Cohort and model

- current condition: EE / 100E only;
- prior reward sampling required;
- 63 current-100E bouts;
- 7 mice;
- predictor: frozen contrast coordinate C=U-R at alpha=.20;
- nuisance controls: animal fixed effects and cubic session progress;
- outcomes: dopamine AUC, AUC/s and log bout duration.

### Pooled animal-clustered result

- AUC: beta(C)=+114.984, P=.00260;
- AUC/s: beta(C)=+0.918, P=.0487;
- log duration: beta(C)=+0.818, P=.0340.

Thus, after worse recent reward history, the same current 100E tends to evoke both a larger dopamine response and longer feeding persistence.

### Serial-structure control

Within each mouse, C was circularly shifted while preserving the serial structure of the selected 100E bouts.

20,000 circular shifts:

- AUC: observed beta=114.984; two-sided P=5e-5;
- AUC/s: observed beta=.918; one-sided P=.00705, two-sided P=.0772;
- log duration: observed beta=.818; one-sided P=.0287, two-sided P=.0776.

The directional behavioral result survives a history-specific serial null, but the two-sided test is not below .05.

### Animal-level direction

Animal-specific session-adjusted slopes were estimable in 6 mice:

- AUC: 5/6 positive; median beta=88.36; one-sided Wilcoxon P=.0781;
- AUC/s: 5/6 positive; median beta=.871; P=.0781;
- log duration: 5/6 positive; median beta=.515; P=.156.

Therefore the QE behavioral-history result is **PROVISIONAL**, not a new strong primary claim.

The robust part is that the same-current 100E neural history effect is reproduced; the behavioral effect is directionally consistent and passes the clustered and one-sided serial tests, but animal-level power is limited.

---

## 2. Current reward potency is not sufficient for behavioral contrast

To ask whether the absence of a history effect simply reflects an inability of a reward manipulation to change feeding, current-reward effects were calculated with the same behavioral endpoint: per-animal median log bout duration.

### Natural reward quality

100E minus 20E:

- 11/11 mice positive;
- median delta log duration=+1.043;
- exact paired Wilcoxon P=.000977.

### QE reward quality

EE minus QE:

- 7/7 mice positive;
- median delta log duration=+2.013;
- exact paired Wilcoxon P=.015625.

### VTA stimulation

ON minus OFF:

- 11/13 mice positive;
- median delta log duration=+.208;
- exact paired Wilcoxon P=.003418.

Therefore all three reward manipulations are behaviorally potent when they are the **current** reward.

Yet their history effects differ.

---

## 3. Three-stage reward-type comparison

### Natural 100E/20E

**Current reward -> behavior: PASS**

Current reward quality strongly changes persistence.

**History -> VTA dopamine: PASS**

Cumulative sampled history retains unique information:
delta R2=.02686, conditional permutation P=.00670.

**History -> behavior: PASS**

The frozen reference predicts:
- log duration beta=.476, P=.00566;
- termination OR=.459, P=.000180.

Interpretation:
the food-based reference is expressed in both VTA dopamine and persistence.

### QE / quinine reward-quality history

**Current reward -> behavior: PASS**

Current quinine devaluation strongly changes persistence.

**History -> VTA dopamine: PASS**

The frozen Natural alpha=.20 history coordinate transfers to QE:
delta R2=.02540, animal-clustered P=.00141;
within-animal circular-shift P=.00205.

The new same-current-100E test also gives:
AUC beta=114.98, P=.00260.

**History -> behavior: PROVISIONAL**

Same-current 100E log duration:
beta=.818, animal-clustered P=.0340;
serial-shift one-sided P=.0287;
5/6 estimable animal slopes positive, one-sided P=.156.

Interpretation:
sensory/devaluation history can reach behavioral persistence, but the present seven-mouse behavioral evidence is not yet strong enough to promote to a primary claim.

### VTA stimulation history

**Current reward -> behavior: PASS**

Acute stimulation changes persistence:
11/13 mice positive; paired log-duration P=.003418.

**History -> VTA dopamine: PASS**

Past stimulation reference remains after current condition, local adaptation, slow session variables and future reference:
unique delta R2=.002524;
conditional permutation P=5e-5;
10/13 animals show the expected Rpast direction after local controls, Wilcoxon P=.0215.

**History -> behavior: NULL**

The same past-history state does not reliably predict later bout duration:
P=.742.

Interpretation:
a reward can be acutely behaviorally potent and leave a persistent neural history trace, yet fail to produce gross behavioral contrast.

---

## 4. Biological conclusion

The data reject two simple explanations for reward-class differences.

### Not simply reward potency

VTA stimulation is behaviorally potent when delivered during the current bout, yet stimulation history does not reliably alter later duration.

### Not simply whether a history trace persists

Stimulation history persists strongly enough to alter later dopamine after stringent controls, yet that neural history signal is not sufficient for a measurable duration contrast.

The working architecture is therefore:

sampled reward history
-> stored reference / history state
-> neural comparison or reference-dependent readout
-> context- and reward-specific behavioral gain

A compact expression is:

Behavioral contrast = stored history × comparison readout × behavioral output gain.

This is conceptual, not a literal multiplicative fitted model.

The key new point is:

**contrast susceptibility depends on access from reward memory to the behavioral comparator/readout, not only on the magnitude of the current reward or the persistence of memory.**

---

## 5. Highest-value tests

### A. Delay × sample-count factorial

Independently vary:

- elapsed time since the prior reward;
- number of prior reward samples;
- sampled amount/value.

Measure both the neural reference and behavioral persistence.

Diagnostic outcomes:

- neural R decays and behavior disappears together -> memory persistence limit;
- neural R remains but behavior disappears -> expression/retrieval limit;
- behavior changes without a neural R change -> parallel non-VTA comparator.

### B. Same history, different current reward identity

Hold the stored history constant and probe different current rewards.

Test history × current-identity interactions in both VTA dopamine and persistence.

This asks whether some current rewards have higher behavioral comparator gain even when memory strength is matched.

### C. Same current reward, different memory strength

The QE same-current analysis should be replicated prospectively with a larger cohort and deliberately separated high-R and low-R histories.

Primary endpoints should be pre-specified:

- sustained VTA dopamine;
- log bout duration;
- termination hazard.

### D. Retrieval-cue manipulation

Build the same history state, then manipulate contextual or sensory cues at retrieval without changing the current reward.

If the neural history trace remains while behavior changes, retrieval/output gating is implicated.

### E. Convert the stimulation reference into behavior

Stim13 is the cleanest testbed because it already has:

- acute behavioral potency;
- a persistent neural history signal;
- no reliable history-dependent duration effect.

Perturb the consumption-period dopamine/downstream persistence pathway during current bouts matched for pre-existing stimulation history.

If behavior becomes history dependent while R is held fixed, this would directly support a behavioral-gain gate.

---

## 6. Boundaries

Do not claim:

1. QE behavioral contrast is fully established; it is provisional.
2. alpha=.20 is a universal memory constant.
3. VTA is the storage site of the reference.
4. absence of a duration effect means absence of all behavioral expression; other endpoints may still carry history.
5. effect magnitudes across Natural, QE and Stim13 are directly comparable; the predictors and measurement scales differ.

---

## 7. Authority files

New analysis:
- `H:/rewardcontrast_model_zoo_20260929/reward_type_gate_20261005/QE_same_current_behavior_expression_v1.csv`
- `H:/rewardcontrast_model_zoo_20260929/reward_type_gate_20261005/QE_same_current_animal_direction_v1.csv`
- `H:/rewardcontrast_model_zoo_20260929/reward_type_gate_20261005/QE_same_current_circular_shift_fast_v2.csv`
- `H:/rewardcontrast_model_zoo_20260929/reward_type_gate_20261005/current_reward_behavior_potency_v1.csv`

Reader-facing:
- `data/NEURON_reward_type_memory_expression_gate_v1.csv`
- `assets/ED8_reward_type_memory_expression_gate_v1.png`
- `assets/ED8_reward_type_memory_expression_gate_v1.pdf`

Related prior authorities:
- `docs/REWARD_CONTRAST_BIOLOGICAL_MODEL_AUTHORITY_v1_20261004.md`
- `docs/REWARD_CONTRAST_STIM_LICKLEVEL_AUTHORITY_v1_20261004.md`
- `docs/REWARD_CONTRAST_VALUE_VS_ACTION_AUTHORITY_v1_20261004.md`
