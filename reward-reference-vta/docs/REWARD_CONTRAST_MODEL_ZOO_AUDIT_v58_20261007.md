# Reward Contrast model-zoo audit v58

Date: 2026-10-07
Authority: NEURON_DOPAMINE_MODEL_ZOO_REGISTRY_v58_20261007.csv

## What changed

The previous 29-family registry was internally complete as a table, but it folded two models that already had independent numerical results into broader labels:

1. Continuous-time HMM — held-out mean relative MAE about 0.923. FullHistory still adds dR2 about 0.0266 beyond HMM (permutation P about 0.0090); the reverse HMM-specific increment is small/not detected.
2. Gershman/Kalman state filter — held-out mean relative MAE about 1.0003; it does not show stable held-out superiority over the scalar cumulative-history family.

They are now explicit rows, bringing the authoritative registry to 31 model families.

## Evidence layers remain separate

- Held-out prediction asks whether a model predicts an unseen animal better than the observable task/behavior baseline.
- Bidirectional unique-information tests ask whether FullHistory still contributes after a strong competitor, and vice versa.
- Simulation/model recovery asks whether historical candidate algorithms can be distinguished from one another under the task.

These layers must not be combined into one leaderboard.

## Current interpretation

The model room supports one strong information-level claim: recent sampled reward history contains information required to explain sustained VTA dopamine beyond current reward, simple context, belief/HMM, reward-rate and learned recurrent alternatives. The biological implementation can still be an explicit scalar reference, an augmented-state generalized RPE, or a distributed population state that contains equivalent information.

## Next decisive task

The highest-priority experiment is a fully crossed within-animal history x current-reward design, with identical expected probes and unexpected catch outcomes, analyzed separately at cue, first sample, 0-2 s and sustained 2-5 s epochs. This makes U, R, C, classical RPE, unsigned surprise and action jointly identifiable before assigning single-cell functional classes.
