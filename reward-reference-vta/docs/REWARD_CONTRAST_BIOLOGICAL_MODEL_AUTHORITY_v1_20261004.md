# Reward Contrast Biological Model Authority v1 — 2026-10-04

## Central biological question

The useful question is no longer simply whether reward contrast exists or which algorithm predicts dopamine best.

The biological question is:

**What determines whether past reward experience becomes a reference, whether that reference is read out during the next reward, and whether the neural comparison is converted into behavior?**

The current data support a layered architecture rather than one universal contrast model.

## 1. Working biological architecture

### Layer 1 — internal state transforms current utility

Let physical reward be q and physiological/internal state be H:

U_t = f(q_t, H_t)

H can include hunger/satiety, illness, GLP-1/semaglutide state, hydration, sodium need, etc.

Current evidence shows that hunger, LiCl and semaglutide alter current reward value/readout. These data establish modulation of **current utility U**, but they do not yet identify how those internal states alter formation or persistence of the history reference R, because reward identity does not vary sufficiently within those fixed-condition sessions.

Therefore homeostatic modulation of U must not be equated with reward-history contrast.

### Layer 2 — experienced samples update a reward reference

The most parsimonious current reference rule is:

R_(t+1) = R_t + alpha * (U_t - R_t)

Updates occur at experienced reward samples/licks, not simply as a function of elapsed clock time.

Direct-history evidence comes from three tasks:

1. Natural 100E/20E reward-quality history.
2. QE independent reward/devaluation history.
3. Interleaved VTA stimulation ON/OFF history.

Across their common alpha grid, alpha=.20 is the maximin shared setting:
- Natural retains 91.14% of its own maximum effect.
- QE retains 97.86%.
- VTA stimulation retains 97.52%.
- Mean retained fraction = 95.51%.

Task-specific optima differ (approximately Natural .15, stimulation .10, QE .30). Thus alpha=.20 should be interpreted as a **shared broad recency regime**, not an identical biological learning constant.

Clock-versus-sampling controls strengthen this interpretation: passive clock terms over 5–640 s do not explain the Natural history effect, whereas sampling dose after reward access does, and cumulative lick/duration sampling survives permutation controls.

Preferred wording:

> The reference is constructed through reward experience rather than passive time alone.

### Layer 3 — current utility is compared with the sampled reference

Natural sustained DA provides direct decomposition because U and R can be entered separately.

Standardized coefficients:
- current utility U: beta = +0.762, P=.00216;
- history reference R: beta = -0.721, P=.0282.

The near-opposite signs are the expected geometry of a comparator.

A direct contrast-versus-sum decomposition reaches the same conclusion:
- sustained contrast coefficient after sum control: beta=+1.638, P=.000693;
- sum coefficient: beta=-.391, P=.244.

Thus the main sustained signal is better described as **relative value / comparison** than as absolute total value.

### Layer 4 — comparator output has context-dependent gain

A useful decomposition is:

G_t = max(U_t - R_t, 0)

L_t = max(R_t - U_t, 0)

G is the positive relative-value side and L is the negative/reward-loss side.

Independent positive-side components are detectable in all three direct-history datasets:
- Natural sustained DA: G unique delta R2=.02922, conditional P=.00370.
- QE AUC: G delta R2=.08818, P=.00160.
- QE AUC/s: G delta R2=.01964, P=.02330.
- Stim13 AUC/s: G delta R2=.001275, P=.00470.

The negative component is not independently significant in those pooled tests:
- Natural L P=.324.
- QE L P>.25.
- Stim13 L P=.666.

However, this does **not** establish a universal biological inequality G >> L. Formal current-reward × reference interactions show:
- Natural: P=.216 — asymmetry not established.
- QE: P=.000527 — strong high/EE-side asymmetry.
- Stim13 after full local/slow/future controls: P=.197 — asymmetry not established.

Animal×current-condition standardized slopes likewise show that Natural directionality is not uniformly positive-side dominated.

Therefore the correct model is:

**shared reference formation + context-dependent comparator gain**

rather than a universally dominant positive comparator channel.

### Layer 5 — neural reference expression and behavioral expression can dissociate

Interleaved VTA stimulation provides the clearest example.

