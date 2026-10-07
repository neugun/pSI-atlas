# Reward Contrast Future Experimental Blueprints

**Version:** 2026-10-06
**Purpose:** convert the Reward Contrast roadmap into executable experiments with explicit hypotheses, controls, readouts, analysis contracts, decisive outcomes, and scientific meaning.

---

# 1. Why the next experiments must change

The existing program has already established that recent sampled reward history changes sustained VTA dopamine and feeding persistence, even when the current reward is matched. The next phase should not simply repeat more 100E/20E block switches. The main unresolved problem is **identifiability**.

In the original alternating design, current reward, recent history, sampling, action, time since switch, satiety, and sensory identity are partially correlated. Bulk photometry can establish a population-level history effect, but it cannot determine whether the underlying computation is:

- a dedicated reference-memory state,
- a signed current-minus-reference comparison,
- a classical reward prediction error,
- unsigned salience or surprise,
- a reward-identity signal,
- a motor/persistence signal,
- a distributed state manifold,
- or a mixture of these signals across cells.

The next generation of experiments must therefore **orthogonalize the variables by design** before asking where the computation lives.

The central goal is:

> **Hold the current reward constant, manipulate the reference independently, and observe the same neurons and behavior while separately measuring current value, history, RPE, identity, internal state, and action.**

---

# 2. Shared experimental and analysis contract

Every major future paradigm should use the same conceptual variables.

- **U:** current reward.
- **R:** recent sampled reward reference.
- **C = U - R:** signed relative-value / contrast coordinate.
- **RPE:** current outcome minus explicit cue/context expectation.
- **Unsigned surprise:** magnitude of unexpected change irrespective of sign.
- **Identity:** sensory/nutrient/social identity of the outcome.
- **Action:** licking, approach, persistence, withdrawal, attack, switching.
- **Internal state:** hunger, satiety, metabolic/hormonal state, stress, social deprivation.
- **Relational state:** familiarity, social identity, distance, visibility, orientation.

The core analysis should never classify a neuron from one contrast alone. For each neuron, bout, or trial, compare models containing:

1. current reward only;
2. recent sampled history only;
3. current reward + history;
4. signed contrast;
5. RPE;
6. unsigned surprise/salience;
7. reward identity;
8. action variables;
9. internal-state terms;
10. interaction terms such as history × current reward and social cue × internal state.

For single-cell work:
- use held-out trials and held-out sessions;
- avoid circular cell selection;
- use split-half or nested cross-validation for functional labels;
- compare stable cell identity with stable population axes;
- report animal-level replication rather than pooling cells as independent biological replicates.

For causal work:
- perturb **reference formation**, **current comparison**, and **action expression** in separate epochs.

This timing separation is essential. The same manipulation can have very different meaning if delivered during history encoding versus during the current probe.

---

# 3. Experiment 1 — Fully crossed food history × current reward

## Question

Does recent reward history alter the neural representation of the current reward independently of the physical reward itself?

## Core design

Use a within-animal **2 × 2 factorial design**:

| History | Current probe |
|---|---|
| High | High |
| High | Low |
| Low | High |
| Low | Low |

A neutral-history condition can later be added to improve dynamic-range estimation.

The critical comparisons are:
- High-history → Low versus Low-history → Low
- Low-history → High versus High-history → High

These hold the current reward constant while changing the reference.

## Recommended structure

Two complementary implementations should be run.

### Ecological free-consumption version
- Mouse samples freely available liquid reward.
- Use the same bout definitions as the current project.
- Preserve licking, pause, re-engagement, and bout-termination structure.
- Best for behavioral significance and naturalistic persistence.

### Mechanistic intraoral / controlled-delivery version
- Deliver matched probe aliquots independent of approach and initiation.
- Reduce the confound between reward value and action initiation.
- Best for dissociating sensory/current-value coding from action-related dopamine.

## What to record

- VTA dopamine photometry or dopamine sensor.
- VTA single-cell 2P/CaRMA where feasible.
- Lick timing and microstructure.
- Bout initiation and termination.
- Pause duration.
- Re-engagement latency.
- Locomotion.
- Optional pupil and autonomic state.

## Critical controls

- Same physical current reward across history conditions.
- Counterbalanced history order.
- Matched exposure duration.
- Matched cue structure.
- Pair-fed or yoked-intake controls when history amount differs.
- Satiety and deprivation matched across comparison blocks.
- Session progress included explicitly in the model.
- Reward delivery and licking dissociated in the controlled-delivery version.

