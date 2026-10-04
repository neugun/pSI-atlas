# Autonomous Artificial-SLM intervention closure v1 — 2026-10-04

## Contract

Five held-animal folds.
Primary inference: 27 learner animals.
Ten paired autonomous rollouts per fold/mode.
The same intact fitted SLM and transition-exemplar world are used across conditions.
Random streams are paired across intervention modes.

Modes:
1. control
2. sensory_mask
3. belief_gate = sensory mask + belief update blocked
4. full_info_gate = sensory mask + belief/Q/slow/feature credit blocked
5. jaws50 = Active-outcome belief learning efficacy reduced to 50%, with Passive/Unrewarded belief update rules left intact

The environment remains physically intact in sensory lesions.
The generated action can still occur.
This distinguishes information efficacy from the motor act of observing.

## Visual Block: sensory-mask result

Real Visual Block:
- SRI: r_rb=-.945, P=1.97e-6
- observation frequency: r_rb=+.200, P=.396
- observation duration: r_rb=+.009, P=.979
- observation occupancy: r_rb=+.188, P=.426

Thus real VB collapses the learned social phenotype without a systematic loss of gross observation.

Autonomous sensory mask, learner n=27:
- observation rate: control .4463 -> .4692
  - mean delta +.0228
  - median delta +.00708
  - r_rb=+.407
  - two-sided P=.0655
- Active contingency: .0940 -> .0856
  - all 27/27 lower
  - mean delta -.00842
  - median relative change about -9.0%
  - r_rb=-1.000
  - P=1.49e-8
- Active-belief mean: .0450 -> .0376
  - mean delta -.00742
  - median relative change about -11.3%
  - r_rb=-.767
  - P=.000209
- direct belief-update magnitude |dB_A|: essentially unchanged
  - r_rb=+.254
  - P=.258
- direct Q-update magnitude |dQ|: essentially unchanged
  - r_rb=.011
  - P=.972

Behavioral fidelity to intact real-mouse organization:
- trajectory r per animal decreases:
  - mean delta -.0337
  - r_rb=-.619
  - P=.00388
- trajectory RMSE increases:
  - mean delta +.00994
  - r_rb=+.550
  - P=.0112
- local kernel r does not reliably change:
  - r_rb=-.122
  - P=.594
- motif occupancy changes only weakly.

Interpretation:
a sensory-information lesion can leave the motor act of observation largely intact while making observation less effective at generating Active contingency and learned Active social value.

This is the closest artificial analogue of real Visual Block.

## Why a full belief gate is NOT the best VB mechanism

Sensory + belief gate:
- observation rate .446 -> .321
- 27/27 lower
- r_rb=-1
- trajectory r decreases strongly
- motif fidelity also worsens.

Full information gate:
- observation rate .446 -> .345
- r_rb=-.926
- trajectory and local kernel both degrade strongly.

These stronger gates abolish too much of the controller and are qualitatively less consistent with the real VB preservation of gross observation.

Use them as mechanistic over-lesion controls, not as the preferred VB simulation.

## JAWS: direct mechanism versus closed-loop propagation

### Fixed-event direct counterfactual

The original validated JAWS event sequence is held fixed.
Only Active-outcome belief learning efficacy is reduced.

At factor .5:
- Active-belief state shifts down in 9/10 informative animals
- r_rb=-1
- Passive belief shifts upward because the three-outcome probability vector renormalizes
- reward belief shifts downward.

This analysis isolates the direct update mechanism without allowing altered policy to change future experience.

### Autonomous JAWS50

In the closed-loop Artificial SLM Agent, selective Active learning attenuation changes future policy, outcomes and state transitions.

Learner n=27:
- direct Active-belief update magnitude |dB_A|:
  - control .003308 -> .002577
  - mean change -22.1%
  - r_rb=-1
  - P=1.49e-8
- Q update magnitude |dQ|:
  - .001835 -> .001825
  - mean change only -0.55%
  - despite directionally consistent r_rb=-.984
  - P=7.45e-8
- relative attenuation of |dB_A| is about 40-fold larger than |dQ|.

Downstream:
- observation rate .4463 -> .4287
  - median relative change about -4.2%
  - r_rb=-.984
- Active contingency is essentially preserved:
  - .0940 -> .0946
  - P=.052 two-sided
- Active-belief mean decreases:
  - .0450 -> .0413
  - r_rb=-.587
  - P=.00645
- Active-minus-Passive belief decreases in 24/27 learners:
  - r_rb=-.889
  - P=6.66e-6
- Passive belief and mean Q state also shift secondarily because altered policy changes subsequent experienced outcomes.

Behavioral organization:
- global trajectory correlation is essentially unchanged:
  - mean paired delta -0.000084
  - r_rb=-.016
  - P=.953
- trajectory RMSE worsens slightly:
  - mean +.00436
  - P=.0319
- local strategy-kernel correlation decreases:
  - mean delta -.01234
  - r_rb=-.582
  - P=.00700
- motif occupancy is only weakly affected.

Interpretation:
a selective Active-belief teaching lesion does not collapse the global behavioral trajectory.
It preferentially weakens the targeted update and reorganizes local social strategy; other latent-state differences arise downstream through closed-loop feedback.

## Relation to real JAWS

Real JAWS:
- SRI endpoint r_rb=-.927
- acute Active belief r_rb=-1
- continuous Active belief r_rb=-.927
- session Active belief r_rb=-.964
- Active-specific belief r_rb=-.927
- Active-Passive per episode r_rb=-.964
- choice-kernel update r_rb=+.164, P=.695

Use two artificial analyses for two different claims:
1. fixed-event lesion -> direct mechanistic selectivity;
2. autonomous lesion -> downstream behavioral consequences.

Do not use autonomous secondary Passive/Q shifts to argue that JAWS directly targets those states.

## Stochastic-rollout audit

The autonomous world is stochastic.
Averaging more rollouts reduces Monte-Carlo noise in posterior-predictive fidelity without changing the model:
- 1 rep trajectory r=.400
- 2 reps=.495
- 3 reps=.532
- 5 reps=.578
- 10 reps=.622

RMSE decreases monotonically over the same averaging sequence.

The prior approximately .506 result is therefore consistent with a low-rep Monte-Carlo estimate.
Current intervention inference uses ten paired rollouts and animal-level paired effects.

Do not describe the higher 10-rep r as a model improvement.


## Native-feeding boundary

The current autonomous Artificial SLM is an event-level social-information controller.

It freely generates Observe / No-observe and the downstream social-learning state, but it does not yet generate a native future feeding action from a strict pre-action decision grid.

Therefore:
- do not call an artificial latent ratio canonical SRI;
- do not claim quantitative reconstruction of the full feeding endpoint under Visual Block or JAWS;
- use Active contingency, belief/update, learning-trajectory fidelity, local strategy and motif occupancy as artificial-agent endpoints.

A true Observe / Feed / Other extension requires a separate all-frame decision contract with future feeding onset defined after the decision time.
