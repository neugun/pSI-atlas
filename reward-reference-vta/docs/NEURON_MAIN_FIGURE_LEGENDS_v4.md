# Neuron main-figure legends v4

## Figure 1. Identical current rewards acquire different value after different histories

(A) Matched-current design. The same current reward is compared after different recent reward histories: S-H for current 100E and L-N for current 20E. The aligned reference effect is defined as one-half of the sum of the two matched-current contrasts.

(B) Feeding persistence. The aligned history contrast is positive in all 9 animals (rank-biserial r=+1.0; two-sided exact Wilcoxon P=0.003906).

(C) Sustained VTA dopamine during 2-5 s of feeding. The aligned history contrast is positive in all 9 animals (rank-biserial r=+1.0; exact Wilcoxon P=0.003906).

(D) Time-resolved aligned dopamine reference effect around feeding onset. The effect is weak or absent around bout onset and increases during ongoing consumption; the shaded 2-5 s interval denotes the sustained summary window used in the matched-current analyses.

(E) Window-sensitivity analysis using the same duration-qualified bouts across windows. The aligned effect is 9/9 positive for 2-4, 2-5, 2.5-5 and 3-5 s (exact Wilcoxon P=0.003906 for each), showing that the result is not specific to one hand-selected late window.

Together, the figure establishes the model-free phenomenon: identical current rewards occupy different behavioral and sustained-dopamine value states after different recent histories.

## Figure 2. Sampled consumption, not passive waiting, updates the reference

(A) Candidate update sources after a programmed reward-state change. The first sampled bout tests whether passive elapsed time advances the reference before new reward experience; later sampled bouts test whether experienced consumption carries graded update information.

(B) First-sample passive-time test. Across candidate time constants from 5 to 640 s, passive-time states add essentially no sustained-dopamine information before the first sample of the new reward state; the maximum added R2 is approximately 0.004.

(C) Experienced-consumption analysis. After nuisance structure is removed, residual sustained dopamine changes monotonically across quartiles of consumed exposure within the block, showing graded information after sampling begins.

(D) Direct early/current licking control. Adding 0-2 s lick count leaves the history-state contribution intact (added R2=0.0613; 10,000-permutation P=0.0356; clustered coefficient P=0.00397). Adding both 0-2 s lick count and current lick rate gives a similar result (added R2=0.0602; permutation P=0.0305; clustered P=0.00266). Black ticks denote the 95% permutation null for added R2.

The figure separates elapsed time from experienced sampling and shows that early licking does not account for the sustained history-dependent dopamine signal.

## Figure 3. A continuous history state generalizes across animals and retains deeper reward path

(A) Continuous reference-state construction. Recent sampled rewards update a recency-weighted reference R, and the history-relative coordinate is current reward minus that reference.

(B) Held-out-animal prediction. Sustained-dopamine LOAO R2 is 0.038 for current reward alone, 0.123 with categorical context, 0.175 with the continuous history state, and 0.178 with context plus state.

(C) Within fixed context, residual sustained dopamine increases monotonically across quartiles of residual history state after animal identity, current reward and categorical context are removed.

(D) Animal-level within-context slopes relative to each animal's permutation-null interval. The observed relation is shared across animals rather than driven by a single subject.

(E) Deeper-history test. After current reward, bout stage, within-block time, session progression, previous-block history and current-block consumption are controlled, cumulative history still explains residual sustained dopamine (added R2=0.02686; conditional-permutation P=0.00670).

(F) Recency profile. Added dopamine R2 varies smoothly across update rates, with a broad optimum around alpha=0.15-0.16; selection-aware inference rejects the corresponding null. The profile is interpreted as a graded recency scale rather than as an exact biological learning rate.

These analyses show that the reference is broader than nominal context and retains dopamine-relevant information beyond recent local history.

## Figure 4. Model comparison identifies information unique to cumulative history

(A) Representative competing latent-state accounts tested against the cumulative-history coordinate: cumulative history, belief/HMM, average reward rate, Pearce-Hall/uncertainty, adaptive gain and Value-RNN. Full model definitions, hyperparameters and recurrent capacity/seed controls are provided in Extended Data and Methods.

(B) Representative simulated latent-state trajectories around the same reward-state change. The same observed switch produces different adaptation dynamics under cumulative-history, belief/HMM, reward-rate and adaptive-gain accounts.

