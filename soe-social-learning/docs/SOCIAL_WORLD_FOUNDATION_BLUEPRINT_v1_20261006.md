# Mouse Social World Model — field-scale blueprint v1
Date: 2026-10-06

## Mission
The target is not a better SOE classifier. The target is a **mouse-first social world model** that learns a reusable internal state of the social world from multiple animals, multiple timescales, neural recordings and interventions.

The state must answer four classes of questions:
1. **What is happening now?** Who is present, where are they, what are they doing, what information is available?
2. **What does each animal believe/value/need?** Familiarity, partner reliability, social need, reward/social credit, rank/capability and motivational state.
3. **What happens next?** Future social action, partner response, outcome, neural trajectory and longer multi-step interaction.
4. **What if the world changes?** Visual block, JAWS/optogenetic manipulation, changed partner, changed social content or altered social history.

## Why the current SOE/SWM is the right seed
The existing model already contains the rare ingredients missing from most behavior classifiers: content-specific observation, multiscale memory, prospective social efficacy, source/outcome credit, generative event/motif rollout, VTA temporal grounding and causal perturbations. The upgrade should therefore preserve the current SLM/SWM semantics while replacing the narrow observer-demonstrator state with a general multi-agent relational state.

## Architecture: Social World Model v2
### 1. Mouse/entity encoder
Each mouse receives a persistent entity token. Inputs include pose/kinematics, body configuration, sex/strain/age/device metadata when available, and an identity embedding that can be replaced by sensory identity when a literal ID is unavailable.

Use egocentric, scale-normalized features so the same action is represented similarly across arenas and labs. Preserve missing-keypoint masks rather than silently imputing everything.

### 2. Directed relation graph
At every time step create directed edges i->j with relative distance, bearing, facing, approach velocity, nose-to-nose/nose-to-tail distances, contact, target-relative body pose and recent interaction history.

A graph-attention/TransformerConv block updates each mouse from all other mice. This directly imports the strongest lesson from MABe2025: social action recognition improves when mice are processed as interacting agents rather than concatenated trajectories.

### 3. Fast temporal dynamics
A temporal encoder operates on each socially enriched mouse token. Benchmark a compact GRU/TCN against a Squeezeformer/Transformer. The purpose is not merely classification: it must predict masked frames/events and multiple future horizons.

### 4. Event and motif tokenizer
Maintain both continuous dynamics and a discrete behavioral vocabulary. Keypoint-MoSeq/VAME-like unsupervised motifs are useful as a tokenizer, but the canonical event ontology is directed:
agent, target, action, social content, outcome, context.

The present 5-event SOE world becomes one specialized slice of this larger event language.

### 5. Slow social-state memory
Use separate recurrent memory for:
- recent action/outcome history;
- minutes-scale social efficacy/reliability;
- social need/satiety;
- identity/familiarity and relationship history;
- rank/opponent capability;
- cross-day retained priors.

Do not force these timescales into one GRU hidden vector. The present SOE memory-horizon result already shows useful history over tens of trials.

### 6. Neural/social alignment
Use a **separate neural-dynamics stream by default**, aligned to but not assumed identical to the behavioral/social world state. External 13-region multifiber leave-one-animal-out tests show that current neural state robustly helps predict future neural state, whereas its increment for the next coarse social behavior is not stable across animals. The default behavioral policy therefore reads from the social core; neural-to-behavior fusion remains an optional diagnostic gate that must earn its way in with held-animal evidence.

Neural targets include:
- VTA DA social policy / APE / social RPE / credit;
- 13-region social-behavior-network photometry;
- CA2 identity/familiarity geometry;
- future Neuropixels/miniscope datasets.

Use CEBRA-like contrastive consistency and future-neural prediction as auxiliary objectives, while retaining generative social future prediction as the main world-model objective.

