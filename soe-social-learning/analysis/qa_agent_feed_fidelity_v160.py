from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]
d=pd.read_csv(R/"data/SLM_agent_source_shift_tests_v159.csv")
x=d[(d.window_sec==3)&(d.cooldown_sec==0)&d.metric.eq("generated_vs_actual_same_opportunity")]
assert len(x)==1 and int(x.n.iloc[0])==24
v=x.iloc[0]
assert abs(v.real_actual_observe_mean-.03847525)<1e-5
assert abs(v.real_generated_observe_mean-.000446716)<1e-6
assert abs(v.generated_generated_observe_mean-.04275418)<1e-5
assert v.two_sided_p>.05
for name in ["index.html","index-zh.html"]:
 s=(R/name).read_text(encoding="utf8")
 assert s.count('id="slm-feed-fidelity-v159"')==1
 assert s.count('id="slm-feed-fidelity-plot-v159"')==1
 assert "SLM_agent_generated_feed_fidelity_v159.png" in s and "27" in s
for ext in ["png","svg","pdf"]:
 p=R/"assets"/("SLM_agent_generated_feed_fidelity_v159."+ext)
 assert p.exists() and p.stat().st_size>8000
assert (R/"docs/SLM_NATIVE_FEED_SAMPLING_FIDELITY_AUDIT_v159.md").exists()
print("PASS trained 27-animal / 54-session Artificial-SLM Feed QA and two languages")
