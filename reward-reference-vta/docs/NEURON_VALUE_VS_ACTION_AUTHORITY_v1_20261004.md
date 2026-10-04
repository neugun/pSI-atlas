# Reward-reference DA versus consummatory action — analysis authority v1
Date: 2026-10-04

## Biological question

Does the sustained VTA dopamine difference attributed to reward history/reference reflect relative reward value, or can it be explained by the animal simply licking more, licking faster, or remaining in the bout longer?

The current answer is **neither a pure value signal nor a pure lick counter**.

The data support a mixed signal:
1. an ongoing consumption/sampling/action component;
2. a history/reference component that remains after current-action controls and becomes more apparent later in consumption.

The manuscript-safe statement is:

> Sustained VTA dopamine contains a reward-reference component that is not reducible to current lick amount, alongside a substantial consummatory/sampling component.

Do **not** write:
- “dopamine is independent of licking”;
- “dopamine purely encodes abstract value”;
- “licking is only a nuisance confound”;
- “all action variance is downstream of dopamine”.

## Why the confound is real

In the strict 192-bout / 11-animal matched-current cohort:
- whole-bout lick count correlates with RWstate: r = 0.611;
- whole-bout duration correlates with RWstate: r = 0.599;
- whole-bout lick count correlates with sustained DA: r = 0.392;
- duration correlates with sustained DA: r = 0.375.

Therefore whole-bout behavior and reward history are strongly coupled.

However, early action is much less coupled to the reference state:
- RWstate vs 0–2 s licks: r = 0.041;
- sustained DA vs 0–2 s licks: r = 0.129.

This makes early-action control more causally interpretable than conditioning only on final bout duration or total lick count.

## Outcome definition matters

The primary neural endpoint is mean DA change in a **fixed 2–5 s window**.
It is not a whole-bout AUC and does not automatically grow when the bout lasts longer.

Whole-bout AUC analyses are useful elsewhere, but the main value-vs-action adjudication uses the fixed-duration sustained signal.

## Causal-order principle

Current reward can affect both dopamine and licking. Dopamine can also affect feeding persistence, and ongoing licking can provide sensory/motor feedback to dopamine.

Therefore:
- 0–2 s licking is the preferred current-action nuisance control for 2–5 s DA;
- 2–5 s concurrent licking is a stricter sensitivity control;
- total bout lick count/rate/duration are deliberately treated as **over-control sensitivity analyses**, because they include behavior occurring after the neural window begins and can sit downstream of value/DA.

## 1. Conditional regression and permutation

Reference-state unique variance in sustained DA:

| Action control | RW unique ΔR² | conditional permutation P |
|---|---:|---:|
| 0–2 s action, flexible polynomial | 0.0543 | 0.0464 |
| 0–2 + 2–5 s action | 0.04895 | 0.0449 |
| whole-bout lick count/rate/duration over-control | 0.03299 | 0.0357 |

Cluster-robust coefficient tests point in the same direction:
- early + concurrent flexible control: RW β = 2.054, cluster P = 0.00253;
- whole-bout over-control: RW β = 1.794, cluster P = 0.00495.

Saturated discrete-action nuisance models are more parameter hungry and land near the threshold:
- early saturated: P_perm = 0.060;
- early + concurrent saturated: P_perm = 0.051.

Interpretation: effect size remains, while exact saturation costs power in a 192-bout dataset.

## 2. Joint model: action and reference both contribute

In one cluster-robust model containing RWstate, 0–2 s licks and 2–5 s licks:

- RWstate: β = 2.283, P = 0.00171;
- early licks: β = 0.376, P = 0.0165;
- concurrent licks: β = 0.554, P = 0.000457.

Thus the correct conclusion is not “action does not matter”.
Both components contribute independently.

## 3. Descriptive partial-variance partition

Using flexible early + concurrent action terms with animal/session covariates:

- base R² = 0.302;
- base + reference R² = 0.353;
- base + action R² = 0.412;
- base + reference + action R² = 0.461.

Incremental decomposition:
- reference increment over base = 0.0511;
- action increment over base = 0.1101;
- joint increment = 0.1590;
- reference unique after action = 0.04895;
- action unique after reference = 0.10791;
- overlap/shared component ≈ 0.00214.

This is an in-sample partial-variance decomposition, not a held-animal prediction claim.

Biological interpretation: the action/sampling component is substantial, but almost all of the reference increment remains unique rather than being shared with the action block.

## 4. Exact action matching

Within animal and current reward:
- exact matching on 0–2 s lick count gives 55 high-R/low-R pairs across 11 animals;
- 9/11 animals retain higher sustained DA in the high-reference condition;
- median animal ΔDA = 0.792;
- one-sided exact Wilcoxon P = 0.0415.

If 0–2 s and 2–5 s lick counts are both required to match exactly:
- only 31 pairs remain;
- 7/11 animals are positive;
- median animal ΔDA remains positive (0.205);
- P = 0.183.

