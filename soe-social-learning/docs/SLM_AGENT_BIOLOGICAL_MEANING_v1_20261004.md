# Biological meaning of the Artificial SLM Agent — 2026-10-04

## What the agent is

The current Artificial SLM framework contains two conceptually distinct agents.

### 1. Mouse-derived Artificial SLM Agent

This agent is not a generic RL system trained from scratch to maximize food reward.

Its policy and update structure are estimated from real mouse SOE behavior:
- current social / dyadic state;
- multi-timescale history;
- contingency-specific social belief;
- sampling policy;
- APE;
- Q / RPE;
- cross-day slow prior.

The fitted mouse-derived computation is then placed back into a held-animal social-foraging world and allowed to generate:
- Observe / No-observe decisions;
- social outcomes;
- belief/value updates;
- behavioral-state transitions.

The biological question is therefore:

> Are the computations extracted from real mouse behavior sufficient to regenerate the organization of social information sampling?

This is a mechanistic-sufficiency / generative-validation test.

### 2. Generic recurrent RL agent

The generic GRU actor-critic is a different test.

It does not receive SLM latent variables as privileged inputs.
It is trained in an empirical 12-motif social world built only from training animals.

Its action is:
- Observe
- No-observe.

Its reward objective is evaluated under two biologically motivated ontologies:
- Active-only social reward;
- Active + Passive food reward.

An observation cost penalizes indiscriminate sampling.
The cost is calibrated using training animals only.

This agent asks:

> If a flexible learner must solve the same social-information acquisition problem, does it independently discover a strategy that can be described by SLM coordinates?

The answer is currently yes:
adding explicit SLM coordinates to current motif improves held-out prediction of the generic GRU policy in all 30 fold x seed x reward runs.

This is convergence evidence, not proof that the GRU implements the exact SLM equations.

## What biological behavior is being modeled

The current agent should NOT be described as a complete simulation of all social foraging.

It specifically models the social-information sampling / social-learning controller embedded within a foraging setting.

The relevant biological loop is:

partner / demonstrator state
-> observer behavioral state
-> Observe vs No-observe
-> Active / Passive / Unrewarded social outcome
-> social reward / information update
-> later sampling policy and behavioral-state trajectory.

Thus the current agent addresses:
- when an observer samples social information;
- how the consequence of observation updates learned social value;
- how those learned states alter later behavior.

Feeding is biologically central to the task and enters outcome/reward structure, but feeding is not yet a native free action in the primary 12-motif artificial agent.

Therefore avoid:
- "a complete virtual mouse";
- "a full social-foraging simulation";
- "the AI learns all feeding behavior".

Preferred descriptions:
- Artificial social-information sampling agent;
- Artificial SLM agent embedded in a social-foraging world;
- Generative model of social observation and social-reward learning.

## Current biological evidence chain

### A. Real mouse -> SLM
Held-animal behavior establishes a compact SLM family that outperforms low-dimensional RL and approaches flexible history-model ceilings.

### B. SLM -> generated behavior
The mouse-derived SLM generates:
- global learning trajectories;
- outcome-conditioned local strategies;
- motif occupancy and transitions;
- autonomous observer-state trajectories.

The fully autonomous transition-exemplar world removes held-out observer-state replay.

### C. Generic RL -> SLM
A generic GRU actor-critic learns the same social-information task without explicit SLM states.

Its learned policy becomes substantially more predictable when SLM coordinates are supplied.

Interpretation:
SLM is not merely a descriptive fit to one behavioral dataset; it resembles a compact solution coordinate system for a more flexible artificial learner.

### D. Artificial SLM -> real computational geometry
Using the same five held-animal folds:

Real mouse vs autonomous Artificial SLM:
- mean policy rho=.789, P=1.50e-9;
- mean RPE rho=.771, P=5.98e-9;
- mean absolute Active-belief update rho=.734, P=7.00e-8;
- mean absolute APE rho=.497, P=.00112.

Outcome-specific profile agreement:
- RPE median profile r ~1.00;
- Active-belief update median profile r=.994;
- APE median profile r=.899.

This shows that the artificial world regenerates not only surface behavior but also much of the computational-variable geometry seen in real mouse trajectories.

### E. Independent biological readout in VTA
Frozen real-mouse VTA evidence:
- Early: SLM sampling policy, r_rb=.810;
- Middle: SLM APE, rho=.667;
- Post: SLM RPE/update, r_rb=.867.

Generic behavioral alternatives do not reproduce the same Early/Middle/Post sequence.

The biological claim is therefore NOT:
"the artificial agent simulates dopamine."

The defensible claim is:
"the Artificial SLM Agent regenerates computational variables whose temporally distinct expression is independently observed in VTA."

### F. Causal tests
Visual Block and JAWS are secondary perturbation tests:
- Visual Block removes access to social information;
- JAWS interferes with Active social-belief updating.

These ask whether the computational coordinates identified in the intact agent are causally required.

## What the current framework does not prove

1. It does not prove that VTA neurons literally implement the exact SLM equations.
2. It does not simulate the entire mouse sensorimotor repertoire.
3. It does not yet make feeding a freely chosen native action in the principal motif-world agent.
4. Generic-GRU convergence does not prove algorithmic identity.
5. The autonomous world still uses an empirical partner/environment process learned from training animals.

## Manuscript-level interpretation

A concise biological interpretation is:

> Social observational eating can be viewed as an information-foraging problem. An observer must decide when social information is worth sampling, assign outcome-specific credit to those observations, and carry the resulting social-reward state forward to guide later behavior. A mouse-derived SLM is sufficient to regenerate substantial aspects of this behavioral organization. Independently, a flexible recurrent agent trained to solve the same information-sampling problem develops policies that are compactly described by SLM coordinates. The same SLM coordinates are expressed in VTA at distinct temporal epochs, linking an abstract computational solution to a biological teaching system.

## Preferred short label

"Artificial SLM agent in an empirical social-foraging world"

rather than

"AI mouse" or "full social-foraging agent".
