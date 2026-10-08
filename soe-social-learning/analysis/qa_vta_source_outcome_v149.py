from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]
s=pd.read_csv(R/"data/SOE_VTA_source_outcome_stepwise_v148.csv")
row=s[s.left=="plus_observation_outcome_interactions"]
assert len(row)==1 and int(row.wins.iloc[0])==7 and int(row.n.iloc[0])==9
assert abs(row.exact_p.iloc[0]-.03125)<1e-9
assert abs(row.mean_delta_mse.iloc[0]-.01368314738855)<1e-8
x=pd.read_csv(R/"data/SOE_VTA_source_outcome_loo_sensitivity_v148.csv")
assert len(x)==9 and abs(x[x.leftout==1].p_exact_two_sided.iloc[0]-.0625)<1e-9
h=pd.read_csv(R/"data/SOE_VTA_source_outcome_halves_v148.csv")
assert len(h)==18 and h.animal.nunique()==9
for name in ["index.html","index-zh.html"]:
 p=R/name;t=p.read_text(encoding="utf-8")
 assert t.count('id="vta-outcome-source-interaction-v148"')==1
 assert t.count('id="vta-source-outcome-plot-v148"')==1
 assert 'BH q≈.0703' in t
 assert '7/9' in t and 'P=.03125' in t and 'P=.0625' in t
 assert 'SOE_VTA_source_outcome_interaction_exploratory_v148.png' in t
 assert t.find('vta-next-choice-goal-test-v134')<t.find('vta-outcome-source-interaction-v148')
for ext in ["png","svg","pdf"]:
 p=R/"assets"/f"SOE_VTA_source_outcome_interaction_exploratory_v148.{ext}"
 assert p.exists() and p.stat().st_size>10000
doc=(R/"docs/VTA_SOURCE_OUTCOME_INTERACTION_EXPLORATORY_v148.md").read_text(encoding="utf8")
assert "OXT intervention and NAc/DMS site/learner analysis stay private" in doc
print("PASS VTA v148: nested held-animal experiment, stepwise source×outcome, BH limit, LOO sensitivity, 2 languages, linked editable charts and privacy boundary")