This second test is low-power and should be described as sensitivity, not as a failed primary test.

## 5. Nonlinear cross-fit nuisance control

To avoid relying on a chosen polynomial action model, nuisance functions were learned on other animals using three nonlinear learners.
The models predict the action-explainable part of RWstate well; DA nuisance prediction is weak across animals, so this is a **functional-form sensitivity test**, not a prediction benchmark.

Residual DA versus residual reference:

| learner | residual slope | cluster P | conditional permutation P | positive animal slopes |
|---|---:|---:|---:|---:|
| Random Forest | 1.890 | 0.00054 | 0.0100 | 8/11 |
| ExtraTrees | 1.895 | 0.00135 | 0.0172 | 9/11 |
| HistGradientBoosting | 1.603 | 0.00080 | 0.00170 | 7/11 |

The reference effect therefore does not depend on a particular linear nuisance specification.

## 6. Time-resolved decomposition

Post-onset DA was analyzed in 0.5-s bins with:
- reference state;
- lick count in the current 0.5-s bin;
- cumulative within-bout licks **before** that bin;
- animal, current reward, session position, Clock and OneShot covariates.

The temporal sequence is:

### 0–1 s
Reference contribution is absent.
Action/sampling terms are still weak.

### ~1–3 s
Prior within-bout sampling becomes the dominant significant term.
Its FDR-corrected q values are <0.05 from 1–1.5 s onward.

### ~3–4.5 s
Reference coefficient becomes positive and nominally significant:
- 3.0–3.5 s: standardized β = 0.921, P = 0.0229;
- 3.5–4.0 s: β = 1.014, P = 0.0145;
- 4.0–4.5 s: β = 0.975, P = 0.0225.

Across ten exploratory temporal bins, these late reference bins reach BH q ≈ 0.076, so the time-resolved result should be called **suggestive timing evidence**, not an independent corrected discovery.

The pre-specified 2–5 s sustained-window action-control tests remain the main inference.

## 7. Current reward U and learned reference R

Without action control:
- current reward U: +1.247, P = 3.26e-6;
- learned reference R: −2.029, P = 0.00995.

With action main effects controlled:
- early action: U = +1.127, P = 1.2e-5; R = −2.172, P = 0.00314;
- early + concurrent action: U = +0.815, P = 8.6e-5; R = −2.211, P = 0.00153.

Corresponding contrast-like U−R term:
- no action: β = 1.638, P = 0.000693;
- early action: β = 1.649, P = 0.000343;
- early + concurrent: β = 1.513, P = 5.9e-5.

If reward-dependent action interactions are made extremely flexible, the U coefficient becomes unstable because current reward and current action are strongly coupled. Importantly, R remains negative and significant even in that conservative specification:
- early + concurrent interacted action: R = −2.054, P = 0.00253;
- whole-bout interacted over-control: R = −1.794, P = 0.00495.

This is the most diagnostic part for the current question: the learned reference is determined before the current bout and cannot be rewritten as “the animal happened to lick more in this bout.”

## 8. Held-animal prediction boundary

On this strict 192-bout subset, the simple leave-one-animal-out prediction comparison is weak:
- base OOF R² ≈ 0.047;
- base + RW ≈ 0.053;
- base + action ≈ 0.020;
- joint ≈ 0.026.

Animal-level MSE improvements are not stable.

Therefore do not use this restricted subset to claim strong held-animal prediction.
Its role is mechanistic within-animal confound adjudication.

## Integrated biological interpretation

The emerging model is sequential rather than binary:

1. Past sampled rewards establish a reference R before the current bout.
2. Current reward initiates consumption.
3. Ongoing within-bout sampling/action contributes strongly to DA during the first seconds.
4. Over continued consumption, DA increasingly expresses a history-relative component involving current reward and the learned reference.
5. DA can in turn influence persistence, making late whole-bout action partly an outcome rather than a clean confound.

Thus action and value are intertwined biologically, but the learned-reference contribution is not reducible to lick number.

## Manuscript-safe claim

> Consumption-period VTA dopamine multiplexes ongoing reward sampling with a history-dependent reference signal. Current licking explains substantial neural variance, but conditioning on early and concurrent action does not absorb the reference effect; the learned reference remains independently associated with sustained dopamine, and a history-relative component emerges later during consumption.

## Key source files

- data/current/NEURON_value_vs_action_bouts_v1.csv
- data/current/NEURON_value_action_conditional_perm_v1.csv
- data/current/NEURON_value_vs_action_joint_coefficients_v1.csv
- data/current/NEURON_value_action_variance_partition_v1.csv
- data/current/NEURON_value_vs_action_exact_match_summary_v1.csv
- data/current/NEURON_value_action_DML_summary_v1.csv
- data/current/NEURON_value_action_timecourse_v2.csv
- data/current/NEURON_value_action_UR_control_v1.csv
- data/current/NEURON_value_action_UR_control_v2.csv
