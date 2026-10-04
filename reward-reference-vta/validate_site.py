from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"

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

p = Collector()
text = HTML.read_text(encoding="utf-8")
p.feed(text)

missing = []
external = []
local = []
for tag, key, ref in p.refs:
    u = urlparse(ref)
    if u.scheme in ("http", "https", "mailto"):
        external.append(ref)
        continue
    target = (ROOT / u.path).resolve()
    local.append((ref, target))
    if not target.exists():
        missing.append((ref, str(target)))

missing_anchors = sorted(set(p.anchor_refs) - p.ids)

print(f"HTML bytes: {HTML.stat().st_size}")
print(f"Local refs: {len(local)}")
print(f"External refs: {len(external)}")
print(f"IDs: {len(p.ids)}")
print(f"Missing local refs: {len(missing)}")
for x in missing:
    print("MISSING", x)
print(f"Missing anchors: {len(missing_anchors)}")
for x in missing_anchors:
    print("MISSING_ANCHOR", x)

assert not missing, "Broken local links"
assert not missing_anchors, "Broken page anchors"
print("SITE_LINK_QA=PASS")
