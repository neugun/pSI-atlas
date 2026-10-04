# Reward-reference: value/reference versus action authority v1 — 2026-10-04

## Question

The sustained VTA dopamine signal is measured while the animal is actively licking/consuming. Therefore a central alternative explanation is:

> the apparent reward-history / value signal is actually a consequence of different amounts or rates of licking, rather than a reference-dependent value computation.

This alternative is biologically plausible and must not be dismissed, because reward reference, feeding persistence and lick amount are naturally coupled.

## First observation: action and value are genuinely coupled

Across the 192 duration-qualified Natural bouts:

- correlation of RWstate with whole-bout lick count: r = 0.611;
- correlation of RWstate with bout duration: r = 0.599;
- correlation of whole-bout lick count with sustained DA: r = 0.392;
- correlation of bout duration with sustained DA: r = 0.375.

Thus whole-bout action amount is not an irrelevant nuisance. It covaries with both the latent reference state and dopamine.

By contrast, early action before the sustained DA window is only weakly related to the reference:

- 0–1 s lick count vs RWstate: r = 0.102;
- 0–2 s lick count vs RWstate: r = 0.041.

This distinction matters causally.

## Causal ordering and why whole-bout controls can over-control

The primary neural outcome is sustained DA from 2–5 s.

A whole-bout lick count or final bout duration contains behavior occurring after that neural window. If the biological pathway is partly:

reference/value → sustained DA → feeding persistence / additional licking,

then conditioning on final lick count or duration can remove legitimate downstream consequences of dopamine and may introduce over-control/collider bias.

Therefore the preferred action-confound test uses pre/same-onset behavior (0–1 or 0–2 s licking), while full-bout action controls are retained as conservative sensitivity analyses.

## Joint model: reference and action both contribute

A joint model containing the same task/animal/time nuisance set plus RWstate, standardized 0–2 s lick count and standardized 2–5 s lick count gives:

- RWstate: beta = 2.283, SE = 0.728, clustered P = 0.00172;
- 0–2 s licks: beta = 0.376, SE = 0.157, clustered P = 0.0165;
- 2–5 s licks: beta = 0.554, SE = 0.158, clustered P = 0.000457.

Therefore sustained dopamine is not well described as either a pure value signal or a pure motor/licking signal.

The current preferred interpretation is:

sustained VTA DA = reference-dependent value component + ongoing consumption/action component.

## Reference survives increasingly strong action controls

Incremental reference information remains after several action-control families:

- no current-action control: ΔR² = 0.0511, RW P = 0.00995;
- flexible 0–2 s action control: ΔR² = 0.0543, RW P = 0.00316;
- flexible 0–2 + 2–5 s action control: ΔR² = 0.0489, RW P = 0.00254;
- whole-bout lick count + lick rate + duration over-control: ΔR² = 0.0330, RW P = 0.00495.

The reference term therefore survives both temporally appropriate early-action controls and a deliberately conservative full-bout over-control.

## Exact discrete action matching

A stronger nonparametric sensitivity test fixes animal, current reward identity and discrete lick counts exactly, then asks whether continuous RWstate still predicts 2–5 s DA within those exact-action strata.

### Same 0–2 s lick count

- 166 bouts;
- 39 exact-action strata;
- 11 animals;
- RW beta = 2.216;
- clustered P = 0.00609.

This is strong evidence that different early action amounts do not explain the history-reference effect.

### Same 0–2 s and same 2–5 s lick counts

- 104 bouts;
- 40 exact-action strata;
- 11 animals;
- RW beta = 2.128;
- clustered P = 0.168.

The point estimate remains close to the unrestricted estimate, but exact matching removes almost half the dataset and the confidence interval broadens strongly. This analysis is directionally consistent but underpowered; it is not a significant independent confirmation.

### Same 0–1, 1–2 and 2–5 s lick counts

- 80 bouts;
- 33 strata;
- 11 animals;
- RW beta = 2.527;
- clustered P = 0.190.

Again the point estimate remains positive but uncertainty is large.

The correct reading is not “exact action matching proves independence from licking.” The correct reading is:

1. early-action exact matching preserves a significant reference effect;
2. regression controls through the 2–5 s window preserve a strong reference effect;
3. exact matching through the full neural window keeps a similar positive effect size but loses power;
4. action itself also contributes independently.

## Exact high-versus-low reference pairs

Within animal and current reward:

- same 0–2 s lick count: 55 pairs / 11 animals, 9/11 animals have positive DA difference, one-sided animal Wilcoxon P = 0.0415;
- same 0–2 and 2–5 s lick counts: 31 pairs / 11 animals, 7/11 positive, P = 0.183;
- same fine time-bin lick counts: 23 pairs / 8 animals, 5/8 positive, P = 0.230.

These pairwise results agree with the exact-stratum analysis: fixing early action retains the effect; increasingly exact matching of concurrent action reduces sample size and statistical power.

## Current biological conclusion

Do not describe the sustained photometry signal as “pure value.”

A more accurate model is:

- early/ongoing licking contributes to sustained dopamine;
- recent reward history contributes additional dopamine information that cannot be reduced to licking amount/rate;
- whole-bout licking and duration are partly consequences of value and dopamine, so they should not be treated only as upstream confounds;
- current data are consistent with multiplexed valuation + consummatory-action coding in the population signal.

This is also compatible with the temporal result: the reference-dependent component grows over 2–5 s while the animal is consuming, exactly when current sensory/reward input, ongoing action and stored reference can be combined.

## Files

- data/current/NEURON_value_vs_action_bouts_v1.csv
- data/current/NEURON_value_vs_action_regression_v1.csv
- data/current/NEURON_value_vs_action_joint_coefficients_v1.csv
- data/current/NEURON_value_vs_action_exact_pairs_v1.csv
- data/current/NEURON_value_vs_action_exact_match_summary_v1.csv
- data/current/NEURON_value_vs_action_exact_strata_v1.csv
- figures/neuron_working/NEURON_value_vs_action_adjudication_v1.png
- scripts/neuron_value_vs_action_adjudication_v1.py
