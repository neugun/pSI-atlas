# Reward Contrast — Reward-Type Memory × Expression Authority v3
## 2026-10-05 — current authority

### Supersedes
This file supersedes the **interpretive layer** of:
- REWARD_CONTRAST_REWARD_TYPE_GATE_AUTHORITY_v2_20261005.md
- REWARD_CONTRAST_REWARD_TYPE_GATE_AUTHORITY_v1_20261005.md

Those files remain provenance.

The v2 core result remains valid:
- Natural reward history is expressed in VTA dopamine and behavior.
- QE same-current behavioral history is provisional.
- Stim13 has strong neural history and no stable **marginal** duration-history effect across the scanned alpha family.

The v3 update adds a necessary distinction:
**marginal history effects, current-conditioned history effects, and deep-reference effects are not the same claim.**

---

## 1. Current conclusion

Reward-history expression is layered.

A useful hierarchy is:

1. current reward potency;
2. history formation / stored reference;
3. neural history readout;
4. marginal behavioral history expression;
5. current-conditioned behavioral structure;
6. deep-reference behavioral expression independent of recent local context.

The current data do **not** support one universal current-reward-dependent deep comparator gate across Natural, QE and Stim13.

Instead:

- **Natural**: current reward identity appears to modulate behavioral history sensitivity, but this gain is not uniquely separable from local-history × current terms.
- **QE**: direction is concordant, but the common-support cohort is too small for a strong gate claim.
- **Stim13**: marginal/deep behavioral reference expression remains unestablished. Condition-specific duration structure can be detected in some analyses, but it is sensitive to recent-history specification and cannot be promoted to an independent deep-reference gate.

The strongest manuscript-safe statement is therefore:

> **Current reward identity and recent context can reshape how reward history appears in behavior, but a cross-task, local-history-independent deep-reference gate has not been established.**

---

## 2. Why this update was necessary

The v2 analysis showed:

### Stim13 marginal history
At frozen alpha=.20:

- neural Rpast beta = -0.230168;
- animal-clustered P=.01421;
- all-control unique neural delta R2=.002524, conditional permutation P=5e-5.

For log duration:

- Rpast beta=.02164;
- P=.74240.

Across alpha=.03-.60:

- neural history: 8/8 significant, BH q<=.0192;
- marginal duration history: 8/8 null, minimum raw P=.682, BH q>=.906.

Thus the marginal behavioral-null result is robust to memory timescale.

However, a null marginal slope can conceal different slopes under current-low and current-high conditions. v3 explicitly tests that possibility.

---

## 3. Common-support R × current-reward test

### Design

For each task:

- use frozen alpha=.20;
- express memory as the stored reference R, not C=U-R;
- restrict within each animal to overlapping R support across current-low and current-high bouts;
- model log bout duration with:
  - standardized R;
  - current condition;
  - R × current interaction;
  - cubic session progress;
  - animal fixed effects;
- infer the interaction with exact animal-cluster wild sign-flips.

Current-high means:
- Natural: 100E;
- QE: EE / non-quinine 100E;
- Stim13: current ON stimulation.

### Natural

333 common-support bouts / 11 mice.

- R × current-high beta = **-.2631**
- exact cluster-wild two-sided P = **.0278**

Interpretation:
the stored-reference slope is more negative when the current food is 100E than when it is 20E.

### QE

131 common-support bouts / 6 mice.

- interaction beta = **-.4156**
- exact cluster-wild two-sided P = **.0769**

Interpretation:
direction is consistent with stronger reference sensitivity on the current-high / EE side, but the common-support cohort is underpowered.

### Stim13

1785 common-support bouts / 13 mice.

- interaction beta = **-.1252**
- exact cluster-wild two-sided P = **.0372**

At this stage alone, one could incorrectly conclude that stimulation history has a robust condition-dependent behavioral expression despite the marginal null.

The subsequent controls show why that conclusion is too strong.

---

## 4. Animal-level cross-task direction