### 7. Intervention/action tokens
Interventions are explicit actions on the world: JAWS, optogenetic pattern, chemo, sensory block. The latent transition is conditioned on the intervention token and evaluated against no-action, wrong-action and shuffled-action controls.

### 8. Multimodal social communication
Add synchronized USV/audio, olfactory/social identity and tactile-contact channels when available. Missing modalities use masks and modality dropout so the core model can run on pose-only datasets.

## External architecture validation already completed
**Directed relation graph is required.** On the official CalMS21 animal-identity split (70 train, 19 unseen test animals), a quick deep SWM screen with the same training budget shows that true synchronized partner/relation state improves future-behavior NLL over resident-only state in 19/19 animals at ~0.4 s and ~0.8 s, and remains significant at ~2 s. Replacing the partner/relation stream with a within-animal time-shifted control gives nearly the same deficit as removing the partner, showing that the gain depends on the correct moment-by-moment relation rather than extra dimensions.

**Neural state is not the behavioral state by default.** In the 13-region social-behavior-network dataset, a fast leave-one-animal-out gate finds no stable neural increment for the next coarse social behavior, while current neural state improves future neural prediction in every evaluable animal. A shallow SWM quick screen reaches the same qualitative conclusion. This motivates a protected social/behavior core plus a neural auxiliary dynamics stream.

These are architecture-selection results, not final claims of external-pretraining transfer into SOE. That promotion is reserved for Stage30.

## Pretraining objectives
Use a weighted multi-objective curriculum rather than one supervised label loss:
- masked pose/keypoint reconstruction;
- masked agent/target identity prediction;
- relative geometry / TREBA-style expert attribute decoding;
- next-action and next-target prediction;
- next social-content/outcome prediction;
- future latent prediction at 0.5 s, 2 s, 10 s and event-scale horizons;
- cross-agent prediction: partner future from self+relation state and vice versa;
- contrastive identity/familiarity consistency;
- long-memory retrieval across separated encounters;
- neural-behavior contrastive alignment when neural data exist;
- intervention-conditioned future likelihood;
- closed-loop multi-step rollout.

## Mouse-first data curriculum
P0 datasets currently registered: User SOE / social-observation feeding, MABe Challenge 2025, CalMS21, MABe22 mouse triplets, 13-region social behavior network multifiber photometry, VTA DA social interaction / social prediction error, STFP cortical-amygdala social memory.

Recommended order:
1. MABe2025 + CalMS21 + MABe22 for broad social geometry/action pretraining.
2. Current SOE to teach observation, information content, value, credit and multi-step social foraging.
3. VTA social-RPE and 13-region multifiber datasets for neural alignment.
4. STFP for social-information-to-food-memory transfer.
5. CA2/social-memory and USV datasets for identity/familiarity and communication.
6. Cross-species datasets only after the mouse model is stable.

## Required evaluation hierarchy
A model is not promoted because its training loss improves. It must pass:
- held-animal;
- held-session;
- held-lab/domain;
- held-partner/identity where possible;
- social-content shuffle;
- wrong-social / no-social controls;
- future rollout against Markov, current-state MLP and recurrent controls;
- few-shot adaptation versus scratch;
- intervention true-vs-no-action, true-vs-wrong-action and shuffled-action;
- neural alignment on independent animals/datasets.

## Immediate engineering targets
1. Build a canonical adapter schema for MABe2025, CalMS21, MABe22 and SOE.
2. Pretrain an egocentric relational encoder using pose + pair geometry + masked/future objectives.
3. Add hierarchical fast/slow memory and the current SOE efficacy/credit heads.
4. Test whether external mouse pretraining improves held-SOE animals versus training from scratch.
5. Test whether SOE-trained slow-state heads improve STFP/VTA-social-RPE targets.
6. Only then scale model width/depth.

## Claim discipline
“World-best” should mean **broadest mouse-social state coverage + strongest held-domain transfer + longest validated memory + explicit causal intervention + neural grounding**, not simply the highest classifier F-score on one benchmark.
