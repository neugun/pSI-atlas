# Reward Contrast — Global Evidence Audit and Execution Plan v2

**Date:** 2026-10-07. **Type:** scientific status and execution contract, not new experimental data.
**Starting Git authority:** e51220c. Preserve the complete Fig. 0–7 / ED1–10 record, including negative and provisional results.

## Scientific center

Science 2025 established sustained VTA dopamine during consumption, the periLC-to-VTA circuit substrate, and bidirectional dopamine causal effects on feeding. Reward Contrast asks what computation explains the sustained signal when current reward is physically matched but prior sampled reward differs.

Proposed information flow: sampled reward history → latent reference/history state R → sustained history-relative VTA dopamine in combination with sampling/action/state → feeding persistence. The explicit coordinate C=U−R is a compact hypothesis. A complete causal mediation from independently perturbed R through DA to behavior **has not yet been established**; an augmented-state generalized RPE remains a serious alternative.

## Figure evidence ledger

| Stage | Main observed result | Boundary and next test |
|---|---|---|
| Fig. 0 | Defines H/L stable and S/N alternating tasks, bout rule, local DA sensor, cohorts and neural windows | Preserve exact provenance, cohort overlap, and session/animal manifests |
| Fig. 1 | Aligned same-current history effect in 9/9 mice; feeding and sustained VTA DA each P≈.00391 | Stable vs alternating sessions are not a fully randomized reference manipulation |
| Fig. 2 | First-sample passive time adds at most ΔR²≈.00385 (P>.55); prior lick count and feeding exposure retain ΔR²≈.0321/.0451 | Lick count, volume, sampled time and passive elapsed time require orthogonal experimental manipulation |
| Fig. 3 | Held-out R²: current U .038; context .123; continuous history .175; context+history .178; deep FullHistory ΔR²≈.027, P≈.0067 | The alpha optimum is a broad timescale regime, not a directly measured biochemical constant |
| Fig. 4 | Registry has 31 named families; continuous-time HMM predicts strongly (relative MAE≈.923) but does not absorb uniquely predictive cumulative history | Distinguish separately tested, task-adapted, non-identifiable, mismatched and recovery-only families |
| Fig. 5 | In 192 qualifying bouts from 11 mice, C slope rises +1.458 from early to sustained, with 11/11 directional agreement; U positive and R negative after sampling | Examine survival/long-bout selection bias, early-vs-late action adjustment, raw signal and coefficient scaling |
| Fig. 6 | QE transfer in 7 mice adds ΔR²≈.0254, P≈.00141 | Transfer of a history computation does not imply a conserved time course or equal behavioral gain |
| Fig. 7 | Consumption-period activation decreases termination hazard (OR≈.690); contingent Jaws increases it (OR≈1.341). Stim13 retains past neural history ΔR²≈.002524, P=5e-5, but marginal duration P≈.742 | Acute DA causality and history encoding/expression are distinct experiments; nonsignificant duration is not proof of no effect |

Extended Data ED1–10 remain part of the evidential foundation: action-matching, nonlinearity, history vs proxy, positive/negative asymmetry, alpha sensitivity, physiological conditions, memory/expression hierarchy and local-history gate adjudication. No statistical statement should lack a visible panel, animal n, statistical test and corresponding reproducible source table.

## Cross-task claims that survive adjudication

**Natural:** Current potency, neural history, and marginal behavioral history are supported. Deep neural R main effect after local-history residualization remains detectable (exact-wild P≈.0083), while a unique local-history-independent R×current behavioral gate is not established.

**QE:** Neural history transfer is supported. Marginal behavioral reference and identity-conditioned expression are provisional, with small common-support cohorts and task-specific latency.

**Stim13:** Robust past ON/OFF neural history survives full controls, but no stable marginal duration effect is detected across alpha; apparent R×current duration effects are absorbed or weakened by recent local context. No universal deep-reference action gate is established.

## Identifiability and model contract — urgent correction

Because C=U−R, the columns U, R and C are exactly linearly dependent. If cue-RPE is defined as delta=U−E, U, E and delta are also dependent. A crossed experiment can increase support for independently manipulated U, R and E, but cannot make mathematical transforms of those variables independently estimable in the same unrestricted linear model.

Compare **alternative models**: an unconstrained U+R coefficient model vs a signed, fixed-opponent C model; a cue-based U−E error model; and a history-augmented belief-state TD/RNN model. Use nested held-out-animal/session/trial competition; report reverse unique-information increments only for non-collinear parameterizations. Do not claim that equally predicted probes force every generalized RPE to zero: history itself may influence inferred expectation.

Proposed mechanistic factorial: high/low sampled history × high/low independently trained cue expectation × high/low delivered reward, using balanced catch and omission probes. Validate behaviorally inferred expectation, empirical common support and design matrix rank before fitting. Separate cue, first sample, 0–2 s, sustained 2–5 s, and post-bout. Address trial censoring/conditioning on bouts lasting more than five seconds.

## New food/hedonic contrast

