# SOE latest analysis master v23 - 2026-10-04

This is an analysis/results authority, NOT a manuscript draft and NOT a GitHub page.

## Scope correction
The earlier phenotype/behavioral layers remain preserved in SOE_MASTER_RESULTS_INVENTORY_v1_20261002.md. This v2 focuses on the current analysis layer beginning with the computational model hierarchy and then integrates dopamine, Visual Block, JAWS, and generalization.

Do not delete previously verified results when newer model analyses are added. New analyses should extend the result graph rather than replace older positive evidence.


## Manuscript-level claim authority

The unique manuscript-level claim graph is now:
- docs/SOE_MASTER_RESULT_GRAPH_v1_20261003.md
- results/SOE_MASTER_RESULT_GRAPH_v1_20261003.csv
- results/SOE_MASTER_RESULT_GRAPH_gap_audit_v1.csv
- results/SOE_MASTER_RESULT_GRAPH_module_summary_v1.csv

It contains eight modules and 28 manuscript-level claims. CORE blocker count is zero.
New analyses should only add or strengthen these nodes unless they genuinely change the core biological interpretation.

## Audited model/comparison authority — 2026-10-03

The first three computational sections are now backed by machine-recomputed canonical tables rather than manual transcription.

### SOE same-27 model comparison
Authority:
- results/SLM_behavior_model_comparison_canonical_v5.csv
- results/SLM_model_comparison_numeric_audit_v3.csv
- results/SLM_classical_paired_recompute_audit_v3.csv
- docs/SLM_MODEL_COMPARISON_NUMERIC_AUDIT_v4_20261003.md

Audit:
- 27 learner animals; 68,624 held-out events.
- weighted Brier maximum reconstruction error 8.33e-17.
- weighted log-loss maximum reconstruction error 1.11e-16.
- paired rank-biserial reconstruction error 0.
- paired exact-P reconstruction error 0.

### Model × Evidence
Authority:
- results/SLM_MODEL_X_EVIDENCE_AUDITED_v4.csv
- docs/SLM_MODEL_X_EVIDENCE_AUDIT_v4_20261003.md

This table explicitly separates:
behavior; Early DA; Middle raw association; Middle conditional uniqueness; Post DA; JAWS; model recovery; and generative validation.
Untested cells remain NA.

### Cross-task/species
Authority:
- results/SLM_cross_task_model_comparison_canonical_v4.csv
- results/SLM_cross_task_neural_activity_comparison_v3.csv
- results/SLM_cross_task_contract_audit_v4.csv
- results/SLM_CROSS_TASK_SPECIES_CONVERGENCE_SUMMARY_v2.csv
- docs/SLM_CROSS_TASK_MODEL_COMPARISON_v4_20261003.md
- docs/SLM_CROSS_TASK_SPECIES_CONVERGENCE_SUMMARY_v1_20261003.md

Only models sharing a contract_id are ranked directly.

### Virtual Agent
Authority:
- results/SLM_virtual_agent_existing_rollouts_v1.csv
- results/SLM_virtual_agent_gap_matrix_v1.csv
- results/SLM_virtual_agent_formal_mapping_v1.csv
- results/SLM_virtual_agent_q_learner27_global_v1.csv
- results/SLM_virtual_agent_q_learner27_paired_v1.csv
- docs/SLM_VIRTUAL_AGENT_ALIGNMENT_AUDIT_v1_20261003.md
- docs/SLM_VIRTUAL_AGENT_Q_ALLFOLDS_AUDIT_v2_20261003.md

Legacy closed-loop simulator tests were rerun: 5/5 passed.
The old simulator/environment should be reused rather than rewritten.

A reconstructed 61-feature conditional agent adds q_diff to current/core + medium memory + run/time + feature-policy + four outcome-belief coordinates + slow day prior.
On the exact 27 current learners:
- trajectory r .80545 vs .80345 for old full-multiscale;
- kernel r .51620 vs .51268;
- lag1 r .33439 vs .26448.
Animal-level paired improvements are directionally positive but not significant (trajectory-r r_rb=.190, P=.400; kernel-r .265, P=.239; lag1-r .164, P=.470).
Therefore q_diff is retained as a valid current-SLM coordinate but is NOT itself promoted as a decisive generative improvement.
The next high-value step is intervention/state alignment, not further scalar feature stacking.

## Metric contract
Paired effects: rank-biserial r_rb in [-1,1] + paired/exact P + n + directional counts.
Independent groups: Cliff delta.
Correlations: Spearman rho.
Predictive models: Brier, Brier skill, AUC, log loss; continuous targets additionally MSE/RMSE/R2 when appropriate.
Raw latent units stay in source tables. Never multiply small latent values merely to make them visually larger.

## Layer 3.9. Formal Social Learning Model (SLM) specification

SLM is the mechanistic model family, not a single leaderboard predictor.

Core computation:
current social state -> multiscale memory / social belief -> sampling policy -> action-policy error -> outcome -> critic RPE + belief update.

For event t, the causal information set F_t^- contains only pre-action information. Let x_t be current social/environmental state and a_t in {0,1} the sampling action.

Multiscale memory:
m_{t+1}^{(k)} = gamma_k m_t^{(k)} + phi(a_t,o_t).

Social-reward belief for contingency c:
B_{t+1}^c = B_t^c + alpha_B g_t^c [r_t-B_t^c].

Actor / sampling policy:
eta_t = beta_0 + beta_x^T x_t + beta_m^T m_t + beta_B^T B_t,
pi_t = sigmoid(eta_t).

Action-policy error:
APE_t = a_t-pi_t (signed) or its pre-specified magnitude/surprise transform.

Critic:
delta_t^R = r_t-Q_t(a_t,s_t),
with feature-based value update w_{a_t,t+1}=w_{a_t,t}+alpha_Q delta_t^R x_t.

The primary model-family hierarchy is:
Current-only -> +short history -> +multiscale state -> +Actor/APE -> +Critic/RPE -> +social belief -> Full SLM.
SLM+choice persistence is the parsimonious behavioral extension. TinyRNN and History-MLP are capacity ceilings, not the mechanistic definition.

Neural adjudication is component matched:
- early Observation: policy pi_t;
- middle Observation: APE_t and learner-linked APE coupling;
- post-outcome: RPE_t and belief update DeltaB_t.

Full equation/transport authority: docs/SOE_SLM_FORMAL_SPEC_v1_20261003.md.
Model-family registry: results/SOE_SLM_MODEL_FAMILY_v1.csv.

## Layer 4. Behavioral computation: baseline ladder -> SLM -> strong alternatives

### 4.1 Baseline ladder
Current 27-learner / 68,624-event held-animal contract:
- Constant prevalence: Brier .256073, AUC .377565.
- Clock only: .244924, .581658.
- Previous choice only: .228180, .613424.
- Current linear: .194191, .771429.
- Current nonlinear: .185812, .790933.
- SLM full: .170824, .823320.

Relative to SLM, these simple baselines have 8-33% larger Brier error.

Additional fixed-model baselines from the earlier model zoo:
- LCNE asymmetric-Q persistent state: Brier .184082, AUC .794607.
- UCL dual controller: .189423, .787684.
- LCNE asymmetric-Q daily state: .190892, .778420.
- 5HT uncertainty state: .193067, .773175.
- 5HT uncertainty global: .196036, .766472.
- Cell deep-RL shallow/deep heterogeneous: .212276/.213134.
- UCL RPE-only: .227295.

Role: these models establish that SLM is substantially stronger than simple state/time heuristics, classical low-dimensional RL, and several biologically motivated alternative controllers. They are baseline families, not a separate negative-results story.

Current table: social_learning_unification_20261002/SOE_baseline_ladder_v2.csv.
### 4.2 Classical RL comparison
Restricted-input classical baselines include RW, WSLS, Q-active, Q-all, asymmetric Q, forgetting-Q, choice kernel, and Q+choice-kernel.
Under this restricted contract SLM beats all eight in 27/27 animals for Brier, paired r_rb=+1, P=1.49e-8.

Important: this demonstrates superiority over low-dimensional RL but is not input-matched because SLM has richer current-state information.

### 4.3 Strong input-matched / capacity alternatives
- Current + choice kernel: Brier .166401, AUC .832245.
- TinyRNN h3: .168031, .828605.
- Current + full-history MLP: .164749, .835124.
- History MLP + formal-all: .163722, .837365.

These should NOT be hidden. They demonstrate behavioral computational equifinality and motivate neural adjudication.

### 4.4 Parsimonious two-branch head
SLM + choice-kernel held-animal OOF stack:
- Brier .165411.
- AUC .834084.
- log loss .499881.
- beats SLM 26/27, r_rb=.942, P=8.20e-7.
- beats CK 20/27, r_rb=.667, P=.00169.
- beats TinyRNN h3 23/27, r_rb=.862, P=1.59e-5.
- indistinguishable from full-history MLP, r_rb=-.079, P=.732.
- recovers 96.9% of Current->full-history-MLP improvement and 92.4% of Current->best-history-model improvement.

Interpretation:
Most behaviorally useful history can be represented by structured social learning plus generic choice persistence. Black-box models remain a capacity ceiling, not the mechanistic explanation.
## 4.5 Recovered pre-SLM multi-timescale results: integrate, do not create a separate old story
These results strengthen the current SLM architecture because they establish that SOE behavior contains multiple timescales before any SLM interpretation is imposed.

Recovered historical analysis:
- current social/food geometry is strongly informative.
- approximately 20-event observation/action history adds substantial held-animal predictive information; earlier full policy AUC .884, NLL .425, history DeltaNLL +.0348.
- food-geometry ablation cost +.0422 NLL in that contract.
- selected memory gamma .95-.97 corresponds roughly to 20-33 events / 4.5-7.5 min.
- chronological day order ranked 1/501 against within-animal day shuffles, empirical P=.001996.
- a retained cross-day prior improved 29/40 animals, paired P=.0125, with its contribution concentrated near the beginning of a new session and fading later.

How this now fits the current model:
1. fast outcome-conditioned action changes motivate an actor/policy-error component;
2. multi-event memory motivates persistent state/history;
3. slower Q/belief accumulation supplies reward-credit memory;
4. transient cross-day state motivates a session prior rather than a completely separate algorithm.

Therefore these old analyses should appear as evidence for the model's temporal architecture, not as a competing pre-SLM narrative.

Simpler RW, uncertainty/reliability, and single-exponential eligibility variants should be folded into the baseline ladder/model comparison. Do not create a separate section whose main message is that they 'failed'.
## 4.6 Learning stage
Richer history becomes more useful later:
- TinyRNN h3 D10+ vs D1-4 gain: r_rb=.434, P=.0491.
- History MLP + formal-all: r_rb=.508, P=.0200.
- formal + external ensemble: r_rb=.534, P=.0140.

