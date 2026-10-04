# Generic recurrent agent -> SLM convergence v2 — 2026-10-04

A generic actor-critic GRU was trained in the same empirical 12-motif social world without SLM latent variables as inputs.

## Artificial strategy
Mean motif occupancy correlation with held-out learner animals:
- active-only reward: 0.745
- Active+Passive reward: 0.757

Mean transition correlation:
- active-only: 0.528
- Active+Passive: 0.533

## SLM compresses generic recurrent policy
Across 5 folds x 3 independent seeds x 2 reward ontologies:
- mean Brier gain from adding explicit SLM coordinates to current motif = 0.0332
- mean NLL gain = 0.0768
- mean AUC gain = 0.2187
- all 30 runs improve on all three metrics.

At the fold level, each reward ontology has 5/5 positive folds for all three policy metrics.
This is convergence evidence, not proof that the GRU literally implements the exact SLM update equations.

## Hidden-state probes
The generic GRU hidden state linearly contains:
- strong information about its own policy (R2 ~ .997-.999);
- partial information about slow/fast memory and Active belief;
- weaker information about Passive/Unrewarded belief.

## Biological adjudication
Behavioral flexibility alone does not establish mechanism.
Frozen real-VTA evidence shows the SLM temporal decomposition is positive across Early policy, Middle APE and Post update, whereas the TinyRNN behavioral alternative does not reproduce that three-stage temporal structure.

Interpretation:
a flexible recurrent agent can solve the task, and its policy becomes substantially more predictable when explicit SLM state coordinates are supplied. SLM therefore acts as a compact mechanistic coordinate system for a more flexible artificial policy, while real VTA timing provides the biological discriminator.
