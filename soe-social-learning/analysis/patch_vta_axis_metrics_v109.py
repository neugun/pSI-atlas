# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPL={
"index.html":[
("Pre-outcome VTA activity follows the SLM sampling policy (effect=.810, P=.0469), while generic Q/RPE is near zero at this stage.","Pre-outcome VTA activity follows the SLM sampling policy (rank-biserial=.810, P=.0469), while generic Q/RPE is near zero at this stage."),
("Middle APE remains related to learning (effect=.667, P=.0416) after controls for choice persistence and classical Q errors.","Across animals, middle APE coupling scales with learning strength (Spearman ρ=.667 vs SRI; exact one-sided permutation P=.0416) after controls for choice persistence and classical Q errors."),
("Post-outcome RPE is supported (effect=.867, P=.0195); generic Q/RPE also works here, so the post period alone cannot identify the full mechanism.","Post-outcome RPE is supported (rank-biserial=.867, P=.0195); generic Q/RPE also works here, so the post period alone cannot identify the full mechanism."),
('<p class="small">Rows are candidate computational-signal families, not a second leaderboard of complete behavioral agents. Effect definitions follow the frozen axis-specific authority: Early tests policy-linked prediction gain, Middle tests learner-linked APE/error coupling, and Post tests outcome-stage prediction gain.</p>','<p class="small">Rows are candidate computational-signal families, not a second leaderboard of complete behavioral agents. Effect definitions follow the frozen axis-specific authority: Early tests policy-linked prediction gain, Middle tests learner-linked APE/error coupling, and Post tests outcome-stage prediction gain. <strong>Effect scales are axis-specific:</strong> Early and Post report rank-biserial signed-rank effect sizes, whereas Middle reports the Spearman ρ linking each animal\'s coupling to SRI; their numerical magnitudes are not directly comparable across columns.</p>')
],
"index-zh.html":[
("结果前 VTA 信号与 SLM 的采样策略一致，效应=.810，P=.0469；通用 Q/RPE 在这一阶段接近零。","结果前 VTA 信号与 SLM 的采样策略一致，秩双列相关=.810，P=.0469；通用 Q/RPE 在这一阶段接近零。"),
("中段 APE 与学习程度保持关系，效应=.667，P=.0416；控制选择惯性和经典 Q 误差后仍保留。","中段 APE 的逐动物耦合强度与学习程度保持关系（Spearman ρ=.667，与 SRI 的精确单侧置换 P=.0416）；控制选择惯性和经典 Q 误差后仍保留。"),
("结果后 RPE 得到支持，效应=.867，P=.0195；此时普通 Q/RPE 也有效，因此这一阶段单独看不足以区分完整机制。","结果后 RPE 得到支持，秩双列相关=.867，P=.0195；此时普通 Q/RPE 也有效，因此这一阶段单独看不足以区分完整机制。"),
('<p class="small">这里每一行代表候选计算信号家族，和上方“完整行为系统预测排名”属于不同问题。效应量沿冻结的时间轴定义读取：早期检验采样策略相关预测增益，中段检验与学习强度相关的 APE/误差耦合，结果后检验结果期预测增益。</p>','<p class="small">这里每一行代表候选计算信号家族，和上方“完整行为系统预测排名”属于不同问题。效应量沿冻结的时间轴定义读取：早期检验采样策略相关预测增益，中段检验与学习强度相关的 APE/误差耦合，结果后检验结果期预测增益。<strong>三列效应量使用不同统计尺度：</strong>早期和结果后报告秩双列效应量，中段报告逐动物耦合强度与 SRI 的 Spearman ρ，因此数值大小不做跨列比较。</p>')
]
}
for fn,pairs in REPL.items():
 p=ROOT/fn; s=p.read_text(encoding="utf-8"); changed=0
 for old,new in pairs:
  if new in s: continue
  if old not in s: raise RuntimeError("missing patch anchor in %s: %s"%(fn,old[:80]))
  s=s.replace(old,new,1); changed+=1
 p.write_text(s,encoding="utf-8"); print(fn,"changed",changed)