This is compatible with the multi-timescale result: the need for flexible history/state becomes stronger as animals acquire the social contingency.

Do not force one isolated history component to explain the effect; action-history/full-history/nonlinearity components individually are weaker than the full late-history pattern.
## 4.7 Social information has adaptive decision value

Define held-out social information value at event t as:
SV_t = log p(actual action | self state + social state) - log p(actual action | self state).

This uses held-animal OOF predictions from the state-family ablation rather than in-sample fits.

Overall SOE social information value:
- full social state vs observer-only: 22/27 animals positive; median +.00365 nats/decision; r_rb=.725; one-sided P=.000268.
- demonstrator component: 22/27; median +.00318; r_rb=.693; P=.000510.
- dyadic component: 20/27; median +.00167; r_rb=.460; P=.0181.

The value is learning dependent:
- late < early in 20/27 animals;
- median late-minus-early = -.00378 nats/decision;
- r_rb=-.619;
- P=.00194.

The value is also strongly behavioral-state dependent. Social information is more useful when the observer is far from its own spout than when it is near:
- demonstrator not feeding: 24/27, r_rb=.905, P=1.88e-6.
- demonstrator feeding: 22/27, r_rb=.593, P=.00297.

At fixed far-from-spout state, demonstrator feeding vs not feeding is not by itself reliable (P=.235). Thus the correct principle is not that one demonstrator event is always valuable; social evidence contributes selectively when the observer's current state leaves room for external information to alter policy.

SOE does not show a simple animal-level high-uncertainty > low-uncertainty rule (13/27; P=.411). Do not force uncertainty as the universal gate.

A same-contract cooperative-foraging analysis recovers a related adaptive-information principle, but its inferential scope is one public demo dyad (YC069):
- Follower social value rises with self-policy entropy at the step level (rho=.129).
- high-vs-low uncertainty follower social value increases by +.0659 nats/decision across held-out trajectories.
- the Follower-vs-Leader uncertainty-gating contrast is +.1744 nats/decision within YC069.
These trajectory-level P values quantify reproducibility within that dyad and must not be presented as population-level inference.

The published multi-animal MAIRL analysis provides independent population-level corroboration of the role asymmetry:
- n=6 animals per role.
- partner distance is a significant model component in 6/6 followers versus 3/6 leaders.
- partner angle is significant in 6/6 followers versus 2/6 leaders.
- proximal partner-distance value is higher in followers than leaders (P=7.7e-6).

The same social-information-value definition can be compared across tasks while keeping the validation unit explicit:
- SOE full social state: animal-level r_rb=.725.
- rat observational maze demonstrator: rat-level r_rb=.867, 4/5 positive, P=.0625 for log predictive-probability gain; moving-object control r_rb=0.
- cooperative follower: within-YC069 held-out-trajectory r_rb=.942; leader r_rb=.399.
- Aeon experiment-level current partner: 4/5 positive, r_rb=.467, P=.219; recent partner-history increment: 5/5, r_rb=1.0, P=.03125.

Thus independent tasks differ in useful source and timescale. The conserved principle is adaptive social-information use; neither uncertainty nor any one history timescale is a universal gate.

Authority:
- docs/SOE_ADAPTIVE_SOCIAL_INFORMATION_VALUE_v2_20261003.md
- docs/SLM_EXTERNAL_MULTIDATASET_AUTHORITY_v5_20261003.md
- results/SOE_social_information_value_state_learning_v1.csv
- results/SOE_adaptive_social_information_bridge_v1.csv
- results/rat_observational_maze_social_value_animal_v3.csv
- results/SOE_cross_task_social_information_value_v2.csv
- results/SOE_cross_task_social_information_value_units_v2.csv
- figures/SOE_adaptive_social_information_value_v2.png/pdf/svg
- figures/SOE_cross_task_social_information_value_v2.png/pdf/svg

## Layer 4B. Model identifiability and generative validation

Behavioral closeness among SLM-related algorithms does not imply intrinsic non-identifiability.

### 4B.1 Primary six-family mouse-matched recovery
A completed synthetic recovery uses the real SOE schedule, generates actions under each candidate mechanism, refits all candidate models on synthetic training animals, and evaluates them on held-out synthetic animals.

Six implementations are included: RW, Q-active, Q-allreward, adaptive-Q, Actor-Critic, and outcome-belief.

Overall exact model recovery is 35/36 = 97.2%.
Actor-Critic, outcome-belief, Q-active, Q-allreward and adaptive-Q are each recovered 6/6. RW is recovered 5/6, with one replicate confused with adaptive-Q.

Median winner NLL margins:
- Actor-Critic: 1.87e-4
- outcome-belief: 7.13e-4
- Q-allreward: 1.15e-4
- Q-active: 7.9e-5
- adaptive-Q: 5.1e-5
- RW: 7e-6

The small margins are informative: several algorithms are behaviorally close, but remain recoverable under realistic SOE task statistics.

### 4B.2 Focused conditional recovery
A stricter 27-learner conditional replay with recursively generated observer choices/action histories gives 59/60 exact recovery (98.3%): policy 20/20, Feature-Q 20/20, and Actor-Critic 19/20; the single Actor-Critic miss is classified as Feature-Q.

### 4B.3 Generative validation
Conditional virtual-mouse simulation reproduces broad learning trajectories:
- short model trajectory r=.782
- memory model r=.788
- core model r=.783
Outcome-conditioned lag-1 switching preserves the principal signs.

Interpretation:
real-data behavioral similarity should be written as computational equifinality, not failure of model identifiability. Synthetic recovery shows that the algorithms can in principle be distinguished under the task; VTA temporal structure and causal perturbations determine which latent computation is biologically expressed.

Boundary:
this establishes algorithm/model recovery, not complete numerical parameter recovery. Individual learning-rate, gamma and belief-alpha parameters should not be claimed as identifiable until dedicated parameter recovery is completed.

Authority:
- docs/SLM_IDENTIFIABILITY_GENERATIVITY_v2_20261003.md
- results/SOE_SLM_mousematched_model_recovery_v1.csv
- results/SOE_SLM_mousematched_recovery_confusion_v1.csv
- results/SOE_SLM_focused_conditional_recovery_v1.csv
- results/SOE_SLM_generative_summary_v1.csv
- results/SOE_SLM_lag1_generative_fidelity_v1.csv


### 4B.4 Virtual Agent now separates social sampling from downstream feeding conversion
A first intervention-level Virtual Block sensitivity ablates current visual/social input while preserving observer-intrinsic state, history, memory, belief, prior and Q.

Across the exact 27 learner animals, this manipulation does NOT reduce observation probability:
- observation-rate VB-control median +.00571; 17/27 positive; two-sided P=.106.
- policy-probability VB-control median +.00580; 17/27 positive; r_rb=.439; two-sided P=.0463.
- absolute APE increases in 25/27; r_rb=.963; P=2.83e-7 two-sided.

This is not a failed simulation of the real phenotype because real Visual Block preserves gross observation amount. The principal real phenotype is loss of observation-to-feeding conversion and SRI, not disappearance of observation itself.

Recovered real Visual Block downstream behavior:
- future active feeding within 60 s: reference .570 vs block .359; 24/25 decrease; P=5.96e-7.
- restricting to observation-source events: .571 vs .361; 22/25 decrease; P=5.25e-6.

An exact-27 held-animal audit of the pre-existing future-feeding hazard model identifies the computational coordinate most relevant to this downstream conversion:
- adding belief state to the baseline improves future-60-s feeding prediction in 22/27 learners; median Brier gain +.001319; r_rb=.545; two-sided P=.01208.
- full belief+policy model: 22/27; r_rb=.513; P=.01866.
- policy alone does not improve the downstream feeding target: r_rb=-.249; P=.269.

Interpretation:
the Virtual Mouse should be explicitly two-stage.
Stage 1 generates social sampling/observation policy.
Stage 2 converts sampled social information into downstream feeding using a belief-dependent head.
This architecture directly mirrors the real Visual Block dissociation: observation persists while the learned social-information-to-feeding conversion collapses.

Authority:
- results/SLM_virtual_visualblock_allfolds_summary_v1.csv
- results/SLM_virtual_visualblock_allfolds_per_animal_v1.csv
- docs/SLM_VIRTUAL_VISUALBLOCK_AUDIT_v1_20261003.md
- results/SLM_future_feeding_learner27_summary_v1.csv
- results/SLM_future_feeding_learner27_paired_v1.csv
- docs/SLM_FUTURE_FEEDING_LEARNER27_AUDIT_v1_20261003.md


### 4B.5 Virtual Mouse intervention closure
The two-stage Virtual Mouse now closes the two major intervention logics separately.

Real Visual Block:
- SRI Visual Block-intact: 23/25 negative; rank-biserial=-.945; P=1.97e-6.
- observation frequency P=.396, duration P=.979, occupancy P=.426.
- future active feeding within 60 s: .570 -> .359; 24/25 decrease; P=5.96e-7.

Two-stage Virtual Block, exact 27 learners:
- observation rate control=.4624 vs VB=.4707; no collapse.
- belief-dependent future-60-s feeding probability control=.4696 vs VB=.4638.
- 26/27 animals show lower virtual feeding conversion.
- rank-biserial=-.963; one-sided exact P=1.42e-7.
The virtual magnitude (~1.25% relative) is much smaller than the real Visual Block magnitude; use directional/mechanistic closure, not quantitative reproduction.

Virtual JAWS counterfactual:
- replay each animal's actual contingent-OFF action/outcome event sequence;
- nominal alpha_B=.01;
- only Active-outcome belief-update efficacy is reduced in a pre-specified factor sweep.

At factor .5:
- virtual final Active belief mean delta=-.0329 vs real JAWS=-.0401.
- virtual Passive=+.0138 vs real=+.0109.
- virtual Active-Passive=-.0467 vs real=-.0510.
- animal-level Active-Passive rank correspondence rho=.418; not exact.
Factor .5 is not a fitted parameter. This result is a mechanism-sufficiency sensitivity, not parameter recovery.

Integrated generative chain:
current social information -> observation/sampling -> belief update -> downstream feeding conversion.
Visual Block primarily removes effective information-to-feeding conversion while gross observation persists.
JAWS selectively disrupts Active-belief updating while generic choice persistence remains intact.

Authority:
- docs/SLM_VIRTUAL_MOUSE_INTERVENTION_CLOSURE_v1_20261003.md
- figures/SOE_VirtualMouse_intervention_closure_v1.png/pdf/svg
- results/SLM_virtual_two_stage_feeding_summary_v1.csv
- results/SLM_virtual_two_stage_feeding_per_animal_v1.csv
- results/SLM_virtual_JAWS_active_belief_lesion_comparison_v1.csv
- results/SLM_virtual_JAWS_factor05_specificity_v1.csv

## Layer 5. Dopamine: restore aggregate SLM test, then resolve models by temporal dynamics

