# NEURON model-evidence authority v10 — 2026-09-28

Current manuscript authority: docs/MANUSCRIPT_NEURON_WORKING_v26.md

Central claim:
Recent reward consumption constructs a continuous recency-weighted reference frame. That reference contains cumulative history beyond local switch/context summaries and is combined with current reward over the first seconds of consumption to generate a sustained comparison-dominated VTA dopamine value code.

Primary positive evidence:
- matched-current behavior and sustained dopamine: 9/9 animals aligned, exact P=0.00390625;
- strict pre-sampling passive clock: max sustained-DA added R2=0.00385, all clustered P>0.55;
- consumption dose beyond bout stage: lick delta R2=0.03208, P=0.00180; feeding-time delta R2=0.04512, P=0.000400;
- state within animal x current reward x categorical context: added sustained-DA R2=0.06454, P=9.999e-05;
- exact local-history residual: cumulative state delta R2=0.02686, conditional P=0.00670;
- strict bidirectional horse race with raw-history controls: FullHistory unique R2 approximately 0.0253-0.0257, P approximately 0.010-0.012; reverse competitor P approximately 0.80-0.97;
- stable recency family: profile alpha approximately 0.16, nested modal alpha=0.15;
- matched temporal analysis: same 192 >=5 s bouts / 11 animals across pre, 0-2 s, 2-5 s;
- U-R contrast: pre -0.485 (P=2.35e-04), early +0.294 (P=0.603), sustained +1.752 (P=0.00893);
- sustained-minus-early interaction beta=+1.458, P=9.02e-08; sustained-minus-pre P=0.00259;
- 11/11 animals have stronger sustained than early U-R slope, exact paired P=0.000977;
- matched U+R does not show the same late strengthening: sustained-minus-early P=0.511;
- 0.5-s raw-trace regression reconstructs the strict pre/0-2/2-5 s authority windows to machine precision and shows U-R changing from negative before the bout to positive late in consumption; pointwise 95% confidence intervals remain above zero from approximately 3 s through 5 s (descriptive timing, not an exact onset estimate);
- raw z-signal without pre-bout subtraction shows no 0-2 s U-R effect (beta=-0.191, P=0.718) but a positive 2-5 s effect (beta=+1.267, P=0.0399);
- matched sustained U beta=+0.721, P=0.00216; R beta=-0.691, P=0.0282;
- DA-selected frozen state transfers to behavior: duration beta=0.476, P=0.00566; termination OR=0.459, P=0.000180.

Implementation boundaries:
- discrete prev1-prev4 block summaries do not isolate a memory cutoff; all conditional lag P>=0.16, while continuous multiblock state remains significant (P=0.00620);
- no exact adaptive model is a stable universal held-out-animal winner;
- adding FullHistory to neighboring models does not significantly improve held-out-mouse prediction;
- alpha is a recency descriptor, not a biological learning-rate constant;
- asymmetric high-to-low versus low-to-high alpha does not improve held-out prediction;
- nested divisive normalization does not improve over U-R (3/11 animals better, P=0.123), and all folds select the weak-normalization boundary;
- additional reference-dependent nonlinear gain terms are not significant (joint P=0.122);
- therefore the data support a reference-dependent comparison but do not prove literal subtraction;
- first-sample cross-block state does not establish a continuously visible dopamine reference before new sampling (P=0.734);
- natural data do not establish state-to-dopamine-to-behavior mediation;
- microscopic update-unit identifiability was directly tested: lick-based and duration-based history states are both significant alone (ΔR²≈0.0520, P≈0.0020; ΔR²≈0.0413, P≈0.0062) and are highly collinear (r≈0.968); neither is uniquely supported beyond the other (duration|lick P≈0.484; lick|duration P≈0.278), and nested LOAO does not distinguish them (P≈0.638). Thus consumption exposure/sampling is identified, but lick count versus feeding time is not separable;
- leave-one-cohort-out effect sizes remain positive, but cohort magnitude heterogeneity is unresolved at the animal level (exact cohort-label P=0.474);
- previous dopamine activation/JAWS results remain downstream functional context, not the new mechanistic endpoint.

Current main figures:
Fig1 submission_ready_v3/figures/main/CNS_FIG1_same_reward_reference_v3.pdf
Fig2 submission_ready_v3/figures/main/CNS_FIG2_sampling_gated_update_v3.pdf
Fig3 figures/neuron_working/NEURON_FIG3_history_beyond_labels_v1.pdf
Fig4 figures/neuron_working/NEURON_FIG4_cumulative_history_v2.pdf
Fig5 figures/neuron_working/NEURON_FIG5_temporal_comparison_v3.pdf
Fig6 figures/neuron_working/NEURON_FIG6_behavior_transfer_v1.pdf


