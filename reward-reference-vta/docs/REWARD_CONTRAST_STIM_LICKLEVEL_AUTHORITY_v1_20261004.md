# VTA stimulation lick-level reward-reference authority v1 — 2026-10-04

## Status

**PROVISIONAL-DIRECT-NEURAL**

This dataset now provides direct evidence that prior stimulation exposure can build a past-specific neural reference/adaptation state. It does **not** yet establish classical behavioral reward contrast, and it does not yet meet the same held-animal generalization standard as the Natural/QE reference results.

## 1. Provenance and reconstruction

Source:
`D:/3_PeriLC/Neurophotometry_MATLAB Code/5sboutanalysis/Contingent_animals/8animals_5s_contingent/0-2hrslongeranalysis`

Animals:
023, 029, 030, 034, 058, 066, 070, 071, 128, 130, 131, 133, 017.

For every animal, OFF and ON MAT files are two condition-specific views of the same recording:
- top-level `beh_norm` is identical across OFF/ON files;
- `Lick_offid` and `Lick_onid` partition the global lick stream;
- `beh_norm[Lick_offid-1]` exactly equals the OFF `FP.beh_norm`;
- `beh_norm[Lick_onid-1]` exactly equals the ON `FP.beh_norm`;
- index-mapping error is zero.

Final AUC-aligned bouts were mapped back to exact `Feed_info.boutstart` values by matching the saved final `Boutduration` vector as a strict chronological subsequence of `Feed_info.boutduration`.

This succeeded for all 26 animal×condition files with maximum duration mismatch = 0.

Final analysis coverage:
- 910 OFF bouts;
- 923 ON bouts;
- total 1,833 bouts;
- 13 animals.

## 2. True per-lick stimulation-history reference

The analysis uses the same update form as the Natural FullHistory model:

`R <- R + alpha * (U - R)`

where:
- `U=1` for stimulation-ON licks;
- `U=0` for stimulation-OFF licks;
- initial `R=.5`;
- only licks strictly before the current bout enter `Rpast`;
- the primary alpha=.20 is frozen from the Natural/QE shared recency analysis.

For current bout condition `U_current`, the stimulation-history contrast can be written as:

`Cpast = U_current - Rpast`.

Because current ON/OFF is explicitly controlled, inference on Cpast is equivalent to testing the prior stimulation reference Rpast with sign reversed.

A time-reversed future reference is reconstructed from licks strictly after the current bout and used as a directionality control.

## 3. Frozen alpha=.20 neural result

Outcome: current-bout dopamine intensity (`AUC_S`).

Base controls:
- current stimulation condition;
- current log bout duration;
- cubic session progress;
- animal fixed effects.

Past history:
- beta(Cpast) = +0.2302;
- cluster P = .0142;
- incremental R2 = .003735.

Future control:
- beta(Cfuture) = -0.1361;
- cluster P = .0953;
- incremental R2 = .001333.

Joint past+future model:
- past beta = +0.2075, P=.0621;
- future beta = -0.0628, P=.5297.

Animal-level joint-model slopes at alpha=.20:
- past effect: 9/13 positive Cpast slopes, median +0.1859, Wilcoxon P=.0266;
- future effect: median approximately zero, Wilcoxon P=.6355.

Equivalent Rpast interpretation: more prior stimulation predicts less current dopamine response.

## 4. Circular-shift validation

At frozen alpha=.20, circularly shifting the past-history state within animal×condition strongly rejects generic serial alignment:

- past beta = +0.2302;
- incremental R2 = .003735;
- two-sided beta permutation P = .00010;
- R2 permutation P = .00010;
- null 95th percentile R2 = .00049.

Thus the observed history effect is substantially larger than expected from the autocorrelation structure preserved by within-condition circular shifts.

## 5. Beyond local run adaptation

ON and OFF are highly interleaved rather than large session blocks:
- individual animals show approximately 15–59 ON/OFF switches;
- typical runs contain only about 1–7 selected bouts.