### 5.1 Aggregate held-animal DA test - recovered
An older but valid aggregate neural-adjudication analysis predicts continuous Post06 VTA DA from a baseline containing action/outcome identity, bout duration, pre-event social geometry, and session-time covariates, using nested leave-one-animal-out Ridge.

Adding time-residualized SLM reward-update variables improves held-animal prediction:
- formal belief surprise: 8/9 animals; median MSE gain +1.749%; r_rb=.867; P=.01953.
- formal Q/RPE: 7/9; +.596%; r_rb=.778; P=.03906.
- Q+belief hybrid: 8/9; +1.636%; P=.01953.

Older event-level signal comparison is directionally consistent:
median within-animal rho with DA:
- belief surprise .207.
- Actor-Critic RPE .154.
- Q-active RPE .124.
- absolute RPE .002.

This aggregate analysis should be restored before the phase-specific results. It establishes that structured reward-update variables explain DA beyond observable event/context covariates.
### 5.2 Aggregate Post06 is not by itself SLM-specific
Direct bounded comparison shows that several reward-update models can explain aggregate Post06 DA:
- SLM belief: r_rb=.867, P=.0195.
- formal Q/RPE: .778, P=.0391.
- UCL-style time-residualized RPE: .956, P=.00781.
- LC asym-Q RPE: .644, P=.0977.
- 5HT-style RPE: .733, P=.0547.
- 5HT uncertainty: .600, P=.1289.

Direct SLM-belief vs UCL-RPE difference is not significant (r_rb=-.200, P=.652).
Adding LC/UCL-APE/5HT-uncertainty terms to the SLM belief model does not yield a robust held-animal incremental improvement.

Interpretation:
aggregate reward-outcome DA establishes a reward-update family of explanations, but aggregate Post06 alone cannot identify the SLM uniquely. The decisive test is the temporal structure across Observation and outcome epochs.

Current table:
DA_global_post06_bounded_modelcomparison_v2.csv.
### 5.3 Temporal SLM adjudication
Use three pre-specified neural axes, each matched to the computation expected at that time.

Early Observation - sampling policy:
- SLM Actor policy: 5/6 positive, median MSE gain +1.94%, r_rb=.810 in the current exact table / .714 in earlier adjudication table; one-sided P=.046875.
- Q-all: r_rb=.048, P=1.0 two-sided.
- Choice-kernel: r_rb=-.238, P=.688.
- Q+CK: r_rb=-.333, P=.563.
- TinyRNN generic probability: significant in the wrong direction, r_rb=-.867, P=.01953.
- History MLP probability: r_rb=-.378, P=.359.

Middle Observation - learner-dependent APE:
- SLM APE x SRI: rho=.667, exact P=.04157.
- APE | CK error remains rho=.667, P=.04157.
- APE | Q+CK error remains rho=.667, P=.04157.
- APE | Q error remains rho=.667, P=.04157.
- reverse CK | APE: rho=-.333, P=.805.
- reverse Q+CK | APE: rho=-.333, P=.805.
- reverse Q | APE: rho=-.357, P=.820.
- TinyRNN action error: rho=-.548, P=.924.
- History-MLP action error: rho=.024, P=.488.

The fact that some unconditioned CK/Q+CK errors correlate with SRI in a looser analysis does not replace the exact partial test. Under the matched APE contract, the SLM APE retains the learner-linked effect and the competing residual does not.
Post-outcome - reward update:
- Actor-Critic RPE: r_rb=.867, P=.01953.
- outcome-belief update: r_rb=.956, P=.00586.
- Q-all RPE can also explain outcome DA: r_rb=.867, P=.01953.
- CK error: r_rb=.467, P=.25.
- CK surprise: r_rb=-.022, P=1.
- TinyRNN probability: r_rb=.733, P=.0547.
- History-MLP surprise: r_rb=-.911, P=.01172, wrong direction.

### 5.4 Overall temporal concordance
A descriptive cross-axis support score now summarizes the three pre-specified DA axes:
- SLM: 3/3 positive significant axes; 3/3 directionally positive.
- Q-all: 1/3 positive significant; 2/3 directionally positive.
- Choice kernel: 0/3 positive significant.
- Q+choice kernel: 0/3.
- TinyRNN: 0/3 positive significant and one significant wrong-direction axis.
- History MLP: 0/3 positive significant and one significant wrong-direction axis.

Do not treat this axis count as a new inferential P value. It is a compact consistency summary.

Current outputs:
- DA_global_temporal_model_adjudication_v2.csv
- SOE_DA_global_temporal_adjudication_v1.png/pdf/svg

Core interpretation:
Aggregate Post06 DA is compatible with several reward-update models, but the full DA dynamics across early policy, learner-dependent APE, and post-outcome update are selectively concordant with the structured SLM.
### 5.5 Raw photometry and longitudinal support
Raw saved-trace timing:
- 7 clean-lineage animals.
- early policy beta is directionally positive pre/onset in 5/7.
- phase-normalized early window positive in 6/7.
- no corrected continuous time cluster; use as timing support only.

Longitudinal Day1->late:
- n=3 paired animals.
- Observation-aligned changes heterogeneous.
- lick/outcome-integrated DA increases late in 3/3.
Use as a small-n longitudinal bridge, not as proof that within-session early/middle/post epochs are a longitudinal sequence.

Behavior-DA bridge:
- n=6 overlap.
- MLP gain beyond Feature-Q vs qAll-RPE DA gain rho=.886, P=.0188.
Keep exploratory.
## Layer 6. Visual Block: behavior, prediction, and clean DA

### 6.1 Behavior
Visual Block substantially reduces SRI while gross observation behavior remains present.
Current large-cohort behavior result: SRI approximately 3.67 -> 1.08; 23/25 animals decrease.

### 6.2 Zero-shot model degradation
Same-14 overlap:
- Feature-Q: r_rb=.695, P=.0203.
- policy: .676, P=.0245.
- Actor: .676, P=.0245.
- full-history MLP: .733, P=.0134.
- Current+CK: Brier degradation r_rb=.829, P=.00403; NLL degradation r_rb=.867, P=.00232.
- CK AUC degradation tracks SRI loss: rho=.600, permutation P=.0272.

Interpretation:
Visual Block changes the social-information regime across mechanistic and high-capacity models; it is not an SLM-specific prediction failure.

### 6.3 Clean photometry rebuild
Old shared-signal Visual Block DA lineage is invalid and must never be reused.
Clean rebuild uses each session's own continuous Feeding_OFF_signals_SFmatch_8.mat, local -3..0 s baseline, and remapped bout timing.
Coverage: 9 Original + 9 Visual Block sessions, 5,347 observation bouts.

Clean demonstrator-feed-locked Original > Visual Block:
- Early: 8/9, r_rb=.867, P=.01953.
- Middle: 7/9, r_rb=.689, P=.0742.
- Late: 6/9, r_rb=.511, P=.203.

Sustained Observation:
Original shows a reliable Early-to-Middle increase; Visual Block does not, but the formal condition x phase interaction is not significant.

Interpretation:
visual access most clearly modulates early demonstrator-feed-locked VTA DA. Do not claim a statistically established flattening interaction.

### 6.4 Information-availability closure authority
Visual Block is now summarized in one intervention-level authority:
- figures/SOE_VisualBlock_information_closure_v1.png/pdf/svg
- results/SOE_VisualBlock_zero_shot_effects_v1.csv
- results/SOE_VisualBlock_DA_phase_effects_v1.csv
- docs/SOE_VISUALBLOCK_INFORMATION_CLOSURE_v1_20261003.md

The closure is three-level:
1. phenotype: SRI approximately 3.67 -> 1.08, 23/25 animals decrease;
2. computation: zero-shot prediction degrades across Feature-Q, policy, actor, full-history MLP and choice-persistence models;
3. neural signal: early demonstrator-feed-locked VTA DA is lower under Visual Block, r_rb=.867, P=.01953.

Interpretation:
Visual Block tests information availability. It should be paired with JAWS, which tests state updating after information is available, but the two interventions should not be collapsed into one mechanism.

## Layer 7. JAWS / VTA inhibition

### 7.1 Behavioral causal endpoint
Contingent Laser ON vs OFF:
- SRI 1.880 -> .786.
- 9/10 lower; r_rb=-.927, P=.00586.
- gross observation remains largely preserved.
- Active rewarded-observation ratio 25.20% -> 15.59%, P=.01172.
- real-minus-shuffle numerator decreases, P=.00586.

Interpretation:
VTA inhibition disrupts the successful coupling between social observation and reward, not simply the amount of social sampling.

### 7.2 Causal latent coordinate
Exact Module 1.3 mapping:
- acute Active belief r_rb=-1.000, P=.00195.
- acute Active-specific belief -.927, P=.00586.
- continuous per-event Active belief -.927, P=.00586.
- session-scale Active belief -.964, P=.00391.
- behavioral SRI endpoint -.927, P=.00586.
- continuous CK update +.164, P=.695.

Active social-reward belief is the most reproducible cross-scale coordinate.

### 7.3 Independent cohort direction
Standard JAWS: 5/5 animals negative Active-belief update.
VTA-copy JAWS: 5/5 negative.
Combined: 10/10, P=.001953.
Use as replication/direction evidence; each n=5 cohort alone has limited exact-test resolution.

### 7.4 Continuous dynamics
- OFF episodes build Active belief, mean delta about +.00249, P=.001953.
- ON episodes reverse/erode Active-belief updating, mean delta about -.000815, 9/10 negative, P=.02734.
- Q remains positive but accumulates more slowly during ON.
- CK update is not similarly disrupted.

Preferred interpretation:
VTA inhibition changes the update dynamics of Active social reward belief rather than directly suppressing social observation policy.

Do not claim every SLM latent is suppressed.
Do not claim a significant contingent-vs-noncontingent latent interaction unless a direct interaction test supports it.

### 7.5 Causal-closure authority figure
The causal result is now summarized in one authority figure:
- figures/SOE_JAWS_causal_closure_v1.png/pdf/svg
- results/SOE_JAWS_causal_closure_effects_v1.csv
- docs/SOE_JAWS_CAUSAL_CLOSURE_v1_20261003.md

The cross-scale result is intentionally explicit:
- phenotype: SRI r_rb=-.927, P=.00586;
- acute Active belief: r_rb=-1.000, P=.001953;
- continuous per-event Active belief: r_rb=-.927, P=.00586;
- session-scale Active belief: r_rb=-.964, P=.00391;
- contingent choice-kernel update: r_rb=+.164, P=.695.

Thus the preferred causal statement is that VTA activity is required for updating/maintaining the Active social-reward belief, rather than for generic observation or generic action-history persistence.

## Layer 8. Generalization: observational fear promoted to current quantitative authority; food neophobia still under source audit

