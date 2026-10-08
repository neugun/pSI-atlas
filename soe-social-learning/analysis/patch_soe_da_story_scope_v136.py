# -*- coding: utf-8 -*-
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sub={
"index.html":[
("VTA dopamine follows pre-outcome sampling policy, sampling action-prediction error, then behavior-derived source/outcome-specific social credit.",
 "VTA DA has time-dependent relationships to pre-outcome sampling policy, APE and post-outcome error/update computations; whether a unique Post social-credit variable is represented remains open."),
("At Post, the historical extended-interval comparison was directionally favorable for selected credit:",
 "At Post, the historical extended-interval comparison was directionally favorable for selected credit:")
],
"index-zh.html":[
("一次观察过程中，VTA 多巴胺依次反映结果前采样策略、采样动作预测误差（APE）和行为数据定义的来源/结果特异社会归因。",
 "VTA 多巴胺在不同时段与结果前采样策略、动作预测误差（APE）及结果后的误差/更新量有关；结果期是否特异编码某个社会归因变量仍须进一步检验。"),
("目前没有得到 DA 在行为状态模型之外稳定预测下一次观察选择的证据。",
 "目前没有得到 DA 在行为状态模型之外稳定预测下一次观察选择的证据。")
]}
for name,ss in sub.items():
 p=R/name;t=p.read_text(encoding="utf-8")
 for old,new in ss:
  if old in t:t=t.replace(old,new,1);print("FIX",name,old[:60],flush=True)
  else:print("NOT_FOUND",name,old[:45],flush=True)
 p.write_text(t,encoding="utf-8")