## Single-cell analysis

For each neuron, fit competing encoding models containing:
- U;
- R;
- C = U - R;
- RPE;
- unsigned surprise;
- lick rate;
- bout age;
- reward identity;
- session progress.

A cell is only classified as **contrast-like** if the history effect survives matched current reward and action covariates and predicts held-out trials.

## Decisive outcomes

### Supports a dedicated contrast computation
- Same-current probe responses differ systematically by history.
- C outperforms U-only and history-only models.
- The same cells preserve sign across sessions.
- The effect transfers across matched probes.

### Supports a distributed reference manifold
- Population decoding of C is strong, but individual cell membership rotates across days or reward identities.

### Weakens the reference hypothesis
- Once current reward and action are matched, history contributes no unique neural information.

## Scientific meaning

This is the single most important experiment because it directly solves the current U–R confound. It converts Reward Contrast from a descriptive history effect into a mechanistically identifiable neural computation.

---

# 4. Experiment 2 — Same-physical-probe induction

## Question

Can an identical reward be represented differently solely because the preceding reward environment differed?

## Design

A strong previously proposed version is:

1. **30-min baseline**
2. **60-min history induction**
   - rich history: e.g. 32% sucrose
   - neutral history: e.g. 8% sucrose
   - lean history: water or approximately 1–2% sucrose
3. **30-min identical 8% sucrose probe**

The exact concentrations can be optimized empirically, but the conceptual requirement is fixed: **the probe must be identical across history conditions**.

## Readouts

Behavior:
- first-lick latency;
- acceptance;
- lick rate;
- lick burst structure;
- bout size;
- pause duration;
- re-engagement;
- switching away;
- persistence.

Neural:
- pre-probe baseline;
- first-sample response;
- 0–2 s;
- 2–5 s;
- 5–10 s;
- later sustained dynamics.

## Controls

- pair-fed history;
- intragastric or non-oral calorie control;
- matched visual/olfactory cues;
- cue-only history without consumption;
- matched elapsed time without sampling;
- deprivation and body-weight state;
- sex/estrous when relevant.

## Key analysis

Estimate whether the probe response depends on:
- reward history identity;
- total calories;
- total licks;
- elapsed time;
- current probe;
- interaction history × current probe.

## Scientific meaning

This is the cleanest demonstration that reward value is **relational rather than intrinsic**. If identical 8% sucrose is represented differently after rich versus lean history, the experiment directly shows that the brain carries a latent reference state into the current experience.

---

# 5. Experiment 3 — Reference formation kinetics: sampling versus passive time

## Question

Does the reference update with elapsed time, with actual reward sampling, or with multiple timescales?

## Design

Vary history duration over a broad range:
- seconds;
- tens of seconds;
- approximately 2 min;
- approximately 10 min;
- approximately 30 min;
- approximately 60 min.

For each duration, compare:
- active reward sampling;
- reward present but inaccessible;
- cue exposure without reward;
- yoked elapsed time;
- matched number of licks delivered at different temporal spacing.

## Critical manipulation

After the history period, deliver the **same probe**.

## Readouts

- immediate probe response;
- contrast magnitude;
- persistence over successive probes;
- recovery back toward baseline;
- behavioral persistence and termination.

## Model comparison

Compare:
- single exponential update;
- dual-timescale update;
- finite-window cumulative history;
- event-count model;
- time-based decay model;
- HMM / latent-state model;
- adaptive learning-rate model.

## Decisive outcomes

- **Sampling-gated:** update depends on actual consumed samples, not passive time.
- **Clock-like:** elapsed time predicts the new reference without sampling.
- **Multi-timescale:** fast adaptation plus slower carryover is required.
- **State-reset:** one or a few new samples sharply reset the reference.

## Scientific meaning

This experiment identifies the **memory kernel** of reward contrast. It tells us whether R is best thought of as an event-integrator, a continuous latent state, a physiological adaptation process, or a hierarchy of fast and slow memories.

---

# 6. Experiment 4 — Explicit contrast versus classical RPE

## Question

Is sustained Reward Contrast simply another form of reward prediction error?

## Design principle

Make cue/context expectation and reward history independently manipulable.

Use contexts that predict the **same current probe**, while recent reward histories differ.

Expected identical probe:
- train and behaviorally verify cue-based predictions in each history;
- the cue-based RPE may be small for the expected probe; history-aware generalized RPE need not be zero;
- C can still differ because R differs.