### 8.1 Source lineage now pinned
The observational-fear source chain has been recovered directly from the workstation rather than inferred from the old manuscript.

Raw/derived roots:
- Z:/sternsonlab/Zhenggang/Behavior/SocialOFL/D1_Fear
- Z:/sternsonlab/Zhenggang/Behavior/SocialOFL/D2_Fear
- Z:/sternsonlab/Zhenggang/Behavior/NonsocialOFL/D1_Fear
- Z:/sternsonlab/Zhenggang/Behavior/NonsocialOFL/D2_Fear

Training-history groups:
- Social-trained: 85, 87, 97, 98, 99, 102.
- Nonsocial-trained: 56, 86, 88, 89, 92, 94.

Important provenance correction: later aggregate analysis folders contain animals from both training histories. Folder location is therefore not a valid group label. Current statistics use the explicit training-history mapping above.

The recovered D1/D2 pipeline contains raw trial videos, 10-Hz conversions, SLEAP tracking, identity-switch correction, per-frame social features, and historical velocity/orientation/observation analyses. Exact within-trial windows are pre 0-20 s, cue 20-37 s, shock 37-40 s, and post 40-60 s.

D1 segmentation was rebuilt from original per-trial MP4 frame counts. Trials contain 603-605 frames. Animal 85 D1 has one extra 600-frame pre-trial recording that is explicitly skipped. Remaining D1 feature rows match raw video frame counts exactly or within three terminal frames. D2 is similarly reconstructed; small terminal row-count differences in a few files do not affect the pre/cue/shock windows.

### 8.2 Day-1 response is temporally structured
The source-rebuilt result is more specific than the older shorthand that socially trained observers simply move less.

Predictive cue / late-trial immobility:
- last 10 D1 trials, cue velocity Social-trained = 0.249 px/frame.
- Nonsocial-trained = 0.362 px/frame.
- Cliff's delta = -0.778.
- exact group-label permutation P = 0.0152.

Shock-locked vicarious reactivity:
- all-30-trial shock velocity = 15.53 vs 8.29 px/frame.
- Cliff's delta = +0.944.
- exact P = 0.00433.
- shock-minus-pre velocity gives the same Cliff's delta = +0.944, P = 0.00433.
- shock absolute angular-velocity change: Cliff's delta = +0.833, P = 0.00866.

Thus the D1 phenotype contains late cue immobility together with a strong shock-locked orienting/reactivity component; it is not a unitary freezing effect.

### 8.3 Prior SOE training maintains shock-focused social observation across trials
In the last 10 D1 trials:
- shock observation fraction Social-trained = 0.450.
- Nonsocial-trained = 0.369.
- Cliff's delta = +0.778.
- exact P = 0.0152.

Trial dynamics:
- shock-observation slope per trial = +0.000475 versus -0.00517.
- slope contrast Cliff's delta = +0.722, exact P = 0.0238.
- last10-minus-first10 shock observation = +0.0078 versus -0.1011.
- change contrast Cliff's delta = +0.778, exact P = 0.0216.

Prior SOE training therefore preserves shock-focused social monitoring while nonsocial-trained animals progressively reduce it.

### 8.4 D1 effects are not explained by a pre-existing motor baseline
A raw-coordinate analysis of available D0 baseline videos computes centroid displacement directly from corrected pose coordinates, avoiding a legacy derived-velocity column that is zero in this archive.

Available D0 cohort: six Social-trained and five Nonsocial-trained animals; animal 92 has no recovered D0 file.

Mean D0 centroid speed:
- Social-trained = 9.073 px/frame.
- Nonsocial-trained = 9.012 px/frame.
- Cliff's delta = +0.067.
- exact P = 0.946.

Median and 90th-percentile baseline speeds are also not different. This argues against a fixed locomotor difference as the explanation for D1 shock reactivity.

### 8.5 Repeated exposure attenuates the D1 group difference
On D2:
- shock velocity = 0.310 vs 0.374 px/frame, Cliff's delta = -0.028, P = 1.0.
- shock observation fraction = 0.0578 vs 0.0648, Cliff's delta = -0.028, P = 1.0.

Formal change-score comparison:
- D2-minus-D1 shock velocity change = -15.22 vs -7.92 px/frame.
- Cliff's delta = -0.944.
- exact P = 0.00433.
- shock angular-velocity change shows the same direction: Cliff's delta = -0.833, P = 0.0130.

Preferred interpretation: prior SOE experience changes the first-day organization of observational-fear behavior, producing stronger shock reactivity and sustained social monitoring with late cue immobility; the amplified D1 response attenuates with repeated exposure. Do not describe this as a fixed trait or generic motor difference.

### 8.6 Exact-boundary time-course corroborates the cue-to-shock transition
A 12/12-animal time-resolved rebuild uses the true per-MP4 trial boundaries rather than a fixed 603-frame reshape. Animal 85's extra 600-frame pre-trial is explicitly skipped.

Metric-wise exact max-cluster tests recover the same temporal structure as the pre-defined windows:
- all30 shock-region velocity 37.3-41.4 s: Cliff delta +0.944, within-metric cluster P=.00866.
- late15 cue velocity 22.8-26.2 s: delta -0.944, cluster P=.01948.
- late15 shock velocity 37.3-40.0 s: delta +0.944, cluster P=.01299.
- late15 shock angular velocity 37.3-39.3 s: delta +1.000, cluster P=.04113.

A stricter max-cluster correction over all eight pre-specified metric x subset families yields no family-wise P<.05. Use this as time-resolved shape/timing support; the pre-defined exact-window statistics remain inferential authority.

### 8.7 Food neophobia / SAFN is now source-rebuilt
The raw source was recovered at Z:/sternsonlab/Zhenggang/Behavior/safn. The 12 animals exactly match the observational-fear training-history cohort.

The protocol document identifies the assay as Social related Novelty-suppressed feeding: after social or nonsocial training, the observer watches a hungry demonstrator familiarized to sunflower seed for 10 min, the demonstrator is removed, and the observer receives unfamiliar sunflower seed for a 10-min test.

Recovered lineage:
raw pre/post MP4 -> SLEAP -> SimBA SAFN project -> manual Feeding labels -> final 2024-01-03 aggregate event/bout logs.

A direct manual-label audit reproduces the final SimBA aggregate latency and duration to less than 0.001 s for feeding animals. Animal 92 contains no Feeding-positive frame and is right-censored at 600 s. This also resolves an earlier fps/version mismatch for animal 88; the final SimBA latency is 148.929 s.

Protocol-defined primary latency:
- Social-trained mean 45.96 s, median 45.87 s.
- Nonsocial-trained mean 199.47 s, median 136.03 s.
- Cliff delta -0.722.
- exact 6-vs-6 permutation P=.01948.
- exact permutation log-rank P=.03030.
- feeding events 6/6 vs 5/6.

Secondary feeding structure:
- first Feeding bout 61.07 vs 8.81 s, delta +0.889, P=.00866; supporting/exploratory.
- total feeding duration over 600 s 291.43 vs 153.86 s, delta +0.500, P=.1342; directional.

Interpretation:
Prior SOE training reduces the novelty-related delay before engaging with unfamiliar food. Do not claim that all consumption measures are significantly increased, and do not promote first-bout duration above the protocol-defined latency endpoint.

### 8.8 Current generalization files
- observational_fear_D1_exact_segmentation_QA_v1.csv
- observational_fear_D1_exact_animal_summary_v1.csv
- observational_fear_D1_exact_group_effects_v1.csv
- observational_fear_D1_exact_learning_dynamics_animal_v1.csv
- observational_fear_D1_exact_learning_dynamics_effects_v1.csv
- observational_fear_D2_exact_segmentation_QA_v1.csv
- observational_fear_D2_exact_animal_summary_v1.csv
- observational_fear_D2_exact_group_effects_v1.csv
- observational_fear_D1D2_attenuation_effects_v1.csv
- observational_fear_D0_rawmotion_animal_v1.csv
- observational_fear_D0_rawmotion_effects_v1.csv
- observational_fear_D1_exact_timecourse_cluster_effects_v2.csv
- food_neophobia_SAFN_manual_label_audit_v1.csv
- food_neophobia_SAFN_final_animal_v2.csv
- food_neophobia_SAFN_final_effects_v2.csv
- food_neophobia_SAFN_final_QA_v2.csv
- SOE_generalization_observational_fear_v1.png/pdf/svg
- SOE_GLOBAL_EFFECT_SIZE_REGISTRY_v12.csv


## Layer 9. Cross-dataset SLM component generalization

The external claim is now stronger than "history helps" and broader than one macaque dataset. The transported object is the computational decompositionâ€”source-tagged evidence, multiscale latent state, policy/value use, and outcome/updateâ€”not an identical sensory feature vector.

### 9.1 Macaque DANDI001435: source-aware multiscale behavior after exact sequence de-duplication
The 10 neural-recording labels do not correspond to 10 independent behavioral sequences. Exact trial-table fingerprinting identifies three same-date Lalo/Offenbach pairs with identical behavioral tables (2023-02-23, 2023-02-28, 2023-03-15). The behavioral authority is therefore **7 unique dyadic sequences**.

Equal-weight unique-sequence means:
- current baseline: Brier .139045; NLL .451710.
- shared single-timescale: .102816; .326225.
- dual/source-specific single-timescale: .096732; .307756.
- shared multiscale: .090844; .294413.
- dual/source-specific multiscale: .085573; .276969.

All structured contrasts are concordant across the 7 unique sequences:
- shared single vs baseline: 7/7; r_rb=1; one-sided P=.0078125.
- dual single vs baseline: 7/7; r_rb=1; P=.0078125.
- shared multiscale vs baseline: 7/7; median relative Brier reduction 33.6%; P=.0078125.
- dual multiscale vs baseline: 7/7; median relative Brier reduction 37.0%; P=.0078125.
- shared multiscale vs shared single: 7/7; P=.0078125.
- dual multiscale vs dual single: 7/7; P=.0078125.
- dual multiscale vs shared multiscale: 7/7; P=.0078125.

An exact-contract causal raw-history MLP provides a nonlinear comparator:
- Brier .118097; NLL .613542.
- better than baseline in 7/7, two-sided P=.015625.
- worse than each structured single/multiscale model in 7/7, P=.015625.
Its Brier improvement but poor log-loss indicates overconfidence/calibration weakness; it is a useful nonlinear raw-history comparator, not a universal flexible ceiling.

A separate 58,922-event macaque global same-zoo contract contains an RNN ceiling. Its absolute Brier cannot be compared numerically with this 7-sequence source-aware contract.


