# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
stats=pd.read_csv(ROOT/"data"/"SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv")

def row(window,left,right):
    q=stats[(stats.window.eq(window))&(stats.left.eq(left))&(stats.right.eq(right))]
    if len(q)!=1: raise RuntimeError((window,left,right,len(q)))
    return q.iloc[0]

pre_a=row("pre_-1_0","active","unrewarded")
pre_p=row("pre_-1_0","passive","unrewarded")
pre_ap=row("pre_-1_0","active","passive")
post_a=row("post_0_2","active","unrewarded")
post_p=row("post_0_2","passive","unrewarded")
phase_a=row("phase_0_25","active","unrewarded")
phase_p=row("phase_0_25","passive","unrewarded")

def rep(s,old,new,label):
    if old not in s:
        print("skip already-patched or variant:",label)
        return s
    return s.replace(old,new,1)

# Update reader-facing pages with the corrected outcome authority.
p=ROOT/"index-zh.html"; s=p.read_text(encoding="utf-8")
s=rep(s,
"主动成功相对未奖赏 P=.027，被动结果相对未奖赏 P=.012。C，观察开始后的 0–2 秒差异进一步增强：P=.008 和 .004。",
f"主动成功相对未奖赏 P={pre_a.p:.3f}，被动结果相对未奖赏 P={pre_p.p:.3f}；这一时段被动结果还高于主动成功（P={pre_ap.p:.3f}）。C，观察开始后的 0–2 秒，两种有结果条件都高于未奖赏（均 P={post_a.p:.3f}）。",
"zh dynamics caption")
s=rep(s,
"逐动物 0–2 秒比较分别为 P=.008 和 .004。",
f"逐动物 0–2 秒比较均为 P={post_a.p:.3f}。",
"zh vta caption")
s=rep(s,
"固定 0–6 秒中，主动成功在结果附近出现快速峰值，被动结果随后出现更持续的正向信号，未奖赏则转为持续负向。",
"以结果出现为时间零点时，主动成功在结果附近出现快速峰值，被动结果随后出现更持续的正向信号，未奖赏则转为持续负向。",
"zh outcome phrasing")
p.write_text(s,encoding="utf-8")

p=ROOT/"index.html"; s=p.read_text(encoding="utf-8")
s=rep(s,
"Active versus Unrewarded P=.027; Passive versus Unrewarded P=.012. C, the separation strengthens during the first 0–2 s after observation onset: P=.008 and .004.",
f"Active versus Unrewarded P={pre_a.p:.3f}; Passive versus Unrewarded P={pre_p.p:.3f}; Passive is also higher than Active in this pre-observation window (P={pre_ap.p:.3f}). C, during the first 0-2 s after observation onset both rewarded-outcome conditions exceed Unrewarded (P={post_a.p:.3f} for each contrast).",
"en dynamics caption")
s=rep(s,
"animal-level 0–2 s comparisons give P=.008 and .004.",
f"animal-level 0-2 s comparisons both give P={post_a.p:.3f}.",
"en vta caption")
p.write_text(s,encoding="utf-8")

# Update the biological readout note.
p=ROOT/"docs"/"SOE_FP_PSTH_BIOLOGICAL_READOUT_v1_20261006.md"; d=p.read_text(encoding="utf-8")
d=d.replace("Passive vs Unrewarded：n=9，8/9 同方向，P=.0117。",f"Passive vs Unrewarded：n=9，8/9 同方向，P={pre_p.p:.4f}。")
d=d.replace("Active vs Passive：P=.25。",f"Active vs Passive：P={pre_ap.p:.4f}；方向为 Passive 高于 Active。")
d=d.replace("Passive vs Unrewarded：9/9，P=.00391。",f"Passive vs Unrewarded：8/9，P={post_p.p:.5f}。",1)
d=d.replace("Active vs Passive：P=.496。",f"Active vs Passive：P={row('post_0_2','active','passive').p:.4f}。")
# Explicit event inventory
if "## 2A. PSTH 事件数量" not in d:
    insert="""## 2A. PSTH 事件数量

结果事件的权威身份来自 RL event table，用它去除 legacy passive row 中重复出现的 33 个 Active anchors：

- 全部结果事件：Active 442、Passive 420、Unrewarded 861，共 1,723 个。
- 两种 FP→DA 方法都有效的共同结果事件：Active 259、Passive 257、Unrewarded 855，共 1,371 个。
- 观察事件：Inside 541、Outside 2,183、All-observation 2,724。
- 从一个结果到下一次重新观察且发生在下一结果之前：Active 后 327、Passive 后 298、Unrewarded 后 665，共 1,290 个；最长间隔 54.4 s。

"""
    d=d.replace("## 3. 上一次结果会延续到下一次观察",insert+"## 3. 上一次结果会延续到下一次观察",1)
p.write_text(d,encoding="utf-8")

# Update mechanistic registry directly from the corrected paired animal-level statistics.
p=ROOT/"data"/"SLM_multiaxis_mechanistic_support_v75.csv"; m=pd.read_csv(p)
mapping=[
("next_observe_pre_active_vs_unrewarded",pre_a,"下一次观察开始前 −1–0 秒仍保留主动成功相对未奖赏的 VTA 状态差异"),
("next_observe_pre_passive_vs_unrewarded",pre_p,"下一次观察开始前 −1–0 秒仍保留被动结果相对未奖赏的 VTA 状态差异"),
("next_observe_post_active_vs_unrewarded",post_a,"下一次观察开始后 0–2 秒主动成功相对未奖赏的 VTA 状态更高"),
("next_observe_post_passive_vs_unrewarded",post_p,"下一次观察开始后 0–2 秒被动结果相对未奖赏的 VTA 状态更高"),
("next_observe_phase25_active_vs_unrewarded",phase_a,"真实观察 bout 前 25% 仍保留主动成功相对未奖赏的状态差异"),
("next_observe_phase25_passive_vs_unrewarded",phase_p,"真实观察 bout 前 25% 仍保留被动结果相对未奖赏的状态差异"),
]
for key,r,interp in mapping:
    mask=m.test.astype(str).eq(key)
    if mask.sum()!=1: raise RuntimeError((key,mask.sum()))
    m.loc[mask,"value"]=float(r.mean_diff)
    m.loc[mask,"n"]=int(r.n)
    m.loc[mask,"p"]=float(r.p)
    m.loc[mask,"interpretation"]=interp
m.to_csv(p,index=False)
print("updated corrected PSTH stats and registry")