At frozen alpha=.20:
- prior stimulation history predicts current AUC/s;
- circular-shift P=.00010;
- past beyond full local/slow controls and future reference gives unique delta R2=.002524, conditional P=5e-5;
- 10/13 animals show the expected Rpast direction after local controls, Wilcoxon P=.0215.

But the same history state does not reliably predict feeding duration:
- past P=.742;
- joint past P=.389.

Held-animal prediction is also incomplete:
- 8/13 animals improve;
- P=.188.

Thus:

**reference memory can be neurally expressed without producing detectable gross behavioral contrast.**

This is central to explaining why some reward classes may appear to lack contrast.

## 2. Temporal biology: not a static RPE label

Natural reward history has a strong temporal reorganization.

Contrast axis:
- pre-bout: beta=-.485, P=.000235;
- early 0–2 s: beta=.294, P=.603;
- sustained 2–5 s: beta=+1.752, P=.00893;
- sustained-minus-early: beta=+1.458, P=9.0e-8;
- sustained-minus-pre: beta=+2.238, P=.00259.

Sum axis:
- pre, early, sustained and their temporal differences are non-significant in the corresponding analysis.

The sustained signed state also contains information beyond unsigned salience:
- signed beyond unsigned: delta R2=.01867, P=.03279;
- unsigned beyond signed: delta R2=.00320, P=.375.

Biological interpretation:

1. Before consumption, reference state is reflected in anticipatory/baseline organization.
2. Reward onset itself contains little robust history-dependent signed signal.
3. During ongoing consumption, current reward becomes evaluated relative to the stored reference.

This resembles the conceptual progression in Schultz's two-component dopamine framework from initial detection toward later valuation, but our signal is seconds-long during consummatory behavior. It should therefore **not** be called a canonical subsecond TD-RPE without qualification.

Preferred wording:

**consummatory reference-dependent utility / valuation signal**

or

**sampled-reference relative-value signal**.

## 3. Competing biological models

### 3.1 Sampled reward reference

Mechanism: experienced reward samples update a compact recency-weighted reference.

Why favored:
- three direct-history contexts;
- frozen cross-task transfer;
- past > future controls;
- survives local history, session progress, cumulative sampling, belief/HMM and reward-rate alternatives;
- common broad recency regime.

Status: **SUPPORTED CORE**.

### 3.2 Tobler adaptive gain / reward-range normalization

Biological idea: dopamine rescales prediction error by variance or range of expected reward.

Current data:
- fixed TD/RW state retains unique information beyond adaptive gain: delta R2=.01563, P=.0464;
- adaptive gain adds little beyond TD/RW: delta R2=.000467, P=.698.

Interpretation: range normalization may coexist with reference coding, but is not sufficient.

Decisive test: manipulate reward variance while holding mean reward and reference history fixed.

### 3.3 Pearce-Hall adaptive learning rate

Biological idea: surprise controls how rapidly new experience updates the reference.

Current data:
- no robust held-animal advantage;
- no unique information beyond fixed TD/RW (competitor unique P=.459).

Interpretation: adaptive alpha is not required by existing data.

### 3.4 Multi-timescale reference

Biological idea: fast and slow memories jointly define expected reward.

Current data:
- a Masset-like dual-timescale state does not add reliable unique information beyond fixed TD/RW (P=.171).

This is not a strong rejection because present sessions may not span enough delays to identify a very slow component.

### 3.5 Bayesian belief / hidden-state inference

Biological idea: the animal infers a hidden environmental state rather than directly integrating experienced reward samples.

Natural data:
- FullHistory beyond HMM: delta R2=.02662, P=.0090;
- HMM beyond FullHistory: delta R2=.00784, P=.138;
- FullHistory beyond another belief model: delta R2=.02541, P=.0124;
- belief beyond FullHistory: delta R2=.000465, P=.726.

Interpretation: hidden-state inference is plausible under ambiguity, but does not absorb the sampled reward reference here.

### 3.6 Niv average reward rate / tonic opportunity cost

Biological idea: long-run average reward rate regulates response vigor.

Current data:
- FullHistory beyond reward rate: delta R2=.02565, P=.0122;
- reward rate beyond FullHistory: delta R2=.000432, P=.722.

Interpretation: average reward rate is better treated as a separate motivational/vigor variable, not the event-specific comparator.

### 3.7 Homeostatic reinforcement learning

Biological idea: internal physiological state changes the utility of the same physical outcome.

This naturally motivates:

U = f(q, H)

