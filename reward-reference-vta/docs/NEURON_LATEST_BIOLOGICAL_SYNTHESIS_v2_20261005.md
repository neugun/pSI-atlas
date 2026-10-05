# Reward Reference × VTA Dopamine
## Latest biological synthesis — 2026-10-05

### One-sentence result

Past sampled rewards establish a persistent reference before the current bout; current consumption recruits a strong sampling/action component in VTA dopamine, and with continued consumption dopamine additionally expresses current reward relative to that learned reference, contributing to feeding persistence while behavioral expression remains context dependent.

---

## 1. Biological sequence

### Step 1 — actual reward sampling writes history

The reward-history signal is not well explained by passive time after a programmed reward switch.

- before the first sample of the new reward, passive-time models add at most ~0.004 R²;
- once consumption begins, sampled exposure carries graded update information.

Interpretation:
the relevant state is experience-gated. Time may modulate memory, but elapsed time alone is not the primary update variable.

### Step 2 — sampled rewards establish a stored reference R

The reference is a continuous history coordinate rather than a categorical context label.

Natural-task held-animal sustained-DA prediction:
- current reward alone: R² ≈ 0.038;
- context: R² ≈ 0.123;
- continuous history state: R² ≈ 0.175;
- context + history: R² ≈ 0.178.

Deeper cumulative history remains informative after local adaptation controls:
- unique ΔR² ≈ 0.02686;
- conditional permutation P ≈ 0.00670.

The exact biological implementation of the recency kernel is not known.
A broad α≈0.15–0.20 regime is empirically useful; α=.20 should not be described as a universal biological constant.

### Step 3 — current consumption contributes a genuine action/sampling component

The action confound is real:

- reference state vs whole-bout lick count: r ≈ 0.611;
- reference state vs bout duration: r ≈ 0.599;
- whole-bout lick count vs sustained DA: r ≈ 0.392.

However, the primary neural endpoint is the **fixed 2–5 s mean DA**, not whole-bout AUC.

Partial variance with flexible early + concurrent action terms:
- reference unique ΔR² ≈ 0.04895;
- action unique ΔR² ≈ 0.10791;
- shared component ≈ 0.00214;
- joint increment ≈ 0.1590.

Thus action is a major component of the population signal, but it is not the same information as the learned reference.

### Step 4 — the learned reference remains after current-action control

Reference-state unique variance after action controls:

- 0–2 s action control: ΔR² ≈ 0.0543, conditional P ≈ 0.0464;
- 0–2 + 2–5 s action control: ΔR² ≈ 0.04895, P ≈ 0.0449;
- whole-bout lick count/rate/duration over-control: ΔR² ≈ 0.03299, P ≈ 0.0357.

Joint clustered model:
- RWstate β ≈ 2.283, P ≈ 0.00171;
- early 0–2 s licks β ≈ 0.376, P ≈ 0.0165;
- concurrent 2–5 s licks β ≈ 0.554, P ≈ 0.000457.

Therefore:
- **not “value instead of licking”**;
- **not “licking explains the reference effect”**;
- best description = multiplexed sampling/action + reference-dependent value.

### Step 5 — current reward and learned reference enter with opposite signs

With early + concurrent action main effects controlled:

- current reward U = +0.815, P = 8.6×10⁻⁵;
- learned reference R = −2.211, P = 0.00153;
- U−R contrast β = 1.513, P = 5.9×10⁻⁵.

Under very flexible reward×action interaction controls, U becomes unstable because current reward strongly drives action.
Crucially, R remains negative:

- early + concurrent interacted action: R ≈ −2.054, P ≈ 0.00253;
- whole-bout interacted over-control: R ≈ −1.794, P ≈ 0.00495.

This is especially diagnostic because R is determined by past experience before the current bout and cannot be rewritten as current lick number.

### Step 6 — the relative-value component strengthens later in consumption

Broad, pre-specified windows:

- pre-bout U−R β ≈ −0.485;
- early 0–2 s β ≈ +0.294, not significant;
- sustained 2–5 s β ≈ +1.752, P ≈ 0.00893;
- sustained − early increase ≈ +1.458, P ≈ 9×10⁻⁸;
- 11/11 animals have a larger sustained than early slope.

Raw-signal control:
- early U−R β ≈ −0.191, P ≈ 0.718;
- sustained U−R β ≈ +1.267, P ≈ 0.0399.

Exploratory 0.5-s decomposition:
- prior within-bout sampling becomes FDR-significant from ~1–1.5 s onward;
- reference coefficient becomes positive around ~3 s and is nominally significant through ~4.5 s;
- across 10 bins, late reference tests reach BH q≈0.076.

Interpretation:
sampling/action appears first; history-relative value strengthens later.
The fine-bin timing is mechanistic evidence, not an independent corrected discovery.

