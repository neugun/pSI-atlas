# SLM model logic and terminology authority — 2026-10-05

## 1. Default behavioral model

The default behavioral SLM is:

**mechanistic SLM state + one generic choice-persistence term**

The mechanistic SLM state contains the variables used for biological interpretation:
- current behavioral/social state;
- multiscale memory;
- sampling policy;
- source/outcome-specific social credit;
- value / reward-update variables.

The choice-persistence term captures generic serial choice bias. It improves behavioral prediction and therefore remains in the default behavioral readout. It is not used as the mechanistic explanation for social learning.

The full-history MLP is a **high-capacity ceiling audit**. It tests whether substantial predictive information remains outside the compact SLM representation. It is not the reference model that defines the value of SLM.

## 2. Why the SLM contains policy, APE and post-outcome update variables

These variables correspond to distinct moments in one Observe episode.

1. **Sampling policy**: before the action, the actor assigns a probability to Observe.
2. **APE (action prediction error)**: after the sampling action, APE is defined as
   **actual sampling action − pre-action policy probability**.
3. **Post-outcome update**: after the social outcome becomes available, reward/value and source-specific social credit can update.

This chronology is experimentally useful because Early and Middle VTA windows precede outcome availability. A reward prediction error cannot be computed from the current outcome before that outcome occurs.

## 3. Response to a single-RPE explanation

A single-RPE account is a serious comparator and is directly tested.

- Post-outcome DA is compatible with reward-update models. Q-all RPE is positive in the Post window (r_rb=.867, P=.0195), and aggregate reward-aligned DA can also be fit by other RPE-like formulations.
- Early sampling-policy DA is not recovered by Q/RPE (r_rb=.048); choice-kernel and Q+CK are negative, and TinyRNN is significantly wrong-direction.
- Middle learner-linked APE remains rho=.667 after conditioning on CK error, Q+CK error or Q error. Reverse competing-error tests after APE conditioning do not recover the learner-linked effect.
- SLM is the only tested family positive and significant across all three prespecified temporal axes.

The main mechanistic claim therefore rests on the **ordered temporal sequence**, not on exclusive ownership of reward-aligned dopamine.

## 4. JAWS terminology

Use the following terms consistently:

- **post-outcome Active social-credit update**: the within-session per-episode Active-belief update measured in alternating OFF/ON periods;
- **accumulated Active credit state**: the session-scale final Active-belief contrast;
- **APE**: the earlier actor-stage action prediction error; do not use APE as a synonym for belief/credit update.

JAWS evidence:
- Observe→Active conversion: .320→.193 under contingent inhibition, 8/10 lower, P=.00391;
- post-outcome Active social-credit update: +.002490 OFF → −.000815 ON, 10/10 lower, P=.001953;
- accumulated Active credit state: .0967 Normal → .0120 Full JAWS, 9/10 lower, P=.003906;
- gross observation fraction is preserved (P=.625);
- Standard and VTA-copy JAWS cohorts each show 5/5 lower endpoint direction.

Generic Active-Q accumulation also slows (.002208→.000963, P=.007812). The supported causal claim is therefore branch-level disruption of successful Active social-credit teaching, not mathematical isolation of a single scalar.

## 5. Native Feed conversion and training-stage boundary

The current short-latency Feed result is a learner-cohort analysis, not a prespecified late-days-only analysis.

Within 3 s of the previous Observe:
- Feed hazard after observing demonstrator feeding = .2273;
- after observing no demonstrator feeding = .1519;
- within-animal difference = +7.54 percentage points;
- 17/26 informative animals positive; P=.0377.

After residualizing a frozen self + current-social predictor:
- residual difference = +6.09 percentage points;
- 17/26 positive; P=.0445.

A first-to-second analyzed-session sensitivity in the 17 animals informative at both sessions gives:
- raw dem-feed contrast shift = +7.74 percentage points;
- 13/17 increase;
- rank-biserial=.556;
- two-sided P=.0448.

The residualized session-to-session shift is positive but not significant (P=.243). This supports acquisition sensitivity while leaving a late-training native-Feed reconstruction as a separate confirmatory analysis.

## 6. Behavioral logic of the multiscale state

The memory architecture follows independently recovered behavioral timescales:

- **seconds / next decision**: Active and Passive outcomes increase stopping by about +10.0 and +12.9 percentage points and reduce re-entry by about 9.0 and 8.3 percentage points;
- **roughly five minutes**: selected gamma=.95–.97 corresponds to 20–33 events, about 4.5–7.5 min; multievent history adds held-animal delta-NLL=.0348, whereas the best single-exponential eligibility trace adds only about .0001;
- **across days**: true chronological day order ranks 1/501 against 500 within-animal shuffles (empirical P=.001996); a retained previous-day prior improves 29/40 animals (P=.0125), strongest early in the next session.

This is the biological motivation for a multiscale state representation.

## 7. Preferred narrative order

1. Establish the learned behavioral phenotype and content-to-action conversion.
2. Show that social information has state-dependent value.
3. Recover the behavioral memory hierarchy from seconds to minutes to days.
4. Introduce default SLM as the compact model that integrates those requirements.
5. Test the mechanistic coordinates in VTA temporal dynamics.
6. Use Visual Block and JAWS to dissociate information access from post-outcome social-credit teaching.
7. Use generative agents and external datasets to test sufficiency and transfer.

This order keeps each computational layer tied to a biological question that was already exposed by the preceding experiment.
