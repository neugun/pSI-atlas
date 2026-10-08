from pathlib import Path
import pandas as pd,math
R=Path(__file__).resolve().parents[1]
M=pd.read_csv(R/"data/SOE_SLM_all_behavior_45_models_reaudit_v179.csv")
N=pd.read_csv(R/"data/SOE_SLM_native_Feed_original_OOF_reaudit_v179.csv")
V=pd.read_csv(R/"data/SOE_VTA_v67_P_post_original_exact_reaudit_v179.csv")
C=pd.read_csv(R/"data/SOE_VTA_v67_new_event_count_QC_v179.csv")
assert len(M)==45 and set(M.n)=={68624}
assert abs(float(M.loc[M.model=="SLM full","brier"].iloc[0])-.1708244)<1e-6
assert len(N)==3 and N.n_animals.eq(27).all()
q=N.set_index("model").loc["plus_observed_content"]
assert q.n_improve_vs_recency==21 and abs(q.mean_brier_gain_vs_recency-.000627164)<1e-6
assert abs(q.signedrank_p_vs_recency-.0245397)<1e-4
x=V.set_index("model").loc["beliefSurprise"]
assert x.animals==9 and x.events==1714 and x.n_positive==8
assert abs(x.original_one_sided_exact_signedrank_p-.005859375)<1e-12
assert len(C)==9 and C.n_match.all() and C.old_v67_n.sum()==1714
for f in ["index.html","index-zh.html"]:
 t=(R/f).read_text(encoding="utf8")
 assert t.count('id="slm-legacy-v179"')==1 and t.count('id="slm-legacy-comparison-v179"')==1
 assert "21/27" in t and "8/9" in t and ".00586" in t and ".0245" in t
 assert "SOE_SLM_VTA_LEGACY_CURRENT_RECONCILIATION_v179.md" in t
for ex in ["png","svg","pdf"]:
 asset=R/"assets"/("SOE_SLM_legacy_positive_independent_audit_v179."+ex)
 assert asset.exists() and asset.stat().st_size>10000
doc=(R/"docs/SOE_SLM_VTA_LEGACY_CURRENT_RECONCILIATION_v179.md").read_text(encoding="utf8")
for item in ["future Feed","1,714","100*(base-model)/base","a unique","Belief surprise"]:assert item.lower() in doc.lower(),item
assert "Z:\\" not in doc and "H:\\" not in doc
hazard=pd.read_csv(R/"data/SOE_SLM_native_Feed_hazard_sidedness_v180.csv")
assert len(hazard)==10
for m,one,two in [("feed_rate_delta",.03773978352546692,.07547956705093384),("residual_delta",.04451450705528259,.08902901411056519)]:
 x=hazard[hazard.window.eq("age_le_3s")&hazard.metric.eq(m)].iloc[0]
 assert x.n==26 and x.n_positive==17
 assert abs(x.original_directional_one_sided_exact_p-one)<1e-12
 assert abs(x.independent_two_sided_exact_p-two)<1e-12
print("PASS 3-sec real native Feed hazard: directional and two-sided conventions distinguished")
print("PASS v179/v180: 45 behavior models, 27 animal held-Feed OOF, n26 hazard, 9 animal Post DA exact tests and counts, both pages and figure")