## Additive cross-context authority — 2026-09-27

The core model evidence above remains unchanged. The following data are independent generalization/perturbation evidence and must not be used to replace the FullHistory/reference analyses.

- Quinine at fixed 100E: 7 animals / 172 bouts. Duration 41.0 -> 5.08 s, AUC 79.0 -> 3.06, sustained AUC 1.68 -> 0.878; all three readouts 7/7 animals in the value-down direction, exact paired P=0.015625.
- Quinine temporal traces were re-audited using each MAT file's basal_time, odor_time, and FP sampling interval. Corrected result: pre-bout separation is not significant (P=0.219); 0-2 s is positive in 7/7 animals (P=0.015625); 2-5 s is positive in 7/7 (P=0.015625). The earlier v1 timebase analysis is superseded.
- 20E stimulation replication A: 13 animals / 1,833 bouts, 1 mW / 25 ms Chrimson. Duration 6.61 -> 9.36 s (12/13, P=0.00806); AUC -1.51 -> 19.40 and sustained AUC -0.361 -> 1.926 (13/13, P=0.000244).
- 20E stimulation replication B: 5 animals / 774 bouts, 10 mW GRAB cohort. Duration, AUC, sustained AUC and peak DA all increase in 5/5 animals; clustered bout-level P values are 5.30e-12, 1.36e-9, 3.83e-9 and 5.91e-9.
- Hunger at fixed 20E: 7 animals / 851 bouts. Duration 7.22 -> 17.84 s (6/7, P=0.03125); total AUC higher in 6/7 (P=0.046875).
- LiCl at fixed 100E: 7 animals. Pre-LiCl higher-value state has longer duration in 7/7 (paired delta +7.68 s, P=0.015625) and higher AUC in 6/7 (delta +12.54, P=0.03125).

Interpretive rule: these contexts establish a broader ongoing-value space. They do not select the history algorithm. FullHistory/ReferenceRW/BeliefState/BlockSampling/TwoStage comparisons, alpha/memory-depth analyses, temporal U-R construction and frozen-state behavioral transfer remain the computational core.


### Frozen natural-reward neural axis
- Axis defined only from natural 100E-versus-20E differences using total AUC and AUC/s; normalized weights approximately 0.710 and 0.704.
- Quinine zero-shot / LOAO projection: 7/7 animals move in the expected higher-value direction for pure 100E versus 100E+quinine; exact paired P=0.015625; mean cosine similarity approximately 0.894.
- Independent 13-animal stimulation cohort: 13/13 animals move positively along the frozen natural-reward axis; exact P=0.000244; mean cosine approximately 0.881.
- Independent 5-animal 10-mW stimulation cohort: 5/5 animals move positively; mean cosine approximately 0.928.
- Interpretation: a neural direction defined by natural reward magnitude generalizes to sensory devaluation and causal stimulation without refitting. This is additive generalization evidence; it does not replace the FullHistory/reference model comparison.


### Equivalent FullHistory-state calibration of external manipulations
- Natural FullHistory behavioral coefficients: log-duration beta=+0.5015; termination-hazard beta=-0.8304.
- Quinine: approximately -3.14 equivalent state units by duration and -2.67 by hazard.
- 13-animal stimulation: approximately +0.49 by duration and +0.42 by hazard.
- 5-animal stimulation: approximately +0.81 by duration and +0.63 by hazard.
- Duration- and hazard-based calibrations agree in sign and similar magnitude for each manipulation.
- This is a descriptive common-scale mapping and must not be interpreted as proof that external manipulations alter the latent history state itself.


## Independent reward-quality task replication of the FullHistory computation
- Provenance: EE and QE lick streams have zero overlap and together exactly cover the global lick stream in all 7 animals; 172/172 selected bouts map uniquely and chronologically to original Feed_info bout starts.
- Frozen rule: alpha=0.20 is imported from the natural reward-contrast analysis and is not reselected in the QE task.
- Strict test subset: 66 pure-100E bouts / 7 animals; current reward is fixed while prior reward-quality history varies.
- Whole-bout DA AUC: FullHistory adds delta R2=0.0254048 after animal, flexible session-time and flexible bout-duration controls; beta=58.60; clustered P=0.00141098.
- Animal-level direction: 6/7 slopes positive; exact Wilcoxon P=0.03125.
- Serial null: within-animal circular-shift P=0.00205 in the strict AUC analysis.
- Past/future asymmetry: past-only P=0.00141; future-only P=0.356; in the joint model past P=0.000325 and future P=0.216.
- Local-history competition: FullHistory remains unique after last20 (P=0.0324), last40 (P=0.000173), last80 (P=0.000133), and cumulative-history controls (P=0.000393). last5/last10 are too highly correlated with FullHistory to discriminate strongly.
- Recency transfer: natural profile optimum is approximately 0.15-0.20; QE profile is broader with a maximum near 0.30, but frozen alpha=0.20 already gives delta R2=0.0254 and .15-.40 occupy the high-performance range. Do not claim identical learning-rate kernels.
- Fixed-window localization: the first 5 s are weak; among pure100 bouts surviving the full window, 10-15 s clustered P=0.0423 and 15-20 s has 7/7 positive animal slopes (P=0.015625). Formal late-versus-early interactions are unresolved, so use this only as temporal localization, not proof of monotonic growth.
- Interpretation: the FullHistory computation itself generalizes to an independent reward-quality task, while its dopamine expression can occur on a different timescale.