Identifiability guardrail: C=U−R and cue-RPE=U−E are deterministic transforms, so do not enter U/R/C or U/E/RPE together as unrestricted regression columns. Cross U, sampled history R and cue expectation E by design, and compare the constrained C model with free U+R, cue-RPE, and augmented-state TD/RNN in held-out data.

Then add catch trials:
- unexpectedly high reward;
- unexpectedly low reward;
- omission.

## Variants

### Free-consumption version
Preserves ecological action.

### Intraoral version
Minimizes approach and seeking.

## Readouts

Separate:
- cue response;
- first-sample response;
- early consumption;
- sustained consumption;
- post-bout signal.

## Cell-level predictions

RPE-like cells:
- respond strongly to unexpected outcomes;
- diminish when outcome is predicted;
- should not differentiate two equally cue-predicted identical probes if the relevant inferred value state is truly matched; history-augmented RPE models may still differentiate.

Contrast-like cells:
- differentiate identical expected probes according to recent reference.

Salience-like cells:
- respond to both positive and negative unexpected changes.

## Scientific meaning

This is the experiment that would most clearly reposition Reward Contrast relative to canonical dopamine theory. It can show that sustained dopamine during eating contains a history-relative value signal that is not reducible to cue-triggered prediction error.

---

# 7. Experiment 5 — Positive versus negative contrast asymmetry

## Question

Are gain and loss relative to the reference implemented symmetrically?

## Design

Include:
- High → Low
- Low → High
- High → High
- Low → Low
- optional neutral baseline transitions

## Readouts

Compare:
- neural magnitude;
- latency;
- persistence;
- recovery;
- behavior;
- variance;
- cell recruitment.

## Models

Compare:
- symmetric learning rate;
- separate alpha+ and alpha−;
- asymmetric gain;
- separate positive and negative reference channels;
- LC-like asymmetric-update analogue.

## Single-cell question

Are positive and negative contrast:
- encoded by the same cells with opposite sign;
- encoded by separate populations;
- represented by different dimensions in population space?

## Scientific meaning

Asymmetry can explain why reward loss, frustration, aversion and reward gain often have different persistence and behavioral consequences. It also provides a bridge from hedonic contrast to social frustration/aggression.

---

# 8. Experiment 6 — Reward identity and cross-identity generalization

## Question

Is the reference a common value currency or an identity-specific memory?

## Candidate reward identities

Food:
- sucrose;
- Ensure;
- fat;
- protein;
- salt;
- quinine-adulterated reward.

Non-food:
- social interaction.

## Design

For reward A and B:
- A history → A probe
- A history → B probe
- B history → A probe
- B history → B probe

The initial implementation should use a manageable pair rather than every reward at once.

## Population analysis

Train a contrast decoder on reward A and test it on reward B.

### If transfer succeeds
Supports an abstract relative-value axis.

### If transfer fails
Supports identity-specific references or identity-specific mixing.

## Single-cell analysis

Separate:
- reward-specific dimensions;
- shared contrast dimension;
- cells contributing to each.

## Molecular follow-up

Ask whether:
- one molecular population contributes to the shared contrast axis;
- separate molecular types contribute to identity-specific axes.

## Scientific meaning

This experiment decides whether “relative value” is a general computational coordinate or simply a set of reward-specific adaptation processes.

---

# 9. Experiment 7 — Refined social contrast: interaction ON versus OFF

## Question

Does recent social reward history change the value/action meaning of an identical current social opportunity?

## Why the design changed

The original plan alternated receptive-female interaction with a condition that also included pSI stimulation and aggression. That design mixed:
- social value;
- action induction;
- aggression;
- stimulation;
- sensory context.

The refined design should isolate social value.

## Core design

Keep the female perceptually present in both conditions.

- **ON:** interaction/access allowed.
- **OFF:** exposure remains, but interaction is blocked.

Acute transitions:
- ON → OFF versus OFF → OFF
- OFF → ON versus ON → ON

## Social readouts

- approach latency;
- time near female;
- investigation;
- contact attempts;
- withdrawal;
- re-approach;
- ultrasonic vocalization;
- preference;
- redirected aggression;
- object biting.

## Neural readouts

- VTA dopamine;
- pSI population activity;
- candidate PBN/pSI inputs;
- optional OFC/BLA/vH/CA2-related nodes depending the experiment.

## pSI as a threshold probe

Use pSI stimulation as a **submaximal probe of action threshold**, not as the source of social reward.

