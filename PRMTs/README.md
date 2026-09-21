# PRMTs/ — archived builds and source snapshots

This folder is an archive. The **current** site is the build at the repository root
(https://neugun.github.io/pSI-atlas/); see the top-level [README](../README.md) for the
full description, rebuild instructions, and deployment steps.

## Contents

| File | Status |
| --- | --- |
| `pSI-localization-atlas-v2.17.1-source.zip` | **Current editable source.** Matches the build deployed at the repository root. |
| `pSI-localization-atlas-v2.17-source.zip` | Superseded source snapshot |
| `pSI-localization-atlas-v2.16-source.zip` | Superseded source snapshot |
| `pSI-localization-atlas-v2.15-source.zip` | Superseded source snapshot |
| `pSI-localization-atlas-v2.14-source.zip` | Superseded source snapshot |
| `pSI-localization-atlas-v2.14-production.zip` | Superseded production build (v2.14) |
| `index.html`, `assets/` | An earlier build of the site (Locator, tissue-identification, paper anatomy, and references pages only; no gene-expression or neural-firing pages). Still reachable at https://neugun.github.io/pSI-atlas/PRMTs/ but superseded by the root build. |

Each source zip unpacks to a single folder (`pSI-localization-atlas-vX.Y.Z-source/`) containing
`package.json`, `src/`, `scripts/`, `docs/`, and the Vite/TypeScript configuration. No
`node_modules/` or `dist/` are included.

## Rebuilding from a snapshot

```bash
unzip pSI-localization-atlas-v2.17.1-source.zip
cd pSI-localization-atlas-v2.17.1-source
npm ci
npm run build   # output in dist/
```

## Scientific definition (unchanged across versions)

> pSI is the posterior part of Allen substantia innominata (SI) corresponding to the region
> targeted and validated in the experiments (Allen SI id 342, approximately AP −0.7 to −1.6 mm
> from bregma).

The website is a targeting and histology aid; the final site should be checked in tissue.
