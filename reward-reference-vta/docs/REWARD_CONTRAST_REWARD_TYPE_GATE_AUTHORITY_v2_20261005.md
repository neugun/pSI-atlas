# Reward Contrast — Reward-Type Memory × Expression Gate Authority v2
## 2026-10-05 — current authority

### Supersedes
For current interpretation, this file supersedes:
- `REWARD_CONTRAST_REWARD_TYPE_GATE_AUTHORITY_v1_20261005.md`;
- the QE behavioral-expression cell in `NEURON_three_context_reference_evidence_v1.csv`.

The v1 files remain provenance. The earlier QE zero-shot log-duration result (P=.621) used a different question and is no longer the current behavioral-expression authority. The current test holds the present reward fixed at 100E and asks whether prior EE/QE history changes the response to that identical reward.

---

## 1. Central result

Reward contrast should be separated into three stages:

1. **current reward potency** — can the reward manipulation alter behavior now?
2. **history memory / neural readout** — does prior reward sampling leave a persistent state that changes later VTA dopamine?
3. **behavioral expression** — does that history state gain access to persistence/termination behavior?

The decisive new finding is that failure of behavioral contrast cannot be explained simply by choosing the wrong recency timescale.

### Natural 100E/20E
- current reward → behavior: **PASS**
- history → VTA dopamine: **PASS**
- history → behavior: **PASS**

### QE / quinine history
- current reward → behavior: **PASS**
- history → VTA dopamine: **PASS**
- history → behavior: **PROVISIONAL**

### VTA stimulation history
- current reward → behavior: **PASS**
- history → VTA dopamine: **PASS**
- history → behavior: **NULL**

Stim13 is therefore a direct dissociation: the current manipulation is behaviorally potent, its history is stored strongly enough to change later dopamine, but that history does not reliably change later bout duration.

---

## 2. Raw Stim13 reconstruction was repeated from source MAT files

Source:
`D:/3_PeriLC/Neurophotometry_MATLAB Code/5sboutanalysis/Contingent_animals/8animals_5s_contingent/0-2hrslongeranalysis`

Animals:
023, 029, 030, 034, 058, 066, 070, 071, 128, 130, 131, 133, 017.

For each animal:
- ON and OFF files share the same global `beh_norm` lick-time stream;
- `Lick_onid` and `Lick_offid` label every lick as ON or OFF;
- final saved `Boutduration` values were mapped back to `Feed_info.boutstart` by strict chronological subsequence matching;
- the reconstruction yielded exactly 923 ON + 910 OFF = 1,833 final bouts.

A lick-level reference was then rebuilt:

`R <- R + alpha * (U - R)`

with:
- U=1 for ON licks;
- U=0 for OFF licks;
- R0=.5;
- only licks strictly before the current bout contribute to Rpast.

### Exact validation at frozen alpha=.20

Neural model:
`AUC_S ~ Rpast + current ON + log duration + cubic session progress + animal FE`

- Rpast beta = **−0.230168**
- animal-clustered P = **.0142127**
- model R2 = .644395

Behavior model:
`log duration ~ Rpast + current ON + cubic session progress + animal FE`

- Rpast beta = **+.021639**
- animal-clustered P = **.742399**
- model R2 = .048580

These reproduce the existing 2026-10-04 authority essentially exactly. Therefore the new timescale analysis is grounded in a validated reconstruction rather than a new approximate dataset.

---

## 3. New decisive test: scan memory timescale instead of assuming alpha=.20

The per-sample update alpha was scanned from .03 to .60 in Stim13.

For intuition only, the exponential half-life in **reward samples/licks** is:

- alpha=.03 → ~22.76 licks
- alpha=.05 → ~13.51
- alpha=.10 → ~6.58
- alpha=.15 → ~4.27
- alpha=.20 → ~3.11
- alpha=.30 → ~1.94
- alpha=.40 → ~1.36
- alpha=.60 → ~0.76

This is a sample-count timescale, not elapsed clock time.

### Stim13 neural history is robust at every scanned timescale

AUC_S Rpast tests:

- alpha=.03: P=.01543
- .05: P=.01916
- .10: P=.01673
- .15: P=.01498
- .20: P=.01421
- .30: P=.01342
- .40: P=.01301
- .60: P=.01325

