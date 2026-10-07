# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def rep(s,old,new,label):
    if old not in s:
        raise RuntimeError("missing anchor: "+label)
    return s.replace(old,new,1)

# ---------- Chinese ----------
p=ROOT/"index-zh.html"
s=p.read_text(encoding="utf-8")

s=rep(s,
'<div class="section-head"><div><div class="section-kicker">神经实现</div><h2>VTA 多巴胺沿着 SLM 的计算顺序展开：先决定是否采样社会信息，再处理采样误差，最后根据结果更新</h2></div><p>这里先保留原来的核心发现，再用 新方法 的真实行为时长读出做同问题复现，随后用原始时间过程解释这些模型效应在神经信号中何时出现、持续多久。</p></div>',
'<div class="section-head"><div><div class="section-kicker">神经实现</div><h2>VTA 多巴胺沿着 SLM 的计算顺序展开：先决定是否采样社会信息，再处理采样误差，最后根据结果更新</h2></div><p>这里先保留原来的核心发现；随后把原始 FP 重新重建成 observation-bout DA，在完全相同的 Early/Middle 分析合同下做严格复现；结果期再用固定 0–6 秒与真实行动时长两种读出交叉验证，最后用 PSTH 解释这些效应的真实时间形状。</p></div>',
"zh section head")

old='<div class="section-kicker" style="margin-top:28px">关键复现｜只改变光纤信号转成多巴胺数值的方法，再看原来的结果期 SLM 结论是否保留</div>'
new='''<div class="section-kicker" style="margin-top:28px">最重要的复现｜Early / Middle 保持原分析合同不变，只把 observation-bout DA 从原始 FP 重新重建</div>
<div class="reader-guide"><div class="reader-step"><b>为什么做</b><span>最关键的问题不是换一个近似统计再问一次，而是检验原来的 Early policy 和 Middle APE 结果是否依赖旧的 FP→DA 数值。</span></div><div class="reader-step"><b>怎么做</b><span>从 9 只动物各自的原始连续 FP 信号重新计算 observation-bout DA；事件划分、session 阶段、行为 latent、协变量、交叉验证和动物级统计全部沿用原分析。新旧 observation DA 共 1,041 个有效事件，逐动物相关中位 r=.9994。</span></div><div class="reader-step"><b>结论</b><span>Early policy 和 Middle APE 两个核心结果都原样复现；不只组水平 P 值一致，逐动物效应排序也完全一致。</span></div></div>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_VTA_early_middle_raw_recon_replication_v102.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_VTA_early_middle_raw_recon_replication_v102_mobile.png"/><img alt="原始 FP 重建后 Early policy 与 Middle APE 的严格复现" loading="lazy" src="assets/SOE_VTA_early_middle_raw_recon_replication_v102.png"/></picture></a><figcaption><strong>Early / Middle 的严格 raw-reconstruction 复现。</strong>A，重新从原始 FP 计算的 observation-bout DA 与旧读出在 9 只动物、1,041 个事件中几乎一致（逐动物相关中位 r=.9994）。B，Early policy 使用同一 5-fold 动物内 block-CV 与同一行为 latent，仍为 5/6 动物改善，rank-biserial=.810，P=.0469；旧值与新值的逐动物 gain 排序 ρ=1.0。C，Middle APE 使用同一中段、同一 residualization 与 SRI 检验，仍为 ρ=.667，exact one-sided permutation P=.0416；逐动物 APE coupling 的新旧排序同样 ρ=1.0。D，总结三层跨方法一致性。</figcaption></figure>
<div class="callout"><strong>这一层回答的是最重要的复现问题｜</strong>采样策略和 APE 的神经结果不是换了一个分析问题后“方向差不多”，而是在保持原 estimand 与统计合同不变时，用重新从 raw FP 得到的 DA 仍得到同一结论。Early 与 Middle 因此可以继续作为 SLM 区分经典结果期 RPE 的关键时间证据。</div>
<div class="section-kicker" style="margin-top:28px">第二层复现｜结果期再换成真实行动时长读出，检验社会归因与 RPE 结构</div>'''
s=rep(s,old,new,"zh primary replication")