Current data strongly motivate this layer, but cannot yet distinguish whether H changes:
- current utility U;
- reference update rate alpha;
- stored reference R;
- comparator gain;
- or DA-to-behavior coupling.

This is one of the highest-value next experiments.

### 3.8 Distributional dopamine coding

Biological idea: different dopamine neurons learn different expectiles/distributional values.

Bulk GRAB-DA cannot adjudicate this. A population average can hide negative-RPE neurons, different reversal points and asymmetric positive/negative scaling.

Therefore null bulk negative-channel results do not prove absence of negative PE at the single-neuron level.

## 4. Relationship to classical successive negative contrast

Classical rat cSNC is not equivalent to the VTA signal identified here.

Canonical cSNC is a behavioral reward-loss phenomenon in which consumption after a high-to-low reward shift falls below an always-low control.

The classical circuit literature is especially informative because it separates memory from comparison/expression.

### Gustatory thalamus

GT lesions abolish consummatory SNC. Critically, the deficit remains across retention intervals from 7.5 min to 24 h, arguing against a simple inability to retain the previous reward memory.

GT lesions can abolish consummatory SNC while sparing instrumental SNC, supporting multiple comparison mechanisms with different neural substrates.

### Insular cortex

Insular lesions abolish consummatory SNC, consistent with a role in relative reward comparison/representation rather than raw reward responsiveness alone.

### Basolateral and central amygdala

BLA lesion work supports a role in reward comparison during reward loss.

Recent c-Fos work shows that amygdala recruitment depends on sufficiently large reward disparity: a 32-to-2% sucrose downshift producing cSNC recruits specific amygdala subregions, whereas a smaller disparity causing consumption suppression without cSNC does not show the same activation pattern.

Thus behavioral cSNC contains a comparison/affective circuit layer beyond merely storing reward history.

### Nucleus accumbens dopamine

Classical SNC studies have reported attenuated NAc dopamine efflux after reward downshift, consistent with relative incentive valuation.

This is broadly compatible with a reference-dependent dopamine signal but differs from our experiments in species, measurement timescale and task structure.

## 5. Unified model

The most defensible architecture is:

physiological state H

→ current utility U = f(q,H)

→ experienced reward samples

→ reference R_(t+1) = R_t + alpha(U_t-R_t)

→ relative comparator

→ g_plus(context) × [U-R]+ and g_minus(context) × [R-U]+

→ VTA/NAc dopamine plus comparison/affect circuits

→ learning, persistence, consummatory behavior

The key feature is:

**reference formation can generalize while output gain and behavioral expression vary by reward class and circuit.**

This naturally explains:
- shared alpha regime across Natural, QE and stimulation;
- different DA expression timing in Natural versus QE;
- strong neural stimulation reference with no feeding-duration effect;
- physiological state changing current value without yet proving a new reference;
- classical cSNC requiring additional comparison/affective circuitry.

## 6. What the current paper can claim

Strong claims supported now:

1. Reward experience forms a sampled, history-dependent reference.
2. This reference is not reducible to passive time, generic serial persistence, reward rate, belief/HMM, or unsigned salience.
3. A common broad recency regime transfers across natural reward quality, independent reward/devaluation history and direct circuit reward.
4. During sustained consumption, VTA dopamine represents current utility relative to this reference.
5. Neural reference expression can occur without detectable gross behavioral contrast.
6. Comparator gain is context dependent.

Claims to avoid:

1. Do not say alpha=.20 is a universal biological learning rate.
2. Do not say every physiological reward uses the same reference rule.
3. Do not say bulk VTA DA lacks negative RPE neurons.
4. Do not equate sustained 2–5 s GRAB-DA with canonical subsecond TD-RPE.
5. Do not claim universal positive-side dominance; formal asymmetry is robust in QE but not Natural or fully controlled stimulation.
6. Do not claim hunger/LiCl/semaglutide change reference persistence until reward identity is varied within those states.

## 7. Highest-value next experiments

### Priority 1 — homeostatic state × interleaved reward identity

Within the same animal/session, interleave two reward qualities under:
- hungry vs sated;
- PBS vs semaglutide;
- potentially thirst vs water-sated.

Estimate independently:
- utility shift U;
- reference alpha;
- stored R;
- positive and negative comparator gain;
- DA-to-behavior coupling.

