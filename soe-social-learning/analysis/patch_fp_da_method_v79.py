# -*- coding: utf-8 -*-
from pathlib import Path
import re, pandas as pd

R=Path(__file__).resolve().parents[1]
RAW=R/"data"/"fp_da_common_event_v1"

ZH='''<details id="vta-fp-da-method-v77"><summary>展开：同一批 FP 信号用两种方式计算多巴胺，结论是否仍然成立？</summary><div class="detail-body">
<div class="bio-logic"><strong>固定结果后窗口｜</strong>Post06 对每个事件都取结果后 0–6 s，计算多巴胺面积/秒。所有事件使用相同时间范围，更容易保留行动结束后继续存在的结果评估和教学更新。</div>
<div class="bio-logic"><strong>真实行动时长｜</strong>ActionBout 从真实行动片段起点积分到真实终点，再除以行动片段时长；持续时间 &lt;0.05 s 的近零片段严格排除。这个读出更集中于真实行为执行期间的多巴胺。</div>
<div class="cards-3">
<div class="card good"><div class="metric-label">先固定完全相同的事件再比较</div><div class="metric">1,371 个共同事件 · 9 只动物</div><p>两种多巴胺读出在每只动物中都正相关，Spearman ρ=.520–.944，中位数 .785。两种算法主要捕获同一底层多巴胺过程，同时对事件内部不同时间段赋予不同权重。</p></div>
<div class="card info"><div class="metric-label">结果后误差项在固定窗中达到更强的统计证据</div><div class="metric">0–6 s：|RPE| 8/9，P=.0391</div><p>同一批事件中，真实 bout 时长读出的 |RPE| 仍有 7/9 动物方向改善，但 P=.164。更关键的是 7/9 动物在两种定义下同时改善；按各自基线归一化后，两种读出的增益差异本身不显著（P=.164）。</p></div>
<div class="card violet"><div class="metric-label">行为学到的社会结果归因跨两种算法重复</div><div class="metric">两种读出同时为正：7/9</div><p>行为选出的被动结果归因在 ActionBout 中相对固定 0.75/1.0 均为 9/9 更好（P=.00391）；在 0–6 s 中为 7/9（P=.0273/.0391）。同一动物的归因优势跨算法保持排序：ρ=.733（P=.0246）和 ρ=.800（P=.00963）。</p></div>
</div>
<div class="callout"><strong>方法学结论｜</strong>最强结果是方法无关的：行为中学到的社会结果归因在两种 FP→DA 定义下都能直接迁移到 VTA，而且同一动物的模型增益跨算法保持一致。固定 0–6 s 对部分结果后误差项达到更强的单独统计证据，但当前直接比较不足以把两种窗口解释成两套不同机制。积分窗口改变灵敏度，没有改变 SLM 行为→神经映射的主方向。</div>
<div class="download-grid"><div class="download-card"><a href="data/SLM_FP_DA_METHOD_AUDIT_v1.csv">FP→DA 双定义权威结果表</a><p>共同事件、逐动物方向、效应量和两套多巴胺定义的并排统计。</p></div><div class="download-card"><a href="docs/SOE_FP_DA_METHOD_AUDIT_v1_20261006.md">FP→DA 方法审计</a><p>固定 0–6 s 与真实行动时长怎样计算，以及哪些 SLM 结论跨方法成立。</p></div></div>
</div></details>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_DA_cross_readout_consensus_v78.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_DA_cross_readout_consensus_v78_mobile.png"/><img alt="同一批 fiber photometry 事件的两种多巴胺量化方法比较" loading="lazy" src="assets/SOE_FP_DA_cross_readout_consensus_v78.png"/></picture></a><figcaption><strong>同一批 1,371 个事件上的 FP→DA 双算法审计。</strong>A，两种多巴胺数值在每只动物中高度相关。B，行动者 |RPE| 在两种算法下有 7/9 动物同时改善；固定 0–6 s 的单独检验更强，但两种读出的归一化增益差异不显著。C–D，行为数据独立选出的被动结果归因相对固定 0.75/1.0 权重，在两种多巴胺算法中有 7/9 动物同时受益，而且同一动物的模型优势跨算法保持排序（ρ=.733/.800）。这说明主要行为→神经映射不依赖人为选择一个 FP 积分窗口。</figcaption></figure>
'''

