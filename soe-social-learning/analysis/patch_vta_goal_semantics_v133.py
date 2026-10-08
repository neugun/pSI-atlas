# -*- coding: utf-8 -*-
"""Make VTA section match the actual timing audit, and expose next-choice non-leak test."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
EN=R/"index.html"; ZH=R/"index-zh.html"
fixes={
"index.html":[
("then test Post credit assignment with bout-matched DA while retaining the fixed-window analysis as a locked reference.",
 "then interpret frozen outcome-stage 0–6 s DA separately from an exploratory extended post-anchor interval, with the actual 2.40-s observation bout kept distinct."),
("Post extended-interval DA preferentially supports behavior-derived social credit; contingent JAWS then suppresses the successful-outcome credit-update branch.",
 "The old extended-interval credit-vs-fixed-weights association does not establish neural teaching beyond the no-credit history baseline; contingent JAWS separately tests successful-outcome learning."),
("On the same 1,371 events, behavior-selected Passive credit beats fixed 0.75 and fixed 1.0 in 9/9 animals under extended-interval DA (both P=.0039). The frozen 0–6 s reference is weaker but directionally concordant.",
 "The historical 1,371-event extended-interval model favors selected Passive credit against two fixed weights (9/9; P=.0039), but is NOT an actual observation-bout readout. On 821 matched genuine-observation events it does not reliably beat the no-credit history baseline (6/9; P=.5703)."),
("The current narrative promotes extended-interval credit for a biological reason—the neural window is matched to the actual outcome/action bout—while the fixed 0–6 s RPE result remains a locked reference and sensitivity check.",
 "The historical extended-interval result is now downgraded: it was not matched to actual observation behavior. The fixed 0–6 s error/update analysis and independent JAWS causal test remain visible under separate statistical contracts."),
("the newer bout-matched social-credit readout rather than silently relabeled.",
 "the historical extended-interval credit comparison rather than silently relabeled."),
("Bout-matched social-credit test","Historical long-interval model comparison"),
("extended-interval DA aligns the neural integration window to the actual outcome/action episode and gives the clearest behavior-to-neural test of social credit.",
 "extended-interval DA averages a modeled post-anchor interval, not genuine observation; its weight-comparator gain requires the separate no-credit baseline test."),
("the priority is based on biological alignment rather than a smaller P value.",
 "neither window is promoted to a definitive credit teaching signal on P value alone."),
("Use biology, rather than significance alone, to choose the main Post readout: extended-interval AUC/s averages the complete action bout, whereas fixed 0–6 s usually samples its early portion (94.4% of bouts exceed 6 s).",
 "The long ActionBout-derived interval is model defined and not an observed action bout. The 94.4% exceeding 6 s applies to this extended interval, whereas true observation bouts are typically 2.40 s and usually precede the outcome anchor."),
("Social credit is readout-robust","Historical weight comparison"),
("Passive credit selected entirely from behavior requires no neural retuning. Versus fixed 0.75 it is significant in both readouts; versus 1.0 it is positive but borderline in fixed 0–6 s (6/9, P=.0547) and 9/9 in extended-interval DA (P=.0039).",
 "The preselected Passive-credit rule has stronger weight-comparator association in the historical long interval, but this does not imply incremental evidence over a no-credit outcome/history baseline or true observation-bout encoding."),
("Earlier versus full-bout integration","Early 0–6 s versus extended model interval"),
("This does not establish activity after the action ended; the full-bout readout includes a much longer duration.",
 "This cannot isolate actual action offset or learning, since the extended interval is not a real behavior bout.")
],
"index-zh.html":[
("结果期用模型延长区间多巴胺检验社会归因，同时把固定窗口保留为锁定参照。",
 "结果期分开保留固定 0–6 秒误差/更新分析与历史延长区间探索性比较，不再把延长区间称为真实观察 bout。"),
("结果期模型延长区间最清楚地支持行为数据定义的社会归因",
 "旧延长区间相对两个固定权重有历史关联，但并未证明其在无归因历史基线之外的稳定增量"),
("同一 1,371 个事件中，行为数据选出的被动结果归因相对固定 0.75 和固定 1.0，在模型延长区间多巴胺下均为 9/9 动物支持（两项 P=.0039）。冻结的固定窗口参照方向一致但较弱。",
 "旧 1,371 事件延长区间的模型权重比较为 9/9、P=.0039，但并非真实观察信号。同一 821 个实际观察事件中，相对无归因历史基线仅 6/9 改善（P=.5703）；不将其作为社会归因的主神经证据。"),
("当前主叙事优先模型延长区间来自生物学理由：神经积分窗口与实际行动/结果片段直接对齐；固定 0–6 秒 RPE 继续作为锁定参照和敏感性证据。",
 "原先将模型延长区间解释为真实行动片段是错误的，该结果保留为历史模型比较。固定 0–6 秒误差/更新分析继续作为冻结的独立结果。"),
("真实行动片段给出最清楚的社会归因结果：",
 "旧的模型延长区间给出较强的固定权重对照结果："),
("模型延长区间给出最清楚的社会归因结果：",
 "旧的模型延长区间给出较强的固定权重对照结果："),
("行为数据独立选出的被动结果归因无需用神经数据重新调参。",
 "行为选定的被动归因权重不使用 DA 重新调参，但这一比较仍需检验能否超越不含该变量的历史模型。"),
("真实行动片段为 9/9、P=.0039。",
 "延长区间为 9/9、P=.0039（历史对照，非实际观察 bout）。")
]}
for name,subs in fixes.items():
 p=R/name;s=p.read_text(encoding="utf-8")
 done=0;missing=[]
 for old,new in subs:
  if old in s:s=s.replace(old,new,1);done+=1
  else:missing.append(old[:62])
 p.write_text(s,encoding="utf-8")
 print("VTA_GLOBAL_GOAL_AUDIT",name,"changed",done,"missing",missing,flush=True)