Within common-support data, current-low and current-high R slopes were estimated separately for each animal after local standardization.

Behavioral slope difference:
current-high slope minus current-low slope.

Results:

- Natural: 8/10 negative;
- QE: 5/6 negative;
- Stim13: 11/13 negative.

Across all 29 independent animals:

- 24/29 negative;
- median standardized delta = -.1398;
- two-sided Wilcoxon P = **.00215**.

Neural slopes:
- 22/29 negative;
- two-sided Wilcoxon P=.0274.

This cross-task concordance is biologically interesting, but it is **descriptive/supportive rather than a universal-mechanism test**, because the three tasks differ in reward identity, neural endpoint and local sequence structure.

---

## 5. Termination-hazard sensitivity

A stratified Cox proportional-hazards sensitivity analysis was run within common support.

R × current-high interaction hazard ratios:

- Natural: HR=**1.544**, P=.000750;
- QE: HR=**2.223**, P=1.57e-12;
- Stim13: HR=**1.143**, P=.00467.

HR>1 means that higher R increases termination relatively more under the current-high condition.

These results support the direction of the log-duration interaction, but they are **not the primary inference**, especially for QE with only six common-support clusters.

Primary small-cluster inference remains the exact wild test.

---

## 6. Alpha-family sensitivity of the behavioral identity interaction

The current-conditioned behavioral interaction was scanned across recency values.

### Natural

Two-sided exact-wild BH q:

- alpha=.10: q=.0451;
- alpha=.20: q=.0464;
- alpha=.30: q=.0451.

The very slow alpha=.03 and very fast alpha=.60 are weaker.

Thus Natural current-identity sensitivity is not confined to alpha=.20.

### QE

Two-sided BH q is ~.062-.077 across the stronger range.

Directional negative-side q reaches ~.046, but because the direction was not an independent confirmatory endpoint, QE remains **PROVISIONAL**.

### Stim13

Two-sided BH q does not fall below .05; minimum is ~.0745.

Directional negative-side q reaches ~.037 at alpha=.20-.60.

This is another reason not to promote the Stim13 conditional effect as a primary discovery.

---

## 7. Local-history adjudication

The critical question is whether R × current remains after recent local sequence variables are added.

Local variables:
- previous bout identity;
- recent 3-bout identity average;
- recent 5-bout identity average;
- previous bout duration;
- current-condition run position.

### Natural

Exact-wild interaction:

- base: P=.0278;
- + local-history main effects: **P=.0122**;
- + local-history main effects and local × current interactions: P=.290.

Interpretation:
Natural current-identity sensitivity is robust to local-history main effects, but its unique separation from local-history × current interactions is not established.

### QE

- base: P=.0769;
- + local main: P=.200;
- + local × current: P=.200.

Interpretation:
underpowered; do not promote.

### Stim13

- base: P=.0372;
- + local-history main effects: **P=.899**;
- + local × current interactions: P=.135.

Interpretation:
the apparent Stim13 condition-dependent duration effect is **not independent of recent local history**.

Therefore the base Stim13 interaction must not be used to overturn the v2 marginal/deep behavioral-null conclusion.

---

## 8. Does a local-history interaction block replace R × current?

A five-term local-history × current block was tested jointly while retaining R × current.

Exact cluster-wild block P:

- Natural: .622;
- QE: .723;
- Stim13: .243.

Thus there is no evidence that one simple local interaction block alone provides a clean replacement mechanism.

The correct interpretation is **shared / collinear information and limited identifiability**, not “the last three bouts are the gate.”

---

## 9. Deep-reference residualization

R was residualized against:

- previous bout identity;
- recent 3- and 5-bout identity;
- previous bout duration;
- run position;
- session progress;
- animal.

The local model explains:

- Natural: R2=.597;
- QE: R2=.788;
- Stim13: R2=.900.

This is expected because the recursive reference is strongly driven by recent samples.

### Deep residual R × current interaction

Behavior:

- Natural: P=.309;
- QE: P=.108;
- Stim13: P=.154.

Neural:

- Natural: P=.778;
- QE: P=.0769;
- Stim13: P=.128.

Therefore a **deep-residual identity-specific gain is not established** in any task.

This does **not** mean deep reference information is absent from neural data. It means that after aggressive recent-history residualization, there is no evidence that the remaining reference component has a different slope under current-low versus current-high conditions.

---

## 10. Deep residual main effects after local-history control

When testing the deep residual R as a main effect, rather than an identity interaction:

### Natural

- neural deep R: exact-wild P=.00830;
- behavior deep R: P=.0542.

This supports neural deep-history information in Natural.

### QE

- neural: P=.0769;
- behavior: P=.354.

The six-animal common-support subset limits inference.

### Stim13

- neural: P=.305;
- behavior: P=.763.

This aggressive residualization removes about 90% of Stim13 R variance and is more severe than the established full-control neural authority. It should **not** replace the earlier Stim13 all-control analysis showing unique past-reference neural information.

Authority remains:
- full-control Stim13 neural unique delta R2=.002524;
- conditional permutation P=5e-5.

---

## 11. Matching adjudication

### A. R + session-position optimal matching

Animal-level high-minus-low behavior difference versus pair mean R:

- Natural: 7/10 negative, P=.275;
- QE: 3/6 negative, P=.688;
- Stim13: 10/13 negative, P=.0479.

### B. Add recent context to the matching distance

Matching additionally included:
- recent 3-bout identity;
- previous duration;
- run position.

Results:
- Natural: 7/10 negative, P=.0645;
- QE: 5/6 negative, P=.0938;
- Stim13: 11/13 negative, P=.0479.

However, match quality in R worsened.

### C. Exact previous-condition matching

Pairs were required to have the same previous bout condition.

Results:
- Natural: null;
- QE: 6/6 negative, P=.0313;
- Stim13: 11/13 negative, P=.0479.

Stim13 R matching became extremely tight:
median |delta R| ~.0046.

### D. Joint R + recent-3 caliper sensitivity

When both R and recent-3 context are progressively tightened, results become unstable:

- strict settings lose animals and pairs;
- Stim13 direction/significance varies with the caliper;
- Natural is inconsistent;
- QE becomes sparsely identifiable.

Therefore matching supports the existence of **conditional structure**, but not a stable universal deep-reference gate.

---

## 12. Relation to ED3 gain/loss asymmetry

The v3 behavioral current-identity analysis is **not the same statistical test** as the ED3 positive-vs-negative comparator-channel analysis.

Existing neural authority:

- Natural formal gain/loss interaction P=.216;
- QE P=.000527;
- fully controlled Stim13 P=.197.

Therefore do not rewrite the neural story as universal gain dominance.

The new behavioral result says something narrower:

> the observed history slope can differ with current reward identity, especially in Natural and in some Stim/QE analyses, but this conditional behavioral structure is partly entangled with local sequence context.

---

## 13. Updated status by task

### Natural 100E/20E

**Current reward potency:** PASS  
**Neural history:** PASS  
**Marginal behavioral history:** PASS  
**Current-conditioned behavioral sensitivity:** SUPPORTED  
**Unique deep identity gate:** NOT ESTABLISHED

Natural is currently the strongest evidence that current reward identity can modulate behavioral expression of history.

### QE

**Current reward potency:** PASS  
**Neural history:** PASS  
**Marginal behavioral history:** PROVISIONAL  
**Current-conditioned structure:** PROVISIONAL  
**Unique deep identity gate:** NOT ESTABLISHED

### Stim13

**Current reward potency:** PASS  
**Neural history:** PASS  
**Marginal behavioral history:** NOT ESTABLISHED / robust marginal null  
**Current-conditioned behavioral structure:** DETECTABLE IN SOME ANALYSES  
**Independence from local history:** NOT ESTABLISHED  
**Unique deep identity gate:** NOT ESTABLISHED

