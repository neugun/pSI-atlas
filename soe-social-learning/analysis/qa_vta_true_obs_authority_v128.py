# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd,json,numpy as np
R=Path(__file__).resolve().parents[1]
q=json.loads((R/"data/SOE_VTA_real_obs_interval_audit_v126.json").read_text(encoding="utf-8"))
assert q["n_action_interval"]==1371 and q["n_real_obs"]==821 and q["n_no_observe"]==550
assert abs(q["med_real_obs_s"]-2.39800166527857)<1e-10
assert abs(q["med_extended_s"]-28.8506808665111)<1e-10
assert q["n_obs_ending_before_anchor"]==730 and q["n_obs_ending_after_anchor"]==91
C=pd.read_csv(R/"data/SOE_VTA_true_obs_post_action_credit_comparisons_v126.csv")
expect={
("DA_ActionBout_AUCperSec","update_selected_vs_w0p75"):(8,.0078125),
("DA_ActionBout_AUCperSec","update_selected_vs_w1p0"):(8,.01171875),
("DA_ActionBout_AUCperSec","update_selected_vs_baseline"):(6,.5703125),
("DA_ObsBout_AUCperSec","update_selected_vs_w0p75"):(4,.8203125),
("DA_ObsBout_AUCperSec","update_selected_vs_w1p0"):(3,.8203125),
("DA_ObsBout_AUCperSec","update_selected_vs_baseline"):(2,.0390625),
("DA_Post06_AUCperSec","update_selected_vs_w0p75"):(5,.1640625),
("DA_Post06_AUCperSec","update_selected_vs_w1p0"):(7,.07421875)}
for (key,model),(wins,pval) in expect.items():
 x=C[(C.target==key)&(C.comparison==model)]
 assert len(x)==1 and x.n.iloc[0]==9 and x.wins_selected.iloc[0]==wins and abs(x.p.iloc[0]-pval)<1e-9,(key,model)
for name in ["index.html","index-zh.html"]:
 s=(R/name).read_text(encoding="utf-8")
 assert s.count('id="vta-true-bout-audit-v126"')==1
 assert s.count('id="vta-real-bout-qa-figure-v126"')==1
 assert "550" in s and "821" in s and "2.40" in s and "28.85" in s
 assert "P=.5703" in s and "P=.0078" in s and "P=.8203" in s
 assert "SOE_VTA_true_obs_interval_audit_v126.png" in s
 assert "SOE_VTA_true_obs_post_action_credit_comparisons_v126.csv" in s
 assert "true_bout" not in name
for ext in ["png","svg","pdf"]:
 assert (R/"assets"/("SOE_VTA_true_obs_interval_audit_v126."+ext)).stat().st_size>20000
print("PASS TRUE OBS V128: source n, timing and three-target matched credit contrasts, no-credit baseline, two languages and figure")
