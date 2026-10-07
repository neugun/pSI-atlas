# -*- coding: utf-8 -*-
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"index-zh.html"
s=p.read_text(encoding="utf-8")
reps={
'学习可复用的“小鼠社会世界状态”，而不是再做一个 behavior classifier。':'目标是学习可复用的“小鼠社会世界状态”，避免把任务收缩成单一的行为分类器。',
'intervention identity 被作为作用于世界的 action，而不是事后 covariate。':'干预身份作为作用于世界的动作输入模型，不再作为事后协变量处理。',
'这里“世界最好”的标准｜</strong>不是某一个行为 benchmark 的 F-score 最高，而是：最完整的小鼠社会状态覆盖 + held-animal / held-lab transfer + multi-step rollout + 长时程 relationship memory + neural alignment + intervention-aware counterfactual prediction。':'这里“世界最好”的标准｜</strong>评价重点包括：完整的小鼠社会状态覆盖、跨动物与跨实验室迁移、多步轨迹预测、长时程关系记忆、神经状态对齐，以及能够显式处理干预的反事实预测。',
}
for old,new in reps.items():
    if old not in s:
        raise RuntimeError("missing target: "+old[:40])
    s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
print("removed banned contrast phrasing introduced by rebase")
