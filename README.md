# pSI Localization Atlas

An interactive Allen Mouse CCFv3 reference for localizing posterior substantia innominata (pSI), checking the site in tissue, and reviewing the main anatomy/circuit figures from the 2021 and 2024 studies.

## Scientific definition

> pSI is the posterior part of Allen substantia innominata (SI) corresponding to the region targeted and validated in the experiments.

The published coordinates are Franklin–Paxinos surgical references. The live viewer loads real Allen CCFv3 histology and annotation slices and reports a bregma-referenced crosshair position together with the corresponding 50-µm CCF voxel. pSI is selected from the posterior Allen SI annotation and neighboring landmarks.

## Version 2.15

- new "Gene expression & spatial profile" page presenting MERFISH spatial-transcriptomics and Allen ABC WMB-10Xv3 scRNA-seq results for pSI: cell-type composition and spatial layout among its five anatomical neighbours, differential expression by functional gene category (GPCRs, ion channels, neuropeptides, neurotransmitter machinery, transcription-factor markers), and cross-neighbour specificity;
- real Allen Mouse CCFv3 50-µm histology and annotation sections;
- the v2.5 bregma-to-CCF conversion is restored: AP/ML/DV index real Allen CCFv3 slices and the corresponding CCF voxel is shown at the crosshair;
- the AP −0.90, ML 2.2–2.3, DV −4.50 mm values remain clearly labeled as Franklin–Paxinos surgical references;
- Page 3 shows eight full-resolution PAG-retrograde sections from bregma −0.70 to −1.40 mm and retains the downloadable PDF;
- synchronized coronal and sagittal crosshairs with AP/ML/DV controls;
- exact Allen structure, structure hierarchy, and nearby annotated regions at the crosshair;
- one two-pixel cyan contour around the exact posterior Allen SI mask; the annotation, structure labels, and coordinate readouts are unchanged;
- Page 2 lists the histological criteria used to assign pSI: bright transmitted light, Nissl/DAPI, caudal GP/internal capsule, optic tract, MeA, CeA/CeM, LH, tracing, and post hoc placement;
- Page 3 is grouped into localization and targeting, input anatomy, and circuit maps;
- Page 3 includes the PAG-retrograde series, high-resolution pSI–PAG targeting images, 2024 Figures 2C and 4O, human SI atlas sections, and the full S8 output and S10 input maps;
- concise cross-species SI links and a reference explaining that the AmgC/M territory substantially overlaps with and is largely the same anatomical territory as pSI;
- the HCN1 single-cell preprint is cited as Li, K., Zhu, Z., et al.;
- ongoing spatial transcriptomics is described as a search for a more selective pSI marker or marker combination;
- shareable coordinate URLs and a self-contained HTML build.

## Development

```bash
npm ci
npm test
npm run typecheck
npm run build
npm run dev -- --host 127.0.0.1
```

## Static deployment

`npm run build` writes the multi-file production site to `dist/`. Deploy the contents of `dist/` to any static host. For GitHub Pages, upload the contents of `dist/` at the repository root and include an empty `.nojekyll` file. The default viewer loads CCFv3 Zarr data from the source configured in `src/lib/ccfData.ts`; set `VITE_CCF_BASE_URL` for self-hosted data.

To create the single-file application shell with all figure images embedded:

```bash
npx vite build --config vite.single.config.ts
node scripts/make-standalone.mjs
```

The HTML shell and figure images are self-contained. Live CCFv3 slices still require internet access unless a local CCF data root is configured.

## Primary sources

- Zhu, Z., Ma, Q., Miao, L., Yang, H., et al. (2021), DOI: 10.1016/j.neuron.2021.03.002
- Zhu, Z., Miao, L., et al. (2024), DOI: 10.1016/j.neuron.2024.06.022
- Li, K., Zhu, Z., et al. (2024), bioRxiv 10.1101/2024.12.07.627305
- Valerie Michael et al. (2020), eLife 63493, AmgC/M–PAG projection-defined targeting and its anatomical overlap with pSI
