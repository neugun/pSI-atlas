# Reward-reference results site

This folder is a self-contained static site for the current reward-reference / VTA dopamine biological model.

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

A deployment workflow is provided at `.github/workflows/pages.yml`.

After this repository is connected to the intended GitHub repository:

1. push the committed site files;
2. in GitHub Settings → Pages, select **GitHub Actions** as the Pages source if it is not already selected;
3. run the workflow manually or push a change under `site/`;
4. verify the repository/Page visibility before sharing the URL.

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
