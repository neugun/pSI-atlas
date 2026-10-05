# Ten-mouse global biological synthesis V46

## Current authority

This authority integrates the ten real biological mice currently resolved in the project:
ANM54, ANM181, ANM112, ANM113, ANM185, ANM492241, ANM496190, ANM496191, ANM378231 and ANM372321.

## Current VTA cohort — five mice

The strongest cross-animal neural invariant is an outcome-to-late response structure rather than a fully invariant predictive/outcome/late PC1.

Across ANM54, ANM181, ANM112, ANM113 and ANM185, animal-level Fisher-mean outcome-versus-late cell-effect correlations are 0.633, 0.769, 0.404, 0.649 and 0.740. All five animals are positive. The five-animal mean is r=0.655 with animal-bootstrap 95% CI 0.534–0.740. A hierarchical null that breaks cell identity between outcome and late within each session gives p=2e-5.

Predictive-to-outcome and predictive-to-late coupling are weaker (five-animal mean r=0.288 and 0.215) and positive in 4/5 animals. ANM185 is the exception: predictive-outcome r=-0.039 and predictive-late r=-0.104, while outcome-late remains r=0.740. Therefore predictive/cue loading is allowed to vary across animals.

A complete three-window predictive/outcome/late PC1 is not used as a five-animal invariant. ANM54/181/112/113 have highly similar axes, but held-out ANM185 remains different after structural identity QC. This does not weaken the outcome-late result.

ANM112, ANM113-conditioning and ANM185 remain full high-quality datasets. Their shorter acquisition counts affect inferential resolution for particular contrasts but do not downgrade imaging, ROI or extraction quality.


### Calcium-kinetics boundary

Raw outcome-to-late coupling is not interpreted as independent proof of a sustained latent neural state. At the raw-response level, coupling remains positive in 5/5 animals at 8-10 s after outcome (five-animal mean r=0.664, bootstrap 95% CI 0.503-0.761), but longer delays are less uniform: 4/5 animals remain positive at 10-12 s (mean r=0.421) and 12-14.5 s (mean r=0.384), with ANM185 losing the delayed relation.

More importantly, AR(1) positive-innovation analysis in the four high-trial MAIN conditioning sessions is sensitive to the assumed calcium-decay constant. Under a very fast tau=0.5 s assumption, modest residual coupling remains in some windows, but for tau>=1 s aggregate cell-shuffle p values are 0.11-0.44 and split confidence intervals include zero. Trial-level carryover residualization also removes the relationship in several sessions, including ANM185. Therefore the current authority distinguishes a reproducible response-level outcome-to-late organization from the stronger claim of a kinetics-independent sustained neural state.

## Named 2021 cohort — three mice

ANM492241, ANM496190 and ANM496191 retain identical original MATLAB vtSel vectors across hunger, social and control within animal. Their nine response matrices are complete and clean, and the Gain/Phase/PC1 geometry survives raw-baseline-z versus historical normalization and leave-one-trial deletion.

Cross-animal geometry is context-specific. Hunger is the reproducible context:
- historical-normalized cross-animal state-RDM mean rho=0.721, global state-label null p=0.0020;
- raw-baseline-z mean rho=0.560, p=0.0063.

Social geometry is not shared across animals. Control is intermediate and representation dependent. Cell bootstrap places hunger above social in 99.96% of resamples in both representations.

The correct interpretation is therefore a robust within-animal low-dimensional coordinate plus a specifically conserved hunger-state geometry, not a claim that all contexts share an identical cross-animal layout.

## Legacy 2017 cohort — two mice

The legacy matrix resolves to ANM378231 and ANM372321; the two ANM372321 source lineages are within-animal robustness units and are never counted as two animals.

Cross-animal state geometry is robust to representation, state deletion and removal of generic cell responsiveness. In ROC space, raw cross-animal RDM rho is 0.901/0.870 for ANM378231 versus the two ANM372321 lineages. After subtracting each cell's mean across all 11 states, rho remains 0.824/0.851; after cell-wise z-scoring it remains 0.789/0.808. In N01, the corresponding cell-centered values are 0.747/0.738 and cell-z values 0.739/0.715.

State-label permutation for the residualized cross-animal comparisons is p<=1e-4 and cell-bootstrap confidence intervals remain positive. Removing each state in turn, including Fear, does not abolish the geometry.

## Final interpretation

The ten-mouse data support three levels of population organization:
1. In current VTA, a five-mouse outcome-to-late response structure is the strongest shared cellular temporal relationship, while predictive/cue loading is more flexible; fluorescence persistence alone does not establish a kinetics-independent sustained neural state.
2. In the named 2021 cohort, low-dimensional geometry is robust within each mouse, but cross-animal conservation is context-specific and strongest in hunger.
3. In the legacy 2017 cohort, state geometry is reproducible across real animals even after removing generic cell responsiveness and individual states.

The remaining global QC gap is historical raw-frame residual-motion re-audit for the 2021/2017 cohorts because the original raw imaging mount is not currently accessible.