The following local variables were explicitly reconstructed from the raw lick stream:
- prior licks within the current ON/OFF run;
- prior selected bouts within the run;
- time since the most recent condition switch;
- lick count in the immediately preceding opposite-condition run;
- cumulative prior lick count;
- cumulative prior ON fraction.

After controlling local run variables:
- Rpast beta = -0.2292;
- cluster P=.0111;
- incremental R2=.003647.

After additionally controlling cumulative slow-session variables:
- Rpast beta=-0.2252;
- P=.0132;
- incremental R2=.003384.

Past+future with local controls:
- Rpast beta=-0.2092, P=.0519;
- future beta=.0565, P=.572.

Animal-level local-control model:
- 10/13 animals have negative Rpast slopes;
- median Rpast beta=-.1416;
- signed-rank rank-biserial = -.714;
- Wilcoxon P=.0215.
- future slopes show no concordance: rank-biserial approximately +.033, P=.946.

## 6. Conditional permutation after all controls

The strictest test residualizes:
- current condition;
- current duration;
- cubic session progress;
- animal identity;
- run-local licks/bouts;
- time since switch;
- previous-run sampling;
- cumulative prior licks;
- cumulative prior ON fraction.

Past beyond all controls:
- beta=-.2252;
- incremental R2=.003384;
- conditional permutation P=5e-5.

Past beyond all controls **and future reference**:
- beta=-.2061;
- unique incremental R2=.002524;
- conditional permutation P=5e-5.

Future beyond all controls and past:
- incremental R2=.000199.

This is the current inferential authority for stimulation-history specificity.

## 7. Behavioral dissociation

The same frozen alpha=.20 history state does not reliably predict feeding bout duration:
- past P=.742;
- future P=.330;
- joint past P=.389;
- joint future P=.218;
- past incremental R2 approximately .000096.

Therefore stimulation-history evidence is currently neural-only.

This is biologically useful rather than a simple failure:
a prior reward-like circuit state can persist and alter subsequent dopamine valuation without a detectable change in gross feeding persistence.

## 8. Held-animal generalization limitation

Held-animal OOF prediction of AUC/s:
- history improves MSE in 8/13 animals;
- median MSE gain=.0206;
- one-sided Wilcoxon P=.188.

Therefore do not describe the stimulation state as a universal cross-animal predictive model.

The correct hierarchy is:
- strong within-session conditional evidence;
- animal-level directional consistency;
- weak/incomplete held-animal prediction.

## 9. Current-condition interaction

Without the full local-history control set, Rpast is more strongly associated with AUC/s during current stimulation-ON bouts:
- OFF Rpast beta=-.0928, P=.125;
- ON Rpast beta=-.3308, P=.00171;
- animal-level ON-minus-OFF slope difference P=.0171.

However, after adding the full local/slow controls plus future reference, the past×ON interaction is no longer reliable (P=.202).

Therefore the manuscript-safe statement is **not** “history acts only on ON bouts.”

Use:
> Prior stimulation exposure builds a cumulative neural reference that attenuates subsequent dopamine responses beyond current stimulation, local run adaptation, session progress, and future-history controls.

## 10. Alpha profile

The neural effect is broad across per-lick alpha values:
- past-only cluster P is approximately .013–.019 from alpha=.03 to .60;
- the frozen shared alpha=.20 is significant without retuning.

This matters because the stimulation result does not depend on selecting a stimulation-specific alpha.

In joint interaction models, very slow alpha values show a more general history effect, while faster alpha values can show stronger apparent ON-specific modulation. Because the fully controlled ON interaction is not robust, this timescale decomposition remains secondary.

## 11. Interpretation and boundary

Current evidence supports:

**prior stimulation exposure -> persistent past-specific neural reference/adaptation -> reduced subsequent VTA dopamine response**

It does not yet support:
- a change in feeding duration;
- classical successive negative contrast behavior;
- a universal held-animal predictor;
- identity between stimulation history and sucrose FullHistory at the circuit level.

The most important conceptual contribution is a dissociation:

**reference memory can be neurally expressed without a detectable behavioral contrast endpoint.**

This provides a concrete mechanism for the broader hypothesis that rewards can differ because memory persistence and behavioral comparison/expression are separable.
