# VTA exploratory observation × outcome interaction (v148; 2026-10-08)

## Why this addresses the paper's biological question
The SOE story asks how social information sampling, subsequent own feeding and outcome feedback are linked. The FP table used for most recent Post analyses is not the general Observe/No-observe action universe: source `ActionLabel=ObsEat` in all 1,723 selected events, while `ObservationLabel` distinguishes the 1,045 events with prior real observation and 678 without. Post0–6s DA is available in 1,714 events across nine independent animals.

We therefore asked a compatible question: **is the recorded outcome-evoked DA response conditional on whether a real social observation occurred before that outcome?** This probes state/outcome interactions. It does not itself establish next-choice prediction or causal learning.

## Frozen inputs and tests
- Source: `neural_da/dudman_policy_update_v1/analysis_events_with_policy_latents.csv.gz`; `DA_Post06_AUCperSec` and exact outcome anchor. The old `DA_ActionBout_AUCperSec` is excluded because it is a model-extended interval, not a true behavior bout.
- Baseline: active/passive event outcome, demonstrator feeding state, pre3 demonstrator feeding, observer inside/outside pre-state, and session time polynomial terms 1–3.
- Nested families, in the fixed order:
  1. + actual observation presence (0/1);
  2. + observed × demonstrator feeding;
  3. + observed × Active and observed × Passive outcome interactions.
- Every model uses all available events for eight training animals, nested inner held-animal selection of Ridge alpha (0.1/1/10/100/1000), and untouched held-out predictions in the ninth animal. Data from the test animal never select alpha. Primary prediction metric = mean squared error on held-animal Post DA. Effect tests = animal-level exact two-sided sign flips, no event-level pseudo-replication.
- Separate prespecified alternatives: Q-RPE+absolute RPE and additional source beliefs, assessed from the same outcome/state baseline.
- This is **exploratory model-family screening**, not a preregistered confirmatory single-hypothesis test. Full sequence and alternative families are retained, including negative contrasts.

## Results and robust bounds
Stepwise compared with preceding layer:
- + observation presence: 5/9 positive, mean ΔMSE −0.000608, P=.46094.
- + observed × demonstrator feeding: 4/9 positive, mean −0.000054, P=.94922.
- + observed × outcome identity after the above: **7/9 positive, mean +0.013683, median +0.003089, two-sided P=.03125**.

Compared directly to outcome/state baseline: full observation×outcome specification 7/9 better, +0.013021 MSE, P=.035156; RPE+|RPE| 7/9 and +0.015235 but P=.066406; four source-belief additions 3/9 and P=.89453. Across the four selected exploratory incremental comparisons the best two have BH FDR **q≈.0703**, therefore no family-wise q<.05 positive finding.

Targeted falsification: 300 shuffles of observation label within exact (session, outcome, demonstrator feeding state, 300-s bin), keeping training-only fitted alphas fixed. Real gain +0.013683 exceeds the conditional shuffled distribution with empirical one-sided P=.02326. Shuffled distribution median +0.012306 itself retains the between-group structural effect: the incremental advantage of the actual pairing is quantitatively small. This is not an independent experimental validation.

Influence/temporal sensitivity:
- Excluding ANM1 yields 6/8 positive, mean +0.00352, exact P=.0625. ANM1 is the largest contributor to the overall mean.
- Source event counts in session first/second halves: 7/9 and 6/9 direction-positive; two-sided P=.05859 and .09375. Only 4/9 are independently positive in *both* halves.
- Animal-resampling bootstrap 95% interval for mean gain roughly +0.00137 to +0.03497; this is a sensitivity interval, not a multiplicity-corrected discovery claim.

## Appropriate conclusion and what it does NOT establish
This is early evidence that VTA Post DA may depend on an **interaction between previous social observation and the subsequently obtained result**. It is biologically closer to context-specific outcome evaluation than a general scalar DA response. But it does **not** yet prove the precise SLM credit variable, neural teaching causality, adaptation of the next sampling policy, or all-animal social behavior. The separate JAWS Active-credit manipulation and Early/Middle dopamine estimates are independent lines of evidence; their estimands must not be equated.

Follow-up: use full real behavior opportunities, not ObsEat-conditioned only; model actual own Feed onset and outcome availability explicitly; match visual observation onset/offset to the FP clock; include movement/time/lick vigor and independent 415 control subtraction; test real Observe×Outcome responses against stronger non-social visual and pseudo-source controls; replicate in an independent set of animals. OXT intervention and NAc/DMS site/learner analysis stay private until physical condition and histology QC pass.

## Artifacts
- [Reproducible exploratory summary](../data/SOE_VTA_source_outcome_stepwise_v148.csv).
- [Leave-one-animal sensitivities](../data/SOE_VTA_source_outcome_loo_sensitivity_v148.csv).
- [Within-session half splits](../data/SOE_VTA_source_outcome_halves_v148.csv).
- [Exploratory neural figure PNG](../assets/SOE_VTA_source_outcome_interaction_exploratory_v148.png), SVG and PDF available alongside.
- Original processing scripts and full per-event predictions retained in the authorized local workstation, not copied to the public website.
