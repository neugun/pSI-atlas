# -*- coding: utf-8 -*-
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
BLOCK={
"index.html":'''<div class="model-contract" id="vta-outcome-source-interaction-v148"><strong>New exploratory neural bridge: does prior observation alter the DA response to the subsequent outcome?</strong>
The current nine-animal FP dataset is <strong>selected on observer-feeding-related ObsEat events</strong> (1,714 usable Post 0–6 s DA events), so it cannot directly estimate the probability of the next general Observe action. For the biological question it can answer, matched nested held-animal models show:
<ul><li>Adding observation presence alone beyond outcome, demonstrator state, pre-event self/social state and session time does not reliably improve held-animal DA prediction.</li>
<li>Adding Observed × DemFeed without outcome interactions also does not reliably help.</li>
<li><strong>Observed × Active / Passive outcome interactions add predictive information in 7/9 animals</strong> beyond all those covariates: mean ΔMSE +0.01368, median +0.00309, exact two-sided P=.03125. Conditional within-session/outcome/demonstrator/5-min-block shuffles (300) give empirical one-sided P=.0233.</li></ul>
<strong>Evidence tier: exploratory, not confirmed.</strong> The comparison family has BH q≈.0703; excluding one influential animal lowers the paired result to P=.0625 (6/8); only 4/9 animals improve in both session halves. This is consistent with <em>social-observation-history-dependent outcome responses</em>, not proof of the exact credit-assignment equation, causal DA teaching, or prospective next-choice prediction. The result preserves the negative boundaries as essential controls. <a href="data/SOE_VTA_source_outcome_stepwise_v148.csv">Model ladder</a> · <a href="data/SOE_VTA_source_outcome_loo_sensitivity_v148.csv">Leave-one-animal audit</a> · <a href="docs/VTA_SOURCE_OUTCOME_INTERACTION_EXPLORATORY_v148.md">Methods / limits</a>.</div>
<figure class="figure evidence-figure manuscript-square" id="vta-source-outcome-plot-v148"><a class="figure-zoom" href="assets/SOE_VTA_source_outcome_interaction_exploratory_v148.png" target="_blank" rel="noopener"><img src="assets/SOE_VTA_source_outcome_interaction_exploratory_v148.png" loading="lazy" alt="Source-conditional outcome dopamine held-animal incremental prediction and conditional shuffles"/></a><figcaption><strong>Exploratory source × outcome interaction.</strong>A, addition of actual observation, observed demonstrator state and Obs×Active/Passive in sequence; B, all nine held-out animals; C, 300 session/outcome/demonstrator/time-stratified shuffles with frozen ridge parameters; D, recorded events are ObsEat-selected, not all possible Observe opportunities. Errors and P values are animal-level unless otherwise noted. This panel is supplementary until replicated in an independent neural cohort and survives a prespecified model family.</figcaption></figure>''',
"index-zh.html":'''<div class="model-contract" id="vta-outcome-source-interaction-v148"><strong>新增探索性神经结果：先前是否观察，会不会改变 VTA 对随后不同结果的 DA 反应？</strong>
这套 9 只动物的 FP 数据以观察鼠进食相关的 <strong>ObsEat 事件</strong>为筛选条件（有效结果后 0–6 秒 DA 共 1,714 个事件），不能直接拿来预测全部观察机会中的一般性 Observe/No-observe 决策。在它能够回答的结果期问题中，逐动物留出、训练集内选择正则化参数后：
<ul><li>在当前结果、同伴状态、观察者事件前状态及场次时间之外，只加入“有没有真实社会观察”，没有稳定增量。</li>
<li>再加入“观察 × 示范鼠是否进食”，也没有稳定增量。</li>
<li>进一步加入<strong>“观察 × Active/Passive 结果类别”</strong>，则在 <strong>7/9 只动物</strong>上改善结果期 DA 预测：均值 ΔMSE +0.01368，中位数 +0.00309，动物级双侧精确 P=.03125。按场次、结果、示范鼠状态和五分钟区间进行 300 次条件打乱，经验单侧 P=.0233。</li></ul>
<strong>证据级别：探索性，不能直接升级为已确认机制。</strong>同族比较 BH q≈.0703；去掉影响最大的动物后为 6/8、P=.0625；只有 4/9 动物在场次前后两半都改善。因此它支持“此前观察经历可能调节随后结果 DA 反应”的研究方向，但尚不能证明具体的社会归因学习方程、DA 的直接教学因果作用，或对下一次观察的独立预测。阴性对照全部保留。<a href="data/SOE_VTA_source_outcome_stepwise_v148.csv">分步模型比较</a> · <a href="data/SOE_VTA_source_outcome_loo_sensitivity_v148.csv">逐动物敏感性</a> · <a href="docs/VTA_SOURCE_OUTCOME_INTERACTION_EXPLORATORY_v148.md">方法与局限</a>。</div>
<figure class="figure evidence-figure manuscript-square" id="vta-source-outcome-plot-v148"><a class="figure-zoom" href="assets/SOE_VTA_source_outcome_interaction_exploratory_v148.png" target="_blank" rel="noopener"><img src="assets/SOE_VTA_source_outcome_interaction_exploratory_v148.png" loading="lazy" alt="社会观察与结果类别交互对应的 VTA 结果期多巴胺探索性分析"/></a><figcaption><strong>社会观察经历与结果 DA 反应的交互。</strong>A，依次加入有无观察、观察到示范鼠进食，以及观察与结果类别的交互；B，9 只留出动物的真实变化；C，300 次按场次、结果、示范鼠状态及时间分层的打乱对照；D，数据选择于观察鼠进食事件，不能冒充完整的观察机会集合。这个图暂列为探索性补充证据，等待独立神经数据和预设模型检验。</figcaption></figure>'''
}
for name,block in BLOCK.items():
 p=ROOT/name;s=p.read_text(encoding="utf-8")
 if 'id="vta-outcome-source-interaction-v148"' in s:continue
 m=re.search(r'<div class="model-contract" id="vta-next-choice-goal-test-v134">.*?</div>',s,flags=re.S)
 assert m is not None,"missing post-readout temporal gate in "+name
 s=s[:m.end()]+"\n"+block+"\n"+s[m.end():]
 p.write_text(s,encoding="utf8")
 print("ADDED exploratory outcome interaction",name)
