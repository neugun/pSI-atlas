from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]
T=pd.read_csv(R/"data/VTA_matched_execpost_stats_v157.csv")
S=pd.read_csv(R/"data/VTA_matched_epoch_robustness_v157.csv")
V=pd.read_csv(R/"data/VTA_matched_epoch_adjusted_v157.csv")
for lab,positives,p in [("active_minus_unrewarded",9,.00390625),("passive_minus_unrewarded",8,.0078125)]:
 q=T[(T.gap.eq(.5))&(T.target.eq("post_minus_exec"))&(T.contrast.eq(lab))]
 assert len(q)==1 and q.n_animals.iloc[0]==9 and q.positive.iloc[0]==positives and abs(q.p_two_sided.iloc[0]-p)<1e-10
assert len(V)==18 and V.animal.nunique()==9
assert abs(S[(S.spec=="primary")&(S.contrast=="active-unrewarded")].p_two_sided.iloc[0]-.00390625)<1e-10
for f in ["index.html","index-zh.html"]:
 s=(R/f).read_text(encoding="utf8")
 assert s.count('id="vta-matched-execution-outcome-v157"')==1
 assert s.count('id="vta-matched-execution-outcome-figure-v157"')==1
 assert "695" in s and ".00391" in s and ".00781" in s
 assert "VTA_matched_observation_vs_outcome_epoch_v157.png" in s
for ext in ["png","pdf","svg"]:
 q=R/"assets"/("VTA_matched_observation_vs_outcome_epoch_v157."+ext)
 assert q.exists() and q.stat().st_size>8000
assert (R/"docs/VTA_REAL_BOUT_TO_OUTCOME_EPOCH_AUDIT_v157.md").exists()
print("PASS matched execution / post-outcome true bout VTA v157; n695 nine animals, exact paired tests, sensitivity and both languages")
