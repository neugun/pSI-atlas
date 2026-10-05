# Reward-history × VTA dopamine: reader guide

Updated 2026-10-04.

## Task

100E is full-strength Ensure. 20E is Ensure diluted to 20% of the full-strength concentration. In variable sessions, 100E and 20E alternate every 120 s.

Feeding bouts are formed from the complete lick stream. An inter-lick interval greater than 5 s starts a new bout. Bout end is the final lick plus approximately 0.12 s. Bouts of 0.2 s or shorter and bouts crossing a 120-s reward boundary are excluded.

GRAB-DA fiber photometry is recorded locally in the ventral tegmental area (VTA), rather than in a downstream projection field.

## Matched-current conditions

H is 100E in a stable high-reward context. L is 20E in a stable low-reward context. S is 100E in the alternating session. N is 20E in the alternating session. H versus S and L versus N hold the current food constant while changing recent reward history.

## Notation

U is the current-reward term, coded 0 for 20E and 1 for 100E in the main models. It is not an independently measured subjective utility.

R is the stored reward reference formed from prior sampled reward identities. At each prior reward sample, R is updated as R <- R + alpha(U - R).

C = U - R is the current reward relative to the stored reference.

The legacy source-data column RWstate is C, not R. Therefore a negative coefficient on R and a positive coefficient on C are opponent descriptions of related geometry when current U is accounted for.

The coefficient that becomes positive around 3 s is the coefficient on C, not R. The previously reported RWstate coefficient is also a coefficient on C.

## Why the two U/R coefficient pairs differ

The standardized U/R model z-scores U and R before entering them together. The action-adjusted U/R model uses raw U and R after adding early and concurrent licking covariates. Their magnitudes should not be compared directly. Neither model constrains the two coefficients to be equal and opposite; equal-and-opposite weights are imposed only when a single C=U-R predictor is fitted.

## Pre-bout sign

The pre-bout C coefficient is negative. Before the first lick, the model assigns the current block identity but the animal has not yet sampled the current food. The pre-bout association is therefore treated as anticipatory/contextual organization of reward history, not as negative current reward value or a negative prediction error.

## Alpha

The optimum in the alternating natural-reward task is broad around alpha 0.15–0.16. Alpha 0.20 is held fixed for cross-task transfer because it remains close to the broad optimum across datasets. It is not interpreted as a biological constant.

## Cohorts

See NEURON_reader_cohort_table_v1.csv for animal IDs and overlap across matched-current, alternating-reward, quinine/hunger/LiCl, stimulation, inhibition, and semaglutide experiments.

## Acute stimulation versus stimulation history

Acute stimulation asks what dopamine stimulation does to the bout being stimulated and directly prolongs feeding persistence.

Stimulation history asks whether the recent sequence of stimulation ON/OFF reward samples affects a later bout after current stimulation condition and local adaptation are controlled. Past stimulation history changes later dopamine but does not produce a detectable later bout-duration effect.

These findings can coexist with the natural-reward result because natural reward history changes both the food-based reference and behavior, whereas an optogenetic history can be stored and read out neurally without enough downstream behavioral gain to alter gross bout duration.
