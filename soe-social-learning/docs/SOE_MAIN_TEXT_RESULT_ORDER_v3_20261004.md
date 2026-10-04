# SOE main-text result order v3 — 2026-10-04

## Result 1 — Social observation creates a learned social-reward state
Phenotype + formal SLM + behavior model comparison.

Key positioning:
behavior alone is computationally underdetermined; SLM is a compact mechanistic family rather than a claim of universal behavioral-likelihood dominance.

## Result 2 — Social observation is an adaptive information-foraging process, and a mouse-derived SLM is generatively sufficient
Start with social information value:
- full social state has positive decision value in 22/27 learner animals;
- social information becomes less decision-relevant later in learning;
- its value is higher in behavioral states where external information can alter action.

Then introduce the mouse-derived Artificial SLM Agent:
- parameters/rules estimated from training mice;
- held-out actions and outcomes are generated, not replayed;
- closed-loop learning trajectories and local outcome-conditioned strategy are reproduced;
- action and outcome organize transition through the frozen 12-motif behavioral space;
- autonomous transition-exemplar world removes held-out observer-state replay.

Biological meaning:
mechanistic sufficiency of the inferred social-information controller, not a generic AI trained from scratch.

## Result 3 — A generic recurrent learner independently converges on SLM-like policy coordinates
Train GRU actor-critic without privileged SLM latents in the empirical 12-motif social world.

Action:
Observe / No-observe.

Artificial reward ontologies:
- Active-only;
- Active+Passive food;
with observation cost, calibrated on training animals.

Do not redefine the mouse phenotype with the artificial reward objective.

Main result:
a flexible recurrent agent solves the task and generates substantial motif occupancy/transition structure; adding explicit SLM memory/belief coordinates improves held-out reconstruction of its learned policy in 30/30 fold x seed x reward runs.

Interpretation:
SLM is a compact coordinate system for a policy that can emerge in a more flexible learner; this does not imply exact algorithmic identity.

## Result 4 — Artificial SLM regenerates real-mouse computational geometry, and VTA resolves it in biological time
Use the same five-fold Full-SLM contract on:
- real held-out mouse trajectories;
- autonomous Artificial-SLM trajectories.

Real vs Artificial animal-level:
- policy rho=.789;
- |APE| rho=.497;
- mean RPE rho=.771;
- |delta Active belief| rho=.734.

Outcome-profile geometry is highly preserved.

Then present independent real-VTA adjudication:
Early policy -> Middle learner-linked APE -> Post reward/update.

Critical wording:
the Artificial SLM does not simulate dopamine.
It regenerates computational variables whose temporally distinct expression is independently observed in VTA.

## Result 5 — Information availability and Active-belief updating are separable causal operations
Visual Block:
social-information availability/gating.

JAWS:
Active social-belief updating.

These are perturbations of an already established intact-agent framework, not the definition of Virtual Mouse.

## Result 6 — The learned social state changes later social learning
Observational fear + SAFN.

## Result 7 — The computational principle converges across tasks and species
Macaque/human/rat/naturalistic mouse/marmoset/neural external datasets.

## Artificial-agent figure sequence

### AI-1 — Information foraging and SLM generative sufficiency
- social information value;
- closed-loop trajectory;
- local social-strategy kernel;
- motif transition dependence on action/outcome.

### AI-2 — Real vs Artificial behavioral state space
- shared frozen v85 map;
- motif occupancy/transition;
- representative Real vs Artificial event-state movie.

### AI-3 — Independent recurrent-agent convergence
- generic GRU task schematic;
- learned motif occupancy/transition;
- SLM coordinate policy probe;
- optional hidden-state probes.

### AI-4 — Biological grounding
- real vs autonomous latent geometry;
- Early/Middle/Post VTA;
- model/evidence temporal adjudication.

### AI-5 — Causal perturbations
- Visual Block information lesion;
- JAWS Active-belief update lesion.
