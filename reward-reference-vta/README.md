# Reward-reference results site

Live page: **https://neugun.github.io/pSI-atlas/reward-reference-vta/**

This folder is a self-contained static site for the current reward-reference / VTA dopamine biological model. Production publishing uses the already-enabled `neugun/pSI-atlas` GitHub Pages host under the isolated `reward-reference-vta/` subdirectory.

## Local preview

Open `index.html` directly in a browser. All scientific figures, evidence tables and authority notes used by the page are copied into this folder with relative links.

## Scientific authority

The page is organized around the 2026-10-04 mechanistic authority:

- internal state H changes current utility U;
- experienced reward samples update a history reference R;
- current utility is evaluated relative to R;
- comparator gain is context dependent;
- neural and behavioral expression can dissociate.

The page intentionally does **not** claim:
- alpha=.20 is a universal biological constant;
- all physiological reward manipulations alter reference formation;
- VTA population dopamine lacks negative-RPE neurons;
- sustained 2–5 s GRAB-DA is identical to canonical subsecond TD-RPE;
- positive comparator gain universally dominates negative comparator gain;
- dopamine fully mediates the behavioral contrast effect.

## GitHub Pages

Production is hosted inside the already-enabled public Pages repository `neugun/pSI-atlas` at the isolated subdirectory `reward-reference-vta/`.

For future updates, run from the analysis repository:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/publish_reward_reference_pages.ps1
```

The publisher validates the source site, fast-forwards the Pages host, refuses to continue when unrelated files are dirty, mirrors only `site/` into `reward-reference-vta/`, validates again, commits only that subdirectory, and pushes `main`.

Because this project contains prepublication work, the site includes:
- `<meta name="robots" content="noindex,nofollow,noarchive">`;
- `robots.txt` with `Disallow: /`.

These reduce indexing but are **not an access-control mechanism**. Repository/Page visibility must still be configured appropriately.

## QA

Run:

```bash
python site/validate_site.py
```

The validator checks local figures, data links and page anchors.
