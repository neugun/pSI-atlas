# SOE Figure Style V52 — 2026-10-05

This is the plotting authority for the SOE / SLM / SWM working page.

## Physical canvas
- Default manuscript canvas: **3.35 × 3.35 in**.
- Raster export: **600 dpi = 2010 × 2010 px**.
- Desktop and mobile scientific figures are both true square canvases; mobile is a separately rendered layout, not a CSS crop.
- Do not use `bbox_inches="tight"` for manuscript exports because it changes the physical canvas.

## Typography and lines
- Arial throughout.
- Base text: 7 pt; panel letters: 9 pt bold.
- Axis/tick line: 0.75 pt.
- Data lines: about 1.2–1.4 pt.
- No sentence-style titles inside panels. Interpretation and statistics belong in the figure caption.
- No grid. Remove top and right spines.

## Color hierarchy
- Focal SOE / SLM / structured model: **#B2232E**.
- Secondary / comparison state when a second hue is necessary: **#87CDD4**.
- Comparator hierarchy uses three grayscale levels: **#555555 / #999999 / #D7D7D7**.
- Do not introduce extra colors without a scientific encoding need.
- Model-comparison figures should be mostly gray, with the focal model highlighted.

## Categorical spacing
For ordinary categorical bars, use the **2n+1 unit rule**: bar width, inter-bar gaps, and left/right outer gaps use the same base unit. For two bars, the five visual units are therefore approximately equal.

- Bar fill only; no bar outline.
- Mean ± SEM is the default population summary.
- For paired designs, individual observations are represented by the connecting lines; do **not** add redundant point markers.
- Independent-group scatter can retain small, light points when they carry information not shown by a paired line.

## Model comparisons
- Prefer dot/lollipop comparisons when a non-zero axis baseline would make bars misleading.
- Strongest classical / black-box comparators use darker gray; weaker comparators recede.
- The focal structured model is the only red item unless another color is required by the experimental contrast.

## Panel layout
- Prefer square figures even for multipanel layouts.
- Two to four panels should be reflowed within the square canvas rather than stretched into a wide strip.
- Long category labels should wrap or be shortened, never collide.
- Keep outer margins and panel-to-panel gaps compact but sufficient for labels.
- Avoid decorative boxes, filled cards, shadows, and unnecessary layers inside scientific figures.

## Web presentation
- Main evidence figures use the `manuscript-square` class.
- The web container uses a light border, no shadow, compact padding, and tighter caption spacing.
- Current page-level QA requires every displayed main figure and its mobile source to exist locally and every V52 PNG to be 2010 × 2010 at 600 dpi.

## 2026-10-05 conversion
The current English SOE page uses 37 V52 main figure families. All 37 desktop figures and their mobile counterparts passed the V52 geometry/static audit. The Chinese page displays the corresponding V52 versions for all of its main figures.