EN='''<details id="vta-fp-da-method-v77"><summary>Expand: do the conclusions survive two different FP-to-dopamine readouts?</summary><div class="detail-body">
<div class="bio-logic"><strong>Fixed post-outcome window.</strong> Post06 uses the same 0–6 s window after every event and reports dopamine area per second, retaining activity that can persist after the action bout ends.</div>
<div class="bio-logic"><strong>Actual action-bout duration.</strong> ActionBout integrates from the real action-bout onset to its real offset and divides by bout duration; near-zero bouts &lt;0.05 s are excluded. This readout concentrates on dopamine expressed during the executed behavior.</div>
<div class="cards-3">
<div class="card good"><div class="metric-label">The comparison uses exactly the same events</div><div class="metric">1,371 common events · 9 animals</div><p>The two dopamine readouts are positively correlated in every animal (Spearman ρ=.520–.944; median .785), indicating a shared underlying process with different temporal weighting.</p></div>
<div class="card info"><div class="metric-label">Post-outcome error reaches stronger evidence in the fixed window</div><div class="metric">0–6 s: |RPE| 8/9, P=.0391</div><p>On the same events, bout-duration |RPE| remains positive in 7/9 animals but P=.164. Seven of nine animals improve under both definitions, and the baseline-normalized gain difference between readouts is itself not significant (P=.164).</p></div>
<div class="card violet"><div class="metric-label">Behavior-derived social credit replicates across both readouts</div><div class="metric">Positive under both: 7/9</div><p>Behavior-selected Passive credit beats fixed .75/1.0 in 9/9 animals for ActionBout (P=.00391) and 7/9 for 0–6 s (P=.0273/.0391). Animal-level advantage is concordant across readouts: ρ=.733 (P=.0246) and ρ=.800 (P=.00963).</p></div>
</div>
<div class="callout"><strong>Methodological conclusion.</strong> The strongest result is method-invariant: behavior-derived social credit transfers to VTA under both FP-to-dopamine definitions, with concordant animal-level model benefit. The fixed 0–6 s window reaches stronger within-readout evidence for some post-outcome error terms, but direct comparisons do not justify treating the two windows as different mechanisms. Window choice changes sensitivity without changing the core SLM behavior-to-neural mapping.</div>
<div class="download-grid"><div class="download-card"><a href="data/SLM_FP_DA_METHOD_AUDIT_v1.csv">FP-to-DA dual-readout authority</a><p>Common-event definitions, directions, effect sizes and paired statistics.</p></div><div class="download-card"><a href="docs/SOE_FP_DA_METHOD_AUDIT_v1_20261006.md">FP-to-DA method audit</a><p>Fixed 0–6 s versus actual-bout duration, and which SLM conclusions survive both.</p></div></div>
</div></details>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_DA_cross_readout_consensus_v78.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_DA_cross_readout_consensus_v78_mobile.png"/><img alt="Two dopamine quantifications on the same fiber-photometry events" loading="lazy" src="assets/SOE_FP_DA_cross_readout_consensus_v78.png"/></picture></a><figcaption><strong>Two FP-to-dopamine definitions on the same 1,371 events.</strong>A, the two values are strongly correlated within each animal. B, actor |RPE| improves both readouts in 7/9 animals; the fixed 0–6 s test is stronger on its own, while the normalized between-readout gain difference is not significant. C–D, Passive credit selected from behavior alone beats fixed .75/1.0 weights under both dopamine definitions in 7/9 animals simultaneously, with concordant animal-level gain ranks across methods (ρ=.733/.800). The core behavior-to-neural mapping therefore does not depend on choosing one FP integration window.</figcaption></figure>
'''

def patch_page(fn,block,zh=False):
    p=R/fn; s=p.read_text(encoding="utf-8")
    s=re.sub(r'<details id="vta-codex-legacy-v75">.*?</details>\s*','',s,count=1,flags=re.S)
    s=re.sub(r'<details id="vta-fp-da-method-v77">.*?</details>\s*<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_DA_cross_readout_consensus_v78\.png".*?</figure>\s*','',s,count=1,flags=re.S)
    anchor='<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_DA_temporal_logic_v67.png"'
    if anchor not in s: raise RuntimeError("anchor missing "+fn)
    s=s.replace(anchor,block+anchor,1)
    if zh:
        s=s.replace('秒级信息需求、RPE/APE 双通路、VTA 时间轴、误差表示、行为→神经迁移与旧 Codex 审计。','秒级信息需求、RPE/APE 双通路、VTA 时间轴、误差表示、行为→神经迁移与 FP→DA 双定义稳健性。')
    else:
        s=s.replace('Fast information demand, RPE/APE dual behavior, VTA timing, error representation, behavior-to-neural transfer and the legacy Codex audit.','Fast information demand, RPE/APE dual behavior, VTA timing, error representation, behavior-to-neural transfer and FP-to-dopamine robustness.')
    p.write_text(s,encoding="utf-8")

