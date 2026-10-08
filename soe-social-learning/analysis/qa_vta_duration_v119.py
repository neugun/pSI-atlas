# -*- coding: utf-8 -*-
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/"data/SOE_VTA_BOUT_DURATION_v118.json").read_text(encoding="utf-8"))
assert d["n_common"]==1371 and d["n_animals"]==9
assert abs(d["duration_s"]["median"]-28.8506808665111)<1e-8
assert abs(d["fraction_bout_gt6"]-.9438366156090445)<1e-8
for f in ["index.html","index-zh.html"]:
 text=(ROOT/f).read_text(encoding="utf-8")
 assert "28.85" in text
 assert "94.4%" in text
 assert "id=\"vta-readout-explained-v116\"" in text
 if f=="index-zh.html":
  assert "固定 0–6 秒记录的是" in text and "早期活动" in text
 else:
  assert "fixed 0–6 s captures an" in text and "early part of the ongoing action" in text
 # Not a post-bout measurement in the usual event.
assert "later evaluation" not in (ROOT/"index.html").read_text(encoding="utf-8")
print("v119 duration QA PASS | n1371, n9, median=28.85s, 94.4% >6s; both languages correct")
