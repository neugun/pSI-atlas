# SOE MASTER RESULTS INVENTORY v1 - 2026-10-02

Purpose: preserve the complete Social Observational Eating / social-foraging evidence chain before manuscript and GitHub integration.

Status labels:
- CURRENT_VERIFIED: current audited source/output exists and can be used now.
- CURRENT_SUPPORT: valid supportive result, not a primary confirmatory claim.
- HISTORICAL_RECOVERED: previously reported positive result that must remain in the story; source/stat lineage should be pinned before final publication.
- LEGACY_MANUSCRIPT_CONTROL: established control in the manuscript/progress-report lineage; retain, then re-audit exact source data during manuscript integration.
- INVALID_OLD_LINEAGE: superseded or contaminated analysis; do not cite.
- GUARDRAIL: result prevents overclaiming.

## Global scientific problem
SOE asks how a mouse converts socially observed evidence into adaptive food-seeking:
social cue -> active observation/sampling -> accumulated history/state -> action policy -> reward/outcome update -> future behavior.

The current mechanistic formulation is:
structured Social Learning Model (SLM: Actor-Critic + state-conditioned APE + action-conditioned reward belief/value) plus a generic choice-persistence branch.
Behavior alone is computationally underdetermined; VTA dopamine timing and causal VTA inhibition adjudicate the structured branch.

Primary behavioral cohort for current models: 27 learners.
Supplementary learner/non-learner cohort: 27 learners + 13 non-learners (40 animals).
Current main behavior model table: 68,624 held-animal events in the 27-learner contract.
Current photometry authority: 9 principal DA animals, with analysis-specific n=6-9.
Current JAWS combined causal authority: n=10 animals (5 Standard JAWS + 5 VTA-copy JAWS).
## 1. Task acquisition and social contingency

### 1.1 Acquisition of socially guided eating
Status: LEGACY_MANUSCRIPT_CONTROL + HISTORICAL_RECOVERED.
Question: does social reward coordination emerge with training rather than exist intrinsically?
Core result:
- about 60% of observer mice learned the contingency across approximately two weeks.
- older progress-report lineage: SRI 0.67 +/- 0.34 to 2.82 +/- 0.44 by days 11-14, n=13 pairs, repeated-measures ANOVA P<.001.
- later strict 40-animal analysis reported learner SRI approximately 1.07 -> 4.58 (delta +3.51).
Interpretation: socially guided eating is acquired, not a trivial baseline synchrony effect.
Action for manuscript integration: reconcile cohort/stat-number differences across manuscript versions before final text.

### 1.2 Simulated demonstrator control
Status: LEGACY_MANUSCRIPT_CONTROL.
Question: is task performance driven by a live conspecific rather than apparatus/reward-delivery cues?
Result: simulated demonstrator SRI approximately 0.4994 +/- 0.2584, n=13 pairs, P<.001 vs live demonstrator.
Interpretation: live social information is required.

### 1.3 Visual access
Status: LEGACY_MANUSCRIPT_CONTROL + CURRENT behavior support.
Opaque-barrier historical control:
- SRI decreased about 69%, n=16 pairs, P<.001.
Newer Visual Block analysis:
- SRI approximately 3.67 -> 1.08, 23/25 animals decreased, P about 2e-6.
- observation frequency/duration/occupancy were not globally suppressed.
Interpretation: vision is required for successful social coordination, not merely for generating observation-like behavior.
## 2. Familiarity and social identity

### 2.1 Familiar versus unfamiliar demonstrator
Status: LEGACY_MANUSCRIPT_CONTROL.
Question: does social identity/familiarity matter beyond generic visual motion?
Historical result:
- replacing the familiar cage-mate with an unfamiliar same-sex conspecific reduced SRI by about 44%, n=11 pairs, P<.05.
Interpretation: social information is weighted by partner familiarity/identity.