Latest exact-contract flexible-ceiling audit:
- 50-lag HistGB: Brier .081148 / NLL .263660 / AUC .956636.
- dual multiscale: .085573 / .276969 / .952317.
- raw-history linear 50-lag: .088585 / .285491 / .949188.
- raw-history MLP grid: .115859 / .371974 / .914359.
- baseline: .139045 / .451710 / .820203.
HistGB is lower-Brier in 6/7 unique sequences versus dual multiscale, but the paired difference is not decisive (r_rb=.786, two-sided P=.078125).
Under strict chronological forward-CV, HistGB remains numerically best (.085754 vs dual .090220) but paired P=.15625.

Interpretation:
the structured source-aware multiscale state is robust and near a strong flexible ceiling; behavior alone does not uniquely identify it. Neural, causal and generative evidence remain the mechanism discriminator.
### 9.2 Macaque ACC: multiscale SLM state survives dependence-aware clustering
Forward encoding predicts choice-aligned ACC population activity under block-held-out CV. The observable baseline contains current player, current choices, difficulty and position in block; current reward/outcome is excluded and the SLM state is pre-trial.

Recording-session view:
- shared single-timescale: 4/10 improve; P=.539.
- shared multiscale: 9/10 improve; r_rb=.891; P=.00488.
- dual multiscale: 8/10 improve; r_rb=.818; P=.00977.

Because three same-date pairs share identical behavior, the preferred dependence sensitivity collapses them into 7 behavior-date clusters:
- shared single-timescale vs current: 2/7; r_rb=-.071; P=.594.
- shared multiscale vs current: 6/7; r_rb=.857; P=.02344.
- dual multiscale vs current: 5/7; r_rb=.786; P=.03906.
- shared multiscale vs shared single: 6/7; r_rb=.929; P=.015625.
- dual multiscale vs shared multiscale: 4/7; P=.406.

Thus the robust neural conclusion is **multiscale pre-trial state**. Source-specific dual state is behaviorally useful, but a neural dual-over-shared advantage is not established.

### 9.3 Rat observational maze: source identity determines later observer choice
The inferential unit is rat rather than session. Trial-count-weighted held-out Brier gives:
- Demo/current demonstrator vs self-history: 5/5 rats improve; median gain +.1105; r_rb=1.0; exact one-sided Wilcoxon P=.03125.
- Object/current moving-object vs self-history: 2/3 improve; median gain +.00655; r_rb=0; P=.625.
- Demo gain > Object gain: Cliff delta=.867; one-sided Mann-Whitney P=.0357.

The same formal log predictive-probability social-information value is directionally positive but weaker at rat level:
- Demo: 4/5 positive; median +.2715 nats/trial; r_rb=.867; P=.0625.
- Object: 2/3 positive; median +.0581; r_rb=0; P=.625.

Long source-history/reliability terms do not improve beyond the current demonstrator cue. The strong claim is therefore source specificity of current social evidence, not universal slow memory.

### 9.4 Cooperative foraging: same-contract transport plus independent multi-animal corroboration
Our direct same-contract benchmark uses the only trajectory dataset committed in the public MAIRL repository: YC069. The first 1000 trajectories are split by the author-style held-out trajectory rule.

Within this dyad:
- Follower current social information vs self-only: 183/200 held-out trajectories improve.
- adding recent social history beyond current partner state improves 126/200.
- current+history social state vs self-only improves 178/200, within-dyad r_rb=.923.
- the corresponding leader gain is smaller.
- uncertainty/role gating is also reproducible within YC069.

These are valid held-out transport results but are not population-level mouse inference.

The published Nature MAIRL analysis supplies the cross-animal corroboration:
- n=6 animals per role.
- partner distance is significant in 3/6 leaders and 6/6 followers.
- egocentric partner angle is significant in 2/6 leaders and 6/6 followers.
- proximal partner-distance value is higher in followers than leaders (P=7.7e-6, n=6 per role).
- the published study also reports role-specific mPFC representations aligned with these inferred social values.

Therefore the manuscript should pair the two levels explicitly: YC069 demonstrates transport of our current/history social-state decomposition under a held-out contract; the independent multi-animal MAIRL result establishes that follower-biased partner value is a reproducible population-level feature.

### 9.5 Marmoset Neuron 2026: active social sampling -> evidence accumulation -> dmPFC decision state
A second primate cooperation dataset provides a particularly close mechanistic bridge to the SLM decomposition. The public source data and analysis code contain repeated behavioral/model sessions and dmPFC neural recordings from two marmosets. Because there are only two independent animals, this is treated as cross-species mechanistic convergence rather than population-level replication.

The gaze-gated drift-diffusion model makes active sampling explicit. In the source model, variability of the partner's holistic action representation during social gaze enters the drift-rate equation as beta4. Reanalysis of the public session-level coefficients shows the same expected direction in both animals:
- Animal K: 16/20 valid sessions negative; median beta4=-.159; r_rb=-.762; within-animal P=.00141.
- Animal D: 19/26 negative; median=-.052; r_rb=-.624; P=.00271.

dmPFC ramping then provides a neural signature of the accumulating social evidence:
- ramp slope vs social evidence, K: 421/490 neurons positive; median rho=.184; r_rb=.867.
- D: 333/466 positive; median rho=.150; r_rb=.428.
- the canonical accumulator hallmark is also present: ramp slope vs reaction time is negative in 489/490 K neurons and 459/466 D neurons.

The neural dynamics map directly onto the computational latent. In the neural DDM, trial-level firing-rate slope predicts drift rate:
- K: 459/464 positive coefficients; median=.450; r_rb=.999.
- D: 350/361 positive; median=.521; r_rb=.997.

History also changes the decision initial condition:
- previous outcome -> starting-point bias, K: 17/18 sessions in the same direction; r_rb=-.930.
- D: 21/21; r_rb=-1.000.

Finally, dmPFC population geometry covaries with social evidence:
- social evidence vs population path variability, K: 14/20 negative; median rho=-.087; r_rb=-.581.
- D: 18/24 negative; median rho=-.106; r_rb=-.600.

The correspondence to SOE is structural rather than anatomical identity: social gaze gating parallels observation/sampling; partner-evidence accumulation parallels the learned social state; ramping maps onto latent accumulation dynamics; prior outcome shifts the decision initial condition; and population geometry represents the evolving social decision state. Do not claim that dmPFC and VTA encode the same scalar latent.

Authority:
- docs/MARMOSET_NEURON2026_SLM_BRIDGE_v1_20261003.md
- results/marmoset_Neuron2026_source_reanalysis_v2.csv
- results/marmoset_Neuron2026_expected_direction_effects_v1.csv
- results/marmoset_Neuron2026_SLM_bridge_v2.csv
- figures/SOE_marmoset_Neuron2026_SLM_bridge_v1.png/pdf/svg

### 9.6 Human experience/observation bridge
Held-subject multiscale history improves in 9/10 human subjects (r_rb=.964, P=.00391).
A value-like multiscale Feature-Q state improves over paper-current in 7/10 (r_rb=.709, one-sided P=.0244).
Thus temporal state and value-like components transport to human behavior without requiring a recurrent-network headline.

### 9.7 Rat DANDI001169: structured multiscale event state
Explicit multiscale event state improves over short/current history in 7/10 rats:
- r_rb=.745;
- one-sided P=.0186; retain two-sided P=.0371 when matching the older table.
TinyRNN is worse than the explicit multiscale state in the matched comparison. This supports structured temporal state, not universal recurrence.

### 9.8 Mouse DANDI001632 defines when physical time must enter the latent state
Trial+physical-time state improves over trial-clock alone in 12/17 animals:
- r_rb=.556;
- one-sided P=.0224.

The effect is concentrated in the 3600-s reward-spacing group:
- 3600 s: 5/5 positive; r_rb=1.0; P=.03125.
- 30 s: 4/6; P=.219.
- 300 s: 3/6; P=.500.

The 3600-s gain exceeds pooled 30/300-s gains:
- Cliff delta=.867;
- P=.00194.

Interpretation: event-centered memory is useful when events define task progression, but physical time should enter the latent state when elapsed interval itself is experimentally informative. This is a boundary condition that strengthens rather than weakens the model family.

### 9.9 Independent neural update convergence

Noritake/Isoda macaque:
- expected-sign source-tagged RPE slopes in 22/22 oRPE+, 38/38 oRPE-, 6/6 sRPE+, and 12/12 sRPE- cells.
This is the strongest independent neural support for the source-tagged RPE/update module.

DANDI000351 NAcc dopamine now passes a stricter held-out neural-to-behavior test.
For each animal, baseline prediction of subsequent licking includes previous reward interval, previous licking, and session progress; evaluation uses held-out contiguous time blocks with nested ridge selection. Adding reward-evoked DA:
- improves prediction in 6/7 animals;
- median relative MSE gain +.66%;
- mean gain +2.06%;
- r_rb=.857;
- one-sided P=.02344.

Excluding the datHT/stGtACR animal leaves:
- 5/6 positive;
- median gain +1.06%;
- r_rb=.810;
- P=.04688.

Thus reward-evoked dopamine carries prospective information about subsequent consummatory behavior beyond behavioral history. Use as independent update-side neural convergence, not as a unique full-SLM test.

DANDI000559 DLS dLight provides a useful boundary. After residualizing stable syllable identity and coarse session time, dLight correlates with future-minus-past reuse at 30-60 s (5/6 positive at both windows). However, in a stricter held-out prediction that already includes past reuse, syllable identity and time:
- +dLight is not incrementally predictive at 30 s (2/6; P=.781).
- +dLight is not incrementally predictive at 60 s (1/6; P=.844).

Therefore keep 000559 only as a timing/correlation boundary in Extended Data; do not use it as main external predictive support.

### 9.10 Supporting datasets and current boundaries
Aeon social foraging:
recent partner-history value is positive in 7/10 subjects nested within five experiments (r_rb=.673; one-sided P=.0322), and all five experiment means are positive. Current partner-state value by itself is not stable at the subject level. This complements the rat maze: some tasks are dominated by the current social cue, whereas naturalistic foraging benefits more from recent partner history. Keep Aeon as supporting transport because only five experiment clusters are available and postsocial carryover is not supported.

DANDI000114 PVN/OXT:
observation, OXT activity and later retrieval are technically linked across two paired animals and three days. This is feasibility/biological convergence only; cohort size is insufficient for model inference.

EcoHAB:
do not promote until cue-side and approach-metric mapping are frozen.

Marmoset cooperation:
public code supports social-RL/DBN analyses, but the trial-level raw data referenced by the notebooks are not public, so it cannot yet enter the matched predictive benchmark.

### 9.11 Manuscript hierarchy
Main external computational panel:
1. DANDI001435 macaque behavior + ACC;
2. rat observational maze source specificity at rat level;
3. cooperative foraging: YC069 same-contract transport plus published n=6/role multi-animal MAIRL corroboration;
4. human experience/observation.

External mechanistic neural bridge:
5. marmoset Neuron 2026: gaze-gated social evidence accumulation -> dmPFC ramping -> DDM drift, with prior-outcome-dependent starting bias in both recorded animals.

