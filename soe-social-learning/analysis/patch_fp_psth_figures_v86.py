# -*- coding: utf-8 -*-
from pathlib import Path

R=Path(__file__).resolve().parents[1]

ZH='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_DA_outcome_contrasts_v85.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_DA_outcome_contrasts_v85_mobile.png"/><img alt="固定结果后时间与真实行为时长对三类社会结果多巴胺差异的影响" loading="lazy" src="assets/SOE_FP_DA_outcome_contrasts_v85.png"/></picture></a><figcaption><strong>两种时间读法揭示同一结果信号的不同时间成分。</strong>A，主动成功相对未奖赏的差异在结果后 0–6 秒更大：固定窗口 P=.012，真实行为片段 P=.055，而且两种读法的差异本身达到 P=.027。这说明主动成功后的多巴胺区分有一部分延续到行为结束以后。B，被动结果相对未奖赏在两种读法中都成立（P=.004 和 .020），说明这类结果信号贯穿行为执行与结果后时段。C，被动结果相对主动成功在真实行为片段内更清楚（P=.039），固定窗口中较弱（P=.203）；两种读法的直接差异 P=.570，因此这里保留为时间分布线索。D，逐动物汇总两种读法对三个结果对比的影响。</figcaption></figure>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_event_selection_v86.png" rel="noopener" target="_blank"><img alt="全部结果事件与两种多巴胺读法共同事件的结果对齐 PSTH" loading="lazy" src="assets/SOE_FP_PSTH_event_selection_v86.png"/></a><figcaption><strong>结果事件的时间结构不依赖共同事件筛选。</strong>A，使用全部权威结果事件：主动成功 442、被动结果 420、未奖赏 861。B，只保留两种 FP→DA 读法都有效的 1,371 个共同事件：259、257、855。主动成功的快速正向响应、被动结果的持续正向响应和未奖赏后的负向状态在两组数据中保持相同总体结构。</figcaption></figure>'''

EN='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_DA_outcome_contrasts_v85.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_DA_outcome_contrasts_v85_mobile.png"/><img alt="Outcome contrasts under fixed post-outcome time and actual bout duration" loading="lazy" src="assets/SOE_FP_DA_outcome_contrasts_v85.png"/></picture></a><figcaption><strong>The two temporal readouts expose different portions of the same outcome signal.</strong>A, Active success versus Unrewarded is larger in the 0–6 s outcome window: P=.012 in fixed time, P=.055 within the actual bout, with a direct readout difference of P=.027. This supports an Active-success signal that continues beyond action execution. B, Passive versus Unrewarded is supported under both views (P=.004 and .020), consistent with a signal spanning behavior and the post-outcome period. C, Passive versus Active is clearest within the actual bout (P=.039) and weaker in the fixed window (P=.203); the direct readout difference is P=.570, so this is retained as a temporal-distribution clue rather than an interaction claim. D, animal-level summary of the three direct readout effects.</figcaption></figure>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_event_selection_v86.png" rel="noopener" target="_blank"><img alt="Outcome aligned PSTHs in all outcome events and the common event subset" loading="lazy" src="assets/SOE_FP_PSTH_event_selection_v86.png"/></a><figcaption><strong>The outcome time course survives common-event selection.</strong>A, all authoritative outcome events: 442 Active, 420 Passive and 861 Unrewarded. B, the 1,371 events valid under both FP-to-dopamine readouts: 259, 257 and 855. The fast Active response, sustained Passive response and post-outcome negative Unrewarded state retain the same overall structure.</figcaption></figure>'''

for fn,block in [("index-zh.html",ZH),("index.html",EN)]:
    p=R/fn; s=p.read_text(encoding="utf-8")
    if "SOE_FP_DA_outcome_contrasts_v85.png" in s:
        print("already patched",fn); continue
    marker='<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">'
    if marker not in s: raise RuntimeError("missing marker "+fn)
    s=s.replace(marker,block+"\n"+marker,1)
    # widen the support label now that it includes the full result set
    if fn=="index-zh.html":
        s=s.replace('展开：观察位置、真实持续时间和逐事件热图','展开：结果事件、两种时间读法、观察位置和逐事件热图',1)
    else:
        s=s.replace('Expand: observation location, actual bout duration and single-event heatmaps','Expand: outcome events, both temporal readouts, observation context and single-event heatmaps',1)
    p.write_text(s,encoding="utf-8")
print("inserted outcome contrast and event-selection PSTH figures")