s=rep(s,
'<div class="callout"><strong>早期和中段为什么不能直接用“整个观察片段”替代｜</strong>新方法得到的完整观察片段平均值会把事件内部时间结构压平。用整段观察平均后，原来的结果前采样策略关系没有重现（6 只动物，P=.438），中段 APE×SRI 也没有重现（8 只动物，ρ=−.119，P=.779）。这说明结果期可以做严格的同事件双读出复现；结果前和中段需要保留时间定位，整个观察片段的平均值会稀释短暂计算。下面的围事件时间曲线因此承担一个关键任务：把模型统计量重新展开到真实时间轴。</div>',
'<div class="bio-logic"><strong>Whole-bout 检查现在只作为边界/敏感性分析，不再当作复现检验｜</strong>先前把整段 observation-bout DA 与 policy 或 APE 做简化相关时得到 Early P=.438、Middle ρ=−.119（P=.779）。但这一步同时改变了神经 readout 的汇总方式和统计 estimand，不能据此说原 Early/Middle 结果“没有复现”。上面的 raw-reconstruction 严格镜像才回答复现问题；whole-bout 阴性结果只说明把原模型合同换成整段平均的简化相关会丢失判别力。</div>',
"zh whole bout boundary")

s=rep(s,
'<div class="callout"><strong>VTA 部分的整合结论｜</strong>行为数据先定义了 SLM 的计算坐标；原始 VTA 分析把采样策略、APE 和结果后更新放在正确的事件内时间位置。新方法 的真实行为时长读出进一步说明，行为中学到的社会归因和标量 RPE 结构并不依赖固定 0–6 秒这一种 多巴胺量化。围事件时间曲线 则解释了两种读出差异的时间来源，并显示有效社会观察与上一结果形成的内部状态会延续到下一次采样。由此得到一条连续神经计算链：<strong>决定是否观察 → 获取社会信息 → 处理采样误差 → 根据结果更新 → 改变下一次社会采样。</strong></div>',
'<div class="callout"><strong>VTA 部分的整合结论｜</strong>行为数据先定义 SLM 的计算坐标，原始 VTA 分析再把采样策略、APE 和结果后更新放到正确的事件内时间位置。最关键的 raw-FP 重建保持 Early/Middle 原分析合同不变，得到同一个 Early policy P=.0469 和 Middle APE×SRI ρ=.667、P=.0416；结果期的真实行动时长读出又独立保留了社会归因与标量 RPE 的主要结构。PSTH 最后解释这些计算何时出现以及为什么不同窗口灵敏度不同。由此得到一条连续神经计算链：<strong>决定是否观察 → 获取社会信息 → 处理采样误差 → 根据结果更新 → 改变下一次社会采样。</strong></div>',
"zh integrated")

s=rep(s,
'<div class="download-card"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">原始 VTA 三阶段 authority</a><p>采样策略、APE、结果后更新与竞争模型的逐阶段结果。</p></div>',
'<div class="download-card"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">原始 VTA 三阶段 authority</a><p>采样策略、APE、结果后更新与竞争模型的逐阶段结果。</p></div>\n<div class="download-card"><a href="data/SOE_VTA_EARLY_MIDDLE_RAW_RECON_SUMMARY_v102.csv">Early/Middle raw-FP 严格复现</a><p>保持原分析合同不变，仅重建 observation-bout DA；包含 Early policy、Middle APE 与逐动物跨方法一致性。</p></div>',
"zh add download")
s=rep(s,
'<div class="download-card"><a href="data/SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv">完整观察片段镜像检验</a><p>完整观察片段平均会稀释结果前和中段的短暂计算。</p></div>',
'<div class="download-card"><a href="data/SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv">Whole-bout 边界检查</a><p>简化 whole-bout 相关改变了 estimand，只用于说明这种简化分析会丢失判别力，不作为复现结论。</p></div>',
"zh boundary card")

p.write_text(s,encoding="utf-8")

# ---------- English ----------
p=ROOT/"index.html"
s=p.read_text(encoding="utf-8")
s=rep(s,
'<div class="section-head"><div><div class="section-kicker">Neural implementation</div><h2>VTA dopamine unfolds in the order predicted by SLM: decide whether to sample, evaluate the sampling action, then update from the outcome</h2></div><p>The section first preserves the original VTA–SLM result, then asks whether the same outcome-stage conclusions survive the Codex real-bout FP-to-DA readout, and finally uses time-resolved PSTHs to reveal when each signal appears.</p></div>',
'<div class="section-head"><div><div class="section-kicker">Neural implementation</div><h2>VTA dopamine unfolds in the order predicted by SLM: decide whether to sample, evaluate the sampling action, then update from the outcome</h2></div><p>The section first preserves the original VTA–SLM result, then reconstructs observation-bout DA directly from raw FP and repeats the original Early/Middle analysis contracts, next cross-validates outcome-stage conclusions with fixed and real-bout readouts, and finally uses PSTHs to expose the underlying time course.</p></div>',
"en section head")