### 2.2 Familiarity x state ambiguity
Status: CURRENT_SUPPORT.
New analysis: results/familiarity_ambiguity/.
Contract:
- primary JAWS animals ANM98/103/109/111/112.
- familiar day 20 versus unfamiliar day 21.
- behavioral-state matching on geometry/kinematics; ambiguity defined from a classifier trained on the core SOE state.
Result:
- 343 matched pairs.
- high-minus-low ambiguity familiarity effect mean +0.1268, median +0.122.
- 3/5 animals positive, Wilcoxon P=.3125.
Interpretation: directionally, familiarity may matter more in ambiguous states, but n=5 does not establish the interaction.
Do not use this to replace the original familiarity effect; keep it as exploratory ED support.
## 3. Social observation behavior and behavioral motifs

### 3.1 Pose-derived social observation
Status: LEGACY_MANUSCRIPT_CONTROL / HISTORICAL_RECOVERED.
Input:
- SLEAP/pose features; older manuscript used 132 observer+demonstrator features in the 3 s before observer feeding.
Key findings:
- demonstrator feeding/spout features are highly predictive.
- observer pose/social-orientation features are the next strong category.
- five observer features (head direction, facing, angular velocity, social turn, social gaze) nearly match the all-feature classifier.
- social gaze is the strongest single observer-side predictor in the manuscript lineage.
Interpretation: rewarded social observation is an active orienting strategy, not passive proximity.

### 3.2 Observation classifier / contra-observation
Status: HISTORICAL_RECOVERED.
Later manuscript lineage used manually labeled pose/social-interaction frames and XGBoost to infer social observation and contra-observation.
Reported findings:
- observation rate increases across training.
- observation bout duration decreases modestly.
- observation rate is positively associated with SRI (P<.001).
- contra-observation does not show the same learning relationship (reported P=.11).
- observation remains associated with SRI after controlling contra-observation.
Interpretation: learning refines where/when observation is deployed rather than globally increasing sociality.

### 3.3 Unsupervised motif/state manifold
Status: HISTORICAL_RECOVERED; exact current source/stats must be pinned.
Result lineage:
- successful active-reward bouts are preceded by distinct behavioral states.
- global behavioral manifold remains broadly stable across learning.
- cluster occupancy is reweighted with training.
Interpretation: reinforcement reweights existing sensorimotor states toward socially informative motifs rather than creating an entirely new repertoire.
## 4. Learner versus non-learner behavior

### 4.1 Strict cohort
Status: HISTORICAL_RECOVERED.
Earlier strict contract:
- 40 animals: 27 learners, 13 non-learners.
- approximately 541 sessions and 102,322 strict events.
- 9 FP sessions reserved for neural adjudication in that analysis lineage.
Primary current predictive modeling remains learner-only; non-learners are supplementary contrasts.

### 4.2 Observation-to-feeding conversion
Status: HISTORICAL_RECOVERED; source pin required.
Earlier strict result:
- learner observation->feeding conversion approximately .431 -> .641 across learning.
- learner conversion progress beta about +.126 versus non-learner -0.097.
- group P about .00147.
- conversion progress correlated with delta SRI: rho about .426, P=.0086.
- observation-rate correlation with delta SRI was near zero (rho about .037).
Interpretation: successful learners improve the conversion of sampled social information into adaptive action, not simply the amount of observation.

### 4.3 Outcome-dependent stopping/sampling
Status: HISTORICAL_RECOVERED; source pin required.
Learner-only result:
- Active minus Unrewarded stopping difference: +5.9 percentage points at events 6-20 (P=.0096), +11.6 pp at 21-50 (P=1.9e-5), +10.7 pp at 51+ (P=1.3e-6).
- Passive stopping difference at 21-50: +17.6 pp (P=2.1e-7).
Interpretation: observation policy becomes outcome-sensitive during learning.
## 5. Behavioral prediction and model hierarchy

### 5.1 Simple baselines - CURRENT_VERIFIED
Same 27 learners / 68,624 held-animal events:
- Constant prevalence: Brier .256073, AUC .377565, Brier skill 0.
- Clock only: .244924, .581658, skill .0435.
- Previous choice only: .228180, .613424, skill .1089.
- Current linear: .194191, .771429, skill .2417.
- Current nonlinear: .185812, .790933, skill .2744.