After BH correction across the eight scanned alphas:
- **8/8 remain significant**
- q <= **.01916**

The standardized neural coefficient is also extremely stable:
approximately −.062 to −.065 SD across the entire scan.

### Stim13 behavioral history is null at every scanned timescale

Log-duration Rpast tests:

- alpha=.03: P=.7479
- .05: P=.9972
- .10: P=.7931
- .15: P=.7529
- .20: P=.7424
- .30: P=.7295
- .40: P=.7137
- .60: P=.6824

After BH correction:
- **8/8 remain null**
- q >= **.9064**

The behavior incremental R2 is only about 0 to 1.4×10^-4 across the scan.

### Interpretation

The lack of stimulation-history behavioral contrast is **not** explained by choosing an alpha that is too slow or too fast.

A neural history trace is detectable from very long-memory to nearly one-sample memory regimes, while gross feeding duration remains insensitive throughout.

This upgrades the interpretation from:

> stimulation history is neural-only at alpha=.20

to:

> **stimulation history is neurally readable across a broad family of memory timescales, yet its behavioral expression remains absent across that same family.**

That is a much stronger memory-versus-expression dissociation.

---

## 4. Natural reward provides the positive comparison

Using the reconstructed Natural 100E/20E task with current reward and session progress controlled:

### Sustained VTA dopamine

History contrast predicts 2–5 s dopamine at all scanned values:

- alpha=.03: P=.000530
- .10: P=.000226
- .20: P=.000778
- .30: P=.000671
- .60: P=.001311

BH q <= .001311 for all five.

### Feeding duration

History contrast predicts log duration across the broad moderate-recency regime:

- alpha=.03: P=.00820
- .10: P=.00319
- .20: P=.00656
- .30: P=.00709
- .60: P=.10079

After BH correction:
- alpha=.03–.30: q ≈ **.01025**
- alpha=.60: q=.10079

### Interpretation

Natural reward history therefore enters both neural and behavioral outputs over a broad range of plausible recency scales.

At the extremely fast alpha=.60 limit, neural history remains but behavioral history weakens, which is consistent with behavior requiring a somewhat more integrated history state.

This is a sensitivity result, not evidence for a uniquely identified alpha.

---

## 5. QE same-current 100E is an intermediate case

The current reward is fixed at EE/100E. Only prior EE/QE sampling changes the history coordinate.

Coverage:
- 63 same-current 100E bouts
- 7 mice

### Neural AUC

Across alpha=.10, .15, .20, .30:

- all 4 clustered tests are significant;
- BH q <= .02253;
- serial-shift two-sided q <= .00665.

Thus QE neural-history transfer is not an alpha=.20 accident.

### Behavioral duration

Raw clustered tests:
- alpha=.10: P=.1045
- .15: P=.04159
- .20: P=.03399
- .30: P=.03442

Directional within-animal serial-shift tests:
- alpha=.10: P=.11184
- .15: P=.04510
- .20: P=.02850
- .30: P=.01995

After correction across the four scanned alphas:
- clustered behavioral q ≈ **.05546** at alpha=.15–.30;
- directional serial-shift q ≈ **.057–.060** at alpha=.15–.30.

### Interpretation

QE behavioral expression is **broad and directionally consistent rather than restricted to a single selected alpha**, but it remains just outside the corrected threshold and the animal-level cohort is small.

Therefore QE remains **PROVISIONAL**, not promoted to a strong primary behavioral claim.

This is precisely the status desired for a rigorous current authority:
the positive direction is retained without converting an underpowered result into a discovery.

---

## 6. What determines whether a reward produces contrast?

The current data argue against two simple models.

### Model A — “Only strong rewards produce contrast”
Rejected.

Acute VTA stimulation changes feeding duration:
- 11/13 animals in the persistence-promoting direction;
- paired P=.00342.

Therefore the stimulation manipulation is behaviorally potent.

### Model B — “Behavioral contrast appears whenever reward memory persists”
Rejected.

Stim13 history:
- changes later dopamine;
- survives full local/slow/future controls;
- remains neurally significant over alpha=.03–.60;
- nevertheless does not change later bout duration at any scanned timescale.

### Current architecture

A better decomposition is:

