# Reward Contrast Storyline in the Uchida–Gershman Dopamine Framework

**Version:** 2026-10-07
**Purpose:** define the strongest, most defensible story for the current Reward Contrast manuscript/page.

## One-sentence story

**During ongoing consumption, VTA dopamine evaluates the current reward in a history-dependent state space: recent sampled rewards build a latent reference R; before the next sample, dopamine carries information about that reference, and once the current reward is sampled, current value U and stored reference R enter with opposite signs, producing a history-relative contrast signal that contributes to feeding persistence.**

The conceptual advance is therefore not “dopamine is not an RPE.” It is:

> **A successful RPE/generalized prediction-error account of ongoing consumption must include recent sampled reward history as part of the animal's internal state representation.**

---

## 1. The lineage from Uchida and Gershman

### Eshel / Uchida 2015–2016: dopamine performs comparison

The early work established that VTA dopamine is not a simple monotonic reward sensor. Dopamine neurons behave like actual-minus-expected reward, and local VTA circuitry contributes expectation-dependent subtraction.

This gives the first essential operation for Reward Contrast:

**current reward must be evaluated relative to something.**

### Starkweather / Babayan / Gershman / Uchida 2017–2019: “expected” depends on inferred state

When the environment is partially observable, the animal does not know its true state directly. TD learning should therefore operate on an inferred belief state rather than on the experimenter's observable state label.

This changes the question from:

> What reward occurred?

to:

> What state does the animal believe it is in when that reward occurs?

### Mikhael / Uchida / Gershman 2022: noncanonical dopamine can emerge from state uncertainty

Dopamine ramps and bumps can emerge under an RPE framework when state uncertainty and sensory feedback are represented appropriately.

The lesson is that unusual dopamine dynamics do not automatically falsify RPE; they may reveal the structure of the latent state representation.

### Gershman et al. 2024 and Qian et al. 2025: generalized prediction errors and learned state representation

The 2024 perspective explicitly argues that simple RPE theory is incomplete but can be generalized by solving the relevant representational and computational problems.

The 2025 prospective-contingency study is especially relevant. Apparent failures of conventional TD learning could be explained once the intertrial-interval state representation was improved, and Value-RNNs learned state spaces resembling the best handcrafted belief-state model.

This establishes the direct intellectual opening for Reward Contrast:

> **What latent state representation is required to explain dopamine during ongoing reward consumption?**

---

## 2. Science 2025 established the substrate; Reward Contrast asks what the signal contains

The Science 2025 study established:

- sustained consumption-phase VTA dopamine;
- bidirectional causal control of hedonic feeding;
- periLC→VTA circuit organization;
- interaction with GLP-1R satiety/semaglutide.

The current project asks a more computational question:

> **What determines the magnitude and meaning of this ongoing dopamine signal when the physical food currently being consumed is the same?**

The answer emerging from the current dataset is: **recent sampled reward history.**

---

## 3. Fig. 1 — The phenomenon: same current reward, different dopamine and behavior

H vs S and L vs N hold the current reward fixed while changing its recent reward context/history.

The key result is not merely that high and low rewards produce different dopamine.

It is:

> **The same 100E or the same 20E produces different sustained VTA dopamine and different feeding persistence depending on what was sampled before it.**

This establishes that the observable current reward U is not a sufficient state description.

In Uchida/Gershman language, the animal's internal state differs even when the current sensory reward is matched.

---

## 4. Fig. 2 — What updates the hidden state: sampling, not passive clock time

If the history effect were merely block timing, fatigue, or passive contextual drift, the latent state should change as time passes after a switch.

Instead:

- before the first sample, passive-time terms explain little;
- once reward is actually sampled, lick amount and feeding-time history carry additional information.

The most important interpretation is:

> **The hidden state is updated by experienced reward samples.**

This is more specific than saying “context matters.”

The proposed reference R is therefore a **sampling-integrated latent state**, not a generic time-since-switch or block-label variable.

---

## 5. Figs. 3–4 — What information is required in the state representation?

A recursive reference model summarizes prior samples:

R_(t+1) = R_t + alpha (U_t - R_t)

and defines the current history-relative coordinate:

C_t = U_t - R_t.

The central empirical point is not that this exact recursion is uniquely correct.

It is that **deeper cumulative sampled history contains predictive information that is not exhausted by current reward, recent/local history, simple context labels, or several flexible alternative latent-state models.**

### How the model zoo should be interpreted

The model zoo is not a leaderboard.

Each model asks whether a different state representation makes the explicit sampled reference unnecessary.

- **Belief / HMM:** Is categorical hidden state sufficient?
- **Reward rate:** Is R just a running average?
- **Pearce–Hall / Kalman / uncertainty:** Is adaptive uncertainty or learning rate the real state variable?
- **Canonical TD/RW-RPE:** Is a standard actual-minus-expected state enough?
- **Multi-timescale:** Is generic temporal integration sufficient?
- **Value-RNN / RNN+time:** Can a flexible learned recurrent state absorb the effect?
- **Unsigned salience:** Is absolute change sufficient without signed relative value?

Some of these models predict raw held-out activity very well.

That is important.

But raw prediction performance does not identify mechanism.

The stronger result is that cumulative FullHistory retains unique information after several strong alternatives are included.

Thus the present conclusion is:

> **An adequate internal-state representation must retain information about actual sampled reward history.**

Whether the brain implements this as an explicit scalar R, a learned recurrent latent state containing equivalent information, or a distributed population manifold remains open.