### Step 7 — nonlinear nuisance models do not remove the reference effect

Cross-fitted nonlinear action removal:

- Random Forest residual reference slope ≈ 1.890; cluster P≈0.00054; conditional permutation P≈0.010;
- ExtraTrees slope ≈ 1.895; P≈0.00135; permutation P≈0.0172;
- HistGradientBoosting slope ≈ 1.603; P≈0.00080; permutation P≈0.00170.

These are functional-form robustness tests.
Their held-animal DA nuisance prediction is weak, so they should not be presented as superior DA predictors.

### Step 8 — dopamine contributes causally to persistence

Natural reference state predicts bout termination:
- OR ≈ 0.459;
- P ≈ 0.000180.

Causal dopamine manipulation:
- activation: OR ≈ 0.690, P≈3.29×10⁻¹⁰;
- contingent JAWS: OR ≈ 1.341, P≈0.0289;
- noncontingent inhibition: OR≈1.116, P≈0.0976;
- contingent vs noncontingent interaction: P≈0.0515.

Conclusion:
consumption-period dopamine contributes to feeding persistence.

Do not claim:
the complete history → dopamine → behavior pathway is proven as full mediation.

### Step 9 — reference memory, neural readout and overt behavior can dissociate

In the lick-level VTA stimulation dataset:

- past stimulation-history reference predicts later DA;
- conditional past-reference information survives local adaptation and future-reference controls;
- 10/13 animals show the expected direction;
- feeding duration does not show a reliable corresponding history effect (P≈0.742).

Interpretation:
absence of gross behavioral contrast does not imply absence of reward-reference memory.
A stored reference can be expressed neurally while downstream behavioral gain is weak.

### Step 10 — the reference computation generalizes, but output gain is context dependent

Natural → QE frozen transfer:
- strict pure-100E bouts;
- history state adds ΔR²≈0.02540 to DA AUC;
- clustered P≈0.00141;
- within-animal circular-shift P≈0.00205;
- 6/7 animal slopes positive.

Direct stimulation-history analysis also contains past-reference information.

This supports:
- transferable history/reference computation;
- broad shared recency regime.

It does **not** establish:
- identical waveform across tasks;
- identical directional asymmetry across tasks;
- one universal comparator gain.

### Step 11 — memory timescale does not explain the reward-class difference in behavioral contrast

The current reward-type gate was tested across a broad family of per-sample recency values rather than only at the frozen alpha=.20.

Natural 100E/20E:
- neural history is significant at all scanned alpha=.03–.60 (BH q<=.00131);
- behavioral history is significant from alpha=.03–.30 (BH q≈.0103), weakening only at the very fast alpha=.60 limit.

QE same-current 100E:
- neural AUC history is significant at all scanned alpha=.10–.30 (cluster BH q<=.0225; serial-shift two-sided q<=.00665);
- behavioral duration is directionally positive across alpha=.15–.30, but after alpha-family correction remains just outside threshold (cluster q≈.0555; directional serial q≈.057–.060), so this remains PROVISIONAL.

Stim13:
- raw lick-level reconstruction reproduces the frozen alpha=.20 neural effect (Rpast beta=-.23017, P=.01421) and behavioral null (beta=.02164, P=.74240);
- across alpha=.03–.60, neural Rpast is significant at 8/8 timescales (BH q<=.0192);
- feeding duration remains null at 8/8 timescales (minimum raw P=.682; BH q>=.906).

Interpretation:
the lack of stimulation-history behavioral contrast is not a consequence of choosing a memory timescale that is too slow or too fast.
Reward history can remain neurally readable across a broad range of recency scales while failing to reach the behavioral output controlling gross feeding persistence.

This supports a separable behavioral expression gate downstream of, or parallel to, neural history readout.

---

## 2. Current mechanistic architecture

### Input transformation
Physical reward q is transformed by physiological state H into current utility U.

### Memory
Previously sampled utilities are compressed into a stored reference R.

### Consumption-period neural signal
VTA dopamine contains at least:
1. ongoing reward-sampling / consummatory-action information;
2. a later history-relative component involving U and R.

Conceptually:

DA(t) ≈ a(t)·Sampling(t) + g_DA(C,t)·[U−R] + other terms

### Behavioral output
Persistence and other actions read out this state through context-dependent gain:

Behavior ≈ g_B(C)·[U−R] + causal DA contribution

The key biological distinction is:
**reference formation can generalize while readout gain differs across neural and behavioral endpoints.**

---

## 3. What the main figures should now mean

### Fig1
Same physical current reward, different recent history → different sustained DA and persistence.

### Fig2
Reference updating is experience-gated; passive time is insufficient.
Current action does not absorb the history signal.

### Fig3
The reference is continuous, retains deeper reward path, and is not only local switch adaptation.