General transport and boundary:
5. rat DANDI001169;
6. mouse DANDI001632.

Neural Extended Data:
6. Noritake/Isoda source-tagged RPE;
7. DANDI000351 predictive DA;
8. DANDI000559 timing boundary.

General transport and boundary:
9. rat DANDI001169;
10. mouse DANDI001632.

Supporting:
11. Aeon;
12. DANDI000114.

Current authority:
- docs/SLM_EXTERNAL_MULTIDATASET_AUTHORITY_v5_20261003.md
- docs/SOE_ADAPTIVE_SOCIAL_INFORMATION_VALUE_v2_20261003.md
- results/SOE_SLM_external_strict_registry_v5.csv
- results/SOE_crossspecies_SLM_component_matrix_v6.csv
- results/SOE_crossspecies_SLM_component_support_map_v4.csv
- figures/SOE_SLM_external_multidataset_v5.png/pdf/svg
- figures/SOE_cross_task_social_information_value_v2.png/pdf/svg

## Current integrated result logic - analysis version, not manuscript language

Model-recovery guardrail: six-family mouse-matched recovery is 35/36 exact (97.2%), so behavioral equifinality is not complete model non-identifiability.

1. SOE behavior cannot be explained by time, previous choice, current geometry, or simple/classical RL alone.
2. SLM is substantially stronger than those baselines.
3. Strong persistence/history models can match or exceed SLM behaviorally, so behavior alone is underdetermined.
4. A parsimonious SLM + choice-persistence head recovers most of the black-box behavioral gain.
5. Held-out social-information value is positive in SOE and changes adaptively with learning stage and behavioral state; YC069 provides a within-dyad same-contract cooperative replication, while the published n=6/role MAIRL analysis independently establishes follower-biased partner value across animals.
6. Recovered multi-timescale results naturally motivate the SLM architecture: fast policy change, multi-event history, slower reward-credit state, transient cross-day prior.
7. Aggregate Post06 DA confirms that reward-update latents carry neural information but is not by itself unique to SLM.
8. The temporal DA pattern is the key model discriminator: SLM is the only current model family with positive significant support on all three pre-specified axes.
9. Visual Block independently tests social-information availability and shows corresponding behavior/model/DA disruption.
10. JAWS provides causal evidence that VTA activity is required for maintaining/updating Active social reward belief while preserving generic sampling/persistence.
11. Observational-fear generalization is source-rebuilt at animal level: prior SOE training predicts stronger D1 shock reactivity, late cue immobility, and sustained shock-focused social monitoring; the D1 effect attenuates on D2.
12. A second source-rebuilt generalization assay, social-related novelty-suppressed feeding, shows a shorter protocol-defined latency to engage with unfamiliar food after prior SOE training (delta=-.722, exact P=.0195; exact permutation log-rank P=.0303).
13. External validation spans multiple social tasks with explicit independent units: macaque DANDI001435 supports multiscale/source-aware state and incremental ACC encoding; rat observational maze supports source specificity in 5 Demo rats versus 3 moving-object controls; cooperative YC069 gives held-out same-contract transport and the published n=6/role MAIRL analysis supplies cross-animal role-specific partner-value corroboration; marmoset Neuron 2026 independently links active social sampling to social-evidence accumulation, dmPFC ramping and history-dependent decision bias; human behavior supports multiscale state/value; Aeon supports recent partner history across 5/5 independent experiments; DANDI001169/DANDI001632 define transport and the physical-time boundary; Noritake/Isoda and DANDI000351 provide update-side neural convergence.

## Files created/updated in this revision
- social_learning_unification_20261002/SOE_baseline_ladder_v2.csv
- social_learning_unification_20261002/DA_global_post06_bounded_modelcomparison_v2.csv
- social_learning_unification_20261002/DA_global_temporal_model_adjudication_v2.csv
- social_learning_unification_20261002/SOE_DA_global_temporal_adjudication_v1.png/pdf/svg
- social_learning_unification_20261002/observational_fear_D1_exact_group_effects_v1.csv
- social_learning_unification_20261002/observational_fear_D1_exact_learning_dynamics_effects_v1.csv
- social_learning_unification_20261002/observational_fear_D2_exact_group_effects_v1.csv
- social_learning_unification_20261002/observational_fear_D1D2_attenuation_effects_v1.csv
- social_learning_unification_20261002/observational_fear_D0_rawmotion_effects_v1.csv
- social_learning_unification_20261002/SOE_generalization_observational_fear_v1.png/pdf/svg
- social_learning_unification_20261002/SOE_GLOBAL_EFFECT_SIZE_REGISTRY_v10.csv
- observational_fear_D1_exact_timecourse_cluster_effects_v2.csv
- food_neophobia_SAFN_manual_label_audit_v1.csv
- food_neophobia_SAFN_final_animal_v2.csv
- food_neophobia_SAFN_final_effects_v2.csv
- SOE_GLOBAL_EFFECT_SIZE_REGISTRY_v12.csv
- this file: SOE_LATEST_ANALYSIS_MASTER_v4_20261003.md


## v5 additions
- Formal SLM specification and nested model-family registry.
- DANDI001435 de-duplicated 7-sequence source-specific multiscale behavior authority.
- ACC shared-state external neural summary with strict nuisance-control boundary.
- Human value-state bridge and independent primate source-tagged RPE convergence.
- Cross-species SLM component matrix replacing a recurrence-centered generalization narrative.

## v7 additions
- docs/SLM_IDENTIFIABILITY_GENERATIVITY_v2_20261003.md
- results/SOE_SLM_mousematched_model_recovery_v1.csv
- results/SOE_SLM_mousematched_recovery_confusion_v1.csv
- results/SOE_SLM_focused_conditional_recovery_v1.csv
- results/SOE_SLM_generative_summary_v1.csv
- results/SOE_SLM_lag1_generative_fidelity_v1.csv
- results/001435_ACC_SLM_encoding_by_session_model_v1.csv
- results/001435_ACC_SLM_encoding_effects_v1.csv
- results/001435_ACC_SLM_encoding_sensitivity_v1.csv
- figures/SOE_DANDI001435_SLM_external_v1.png/pdf/svg
- figures/SOE_SLM_identifiability_v1.png/pdf/svg

## v8 additions
- docs/SLM_EXTERNAL_MULTIDATASET_AUTHORITY_v3_20261003.md
- results/SOE_SLM_external_multidataset_registry_v1.csv
- results/SOE_crossspecies_SLM_component_matrix_v3.csv
- results/SOE_crossspecies_SLM_component_support_map_v2.csv
- figures/SOE_SLM_external_multidataset_v2.png/pdf/svg

## v9 additions
- docs/SOE_ADAPTIVE_SOCIAL_INFORMATION_VALUE_v1_20261003.md
- docs/SLM_EXTERNAL_MULTIDATASET_AUTHORITY_v3_20261003.md
- results/SOE_social_information_value_state_learning_v1.csv
- results/SOE_adaptive_social_information_bridge_v1.csv
- results/Cooperative_social_information_uncertainty_gating_v1.csv
- results/SOE_crossspecies_SLM_component_matrix_v3.csv
- results/SOE_crossspecies_SLM_component_support_map_v2.csv
- results/SOE_SLM_external_strict_registry_v2.csv
- results/DANDI000351_DA_incremental_behavior_v1.csv
- results/DANDI000351_DA_incremental_behavior_summary_v1.csv
- results/DANDI000351_DA_incremental_behavior_sensitivity_v1.csv
- results/DANDI000559_dlight_incremental_future_reuse_v1.csv
- results/DANDI000559_dlight_incremental_future_reuse_summary_v1.csv
- figures/SOE_adaptive_social_information_value_v1.png/pdf/svg
- results/SOE_cross_task_social_information_value_v1.csv
- results/SOE_cross_task_social_information_value_units_v1.csv
- figures/SOE_cross_task_social_information_value_v1.png/pdf/svg

## v10 additions â€” independent-unit correction
- Rat observational-maze headline inference moved from session to rat.
- Cooperative-foraging trajectory statistics explicitly restricted to YC069 within-dyad transport.
- Published multi-animal MAIRL (n=6 per role) added as the independent population-level role-value corroboration.
- Same-formal-quantity cross-task social-information plot rebuilt with rat-level values and scope labels.
- External validation figure rebuilt as v4 with rat-level points and published multi-animal cooperative panel.
- docs/SLM_EXTERNAL_MULTIDATASET_AUTHORITY_v5_20261003.md
- docs/SOE_ADAPTIVE_SOCIAL_INFORMATION_VALUE_v2_20261003.md
- results/SOE_SLM_external_strict_registry_v5.csv
- results/SOE_crossspecies_SLM_component_matrix_v6.csv
- figures/SOE_SLM_external_multidataset_v5.png/pdf/svg
- figures/SOE_cross_task_social_information_value_v2.png/pdf/svg
- figures/SOE_adaptive_social_information_value_v2.png/pdf/svg

## v11 additions â€” primate social-evidence accumulation bridge
- Public 2026 marmoset Neuron source-data/code repository cloned and audited.
- Gaze-gated partner-evidence drift coefficient reanalyzed in both animals.
- dmPFC ramp slope -> social evidence and ramp slope -> DDM drift quantified with bounded effects.
- Prior-outcome -> starting-bias and population-geometry effects recovered in both animals.
- This evidence is explicitly labeled a two-animal mechanistic bridge, not a population-level replication.
- docs/MARMOSET_NEURON2026_SLM_BRIDGE_v1_20261003.md
- results/marmoset_Neuron2026_source_reanalysis_v2.csv
- results/marmoset_Neuron2026_expected_direction_effects_v1.csv
- results/SOE_SLM_external_strict_registry_v5.csv
- results/SOE_crossspecies_SLM_component_matrix_v6.csv
- figures/SOE_marmoset_Neuron2026_SLM_bridge_v1.png/pdf/svg


## v12 additions — claim graph and causal closure
- Eight-module manuscript-level master result graph created from current authorities.
- 28 manuscript-level quantitative nodes retained; CORE blocker count = 0.
- Exact-boundary fear clusters and raw continuous photometry explicitly remain corroborating/boundary analyses.
- Additional public datasets are no longer P0 unless they fill a missing SLM component.
- JAWS causal closure consolidated across phenotype, acute belief, continuous update, session-scale belief, cohort replication and choice-kernel specificity.
- docs/SOE_MASTER_RESULT_GRAPH_v1_20261003.md
- results/SOE_MASTER_RESULT_GRAPH_v1_20261003.csv
- results/SOE_MASTER_RESULT_GRAPH_gap_audit_v1.csv
- results/SOE_MASTER_RESULT_GRAPH_module_summary_v1.csv
- docs/SOE_JAWS_CAUSAL_CLOSURE_v1_20261003.md
- results/SOE_JAWS_causal_closure_effects_v1.csv
- figures/SOE_JAWS_causal_closure_v1.png/pdf/svg