These worse baselines MUST remain visible. They establish that the task requires more than prevalence, time, previous choice, or instantaneous geometry alone.

### 5.2 Classical low-dimensional RL baselines - CURRENT_VERIFIED
Separate restricted-input contract:
- Rescorla-Wagner: Brier .244263, AUC .578426.
- WSLS: .237987, .621375.
- Q-active: .217536, .710050.
- Q-all: .211365, .728705.
- asymmetric Q: .212843, .722418.
- forgetting Q: .203686, .749394.
- choice kernel: .190135, .781354.
- Q + choice kernel: .190398, .780822.
SLM full beats all eight in 27/27 animals under this restricted-input contract (paired r_rb=+1, P=1.49e-8 for Brier comparisons).
Guardrail: do not call these input-matched to SLM because SLM has richer current-state information.
### 5.3 Mechanistic SLM and input-matched strong controls - CURRENT_VERIFIED
- Direct policy Brier .170994, AUC .823191.
- Common belief .171093, .823163.
- Actor-Critic .171063, .823088.
- Feature-Q .170891, .823558.
- SLM full .170824, .823320.
Thus SLM is much stronger than the simple/current and low-dimensional RL baselines.

Input-matched strong alternatives:
- Current + choice kernel .166401, AUC .832245.
- Current + Q+choice kernel .166666, .831513.
- Current + forgetting-Q .172217, .820855.

Black-box/capacity controls:
- TinyRNN h3 Brier .168031.
- Current + full-history MLP .164749.
- History MLP + formal-all .163722.
Do not claim SLM is the top behavioral predictor.

### 5.4 Parsimonious two-branch behavioral head - CURRENT_VERIFIED
SLM + choice-kernel OOF meta-stack:
- Brier .165411, AUC .834084, log loss .499881.
- beats SLM: 26/27, r_rb=.942, P=8.20e-7.
- beats input-matched CK: 20/27, r_rb=.667, P=.00169.
- beats TinyRNN h3: 23/27, r_rb=.862, P=1.59e-5.
- statistically indistinguishable from full-history MLP: r_rb=-.079, P=.732.
- recovers 96.9% of Current->full-history-MLP gain and 92.4% of Current->best-history-model gain.
Interpretation: most useful behavioral history separates into structured social learning + generic persistence.
## 6. Learning-stage changes in computation

### 6.1 Rich-history advantage grows late
Status: CURRENT_VERIFIED.
Relative to Feature-Q:
- TinyRNN h3 gain is larger D10+ than D1-4: r_rb=.434, P=.0491.
- History MLP + formal-all: r_rb=.508, P=.0200.
- Formal + external ensemble: r_rb=.534, P=.0140.
Interpretation: richer history/state information becomes more valuable later in learning.

### 6.2 Decomposition of history
Status: CURRENT_SUPPORT.
Action-history gain over Current nonlinear:
- early .01827 -> late .02277.
Full-history gain:
- .01742 -> .02271.
Action-nonlinearity:
- .00543 -> .00825.
Full-nonlinearity:
- .00466 -> .00833.
Outcome-history alone remains weak/negative.
Component-specific early-late tests are not individually significant.
Interpretation: the strong late effect is better framed as flexible-history/model gain, not one isolated component.

### 6.3 Learner/non-learner SLM gain
Status: CURRENT_VERIFIED GUARDRAIL.
Do NOT claim SLM behavioral prediction is learner-specific.
Between-group learner-vs-nonlearner differences in SLM gain are not significant across the main day bins.
The strongest learner-linked SLM result is neural APE x SRI, not binary behavioral model gain.
## 7. Prospective action / future feeding

### 7.1 Observation predicts future feeding after controls
Status: HISTORICAL_RECOVERED; source pin required.
Earlier held-animal analysis:
- adding Observe improved prediction of feeding in the next 10 s in 18/27 animals, P=.028.
- adding policy/belief components improved in 18/27, P=.021.
- raw P(feed | Observe) about 7.9% versus P(feed | NoObserve) about 11.3%.
Interpretation: Observation is an information-sampling action rather than a direct motor command to feed; its predictive value appears after accounting for state/context.