Calibrate an input-output curve, using previous 5/10/20/40-Hz experience as a starting range. Choose a level that yields intermediate attack probability rather than ceiling behavior.

Measure:
- attack probability;
- attack latency;
- attack duration;
- threshold / I50;
- slope of the stimulation-response curve.

## Key interpretation

If the same pSI input produces different aggression output after different social histories, the result supports a history-dependent shift in action threshold or policy.

## Scientific meaning

This provides a direct social analogue of hedonic contrast and links reward history to aggression without conflating the reference manipulation with aggression induction.

---

# 10. Experiment 8 — Social identity specificity and generalization

## Question

Is a social reference attached to a specific individual or generalized across social partners?

## Design

History:
- approximately 30 min Female A ON
- matched Female A OFF / exposure history

Probe:
- Female A OFF
- novel Female B OFF

Possible extension:
- familiar versus novel female;
- male conspecific;
- juvenile conspecific.

## Readouts

- approach;
- investigation;
- attempt to access;
- DA;
- pSI threshold curve;
- decay over time.

## Interpretation

### Same-female only
Partner-specific reference memory.

### Transfer to Female B
Generalized social-value reference.

### Transfer only within sex/relationship category
Hierarchical social identity coding.

## Scientific meaning

This moves Reward Contrast from “social state” to **social identity and relational memory**, which is much more relevant to natural social behavior.

---

# 11. Experiment 9 — Observational reward history

## Question

Can another animal's reward history update the observer's own value reference?

## Foundation

The social observational feeding line already provides a causal framework:
- visual access matters;
- familiarity matters;
- observer VTA dopamine is engaged during demonstrator feeding;
- temporally contingent VTA-dopamine inhibition suppresses observational feeding;
- replayed/noncontingent timing does not reproduce the effect.

A particularly informative prior design used approximately 1-h sessions with alternating 2-min OFF/ON epochs. Contingent 635-nm inhibition was delivered for about 1 s after demonstrator licks, with matched replay controls.

## New reward-contrast version

Demonstrator history:
- palatable food;
- bitter food;
- transient malaise-associated food;
- no-reward control.

Observer probe:
- same food;
- different food;
- social approach;
- self-feeding.

## Model variables

Organize each trial as:

**external event**
- demonstrator feed;
- cue;
- food delivery;
- self-eat;
- outcome.

**relationship geometry**
- visibility;
- facing;
- distance;
- head direction;
- nose-to-nose;
- demonstrator identity.

**internal state**
- hunger;
- session progress;
- previous reward;
- learning status.

**action preparation**
- turn;
- approach;
- velocity;
- lick initiation.

**outcome**
- reward/no reward;
- palatability;
- contrast;
- social outcome.

Critical interactions:
- demonstrator feeding × visibility;
- demonstrator feeding × facing;
- distance × social identity;
- social cue × hunger;
- demonstrator feeding × history;
- social information × future action;
- reward × history;
- social × self outcome.

## Additional physiological readouts

- glucose;
- insulin;
- pupil;
- heart rate / HRV;
- ACTH/corticosterone;
- inflammatory/cytokine measures.

## Scientific meaning

This asks whether reward references can be learned **vicariously**, not just from self-consumption. It is a direct bridge between Reward Contrast and social learning.

---

# 12. Experiment 10 — Cross-domain food ↔ social contrast

## Question

Is there a domain-general relative-value computation?

## Design

Train a neural decoder on one domain and test it on another.

Examples:
- food rich/lean history → identical food probe;
- social rich/lean history → identical social probe.

Then test:
- food-trained contrast decoder on social trials;
- social-trained decoder on food trials.

A more ambitious causal version manipulates the same candidate circuit during both domains.

## Possible outcomes

### Cross-domain transfer
Supports an abstract relative-value coordinate.

### No transfer but shared downstream behavior
Suggests domain-specific references converging on common policy circuitry.

### Shared cells but different axes
Suggests multiplexing.

### Separate cells and separate axes
Suggests parallel reference systems.

## Scientific meaning

This is one of the most conceptually important experiments because it tests whether “reward contrast” is a general brain computation or only a food-specific phenomenon.

---

# 13. Experiment 11 — Circuit localization by encoding versus probe epoch

## Question

Which circuit elements build the reference, compare the current reward to it, and convert contrast into action?

## Food circuit candidates

Established or strongly motivated nodes:
- periLC current reward / feeding-related inputs;
- VTA GABA;
- VTA dopamine;
- downstream amygdala / reticular / striatal pathways.

