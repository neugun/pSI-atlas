# -*- coding: utf-8 -*-
"""Regression contract: published SOE narrative serves biological question, not DA readout p-chasing."""
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]
story=R/"docs/SOE_GLOBAL_GOAL_EVIDENCE_ACTIONS_20261007.md"
assert story.exists() and story.stat().st_size>5000
s=story.read_text(encoding="utf-8")
for k in ["native Feed","Visual Block","JAWS","OXT","NAc/DMS","Artificial-SLM","no-credit","observation bout"]:
 assert k.lower() in s.lower(), k
m=pd.read_csv(R/"data/SOE_VTA_next_choice_timing_QC_v131.csv")
a=m.set_index("target")
assert int(a.loc["DA_Post06_AUCperSec","n_events"])==1391
assert int(a.loc["DA_ActionBout_AUCperSec","n_events"])==625
assert int(a.loc["DA_Post06_AUCperSec","n_gain"])==5
assert int(a.loc["DA_ActionBout_AUCperSec","n_gain"])==1
assert abs(a.loc["DA_Post06_AUCperSec","p_two_sided"]-.5703125)<1e-9
assert abs(a.loc["DA_ActionBout_AUCperSec","p_two_sided"]-.12890625)<1e-9
b=pd.read_csv(R/"data/SOE_VTA_next_choice_event_overlap_v131.csv").set_index("readout")
assert int(b.loc["fixed_0_6","n_cross_next"])==315
assert int(b.loc["historical_extended","n_cross_next"])==738
for name in ["index.html","index-zh.html"]:
 p=R/name;t=p.read_text(encoding="utf-8")
 assert t.count('id="soe-master-goal-v132"')==1
 assert t.count('id="vta-next-choice-goal-test-v134"')==1
 assert "SOE_GLOBAL_GOAL_EVIDENCE_ACTIONS_20261007.md" in t
 assert "5/9" in t and "1/9" in t and "P=.5703" in t and "P=.1289" in t
 assert "n=625" in t and "n=1,391" in t
 assert "DA is the primary mechanistic display" not in t
 assert "SOE_VTA_next_choice_event_overlap_v131.csv" in t
 assert "SOE_VTA_next_choice_timing_QC_v131.csv" in t
 assert t.index('id="soe-master-goal-v132"') < t.index('id="vta"')
print("GLOBAL SOE STORY + next-choice temporal nonleak evidence: QA PASS")