Retain the ecological alternating task but add a randomized, matched-current reward probe. For longer-term reference formation, use the previously specified **30-min baseline → 60-min rich/neutral/lean induction → 30-min identical 8% sucrose probe**. Cross sampling count, nutrient intake, elapsed time, sensory presence, and cue exposure with paired/yoked control conditions.

Run free-consumption and controlled intraoral delivery versions. Record DA, lick microstructure, positive/negative orofacial taste-reactivity measures, acceptance/rejection, re-engagement and termination hazard. Bout length alone is not a pure hedonic measure. Positive/negative mismatch asymmetry requires balanced gains/losses; current direct asymmetry evidence is most robust in QE, not universally across Natural and Stim13.

## Single-cell and molecule program

Existing D1–D9 longitudinal sessions span trace conditioning, 100E/20E/50E concentrations, and 100E vs quinine-adulterated 100E. They do not fully disentangle current U and prior R. Current traces must keep **raw ROI, exact CaRMA v3, Suite2p neuropil correction and local background** as separate linked views, along with trial/movie/ROI/mask/day identities. Agreement between two subtraction pipelines does not establish that neither removed condition-locked biological signal.

The deliverable is a complete cell×day×trial atlas, same-cell registration QC, trial PSTHs, raw/corrected sensitivity and held-out tests of U, R, constrained C, RPE, salience, reward identity, action and state. Then test cross-day population axes and cross-reward transfer. Dedicated contrast-class claims require stable same-cell tuning, held-out generalization, molecular/projection enrichment and selective causal dissociation. A stable population axis with changing contributing cells favors a distributed manifold. Link retrospective >100-gene EASI/EASEQ-FISH and projections only after functional evidence is stable.

## Social, observational, and circuit transfer

Social contrast must **hold female sensory exposure continuously present**: ON permits interaction; OFF preserves female presence but prevents interaction. Test ON→OFF vs OFF→OFF and OFF→ON vs ON→ON, female A→A/B, balanced barrier/olfactory/visual/timing controls. pSI stimulation is a calibrated **submaximal attack-threshold probe**, not itself a claim about reward identity; start calibration from 5/10/20/40 Hz and estimate the input-output threshold away from ceiling.

SOE allows a fundamentally different history source—observed others rather than self-sampled reward. Transfer a frozen food-contrast decoder to observational trials only with observer state, demonstrator reward, social relationship, visual access, familiarity and action/history controls. Keep OXT/VTA social mechanisms and NAc/DMS dopamine release as adjacent programs until independently analyzed.

Candidate mechanistic nodes include periLC, VTA DA/GABA, BLA, gustatory cortex/insula/thalamus, PBN, pSI and downstream striatal action pathways. Do not label any one as the biological R store without encoding-vs-probe phase-specific causal tests. Hunger, GLP-1R modulation, obesity, chronic stress/anhedonia and social isolation should separately vary history encoding vs probe state and test whether U, R, update rate, contrast gain or action-readout gain changes.

## Prioritized execution matrix

| Priority | Input | Concrete artifact and pass condition |
|---|---|---|
| P0-A | Fig0–7 + ED1–10 + current ledger | Unique source/test/n/P per claim; correct scale and plotting contracts; no inconsistent coefficient labels |
| P0-B | Task/model code and trial tables | Design-rank test, no future leakage, U+R vs constrained C competition, expectation-validated RPE alternatives |
| P0-C | All available 2P/CaRMA animals and days | Full raw/CaRMA/Suite2p ROI×trial×day QA; movies/masks, identity review, model-ready per-cell tables |
| P0-D | Natural/QE/Stim13 | Harmonized neural, marginal behavior, current-conditioned behavior and deep-reference PASS/PROVISIONAL/NULL |
| P1 | New factorial + identical-probe experiments | Pre-specified early/sustained DA and termination hazard endpoints; cue-RPE vs comparator identification |
| P2 | Same-cell repeated-day imaging / reward identity | Held-out functional components, stable population axes, molecular/projection follow-up |
| P3 | ON/OFF social access, partner identity, SOE | Independent social contrast and frozen cross-domain generalization |
| P4 | Phase-specific circuit and physiological perturbations | Distinguish R formation, comparator readout and dopamine-to-action expression |

## Publication and privacy contract

Main figures are square or close to square unless justified by many categories; use animal-level n, means/SEM, readable p-values, edit-friendly SVG, minimal grid, no redundant dot overlays on paired line plots, and direct discoverability without nested clicks. English and Chinese pages must both explain rationale → method → result → inference; failed controls remain traceable in Extended Data.

**GitHub Pages noindex/robots is not access control.** A public repository does not become private because links are hidden. Audit exposure before posting unpublished analyses; use real access control or encrypted private mobile views for material that must not be public.

**Scientific destination:** establish a history-built value state required for ongoing dopamine computation, identify its relationship with generalized RPE, determine whether it lives in dedicated cell types or a distributed manifold, and test pre-specified transfer from food to social valuation and physiological/disease states.
