# -*- coding: utf-8 -*-
from pathlib import Path
P=Path(__file__).resolve().parents[1]
M={
"index.html":'''<div class="model-contract" id="vta-readout-explained-v116">
<strong>What do the two DA readouts actually measure?</strong>
Consider an action/outcome episode that lasts 3 seconds. <strong>Real action-bout DA</strong> integrates fluorescence from the action onset to its recorded end, divided by its actual duration (AUC/s); in this example, 0–3 s. <strong>Fixed-window DA</strong> integrates the identical event's 0–6 s window, even when the action stops earlier.
The two readings can differ because the second may additionally include activity after the action ends. For an action lasting longer than 6 seconds, the fixed window instead omits the later part. <strong>They are not two different sensors or separate experimental cohorts.</strong>
<table class="metric-table" style="width:100%;margin:12px 0"><thead><tr><th>Same 1,371 events · 9 animals</th><th>Real action-bout DA</th><th>Fixed 0–6 s DA</th></tr></thead><tbody>
<tr><td>Behavior-selected Passive social credit vs weight 0.75</td><td>9/9; P=.0039</td><td>7/9; P=.0391</td></tr>
<tr><td>Behavior-selected Passive social credit vs weight 1.0</td><td>9/9; P=.0039</td><td>6/9; P=.0547 (borderline)</td></tr>
<tr><td>Actor RPE + absolute RPE</td><td>6/9; P=.3594</td><td>9/9; P=.0039</td></tr>
</tbody></table>
<strong>Why keep both?</strong> Real-bout is the principal <em>Post social-credit readout</em> because it follows the duration of the actual behavioral episode; fixed-window remains the original frozen comparator and can be more sensitive to some RPE-family activity. The credit-selected rule and RPE models are different hypotheses, not proof that the neurons encode exactly one mathematical variable.
<strong>Boundary:</strong> neither readout alone separates action execution from post-action evaluation. The after-bout-only response (relative to each event's actual offset), duration-matched controls and prediction of the next action still require dedicated analysis. A smaller P value alone is not a reason to replace a result.
</div>''',
"index-zh.html":'''<div class="model-contract" id="vta-readout-explained-v116">
<strong>为什么同一次多巴胺记录要用两种时间窗口？</strong>
假设一次有结果的行动持续 3 秒。<strong>真实行动片段 DA</strong> 统计从行动开始到实际结束的荧光面积，再除以真实时长（AUC/秒），本例为 0–3 秒。<strong>固定窗口 DA</strong> 仍然从同一事件开始，但固定统计 0–6 秒，因此还可能包含行动结束后的活动。反过来，如果行动超过 6 秒，固定窗口会遗漏后面的活动。<strong>两者取自相同动物、相同传感器和相同记录，仅取值窗口不同。</strong>
<table class="metric-table" style="width:100%;margin:12px 0"><thead><tr><th>同一批 1,371 个事件、9 只动物</th><th>真实行动片段 DA</th><th>固定 0–6 秒 DA</th></tr></thead><tbody>
<tr><td>行为选出的被动社会归因优于固定权重 0.75</td><td>9/9；P=.0039</td><td>7/9；P=.0391</td></tr>
<tr><td>行为选出的被动社会归因优于固定权重 1.0</td><td>9/9；P=.0039</td><td>6/9；P=.0547（边缘）</td></tr>
<tr><td>主动者奖赏预测误差加上误差绝对值</td><td>6/9；P=.3594</td><td>9/9；P=.0039</td></tr>
</tbody></table>
<strong>应该如何解读？</strong> 社会归因主分析优先使用真实行动时长，因为它与实际行动过程对齐；固定 0–6 秒保留为原始统计参照，而且可能更容易捕捉部分奖赏预测误差信号。两类模型解释的是不同问题，不能仅因为某个 P 值更小就认定神经元只编码一种变量。
<strong>尚未得到证明的部分：</strong>现有两种取值方式本身，不能把“正在行动”和“行动结束后的结果评价”完全区分。需要另外以真实行动结束为零点，单独分析结束后的信号，并控制行动持续时间，再检验能否预测下一次行为。
</div>'''
}
for name,block in M.items():
 p=P/name
 s=p.read_text(encoding="utf-8")
 mark='id="vta-readout-explained-v116"'
 if mark in s:print(name,"already patched");continue
 anchor=('<div class="section-kicker" style="margin-top:28px">Post-stage mechanistic readout'
         if name=="index.html" else
         '<div class="section-kicker" style="margin-top:28px">结果期主机制读出')
 pos=s.find(anchor,s.find('id="vta-causal-spine-v113"'))
 if pos<0: raise RuntimeError("post section anchor absent in "+name)
 s=s[:pos]+block+"\n"+s[pos:]
 p.write_text(s,encoding="utf-8")
 print("patched",name,"bytes",len(s))
