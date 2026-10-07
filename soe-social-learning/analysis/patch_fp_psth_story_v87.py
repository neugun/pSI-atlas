# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd

R=Path(__file__).resolve().parents[1]

# Add source-data cards to both reader pages.
for fn, zh in [("index-zh.html",True),("index.html",False)]:
    p=R/fn; s=p.read_text(encoding="utf-8")
    if "SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv" not in s:
        if zh:
            old='<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">逐动物 PSTH 源数据</a><p>固定时间轴、真实 bout 归一化以及下一次观察条件下的逐动物平均曲线。</p></div><div class="download-card"><a href="data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv">下一次观察状态统计</a><p>观察前、观察后以及真实 bout 阶段的逐动物配对检验。</p></div></div>'
            new='<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">逐动物 PSTH 源数据</a><p>结果事件、真实行为时长以及下一次观察条件下的逐动物平均曲线。</p></div><div class="download-card"><a href="data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv">下一次观察状态统计</a><p>观察前、观察后以及真实行为片段阶段的逐动物配对检验。</p></div><div class="download-card"><a href="data/SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv">结果信号的时间读法比较</a><p>主动成功、被动结果和未奖赏在固定结果后时间与真实行为时长下的逐动物对比。</p></div><div class="download-card"><a href="data/SOE_FP_PSTH_EVENT_COUNTS_v82.csv">PSTH 事件清单</a><p>全部结果事件与 1,371 个共同事件的数量和真实持续时间。</p></div></div>'
        else:
            old='<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">Animal-level PSTH source data</a><p>Animal-average curves for fixed time, actual-bout normalization and next-observation conditions.</p></div><div class="download-card"><a href="data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv">Next-observation state statistics</a><p>Paired animal-level tests before observation, after onset and across actual bout phase.</p></div></div>'
            new='<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">Animal-level PSTH source data</a><p>Animal-average curves for outcomes, actual-bout normalization and next-observation conditions.</p></div><div class="download-card"><a href="data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv">Next-observation state statistics</a><p>Paired animal-level tests before observation, after onset and across actual bout phase.</p></div><div class="download-card"><a href="data/SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv">Outcome signals across temporal readouts</a><p>Animal-level Active, Passive and Unrewarded contrasts in fixed post-outcome time and actual bout duration.</p></div><div class="download-card"><a href="data/SOE_FP_PSTH_EVENT_COUNTS_v82.csv">PSTH event inventory</a><p>Counts and real durations for all authoritative outcomes and the 1,371 common events.</p></div></div>'
        if old not in s: raise RuntimeError("download block missing "+fn)
        s=s.replace(old,new,1)
    p.write_text(s,encoding="utf-8")

# Add the direct readout findings to the biological note.
p=R/"docs"/"SOE_FP_PSTH_BIOLOGICAL_READOUT_v1_20261006.md"
d=p.read_text(encoding="utf-8")
sec='''## 2B. 哪些结果成分真正受时间读法影响

逐动物比较固定结果后 0–6 秒和真实行为时长：

- **主动成功 − 未奖赏**：固定窗口 8/9 为正，P=.0117；真实行为片段 8/9 为正，P=.0547。固定窗口的对比更大，直接配对 P=.0273。主动成功后的 VTA 区分因此有一部分延续到行为结束以后。
- **被动结果 − 未奖赏**：固定窗口 9/9 为正，P=.00391；真实行为片段 8/9 为正，P=.0195。两种读法都保留这一结果，直接差异 P=.0547。
- **被动结果 − 主动成功**：固定窗口 P=.203；真实行为片段 8/9 为正，P=.0391。读法间直接差异 P=.570，因此它提示被动结果在行为执行期更持续，但当前数据不支持显著的读法交互。

这组结果把“窗口选择”转化为时间结构问题：主动成功相对未奖赏的区分明确从行为执行期延续到结果后；被动结果相对未奖赏则跨两个时间范围都很稳定。

'''
if "## 2B. 哪些结果成分真正受时间读法影响" not in d:
    d=d.replace("## 3. 上一次结果会延续到下一次观察",sec+"## 3. 上一次结果会延续到下一次观察",1)
p.write_text(d,encoding="utf-8")

# Mechanistic support registry.
p=R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv"
m=pd.read_csv(p)
extra=pd.DataFrame([
["fp_outcome_time_structure","Active_vs_Unrewarded_fixed_minus_bout","paired_readout_difference",0.192237,9,0.02734375,"主动成功相对未奖赏的 VTA 区分在结果后 0–6 秒显著大于真实行为片段，支持行为结束后的持续结果信号","SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv"],
["fp_outcome_time_structure","Passive_vs_Unrewarded_actual_bout","paired_DA_contrast",0.326449,9,0.01953125,"被动结果相对未奖赏的多巴胺差异在真实行为片段内仍成立，8/9 动物同方向","SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv"],
["fp_outcome_time_structure","Passive_vs_Active_actual_bout","paired_DA_contrast",0.167553,9,0.0390625,"真实行为片段内被动结果高于主动成功，8/9 动物同方向；读法间直接差异不显著","SOE_FP_OUTCOME_CONTRASTS_BY_READOUT_v85.csv"],
],columns=m.columns)
for key in extra.test:
    m=m[m.test.astype(str)!=key]
m=pd.concat([m,extra],ignore_index=True)
m.to_csv(p,index=False)
print("updated PSTH story, source cards and mechanistic registry")
