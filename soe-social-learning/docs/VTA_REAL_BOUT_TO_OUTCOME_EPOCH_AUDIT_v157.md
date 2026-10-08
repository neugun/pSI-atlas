# VTA matched DA epochs, v157

The source is the nine-mouse VTA FP `analysis_events_with_policy_latents.csv.gz`. Its 1,723 rows are all selected on `ActionLabel=ObsEat`; only `ObservationLabel=Obs` defines true observation. The true observation bout, not the constructed approximately 28.85-second ActionBout, determines the acquisition-stage DA window. The original fixed 0–6-second post-anchor DA response is retained without re-anchoring.

Source: same 695 real observation events and nine mice. Each animal contributes its own mean DA contrast (Active−Unrewarded or Passive−Unrewarded); the paired difference of contrasts across time windows is tested by all 512 possible exact animal sign flips, two-sided. All event selections are identical for the two DA readouts; there is no trial pseudo-replication.  Real Obs bouts last 0.5–10 seconds and end at least 0.5 seconds before the fixed result-period anchor. Post–Obs-bout outcome-contrast enhancement: Active versus Unrewarded +0.3600 AUC/s, 9/9, exact P=.00391; Passive versus Unrewarded +0.3522 AUC/s, 8/9, P=.00781. Active versus Passive phase enhancement not significant, P=.8867.

## Interpretation

Evidence level: exploratory temporal outcome discrimination, not direct proof of VTA DA teaching, RPE, or next-Observe credit assignment. Post-window signals may reflect consummatory licking, motor activity or arousal; neither current matching nor the covariate controls prove otherwise. The DA recording table does not cover all future Observe opportunities. Keep real-bout and fixed-window measures on identical event sets but as distinct biological epochs; retain the earlier source×outcome, RPE and causal JAWS analyses separately.

## Files

- [Primary contrasts](../data/VTA_matched_execpost_stats_v157.csv); [threshold sensitivity](../data/VTA_matched_epoch_robustness_v157.csv); [animal-adjusted estimates](../data/VTA_matched_epoch_adjusted_v157.csv).
- [Figure, SVG](../assets/VTA_matched_observation_vs_outcome_epoch_v157.svg); [PNG](../assets/VTA_matched_observation_vs_outcome_epoch_v157.png).
- Full source scripts and individual-event/animal details are retained privately on the authorized workstation under `C:\Users\Public\SOE_VTA_matched_readout_20261008`.

## Robustness and limits

At least 1 second separation: 486 events, Active 9/9 P=.00391, Passive 8/9 P=.00781. Maximum bout 5 seconds: 586 events, Active 8/8 P=.00781, Passive 8/9 P=.01172. Both stricter criteria: 403 events, Active 8/8 P=.00781, Passive 8/9 P=.01563. Excluding events with the NEXT selected anchor within 6 seconds: 610 events, Active 8/8 P=.00781, Passive 7/9 P=.01563. This does not remove unsampled licking/movement. Per-animal nuisance-adjusted analyses of demonstrator feeding, previous behavior, bout duration, time gap and session time preserve a positive estimate for both reward classes in all nine mice, exact P=.00391 each. Within-animal readout standardization agrees. Nuisance-model collinearity makes the unadjusted identical-event comparison the primary evidence. The first half supports Active 7/7 P=.01563 and Passive 9/9 P=.00391; Active is weaker in the second half (5/7 P=.09375), Passive remains 8/9 P=.01953.