Candidate upstream/downstream modulators from prior planning:
- LHA;
- PVH;
- NAc;
- BLA/CeA;
- pSI;
- SC-related pathways where appropriate.

## Social circuit candidates

- visual / superior-colliculus-related inputs;
- OXT-related social-state input;
- VTA dopamine;
- pSI;
- PBN→pSI;
- OFC/BLA/vH/CA2-related identity/context inputs.

## Timing-specific perturbation logic

### Perturb during history induction only
Tests reference formation / memory update.

### Perturb during the transition boundary only
Tests state updating.

### Perturb during current probe only
Tests comparison/readout.

### Perturb during action execution only
Tests downstream policy expression.

## Neurochemical timescales

Prior planning specifically separated:
- fast glutamatergic / GABAergic mechanisms;
- dopamine;
- slower GLP-1;
- neurotensin;
- OXT;
- cAMP-like intracellular state.

## Scientific meaning

This design can assign different circuit components to different **computational stages**, rather than simply showing that a region affects feeding or social behavior.

---

# 14. Experiment 12 — Longitudinal single-cell Reward Contrast

## Foundation from current D1-D9 CaRMA work

The existing longitudinal VTA series spans:
- D1/D2: trace-conditioning components;
- D3: 100E;
- D4: 20E;
- D5: 100E versus 20E;
- D6: 100E versus 100E + 3 mM quinine;
- D7: 50E;
- D8: 100E versus 50E;
- D9: 20E.

Current interpretation:
- common temporal / consumption scaffold;
- distributed reward-quality effects;
- animal-specific residual geometry;
- weaker evidence for a universal concentration-preferring cell class;
- no simple classical one-dimensional line attractor.

D6 reward-quality effects are particularly useful because they show a lick-independent neural component without requiring a large set of individually significant “value cells.”

## Next-generation recording design

Use the fully crossed history × current reward design under longitudinal 2P/CaRMA.

Target:
- enough repetitions for stable held-out decoding;
- approximately 40–60 analyzable trials per critical cell/condition set where feasible;
- repeated days for stability.

## Per-cell model competition

For each neuron compare:
- current reward;
- reference/history;
- signed contrast;
- RPE;
- unsigned surprise;
- identity;
- action;
- state;
- interactions.

## Population geometry

Measure:
- contrast axis;
- identity axis;
- action axis;
- state axis;
- cross-day alignment;
- within-animal versus across-animal geometry.

## Generalization tests

- same decoder across days;
- same decoder across reward identity;
- same decoder across social and food reward;
- decoder after internal-state change.

## Scientific meaning

This determines whether Reward Contrast is implemented by:
- dedicated stable cells;
- stable subspaces with changing cell membership;
- or a fully distributed state-dependent manifold.

---

# 15. Experiment 13 — Function-to-molecule mapping

## Question

Do functionally defined reference/contrast populations correspond to molecular or projection-defined cell types?

## Workflow

1. Record longitudinal single-cell activity.
2. Register same cells across sessions.
3. Assign functional evidence using held-out model competition.
4. Preserve spatial coordinates.
5. Perform retrospective EASI/EASEQ-FISH with approximately 100 genes.
6. Add projection identity where possible.
7. Test enrichment and causal predictions.

## Candidate marker families from prior planning

Examples include:
- Npy1r;
- Ntsr1;
- Esr1;
- Oxtr;
- Syn2 and broader disease-related markers.

These should be treated as candidate axes, not pre-specified “contrast markers.”

## Strong evidence for a dedicated class

Requires all of:
- stable same-cell tuning;
- matched-current generalization;
- molecular enrichment;
- projection enrichment;
- selective causal perturbation.

## Strong evidence for a distributed manifold

Would include:
- stable population decoding;
- weak or rotating single-cell membership;
- limited transcriptomic segregation;
- cross-domain population transfer without a single molecularly defined cell class.

## Scientific meaning

This experiment turns Reward Contrast into a function-to-cell-type problem and directly connects the project to the broader FSO platform.

---

# 16. Experiment 14 — Internal state and disease: encoding state versus probe state

## Question

Does disease alter current reward, the stored reference, the update rule, contrast gain, or action readout?

## Candidate states

Metabolic:
- fasting/refeeding;
- obesity;
- diabetes-related state;
- GLP-1R agonism;
- GIP;
- amylin;
- gastric/vagal manipulation.

Affective:
- chronic stress;
- inflammatory state;
- anhedonia-like conditions.

