# -*- coding: utf-8 -*-
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def replace_once(path, old, new):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    if new in s:
        print(path, "already current")
        return
    if old not in s:
        raise RuntimeError(f"missing anchor in {path}: {old[:180]}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print(path, "updated")

# English VTA section
replace_once("index.html",
'<div class="section-head"><div><div class="section-kicker">Neural implementation</div><h2>VTA dopamine unfolds in the order predicted by SLM: decide whether to sample, evaluate the sampling action, then update from the outcome</h2></div><p>The section first preserves the original VTA–SLM result, then reconstructs observation-bout DA directly from raw FP and repeats the original Early/Middle analysis contracts, next cross-validates outcome-stage conclusions with fixed and real-bout readouts, and finally uses PSTHs to expose the underlying time course.</p></div>',
'<div class="section-head"><div><div class="section-kicker">Neural implementation</div><h2>VTA dopamine traces a learning sequence from sampling policy to action-prediction error to outcome-specific credit</h2></div><p>Early and Middle keep the original inferential contracts and are rebuilt directly from raw FP. For Post, the main mechanistic display uses bout-matched real-action DA because it aligns the neural integration window to the actual outcome/action episode; the frozen 0–6 s result stays visible as the original statistical reference. Contingent JAWS then asks whether VTA is required for the corresponding credit-assignment branch.</p></div>')

replace_once("index.html",
'<div class="reader-guide"><div class="reader-step"><b>Why</b><span>If SLM captures the neural computation, each variable should appear at the time when it can be used.</span></div><div class="reader-step"><b>How</b><span>We separately test pre-outcome sampling policy, middle APE, and post-outcome updating against Q-learning, choice persistence and flexible alternatives.</span></div><div class="reader-step"><b>Result</b><span>SLM is supported on all three pre-specified temporal axes; generic Q/RPE is mainly supported after the outcome.</span></div></div>',
'<div class="reader-guide"><div class="reader-step"><b>Why</b><span>If SLM captures the neural computation, each variable should appear at the time when it can be used.</span></div><div class="reader-step"><b>How</b><span>We test Early sampling policy and Middle APE with the frozen original contracts, then test Post credit assignment with bout-matched DA while retaining the fixed-window analysis as a locked reference.</span></div><div class="reader-step"><b>Result</b><span>Early policy and Middle APE survive raw-FP reconstruction; Post real-bout DA preferentially supports behavior-derived social credit; contingent JAWS then suppresses the successful-outcome credit-update branch.</span></div></div>')

replace_once("index.html",
'''<div class="cards-3">
<div class="card good"><div class="metric-label">Before outcome: is social information worth sampling?</div><div class="metric">Sampling policy</div><p>Pre-outcome VTA activity follows the SLM sampling policy (rank-biserial=.810, P=.0469), while generic Q/RPE is near zero at this stage.</p></div>
<div class="card info"><div class="metric-label">After sampling, before outcome: how unexpected was the action?</div><div class="metric">APE</div><p>Across animals, middle APE coupling scales with learning strength (Spearman ρ=.667 vs SRI; exact one-sided permutation P=.0416) after controls for choice persistence and classical Q errors.</p></div>
<div class="card violet"><div class="metric-label">After outcome: update from what happened</div><div class="metric">RPE / social credit</div><p>Post-outcome RPE is supported (rank-biserial=.867, P=.0195); generic Q/RPE also works here, so the post period alone cannot identify the full mechanism.</p></div>
</div>''',
'''<div class="cards-4" id="vta-causal-spine-v113">
<div class="card good"><div class="metric-label">Early · decide whether to sample</div><div class="metric">Policy → VTA</div><p>With the frozen Early contract, sampling policy improves DA prediction in 5/6 animals (rank-biserial=.810, P=.0469); raw-FP reconstruction returns the same inference and animal ranking.</p></div>
<div class="card info"><div class="metric-label">Middle · evaluate the sampling action</div><div class="metric">APE × learning strength</div><p>Middle APE coupling scales with social-learning strength across animals (Spearman ρ=.667 vs SRI; exact one-sided permutation P=.0416), again unchanged after raw-FP reconstruction.</p></div>
<div class="card violet"><div class="metric-label">Post · assign outcome-specific social credit</div><div class="metric">Real-bout credit → VTA</div><p>On the same 1,371 events, behavior-selected Passive credit beats fixed 0.75 and fixed 1.0 in 9/9 animals under real-bout DA (both P=.0039). The frozen 0–6 s reference is weaker but directionally concordant.</p></div>
<div class="card good"><div class="metric-label">Causal · is VTA required for teaching?</div><div class="metric">JAWS → credit update</div><p>Contingent JAWS lowers the Active social-credit update in 10/10 animals (P=.001953) and accumulated Active credit in 9/10 (P=.003906). This tests the same credit-assignment branch on successful Active outcomes, rather than the Passive-credit readout used above.</p></div>
</div>''')

replace_once("index.html",
'<figcaption><strong>Original core result: the three SLM computations appear in VTA dopamine in the correct temporal order.</strong>A, pre-outcome sampling policy. B, middle APE. C, post-outcome RPE. D, model-family temporal adjudication. SLM is positive on 3/3 axes; Q/RPE is mainly supported after outcome.</figcaption>',
'<figcaption><strong>Frozen original temporal anchor.</strong>A, pre-outcome sampling policy. B, middle APE. C, the original fixed-window post-outcome RPE result. D, model-family temporal adjudication. This panel is retained unchanged as the historical statistical authority; the current mechanistic Post readout is the bout-matched social-credit analysis shown below.</figcaption>')

replace_once("index.html",
'<div class="callout"><strong>What the original result establishes.</strong> The discriminative information comes from within-event timing. Post-outcome RPE alone is broad; the earlier sampling-policy and APE stages provide the additional mechanistic structure.</div>',
'<div class="callout"><strong>Why the frozen fixed-window result stays visible.</strong> It preserves the original statistical authority and prevents the stronger real-bout credit result from becoming a replacement selected only because its P value is smaller. The current narrative promotes real-bout credit for a biological reason—the neural window is matched to the actual outcome/action bout—while the fixed 0–6 s RPE result remains a locked reference and sensitivity check.</div>')

replace_once("index.html",
'<div class="model-contract" id="vta-signal-zoo-v105"><strong>Why the behavioral model zoo becomes a VTA signal zoo.</strong> The behavioral section compares complete systems for predicting Observe. The neural section freezes computational readouts generated by those systems and asks where they appear on prespecified Early, Middle and Post axes. A family can explain Post dopamine while failing the earlier axes; therefore a successful post-outcome RPE fit does not by itself replace the full SLM sequence.</div>',
'<div class="model-contract" id="vta-signal-zoo-v105"><strong>Why the behavioral model zoo becomes a VTA signal zoo.</strong> The behavioral section compares complete systems for predicting Observe. The neural section freezes computational readouts generated by those systems and asks where they appear on prespecified Early, Middle and Post axes. A family can explain Post dopamine while failing the earlier axes; therefore a successful post-outcome RPE fit does not by itself replace the full SLM sequence. <strong>Authority note:</strong> the Post column below remains the frozen original fixed-window metric; it is kept separate from the newer bout-matched social-credit readout rather than silently relabeled.</div>')

replace_once("index.html",
'<div class="card info"><div class="metric-label">Evidence level 2 · alternative readout</div><div class="metric">Same biology, different integration</div><p>At outcome, fixed 0–6 s DA is replaced by real action-bout DA on the same 1,371 events. This is the stronger readout-robustness test for social credit and scalar RPE.</p></div>',
'<div class="card info"><div class="metric-label">Evidence level 2 · Post-stage mechanistic readout</div><div class="metric">Bout-matched social-credit test</div><p>On the same 1,371 events, real action-bout DA aligns the neural integration window to the actual outcome/action episode and gives the clearest behavior-to-neural test of social credit. The frozen 0–6 s analysis remains visible as the original reference, so the priority is based on biological alignment rather than a smaller P value.</p></div>')

replace_once("index.html",
'<div class="section-kicker" style="margin-top:28px">Alternative-readout robustness | At outcome, change the readout to real action-bout DA</div>',
'<div class="section-kicker" style="margin-top:28px">Post-stage mechanistic readout | use bout-matched DA for social credit, retain fixed 0–6 s as the frozen reference</div>')

replace_once("index.html",
'<div class="reader-guide"><div class="reader-step"><b>Why</b><span>Test whether the SLM-to-VTA result depends on the fixed 0–6 s integration window.</span></div><div class="reader-step"><b>How</b><span>Freeze the same behavior-derived variables and model comparisons, restrict to the same 1,371 events from 9 animals, and replace fixed 0–6 s DA with Codex strict real action-bout AUC/s; near-zero bouts &lt;0.05 s are excluded.</span></div><div class="reader-step"><b>Result</b><span>Behavior-selected credit is directionally robust: versus 0.75 it is significant in both readouts; versus 1.0 the fixed-window result is borderline while real-bout DA is significant. Scalar-RPE structure also survives, with stronger RPE evidence in the fixed post-outcome window.</span></div></div>',
'<div class="reader-guide"><div class="reader-step"><b>Why</b><span>Use biology, rather than significance alone, to choose the main Post readout: real-bout AUC/s isolates the actual action/outcome episode, whereas fixed 0–6 s also includes later evaluation.</span></div><div class="reader-step"><b>How</b><span>Freeze the same behavior-derived variables and model comparisons on the same 1,371 events from 9 animals, then compare real action-bout AUC/s with the original fixed 0–6 s reference; near-zero bouts &lt;0.05 s are excluded.</span></div><div class="reader-step"><b>Result</b><span>Real-bout DA gives the clearest social-credit result: behavior-selected credit beats both fixed 0.75 and 1.0 in 9/9 animals (both P=.0039). The fixed-window results remain concordant but weaker for credit, while classical RPE is more sensitive in the broader fixed window.</span></div></div>')

replace_once("index.html",
'<figcaption><strong>The core outcome-stage SLM-to-VTA mapping survives the Codex real-bout readout.</strong>A, both DA measures are positively correlated within every animal (median ρ=.785). B, RPE-family effects retain the same direction but are weaker in the real-bout readout. C, behavior-selected Passive credit versus fixed 0.75 is positive in 7/9 animals for fixed 0–6 s (P=.0391) and 9/9 for real-bout DA (P=.0039); versus fixed 1.0, the fixed-window comparison is positive but borderline (6/9, P=.0547), whereas real-bout DA is 9/9 (P=.0039). D, outcome-vector PE adds no benefit after scalar RPE under either readout.</figcaption>',
'<figcaption><strong>Primary mechanistic Post readout plus the frozen fixed-window reference.</strong>A, the two DA measures remain positively correlated within every animal (median ρ=.785). B, classical RPE-family effects keep their direction but are generally stronger in the broader fixed window. C, the behavior-derived Passive-credit rule is clearest in real-bout DA: versus fixed 0.75 and fixed 1.0, 9/9 animals favor the selected rule (both P=.0039). The frozen fixed-window results are 7/9 (P=.0391) and 6/9 (P=.0547), respectively. D, outcome-vector PE adds no benefit after scalar RPE under either readout.</figcaption>')

replace_once("index.html",
'<div class="callout"><strong>Integrated VTA conclusion.</strong> Behavior first defines the SLM coordinates and the original VTA analysis places policy, APE and post-outcome updating at the appropriate within-event times. The most direct raw-FP reconstruction keeps the original Early/Middle analysis contracts fixed and returns the same Early policy P=.0469 and Middle APE×SRI ρ=.667, P=.0416. The outcome-stage real-action-bout readout independently preserves the main social-credit and scalar-RPE structure. PSTHs then explain when these computations emerge and why integration windows differ in sensitivity. The resulting neural sequence is <strong>decide whether to observe → acquire social information → evaluate the sampling action → update from the outcome → alter the next social sample.</strong></div>',
'<div class="callout"><strong>Integrated VTA conclusion: Early → Middle → Post → causal.</strong> Early sampling policy survives strict raw-FP reconstruction (5/6, rank-biserial=.810, P=.0469). Middle APE coupling tracks SRI and is unchanged by reconstruction (ρ=.667, P=.0416). At Post, bout-matched DA gives the clearest source-specific credit result: behavior-selected Passive credit beats both fixed-credit comparators in 9/9 animals (both P=.0039), while the original fixed-window RPE result remains the frozen reference. Finally, contingent JAWS suppresses successful-Active credit updating in 10/10 animals (P=.001953), closing the sequence at the causal level. The supported chain is <strong>decide whether to observe → evaluate the sampling action → assign outcome-specific social credit → use VTA-dependent teaching to alter future sampling.</strong></div>')

# Chinese overview
replace_once("index-zh.html",
'<div class="card violet"><div class="metric-label">多巴胺跟随社会学习的真实计算顺序</div><div class="metric">决定 → 采样 → 学习</div><p>一次观察过程中，VTA 多巴胺依次反映结果前的采样策略、采样动作预测误差（APE），以及结果后的奖赏和社会结果归因更新。</p></div>',
'<div class="card violet"><div class="metric-label">多巴胺跟随社会学习的真实计算顺序</div><div class="metric">决定 → 评估 → 归因</div><p>一次观察过程中，VTA 多巴胺依次反映结果前采样策略、采样动作预测误差（APE）和行为数据定义的来源/结果特异社会归因。结果期的机制展示优先采用真实行动片段多巴胺，固定 0–6 秒结果作为冻结的原始统计参照。</p></div>')

replace_once("index-zh.html",
'<div class="card good"><div class="series-index">07</div><h3>多巴胺实时跟随社会学习的计算过程</h3><p>结果前依次出现采样策略和动作预测误差信号，结果后进入奖赏和社会归因更新。</p></div>',
'<div class="card good"><div class="series-index">07</div><h3>多巴胺实时跟随社会学习的计算过程</h3><p>早期采样策略和中段 APE 提供最有区分力的时间证据；结果期真实行动片段多巴胺在 9/9 动物中支持行为数据选出的社会归因规则（相对 0.75 和 1.0 均 P=.0039），固定窗口 RPE 保留为冻结的经典参照。</p></div>')

replace_once("index-zh.html",
'<div class="section-head"><div><div class="section-kicker">神经实现</div><h2>VTA 多巴胺沿着 SLM 的计算顺序展开：先决定是否采样社会信息，再处理采样误差，最后根据结果更新</h2></div><p>这里先保留原来的核心发现；随后从原始光纤信号重新计算观察片段多巴胺，在完全相同的早期/中段分析合同下做严格复现；结果期再用固定 0–6 秒与真实行动时长两种读出交叉验证，最后用围事件时间曲线解释这些效应的真实时间形状。</p></div>',
'<div class="section-head"><div><div class="section-kicker">神经实现</div><h2>VTA 多巴胺沿一条连续学习序列展开：采样策略 → 动作预测误差 → 结果特异社会归因</h2></div><p>早期和中段保留冻结的原始统计合同，并直接从原始光纤信号重建。结果期的主机制展示采用与真实行动/结果片段对齐的多巴胺读出，同时保留固定 0–6 秒分析作为原始统计参照；随后用结果配对的 JAWS 检验 VTA 对社会归因教学分支的必要性。</p></div>')

replace_once("index-zh.html",
'<div class="reader-guide"><div class="reader-step"><b>为什么做</b><span>如果 SLM 描述了真实神经计算，相关变量应出现在与其功能一致的时间位置。</span></div><div class="reader-step"><b>怎么做</b><span>分别检验结果前采样策略、中段 APE 和结果后更新，并用 Q 学习、选择惯性与灵活模型作竞争对照。</span></div><div class="reader-step"><b>结论</b><span>SLM 在三个预设时间轴均得到支持；通用 Q/RPE 主要解释结果后阶段。</span></div></div>',
'<div class="reader-guide"><div class="reader-step"><b>为什么做</b><span>如果 SLM 描述了真实神经计算，相关变量应出现在与其功能一致的时间位置。</span></div><div class="reader-step"><b>怎么做</b><span>早期采样策略和中段 APE 使用冻结的原始合同；结果期用真实行动片段多巴胺检验社会归因，同时把固定窗口保留为锁定参照。</span></div><div class="reader-step"><b>结论</b><span>早期采样策略和中段 APE 经原始光纤重建后保持；结果期真实行动片段最清楚地支持行为数据定义的社会归因；结果配对 JAWS 随后削弱成功结果后的归因更新。</span></div></div>')

replace_once("index-zh.html",
'''<div class="cards-3">
<div class="card good"><div class="metric-label">结果前：是否值得获取社会信息</div><div class="metric">采样策略</div><p>结果前 VTA 信号与 SLM 的采样策略一致，秩双列相关=.810，P=.0469；通用 Q/RPE 在这一阶段接近零。</p></div>
<div class="card info"><div class="metric-label">采样后、结果前：这次动作有多出乎预期</div><div class="metric">APE</div><p>中段 APE 的逐动物耦合强度与学习程度保持关系（Spearman ρ=.667，与 SRI 的精确单侧置换 P=.0416）；控制选择惯性和经典 Q 误差后仍保留。</p></div>
<div class="card violet"><div class="metric-label">结果出现后：根据结果完成更新</div><div class="metric">RPE / 社会归因</div><p>结果后 RPE 得到支持，秩双列相关=.867，P=.0195；此时普通 Q/RPE 也有效，因此这一阶段单独看不足以区分完整机制。</p></div>
</div>''',
'''<div class="cards-4" id="vta-causal-spine-v113">
<div class="card good"><div class="metric-label">早期 · 决定是否采样</div><div class="metric">采样策略 → VTA</div><p>冻结早期合同下，采样策略在 5/6 动物中提高多巴胺预测，秩双列相关=.810、P=.0469；从原始光纤信号重建后得到同一推断和逐动物排序。</p></div>
<div class="card info"><div class="metric-label">中段 · 评估这次采样动作</div><div class="metric">APE × 学习强度</div><p>中段 APE 耦合强度随社会学习程度增加，和 SRI 的 Spearman ρ=.667、精确单侧置换 P=.0416；原始光纤重建后保持一致。</p></div>
<div class="card violet"><div class="metric-label">结果期 · 给结果分配来源特异社会归因</div><div class="metric">真实行动片段归因 → VTA</div><p>同一 1,371 个事件中，行为数据选出的被动结果归因相对固定 0.75 和固定 1.0，在真实行动片段多巴胺下均为 9/9 动物支持（两项 P=.0039）。冻结的固定窗口参照方向一致但较弱。</p></div>
<div class="card good"><div class="metric-label">因果 · VTA 是否参与教学</div><div class="metric">JAWS → 归因更新</div><p>结果配对 JAWS 使主动社会归因更新在 10/10 动物中下降（P=.001953），累积主动归因在 9/10 动物中下降（P=.003906）。这里检验同一归因教学分支中的成功主动结果，和上方被动结果归因读出属于不同结果分支。</p></div>
</div>''')

replace_once("index-zh.html",
'<figcaption><strong>原始核心结果：SLM 的三个计算阶段按正确的时间顺序出现在 VTA 多巴胺中。</strong>A，结果前采样策略；B，中段 APE；C，结果后 RPE；D，模型家族的时间轴比较。SLM 为 3/3，Q/RPE 主要只在结果后阶段得到支持。这个结果构成行为模型与 VTA 神经计算之间的主要机制桥梁。</figcaption>',
'<figcaption><strong>冻结的原始时间轴参照。</strong>A，结果前采样策略；B，中段 APE；C，原始固定窗口的结果后 RPE；D，模型家族时间轴比较。这张图完整保留原始统计 authority；当前主机制叙事中的结果期读出采用下方真实行动片段的社会归因分析。</figcaption>')

replace_once("index-zh.html",
'<div class="callout"><strong>先把原结论固定下来｜</strong>VTA 数据最有区分力的地方来自事件内部的时间顺序。结果后 RPE 本身并不特殊；真正增加机制信息的是更早出现的采样策略和 APE。</div>',
'<div class="callout"><strong>为什么继续保留冻结的固定窗口结果｜</strong>它锁定原始统计 authority，也避免因为真实行动片段的 P 值更小就事后替换旧结果。当前主叙事优先真实行动片段来自生物学理由：神经积分窗口与实际行动/结果片段直接对齐；固定 0–6 秒 RPE 继续作为锁定参照和敏感性证据。</div>')

replace_once("index-zh.html",
'<div class="model-contract" id="vta-signal-zoo-v105"><strong>为什么行为模型库到了 VTA 变成“候选计算信号库”｜</strong>行为部分比较完整系统预测“是否观察”的能力；神经部分冻结这些系统产生的计算量，再检验它们分别出现在预设的早期、中段和结果后时间轴上的程度。某一模型家族可以解释结果期多巴胺，同时在更早时间轴缺乏支持。因此结果期 RPE 有效，只说明结果更新家族能解释这一阶段；覆盖完整社会学习链还需要早期采样策略和中段 APE。</div>',
'<div class="model-contract" id="vta-signal-zoo-v105"><strong>为什么行为模型库到了 VTA 变成“候选计算信号库”｜</strong>行为部分比较完整系统预测“是否观察”的能力；神经部分冻结这些系统产生的计算量，再检验它们分别出现在预设的早期、中段和结果后时间轴上的程度。某一模型家族可以解释结果期多巴胺，同时在更早时间轴缺乏支持。因此结果期 RPE 有效，只说明结果更新家族能解释这一阶段；覆盖完整社会学习链还需要早期采样策略和中段 APE。<strong>Authority 注释｜</strong>下表结果后列继续使用冻结的原始固定窗口指标，并与新增的真实行动片段社会归因读出分开呈现。</div>')

replace_once("index-zh.html",
'<div class="card info"><div class="metric-label">证据层级 2 · 替代读出稳健性</div><div class="metric">同一生物学问题，换积分方式</div><p>结果期在同一 1,371 个事件上，把固定 0–6 秒多巴胺换成真实行动时长多巴胺。这一层对社会归因和标量 RPE 提供更独立的读出稳健性检验。</p></div>',
'<div class="card info"><div class="metric-label">证据层级 2 · 结果期主机制读出</div><div class="metric">与真实行为片段对齐的社会归因检验</div><p>同一 1,371 个事件上，真实行动片段多巴胺把神经积分窗口直接对齐实际行动/结果过程，并给出最清楚的“行为参数→神经社会归因”检验。固定 0–6 秒分析继续保留为原始参照，因此优先级依据生物学对齐关系，而非单纯依据更小的 P 值。</p></div>')

replace_once("index-zh.html",
'<div class="section-kicker" style="margin-top:28px">替代读出稳健性｜结果期换成真实行动时长读出，检验社会归因与 RPE 结构</div>',
'<div class="section-kicker" style="margin-top:28px">结果期主机制读出｜社会归因采用真实行动片段多巴胺，同时保留固定 0–6 秒原始参照</div>')

replace_once("index-zh.html",
'<div class="reader-guide"><div class="reader-step"><b>为什么做</b><span>确认原来的 SLM→VTA 结果没有依赖固定 0–6 秒这一种积分方式。</span></div><div class="reader-step"><b>怎么做</b><span>锁定同一批 1,371 个结果事件、9 只动物以及同一套行为参数和模型比较，只把多巴胺读出换成新方法得到的真实行动片段 AUC/秒；持续时间低于 0.05 秒的近零片段排除。</span></div><div class="reader-step"><b>结论</b><span>行为数据选出的归因规则跨读出保持方向：相对 0.75 两种读出均显著；相对 1.0，固定 0–6 秒为边缘结果，真实行动片段显著。标量 RPE 结构也保留，固定结果后窗口的 RPE 证据更强。</span></div></div>',
'<div class="reader-guide"><div class="reader-step"><b>为什么做</b><span>结果期读出按生物学对齐关系决定主次：真实行动片段 AUC/秒对应实际行动/结果过程，固定 0–6 秒同时保留动作结束后的评估阶段。</span></div><div class="reader-step"><b>怎么做</b><span>锁定同一批 1,371 个结果事件、9 只动物以及同一套行为参数和模型比较，并排比较真实行动片段 AUC/秒与原始固定 0–6 秒参照；持续时间低于 0.05 秒的近零片段排除。</span></div><div class="reader-step"><b>结论</b><span>真实行动片段给出最清楚的社会归因结果：行为数据选出的归因规则相对固定 0.75 和 1.0 均为 9/9 动物支持（两项 P=.0039）。固定窗口的归因结果方向一致但较弱，经典 RPE 则在较宽的固定窗口中更敏感。</span></div></div>')

replace_once("index-zh.html",
'<figcaption><strong>把结果期分析原样换成新方法得到的真实行为时长读出后，核心 SLM→VTA 关系仍保留。</strong>A，两种多巴胺数值在每只动物中均正相关，中位 ρ=.785。B，RPE 家族在两种读出中保持相同方向，但真实行动片段的效应较弱。C，只用行为数据确定的被动结果归因相对 0.75 在固定窗口为 7/9（P=.0391）、真实行动片段为 9/9（P=.0039）；相对 1.0，固定窗口为 6/9（P=.0547，边缘），真实行动片段为 9/9（P=.0039）。D，在两种读出中，结果向量误差加入标量 RPE 后都没有额外预测收益。</figcaption>',
'<figcaption><strong>结果期主机制读出与冻结固定窗口参照。</strong>A，两种多巴胺数值在每只动物中均正相关，中位 ρ=.785。B，经典 RPE 家族方向一致，在较宽的固定窗口中通常更强。C，行为数据确定的被动结果归因在真实行动片段中最清楚：相对固定 0.75 和固定 1.0 均为 9/9 动物支持（两项 P=.0039）；冻结固定窗口分别为 7/9（P=.0391）和 6/9（P=.0547）。D，两种读出中，结果向量误差加入标量 RPE 后均无额外预测收益。</figcaption>')

replace_once("index-zh.html",
'<div class="callout"><strong>VTA 部分的整合结论｜</strong>行为数据先定义 SLM 的计算坐标，原始 VTA 分析再把采样策略、APE 和结果后更新放到正确的事件内时间位置。最关键的原始光纤信号重建保持早期/中段原分析合同不变，得到同一个早期采样策略 P=.0469 和中段 APE×SRI ρ=.667、P=.0416；结果期的真实行动时长读出又独立保留了社会归因与标量 RPE 的主要结构。围事件时间曲线最后解释这些计算何时出现以及为什么不同窗口灵敏度不同。由此得到一条连续神经计算链：<strong>决定是否观察 → 获取社会信息 → 处理采样误差 → 根据结果更新 → 改变下一次社会采样。</strong></div>',
'<div class="callout"><strong>VTA 整合主线：早期 → 中段 → 结果期 → 因果。</strong>早期采样策略经过严格原始光纤重建后保持 5/6 动物改善、秩双列相关=.810、P=.0469；中段 APE 与 SRI 的耦合保持 ρ=.667、P=.0416。结果期采用与真实行为片段对齐的多巴胺后，行为数据选出的被动结果归因相对两个固定权重均为 9/9 动物支持（两项 P=.0039），固定窗口 RPE 继续保留为冻结原始参照。最后，结果配对 JAWS 使成功主动结果后的社会归因更新在 10/10 动物中下降（P=.001953），把这条序列推进到因果层面。当前最紧的计算链是：<strong>决定是否观察 → 评估采样动作 → 给结果分配来源特异社会归因 → 通过 VTA 依赖的教学改变未来采样。</strong></div>')

print("v113b patch complete")
