# OXT / SF15 expanded optogenetic experiments, 2026-10-08

## Scientific scope
The old seven OXT mice and the 2026 Aug-Sep SF15 OXT_NAc_PVH animals are separate experimental cohorts, not 13 interchangeable replicates. Only true physical-animal × original-day × stimulation-state comparisons can establish optical inhibition effects.

## Original 7 mice
ANM118/119/121/122/125/126/129: original shuffle-corrected SRI contingent D50 OFF 3.222 to D51 ON 2.311; 7/7 declining, exact P=.015625. Noncontingent D52 OFF 3.379 to D53 ON 3.231, P=.796875. Paired contingent-versus-noncontingent interaction P=.25. Normal D21/D60 comparisons must be distinguished from acute OFF/ON.

## New SF15 data from original September 29 MATLAB batch
All values are Active SRI in ODD-numbered stimulation segments MINUS EVEN-numbered stimulation segments. This does NOT imply ON minus OFF until hardware/rig status is confirmed.

| Animal | Original day | Derived pseudodays | Odd minus even | Filename-source QA |
|---|---:|---|---:|---|
| 174 | 22 | 41/42 | -0.5914 | Derived D42 includes 15 unrelated ANM173 D28 segments |
| 180 | 22 | 43/44 | -3.9847 | Consistent |
| 184 | 26 | 45/46 | +0.6770 | Rig basename labels animal 180 while folder labels 184 |
| 173 | 28 | 47/48 | -0.3030 | Consistent |
| 179 | 31 | 49/50 | -0.2307 | Consistent |
| 305 | 32 | 51/52 | +1.4174 | Separate VTA-JAWS branch; do not pool |

Five provisional NAc animals: Active SRI 4/5 lower in odd segments, mean difference -0.88654, exact paired two-sided P=.375. Clean filename-only 173/179/180: 3/3 lower, mean -1.50610, P=.25. Passive PRI odd-minus-even mean +0.25445 (3/5 positive), P=.875. VTA animal 305 is an individual example only. ANM183 has original D0-1 and 185 D0 only; neither has verified optical pairing.

## Source-authority warning
The 53 numbered Day0-52 directories contain 6083 event files; derived Days41-52 contain 195 files with matching filenames and sizes in earlier original-day directories. Full hashes were not verifiable because byte-reading those files was denied. D42/174 has the 15-file ANM173 contamination, and D45/46/184 are annotated 180 in rig basenames. Do not treat these virtual days as dates, new independent sessions or proven ON/OFF conditions.

## Decision
Restore optical state from source hardware pulses and actual acquisition clock, verify subject/rack ID and histology, recover normal reference, stratify learner versus nonlearner only from an authorized cohort registry, then recompute Active SRI and Passive PRI, Observe-to-native Feed conversion, and photometry/behavior interactions on valid independent animals.

## Sanitized source results
[Per-animal SRI/PRI and provenance](../data/SOE_OXT_SF15_new_animal_opto_audit_v166.csv) / [Group parity tests](../data/SOE_OXT_SF15_new_opto_tests_v166.csv) / [Virtual source mapping](../data/SOE_OXT_SF15_pseudoday_provenance_v166.csv) / [Figure](../assets/OXT_SF15_recent_opto_provenance_v166.png). Raw filesystem paths and detailed private segment inventory are not published.
