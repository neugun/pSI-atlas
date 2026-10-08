# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import pandas as pd
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT=Path(__file__).resolve().parents[1]
fail=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fail.append(name)

rep=pd.read_csv(ROOT/"data"/"SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv")
def one(test):
    q=rep[rep.test.eq(test)]
    return q.iloc[0] if len(q)==1 else None

q=one("update_selected_vs_w0p75")
ck("credit075_post_wins",q is not None and int(q.post_wins)==7,getattr(q,"post_wins",None))
ck("credit075_post_p",q is not None and abs(float(q.post_p)-.0390625)<1e-12,getattr(q,"post_p",None))
ck("credit075_bout_wins",q is not None and int(q.bout_wins)==9,getattr(q,"bout_wins",None))
ck("credit075_bout_p",q is not None and abs(float(q.bout_p)-.00390625)<1e-12,getattr(q,"bout_p",None))

q=one("update_selected_vs_w1p0")
ck("credit100_post_wins",q is not None and int(q.post_wins)==6,getattr(q,"post_wins",None))
ck("credit100_post_p",q is not None and abs(float(q.post_p)-.0546875)<1e-12,getattr(q,"post_p",None))
ck("credit100_bout_wins",q is not None and int(q.bout_wins)==9,getattr(q,"bout_wins",None))
ck("credit100_bout_p",q is not None and abs(float(q.bout_p)-.00390625)<1e-12,getattr(q,"bout_p",None))

summ=pd.read_csv(ROOT/"data"/"SOE_VTA_CODEX_REPLICATION_SUMMARY_v96.csv")
q=summ[summ.question.eq("social_credit")]
ck("summary_one_row",len(q)==1,len(q))
if len(q)==1:
    q=q.iloc[0]
    ck("summary_result",q.result=="readout-robust with boundary",q.result)
    m=str(q.meaning)
    for tag in ["7/9 P=.0391","9/9 P=.0039","6/9 P=.0547 (borderline)"]:
        ck("summary_"+tag,tag in m,m)

en=(ROOT/"index.html").read_text(encoding="utf-8")
zh=(ROOT/"index-zh.html").read_text(encoding="utf-8")
for tag in ["The frozen fixed-window results are 7/9 (P=.0391) and 6/9 (P=.0547)","9/9 animals favor the selected rule (both P=.0039)","8/9 extended intervals (P=.0078)"]:
    ck("en_"+tag,tag in en)
for tag in ["冻结固定窗口分别为 7/9（P=.0391）和 6/9（P=.0547）","均为 9/9 动物支持（两项 P=.0039）","延长区间为 8/9（P=.0078）"]:
    ck("zh_"+tag,tag in zh)

for old in ["beats fixed weights under both readouts","outperforms fixed credit under both DA definitions"]:
    ck("en_removed_"+old,old not in en)
for old in ["在两种读出中都优于固定权重","在固定结果后窗口和真实行动时长中都优于固定归因权重"]:
    ck("zh_removed_"+old,old not in zh)

builder=(ROOT/"analysis"/"build_vta_codex_replication_v96.py").read_text(encoding="utf-8")
ck("builder_old_claim_removed","beats fixed 0.75/1.0 under both readouts" not in builder)
ck("builder_boundary_present","readout-robust with boundary" in builder and "6/9 P=.0547 (borderline)" in builder)

doc=(ROOT/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md").read_text(encoding="utf-8")
for tag in ["固定窗口 7/9，P=.0391","真实行动片段 9/9，P=.00391","固定窗口 6/9，P=.0547"]:
    ck("audit_"+tag,tag in doc)

print("FAILURES",fail)
sys.exit(1 if fail else 0)