### 7.2 Policy and value contributions across learning
Status: HISTORICAL_RECOVERED.
Earlier learner-only analysis reported policy latent ablation increasing from approximately 0 to 1.39 percentage points, 27/27 animals, P about 1.5e-8.
A later decomposition found late policy contribution negative relative to its comparator (-0.90 pp) while all-reward Q contributed +1.71 pp; direct policy-vs-Q ranking was not significant (P=.155).
Interpretation: policy and value contributions reweight across learning; do not force a single monotonic policy story.
## 8. VTA dopamine - descriptive biological results

### 8.1 Demonstrator state / food-zone context
Status: HISTORICAL_RECOVERED; retain as biological context and re-audit exact current source.
Earlier analysis:
- observer DA is elevated when the demonstrator is in the food zone and lower/suppressed outside.
- demonstrator feeding-spatial, posture, social proximity, velocity and turning features contribute to observer DA.
- learner coupling is substantially stronger, especially for demonstrator-inside-food-zone epochs.
Historical GLM example: Learner Inside R2 about .235 with 4/14 LASSO features; non-learner All about .06 and Outside about .07.
Interpretation: DA reflects socially relevant demonstrator state, not reward delivery alone.

### 8.2 Social gaze and DA
Status: HISTORICAL_RECOVERED.
Manuscript lineage:
- observer-initiated social gaze evokes a VTA DA increase.
- observer gaze response exceeds demonstrator-gaze response.
- active-reward eating preceded by social gaze shows greater DA than eating without prior social gaze.
Interpretation: DA is linked to active social information acquisition and socially coordinated reward.

### 8.3 Non-learners
Status: GUARDRAIL.
Do not portray non-learners as having flat or absent outcome DA.
Earlier interpretation: outcome/reward responses may remain intact while social credit assignment or updating fails.
## 9. VTA dopamine - current mechanistic adjudication

### 9.1 Early-session Observation policy
Status: CURRENT_VERIFIED.
Held-block CV:
- n=6 evaluable animals.
- Actor policy median MSE gain +1.94%.
- 5/6 positive.
- r_rb=.810.
- exact one-sided P=.046875.
Classical controls:
- Q-all r_rb=.048, P=.50 one-sided.
- choice-kernel r_rb=-.238, two-sided P=.688.
- Actor policy + CK does not improve the signal.
Interpretation: early-session Observation DA carries structured sampling/policy information.

### 9.2 Middle-session learner-dependent APE
Status: CURRENT_VERIFIED.
Frozen 40-60% session window:
- n=8.
- rho(APE-DA coupling, SRI)=.667.
- exact permutation P=.04157.
- partial APE given CK error remains rho=.667, P=.04157.
- reverse CK given APE rho=-.333, P=.805.
- same result after Q+CK and Q-error controls.
Interpretation: learner-dependent APE is not reducible to generic persistence/error.

### 9.3 Post-outcome update
Status: CURRENT_VERIFIED.
- Actor-Critic RPE r_rb=.867, P=.01953.
- belief surprise/update r_rb=.956, P=.00586.
- time-residualized CK error r_rb=.467, P=.25.
- CK surprise r_rb=-.022, P=1.
Interpretation: reward-specific critic/belief updating explains post-outcome DA better than generic choice error.
### 9.4 Raw photometry timing support
Status: CURRENT_SUPPORT.
Lineage-clean saved-trace animals: 3,4,5,18,19,27,35 (n=7).
Early-policy raw_z2:
- pre [-1,0] mean beta .0984, median .1917, 5/7 positive.
- onset [0,1] mean beta .0615, median .0633, 5/7 positive.
Cluster-corrected time-resolved tests are not significant.
Phase-normalized 5%-30% early window: mean policy beta .1229, median .1102, 6/7 positive.
Interpretation: supports timing/direction; does not independently establish a continuous significant cluster.

