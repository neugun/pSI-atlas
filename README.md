# pSI Localization Atlas

A reference site for posterior substantia innominata (pSI) in the mouse brain: where it is, how to find it in tissue, what its circuits look like, and what's known about its gene expression and firing.

> pSI is the posterior part of Allen substantia innominata (SI), corresponding to the region targeted and validated in our experiments (Allen SI id 342, AP −0.7 to −1.6 mm from bregma).

## Pages

**CCFv3 Locator.** An interactive Allen Mouse CCFv3 viewer (50 µm resolution). Enter an AP/ML/DV coordinate or a Franklin–Paxinos surgical reference and see the matching coronal and sagittal slices, with the corresponding CCF voxel, structure name, and nearby annotated regions read out at the crosshair. Coordinates are shareable as URLs.

**Locating pSI.** The histological criteria used to identify pSI under the microscope: transmitted light, Nissl/DAPI landmarks, and the surrounding structures (caudal GP, internal capsule, optic tract, MeA, CeA/CeM, LH) that place it in a section.

**Anatomy & circuits.** Figures from the underlying papers, organized into localization/targeting, input anatomy, and circuit maps — including the PAG-retrograde series and the high-resolution pSI–PAG targeting images.

**Gene expression & spatial profile.** MERFISH spatial transcriptomics and Allen ABC (WMB-10Xv3) single-cell RNA-seq for pSI, compared against its five nearest anatomical neighbours (CEAl, CEAm, GPe, GPi, MEA) and anterior SI. Covers cell-type composition, differential expression by functional gene category, and cross-neighbour marker specificity, at both the MERFISH panel and full-transcriptome level.

**Neural firing (Neuropixels).** How pSI units fire around behavioural events (cue, action, reward vs. omission), using public IBL Brain-Wide Map recordings, compared against the same five neighbours. Includes the prior in vivo tetrode data this analysis builds on, where the recorded units are located anatomically, and a population-level response-manifold analysis (PCA over each unit's event-aligned firing) asking whether pSI occupies a distinguishable region of response state-space.

**References & other species.** Source papers, cross-species SI links, and background on regions (e.g. AmgC/M) that overlap anatomically with pSI.

## Development

```bash
npm ci
npm test
npm run typecheck
npm run build
npm run dev -- --host 127.0.0.1
```

## Static deployment

`npm run build` writes the production site to `dist/`. Deploy the contents of `dist/` to any static host. For GitHub Pages, upload the contents of `dist/` at the repository root and include an empty `.nojekyll` file. The Locator loads CCFv3 Zarr data from the source configured in `src/lib/ccfData.ts`; set `VITE_CCF_BASE_URL` to point at self-hosted data instead.

To build a single-file version with all figures embedded:

```bash
npx vite build --config vite.single.config.ts
node scripts/make-standalone.mjs
```

The resulting HTML is self-contained; only the live CCFv3 slices in the Locator still need network access, unless a local CCF data root is configured.

## Primary sources

- Zhu, Z., Ma, Q., Miao, L., Yang, H., et al. (2021), DOI: 10.1016/j.neuron.2021.03.002
- Zhu, Z., Miao, L., et al. (2024), DOI: 10.1016/j.neuron.2024.06.022
- Li, K., Zhu, Z., et al. (2024), bioRxiv 10.1101/2024.12.07.627305
- Michael, V., et al. (2020), eLife 63493 — AmgC/M–PAG projection-defined targeting and its anatomical overlap with pSI
