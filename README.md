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

## Live site

The site is published with GitHub Pages from the `main` branch of this repository:

- **Current site:** https://neugun.github.io/pSI-atlas/ (production build of **v2.17.1**)
- Archived earlier build: https://neugun.github.io/pSI-atlas/PRMTs/ (see [Repository layout](#repository-layout))

## Repository layout

This repository holds the *built* site, not the editable source tree. The source is archived as zip files.

| Path | What it is |
| --- | --- |
| `index.html`, `assets/` | Production build (Vite output) of the current release, **v2.17.1**. This is what https://neugun.github.io/pSI-atlas/ serves. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is (no Jekyll processing). |
| `PRMTs/pSI-localization-atlas-v2.17.1-source.zip` | **Current editable source** (React + TypeScript + Vite). Use this to rebuild or extend the site. |
| `PRMTs/pSI-localization-atlas-v2.14-source.zip` … `v2.17-source.zip` | Older source snapshots, kept for reference only. |
| `PRMTs/pSI-localization-atlas-v2.14-production.zip` | Older production build (v2.14), kept for reference only. |
| `PRMTs/index.html`, `PRMTs/assets/` | An earlier build of the site (before the gene-expression and neural-firing pages were added). Superseded by the root build. |
| `pSI_Localization_Atlas_Rebuild_Specification.docx` | Specification and reusable prompts describing the scientific requirements, page structure, and validation checks used to build the site. |

### Version history

| Version | Change |
| --- | --- |
| v2.17.1 (current) | Reordered neural page, expanded tetrode context, fixed undersized figures, rewrote README |
| v2.17 | Manifold analysis, probe-location diagram, tetrode context, navigation renames |
| v2.16 | Neural firing (Neuropixels) page; refreshed gene-expression page |
| v2.15 | Gene expression & spatial profile page |
| v2.14 | Baseline of the archived source/production zips |

## Rebuilding from source

The source zip contains `package.json`, `package-lock.json`, `src/`, `scripts/`, and `docs/` (no `node_modules/`, no `dist/`). Node.js 18+ and npm are required.

```bash
unzip PRMTs/pSI-localization-atlas-v2.17.1-source.zip
cd pSI-localization-atlas-v2.17.1-source
npm ci
npm test
npm run typecheck
npm run build            # writes the production site to dist/
npm run dev -- --host 127.0.0.1   # local dev server
```

`vite.config.ts` uses `base: './'`, so the build works both at the repository root of a GitHub Pages project site and in any subfolder.

To build a single-file version with all figures embedded:

```bash
npx vite build --config vite.single.config.ts
node scripts/make-standalone.mjs
```

The resulting HTML is self-contained; only the live CCFv3 slices in the Locator still need network access, unless a local CCF data root is configured.

## Deploying to GitHub Pages

GitHub Pages is configured to serve the **root of the `main` branch**. To publish a new build:

1. Run `npm run build` in the unzipped source tree.
2. Replace `index.html` and the `assets/` directory at the root of this repository with the contents of `dist/`. Keep `.nojekyll`.
3. Add the new source snapshot as `PRMTs/pSI-localization-atlas-vX.Y.Z-source.zip` and update the version table above.
4. Commit and push to `main`; Pages redeploys automatically within a few minutes.

The Locator loads Allen CCFv3 Zarr data from the source configured in `src/lib/ccfData.ts` (by default the public `thewtex/allen-ccf-itk-vtk-zarr` mirror; see `docs/DATA_SOURCES.md` in the source zip). Set `VITE_CCF_BASE_URL` at build time to point at self-hosted data instead.

## Primary sources

- Zhu, Z., Ma, Q., Miao, L., Yang, H., et al. (2021), DOI: 10.1016/j.neuron.2021.03.002
- Zhu, Z., Miao, L., et al. (2024), DOI: 10.1016/j.neuron.2024.06.022
- Li, K., Zhu, Z., et al. (2024), bioRxiv 10.1101/2024.12.07.627305
- Michael, V., et al. (2020), eLife 63493 — AmgC/M–PAG projection-defined targeting and its anatomical overlap with pSI

## License

No license has been specified for this repository yet. Until one is added, the code and site content are "all rights reserved" by default; figure panels reproduced from the primary sources remain subject to their publishers' terms.