old='<div class="section-kicker" style="margin-top:28px">Key replication | Change only the FP-to-DA readout and repeat the outcome-stage SLM tests</div>'
new='''<div class="section-kicker" style="margin-top:28px">Primary replication | Keep the original Early/Middle analysis contracts and rebuild observation-bout DA from raw FP</div>
<div class="reader-guide"><div class="reader-step"><b>Why</b><span>The decisive robustness question is not whether a nearby statistic has the same sign, but whether the original Early policy and Middle APE conclusions survive when only the FP→DA reconstruction is changed.</span></div><div class="reader-step"><b>How</b><span>Observation-bout DA was rebuilt directly from each animal's continuous raw FP signal. Event selection, session epoch, behavioral latents, nuisance covariates, cross-validation and animal-level inference were otherwise left unchanged. Across 1,041 valid events from 9 animals, the old and reconstructed observation DA measures had a median within-animal correlation of r=.9994.</span></div><div class="reader-step"><b>Result</b><span>Both core Early/Middle results reproduce exactly at the inferential level, and the animal-level effect rankings are unchanged.</span></div></div>
<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_VTA_early_middle_raw_recon_replication_v102.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_VTA_early_middle_raw_recon_replication_v102_mobile.png"/><img alt="Strict raw-FP reconstruction replication of Early policy and Middle APE" loading="lazy" src="assets/SOE_VTA_early_middle_raw_recon_replication_v102.png"/></picture></a><figcaption><strong>Strict raw-reconstruction replication of Early and Middle VTA results.</strong>A, raw-FP reconstruction closely matches the legacy observation-bout DA across 9 animals and 1,041 events (median within-animal r=.9994). B, with the identical 5-fold within-animal block-CV and behavioral policy latent, Early policy again improves prediction in 5/6 animals (rank-biserial=.810, P=.0469); old versus reconstructed animal-level gains have ρ=1.0. C, with the identical middle-session window, residualization and SRI test, APE coupling again scales with learning strength (ρ=.667, exact one-sided permutation P=.0416); old versus reconstructed animal-level APE effects also have ρ=1.0. D, the three cross-method agreement checks.</figcaption></figure>
<div class="callout"><strong>This is the key replication layer.</strong> Early policy and Middle APE are not merely directionally similar under a different analysis. When the original estimands and statistical contracts are held fixed and DA is rebuilt from raw FP, the original inferences are retained. These stages therefore remain the temporally discriminative evidence that extends the model beyond a generic post-outcome RPE account.</div>
<div class="section-kicker" style="margin-top:28px">Second replication | At outcome, change the readout to real action-bout DA</div>'''
s=rep(s,old,new,"en primary replication")

s=rep(s,
'<div class="callout"><strong>Why whole-observation-bout averaging cannot replace the early/middle analyses.</strong> Averaging the entire observation bout removes temporal localization. The old early-policy relationship is not recovered by the whole-bout readout (6 animals, P=.438), and the middle APE×SRI relationship is also lost (8 animals, ρ=−.119, P=.779). Outcome-stage tests permit a strict same-event dual-readout replication; early and middle computations require time-resolved localization.</div>',
'<div class="bio-logic"><strong>The whole-bout check is now treated only as a boundary/sensitivity analysis, not a replication test.</strong> A simplified whole-observation-bout correlation gave Early P=.438 and Middle ρ=−.119 (P=.779), but that analysis changed both the neural summary and the statistical estimand. It therefore cannot be interpreted as a failure to replicate the original Early/Middle findings. The raw-reconstruction mirror above is the appropriate replication test; the whole-bout result only shows that a simplified bout-average association loses discriminative power.</div>',
"en whole bout")

s=rep(s,
'<div class="callout"><strong>Integrated VTA conclusion.</strong> Behavior first defines the SLM coordinates; the original VTA analysis places policy, APE and post-outcome updating at the correct within-event times. The Codex real-bout readout independently preserves behavior-derived social credit and the scalar-RPE structure, showing that these mappings are not artifacts of the fixed 0–6 s definition. PSTHs reveal why sensitivity differs across readouts and show that effective social observation and outcome history shape a VTA state that carries into future sampling. The resulting neural sequence is <strong>decide whether to observe → acquire social information → evaluate the sampling action → update from the outcome → alter the next social sample.</strong></div>',
'<div class="callout"><strong>Integrated VTA conclusion.</strong> Behavior first defines the SLM coordinates and the original VTA analysis places policy, APE and post-outcome updating at the appropriate within-event times. The most direct raw-FP reconstruction keeps the original Early/Middle analysis contracts fixed and returns the same Early policy P=.0469 and Middle APE×SRI ρ=.667, P=.0416. The outcome-stage real-action-bout readout independently preserves the main social-credit and scalar-RPE structure. PSTHs then explain when these computations emerge and why integration windows differ in sensitivity. The resulting neural sequence is <strong>decide whether to observe → acquire social information → evaluate the sampling action → update from the outcome → alter the next social sample.</strong></div>',
"en integrated")

