# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
messages={
"index.html":'''<div class="model-contract" id="soe-master-goal-v132"><strong>The biological target, not a model-ranking target.</strong> Mice learn how to use *what the demonstrator is doing* to guide their own feeding; the result updates when they next seek social information. Two controllers must be distinguished: <strong>Observe = obtain social information</strong>; <strong>Feed = execute a self-state-dominated action whose probability can briefly depend on observed content</strong>. The linked analyses must separately establish behavioral conversion, memory/state, timed VTA signals, Visual Block versus JAWS interventions, and an agent that genuinely generates the behavior. <a href="docs/SOE_GLOBAL_GOAL_EVIDENCE_ACTIONS_20261007.md">Full story, evidence tiers and next decisive tests</a>.
<br/><strong>Current VTA boundary:</strong> Early policy and Middle APE retain separate neural evidence. Frozen Post 0–6 s DA tests error/update hypotheses; the historical 28.85-s “action bout” is a <em>long modeled interval</em>, not a 2.40-s actual observation bout. Its 9/9 selected-credit comparator must not headline the neural mechanism. On matched 821 events, extended DA improves over history-only baseline in only 6/9 animals (P=.5703). A separate causal JAWS branch supports VTA involvement in Active-credit updating but does not identify one unique DA variable.</div>''',
"index-zh.html":'''<div class="model-contract" id="soe-master-goal-v132"><strong>文章的大目标不是找到拟合最好的模型。</strong>小鼠真正学到的是：<strong>何时从同伴那里获取信息，如何把观察到的具体内容变成自己的进食，以及如何根据结果更新以后是否继续观察</strong>。所以必须区分两个控制过程：<strong>观察是主动获取社会信息</strong>；<strong>自身进食主要受自身状态控制，但会短暂受到观察内容影响</strong>。行为转化、多时间尺度记忆、VTA 神经时间结构、视觉阻断与 JAWS 的不同因果作用，以及能自主生成行为的智能体，最终需要在这条机制链中相互验证。<a href="docs/SOE_GLOBAL_GOAL_EVIDENCE_ACTIONS_20261007.md">查看完整科学目标、证据分级和下一步关键实验</a>。
<br/><strong>当前 VTA 证据边界：</strong>早期策略和中段动作预测误差保留独立的神经证据；结果后固定 0–6 秒主要检验误差/更新模型。旧的 28.85 秒“行动片段”其实是<strong>模型延长区间</strong>，不是真实中位 2.40 秒的观察 bout；原来 9/9 动物的固定权重比较不能作为真实观察期社会归因的主证据。同一 821 个事件中，延长区间的归因模型相对无归因历史基线仅 6/9 改善（P=.5703）。独立 JAWS 操控支持 VTA 参与主动成功后的归因更新，但尚不能指定唯一的 DA 计算变量。</div>'''
}
for filename,note in messages.items():
 p=ROOT/filename
 s=p.read_text(encoding="utf-8")
 if 'id="soe-master-goal-v132"' in s:continue
 if filename=="index.html":
  import re
  new="The frozen 0–6 s DA retains the outcome-stage analysis contract. An extended modeled interval was misidentified as a real behavioral bout; its credit comparison is now exploratory rather than primary neural evidence."
  s,n=re.subn(r"At outcome, real-bout DA is the primary mechanistic display;.*?original statistical reference\.",new,s,count=1)
  assert n==1,("hero_en",n)
  new2="Post 0–6 s error/update signals and the separate causal JAWS branch remain important. The 9/9 extended-interval association is exploratory, not genuine observation-bout social credit."
  s,n=re.subn(r"At Post, exploratory extended-interval DA favors behavior-selected social credit.*?frozen classical reference\.",new2,s,count=1)
  assert n==1,("card_en",n)
 else:
  s=s.replace("已从主证据降级，固定窗口 RPE 保留为冻结的经典参照。","已从主证据降级。固定窗口的误差/更新信号和独立 JAWS 因果结果仍按各自合同保留。")
 anchor='<div class="section-significance"><strong>Central contribution' if filename=="index.html" else '<div class="section-significance"><strong>核心贡献'
 assert anchor in s,filename
 s=s.replace(anchor,note+"\n"+anchor,1)
 p.write_text(s,encoding="utf-8")
 print("GLOBAL_STORY_PATCH",filename,"master block count",s.count('id="soe-master-goal-v132"'))
