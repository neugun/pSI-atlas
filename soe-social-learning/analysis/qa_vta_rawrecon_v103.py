# -*- coding: utf-8 -*-
from pathlib import Path
import math
import pandas as pd

R=Path(__file__).resolve().parents[1]
checks=[]

def ok(name,cond,detail=""):
    checks.append((name,bool(cond),detail))
    if not cond:
        raise AssertionError(name+" :: "+detail)

s=pd.read_csv(str(R/"data"/"SOE_VTA_EARLY_MIDDLE_RAW_RECON_SUMMARY_v102.csv"))
get=lambda k: s[s.test.eq(k)].iloc[0]
ok("obs n=1041",int(get("observation_readout_agreement").n_events_or_animals)==1041)
ok("obs animals=9",int(get("observation_readout_agreement").n_animals)==9)
ok("obs agreement",abs(float(get("observation_readout_agreement").estimate)-0.9994126783079704)<1e-9)
ok("early raw p",abs(float(get("early_policy_rawrecon").p)-0.046875)<1e-12)
ok("early rank-biserial",abs(float(get("early_policy_rawrecon").effect_size)-0.8095238095238095)<1e-9)
ok("middle raw rho",abs(float(get("middle_APE_rawrecon").estimate)-2.0/3.0)<1e-6)
ok("middle exact p",abs(float(get("middle_APE_rawrecon").p)-0.041566429404032636)<1e-9)
ok("early rank agreement",abs(float(get("early_gain_rank_agreement").estimate)-1.0)<1e-12)
ok("middle rank agreement",abs(float(get("middle_effect_rank_agreement").estimate)-1.0)<1e-12)

for fn in [
 "assets/SOE_VTA_early_middle_raw_recon_replication_v102.png",
 "assets/SOE_VTA_early_middle_raw_recon_replication_v102_mobile.png",
 "assets/SOE_VTA_early_middle_raw_recon_replication_v102.pdf",
 "assets/SOE_VTA_early_middle_raw_recon_replication_v102.svg",
 "data/SOE_VTA_EARLY_POLICY_RAW_RECON_v102.csv",
 "data/SOE_VTA_MIDDLE_APE_RAW_RECON_v102.csv",
 "data/SOE_VTA_OBSBOUT_RAW_RECON_AUDIT_v102.csv"]:
    ok("exists "+fn,(R/fn).exists())

zh=(R/"index-zh.html").read_text(encoding="utf-8")
en=(R/"index.html").read_text(encoding="utf-8")
doc=(R/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md").read_text(encoding="utf-8")
for name,text in [("zh",zh),("en",en)]:
    ok(name+" v102 figure","SOE_VTA_early_middle_raw_recon_replication_v102.png" in text)
    ok(name+" authority link","SOE_VTA_EARLY_MIDDLE_RAW_RECON_SUMMARY_v102.csv" in text)
    ok(name+" raw reconstruction","raw" in text.lower() and "1,041" in text)
ok("zh whole bout demoted","不再当作复现检验" in zh)
ok("en whole bout demoted","not a replication test" in en)
ok("audit strict replication","保持原分析合同不变" in doc and "P=.041566" in doc)
ok("old zh failure language removed","为什么不能直接用“整个观察片段”替代" not in zh)
ok("old en failure language removed","Why whole-observation-bout averaging cannot replace" not in en)

for n,c,d in checks:
    print(("PASS " if c else "FAIL ")+n+((" :: "+d) if d else ""))
print("TOTAL",len(checks),"PASS")