s=rep(s,
'<div class="download-card"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">Original VTA temporal authority</a><p>Sampling policy, APE, post-outcome updating and model-family controls.</p></div>',
'<div class="download-card"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">Original VTA temporal authority</a><p>Sampling policy, APE, post-outcome updating and model-family controls.</p></div>\n<div class="download-card"><a href="data/SOE_VTA_EARLY_MIDDLE_RAW_RECON_SUMMARY_v102.csv">Early/Middle raw-FP strict replication</a><p>Original analysis contracts held fixed while observation-bout DA is rebuilt from raw FP.</p></div>',
"en add download")
s=rep(s,
'<div class="download-card"><a href="data/SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv">Whole-observation-bout mirror</a><p>Shows dilution of temporally localized early/middle computations by whole-bout averaging.</p></div>',
'<div class="download-card"><a href="data/SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv">Whole-bout boundary check</a><p>A simplified association that changes the estimand; retained as a sensitivity check, not as the Early/Middle replication test.</p></div>',
"en boundary card")

p.write_text(s,encoding="utf-8")

# ---------- audit document ----------
p=ROOT/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md"
s=p.read_text(encoding="utf-8")
newsec='''### 6.2 Early / middle：保持原分析合同不变的 raw-FP 严格复现

Early / middle 的关键复现不能把原来的模型统计改成一个简化 whole-bout correlation。这里重新从 9 只动物各自的连续 raw FP 中计算 observation-bout DA，同时保持原分析的事件、session 阶段、行为 latent、协变量、交叉验证和动物级统计不变。

首先验证新旧 DA 是否确实对应同一神经量：
- 9 只动物、1,041 个有效 observation-bout 事件。
- 新旧 observation DA 的逐动物相关为 .9983–.99999，中位 r=.9994。
- 因而下面比较主要反映 FP→DA 重建方式，而不是事件集合或行为模型变化。

Early policy：
- 原始结果：5/6 动物改善，median MSE gain=1.94%，rank-biserial=.810，P=.046875。
- raw-FP 重建后：仍为 5/6 动物改善，median gain=2.82%，rank-biserial=.810，P=.046875。
- 新旧逐动物 gain 的秩相关 ρ=1.0。

Middle APE：
- 原始 authority：8 只动物，APE coupling 与 SRI 的关系 ρ=.667，exact one-sided permutation P=.041566。
- raw-FP 重建后：ρ=.667，exact one-sided permutation P=.041566。
- 新旧逐动物 APE coupling 的秩相关 ρ=1.0。

因此 Early policy 与 Middle APE 不只是“方向类似”，而是在保持原 estimand 和统计合同不变时对 raw-FP 重建完全保留了主要推断。这一层是 Early/Middle 的正式复现。

来源：data/SOE_VTA_OBSBOUT_RAW_RECON_AUDIT_v102.csv；data/SOE_VTA_EARLY_POLICY_RAW_RECON_v102.csv；data/SOE_VTA_MIDDLE_APE_RAW_RECON_v102.csv；data/SOE_VTA_EARLY_MIDDLE_RAW_RECON_SUMMARY_v102.csv。

### 6.3 Whole-observation-bout 简化相关只作为边界/敏感性检查

先前 whole-bout mirror 得到：
- Early 简化 policy association：P=.438。
- Middle 简化 APE×SRI：ρ=−.119，P=.779。

但这一步同时改变了神经汇总方式和统计 estimand，因此不能再表述为“Early/Middle 没有复现”，也不能把阴性结果直接解释成时间稀释的证据。它只说明：如果把原来的交叉验证/残差化模型合同换成整段平均后的简化相关，判别力会丢失。

PSTH 和 time-resolved 分析仍然用于解释信号在事件内部何时出现；复现结论本身以上面的同合同 raw-FP mirror 为准。

来源：data/SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv。

'''
pattern=r'### 6\.2 Early / middle 不能用整个 observation bout 的平均值直接替代\n.*?(?=## 7\.)'
if not re.search(pattern,s,flags=re.S):
    raise RuntimeError("missing audit 6.2 anchor")
s=re.sub(pattern,newsec,s,count=1,flags=re.S)
p.write_text(s,encoding="utf-8")
print("patched v102 pages + audit")