### 9.5 Longitudinal Day1-to-late DA
Status: CURRENT_SUPPORT, small n.
Paired animals ANM18/19/35:
- Observation-aligned changes are heterogeneous.
- lick/outcome integrated activity increases late in 3/3 for 0-1 s and 0-2 s means.
Use only as longitudinal support, never to convert within-session early/mid DA results into a longitudinal three-stage story.

### 9.6 Behavior-DA bridge
Status: EXPLORATORY_SMALL_N.
Six-animal overlap:
- MLP gain beyond Feature-Q vs qAll-RPE DA gain rho=.886, n=6, P=.0188.
- late-history gain vs qAll-RPE DA gain rho=.543, P=.266.
Interpretation: hypothesis-generating link between animals needing richer behavioral history and stronger DA outcome-update readout.
## 10. Visual Block behavior and dopamine

### 10.1 Behavioral zero-shot degradation
Status: CURRENT_VERIFIED.
Same-14 model comparison:
- Feature-Q all-reward: Visual Block worsens Brier, r_rb=.695, P=.0203.
- policy_active: r_rb=.676, P=.0245.
- statevalue Actor all-reward: r_rb=.676, P=.0245.
- full-history MLP: r_rb=.733, P=.0134.
Input-matched Current + Choice-kernel zero-shot:
- Brier degradation r_rb=.829, P=.00403.
- NLL degradation r_rb=.867, P=.00232.
- AUC degradation itself not significant.
- CK AUC degradation scales with SRI loss: rho=.600, permutation P=.0272.
Interpretation: Visual Block removes socially informative structure across model classes; it is not an SLM-specific failure.

### 10.2 Clean raw-photometry rebuild
Status: CURRENT_VERIFIED.
The old Visual Block DA table is INVALID_OLD_LINEAGE because Original and VB sessions could resolve DA from the same shared signal directory.
Clean rebuild uses each session's own continuous Feeding_OFF_signals_SFmatch_8.mat, local -3 to 0 s baseline, and remapped bout timing.
Coverage: 9 Original + 9 VB sessions, 5,347 observation bouts.

### 10.3 Clean Visual Block DA
Status: CURRENT_VERIFIED / SUPPORTING_CONTROL.
Sustained observation DA:
- Original Early-to-Middle increase: r_rb=-.778 for Early-Middle contrast, P=.0391 (Middle > Early).
- Visual Block Early-to-Middle: P=.164.
- condition x phase interaction P=.359; do not claim formal flattening.
Early sustained Original > VB:
- 8/9, r_rb=.733, P=.0547 (directional).
Demonstrator-feed locked 0-6 s DA, Original > VB:
- Early: 8/9, r_rb=.867, P=.01953.
- Middle: 7/9, r_rb=.689, P=.0742.
- Late: 6/9, r_rb=.511, P=.203.
Interpretation: visual access most strongly modulates early demonstrator-feed-locked DA; the effect weakens later in-session.
## 11. VTA inhibition / JAWS

### 11.1 Behavioral endpoint
Status: CURRENT_VERIFIED.
Contingent Laser ON vs OFF:
- SRI 1.880 -> .786; delta -1.094.
- 9/10 lower; r_rb=-.927; P=.00586.
- gross observation rate unchanged (P=.736 in the original endpoint analysis; continuous replay observation fraction P=.625/.922 depending normalization/contrast).
- mean bout duration unchanged.
- Active real rewarded-observation ratio 25.20% -> 15.59%, delta -9.61 percentage points, P=.01172.
- real-minus-shuffle numerator delta -5.667, P=.00586.
Interpretation: inhibition disrupts contingency-sensitive rewarded social observation while preserving gross sampling.

