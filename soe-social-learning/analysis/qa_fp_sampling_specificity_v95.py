# -*- coding: utf-8 -*-
from pathlib import Path
import sys, pandas as pd
R=Path(__file__).resolve().parents[1]
fails=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fails.append(name)

for fn in ["index-zh.html","index.html"]:
    s=(R/fn).read_text(encoding="utf-8")
    for asset in ["SOE_FP_social_sampling_specificity_v92.png","SOE_FP_PSTH_event_controls_v90.png","SOE_FP_PSTH_additional_events_v91.png"]:
        ck(fn+"_"+asset,s.count(asset)==2 if asset=="SOE_FP_social_sampling_specificity_v92.png" else s.count(asset)>=1,s.count(asset))
    ck(fn+"_key_numbers",all(x in s for x in [".0078",".0039"]))
    ck(fn+"_no_mojibake",all(x not in s for x in ["???","�","Ã","â€"]))

zh=(R/"index-zh.html").read_text(encoding="utf-8")
for banned in ["不是","而不是","并不是","不只是"]:
    ck("zh_no_"+banned,banned not in zh,zh.count(banned))
ck("zh_sampling_claim","有效社会信息采样" in zh)
ck("zh_no_raw_observation_bout","真实 observation bout" not in zh)
ck("zh_no_raw_inside_stat","inside P=1.0" not in zh)
ck("zh_no_raw_trigger_terms","示范鼠 triggered" not in zh and "untriggered 事件" not in zh)

S=pd.read_csv(R/"data"/"SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv")
def row(comp,window):
    q=S[(S.comparison==comp)&(S.window==window)]
    return q.iloc[0] if len(q)==1 else None
q=row("observe_inside_vs_random_inside","post_0_6")
ck("inside_vs_random",q is not None and int(q.positive)==8 and abs(float(q.p)-.0078125)<1e-10)
q=row("observe_inside_vs_observe_outside","post_0_2")
ck("inside_vs_outside_fixed",q is not None and int(q.positive)==9 and abs(float(q.p)-.00390625)<1e-10)
q=row("observe_inside_vs_observe_outside","phase_whole")
ck("inside_vs_outside_bout",q is not None and int(q.positive)==8 and abs(float(q.p)-.0078125)<1e-10)
q=row("dem_transition_inside_vs_random_inside","post_0_2")
ck("transition_inside_null",q is not None and abs(float(q.p)-1.0)<1e-10)
q=row("dem_transition_outside_vs_random_outside","post_0_2")
ck("transition_outside_null",q is not None and abs(float(q.p)-.91015625)<1e-10)

C=pd.read_csv(R/"data"/"SOE_FP_EVENT_CONTROL_STATS_v90.csv")
q=C[(C.left=="observer_feeding")&(C.window=="post_0_2")].iloc[0]
ck("feeding_fixed_positive",int(q.positive)==8 and abs(float(q.p)-.01171875)<1e-10)
B=pd.read_csv(R/"data"/"SOE_FP_ADDITIONAL_BOUT_EVENT_STATS_v91.csv")
q=B[(B.left=="observer_feeding")&(B.window=="phase_whole")].iloc[0]
ck("feeding_bout_positive",int(q.positive)==9 and abs(float(q.p)-.00390625)<1e-10)

M=pd.read_csv(R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv")
for key in ["Observe_inside_vs_random_inside_post06","Observe_inside_vs_outside_post02","Observe_inside_vs_outside_whole_bout","Dem_transition_inside_vs_random_post02","Observer_feeding_post_vs_pre","Observer_feeding_whole_bout"]:
    ck("authority_"+key,(M.test.astype(str)==key).sum()==1)

for asset in ["SOE_FP_social_sampling_specificity_v92.png","SOE_FP_social_sampling_specificity_v92.pdf","SOE_FP_social_sampling_specificity_v92.svg",
              "SOE_FP_PSTH_event_controls_v90.png","SOE_FP_PSTH_event_controls_v90.pdf","SOE_FP_PSTH_event_controls_v90.svg",
              "SOE_FP_PSTH_additional_events_v91.png","SOE_FP_PSTH_additional_events_v91.pdf","SOE_FP_PSTH_additional_events_v91.svg"]:
    p=R/"assets"/asset; ck("asset_"+asset,p.exists() and p.stat().st_size>1000,p.stat().st_size if p.exists() else "missing")

doc=(R/"docs"/"SOE_FP_PSTH_BIOLOGICAL_READOUT_v1_20261006.md").read_text(encoding="utf-8")
ck("doc_specificity_section","## 2C. 观察期 VTA 信号属于有效社会信息采样状态" in doc)
ck("doc_control_numbers","P=.00781" in doc and "P=.00391" in doc)

print("FAILURES",fails)
sys.exit(1 if fails else 0)