patch_page("index-zh.html",ZH,True); patch_page("index.html",EN,False)

actor=pd.read_csv(RAW/"actor_common_event_contrasts.csv")
credit=pd.read_csv(RAW/"passive_credit_common_event_contrasts.csv")
agree=pd.read_csv(RAW/"target_agreement_per_animal.csv")
rows=[
["definition","Post06","固定 0–6 s 结果后窗口；AUC/秒",1371,9,"","","","共同时间窗"],
["definition","ActionBout","真实 action-bout 时长；AUC/真实时长；排除 <0.05 s",1371,9,"","","","真实行为执行期"],
["agreement","both","逐动物两种 DA readout 相关",1371,9,"positive",f"median rho={agree.spearman_rho.median():.3f}; range={agree.spearman_rho.min():.3f}-{agree.spearman_rho.max():.3f}","","同一底层信号，不同时间加权"],
["cross_readout","both","actor |RPE| 两种 readout 同时为正",1371,9,"7_of_9","Post06 median +1.761%; ActionBout +0.689%","0.164062","方向跨算法保留；readout 间归一化差异不显著"],
["cross_readout","both","behavior-selected credit vs fixed 0.75",1371,9,"7_of_9_both","gain-rank rho=0.733; rho P=0.0246","0.097656","行为→神经归因映射跨算法重复"],
["cross_readout","both","behavior-selected credit vs fixed 1.0",1371,9,"7_of_9_both","gain-rank rho=0.800; rho P=0.00963","0.097656","行为→神经归因映射跨算法重复"],
]
pd.DataFrame(rows,columns=["analysis_scope","da_definition","test","n_events","n_animals","direction","effect","p","interpretation"]).to_csv(R/"data"/"SLM_FP_DA_METHOD_AUDIT_v1.csv",index=False)

p=R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv"; m=pd.read_csv(p)
m=m[m.domain.astype(str)!="legacy_codex"].copy()
extra=pd.DataFrame([
["fp_readout_robustness","Passive_credit_cross_readout_fixed075","gain_rank_spearman_rho",0.7333333,9,0.0245542,"被动结果归因的神经模型优势在两种 FP→DA 定义间保持动物排序；7/9 两种定义同时为正","SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv"],
["fp_readout_robustness","Passive_credit_cross_readout_fixed100","gain_rank_spearman_rho",0.8,9,0.0096279,"被动结果归因的神经模型优势在两种 FP→DA 定义间保持动物排序；7/9 两种定义同时为正","SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv"],
["fp_readout_robustness","Actor_absRPE_positive_both","animals_positive_in_both","7_of_9",9,"","actor |RPE| 在固定 0–6 s 与真实 bout 时长两种定义中方向同时为正","SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv"],
],columns=m.columns)
m=pd.concat([m,extra],ignore_index=True); m.to_csv(p,index=False)

p=R/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md"; d=p.read_text(encoding="utf-8")
newsec='''## 6. Fiber photometry → 多巴胺数值的双定义稳健性

这里比较的是同一条 FP 信号怎样变成事件级多巴胺数值，而非另一套 RPE/APE 模型。

- 固定 0–6 s：每个事件统一取结果后 0–6 s 的多巴胺 AUC/秒。
- 真实 bout 时长：从行动起点积分到真实 bout 终点，再除以真实 bout 时长；<0.05 s 的近零 bout 排除。
- 公平比较只保留两种定义都有效的 1,371 个事件、9 只动物。
- 两种 DA 数值逐动物相关 ρ=.520–.944，中位数 .785。
- behavior-selected Passive credit 相对 fixed 0.75/1.0 在两种定义中均保持优势；同一动物的优势跨算法相关分别 ρ=.733（P=.0246）和 .800（P=.00963）。
- actor |RPE| 有 7/9 动物在两种定义下同时改善。固定 0–6 s 单独统计更强，但 readout 间归一化增益差异 P=.164。

因此最重要的结论是：**SLM 的行为→神经归因映射不依赖人为挑选一个 FP 积分窗口。** 两种窗口改变灵敏度，但没有改变主方向。

来源：data/SLM_FP_DA_METHOD_AUDIT_v1.csv；data/SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv。

'''
d=re.sub(r'## 6\. 旧 Codex 3\.2/3\.3 的两条多巴胺计算路线\n.*?(?=## 7\.)',newsec,d,flags=re.S)
p.write_text(d,encoding="utf-8")
print("patched pages, authority, and audit")
