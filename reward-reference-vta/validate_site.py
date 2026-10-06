from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
import struct

ROOT = Path(__file__).resolve().parent
PAGES = [ROOT / "index.html", ROOT / "zh" / "index.html"]

class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
        self.anchor_refs = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        for key in ("src", "href"):
            if key not in d:
                continue
            value = d[key]
            if value.startswith("#"):
                self.anchor_refs.append(value[1:])
            else:
                self.refs.append((tag, key, value))

def local_target(page, ref):
    u = urlparse(ref)
    if u.scheme in ("http", "https", "mailto"):
        return None
    return (page.parent / u.path).resolve()

def png_size(path):
    head = path.read_bytes()[:24]
    assert head[:8] == b"\x89PNG\r\n\x1a\n", f"Not PNG: {path}"
    return struct.unpack(">II", head[16:24])

all_missing = []
all_missing_anchors = []
external_count = 0
local_count = 0

for page in PAGES:
    parser = Collector()
    text = page.read_text(encoding="utf-8")
    parser.feed(text)
    missing = []
    external = []
    local = []
    for tag, key, ref in parser.refs:
        target = local_target(page, ref)
        if target is None:
            external.append(ref)
            continue
        local.append((ref, target))
        if not target.exists():
            missing.append((ref, str(target)))
    missing_anchors = sorted(set(parser.anchor_refs) - parser.ids)
    all_missing.extend((page.name, *x) for x in missing)
    all_missing_anchors.extend((page.name, x) for x in missing_anchors)
    external_count += len(external)
    local_count += len(local)
    print(f"{page.relative_to(ROOT)}: bytes={page.stat().st_size} local={len(local)} external={len(external)} ids={len(parser.ids)}")
    print(f"  missing_local={len(missing)} missing_anchors={len(missing_anchors)}")

assert not all_missing, f"Broken local links: {all_missing[:10]}"
assert not all_missing_anchors, f"Broken page anchors: {all_missing_anchors[:10]}"
print("SITE_LINK_QA=PASS")

# Strict figure contract: every manuscript panel is a square source image,
# both language pages expose the same 19 figure containers, and legacy
# crop-based strict_v52/v53 assets are not referenced.
panel_paths = set()
for page in PAGES:
    text = page.read_text(encoding="utf-8")
    n_fig = len(re.findall(r'<figure[^>]*class="[^"]*strict-panels[^"]*"', text))
    srcs = re.findall(r'<img[^>]+src="([^"]+)"[^>]*>', text)
    strict_srcs = [s for s in srcs if "true_square_v5" in s]
    legacy = [s for s in srcs if "strict_v52" in s or "strict_v53" in s]
    assert n_fig == 19, f"{page}: expected 19 strict figure containers, got {n_fig}"
    assert len(strict_srcs) == 72, f"{page}: expected 72 strict panel references, got {len(strict_srcs)}"
    assert not legacy, f"{page}: legacy strict panels still referenced: {legacy[:5]}"
    for ref in strict_srcs:
        target = local_target(page, ref)
        assert target and target.exists(), f"Missing strict panel: {page} -> {ref}"
        w, h = png_size(target)
        assert w == h, f"Non-square source panel: {target.name} {w}x{h}"
        panel_paths.add(target)
    print(f"{page.relative_to(ROOT)}: strict_figures={n_fig} strict_panel_refs={len(strict_srcs)}")

style = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
for token in ("aspect-ratio: 1 / 1", "object-fit: contain", "@media (max-width: 620px)"):
    assert token in style, f"Missing strict-panel CSS contract: {token}"
print(f"FIGURE_GEOMETRY_QA=PASS unique_panels={len(panel_paths)}")

# On workstations with Pillow, also reject visible content that touches the
# outer 20 px safety zone. CI can run without Pillow and still enforce geometry.
try:
    from PIL import Image
    import numpy as np
except Exception:
    print("FIGURE_EDGE_QA=SKIP (Pillow unavailable)")
else:
    bad_edges = []
    for path in sorted(panel_paths):
        im = Image.open(path).convert("RGB")
        arr = np.asarray(im)
        nonwhite = np.any(arr < 245, axis=2)
        if not nonwhite.any():
            continue
        ys, xs = np.where(nonwhite)
        margins = (
            int(xs.min()),
            int(im.width - 1 - xs.max()),
            int(ys.min()),
            int(im.height - 1 - ys.max()),
        )
        if min(margins) < 20:
            bad_edges.append((path.name, margins))
    assert not bad_edges, f"Panel content too close to edge: {bad_edges[:10]}"
    print(f"FIGURE_EDGE_QA=PASS panels={len(panel_paths)} min_margin_px>=20")
