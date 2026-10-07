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
    k=s.find('id="vta"'); a=s.rfind("<section",0,k); b=s.find("<section",k+1); sec=s[a:b]
    ck(fn+"_one_vta",s.count('id="vta"')==1)
    order=[
      "SOE_DA_temporal_logic_v67.png",
      "SOE_VTA_early_middle_raw_recon_replication_v102.png",
      "SOE_VTA_codex_exact_replication_v96.png",
      "SOE_FP_social_sampling_specificity_v92.png",
      "SOE_FP_PSTH_biological_story_v82.png",
      "SOE_FP_next_observe_memory_v83.png"]
    pos=[sec.find(x) for x in order]
    ck(fn+"_story_order",all(x>=0 for x in pos) and pos==sorted(pos),pos)
    ck(fn+"_codex_exact_once",sec.count("SOE_VTA_codex_exact_replication_v96.png")==2,sec.count("SOE_VTA_codex_exact_replication_v96.png"))
    ck(fn+"_support_present",all(x in sec for x in ["SOE_FP_PSTH_model_variables_v88.png","SOE_FP_PSTH_event_controls_v90.png","SOE_FP_PSTH_trial_heatmaps_v82.png"]))
    ck(fn+"_clean",all(x not in sec for x in ["???","�","Ã","â€"]))

zh=(R/"index-zh.html").read_text(encoding="utf-8")
k=zh.find('id="vta"'); a=zh.rfind("<section",0,k); b=zh.find("<section",k+1); z=zh[a:b]
ck("zh_why_how_result",z.count("为什么做")>=4 and z.count("怎么做")>=4 and z.count("结论")>=4,(z.count("为什么做"),z.count("怎么做"),z.count("结论")))
ck("zh_smooth_note","轻度高斯平滑" in z and "P 值都使用未平滑数据" in z)
ck("zh_exact_replication_message","SOE_VTA_early_middle_raw_recon_replication_v102.png" in z and "1,041 个有效事件" in z and "1,371 个结果事件" in z)
ck("zh_return_to_slm",z.count("回到 SLM")>=2)
for banned in ["不是","而不是","并不是","不只是"]:
    ck("zh_no_"+banned,banned not in z,z.count(banned))

rep=pd.read_csv(R/"data"/"SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv")
def row(test):
    q=rep[rep.test==test]; return q.iloc[0] if len(q)==1 else None
q=row("q_signed_unsigned")
ck("q_rpe_rep",q is not None and int(q.post_wins)==8 and int(q.bout_wins)==7 and abs(float(q.post_p)-.0078125)<1e-9)
q=row("update_selected_vs_w0p75")
ck("credit075_rep",q is not None and int(q.post_wins)==7 and int(q.bout_wins)==9 and abs(float(q.post_p)-.0390625)<1e-9 and abs(float(q.bout_p)-.00390625)<1e-9)
q=row("update_selected_vs_w1p0")
ck("credit100_rep",q is not None and int(q.post_wins)==6 and int(q.bout_wins)==9 and abs(float(q.post_p)-.0546875)<1e-9 and abs(float(q.bout_p)-.00390625)<1e-9)
q=row("vector_after_scalar")
ck("vector_no_increment",q is not None and float(q.post_effect)<0 and float(q.bout_effect)<0)

mir=pd.read_csv(R/"data"/"SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv")
q=mir[mir.test=="whole_obs_bout_policy"].iloc[0]
ck("whole_bout_policy_boundary",abs(float(q.p)-.4375)<1e-9)
q=mir[mir.test=="whole_obs_bout_APE_x_SRI"].iloc[0]
ck("whole_bout_ape_boundary",abs(float(q.effect)+.119047619)<1e-6 and abs(float(q.p)-.778885726)<1e-6)

M=pd.read_csv(R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv")
for key in ["Q_RPE_signed_abs_both_readouts","Passive_credit_vs_fixed075_both","Vector_after_scalar_both","Whole_observation_bout_policy","Whole_observation_bout_APE_x_SRI"]:
    ck("authority_"+key,(M.test.astype(str)==key).sum()==1)

for asset in [
"SOE_VTA_codex_exact_replication_v96.png","SOE_VTA_codex_exact_replication_v96.pdf","SOE_VTA_codex_exact_replication_v96.svg",
"SOE_FP_PSTH_biological_story_v82.png","SOE_FP_social_sampling_specificity_v92.png","SOE_FP_next_observe_memory_v83.png"]:
    p=R/"assets"/asset
    ck("asset_"+asset,p.exists() and p.stat().st_size>1000,p.stat().st_size if p.exists() else "missing")

doc=(R/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md").read_text(encoding="utf-8")
ck("doc_codex_replication","## 6. Codex FP→DA 读出对原 VTA–SLM 结论的复现" in doc)
ck("doc_psth","## 7A. PSTH 的作用" in doc)
ck("doc_smoothing","统计窗口、逐动物效应和 P 值全部使用未平滑数据" in doc)

print("FAILURES",fails)
sys.exit(1 if fails else 0)