Social:
- social isolation;
- social enrichment.

## Critical design principle

Manipulate state separately during:

### History encoding
Does the state alter formation of R?

### Current probe
Does the state alter U or the transformation of C into behavior?

This 2 × 2 separation is essential.

## Example interpretations

### Obesity
Could produce:
- higher reference;
- compressed contrast;
- slower reference updating;
- normal neural contrast but reduced behavioral gain;
- altered GLP-1-sensitive output.

### Anhedonia / chronic stress
Could produce:
- weak positive contrast;
- prolonged negative carryover;
- impaired reference formation;
- intact reference signal but failed action translation.

### Social isolation
Could alter:
- current social utility;
- social-reference memory;
- partner identity coding;
- pSI aggression threshold;
- neural-to-behavioral coupling.

## Scientific meaning

The disease question becomes mechanistically specific. Rather than asking whether “dopamine is lower,” the experiment can identify **which computational variable is abnormal**.

---

# 17. Experiment 15 — Causal ensemble test

## Question

If contrast-related cells can be identified, are they necessary or sufficient for reference-dependent behavior?

## Strategy

After longitudinal functional identification:
- label or target candidate contrast-enriched cells;
- perturb during history encoding versus current probe;
- compare with identity-like and action-like populations.

## Strongest test

A double dissociation:

- reference/contrast population perturbation changes matched-current history effects;
- action population perturbation changes behavior without erasing the neural reference;
- identity population perturbation alters reward-specific decoding but leaves a generalized contrast axis intact.

## Scientific meaning

This is the point at which the project moves from correlational geometry to a causal computational circuit.

---

# 18. Decision tree for interpreting future data

## Outcome A: stable contrast cells + molecular enrichment
Conclusion:
- dedicated reference/contrast cell class is plausible.

Next:
- projection-specific causal manipulation.

## Outcome B: stable population axis + unstable individual cells
Conclusion:
- distributed manifold with stable computation.

Next:
- perturb population subspace or convergent downstream reader.

## Outcome C: history effect disappears after action matching
Conclusion:
- previous effect may be primarily policy/motor.

Next:
- move causal emphasis downstream.

## Outcome D: RPE explains only early response, contrast explains sustained response
Conclusion:
- dopamine multiplexes timescales.

Next:
- map early versus sustained cells/projections.

## Outcome E: food contrast transfers to social contrast
Conclusion:
- domain-general relative-value coordinate.

Next:
- identify common molecular/projection substrate.

## Outcome F: no food-social transfer
Conclusion:
- identity/domain-specific references.

Next:
- map convergence at policy/output stages.

---

# 19. Recommended project sequence

## Tier 1 — Solve identifiability
1. Fully crossed food history × current reward.
2. Same-physical-probe induction.
3. Explicit contrast-versus-RPE catch-trial experiment.
4. Reference-formation timecourse.

## Tier 2 — Establish generality
5. Positive/negative asymmetry.
6. Reward-identity generalization.
7. Social ON/OFF contrast.
8. Social identity and observational-history transfer.
9. Food-social cross-domain decoder transfer.

## Tier 3 — Map mechanism
10. Epoch-specific circuit perturbation.
11. Longitudinal single-cell imaging.
12. Function-to-molecule mapping.
13. Causal ensemble manipulation.

## Tier 4 — Disease and therapeutic relevance
14. Obesity / metabolic state.
15. Stress / anhedonia / inflammation.
16. Social isolation and social-state perturbations.
17. GLP-1 and other therapeutic-state manipulations.

---

# 20. The larger significance

The broad significance of Reward Contrast is not that the brain can distinguish rich from poor food. That is already expected.

The deeper idea is that the nervous system may carry a **history-dependent reference state** that changes the neural and behavioral meaning of the same present event.

If correct, this provides a common framework for:

- hedonic contrast;
- frustration;
- satiety;
- social disappointment;
- social opportunity;
- observational learning;
- reward identity;
- anhedonia;
- obesity;
- maladaptive persistence;
- aggression after social loss.

At the single-cell level, the key unresolved issue is whether this reference is implemented by dedicated cell classes or emerges from distributed population geometry.

At the circuit level, the key unresolved issue is whether reference formation, comparison, and behavioral expression are implemented by separable nodes.

At the translational level, the key unresolved issue is whether disease changes reward itself or changes the **reference against which reward is evaluated**.

That distinction can produce fundamentally different therapeutic strategies.