(C) Held-out prediction improvement, expressed as one minus relative MAE versus the observable task-and-behavior baseline. Continuous-time HMM, reward rate and belief-state models capture part of the signal; other alternatives provide weaker or inconsistent standalone gains.

(D) Bidirectional unique-information tests. After each strong competitor is included, the cumulative-history state retains approximately 0.025-0.027 unique sustained-dopamine R2: belief, 0.0254 (permutation P=0.0124); continuous HMM, 0.0266 (P=0.0090); reward rate, 0.0256 (P=0.0122); Value-RNN, 0.0269 (P=0.0128); and Value-RNN plus elapsed time, 0.0269 (P=0.00780). Reverse competitor-specific increments are small and not detected.

These model comparisons identify cumulative path information that is not eliminated by stronger belief, reward-rate or learned recurrent alternatives, without claiming one uniquely correct microscopic neural algorithm.

## Figure 5. Current reward becomes relative to stored history over seconds

(A) Time-resolved regression around bout onset in the same 192 post-switch bouts from 11 animals that lasted at least 5 s. The current-reward-minus-reference coefficient (U-R) is negative before feeding, remains weak early after onset, and becomes progressively positive during consumption; the orthogonal sum-like component (U+R) remains comparatively stable.

(B) Matched pre, early and sustained windows. U-R changes from beta=-0.485 before feeding to +0.294 during 0-2 s and +1.752 during 2-5 s. The sustained-minus-early increase is +1.458 (P=9.02e-08), and the sustained slope exceeds the early slope in all 11 animals (rank-biserial r=+1.0; exact paired Wilcoxon P=0.000977).

(C) Decomposition of the sustained comparison. During 2-5 s, current reward enters positively (U beta=+0.721, P=0.00216) and learned reference enters negatively (R beta=-0.691, P=0.0282).

Thus, stored history is recruited over the first seconds of consumption to place current reward in a relative-value coordinate.

## Figure 6. The history computation generalizes across value contexts

(A) Independent reward-quality transfer. The natural-task history rule is frozen at alpha=0.20 and tested only on pure-100E bouts after different reward-quality histories. Across 66 bouts from seven animals, the frozen state predicts dopamine AUC (added R2=0.02540; clustered P=0.00141; within-animal circular-shift P=0.00205).

(B) Recency profile in the independent reward-quality task. Transfer is broad across update rates around alpha approximately 0.15-0.40, with the frozen alpha=0.20 lying inside the high-performing range.

(C) Alignment of orthogonal value manipulations with a frozen natural 100E-versus-20E value direction. Under the primary standard-deviation scaling, cosine alignment is positive in 7/7 quinine animals, 7/7 hunger animals, 7/7 LiCl animals, 12/13 animals in the larger dopamine-stimulation cohort and 5/5 in the smaller stimulation cohort.

(D) Animal-level projections of each manipulation onto the frozen natural value axis. Most animal-level projections are positive across sensory-quality, motivational, devaluation and causal-dopamine manipulations.

The figure shows that recent consumption history is one transferable coordinate inside a broader ongoing-value space rather than a task-specific label.

## Figure 7. Consumption-period dopamine contributes to feeding persistence

(A) Natural-state continuation curves. Higher dopamine-selected history state predicts greater feeding persistence and lower bout-termination probability (termination OR=0.459, P=0.000180).

(B) Dopamine activation during consumption increases persistence and reduces termination hazard (OR=0.690, 95% CI 0.615-0.775, P=3.29e-10).

(C) Contingent JAWS inhibition during consumption reduces persistence and increases termination hazard (OR=1.341, 95% CI 1.031-1.746, P=0.0289).

(D) Unified termination-hazard summary. The natural high state and dopamine activation shift termination below OR=1, whereas contingent JAWS shifts termination above 1. The noncontingent JAWS effect is weaker and is not detected (OR=1.116, 95% CI 0.980-1.271, P=0.0976). The direct contingent-versus-noncontingent interaction is borderline (OR=1.233, P=0.0515), so the data are not interpreted as definitive evidence for timing specificity.

The natural and perturbational results converge on a functional role for consumption-period dopamine in sustaining feeding, while stopping short of a complete mediation claim from history reference to dopamine to behavior.
