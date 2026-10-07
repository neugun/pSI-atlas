# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def insert_before(text,anchor,block,marker):
    if marker in text:
        return text
    if anchor not in text:
        raise RuntimeError("anchor missing: "+anchor[:80])
    return text.replace(anchor,block+"\n"+anchor,1)

ZH_DYN='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_next_observe_memory_v83.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_next_observe_memory_v83_mobile.png"/><img alt="上一次社会结果如何延续到下一次观察时的 VTA 多巴胺状态" loading="lazy" src="assets/SOE_FP_next_observe_memory_v83.png"/></picture></a><figcaption><strong>上一次社会结果会延续到下一次社会信息采样。</strong>A，只看结果后 60 秒内首次重新观察的事件。B，在下一次观察真正开始之前的 −1–0 秒，VTA 多巴胺已经保留前一结果的信息：主动成功相对未奖赏 P=.027，被动结果相对未奖赏 P=.012。C，观察开始后的 0–2 秒差异进一步增强：P=.008 和 .004。D，把每次观察按真实持续时间归一化后，前 25% 的观察阶段仍保留同样的结果依赖状态，两项比较均 P=.004。该分析只检验已经发生重新观察的事件；是否会重新观察由前面的行为结果独立给出。</figcaption></figure>
<div class="callout"><strong>神经层面的快速记忆｜</strong>行为结果先改变下一次是否继续寻找社会信息；当动物随后再次观察时，VTA 的状态在观察开始前就已经携带上一次结果的痕迹，并延续到新的观察过程中。这样，秒级行为调整和下一次采样时的神经状态被连到同一条跨事件学习链上。</div>'''

EN_DYN='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_next_observe_memory_v83.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_next_observe_memory_v83_mobile.png"/><img alt="Previous social outcome persists into VTA dopamine during the next observation" loading="lazy" src="assets/SOE_FP_next_observe_memory_v83.png"/></picture></a><figcaption><strong>The previous social outcome persists into the next social-information sample.</strong>A, first re-observation bouts occurring within 60 s of an outcome. B, VTA dopamine already differs during the −1–0 s period before the next observation begins: Active versus Unrewarded P=.027; Passive versus Unrewarded P=.012. C, the separation strengthens during the first 0–2 s after observation onset: P=.008 and .004. D, the same ordering persists when each observation is normalized to its actual bout duration; during the first quarter of the bout both rewarded-outcome contrasts give P=.004. This analysis conditions on re-observation occurring; the probability of re-sampling is established independently by the behavioral analysis above.</figcaption></figure>
<div class="callout"><strong>Neural correlate of the fast memory.</strong> The outcome first changes whether another social sample is taken. When re-observation does occur, VTA state already carries the previous outcome before the new sample starts and remains separated during the new observation bout, linking the fast behavioral rule to a cross-event neural state.</div>'''