The correct Stim13 description is now:

> Past stimulation leaves a robust neural history signal. Gross bout duration has no stable marginal or deep-reference history effect. Some current-conditioned duration structure can be detected, but it is sensitive to recent local context and therefore cannot yet be interpreted as an independent behavioral readout of the stored reference.

---

## 14. Manuscript-safe mechanistic architecture

The current architecture should be:

sampled reward history  
→ reference / latent history state  
→ VTA history readout  
→ behavioral expression shaped by current reward and local context

with the following constraints:

1. reference formation and neural readout are better established than a universal behavioral comparator;
2. marginal and conditional behavioral effects must be separated;
3. current reward identity may alter behavioral gain;
4. local recent history can strongly affect identifiability of that gain;
5. no universal deep-reference × current-reward gate is established.

A concise formulation:

> **Behavioral contrast is the context-dependent expression of a stored reward history, not an obligatory consequence of storing or neurally reading that history.**

---

## 15. Highest-value next experiment

The decisive design is no longer merely “scan alpha.”

Prospectively create a factorial design that independently controls:

- stored reference R;
- previous one-bout condition;
- recent 3-5-bout context;
- current reward identity;
- current reward magnitude;
- elapsed delay.

Then randomize the current outcome after constructing matched history states.

Primary endpoints:

- sustained VTA dopamine;
- log bout duration;
- termination hazard.

This allows direct identification of:

- deep reference memory;
- local carryover;
- current-reward-dependent comparator gain;
- DA-to-behavior coupling.

For Stim13 specifically:

1. construct matched R states;
2. exact-match previous ON/OFF history;
3. randomize current ON/OFF;
4. measure early/current-bout DA and persistence.

That experiment directly tests whether the current-conditioned structure is genuine comparator gain or local stimulation carryover.

---

## 16. Current v3 authority files

Primary:
- NEURON_reward_type_memory_expression_gate_v3_20261005.csv
- NEURON_three_context_reference_evidence_v3_20261005.csv
- CURRENT_IDENTITY_GATE_ADJUDICATION_SUMMARY_v1.csv
- CURRENT_IDENTITY_REFERENCE_WILD_CLUSTER_EXACT_v1.csv
- CURRENT_IDENTITY_REFERENCE_COX_HAZARD_v1.csv
- BEHAVIOR_IDENTITY_GATE_LOCAL_ADJUDICATION_v1.csv
- DEEP_REFERENCE_IDENTITY_GATE_AFTER_LOCAL_HISTORY_v1.csv
- DEEP_REFERENCE_MAIN_EFFECT_AFTER_LOCAL_HISTORY_v1.csv
- BEHAVIOR_IDENTITY_GATE_TIMESCALE_EXACT_WILD_v1.csv
- CURRENT_IDENTITY_PREVCONDITION_EXACT_MATCHED_SUMMARY_v1.csv
- CURRENT_IDENTITY_PREVCONDITION_MATCH_CALIPER_SENSITIVITY_v1.csv

Figures:
- ED8_reward_type_memory_expression_gate_v2.png/pdf
- ED9_memory_timescale_vs_expression_gate_v1.png/pdf
- ED10_current_identity_gate_adjudication_v1.png/pdf

Retained prior authorities:
- REWARD_CONTRAST_REWARD_TYPE_GATE_AUTHORITY_v2_20261005.md
- REWARD_CONTRAST_STIM_LICKLEVEL_AUTHORITY_v1_20261004.md
- REWARD_CONTRAST_VALUE_VS_ACTION_AUTHORITY_v1_20261004.md
- REWARD_CONTRAST_BIOLOGICAL_MODEL_AUTHORITY_v1_20261004.md

### One-sentence current authority

**Reward history can be stored and read out neurally without a stable marginal behavioral contrast; current reward identity can reshape behavioral history slopes, but this conditional structure is not yet separable from recent local context as a universal deep-reference gate.**