This directly tests whether physiological state alters reference formation or only current utility/readout.

### Priority 2 — delay × sample-count factorial

Orthogonalize:
- elapsed time since previous reward;
- number of reward samples;
- value of those samples.

Prediction: if R is sample-updated, sample number/value should dominate elapsed time after matching.

### Priority 3 — balanced upshift/downshift design

Create matched positive and negative mismatch magnitudes with equal current-reward sampling and matched variance.

This is required to formally identify g_plus versus g_minus without current-reward confounding.

### Priority 4 — circuit dissociation

Simultaneously record VTA DA while manipulating or recording:
- BLA;
- insula;
- gustatory thalamus;
- possibly CeA/ACC depending endpoint.

Prediction: VTA will carry reference-dependent utility, whereas classical reward-loss regions will be especially important for converting negative comparison into behavioral suppression/affective output.

### Priority 5 — make stimulation reference behavioral

The stimulation dataset already has neural R with no feeding-duration contrast.

Use it as a causal testbed to alter downstream DA/NAc action during high-reference versus low-reference current bouts and ask whether a latent neural reference can be converted into persistence/choice.

### Priority 6 — single-cell dopamine test

Test whether population-level asymmetry is produced by heterogeneous positive/negative PE neurons, distributional expectile coding or projection-specific dopamine populations.

## 8. Manuscript-level summary

> Reward value during consumption is not determined by the current outcome alone. Recent reward samples build a persistent reference state that generalizes across natural reward quality, reward devaluation, and direct circuit reward. During ongoing consumption, current utility and this reference exert opposing influences on dopamine, producing a relative-value signal whose temporal expression and directional gain depend on reward context. Crucially, stimulation history can alter subsequent dopamine without altering gross feeding persistence, demonstrating that formation of a reward reference, its neural readout, and its behavioral expression are separable processes.

A stronger conceptual final sentence:

> Reward contrast is therefore not a unitary response to reward loss, but the behavioral expression of a multi-stage computation in which experienced outcomes establish a reference, current utility is evaluated relative to that reference, and context-specific circuits determine whether the comparison is expressed in dopamine, behavior, or both.

## 9. Current authority files

Core:
- data/current/NEURON_biological_model_adjudication_v1.csv
- data/current/NEURON_three_context_reference_evidence_v1.csv
- data/current/NEURON_three_task_shared_recency_summary_v1.csv
- data/current/NEURON_reference_direction_asymmetry_adjudication_v1.csv
- data/current/NEURON_positive_negative_reference_channels_v1.csv
- data/current/NEURON_reward_reference_two_channel_v1.csv
- data/current/NEURON_reward_reference_two_channel_crosscontext_v1.csv
- data/current/NEURON_positive_side_robustness_summary_v1.csv
- data/current/standardized_U_R_alloutcomes.csv
- data/current/contrast_vs_sum_decomposition_alpha02_v2.csv
- data/current/NEURON_temporal_contrast_vs_sum_interactions_v3.csv

Figure:
- figures/neuron_working/NEURON_biological_reward_reference_model_v1.png/pdf/svg

Detailed stimulation authority:
- docs/REWARD_CONTRAST_STIM_LICKLEVEL_AUTHORITY_v1_20261004.md

Persistence/expression authority:
- docs/REWARD_CONTRAST_PERSISTENCE_EXPRESSION_AUTHORITY_v1_20261003.md

## 10. Literature anchors

Dopamine/reference:
- Tobler PN, Fiorillo CD, Schultz W. Science 2005. DOI 10.1126/science.1105370.
- Schultz W. Nat Rev Neurosci 2016. DOI 10.1038/nrn.2015.26.
- Niv Y et al. Psychopharmacology 2007. DOI 10.1007/s00213-006-0502-4.
- Keramati M, Gutkin B. eLife 2014. DOI 10.7554/eLife.04811.
- Starkweather CK et al. Neuron 2018. DOI 10.1016/j.neuron.2018.03.036.
- Dabney W et al. Nature 2020. DOI 10.1038/s41586-019-1924-6.