---

## 6. Fig. 5 — The strongest mechanistic clue: reference before sampling, subtraction during consumption

This is arguably the most important part of the current story.

### Before the current bout

Pre-bout dopamine covaries positively with stored reference R.

This is consistent with the animal entering the bout in a history-dependent baseline state.

### After current sampling begins

During sustained 2–5 s consumption:

- current reward U enters positively;
- stored reference R enters negatively.

This opposite-sign structure is exactly what a comparator requires.

Conceptually:

**before sample: reference state is present**

then

**after sample: current reward is compared against reference**

yielding a signal consistent with:

C = U - R.

The history-relative coefficient also becomes markedly stronger from early to sustained consumption.

This produces a much sharper story than “dopamine correlates with reward history”:

> **VTA dopamine dynamics are consistent with a state-to-comparison transition: recent history establishes a latent reference before the bout, and current sampling converts that latent state into a signed relative-value signal.**

This is the point where Reward Contrast becomes directly relevant to the Uchida/Gershman state-representation framework.

---

## 7. Fig. 6 — Generalization: the coordinate is not limited to one concentration contrast

The frozen natural-task history rule transfers to an independent quinine/reward-quality dataset, and several manipulations align with a common lower-to-higher value direction.

The safe conclusion is not that all reward manipulations have identical history updating.

It is:

> **The relative-value geometry is not specific to one 100E/20E concentration comparison.**

This motivates testing whether a common contrast axis generalizes across reward identity and ultimately across food and social reward.

---

## 8. Fig. 7 — Why the signal matters: it changes current policy

Consumption-period dopamine activation decreases bout-termination probability; contingent inhibition increases it.

Therefore sustained dopamine is not merely a passive readout of history-relative value.

It contributes to whether ongoing consumption persists.

The current computational chain is:

**sampled history → latent reference R → current/reference comparison → sustained VTA dopamine → bout persistence**

The stimulation-history dissociation is also informative: a neural history can persist without necessarily producing a measurable later change in gross bout duration.

That implies two separable computational stages:

1. reference/history memory;
2. downstream gain that converts neural state into behavior.

---

## 9. The strongest integrated interpretation

A simple cue-RPE account is insufficient because two physically identical current rewards can evoke different sustained dopamine signals after different sampled histories.

But this does **not** require abandoning RPE/generalized prediction-error theory.

The stronger formulation is:

> **Reward history augments the state space over which value and prediction error are computed.**

One possibility is that VTA dopamine directly represents a signed contrast variable C.

A second possibility, fully compatible with the modern Uchida/Gershman framework, is that dopamine represents a generalized prediction error over an augmented latent state b_t that includes reference information R_t.

These possibilities are experimentally distinguishable.

---

## 10. The next decisive experiment

Use a fully crossed history × current reward design:

- high history → high current;
- high history → low current;
- low history → high current;
- low history → low current.

Then separately manipulate explicit cue expectation.

This orthogonalizes:

- U: current reward;
- R: sampled history/reference;
- C: U-R;
- classical RPE;
- unsigned surprise;
- reward identity;
- action.

At single-cell resolution, compare these models on held-out trials.

### If the same cells encode C across matched probes and days

This supports dedicated contrast-like populations.

### If the population contrast axis is stable but contributing cells rotate

This supports a distributed reference manifold.

### If an augmented-state TD/RNN model fully explains the matched-current effect

Reward Contrast becomes a concrete experimental identification of the state representation required by generalized RPE theory.

### If explicit C remains uniquely necessary even against strong learned-state models

That would support a more specialized comparator computation beyond generic recurrent state inference.

---

## 11. The manuscript-level claim hierarchy

### Claim 1 — Strong and directly supported
Recent sampled reward history changes sustained VTA dopamine and feeding persistence for the same current reward.

### Claim 2 — Strong
The relevant history is sampling-dependent and cumulative, not simply passive elapsed time or a categorical block label.

### Claim 3 — Strong but mechanistically phrased
The temporal coefficient structure is consistent with a latent reference present before sampling and a current-minus-reference comparison during sustained consumption.

### Claim 4 — Strong
Sustained VTA dopamine causally contributes to feeding persistence.

### Claim 5 — Important but still a model interpretation
R is a compact explicit representation of the required history information; the biological implementation could instead be a richer latent/recurrent population state.

### Claim 6 — Future test
Reward Contrast may be a domain-general reference computation shared by food and social reward.

---

## 12. What not to say

Avoid:
- “Reward Contrast disproves RPE.”
- “Dopamine encodes R.”
- “alpha is the biological learning rate.”
- “HMM is wrong because FullHistory wins.”
- “There is a dedicated contrast neuron class.”
- “All reward manipulations use the same scalar reference.”

Prefer:
- “observable-state / cue-only accounts are insufficient.”
- “sampled reward history is a necessary component of the internal state representation.”
- “pre-bout dopamine carries reference-related information; sustained dopamine shows opposite-sign current and reference coefficients.”
- “the explicit R model is a compact mechanistic hypothesis whose implementation remains to be identified.”
- “future crossed designs will distinguish explicit comparator coding from generalized prediction errors over an augmented state.”

---

## 13. The conceptual payoff

The Uchida/Gershman work asks:

> **What state representation makes dopamine responses computationally coherent?**

Reward Contrast provides a concrete answer for ongoing consumption:

> **The state must remember what was recently sampled.**

And the biological consequence is not merely better prediction.

That remembered state changes the value and action meaning of the same reward being consumed now.