## Held-out cross-task recency validation — 2026-09-28
- QE leave-one-animal-out prediction: alpha=0.20 minimizes mean normalized MAE (0.545258); no tested alpha improves on it.
- QE nested LOAO: modal selected alpha=0.20; outer-fold selections are 0.08;0.2;0.3.
- Cross-task maximin: alpha=0.20 maximizes the minimum fraction of task-specific peak performance.
- At alpha=0.20, natural-task efficiency is 0.911 of its own maximum and QE efficiency is 0.979.
- The task-specific optima remain different (natural 0.15, QE 0.3); therefore claim a shared effective recency range, not an identical biological learning rate.
- Figure authority: figures/neuron_working/NEURON_QE_cross_task_recency_validation_v1.pdf.


## Cross-context joint value geometry robustness — 2026-09-28
- quinine: mean cosine remains positive across all 4 axis definitions; range 0.961-0.975; minimum positive-animal fraction 1.000.
- hunger: mean cosine remains positive across all 4 axis definitions; range 0.433-0.735; minimum positive-animal fraction 0.857.
- LiCl: mean cosine remains positive across all 4 axis definitions; range 0.723-0.819; minimum positive-animal fraction 0.857.
- stim13: mean cosine remains positive across all 4 axis definitions; range 0.833-0.882; minimum positive-animal fraction 0.923.
- stim5: mean cosine remains positive across all 4 axis definitions; range 0.952-0.988; minimum positive-animal fraction 1.000.
- Temporal geometry boundary, quinine: U-R > U+R (paired P=0.03125), but U-R is not better than linear ramp (P=0.57812) or onset step (P=0.9375).
- Temporal geometry boundary, stimulation: U-R > U+R (P=0.00024414), but generic monotonic trajectories align as well or better; U-R-minus-ramp and U-R-minus-step are negative.
- Interpretation boundary: use external contexts to support a common value direction/generalization. Do not use them to claim that the U-R temporal waveform itself is uniquely replicated outside the matched-history experiment.
- Figure authority: figures/neuron_working/NEURON_ED_value_geometry_robustness_v1.pdf.


## QE whole-bout AUC duration-interaction robustness — 2026-09-28
- Strict subset remains 66 pure-100E bouts / 7 animals.
- Base nuisance already includes animal, flexible session-time spline and flexible log-duration spline.
- Adding centered FullHistory x centered log-duration contributes delta R2=0.007895; clustered interaction P=0.382436.
- With the interaction present, the centered FullHistory main effect at mean log-duration is beta=65.912, clustered P=0.0113669.
- Interpretation: no evidence that the replicated AUC-history relationship requires a selectively stronger FullHistory effect in long bouts. This is a duration-confound control, not evidence that dopamine timing is duration-invariant.


## Dopamine-theory discrimination — science-first update

### Bayesian belief state
- Nested held-out model: mean relative MAE 0.971; 9/11 animals better than current-reward baseline; exact P=0.240.
- FullHistory beyond literature-derived belief: ΔR²=0.02541; permutation P=0.0124.
- Belief beyond FullHistory: ΔR²=0.000465; P=0.726.
- Interpretation: latent-state inference is plausible, but categorical/context belief does not recover the cumulative path information carried by FullHistory.

### Average reward rate
- Niv-style reward-rate state: mean held-out relative MAE=0.938; 9/11 better than baseline; exact P=0.240.
- FullHistory beyond reward rate: ΔR²=0.02565; P=0.0122.
- Reward rate beyond FullHistory: ΔR²=0.000432; P=0.722.

### Adaptive coding, uncertainty, and salience
- Tobler-style adaptive gain: TD/RW beyond gain ΔR²=0.01563, P=0.0494; gain beyond TD/RW ΔR²=0.000467, P=0.687.
- Belief entropy beyond FullHistory+belief: ΔR²=0.00192, P=0.476.
- Posterior variance beyond FullHistory+belief: ΔR²=0.00271, P=0.404.
- 0–2 s signed beyond unsigned: ΔR²=0.00477, P=0.231; unsigned beyond signed: ΔR²=0.00181, P=0.461.
- 2–5 s signed beyond unsigned: ΔR²=0.01867, P=0.0328; unsigned beyond signed: ΔR²=0.00320, P=0.375.
- Interpretation: sustained phase is more specifically signed history-relative value than generic salience.