ZH_VTA='''<div id="vta-psth-biological-v84">
<div class="section-kicker" style="margin-top:28px">先看原始时间过程</div>
<div class="bio-logic"><strong>两种多巴胺读法回答两个互补问题｜</strong>固定结果后 0–6 秒强调结果出现后的评估与更新；真实行为时长归一化强调行为执行期间的多巴胺。把两种时间表示放在同一批事件上，可以直接看到哪些结果跨方法保留，哪些计算更依赖结果后的持续信号。</div>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_biological_story_v82.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_PSTH_biological_story_v82_mobile.png"/><img alt="两种 fiber photometry 多巴胺读法下的结果事件与下一次观察 PSTH" loading="lazy" src="assets/SOE_FP_PSTH_biological_story_v82.png"/></picture></a><figcaption><strong>同一批事件的多巴胺时间结构说明两种读法各自抓住了什么。</strong>A，固定 0–6 秒中，主动成功在结果附近出现快速峰值，被动结果随后出现更持续的正向信号，未奖赏则转为持续负向。B，把同一批事件按真实行为时长归一化后，被动结果在行为期间保持较高多巴胺，主动成功更集中于行为早期，未奖赏在大部分行为阶段保持较低。C–D，上一次结果还能延续到下一次观察：未奖赏之后的重新观察处于更低的 VTA 状态，主动成功或被动结果后的重新观察更高。逐动物 0–2 秒比较分别为 P=.008 和 .004。</figcaption></figure>
<details id="vta-psth-support-v82"><summary>展开：观察位置、真实持续时间和逐事件热图</summary><div class="detail-body">
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_observation_context_v82.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_PSTH_observation_context_v82_mobile.png"/><img alt="不同观察位置及前一结果条件下的 VTA 多巴胺 PSTH" loading="lazy" src="assets/SOE_FP_PSTH_observation_context_v82.png"/></picture></a><figcaption><strong>观察事件本身也具有可分离的时间结构。</strong>A–B，学习者位于观察区域内部时，观察开始后多巴胺明显转正，并在真实观察 bout 内逐步升高；观察区域外部以及总体观察的平均信号更低。C–D，用前一结果重新分组后，主动成功和被动结果后的下一次观察都高于未奖赏后的重新观察，固定时间轴和真实 bout 归一化两种表示给出相同方向。</figcaption></figure>
<figure class="figure evidence-figure"><a class="figure-zoom" href="assets/SOE_FP_PSTH_trial_heatmaps_v82.png" rel="noopener" target="_blank"><img alt="主动成功 被动结果 未奖赏的逐事件多巴胺热图" loading="lazy" src="assets/SOE_FP_PSTH_trial_heatmaps_v82.png"/></a><figcaption><strong>逐事件热图。</strong>上排使用固定结果后时间轴，下排把同一批可比较事件按真实 bout 时长归一化。主动成功、被动结果和未奖赏的差异在单 trial 层面都能看到，同时保留了明显的事件间异质性。</figcaption></figure>
<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">逐动物 PSTH 源数据</a><p>固定时间轴、真实 bout 归一化以及下一次观察条件下的逐动物平均曲线。</p></div><div class="download-card"><a href="data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv">下一次观察状态统计</a><p>观察前、观察后以及真实 bout 阶段的逐动物配对检验。</p></div></div>
</div></details>
</div>'''

EN_VTA='''<div id="vta-psth-biological-v84">
<div class="section-kicker" style="margin-top:28px">Start from the dopamine time course</div>
<div class="bio-logic"><strong>The two readouts answer complementary biological questions.</strong> The fixed 0–6 s window emphasizes evaluation and updating after an outcome appears; actual-bout normalization emphasizes dopamine expressed while the behavior is being executed. Applying both views to the same events reveals which effects are method-invariant and which depend on sustained post-outcome activity.</div>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_biological_story_v82.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_PSTH_biological_story_v82_mobile.png"/><img alt="Outcome and next-observation dopamine PSTHs under two fiber-photometry readouts" loading="lazy" src="assets/SOE_FP_PSTH_biological_story_v82.png"/></picture></a><figcaption><strong>The time course shows what each dopamine readout captures.</strong>A, in fixed 0–6 s time, Active success peaks around the outcome, Passive produces a later and more sustained positive signal, and Unrewarded becomes persistently negative. B, after normalizing the same events to actual bout duration, Passive remains elevated through much of the behavior, Active is more onset-weighted, and Unrewarded stays lower through most of the bout. C–D, the previous outcome also carries into the next observation: re-observation after Unrewarded occurs in a lower VTA state than re-observation after Active or Passive outcomes; animal-level 0–2 s comparisons give P=.008 and .004.</figcaption></figure>
<details id="vta-psth-support-v82"><summary>Expand: observation location, actual bout duration and single-event heatmaps</summary><div class="detail-body">
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_observation_context_v82.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_PSTH_observation_context_v82_mobile.png"/><img alt="VTA dopamine PSTHs across observation locations and previous outcomes" loading="lazy" src="assets/SOE_FP_PSTH_observation_context_v82.png"/></picture></a><figcaption><strong>Observation itself contains separable temporal structure.</strong>A–B, when the learner is inside the observation zone, dopamine turns positive after observation onset and rises across the actual observation bout; outside-zone and pooled observation signals are lower. C–D, conditioning the next observation on the previous outcome reproduces the same Active/Passive versus Unrewarded ordering in both fixed time and bout-normalized views.</figcaption></figure>
<figure class="figure evidence-figure"><a class="figure-zoom" href="assets/SOE_FP_PSTH_trial_heatmaps_v82.png" rel="noopener" target="_blank"><img alt="Single-event dopamine heatmaps for Active Passive and Unrewarded outcomes" loading="lazy" src="assets/SOE_FP_PSTH_trial_heatmaps_v82.png"/></a><figcaption><strong>Single-event heatmaps.</strong>The upper row uses fixed post-outcome time; the lower row normalizes the same comparable events to actual bout duration. Active, Passive and Unrewarded differences remain visible at the trial level while preserving substantial event-to-event heterogeneity.</figcaption></figure>
<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">Animal-level PSTH source data</a><p>Animal-average curves for fixed time, actual-bout normalization and next-observation conditions.</p></div><div class="download-card"><a href="data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv">Next-observation state statistics</a><p>Paired animal-level tests before observation, after onset and across actual bout phase.</p></div></div>
</div></details>
</div>'''

