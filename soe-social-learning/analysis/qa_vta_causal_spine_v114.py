# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
fails = []

def ck(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        fails.append(name)

en = (ROOT / "index.html").read_text(encoding="utf-8")
zh = (ROOT / "index-zh.html").read_text(encoding="utf-8")

# Exact outcome-stage source data.
rep = pd.read_csv(ROOT / "data" / "SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv")
for test in ["update_selected_vs_w0p75", "update_selected_vs_w1p0"]:
    q = rep[rep.test.eq(test)]
    ck(test+"_one_row", len(q)==1, len(q))
    if len(q)==1:
        q = q.iloc[0]
        ck(test+"_realbout_9of9", int(q.bout_wins)==9, q.bout_wins)
        ck(test+"_realbout_p", abs(float(q.bout_p)-0.00390625)<1e-12, q.bout_p)

q075 = rep[rep.test.eq("update_selected_vs_w0p75")].iloc[0]
q100 = rep[rep.test.eq("update_selected_vs_w1p0")].iloc[0]
ck("fixed075_preserved", int(q075.post_wins)==7 and abs(float(q075.post_p)-.0390625)<1e-12)
ck("fixed100_preserved", int(q100.post_wins)==6 and abs(float(q100.post_p)-.0546875)<1e-12)

# The narrative spine must exist once in each language.
for fn, s in [("en", en), ("zh", zh)]:
    ck(fn+"_spine_once", s.count('id="vta-causal-spine-v113"')==1, s.count('id="vta-causal-spine-v113"'))

for tag in [
    "Early · decide whether to sample",
    "Middle · evaluate the sampling action",
    "Post · assign outcome-specific social credit",
    "Causal · is VTA required for teaching?",
    "8/9 extended intervals (P=.0078)",
    "10/10 animals (P=.001953)",
    "frozen original fixed-window metric",
    "priority is based on biological alignment rather than a smaller P value",
    "Integrated VTA conclusion: Early → Middle → Post → causal."
]:
    ck("en_"+tag, tag in en)

for tag in [
    "早期 · 决定是否采样",
    "中段 · 评估这次采样动作",
    "结果期 · 给结果分配来源特异社会归因",
    "因果 · VTA 是否参与教学",
    "延长区间为 8/9（P=.0078）",
    "10/10 动物中下降（P=.001953）",
    "优先级依据生物学对齐关系，而非单纯依据更小的 P 值",
    "VTA 整合主线：早期 → 中段 → 结果期 → 因果。"
]:
    ck("zh_"+tag, tag in zh)

# Guard against replacing the historical authority with the new readout.
ck("en_frozen_figure_retained", "Frozen original temporal anchor." in en and "original fixed-window post-outcome RPE result" in en)
ck("zh_frozen_figure_retained", "冻结的原始时间轴参照。" in zh and "原始固定窗口的结果后 RPE" in zh)
ck("en_no_old_core_post_card", '<div class="metric">RPE / social credit</div>' not in en)
ck("zh_no_old_core_post_card", '<div class="metric">RPE / 社会归因</div>' not in zh)

# Explicitly preserve the distinction between the passive-credit neural readout
# and the Active-credit causal perturbation.
ck("en_branch_distinction", "same credit-assignment branch on successful Active outcomes, rather than the Passive-credit readout used above" in en)
ck("zh_branch_distinction", "和上方被动结果归因读出属于不同结果分支" in zh)

# Chinese VTA section retains the no-template-negation style rule.
k = zh.find('id="vta"')
a = zh.rfind("<section", 0, k)
b = zh.find("<section", k+1)
vta_zh = zh[a:b]
for banned in ["不是", "而不是", "并不是", "不只是"]:
    ck("zh_no_"+banned, banned not in vta_zh, vta_zh.count(banned))

print("FAILURES", fails)
sys.exit(1 if fails else 0)