## v13 additions — intervention closure and manuscript result order
- Visual Block consolidated into a single information-availability intervention figure.
- Visual Block and JAWS are now explicitly separated mechanistically:
  - Visual Block removes the social-information channel.
  - JAWS disrupts updating/maintenance of the Active social-reward belief.
- Main-text result order frozen in docs/SOE_MAIN_TEXT_RESULT_ORDER_v1_20261003.md.
- docs/SOE_VISUALBLOCK_INFORMATION_CLOSURE_v1_20261003.md
- figures/SOE_VisualBlock_information_closure_v1.png/pdf/svg
- results/SOE_VisualBlock_zero_shot_effects_v1.csv
- results/SOE_VisualBlock_DA_phase_effects_v1.csv

## v14 additions — numerical audit, contract correction and Virtual Agent alignment
- SOE 27-animal model table re-audited from per-animal sources: Brier/log-loss reconstruction errors are numerical precision only; paired r_rb/P reproduce exactly.
- Complete classical RL results retained rather than compressed into a single "8 baselines" sentence.
- Model × Evidence v2 separates raw middle-DA association from conditional uniqueness and keeps untested cells NA.
- DANDI001435 behavior corrected from 10 recording labels to 7 unique behavioral sequences after exact fingerprinting.
- DANDI001435 ACC retains recording-level analysis plus preferred 7-date-cluster dependence sensitivity.
- Exact-contract 001435 raw-history MLP added and loses to all structured source-aware states in 7/7 unique sequences.
- Cross-task/species comparison is now contract-indexed; 17 convergence datasets/assays are inventoried with baseline, structured model, strong alternative, neural endpoint and remaining gap.
- Legacy Virtual Agent simulator recovered and tested (5/5 tests passed); full current SLM needs a composite state adapter, not a rewritten environment.

## v15 additions — complete input-matched inventory
- Comprehensive SOE behavior inventory expanded to 38 unique model/variant rows.
- All eight Current-matched classical controls are present.
- Historical SLM+CK naming duplication normalized after metric-equality audit.
- 27-animal paired comparisons between SLM and every Current-matched control are stored in results/SLM_vs_currentmatched_all_paired_v4.csv.
- Model × Evidence v3 adds the six previously omitted Current-matched behavior-only controls while leaving neural/causal cells NA unless truly tested.

## v16 additions — latest audited authority convergence
- Behavior authority upgraded to the 45-row semantically deduplicated v5 inventory, including restricted RL, all eight current-matched controls, flexible ceilings and biologically inspired comparators.
- Model×Evidence authority upgraded to v4 (32 unique model/evidence families); stale Early SLM r_rb=.714 is retired in favor of exact .8095238.
- Cross-task/species authority upgraded to v4/v2, including exact 001435 7-sequence de-duplication and same-contract HistGB/raw-history comparators.
- Exact-current-27 Virtual Agent q_diff audit added. q_diff gives small global fidelity gains but no decisive 27-animal paired improvement; do not overclaim.
- Virtual Block feature audit separates 13 current visual/social channels from 10 observer-intrinsic current channels and preserves learned/history state during the intervention.

## v17 additions — two-stage Virtual Mouse mechanism
- Virtual Block input ablation was run across all five folds and scored on exact 27 learners.
- Gross virtual observation does not collapse, matching the real Visual Block fact that observation amount is preserved.
- Virtual absolute APE increases strongly under current-social-input ablation; this is a diagnostic, not yet a neural claim.
- Real Visual Block selectively collapses future-feeding conversion.
- Exact-27 held-animal future-feeding audit shows belief, not policy alone, adds significant downstream predictive value.
- Virtual Mouse architecture is therefore frozen as two-stage: sampling policy -> belief-dependent feeding conversion.

## v18 additions — generative intervention closure
- Real Visual Block observation preservation was re-audited quantitatively.
- Two-stage Virtual Mouse now generates a belief-dependent downstream feeding probability.
- Five-fold exact-27 Virtual Block shows 26/27 lower feeding-conversion probability without observation collapse.
- Selective Active-belief update counterfactual reproduces the group-scale JAWS Active/Passive selectivity at an intermediate pre-specified lesion factor.
- Virtual intervention evidence is now separated into directional closure versus magnitude reproduction; current Virtual Block magnitude remains smaller than real data.

## Layer 4C. Artificial SLM Agent is now the primary generative framework

Authority:
- docs/SLM_ARTIFICIAL_AGENT_MAIN_FRAMEWORK_v1_20261003.md
- docs/SLM_ARTIFICIAL_AGENT_CURRENT_AUTHORITY_v1_20261003.md
- docs/SLM_FULL_CLOSEDLOOP_ARTIFICIAL_AGENT_v1_20261003.md
- docs/SLM_EVENT_MOTIF_TRANSITION_BENCHMARK_v1_20261003.md
- docs/SLM_MOTIF_STATE_ENVIRONMENT_v1_20261003.md
- docs/SLM_ARTIFICIAL_AGENT_MOTIF_ROLLOUT_v1_20261003.md
- results/SLM_closedloop_agent_global_v1.csv
- results/SLM_artificial_agent_benchmark_v1.csv
- results/SLM_motif_state_environment_paired_v1.csv
- results/SLM_agent_motif_rollout_global_v1.csv
- results/SLM_agent_motif_rollout_paired_v1.csv
- figures/SOE_ArtificialSLM_Agent_summary_v2.png/pdf/svg

The generative hierarchy is now:
real SOE -> formal SLM -> closed-loop Artificial SLM Agent -> motif/strategy emergence -> VTA correspondence -> causal lesions.

Full-SLM closed-loop:
- learning trajectory r=.7793 (highest structural correlation among baseline/Q/belief/SLM);
- Q has slightly lower trajectory RMSE (.1665 vs .1683), so do not claim a complete behavioral sweep;
- local outcome-conditioned kernel r=.3118 and RMSE=.08255, better than baseline, Q and belief;
- kernel sign agreement=.6213, highest among these mechanistic agents;
- generated outcome composition r=.9882.

Frozen v85 motif bridge:
- exact ANM4 D139 viewer QA gives 60/60 identical 1-based motif assignments under current projection;
- median t-SNE coordinate deviation=.333, mean=.467, max=2.13;
- current sklearn-version warning does not change motif identity on this exact audit.

Next-motif prediction:
- motif only log loss=1.9856;
- +action=1.9550, 39/40 animals improve, r_rb=.959, P=1.88e-10;
- +action+outcome=1.9382, 40/40 improve, r_rb=1, P=9.09e-13;
- +day is not robust and is not retained.

Artificial-agent motif rollout:
- occupancy JS: Full SLM .05201, Q .05367, belief .05417.
- Full SLM vs Q: 24/40 better, r_rb=.354, one-sided P=.0257.
- Full SLM vs belief: 25/40 better, r_rb=.402, one-sided P=.01295.
- edge JS: Full SLM .10434, Q .10651, belief .10782.
- transition matrix r is similar for Full SLM (.7328) and Q (.7335); this remains a boundary.

Interpretation:
Full SLM has a modest but reproducible advantage in generated behavioral-state occupancy/edge structure, while Q remains competitive for transition-matrix correlation.
The next high-value improvement is a fully motif-state-feedback artificial agent, not more Visual Block tuning.

Visualization:
five fold-specific Full-SLM viewer schemas and a frozen 12-motif viewer library are available for the existing two-panel Virtual mouse | Behavioral space renderer.

Visual Block and JAWS remain important but are now secondary artificial-agent perturbation modules rather than the definition of Virtual Mouse.

## Layer 4D. Generic recurrent artificial agent converges onto SLM coordinates

Authority:
- docs/SLM_GENERIC_RNN_SLM_CONVERGENCE_v2_20261004.md
- results/SLM_generic_RNN_per_animal_alignment_v1.csv
- results/SLM_generic_RNN_hidden_summary_v2.csv
- results/SLM_generic_RNN_policy_probe_fold_summary_v2.csv
- figures/SOE_GenericRNN_SLM_convergence_v2.png/pdf/svg

A generic actor-critic GRU was trained in a held-animal empirical 12-motif social world without SLM latent variables as inputs.

Artificial strategy alignment:
- motif occupancy r: .745 active-only reward; .757 Active+Passive reward.
- motif transition r: .528 and .533.
- motif-specific observation policy rho is weak, indicating the generic agent can organize the state space without reproducing every mouse policy detail.

SLM -> generic-GRU policy compression:
Adding explicit SLM coordinates to current motif strongly improves held-episode reconstruction of the GRU's learned action policy.

Across 5 folds x 3 independent seeds:
Active-only:
- mean Brier gain=.03283.
- mean NLL gain=.07499.
- mean AUC gain=.20966.
- 5/5 fold-averaged gains positive for all three metrics; r_rb=1; exact one-sided P=.03125.

Active+Passive:
- mean Brier gain=.03352.
- mean NLL gain=.07855.
- mean AUC gain=.22784.
- 5/5 fold-averaged gains positive for all three metrics; r_rb=1; exact one-sided P=.03125.

Thus a flexible recurrent agent can learn the task, but its learned policy is substantially more predictable when expressed in explicit SLM memory/belief coordinates.

GRU hidden-state probes:
- own policy is almost perfectly linearly decodable (R2 ~.997-.999).
- slow/fast SLM-like memory and Active belief are partially represented.
- Passive/Unrewarded belief is weaker.

Biological discriminator:
real VTA temporal authority remains:
- SLM Early +.810, Middle +.667, Post +.867.
- TinyRNN Early -.867, Middle -.548, Post +.733.
A flexible behavior model therefore does not reproduce the same temporally organized neural computation.

Interpretation:
SLM is not merely a competitor to a recurrent model.
It provides a compact mechanistic coordinate system for a generic learned artificial policy, and real VTA timing adjudicates which coordinates are biologically expressed.

## Layer 4E. Motif feedback is a frozen boundary

Authority:
- docs/SLM_MOTIF_FEEDBACK_BOUNDARY_v1_20261004.md

Hard replacement of continuous policy state by generated 12-motif state degrades global trajectory fidelity.
A motif-specific residual policy adapter creates tradeoffs but no simultaneous global/local improvement.

Generated motif is therefore retained as an emergent strategy/world-state readout driven by SLM action/outcome, not promoted as a second policy controller.

This prevents unnecessary expansion into a physical-body world model that is not required for the SLM claim.

## Visualization update

Representative session selection is now rule-based rather than cherry-picked.
Among held-out learner sessions with >=80 events, SocialFeeding_DMS:ANM139:D10 is closest to the cohort median occupancy/transition fidelity.

Authority:
- results/SLM_artificial_viewer_representative_candidates_v1.csv
- figures/SOE_Real_vs_ArtificialSLM_ANM139_D10_v2.png/pdf/svg