Successive negative contrast / circuits:
- Reilly S, Trifunovic R. Behav Neurosci 1999. PMID 10636302.
- Reilly S, Trifunovic R. Behav Neurosci 2003. DOI 10.1037/0735-7044.117.3.606.
- Lin JY, Roman C, Reilly S. Behav Neurosci 2009. PMID 19634939.
- Morón I et al. 2017. PMID 28511980.
- Genn RF, Ahn S, Phillips AG. Behav Neurosci 2004. DOI 10.1037/0735-7044.118.4.869.
- Arjol D et al. Neurobiol Learn Mem 2024. DOI 10.1016/j.nlm.2024.107942.


## 11. Neural-to-behavior pathway: shared state is supported; mediation is not yet proven

A useful cross-modal result is that alpha=.20 was selected using held-animal dopamine prediction alone and only then frozen for independent behavioral tests.

The DA-selected state predicts:
- log-duration behavior: beta=.476, P=.00566;
- termination hazard: beta=-.780, OR=.459, P=.000180.

Thus the same reward-history timescale transfers from a neural endpoint to independent behavioral endpoints without tuning alpha on behavior.

This supports a **shared reference axis** used across modalities.

However, current data should not be described as proving that dopamine mediates the behavioral effect.

Reasons:
1. In the Natural hazard model containing state and dopamine together, neither term provides a clean independent mediation signature under the restricted common sample.
2. In interleaved VTA stimulation, reward-history reference is robustly expressed in dopamine but does not reliably alter feeding duration.
3. Therefore neural reference expression is not sufficient for gross behavioral expression.

Current preferred architecture:

reference R
→ VTA dopamine readout

and, in parallel,

reference R
→ behavioral comparison/expression circuits

with causal coupling between these branches still open.

The decisive experiment is to perturb sustained VTA dopamine during bouts matched for pre-existing R. If behavior changes while R is held fixed, this supports a mediating/gating role for dopamine. If behavior retains its reference dependence despite loss of the DA signal, the two outputs are more parallel.

Experiment prediction authority:
- data/current/NEURON_biological_model_experiment_predictions_v1.csv


## 12. Sustained dopamine is multiplexed: reference/value plus consummatory action

A major alternative explanation for the sustained 2–5 s dopamine effect is that reward-history conditions change how much the animal licks, and dopamine merely follows action output.

This alternative is real rather than hypothetical. Whole-bout lick count and duration covary strongly with RWstate and with sustained dopamine. However, temporal ordering matters: final bout duration and whole-bout lick count contain behavior occurring after the 2–5 s dopamine window and therefore can be downstream of value and dopamine. They are conservative sensitivity controls rather than clean upstream confounds.

The preferred causal nuisance is early action before the sustained window.

A joint clustered model containing RWstate, 0–2 s lick count and concurrent 2–5 s lick count finds independent contributions from all three:
- RWstate beta=2.283, SE=.728, P=.00172;
- early 0–2 s licks beta=.376, SE=.157, P=.0165;
- concurrent 2–5 s licks beta=.554, SE=.158, P=.000457.

Reference information also survives flexible action-control models:
- after 0–2 s action control: RW delta R2=.0543, P=.00316;
- after 0–2 plus 2–5 s action control: RW delta R2=.0489, P=.00254;
- after whole-bout lick count, lick rate and duration over-control: RW delta R2=.0330, P=.00495.

Exact discrete action strata provide a nonparametric sensitivity analysis. Holding animal, current reward identity and exact 0–2 s lick count fixed leaves 166 bouts in 39 strata; RWstate remains associated with sustained dopamine (beta=2.216, P=.00609). Matching both 0–2 s and 2–5 s counts leaves 104 bouts; the RW point estimate remains similar (beta=2.128) but uncertainty increases and the test is no longer significant (P=.168). Fine-bin matching leaves 80 bouts with beta=2.527, P=.190.

Thus the current data do not support either a pure-value or pure-action interpretation.

Preferred wording:

**Sustained VTA dopamine contains a reference-dependent relative-value component together with an independent consummatory-action component.**

The reference-dependent component cannot be reduced to differences in early licking. Concurrent action also carries independent dopamine information. Exact matching through the neural window becomes underpowered and therefore should not be described as definitive proof of action independence.

Detailed authority:
- docs/REWARD_CONTRAST_VALUE_VS_ACTION_AUTHORITY_v1_20261004.md
- data/current/NEURON_value_vs_action_joint_coefficients_v1.csv
- data/current/NEURON_value_vs_action_exact_strata_v1.csv
- figures/neuron_working/NEURON_value_vs_action_adjudication_v1.png
