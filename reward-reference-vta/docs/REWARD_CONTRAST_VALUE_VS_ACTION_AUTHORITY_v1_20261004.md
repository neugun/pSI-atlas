# Reward Contrast — Value vs Action Authority v1 — 2026-10-04

## Biological question

The central confound is real:

> If sustained dopamine is larger in bouts with larger reward-history/reference values, is dopamine representing relative reward value, or merely reporting that the animal licks more / consumes longer?

The current answer is **neither pure-value nor pure-action**.

The sustained 2–5 s dopamine signal contains:
1. a reward-reference / relative-value component that survives current-action controls; and
2. an independent consummatory-action component associated with ongoing licking.

The two components are biologically coupled but not interchangeable.

---

## 1. Why the confound is serious

Across the strict 192 post-switch bouts from 11 animals:

- whole-bout lick count vs RWstate: r = 0.611;
- whole-bout duration vs RWstate: r = 0.599;
- whole-bout lick count vs sustained DA: r = 0.392;
- whole-bout duration vs sustained DA: r = 0.375.

Thus later/high-reference bouts often contain more consummatory output.

It would be incorrect to claim that dopamine is unrelated to licking.

---

## 2. Causal ordering changes the interpretation

The relevant dopamine endpoint is sustained DA from 2–5 s after bout onset.

Action measured before that window is much less coupled to reference:

- 0–2 s lick count vs RWstate: r = 0.041;
- 0–2 s lick count vs sustained DA: r = 0.129.

Concurrent action during the DA window is somewhat more coupled:

- 2–5 s lick count vs RWstate: r = 0.236;
- 2–5 s lick count vs sustained DA: r = 0.207.

Whole-bout measures become much more strongly coupled to both reference and DA.

This temporal gradient matters because whole-bout lick count and duration are partly downstream behavioral outputs. If:

reference/value → dopamine → persistence/licking

or

reference/value → persistence/licking

then regressing the final whole-bout action out of dopamine is an **over-control** and can remove genuine value-related signal or induce collider bias.

Therefore the preferred causal control is early action (0–2 s), with concurrent and whole-bout controls treated as progressively more conservative sensitivity analyses.

---

## 3. Reference survives early-action control

Using the same nuisance family as the main Natural analysis and conditional residual permutation:

### Flexible 0–2 s action control

Reference-state unique ΔR² = 0.05431  
conditional permutation P = 0.04640

Clustered coefficient:
beta = 2.131  
P = 0.00316

### Saturated early-action count control

Reference-state unique ΔR² = 0.06540  
conditional permutation P = 0.06039

The saturated model has many discrete-action nuisance degrees of freedom and sits at the significance boundary, but the effect size does not collapse.

Interpretation:

> early licking alone does not explain the sustained reward-history dopamine signal.

---

## 4. Reference survives concurrent-action control

When 0–2 s and 2–5 s licking are modeled together with flexible nonlinear terms:

Reference-state unique ΔR² = 0.04895  
conditional permutation P = 0.04490

Clustered coefficient:
beta = 2.054  
P = 0.00253

A saturated exact-action-count nuisance model gives:

Reference-state unique ΔR² = 0.05371  
conditional permutation P = 0.05119

Again, increased nuisance dimensionality reduces permutation power, but the reference effect size remains.

Interpretation:

> even contemporaneous licking during the sustained-DA window does not absorb the reward-reference signal.

---

## 5. Whole-bout action over-control still leaves reference information

Controlling whole-bout:
- lick count,
- lick rate,
- duration,

with flexible nonlinear and reward-interaction terms gives:

Reference-state unique ΔR² = 0.03299  
conditional permutation P = 0.03570

Clustered coefficient:
beta = 1.794  
P = 0.00495

This is a conservative sensitivity analysis because the nuisance variables include behavioral consequences occurring after the beginning of the neural response.

Preferred wording:

> the history effect survives even a conservative full-bout consumption over-control, but early-action controls are more causally interpretable.

---

## 6. Action itself also contributes independently to dopamine

A joint model containing reference state, 0–2 s licks and 2–5 s licks shows:

Reference state:
beta = 2.283  
clustered P = 0.00171

Early 0–2 s licks:
beta = 0.376  
clustered P = 0.0165

Concurrent 2–5 s licks:
beta = 0.554  
clustered P = 0.000457

Therefore the correct interpretation is not:

“dopamine is pure value and licking does not matter.”

It is:

> sustained dopamine carries a reference-dependent value component together with an independent ongoing consummatory-action component.

---

## 7. Exact action matching

To avoid depending entirely on regression adjustment, high-reference and low-reference bouts were matched within animal and current reward.

### Exact 0–2 s lick-count match

55 matched pairs across 11 animals.

9/11 animals show higher sustained DA in the high-reference member.

Median animal ΔDA (high-R − low-R) = 0.792.

One-sided exact Wilcoxon P = 0.0415.

This is the cleanest action-matched support because matching is based on action before the sustained 2–5 s DA endpoint.

### Exact 0–2 s + 2–5 s lick-count match