**reward potency**
→ **history formation**
→ **neural comparison/readout**
→ **behavioral access/gain**

The first three stages can be present without the fourth.

Thus:

> **Contrast susceptibility is determined not only by whether a reward is remembered, but by whether that memory is routed into the behavioral comparison/readout controlling the measured action.**

---

## 7. Biological implications

### Memory persistence and behavioral expression are separable

Stim13 is now the cleanest example:
- neural memory present;
- many memory timescales work;
- behavior absent.

Therefore “no behavioral contrast” should not be interpreted as “no stored reference.”

### Reward identity likely gates readout

Natural food-quality history reaches persistence robustly.
QE history shows a weaker/provisional but broad behavior effect.
Artificial stimulation history remains mostly neural.

A plausible next variable is therefore **reward identity / sensory-affective context**, not only memory strength.

### Behavioral endpoint matters

The current null concerns gross bout duration.
Other outputs may still express stimulation history:
- lick microstructure;
- approach latency;
- choice;
- vigor;
- affective/avoidance responses.

The present result supports weak duration readout, not absence of every behavioral consequence.

---

## 8. Highest-value next analyses/experiments

### 8.1 Same memory strength × different current reward identity

Match Rpast across bouts but change the current reward identity.

Ask whether:
- VTA history readout is similar;
- behavioral gain differs.

This directly tests a reward-specific output gate.

### 8.2 Same current reward × experimentally separated history strength

Prospectively construct high-R and low-R histories with the same current reward.

Pre-specify:
- sustained DA;
- log duration;
- termination hazard.

QE is the best near-term behavioral replication.

### 8.3 Delay × sample-count factorial

Independently vary:
- elapsed unsampled delay;
- number of reward samples;
- sampled reward value.

If neural R persists but behavior disappears with delay, retrieval/output gating is implicated.
If both disappear together, memory decay is implicated.

### 8.4 Convert the latent Stim13 neural reference into behavior

Because Stim13 already has:
- acute behavioral potency;
- robust history memory;
- no duration contrast,

it is the cleanest causal substrate for testing a downstream gate.

Manipulate the DA/NAc persistence pathway or candidate comparison circuits on current bouts matched for pre-existing Rpast.

---

## 9. Statistical boundaries

1. alpha=.20 remains the frozen cross-task primary value.
2. Alpha scans are sensitivity analyses, not post-hoc alpha selection.
3. BH correction is reported within endpoint across scanned alphas.
4. QE behavioral history remains PROVISIONAL after alpha-family correction.
5. Do not compare raw beta magnitudes across Natural, QE and Stim13 because predictors and neural endpoints differ.
6. Do not claim full dopamine mediation of history-dependent behavior.
7. Do not interpret sample half-life as elapsed-time half-life.
8. Do not infer the anatomical storage site of R from bulk VTA photometry.

---

## 10. Current data authorities

New 2026-10-05:
- `STIM13_reconstructed_history_bouts_v1.csv`
- `STIM13_memory_timescale_neural_vs_behavior_v2_BH.csv`
- `NATURAL_timescale_neural_vs_behavior_v2_BH.csv`
- `QE_same_current_timescale_scan_v2_BH.csv`
- `REWARD_MEMORY_TIMESCALE_EXPRESSION_SUMMARY_v1.csv`
- `NEURON_three_context_reference_evidence_v2_20261005.csv`
- `NEURON_reward_type_memory_expression_gate_v2_20261005.csv`
- `ED9_memory_timescale_vs_expression_gate_v1.png/pdf`

Primary earlier authorities retained:
- `REWARD_CONTRAST_REWARD_TYPE_GATE_AUTHORITY_v1_20261005.md`
- `REWARD_CONTRAST_STIM_LICKLEVEL_AUTHORITY_v1_20261004.md`
- `REWARD_CONTRAST_VALUE_VS_ACTION_AUTHORITY_v1_20261004.md`
- `REWARD_CONTRAST_BIOLOGICAL_MODEL_AUTHORITY_v1_20261004.md`

### Current one-sentence conclusion

**Reward history can remain neurally readable across a broad range of memory timescales without becoming behavior; reward contrast therefore depends on a separable behavioral expression gate, not simply on reward potency or memory persistence.**
