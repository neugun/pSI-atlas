# -*- coding: utf-8 -*-
from pathlib import Path
import sys, pandas as pd

R=Path(__file__).resolve().parents[1]
fail=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fail.append(name)

for fn in ["index-zh.html","index.html"]:
    s=(R/fn).read_text(encoding="utf-8")
    ck(fn+"_bio_main",s.count("SOE_FP_PSTH_biological_story_v82.png")==2)
    ck(fn+"_obs_context",s.count("SOE_FP_PSTH_observation_context_v82.png")==2)
    ck(fn+"_heatmap",s.count("SOE_FP_PSTH_trial_heatmaps_v82.png")==2)
    ck(fn+"_next_memory",s.count("SOE_FP_next_observe_memory_v83.png")==2)
    ck(fn+"_vta_block",s.count('id="vta-psth-biological-v84"')==1)
    ck(fn+"_support_details",s.count('id="vta-psth-support-v82"')==1)
    ck(fn+"_key_pvals",all(x in s for x in ["P=0.027","P=0.020","P=0.008"]))
    ck(fn+"_outcome_readout_figure",s.count("SOE_FP_DA_outcome_contrasts_v85.png")==2)
    ck(fn+"_event_selection_figure",s.count("SOE_FP_PSTH_event_selection_v86.png")==2)
    ck(fn+"_model_psth_figure",s.count("SOE_FP_PSTH_model_variables_v88.png")==2)
    ck(fn+"_model_psth_source","SOE_FP_PSTH_MODEL_VARIABLES_v88.csv" in s)
    ck(fn+"_clean",all(x not in s for x in ["???","�","Ã","â€"]))

zh=(R/"index-zh.html").read_text(encoding="utf-8")
for bad in ["不是","而不是","并不是","不只是"]:
    ck("zh_no_"+bad,bad not in zh,zh.count(bad))

stats=pd.read_csv(R/"data"/"SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv")
ck("stats_rows",len(stats)==12,len(stats))
def pval(w,l,r):
    q=stats[(stats.window==w)&(stats.left==l)&(stats.right==r)]
    return None if len(q)!=1 else float(q.iloc[0].p)
ck("pre_active",abs(pval("pre_-1_0","active","unrewarded")-0.02734375)<1e-12)
ck("pre_passive",abs(pval("pre_-1_0","passive","unrewarded")-0.01953125)<1e-12)
ck("pre_passive_gt_active",abs(pval("pre_-1_0","active","passive")-0.02734375)<1e-12)
ck("post_active",abs(pval("post_0_2","active","unrewarded")-0.0078125)<1e-12)
ck("post_passive",abs(pval("post_0_2","passive","unrewarded")-0.0078125)<1e-12)
ck("phase_active",abs(pval("phase_0_25","active","unrewarded")-0.00390625)<1e-12)
ck("phase_passive",abs(pval("phase_0_25","passive","unrewarded")-0.00390625)<1e-12)

curves=pd.read_csv(R/"data"/"SOE_FP_PSTH_ANIMAL_CURVES_v82.csv")
ck("curve_analyses",set(curves.analysis)=={"outcome_fixed","outcome_bout_phase","next_observe_fixed","next_observe_bout_phase"},sorted(curves.analysis.unique()))
ck("curve_animals",curves.AnmID.nunique()==9,curves.AnmID.nunique())

for f in [
"SOE_FP_PSTH_biological_story_v82.png","SOE_FP_PSTH_biological_story_v82.pdf","SOE_FP_PSTH_biological_story_v82.svg","SOE_FP_PSTH_biological_story_v82_mobile.png",
"SOE_FP_PSTH_observation_context_v82.png","SOE_FP_PSTH_trial_heatmaps_v82.png",
"SOE_FP_DA_outcome_contrasts_v85.png","SOE_FP_DA_outcome_contrasts_v85.pdf","SOE_FP_DA_outcome_contrasts_v85.svg","SOE_FP_DA_outcome_contrasts_v85_mobile.png",
"SOE_FP_PSTH_event_selection_v86.png","SOE_FP_PSTH_event_selection_v86.pdf","SOE_FP_PSTH_event_selection_v86.svg",
"SOE_FP_next_observe_memory_v83.png","SOE_FP_next_observe_memory_v83.pdf","SOE_FP_next_observe_memory_v83.svg","SOE_FP_next_observe_memory_v83_mobile.png",
"SOE_FP_PSTH_model_variables_v88.png","SOE_FP_PSTH_model_variables_v88.pdf","SOE_FP_PSTH_model_variables_v88.svg","SOE_FP_PSTH_model_variables_v88_mobile.png"]:
    p=R/"assets"/f
    ck("asset_"+f,p.exists() and p.stat().st_size>1000,p.stat().st_size if p.exists() else "missing")

main=pd.read_csv(R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv")
for key in [
"next_observe_pre_active_vs_unrewarded","next_observe_pre_passive_vs_unrewarded",
"next_observe_post_active_vs_unrewarded","next_observe_post_passive_vs_unrewarded",
"next_observe_phase25_active_vs_unrewarded","next_observe_phase25_passive_vs_unrewarded"]:
    ck("authority_"+key,(main.test.astype(str)==key).sum()==1)

doc=(R/"docs"/"SOE_FP_PSTH_BIOLOGICAL_READOUT_v1_20261006.md").read_text(encoding="utf-8")
ck("doc_state","上一次结果会延续到下一次观察" in doc)
ck("doc_boundary","条件化在“已经发生重新观察”" in doc)
ck("doc_readout_effect","主动成功 − 未奖赏" in doc and "P=.0273" in doc)

counts=pd.read_csv(R/"data"/"SOE_FP_PSTH_EVENT_COUNTS_v82.csv")
def nev(scope,event):
    q=counts[(counts.scope==scope)&(counts.event_type==event)]
    return None if len(q)!=1 else int(q.iloc[0].n_events)
ck("all_event_counts",(nev("all","active"),nev("all","passive"),nev("all","unrewarded"))==(442,420,861))
ck("common_event_counts",(nev("common","active"),nev("common","passive"),nev("common","unrewarded"))==(259,257,855))
nextobs=pd.read_csv(R/"data"/"SOE_FP_NEXT_OBSERVE_AFTER_OUTCOME_v82.csv")
vc=nextobs.previous_outcome.value_counts().to_dict()
ck("next_observe_counts",(vc.get("active"),vc.get("passive"),vc.get("unrewarded"))==(327,298,665),vc)

oc=pd.read_csv(R/"data"/"SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv")
def op(scope,left,right):
    q=oc[(oc.comparison_scope==scope)&(oc.left==left)&(oc.right==right)]
    return None if len(q)!=1 else float(q.iloc[0].p)
ck("active_unrewarded_direct",abs(op("fixed_minus_bout","active","unrewarded")-0.02734375)<1e-12)
ck("passive_unrewarded_bout",abs(op("bout_duration","passive","unrewarded")-0.01953125)<1e-12)
ck("passive_active_bout",abs(op("bout_duration","passive","active")-0.0390625)<1e-12)
for key in ["Active_vs_Unrewarded_fixed_minus_bout","Passive_vs_Unrewarded_actual_bout","Passive_vs_Active_actual_bout"]:
    ck("authority_"+key,(main.test.astype(str)==key).sum()==1)

print("FAILURES",fail)
sys.exit(1 if fail else 0)

modelsrc=R/"data"/"SOE_FP_PSTH_MODEL_VARIABLES_v88.csv"
ck("model_psth_source_exists",modelsrc.exists() and modelsrc.stat().st_size>1000,modelsrc.stat().st_size if modelsrc.exists() else "missing")
