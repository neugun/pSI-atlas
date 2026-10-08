from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]
X=pd.read_csv(R/"data/SOE_OXT_SF15_new_animal_opto_audit_v166.csv")
T=pd.read_csv(R/"data/SOE_OXT_SF15_new_opto_tests_v166.csv")
P=pd.read_csv(R/"data/SOE_OXT_SF15_pseudoday_provenance_v166.csv")
assert X.animal.nunique()==6 and set(X.animal)=={173,174,179,180,184,305}
assert X.groupby("animal").size().eq(2).all() and X.optostim_state.eq("NOT_HARDWARE_VERIFIED").all()
assert set(X[X.animal.ne(305)].cohort)=={"OXT_NAc_PVH"} and X[X.animal.eq(305)].cohort.eq("VTA-JAWS-other").all()
n=T[(T.scope=="ALL_NAc_provisional")&(T.readout=="Active/SRI")&(T.metric=="FeedOB_ratio_index")]
assert len(n)==1 and int(n.n.iloc[0])==5 and int(n.negative.iloc[0])==4 and abs(n.exact_two_sided_p.iloc[0]-.375)<1e-9
q=T[(T.scope=="filename_clean_only")&(T.readout=="Active/SRI")&(T.metric=="FeedOB_ratio_index")]
assert len(q)==1 and int(q.n.iloc[0])==3 and int(q.negative.iloc[0])==3 and abs(q.exact_two_sided_p.iloc[0]-.25)<1e-9
assert set(X[X.provenance=="CLEAN_FILENAME"].animal)=={173,179,180}
assert X[X.animal.eq(174)].provenance.eq("MIXED_173_IN_EVEN_FOLDER").all()
assert X[X.animal.eq(184)].provenance.eq("SOURCE_RIG_ID_180_FOR_184").all()
assert P.n_evt_segments.sum()==195 and P.folder_day.nunique()==12
assert P[P.folder_day.eq(42)].source_animal.nunique()==2
assert set(P[P.folder_day.isin([45,46])].source_animal)=={180}
for name in ["index.html","index-zh.html"]:
 s=(R/name).read_text(encoding="utf8")
 assert s.count('id="oxt-expanded"')==1 and s.count('href="#oxt-expanded"')==1
 assert s.count('id="oxt-new-sf15-figure-v166"')==1
 assert "SRI" in s and ".375" in s and ".25" in s and "305" in s
 assert "OXT_SF15_recent_opto_provenance_v166.png" in s
 assert "NOT_HARDWARE_VERIFIED" not in s or "hardware" in s.lower()
for ext in ["png","svg","pdf"]:
 f=R/"assets"/("OXT_SF15_recent_opto_provenance_v166."+ext)
 assert f.exists() and f.stat().st_size>5000
for f in [R/"docs/OXT_SF15_EXPANDED_STIM_PROVENANCE_v166.md",R/"data/SOE_OXT_SF15_pseudoday_provenance_v166.csv"]:
 assert f.exists()
 assert "Z:\\" not in f.read_text(encoding="utf8")
D=pd.read_csv(R/"data/SOE_OXT_SF15_D1_22_training_index_v172.csv")
H=pd.read_csv(R/"data/SOE_OXT_SF15_training_comparisons_v172.csv")
assert D.animal.nunique()==6 and len(D)==6*22*2*2
assert D[D.animal.eq(305)].cohort.eq("VTA_JAWS_separate").all()
assert H.n_shuffles_field.eq(100).all()
for readout,change,positive,pval in [("Active/SRI",.8899,4,.125),("Passive/PRI",-.9098,1,.125)]:
 t=H[H.cohort.eq("NAc_5")&H.readout.eq(readout)&H.metric.eq("FeedOB_ratio_index")&H.comparison.eq("D1_3_to_D15_20")]
 assert len(t)==1 and t.n.iloc[0]==5 and t.n_increase.iloc[0]==positive
 assert abs(t.change.iloc[0]-change)<.001 and abs(t.exact_two_sided_p.iloc[0]-pval)<1e-9
for name in ["index.html","index-zh.html"]:
 s=(R/name).read_text(encoding="utf8")
 assert s.count('id="oxt-sf15-training-v173"')==1 and s.count('id="oxt-sf15-training-fig-v173"')==1
 assert "OXT_SF15_training_SRI_PRI_v173.png" in s
for ext in ["png","pdf","svg"]:
 img=R/"assets"/("OXT_SF15_training_SRI_PRI_v173."+ext)
 assert img.exists() and img.stat().st_size>20000
print("PASS SF15 original MAT n6; NAc n5; D1-22 training 100 actual shuffles; virtual stimulation/rig provenance; laser-state flags; 2 languages")
