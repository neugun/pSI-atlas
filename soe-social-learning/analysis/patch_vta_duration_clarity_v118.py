# -*- coding: utf-8 -*-
"""Correct v116's short-bout intuition using the actual n=1371 action-bout durations."""
from pathlib import Path
import re
P=Path(__file__).resolve().parents[1]
blocks={
"index.html":'''<div class="model-contract" id="vta-readout-explained-v116">
<strong>Why are there two DA readouts from the same neural recordings?</strong>
These are two summaries of <strong>the same 1,371 action/outcome events in 9 animals</strong>, using identical model variables. The difference is the neural integration window:
<strong>Fixed 0–6 s DA</strong> measures the first 6 seconds after event onset; <strong>real action-bout DA</strong> integrates until the recorded action bout ends, then divides by its actual duration (AUC/s).
<strong>Actual bout length matters:</strong> median 28.85 s (interquartile range 12.82–64.12 s); <strong>94.4% of bouts last longer than 6 seconds</strong>. Thus for the great majority of events, fixed 0–6 s captures an <em>early part of the ongoing action</em>, while real-bout DA averages a much longer behavioral episode. Only the minority of bouts ending before 6 s allow the fixed window to contain activity after action offset.
<table class="metric-table" style="width:100%;margin:12px 0"><thead><tr><th>Same matched events</th><th>Real action-bout</th><th>Fixed 0–6 s</th></tr></thead><tbody>
<tr><td>Behavior-selected Passive social credit vs fixed 0.75</td><td>9/9; P=.0039</td><td>7/9; P=.0391</td></tr>
<tr><td>Behavior-selected Passive social credit vs fixed 1.0</td><td>9/9; P=.0039</td><td>6/9; P=.0547 (borderline)</td></tr>
<tr><td>Actor RPE plus absolute RPE</td><td>6/9; P=.3594</td><td>9/9; P=.0039</td></tr>
</tbody></table>
<strong>Interpretation:</strong> the bout-matched readout provides the clearest association with behavior-selected Passive social credit; the first-6-s readout is stronger for some RPE-family tests. One possibility is sustained action/credit signals versus earlier outcome-related responses, <em>not a demonstrated separation of neural mechanisms</em>.
<strong>Still to test:</strong> event duration confounds, time-resolved responses beyond 6 s, and independent DA aligned to the true <em>end</em> of each action bout. Neither of these existing readouts measures a post-bout-only period for the typical long event.
</div>''',
"index-zh.html":'''<div class="model-contract" id="vta-readout-explained-v116">
<strong>同一批多巴胺信号，为什么取两个窗口？</strong>
两种方法使用<strong>相同的 1,371 个行动/结果事件、9 只动物，以及相同的行为模型变量</strong>。区别只在于神经信号累计了多长时间：<strong>固定 0–6 秒 DA</strong>只取事件开始后的前 6 秒；<strong>真实行动片段 DA</strong>取到每次行动真正结束为止，再除以实际持续时间（AUC/秒）。
<strong>最重要的是实际时长：</strong>行动片段的中位数为 <strong>28.85 秒</strong>，四分位范围为 12.82–64.12 秒；<strong>94.4% 的行动持续超过 6 秒</strong>。因此，在绝大多数事件中，固定 0–6 秒记录的是<strong>行动仍在进行时的早期活动</strong>；真实片段则平均更长时间内的 DA。只有少数行动提前结束时，固定窗口才可能包含行动结束后的信号。
<table class="metric-table" style="width:100%;margin:12px 0"><thead><tr><th>同一事件集合</th><th>真实行动片段</th><th>固定 0–6 秒</th></tr></thead><tbody>
<tr><td>行为选出的被动社会归因优于固定权重 0.75</td><td>9/9；P=.0039</td><td>7/9；P=.0391</td></tr>
<tr><td>行为选出的被动社会归因优于固定权重 1.0</td><td>9/9；P=.0039</td><td>6/9；P=.0547（边缘）</td></tr>
<tr><td>主动者奖赏预测误差加上误差绝对值</td><td>6/9；P=.3594</td><td>9/9；P=.0039</td></tr>
</tbody></table>
<strong>如何理解？</strong>真实行动片段对行为数据选出的被动社会归因更敏感，固定前 6 秒对部分奖赏预测误差更敏感。可能存在较持久的行动/归因信号与较早出现的结果反应，但<strong>现有比较尚不能证明它们属于两个分离的神经机制</strong>。
<strong>还需要做的分析：</strong>控制行为持续时间，查看 6 秒之后的真实时间过程，再以每次行动的<strong>结束时刻</strong>重新对齐 DA。现有两种方法对绝大多数长事件都没有直接测量“行动结束之后”这一独立阶段。
</div>'''
}
for name,replacement in blocks.items():
 p=P/name;s=p.read_text(encoding="utf-8")
 pat=r'<div class="model-contract" id="vta-readout-explained-v116">.*?</div>'
 ns,n=re.subn(pat,lambda _:replacement,s,count=1,flags=re.S)
 assert n==1,(name,n)
 # Replace the misleading original one-sentence causal justification as well.
 if name=="index.html":
  ns=ns.replace("real action-bout AUC/s isolates the actual action/outcome episode, whereas fixed 0–6 s also includes later evaluation",
    "real action-bout AUC/s averages the full action, whereas fixed 0–6 s usually samples only its early segment")
 else:
  ns=ns.replace("真实行动片段 AUC/秒对应实际行动/结果过程，固定 0–6 秒同时保留动作结束后的评估阶段",
    "真实行动片段 AUC/秒平均完整行动过程，而固定 0–6 秒通常只覆盖行动最初的部分")
 p.write_text(ns,encoding="utf-8")
 print("CORRECTED",name)