### 11.2 Causal SLM latent
Status: CURRENT_VERIFIED.
Acute contingent:
- Active belief r_rb=-1.000, P=.00195.
- Active-specific belief r_rb=-.927, P=.00586.
- Active Q r_rb=-.956, P=.00781.
- Passive belief P=.275.
Continuous exact per-event:
- Active belief r_rb=-.927, P=.00586.
- Active Q r_rb=-.733, P=.0547.
- CK update r_rb=+.164, P=.695.
Session scale:
- Active belief r_rb=-.964, P=.00391.
Interpretation: Active social-reward belief is the most reproducible cross-scale causal coordinate.
### 11.3 Independent JAWS cohort direction
Status: CURRENT_SUPPORT.
Continuous contingent Active-belief update:
- Standard JAWS 5/5 negative, mean about -.00403; P=.0625 (n=5 resolution).
- VTA-copy JAWS 5/5 negative, mean about -.00258; P=.0625.
- combined 10/10, P=.001953.
This is useful replication/direction evidence across the two causal cohorts.

### 11.4 Continuous state dynamics
Status: CURRENT_VERIFIED.
Contingent:
- OFF episodes build Active belief: mean +.002490, P=.001953 vs zero.
- ON episodes reverse Active-belief updating: mean -.000815, 9/10 negative, P=.02734.
- Active-Q remains positive but accumulates more slowly ON than OFF.
Noncontingent:
- OFF builds Active belief.
- ON largely neutralizes accumulation rather than showing the same clear negative update.
Guardrail: formal contingent-vs-noncontingent latent interaction is not significant; describe state-sign pattern, do not overclaim interaction.

### 11.5 Immediate-next-choice / slow-history controls
Status: GUARDRAIL.
Immediate lag1-5 observation-update kernel does not show a robust contingent effect.
Simple gamma=.95 slow-credit history also does not establish a condition interaction.
Interpretation: DA inhibition is not simply controlling the immediately next observation choice or one simple exponentially decayed behavioral history.
## 12. Generalization beyond the trained feeding contingency

### 12.1 Food neophobia
Status: LEGACY_MANUSCRIPT_CONTROL / HISTORICAL_RECOVERED.
Socially trained mice subsequently approach/eat novel sunflower seed faster and spend longer eating than nonsocial visual-cue controls after observing a demonstrator.
Manuscript figure lineage reports n=12/6 pairs for social/control.
Exact final statistics should be pinned during manuscript integration.
Interpretation: training changes use of social information beyond the original SOE motor contingency.

### 12.2 Observational fear
Status: HISTORICAL_RECOVERED.
Socially trained observers show stronger behavioral responses during demonstrator shock observation:
- greater velocity reduction,
- stronger orientation toward demonstrator,
- increased social observation during shock.
No increase in prosocial allogrooming.
Interpretation: transfer is selective to observational use of social information, not general affiliative behavior.
Keep separate from the core SOE mechanism unless manuscript scope includes generalization.

## 13. External task/species support
Status: EXTERNAL_SUPPORT.
Mouse cooperative task: social history adds held-out predictive value.
Macaque Actor/Observer task: explicit multiscale and recurrent history improve held-session prediction; recurrent hidden state decodes role-specific history.
Human same task family: multiscale history robustly improves held-subject calibration; recurrence adds discrimination.
Rat DANDI 001169: explicit multiscale history improves Brier (7/10, r_rb=.745, P=.0371); TinyRNN is not significant vs baseline and is worse than explicit multiscale in 9/10 (r_rb=-.855, P=.0137).
Use these as generalization/boundary evidence, not as proof of identical mouse neural coordinates.
## 14. Results that disappeared from recent narrow authorities and must be restored

Restore to the master narrative/inventory:
1. task acquisition and SRI learning curve.
2. simulated-demonstrator control.
3. opaque-barrier / visual-dependence behavior.
4. unfamiliar-demonstrator / familiarity effect.
5. pose/social-gaze result and five-feature compression.
6. observation-rate vs contra-observation specificity.
7. unsupervised motif occupancy reweighting.
8. learner observation-to-feeding conversion.
9. outcome-dependent stopping/sampling.
10. future-feeding prediction from Observe/latents.
11. demonstrator food-zone/feature coupling to DA.
12. social-gaze-evoked DA.
13. Visual Block clean raw-DA effects.
14. Standard JAWS and VTA-copy cohort replication.
15. food-neophobia and observational-fear transfer.
16. simple and classical baseline models that are clearly worse than SLM.