31 matched pairs across 11 animals.

7/11 animals positive.

Median pair ΔDA remains positive (~1.07), but median animal ΔDA is smaller (~0.205).

One-sided Wilcoxon P = 0.183.

Interpretation:

> the concurrent exact-match analysis is directionally consistent but low power because exact matching discards most bouts. It should be presented as sensitivity evidence, not as the primary causal test.

A still stricter 0–1 / 1–2 / 2–5 s exact count match leaves only 23 pairs from 8 animals and is correspondingly underpowered.

---

## 8. Variance partition

With a common base nuisance model:

Base R² = 0.3022

Base + reference:
R² = 0.3533  
increment = 0.05109

Base + flexible action block:
R² = 0.4123  
increment = 0.11005

Base + reference + action:
R² = 0.4612  
joint increment = 0.15900

Unique reference after action:
ΔR² = 0.04895

Unique action after reference:
ΔR² = 0.10791

Shared/suppressor component:
~0.00214

The raw action block explains more in-sample variance, but it also contains many more parameters and includes contemporaneous measurements.

Therefore raw ΔR² magnitude should not be interpreted as biological priority.

---

## 9. Complexity penalty changes the model ranking

Model sizes and information criteria:

Base:
18 parameters  
AIC = 818.58  
BIC = 877.22  
adjusted R² = 0.234

Base + one-dimensional reference:
19 parameters  
AIC = 805.98  
BIC = 867.87  
adjusted R² = 0.286

Base + flexible action block:
30 parameters  
AIC = 809.63  
BIC = 907.35  
adjusted R² = 0.307

Base + reference + action:
31 parameters  
AIC = 794.93  
BIC = 895.91  
adjusted R² = 0.361

Thus:
- AIC / adjusted R² favor the richer joint model;
- BIC strongly favors the parsimonious one-dimensional reference model over the action-only and joint high-dimensional models.

Biological interpretation:

> action explains substantial local neural variance, but the compact reference state provides unusually efficient explanatory structure.

---

## 10. Held-animal prediction is a boundary, not a positive result

On the strict 192-bout subset:

Base OOF R² = 0.0472  
Base + reference = 0.0533  
Base + action = 0.0201  
Base + both = 0.0261

Animal-level MSE improvements are not significant.

Therefore this subset should not be used to claim that either current action or reference provides strong new cross-animal prediction.

The value of these analyses is mechanistic within-animal adjudication.

Cross-task transfer of the frozen reference state to QE and VTA-stimulation history provides the stronger generalization evidence for the reference computation.

---

## 11. Current biological model

The most defensible architecture is:

reward history → reference R

current reward + internal state → utility U

U relative to R → reference-dependent dopamine component

ongoing consummatory action → additional dopamine component

R / U / dopamine / other comparison circuits → feeding persistence and action

This architecture permits:
- dopamine to carry value/reference information;
- dopamine to covary with and respond to ongoing consummatory action;
- action to be partly downstream of value;
- dopamine to contribute causally to persistence without being the sole mediator of all behavior.

---

## 12. Claims supported now

Supported:

1. Whole-bout licking is strongly correlated with reward-history state and sustained DA; the action confound is real.
2. Early action is only weakly correlated with reference state.
3. Reference information survives early-action, concurrent-action, and conservative full-bout action controls.
4. Reference and licking both contribute independently to sustained DA.
5. Exact early-action matching retains a positive reference effect.
6. A compact one-dimensional reference is more parsimonious than a high-dimensional action-only model under BIC.
7. Sustained DA is best described as a **mixed reference/value + consummatory-action readout**, not a pure motor signal or a pure abstract value signal.

Not supported:

1. Do not say dopamine is independent of licking.
2. Do not say action is merely a nuisance with no neural contribution.
3. Do not interpret whole-bout action regression as the uniquely correct causal adjustment.
4. Do not claim the strict 192-bout action analysis provides strong held-animal prediction.
5. Do not claim observational regression proves dopamine mediates all reference effects on behavior.

---

## 13. Authority files

Primary analysis:
- data/current/NEURON_value_vs_action_bouts_v1.csv
- data/current/NEURON_value_vs_action_regression_v1.csv
- data/current/NEURON_value_action_conditional_perm_v1.csv
- data/current/NEURON_value_vs_action_joint_coefficients_v1.csv
- data/current/NEURON_value_vs_action_exact_match_summary_v1.csv
- data/current/NEURON_value_vs_action_exact_pairs_v1.csv
- data/current/NEURON_value_action_variance_partition_v1.csv
- data/current/NEURON_value_action_information_criteria_v1.csv
- data/current/NEURON_value_action_LOAO_summary_v1.csv
- data/current/NEURON_value_action_LOAO_comparisons_v1.csv

Figure:
- figures/extended_data_current/NEURON_ED_value_vs_action_adjudication_v1.png/pdf/svg

Related earlier controls:
- data/current/NEURON_early_licking_linear_control_stats_v2.csv
- data/current/NEURON_current_licking_confound_stats_v1.csv
