# CaRMA 2P Tool V1

Executable, auditable Stage00→10 workflow for a new two-photon dataset.

## Minimum inputs for a new RAW_MOVIE dataset
- `dataset.yaml`
- `sessions.csv`
- raw TIFF or an already registered TIFF
- event CSV with unique `trial_id` and `event_frame` or `event_time_s`
- behavior CSV with unique `trial_id` and condition metadata
- ROI CSV (`roi_id,x,y[,radius]`) or NPY masks / Suite2p `stat.npy`

## Normal run

    python carma.py init <dataset.yaml> <project_dir>
    python carma.py run <project_dir>
    python carma.py status <project_dir>
    python carma.py report <project_dir>

`report` now writes a dataset dashboard plus one report per session. For every completed session it exposes the Stage00→10 ledger, inputs/parameters/outputs/QC, ROI overlay, per-ROI authority table, and a real single-ROI explorer with mask, continuous raw/background/final traces, event-aligned mean traces, and trial × time heatmap. The viewer is file:// compatible and can be opened by double-clicking `reports/index.html`.

## Selective rerun / invalidation

    python carma.py run <project_dir> --session ANM999_D1 --from-stage 03 --to-stage 06
    python carma.py invalidate <project_dir> --session ANM999_D1 --stage 03 --reason "changed extraction"
    python carma.py resume <project_dir>

Invalidation propagates only to downstream stages; upstream registration/ROI work is preserved.

## Per-ROI export

    python carma.py export-roi <project_dir>

The canonical Stage06 schema is exported across sessions to `exports/per_roi_all.csv` (and parquet when supported).

## Stage07/08 independent identity review

Stage08 produces candidates only. It never silently freezes cross-day identity.

    python carma.py identity-review-import <project_dir> --session <source_session> --reviewer reviewerA --decisions reviewerA.json
    python carma.py identity-review-import <project_dir> --session <source_session> --reviewer reviewerB --decisions reviewerB.json
    python carma.py identity-consensus <project_dir> --session <source_session> --min-reviewers 2

Consensus requires independent reviewer names and enforces one-to-one integrity. ACCEPT edges are frozen only after consensus; unresolved/conflicted candidates keep Stage08 at REVIEW_REQUIRED.

## Rich viewer bundle for migrated/reference sessions

For a session whose frozen checkpoint already contains per-trial `raw/bg/sub/time_s` arrays:

    python build_rich_roi_bundle_v1.py --session-dir <session_dir> --session-id <ANIMAL_DAY> --out <private_bundle.json>

The bundle includes reference-plane overlays, ROI mask crops, mean traces, trial heatmaps, ROI QC, trial metrics, cell models, and SHA256 source lineage. These bundles are private/local and must not be committed to the public Pages repo.

## Regression and reference validation

    python carma.py cold-test <work_dir>
    python validate_reference_invariants_v1.py

The cold test starts from a synthetic raw TIFF and must reach Stage10 plus a functional per-ROI report. The reference validator checks bundle animal/session consistency, candidate endpoint existence, ROI existence, duplicate IDs, and manifest counts.

## Persistent stage record

Each `sessions/<session>/stage_XX/` records:
- `inputs.json`
- `params.json`
- `outputs.json`
- `qc.json`
- `software_environment.json`
- stage-specific tables/images

`state.json` is the session source of truth.

## Boundaries

- Stage08 candidates are not biological identity until independent review consensus.
- Generic Stage04 is biology-blind; it does not replace stronger frozen METHOD_QC_V3/TRACE-CV authority in migrated sessions.
- Generic Stage09 is a basic population adapter; project-specific decoding/remapping remains an analysis layer.
- Public GitHub Pages contains contracts, summaries, code, and de-identified aggregate results. Unpublished raw traces, masks, private paths, and private rich bundles stay local.