ANM4 D139 remains useful for exact viewer/projection QA but is not the representative science session.


## Layer 4D. Biological meaning of the Artificial SLM Agent

Authority:
- docs/SLM_AGENT_BIOLOGICAL_MEANING_v1_20261004.md
- docs/SLM_REAL_VS_AUTONOMOUS_LATENT_GEOMETRY_v1_20261004.md
- results/SLM_real_vs_autonomous_latent_metrics_v1.csv
- results/SLM_real_vs_autonomous_outcome_profiles_summary_v1.csv
- results/SLM_real_vs_autonomous_dayprofile_summary_v1.csv
- figures/SOE_ArtificialAgent_biological_meaning_v1.png/pdf/svg

Two agent classes must remain conceptually separate.

### Mouse-derived Artificial SLM Agent
The SLM policy/update mechanism is estimated from real mouse SOE and placed back into a held-animal social-foraging world.

Question:
Are mouse-derived social-learning computations sufficient to regenerate social-information sampling and behavioral-state organization?

This is a mechanistic-sufficiency / generative-validation test.
It is not an independently reward-trained AI model.

### Generic recurrent RL agent
A generic GRU actor-critic is trained in the empirical 12-motif world without explicit SLM latent inputs.

Action:
Observe vs No-observe.

Reward objectives:
- Active-only social reward;
- Active + Passive food reward;
with observation cost.

Question:
Will a flexible learner solving the same social-information acquisition problem independently converge onto a policy describable by SLM coordinates?

All 30 fold x seed x reward runs improve Brier/NLL/AUC when SLM coordinates are added to current motif.

### Biological task interpretation
The current agent models the social-information sampling / social-learning controller embedded in social foraging.

Preferred label:
Artificial social-information sampling agent embedded in an empirical social-foraging world.

Do not call it a complete virtual mouse or a complete simulation of social foraging.
Feeding is biologically central and enters the reward/outcome structure, but it is not yet a free native action in the primary motif-world agent.

### Real vs autonomous computational geometry
The same five-fold Full-SLM contract was replayed on real held-out mouse trajectories and autonomous artificial trajectories.

Animal-level Real vs Artificial:
- mean policy: rho=.7887, P=1.50e-9;
- mean absolute APE: rho=.4966, P=.00112;
- mean RPE: rho=.7707, P=5.98e-9;
- mean absolute Active-belief update: rho=.7341, P=7.00e-8.

Outcome-specific profile agreement:
- APE median profile r=.899;
- RPE median profile r=.99999;
- Active-belief update median profile r=.9936.

Day-wise profiles:
- policy positive in 87.5% animals; median rho=.512;
- Active-belief-update positive in 90%; median rho=.286.

Interpretation:
The artificial world regenerates substantial real-mouse computational geometry, not merely surface motif occupancy.

### VTA bridge
The artificial agent is not claimed to simulate dopamine.
The non-circular biological bridge is:

1. Artificial SLM regenerates real-mouse policy / APE / reward-update geometry.
2. Frozen real VTA independently expresses:
   - Early policy: r_rb=.810;
   - Middle APE: rho=.667;
   - Post reward/update: r_rb=.867.
3. Generic behavioral alternatives do not reproduce the same three-stage temporal sequence.

Preferred claim:
The Artificial SLM Agent regenerates computational variables whose temporally distinct expression is independently observed in VTA.

## Layer 4E. Autonomous-world slow individual state

Confirmatory folds 1-4, n=32:
- D1-derived slow calibration improves D2+ trajectory r .480 -> .508.
- D2+ trajectory RMSE .23114 -> .22576.
- 20/32 animals improve RMSE; r_rb=.468; one-sided P=.0110.
- observation-rate absolute error improves modestly; one-sided P=.0481.
- kernel and motif occupancy do not reliably improve.

Interpretation:
slow state helps cross-day individual calibration but does not solve local dynamics.
Do not inflate this into a new broad mechanism.

## Layer 4F. Social-information foraging is now the biological entry point for the Artificial Agent

Authority:
- docs/SOE_RESULTS_ARTIFICIAL_AGENT_v1_20261004.md
- docs/SOE_MAIN_TEXT_RESULT_ORDER_v3_20261004.md
- docs/SOE_ARTIFICIAL_AGENT_MAIN_FIGURE_LEGEND_v1_20261004.md
- docs/SLM_REAL_VS_ARTIFICIAL_VIEWER_v1_20261004.md
- figures/SOE_SocialInformationForaging_ArtificialAgent_main_v1.png/pdf/svg

### Real-mouse information value
Full social state:
- 22/27 learner animals have positive social information value;
- median +.003654 nats/decision;
- rank-biserial=.7249;
- P=.0002678.

Learning dependence:
- late minus early median=-.003783 nats/decision;
- r_rb=-.619;
- P=.001939.

Behavioral-state dependence:
- DEM not feeding, far vs near own spout: 24/27 expected direction, r_rb=.905, P=1.885e-6.
- DEM feeding, far vs near: 22/27, r_rb=.593, P=.00297.

Interpretation:
the observer does not merely have a fixed tendency to watch another mouse.
The decision value of social information varies with learning stage and current behavioral state.
This motivates the Artificial Agent as an information-sampling controller.

### Task-return / SIP boundary
State-targeting gain is positive for many policies, including simple baselines.
It supports the claim that observation can have state-dependent task value but is not SLM-specific evidence.

Social Information Performance (SIP) is positive in learners but is also present in non-learners and is not currently linked to canonical SRI.
Do not promote SIP as a replacement for SRI or as a primary SLM result.

### Two distinct agents
Mouse-derived Artificial SLM:
- fitted from real mouse computation;
- generative sufficiency test.

Generic GRU:
- independently reward-trained in the empirical motif world;
- computational convergence test.

Do not collapse these into one "AI mouse."

### Real vs Artificial viewer
A 70-s QA movie now displays:
- real framewise Virtual Mouse behavior;
- exact real v85 t-SNE trajectory;
- Artificial-SLM event-level generated motif state;
- generated action/outcome/policy/APE.

No framewise Artificial-SLM motor trajectory is imputed.

### Manuscript result logic
Result 2 now begins with adaptive social information value, then asks whether a mouse-derived SLM is sufficient to generate the organization of information sampling.
Result 3 uses the generic recurrent learner as an independent convergence system.
Result 4 connects real-versus-artificial latent geometry to independent VTA temporal encoding.
Result 5 applies Visual Block and JAWS as information/update lesions.


## Layer 4G. Autonomous intervention closure — information efficacy vs Active-belief teaching

Authority:
- docs/SLM_AUTONOMOUS_INTERVENTION_CLOSURE_v1_20261004.md
- docs/SOE_RESULTS_ARTIFICIAL_AGENT_v2_20261004.md
- results/SLM_autonomous_intervention_QA_v1.json
- results/SLM_autonomous_lesions_paired_effects_v1.csv
- results/SLM_autonomous_lesions_behavior_paired_v1.csv
- results/SLM_autonomous_lesions_behavior_scoped_global_v1.csv
- results/SLM_autonomous_rep_convergence_v1.csv
- figures/SOE_ArtificialSLM_intervention_mapping_v2.png/pdf/svg

Five held-animal folds; ten paired autonomous rollouts per mode. Primary manuscript inference unit is the 27 learner animals; all 40 animals are robustness.

### Visual Block analogue
Real VB collapses SRI but preserves gross observation.
Autonomous sensory mask:
- observation .4463 -> .4692; r_rb=+.407; P=.0655;
- Active contingency .0940 -> .0856; 27/27 lower; r_rb=-1; P=1.49e-8;
- Active-belief mean .0450 -> .0376; r_rb=-.767; P=.000209;
- direct |delta Active-belief| update magnitude unchanged, P=.258;
- direct |delta Q| magnitude unchanged, P=.972.
Trajectory fidelity decreases (r_rb=-.619, P=.00388), whereas local kernel r does not reliably change (P=.594).

Interpretation: social observation can remain behaviorally expressed while losing efficacy for creating Active contingency and learned Active social value.

Belief-gate and full-information-gate manipulations reduce observation strongly and are therefore over-lesion controls rather than the preferred VB mechanism.

### JAWS50
Selective Active-outcome belief learning efficacy is reduced to 50%.

Direct update magnitude:
- |delta B_Active| .003308 -> .002577: -22.1%, 27/27 lower, r_rb=-1, P=1.49e-8.
- |delta Q| .001835 -> .001825: -0.55%.
- fractional attenuation is ~39.9x larger for Active-belief than Q updating.

Closed-loop:
- Active-belief mean .0450 -> .0413; r_rb=-.587; P=.00645;
- Active contingency .0940 -> .0946; P=.0521, approximately preserved;
- global trajectory-r change ~0; r_rb=-.016; P=.953;
- local strategy-kernel r decreases; r_rb=-.582; P=.0070.

Large signed-rank effects can occur for tiny consistent changes. Pathway specificity must report raw magnitude together with bounded effect and P.

### Computational double dissociation
Sensory lesion:
- Active contingency DOWN;
- Active belief DOWN;
- direct Active-belief update magnitude preserved;
- gross observation preserved.

JAWS-like teaching lesion:
- direct Active-belief update magnitude DOWN;
- Active belief DOWN;
- Active contingency approximately preserved;
- global behavior preserved more than local social strategy.

Preferred claim: information efficacy and contingency-specific social-value updating are separable operations within the same intact SLM.

### Stochastic posterior-predictive audit
Same frozen intact model, trajectory r after averaging:
1 rollout=.400; 2=.495; 3=.532; 5=.578; 10=.622.
RMSE decreases monotonically.
The higher 10-rollout value is a lower-noise posterior-predictive estimate, not a model change.

Learner-only ten-rollout control:
trajectory r=.6377; RMSE=.2141; kernel r=.4440; kernel RMSE=.0727; motif occupancy r=.8643; JS=.0390.

## Layer 4H. Artificial cooperation precedent mapping

Authority:
- docs/SLM_AGENT_HONG_SCIENCE_MAPPING_v1_20261004.md

Use the Jiang/Hong evidence architecture rather than claiming the tasks are the same:
task world -> independently trained recurrent learner -> emergent strategy -> social-information/value representation -> information removal -> internal-component perturbation.

SOE adds a mouse-derived Artificial SLM sufficiency layer and independent VTA temporal grounding.

Do not conflate training an agent without social information with acutely removing information from an already learned controller.

## Layer 4I. Virtual-SRI guardrail

Canonical target_sri is carried from the real dataset and is not natively generated by the event-level Artificial SLM simulator.

Do not invent an ad-hoc virtual ratio and label it SRI.
Use Active contingency, Active-belief state/update, trajectory fidelity, local strategy kernel, and motif occupancy as artificial-agent endpoints.