### Distributional RL
- Distributional mean vs FullHistory: r=0.993.
- Distributional spread beyond FullHistory + distributional mean: ΔR²=0.000012, P=0.941.
- Boundary: bulk photometry does not require an added spread dimension; this does not test or reject single-neuron distributional coding.

### Value-RNN / learned-state result
- Full sensitivity completed on Titan: reward-only and reward+elapsed-time inputs; hidden sizes 2, 5, 10, 20, 50, 100; 3 seeds; 150 epochs.
- Hennig-aligned confirmatory completed: H=50, both input variants, 12 seeds.
- Reducer audit: the first RNN-only held-out summary incorrectly intersected with the FullHistory table before evaluation; corrected v5 summaries use the full RNN authority for held-out prediction and the 192-bout common subset only for FullHistory-versus-RNN horse races.
- Corrected H=50 held-out ensemble: reward-only mean relative MAE=1.011 (8/11 numerically better, exact P=0.465); reward+time=1.013 (8/11, P=0.413).
- FullHistory beyond H=50 RNN: ΔR²=0.02685, P=0.0128 (reward-only) and P=0.0078 (reward+time).
- H=50 RNN beyond FullHistory: ΔR²≈4–5×10^-5, P≈0.86 for both variants.
- Across H=5–100, FullHistory remains uniquely informative and RNN residuals are negligible.
- Reward-only H=2 was a nominal three-seed sensitivity exception (RNN unique ΔR²≈0.0153, nominal P≈0.0226), but a synchronized 10,000-permutation max-stat test across all 12 recurrent configurations gives family-wise P≈0.0646 (observed 0.01529 below the 95% max-null threshold≈0.01659). A dedicated H=2/12-seed confirmation then removed the residual: RNN beyond FullHistory was not detected for reward-only (ΔR²≈0.00443, P≈0.186) or reward+time (ΔR²≈0.00038, P≈0.686), whereas FullHistory remained unique beyond both RNN states (ΔR²≈0.03124, P≈0.0018; ΔR²≈0.02473, P≈0.0120). Its state is 97.5–98% predictable from existing task/history variables.
- Independent fresh-seed H=2 reward-only replication (seeds 100–111) converged on the same boundary: held-out mean relative MAE=0.969 (7/11 numerically better, exact P=0.240); FullHistory remained unique beyond the RNN (ΔR²=0.02668, P=0.0070), whereas RNN beyond FullHistory was negligible (ΔR²=0.00082, P=0.616).
- Implementation audit against the Hennig repository confirms matching GRU/value-head structure, TD target r_(t+1)+gamma*V_(t+1), gamma=0.93, Adam lr=0.003, 150-epoch paper fit setting, and default PyTorch initialization path.
- Interpretation: a recurrent learner can recover a history-related coordinate but does not reveal a stable additional population-level dimension that replaces cumulative FullHistory.

### Main-text rule
Use model competition only to answer biological questions. Do not present a leaderboard. Full parameter grids, recovery, seed robustness, and model-zoo tables remain Extended Data/Methods.

## Continuous QE temporal expression — v26 addition
- Same fixed 40 pure-100E bouts lasting >=20 s / 7 animals across all bins.
- Frozen FullHistory state is associated with pre-bout dopamine from -2.0 to -0.5 s (positive-cluster P=0.0089).
- No stable positive cluster during approximately 0–8 s after bout onset.
- Late positive clusters: 8–12 s, P=0.0020; 13–20 s, P=0.00020.
- Null preserves temporal covariance by circularly shifting the residualized frozen state within each animal.
- Interpretation: cross-task generalization is a shared history-reference computation, not a fixed latency or waveform.

## Behavioral/circuit convergence — v26 addition
- History contrast predicts bout duration beta=+0.698, P=3.89e-15, and termination hazard beta=-1.229, P=1.53e-14.
- DA-selected alpha=0.20 state predicts behavior without behavioral retuning: duration beta=+0.476, P=0.00566; termination beta=-0.780, OR=0.459, P=0.000180.
- Dopamine activation reduces termination hazard: OR=0.690, P=3.29e-10.
- Contingent Jaws inhibition increases termination hazard: OR=1.34, P=0.0289; noncontingent inhibition is weaker/not detected, P=0.098.
- Interpretation: evidence supports history -> reference -> sustained dopamine value -> persistence as a directional chain, but does not establish complete causal mediation of the reference itself.