# Apply page insertions
p=ROOT/"index-zh.html"; s=p.read_text(encoding="utf-8")
s=insert_before(s,'<div class="callout"><strong>秒级效应的生物学含义｜</strong>',ZH_DYN,"SOE_FP_next_observe_memory_v83.png")
s=insert_before(s,'<details id="vta-fp-da-method-v77">',ZH_VTA,'id="vta-psth-biological-v84"')
p.write_text(s,encoding="utf-8")

p=ROOT/"index.html"; s=p.read_text(encoding="utf-8")
s=insert_before(s,'<div class="callout"><strong>Biological meaning of the fast effect.</strong>',EN_DYN,"SOE_FP_next_observe_memory_v83.png")
s=insert_before(s,'<details id="vta-fp-da-method-v77">',EN_VTA,'id="vta-psth-biological-v84"')
p.write_text(s,encoding="utf-8")

# Add the new cross-event neural state to the mechanistic support registry.
p=ROOT/"data"/"SLM_multiaxis_mechanistic_support_v75.csv"
m=pd.read_csv(p)
rows=[
["fp_cross_event_memory","next_observe_pre_active_vs_unrewarded","paired_DA_diff",0.2253532274,9,0.02734375,"下一次观察开始前 −1–0 秒仍保留主动成功相对未奖赏的 VTA 状态差异","SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv"],
["fp_cross_event_memory","next_observe_pre_passive_vs_unrewarded","paired_DA_diff",0.2940556145,9,0.01171875,"下一次观察开始前 −1–0 秒仍保留被动结果相对未奖赏的 VTA 状态差异","SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv"],
["fp_cross_event_memory","next_observe_post_active_vs_unrewarded","paired_DA_diff",0.3135910169,9,0.0078125,"下一次观察开始后 0–2 秒主动成功相对未奖赏的 VTA 状态更高","SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv"],
["fp_cross_event_memory","next_observe_post_passive_vs_unrewarded","paired_DA_diff",0.3563680387,9,0.00390625,"下一次观察开始后 0–2 秒被动结果相对未奖赏的 VTA 状态更高","SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv"],
["fp_cross_event_memory","next_observe_phase25_active_vs_unrewarded","paired_DA_diff",0.3175375815,9,0.00390625,"真实观察 bout 前 25% 仍保留主动成功相对未奖赏的状态差异","SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv"],
["fp_cross_event_memory","next_observe_phase25_passive_vs_unrewarded","paired_DA_diff",0.2843135558,9,0.00390625,"真实观察 bout 前 25% 仍保留被动结果相对未奖赏的状态差异","SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv"],
]
extra=pd.DataFrame(rows,columns=m.columns)
for key in extra.test:
    m=m[m.test.astype(str)!=key]
m=pd.concat([m,extra],ignore_index=True)
m.to_csv(p,index=False)
print("patched FP PSTH biological story")
