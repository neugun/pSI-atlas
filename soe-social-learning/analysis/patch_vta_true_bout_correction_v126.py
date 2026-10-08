# -*- coding: utf-8 -*-
"""2026-10-07 urgent correction: ActionBout is not ObsBout. Preserve historical stats as exploratory."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
NOTICE={
"index.html":'''<div class="model-contract" id="vta-true-bout-audit-v126">
<strong>Corrected source audit: long model action intervals are not actual observation bouts.</strong>
On the original 1,371 events, the old variable named <code>DA_ActionBout_AUCperSec</code> integrates an extended post-anchor interval (median 28.85 s), including <strong>550 no-observation events</strong>. True observation bouts have a median duration of <strong>2.40 s</strong>; 730/821 finish before the outcome anchor. These windows measure different biological phases.
On the same <strong>821 genuine-observation events / 9 animals</strong>, behavior-selected Passive-credit update beats fixed weight 0.75 in <strong>8/9 extended intervals (P=.0078)</strong>, <strong>4/9 real observation bouts (P=.8203)</strong>, and <strong>5/9 fixed 0–6 s (P=.1641)</strong>. Against weight 1.0 the counts are <strong>8/9 (P=.0117)</strong>, <strong>3/9 (P=.8203)</strong>, and <strong>7/9 (P=.0742)</strong>. Critically, the extended-interval selected model beats the history-only baseline in only <strong>6/9 (P=.5703)</strong>.
<strong>Revised inference:</strong> the longer event-defined interval has a model-comparator association, not proof of DA encoding social credit during real observation. The earlier 9/9 (P=.0039) must be labeled a historical extended-interval result. True-observation DA is an earlier sampling-phase measurement, so its null Post-credit result does not disprove outcome-stage updating. Early/Middle original analyses, fixed-window outcome analyses and the separate JAWS causal branch retain their own frozen contracts.
</div>
<figure class="figure evidence-figure manuscript-square" id="vta-real-bout-qa-figure-v126"><a class="figure-zoom" href="assets/SOE_VTA_true_obs_interval_audit_v126.png" target="_blank" rel="noopener"><img src="assets/SOE_VTA_true_obs_interval_audit_v126.png" loading="lazy" alt="Source-verified 2.4-second real observation bouts versus 28.85-second extended intervals, temporal landmarks, matched credit-model comparisons"/></a><figcaption><strong>Source-level correction of action interval versus actual observation bout.</strong> A, event-duration distributions; B, one original observation event versus 0–6 s and extended outcome interval; C, matched 821-event comparison; D, importance of testing the no-credit history baseline. All animal-level P values are two-sided, exploratory and uncorrected for multiplicity. Download <a href="data/SOE_VTA_true_obs_post_action_credit_comparisons_v126.csv">complete contrasts</a>.</figcaption></figure>''',
"index-zh.html":'''<div class="model-contract" id="vta-true-bout-audit-v126">
<strong>数据来源纠错：模型里的长 action 区间，不能当作真正的观察 bout。</strong>
原先 1,371 个事件中的 <code>DA_ActionBout_AUCperSec</code> 来自以结果锚点为起点的较长区间，中位数 <strong>28.85 秒</strong>，其中还包含 <strong>550 个没有观察行为的事件</strong>。真正观察 bout 的中位数是 <strong>2.40 秒</strong>；821 个可用观察事件中，有 730 个观察 bout 在结果锚点之前已经结束。两类信号来自不同的行为阶段。
把三种读出严格限制到<strong>同一批 821 个真实观察事件、9 只动物</strong>，行为选出的被动社会归因相对固定权重 0.75，在<strong>延长区间为 8/9（P=.0078）</strong>、<strong>真实观察片段为 4/9（P=.8203）</strong>、<strong>固定 0–6 秒为 5/9（P=.1641）</strong>；相对权重 1.0 分别为 <strong>8/9（P=.0117）</strong>、<strong>3/9（P=.8203）</strong> 和 <strong>7/9（P=.0742）</strong>。但延长区间模型相对不含该归因变量的历史基线只有 <strong>6/9 改善（P=.5703）</strong>。
<strong>修订后的结论：</strong>长区间的相关性不能被称为真实观察期 DA 对社会归因的直接编码。原先 9/9、P=.0039 属于历史延长区间模型比较，必须降低证据等级。真实观察信号多数发生在结果之前，所以观察期的阴性结果也不能否定结果期更新。原有早期/中段分析、固定结果窗口和独立 JAWS 因果证据继续按各自原始统计合同保留。
</div>
<figure class="figure evidence-figure manuscript-square" id="vta-real-bout-qa-figure-v126"><a class="figure-zoom" href="assets/SOE_VTA_true_obs_interval_audit_v126.png" target="_blank" rel="noopener"><img src="assets/SOE_VTA_true_obs_interval_audit_v126.png" loading="lazy" alt="真实观察2.4秒与事件后延长区间28.85秒及相同事件的神经模型比较"/></a><figcaption><strong>把真实观察与模型延长区间分开检验。</strong>A，时长分布；B，真实事件的观察、结果后固定窗口和延长区间；C，相同 821 个事件的三读出模型比较；D，加入社会归因是否真正优于不含社会归因的历史基线。P 值为动物级双侧探索性结果，尚未做多重比较校正。<a href="data/SOE_VTA_true_obs_post_action_credit_comparisons_v126.csv">查看完整比较表</a>。</figcaption></figure>'''
}
for name,note in NOTICE.items():
 p=R/name;s=p.read_text(encoding="utf-8")
 if 'id="vta-true-bout-audit-v126"' in s:print(name,"already corrected");continue
 if name=="index.html":
  s=s.replace("At outcome, real-bout DA is the primary mechanistic display; the frozen 0-6 s result remains the original statistical reference.",
    "At outcome, the frozen 0-6 s result remains the original reference; an extended-interval DA measure previously mislabeled real-bout is undergoing a source-level correction.")
  s=s.replace("At Post, real-bout DA favors behavior-selected social credit", "At Post, exploratory extended-interval DA favors behavior-selected social credit")
 else:
  s=s.replace("结果期的机制展示优先采用真实行动片段多巴胺，固定 0–6 秒结果作为冻结的原始统计参照。",
    "结果期保留固定 0–6 秒原始统计参照；此前称作真实行动片段的长区间信号已发现定义问题，正在重新审查。")
  s=s.replace("结果期真实行动片段多巴胺在 9/9 动物中支持行为数据选出的社会归因规则（相对 0.75 和 1.0 均 P=.0039）",
    "此前所谓真实行动片段的 9/9 结果实际来自较长的模型事件区间，已从主证据降级")
 anchor='<section class="alt" id="vta"><div class="container">' if name=="index.html" else '<section id="vta"><div class="container">'
 if anchor not in s:
  anchor=re.search(r'<section[^>]*id="vta"[^>]*><div class="container">',s).group()
 assert anchor in s
 s=s.replace(anchor,anchor+'\n'+note,1)
 # Clearly name the previous readout without changing numeric historical model results.
 st=s.index('id="vta"');en=s.find('</section>',st)
 pre,part,post=s[:st],s[st:en],s[en:]
 if name=="index.html":
  part=part.replace("real-bout DA","extended-interval DA").replace("real action-bout DA","extended-interval DA").replace("real action-bout AUC/s","extended-interval AUC/s").replace("Real-bout","Extended-interval").replace("real-bout","extended-interval")
 else:
  part=part.replace("真实行动片段","模型延长区间").replace("真实行动时长","模型延长区间").replace("真实行动/结果片段","模型延长区间")
 s=pre+part+post
 p.write_text(s,encoding="utf-8")
 print("CORRECTED",name,"num_audit",s.count('id="vta-true-bout-audit-v126"'))
