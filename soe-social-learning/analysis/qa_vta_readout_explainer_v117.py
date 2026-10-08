from pathlib import Path
import json,os,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
x=pd.read_csv(ROOT/"data/SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv").set_index("test")
m=ROOT/"data/SOE_VTA_READOUT_CONTRACT_v116.json"
assert m.exists(),"The frozen common-event contract was not committed"
meta=json.loads(m.read_text(encoding="utf-8"))
source=Path(os.environ["SOE_VTA_SOURCE_MANIFEST"]) if os.environ.get("SOE_VTA_SOURCE_MANIFEST") else None
if source is not None and source.exists():
 original=json.loads(source.read_text(encoding="utf-8"))
 for k in ("n_common","n_animals","rule"):
  assert meta[k]==original[k],f"External source contract drift: {k}"
assert meta["n_common"]==1371 and meta["n_animals"]==9
assert "ActionBoutDur_FP>=0.05 s" in meta["rule"]
expect={
"update_selected_vs_w0p75":(9,.00390625,7,.0390625),
"update_selected_vs_w1p0":(9,.00390625,6,.0546875),
"actor_rpe_abs":(6,.359375,9,.00390625)}
for name,(boutwins,boutp,fixedwins,fixedp) in expect.items():
 q=x.loc[name]
 assert q.bout_wins==boutwins and abs(q.bout_p-boutp)<1e-9
 assert q.post_wins==fixedwins and abs(q.post_p-fixedp)<1e-9
for file,key in (("index.html","Why are there two DA readouts from the same neural recordings?"),("index-zh.html","同一批多巴胺信号，为什么取两个窗口？")):
 s=(ROOT/file).read_text(encoding="utf-8")
 assert s.count('id="vta-readout-explained-v116"')==1
 assert key in s
 # Explanation must precede Post-stage readout section and explicitly delimit inference.
 assert s.find('id="vta-readout-explained-v116"')<s.find("Post-stage mechanistic readout" if file=="index.html" else "结果期主机制读出",s.find('id="vta-readout-explained-v116"'))
 if file=="index.html":
  assert "post-bout-only period for the typical long event" in s
 else:
  assert "现有两种方法对绝大多数长事件都没有直接测量" in s
 assert "1,371" in s and ("0–6" in s or "0-6" in s)
print("READOUT EXPLAINER v117: PASS | 1371 same events, n=9, bout>=0.05; 3 tests, two languages, no isolated-phase overclaim")