Reason they disappeared:
- recent checkpoints were intentionally narrowed around SLM-vs-alternatives neural adjudication.
- several old results were not copied into the new authority files.
- old Visual Block DA was correctly removed because of a signal-lineage bug, but valid behavior/clean-DA results should have been restored separately.
- familiarity ambiguity and some older analyses existed on Titan but were not synchronized into the main H-drive authority.
## 15. Main narrative hierarchy for the next manuscript/GitHub step

Layer 1 - establish the phenomenon:
SOE acquisition -> live-social specificity -> visual dependence -> familiarity dependence.

Layer 2 - define the learned behavioral strategy:
pose/social gaze -> observation specificity -> learner conversion -> outcome-sensitive sampling -> motif occupancy reweighting.

Layer 3 - computational explanation:
simple baselines -> classical RL baselines -> SLM components -> SLM full -> input-matched persistence -> SLM+CK two-branch head -> black-box capacity ceiling.

Layer 4 - neural adjudication:
descriptive social-state DA -> early policy -> middle learner-dependent APE -> post-outcome RPE/belief -> raw timing/longitudinal support.

Layer 5 - causal test:
JAWS preserves gross sampling but reduces SRI/reward coupling -> Active-belief/Active-Q causal effects -> cross-scale continuous/session replication -> Standard and VTA-copy direction replication.

Layer 6 - condition tests:
Visual Block behavior -> clean Visual Block DA -> familiarity and ambiguity.

Layer 7 - generalization/boundaries:
food neophobia / observational fear -> cooperative/macaque/human/rat external support.

The eventual GitHub page should expose for every layer:
question -> cohort/input -> preprocessing -> model/statistic -> output -> bounded effect size -> figure -> conclusion -> guardrail -> source file.
## 16. Frozen metric policy
For paired-animal/session inference:
- report raw/native quantity.
- report rank-biserial r_rb in [-1,1].
- report paired Wilcoxon/exact P.
- report n and directional counts.
For independent groups:
- Cliff delta in [-1,1].
For correlations:
- retain Spearman rho in [-1,1].
For predictive models:
- Brier, Brier skill, AUC, centered AUC, log loss/log-loss skill; add RMSE/R2 only when target is continuous.
Never numerically rescale small latent variables merely to make the raw number look larger.

## 17. Current files to treat as authority
- rl_model2_20261001/SOE_CURRENT_CHECKPOINT_v8_20261002.md
- rl_model2_20261001/SOE_CURRENT_FIGURE_MANIFEST_v5_20261002.csv
- rl_model2_20261001/social_learning_unification_20261002/SOE_GLOBAL_EFFECT_SIZE_REGISTRY_v8.csv
- rl_model2_20261001/social_learning_unification_20261002/SLM_maintext_stratified_model_panel_v4.csv
- rl_model2_20261001/SOE_DA_SAMESESSION_VISUALBLOCK_AUTHORITY_20261002.md
- rl_model2_20261001/social_learning_unification_20261002/SLM_JAWS_TWO_TIMESCALE_AUTHORITY_v4_20261002.md
- rl_model2_20261001/social_learning_unification_20261002/SLM_MODELZOO_LEARNER_JAWS_AUTHORITY_20261002.md
- results/familiarity_ambiguity/summary.json

This inventory supersedes narrow story-only summaries as the project-wide result index. It does NOT supersede the underlying numeric authority files.
## 18. Recovered pre-SLM computational results that must not disappear

These results came from the hypothesis-centered / 20-model computational lineage and remain useful because they establish the structure of the behavior before the newer SLM adjudication.