### Fig4
Belief/HMM, average reward rate, uncertainty/adaptive gain and recurrent alternatives do not absorb the cumulative-history information.

### Fig5
History-relative value is constructed across consumption rather than being a fixed onset response.

### Fig6
Reference information transfers across reward contexts, but broader value geometry and temporal expression should not be conflated.

### Fig7
Natural state and causal dopamine perturbations converge on feeding persistence, without proving complete mediation.

### Extended Data — Value vs Action
VTA dopamine multiplexes action/sampling and reward-reference information.
This figure is now central to interpreting the neural signal rather than a secondary confound check.

### Extended Data — Reward-type gate / memory timescale
ED8 separates current reward potency, neural history readout and behavioral history expression.
ED9 shows that the Stim13 neural-history / behavioral-null dissociation survives the full scanned recency range, while Natural expresses history in both outputs and QE remains intermediate/provisional.

---

## 4. Claim hierarchy

### Strong / primary

1. Experienced reward history changes the neural and behavioral response to an identical current reward.
2. Actual reward sampling is more important than passive elapsed time for updating the reference.
3. A continuous reward-history state contains information not absorbed by several strong latent-state alternatives.
4. Sustained VTA DA contains both consummatory-action and learned-reference information.
5. Current reward and learned reference enter sustained DA with opposite signs under appropriate action controls.
6. Consumption-period dopamine contributes causally to feeding persistence.
7. Reference memory and gross behavioral expression can dissociate.
8. In Stim13, this dissociation is robust across alpha=.03–.60: neural history remains significant while gross duration remains null, ruling out a simple memory-timescale mismatch.

### Supported but secondary

1. A broad recency regime transfers across Natural, QE and stimulation datasets.
2. Fine temporal analysis suggests sampling/action precedes the stronger reference component.
3. Signed reference error adds information beyond unsigned salience.
4. A frozen Natural reference transfers to QE neural data.
5. Same-current QE behavior is directionally history-dependent across alpha=.15–.30, but remains provisional after alpha-family correction.

### Provisional / do not overclaim

1. one exact biological α;
2. one universal comparator gain;
3. positive-vs-negative directional asymmetry in every context;
4. complete mediation of history effects by VTA dopamine;
5. one identified cellular population storing R;
6. strong held-animal prediction from the strict 192-bout value-vs-action subset;
7. QE behavioral-history expression as a fully established primary result.

---

## 5. Manuscript-safe core paragraph

Past sampled rewards establish a persistent reference that shapes subsequent valuation. During a new bout, VTA dopamine is not a pure abstract value signal: ongoing consumption contributes substantial action/sampling-related variance. However, current action does not absorb the history effect. The learned reference remains independently associated with sustained dopamine, current reward and reference enter with opposing signs, and the relative-value component strengthens with continued consumption. Dopamine perturbations bidirectionally alter feeding persistence, whereas direct stimulation history can produce robust neural reference effects without reliable gross behavioral contrast. Crucially, the stimulation-history dissociation persists from very slow to very fast sample-based memory kernels: neural history remains detectable at every scanned timescale while duration remains null. Together, these results support a layered architecture in which reward sampling writes a transferable reference, VTA dopamine multiplexes ongoing sampling with history-relative utility, and a separable context-dependent gate determines whether stored reward history becomes overt behavior.

---

## 6. Current primary authorities

- REWARD_CONTRAST_REWARD_TYPE_GATE_AUTHORITY_v2_20261005.md
- NEURON_LATEST_BIOLOGICAL_SYNTHESIS_v2_20261005.md
- NEURON_VALUE_VS_ACTION_AUTHORITY_v1_20261004.md
- REWARD_CONTRAST_BIOLOGICAL_MODEL_AUTHORITY_v1_20261004.md
- REWARD_CONTRAST_STIM_LICKLEVEL_AUTHORITY_v1_20261004.md
- NEURON_MODEL_EVIDENCE_AUTHORITY_v10_20260928.md
- NEURON_FIGURE_VISUAL_QC_20261004.md

Primary new quantitative tables:
- NEURON_three_context_reference_evidence_v2_20261005.csv
- NEURON_reward_type_memory_expression_gate_v2_20261005.csv
- STIM13_memory_timescale_neural_vs_behavior_v2_BH.csv
- NATURAL_timescale_neural_vs_behavior_v2_BH.csv
- QE_same_current_timescale_scan_v2_BH.csv
- REWARD_MEMORY_TIMESCALE_EXPRESSION_SUMMARY_v1.csv
- NEURON_value_action_conditional_perm_v1.csv
- NEURON_value_action_variance_partition_v1.csv
- NEURON_value_action_timecourse_v2.csv
- NEURON_value_action_UR_control_v2.csv
- NEURON_value_action_DML_summary_v1.csv
