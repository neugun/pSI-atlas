# -*- coding: utf-8 -*-
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
blocks={
"index.html":'''<div class="model-contract" id="vta-next-choice-goal-test-v134">
<strong>Does outcome DA improve prediction of the mouse's next choice?</strong> This matters for the paper's goal of understanding how learned social information reshapes future information seeking. A source-timing audit found that <strong>315/1,706 (18.5%)</strong> of fixed 0–6 s DA events and <strong>738/1,363 (54.1%)</strong> of historical extended-interval DA events overlap the next choice anchor. They are unsuitable for a simple earlier-signal → future-choice claim. Re-fitting the same leave-animal-out behavior-only versus behavior+DA comparison on temporally restricted cases gives:
<table class="metric-table"><thead><tr><th>Signal</th><th>Time exclusion</th><th>Animal-level additional DA benefit</th></tr></thead><tbody>
<tr><td>Fixed Post 0–6 s</td><td>Next event begins at least 6 s after anchor; n=1,391</td><td>5/9 improve, P=.5703</td></tr>
<tr><td>Historical extended interval</td><td>No extension beyond next anchor; boundary touch allowed; n=625</td><td>1/9 improve, P=.1289</td></tr></tbody></table>
<strong>Conclusion:</strong> independent prediction of the next Observe choice by residual outcome DA is <em>not established</em> by these models. The second row is only a boundary-touch sensitivity, not a strict offset-separated prospective DA test. It does not invalidate the independent learned behavior, Early/Middle signals, or JAWS perturbation. <a href="data/SOE_VTA_next_choice_timing_QC_v131.csv">Animal-held-out contrasts</a> · <a href="data/SOE_VTA_next_choice_event_overlap_v131.csv">Event-overlap audit</a>.
</div>''',
"index-zh.html":'''<div class="model-contract" id="vta-next-choice-goal-test-v134">
<strong>结果后的 DA 是否真的帮助预测小鼠下一次会不会观察？</strong>这关系到整篇文章的目标：一次社会结果如何改变未来社会信息采样。复查时间轴发现，固定 0–6 秒信号的 <strong>315/1,706（18.5%）</strong> 个事件，以及旧延长区间信号的 <strong>738/1,363（54.1%）</strong> 个事件，实际上与下一次行为时间重叠，不能直接解释为“先有 DA，之后才有行为”。重新按动物留出、只比较原行为模型与行为模型加 DA 的增量：
<table class="metric-table"><thead><tr><th>信号</th><th>时间筛选</th><th>额外增加 DA 后的改善</th></tr></thead><tbody>
<tr><td>结果后固定 0–6 秒</td><td>至少 6 秒后才发生下一事件，n=1,391</td><td>5/9 动物，P=.5703</td></tr>
<tr><td>历史延长区间</td><td>区间不能超过下一事件，但允许恰好接触边界，n=625</td><td>1/9 动物，P=.1289</td></tr></tbody></table>
<strong>结论：</strong>目前没有得到 DA 在行为状态模型之外稳定预测下一次观察选择的证据。第二行只是允许边界接触的探索性分析，不能当作完全时间分离的前瞻预测。这不否定已确认的行为学习、VTA 早期/中段分析或独立 JAWS 因果证据。<a href="data/SOE_VTA_next_choice_timing_QC_v131.csv">留出动物的比较表</a> · <a href="data/SOE_VTA_next_choice_event_overlap_v131.csv">事件重叠核查</a>。
</div>'''
}
for name,block in blocks.items():
 p=R/name;s=p.read_text(encoding="utf-8")
 if 'id="vta-next-choice-goal-test-v134"' in s:continue
 pat=r'(<figure\b[^>]*id="vta-real-bout-qa-figure-v126".*?</figure>)'
 ns,n=re.subn(pat,lambda m:m.group(1)+"\n"+block,s,count=1,flags=re.S)
 assert n==1,(name,n)
 p.write_text(ns,encoding="utf-8")
 print("NEXT_CHOICE_BLOCK",name,flush=True)