### 18.1 Visible state, observation persistence, and food geometry
Status: HISTORICAL_RECOVERED; underlying held-animal dashboard result is well documented.
Animal-held-out learner full policy model:
- AUC .884.
- NLL .425.
- adding approximately 20-event observation history gives DeltaNLL +.0348 beyond visible state/context.
- food-geometry ablation loss is +.0422 NLL, the largest current-state feature-group loss in that analysis.
- day/session-time context contributes approximately zero after visible state + observation history.
Interpretation: current social-food geometry and recent observation history are the dominant behaviorally available coordinates; simple elapsed training/session time is not the explanation.

### 18.2 Immediate outcome-conditioned stop/re-entry rule
Status: HISTORICAL_RECOVERED.
Conditional transition result:
- when currently Observe, Active vs Unrewarded raises next-event transition to No-observe by about +10.0 percentage points.
- Passive vs Unrewarded raises stopping by about +12.9 points.
- when currently No-observe, Active and Passive reduce re-entry into Observe by about 9.0 and 8.3 points, respectively.
Interpretation: reward outcome immediately changes the next sampling decision.
Guardrail: call this a stop/re-entry rule, not "the animal has enough information and therefore stops."
### 18.3 Fast rule versus slow latent
Status: HISTORICAL_RECOVERED.
- the fast outcome-conditioned transition rule is already visible early in a session.
- Q/belief-like slow latent is reset near zero and accumulates across events.
- by event 51+, its absolute impact on choice probability reaches about 7-8 percentage points in the earlier analysis.
Interpretation: the behavior contains at least two separable timescales: immediate outcome-conditioned policy change and slower accumulated state/value.

### 18.4 Multi-event and cross-day memory
Status: HISTORICAL_RECOVERED.
- fold-selected action-memory gamma=.95-.97 corresponds to roughly 20-33 events, median real time about 4.5-7.5 min.
- this memory outperforms current run length / elapsed time.
- chronological day order ranked 1/501 among within-animal whole-day shuffles, empirical P=.001996.
- adding cross-day retained prior to the final within-day model improved 29/40 animals, paired P=.0125.
- the cross-day prior contributes mainly at the beginning of a new session and fades by around event 50.
Interpretation: behavior contains within-session multiscale memory plus a transient cross-day prior.

### 18.5 State representation ablation
Status: HISTORICAL_RECOVERED.
Under the earlier matched-state contract:
- Full state versus DemFeed + Facing improved 31/40 animals, supporting independent NearSpout / food-geometry information.
- Full state versus DemFeed + NearSpout: 21/40, P=.501; Facing is not required once food geometry is represented.
- current observation rate must never be used to predict simultaneous action_observe because that is circular; past observation tendency enters only through lag/history terms.
Interpretation: food geometry is a core state variable; facing/social orientation is biologically meaningful but not a necessary computational predictor once the relevant geometry is present.
### 18.6 Scalar outcome value, reliability, and information-gain constraint
Status: HISTORICAL_RECOVERED / GUARDRAIL.
Earlier held-animal dashboard:
- a strictly prior RW-like scalar outcome state predicts conversion context but contributes little to observation choice.
- learner best scalar-RW conversion gain DeltaNLL about +.00945 (alpha about .02, Passive weight about .5).
- non-learner gain about +.00604.
- reliability/uncertainty state is slightly stronger: with common coding, learner reliability +.01174 NLL versus RW +.00983.
- adding RW on top of reliability adds essentially nothing (+.00003).
- simple Beta-Bernoulli expected-information-gain proxy is negative for observation choice after state/history/reliability controls: learner DeltaNLL about -.00011; non-learner about -.00031.
Interpretation: a slow outcome/reliability state helps explain conversion, but current data do not support a simple "observe because expected information gain is high" rule.

### 18.7 Observation-delay eligibility kernel constraint
Status: GUARDRAIL.
Earlier explicit timing test:
- median last-observation delay about 1.0 s and observation duration about 1.3 s within the 3-s pre-event window.
- across tau=.1-4 s and future lags 1/2/3/5, best held-out NLL gains were about 1e-4 or smaller and inconsistent across groups.
Interpretation: current behavior does not support a simple single-exponential observation-to-outcome temporal-credit kernel.
