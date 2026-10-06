from pathlib import Path
from html.parser import HTMLParser
import csv, re, sys

R=Path(__file__).resolve().parents[1]
fails=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond:fails.append(name)

for fn in ["index-zh.html","index.html"]:
    s=(R/fn).read_text(encoding="utf-8")
    HTMLParser().feed(s)
    ck(fn+"_slm_bridge_once",s.count('id="slm-learning-axis-bridge-v75"')==1,s.count('id="slm-learning-axis-bridge-v75"'))
    ck(fn+"_vta_multiaxis_once",s.count('id="vta-multiaxis-v75"')==1,s.count('id="vta-multiaxis-v75"'))
    ck(fn+"_codex_legacy_once",s.count('id="vta-codex-legacy-v75"')==1,s.count('id="vta-codex-legacy-v75"'))
    ck(fn+"_fast_switch_training",".041" in s and "4.3" in s and "10.8" in s)
    ck(fn+"_reentry_effects","9.0" in s and "8.3" in s)
    ck(fn+"_dual_behavior",".1911" in s and ".2273" in s and "4.92×10⁻⁷" in s)
    ck(fn+"_temporal_3axes","P=.0469" in s and "P=.0416" in s and "P=.0195" in s)
    ck(fn+"_scalar_vector",".01518" in s and ".00544" in s and ".00871" in s and "−.00035" in s)
    ck(fn+"_credit_transfer","9/9" in s and ".0039" in s)
    ck(fn+"_legacy_v24",".131" in s and ".185" in s and ".195" in s and "−.293" in s)
    ck(fn+"_no_corruption","???" not in s and "????" not in s and "? APE" not in s and "? RPE" not in s)

zh=(R/"index-zh.html").read_text(encoding="utf-8")
for bad in ["不是","而不是","并不是","不只是"]:
    ck("zh_no_"+bad,bad not in zh,zh.count(bad))
ck("zh_fast_result_meaning","结果立刻改变是否继续找信息" in zh)
ck("zh_no_naked_new_terms",all(x not in zh for x in ["Passive 归因可迁移","ActionBout 多巴胺","平均留出 MSE","Spearman ρ=.453"]))
ck("zh_exact_model_name_retained","UCL RPE-only" in zh)

rows=list(csv.DictReader((R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv").open(encoding="utf-8-sig")))
ck("authority_rows",len(rows)>=37,len(rows))
tests={r["test"]:r for r in rows}
for key in ["Active_vs_Unrewarded_next_reentry","UCL_APE_vs_RPE_daily","SLM_early_policy","Post06_scalar_signed_abs_RPE","behavior_selected_Passive_credit_vs_fixed_075","v24_State_Value_RPE","v24_RPE_only"]:
    ck("authority_"+key,key in tests)
if "UCL_APE_vs_RPE_daily" in tests:
    ck("ape_vs_rpe_p",tests["UCL_APE_vs_RPE_daily"]["p"]=="1.49e-8",tests["UCL_APE_vs_RPE_daily"]["p"])
if "v24_RPE_only" in tests:
    rr=[r for r in rows if r["test"]=="v24_RPE_only" and r["metric"]=="animal_holdout_R2"]
    ck("legacy_rpe_holdout",len(rr)==1 and rr[0]["value"]=="-0.293",rr[0]["value"] if rr else "")

doc=(R/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md").read_text(encoding="utf-8")
ck("audit_doc_fast","社会信息需求" in doc)
ck("audit_doc_codex","State+Value+RPE" in doc and "RPE-only" in doc)
ck("audit_doc_transfer","9/9" in doc and "P=.0039" in doc)

print("FAILURES",fails)
sys.exit(1 if fails else 0)
