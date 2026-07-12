# pSI Localization Atlas

An interactive Allen Mouse CCFv3 reference for localizing posterior substantia innominata (pSI), checking the site in tissue, and reviewing the main anatomy/circuit figures from the 2021 and 2024 studies.

## Scientific definition

> pSI is the posterior part of Allen substantia innominata (SI) corresponding to the region targeted and validated in the experiments.

The pSI overlay is the Allen CCFv3 SI mask within approximately AP −0.7 to −1.6 mm from bregma. The website is a targeting and histology aid; the final site should be checked in tissue.

## Version 2.8

- real Allen Mouse CCFv3 50-µm histology and annotation sections;
- synchronized coronal and sagittal crosshairs with AP/ML/DV controls;
- exact Allen structure, structure hierarchy, and nearby annotated regions at the crosshair;
- cyan posterior-SI overlay that remains visible over red hypothalamic annotation colors;
- Page 2 is a practical tissue-identification workflow using bright transmitted light, Nissl/DAPI, caudal GP/internal capsule, optic tract, MeA, CeA/CeM, LH, tracing, and post hoc placement;
- a paper anatomy/circuit page grouped into localization, inputs, outputs/pathway tests, and atlas context;
- supplied panels from 2021 Figures 1D, 4D–E, 7B, the full S8 output map and S10 input map; 2024 Figures 2C and 4O; and a Franklin–Paxinos/Allen coordinate crosswalk;
- concise cross-species SI links and a reference explaining that the AmgC/M territory substantially overlaps with and is largely the same anatomical territory as pSI;
- shareable coordinate URLs and website https://neugun.github.io/pSI-atlas/.

## Development

```bash
npm ci
npm test
npm run typecheck
npm run build
npm run dev -- --host 127.0.0.1
```

## Static deployment

`npm run build` writes the multi-file production site to `dist/`. Deploy the contents of `dist/` to any static host. The default viewer loads CCFv3 Zarr data from the source configured in `src/lib/ccfData.ts`; set `VITE_CCF_BASE_URL` for self-hosted data.

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
