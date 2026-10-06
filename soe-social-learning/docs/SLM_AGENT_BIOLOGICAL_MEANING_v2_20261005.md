# Artificial SLM agent — biological meaning and comparator hierarchy v2
Date: 2026-10-05

## Biological question
Held-animal prediction establishes that SLM variables forecast choices. A generative test asks a stronger question: when the fitted policy and update rules are placed back into an empirical social-foraging environment, are they sufficient to regenerate the organization of social-information sampling?

## Comparator hierarchy
The mouse-derived Artificial SLM Agent is compared with simpler generative alternatives using the same environment:
- baseline;
- Q-allreward;
- outcome-belief;
- Full SLM.

The intended claim is local/mechanistic generative sufficiency. Full SLM does not uniformly dominate every global metric.

## Global trajectory
Learning-trajectory Pearson r:
- baseline .7684
- Q-allreward .7768
- outcome-belief .7742
- Full SLM .7793

Trajectory RMSE:
- baseline .1691
- Q-allreward .1665
- outcome-belief .1670
- Full SLM .1683

Q therefore has a slightly lower global trajectory RMSE than Full SLM. The generative claim should not be framed as blanket superiority on global trajectory error.

## Local outcome-conditioned social strategy
Kernel correlation:
- baseline .2743
- Q-allreward .2735
- outcome-belief .2464
- Full SLM .3118

Kernel RMSE:
- baseline .0899
- Q-allreward .0867
- outcome-belief .0881
- Full SLM .0826

Kernel-sign agreement:
- baseline .5888
- Q-allreward .6138
- outcome-belief .5625
- Full SLM .6213

This is the clearest generative advantage: Full SLM better preserves the organization of local outcome-conditioned social strategies.

## Motif occupancy
Occupancy Jensen-Shannon divergence:
- Full SLM .05201
- Q-allreward .05366
- outcome-belief .05417

Animal-level paired tests:
- Full SLM vs Q: 24/40 improve, one-sided P=.0257
- Full SLM vs outcome-belief: 25/40 improve, one-sided P=.0130

Full transition-matrix correlation is essentially tied between Full SLM and Q; the occupancy result is the more informative state-organization readout.

## Generic recurrent learner
A separate recurrent actor-critic is trained to solve the same social-information acquisition problem without privileged SLM coordinates.

Adding SLM coordinates to the recurrent policy probe improves held-out prediction:
- Active-only reward: AUC gain +.2097, 5/5 folds, P=.03125
- Active+Passive reward: AUC gain +.2278, 5/5 folds, P=.03125
- Brier and NLL also improve in 5/5 folds for both reward modes.

Interpretation: SLM coordinates provide a compact description of policies learned by a flexible recurrent agent. This is convergence evidence; it does not imply exact algorithmic identity.

## Preferred integrated statement
The Artificial SLM Agent tests generative sufficiency, not generic predictive dominance. Its strongest advantage over simpler Q/belief agents lies in preserving local outcome-conditioned social strategy and behavioral-state occupancy. A separate recurrent learner supplies convergence evidence: policies learned under flexible optimization become substantially more predictable when expressed in SLM coordinates.

## Scope
The current principal agent freely generates Observe / No-observe and social outcomes inside an empirical social-foraging world. Native free feeding is not yet part of the main motif-world action space.
