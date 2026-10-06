from pathlib import Path
R=Path(__file__).resolve().parents[1]

css="""
<style id="model-explainer-v66">
.model-map{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:16px 0}
.model-family{border:1px solid #d9dde2;border-radius:10px;padding:12px;background:#fff}
.model-family h4{font-size:14px;margin:0 0 6px}.model-family p{font-size:12px;line-height:1.45;margin:4px 0}
.model-tag{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#666}
.model-contract{border-left:3px solid #bd202b;padding:10px 12px;margin:14px 0;background:#fafafa;font-size:13px;line-height:1.55}
@media(max-width:850px){.model-map{grid-template-columns:1fr 1fr}}@media(max-width:520px){.model-map{grid-template-columns:1fr}}
</style>
"""
en="""
<div class="model-contract"><strong>One zoo, different contracts.</strong> The page uses one frozen model registry, but not every scientific question has the same target. A model can be strong for <em>choice prediction</em>, weak for <em>mechanistic interpretability</em>, or useful only as a <em>capacity ceiling</em>. Comparisons are therefore made only within a matched contract: same target, held-animal split, observable inputs and evaluation metric. “Best model” below always means best for that stated contract, not best everywhere.</div>
<div class="model-map">
<div class="model-family"><div class="model-tag">0 · Null / linear readout</div><h4>Prevalence, clock, current state, logistic readout</h4><p><b>Principle:</b> no learned latent state; weighted sum of directly observed predictors.</p><p><b>Parameters:</b> intercept + feature weights; regularization selected inside training folds.</p><p><b>Role:</b> asks how much is already predictable without learning or nonlinear memory.</p></div>
<div class="model-family"><div class="model-tag">1 · Classical learning rules</div><h4>RW / WSLS / Q / forgetting-Q / choice kernel</h4><p><b>Principle:</b> a few scalar values updated after outcomes; Q/RPE uses δ=r+γV′−V.</p><p><b>Parameters:</b> learning/forgetting rates, reward/value weights, inverse-temperature or logistic readout; choice-kernel decay/weight.</p><p><b>Role:</b> interpretable RL alternatives and persistence controls.</p></div>
<div class="model-family"><div class="model-tag">2 · Mechanistic hypothesis</div><h4>SLM core → default SLM</h4><p><b>Principle:</b> multiscale social memory + source/outcome-specific credit determine an <b>Observe policy</b>; sampled outcomes generate an <b>APE</b> before reward and a source-specific value/credit update after reward.</p><p><b>Default:</b> SLM core + one generic choice-persistence term. This is the behavioral predictor.</p><p><b>Role:</b> variables are defined before VTA/JAWS tests, so policy, APE and post-outcome credit are predictions rather than post-hoc labels.</p></div>
<div class="model-family"><div class="model-tag">3 · Flexible nonlinear controls</div><h4>Full-history MLP / TinyRNN / generic recurrent agent</h4><p><b>Principle:</b> nonlinear hidden units learn flexible history interactions with fewer mechanistic constraints.</p><p><b>Parameters:</b> hidden-state/hidden-layer weights and regularization chosen within training data; no SLM latent semantics are imposed.</p><p><b>Role:</b> capacity ceiling, identifiability stress test, and independent convergence—not the mechanistic reference by default.</p></div>
<div class="model-family"><div class="model-tag">4 · Dynamics model</div><h4>SWM (Social World Model)</h4><p><b>Principle:</b> recurrent latent state predicts future behavioral/social dynamics and supports counterfactual perturbations.</p><p><b>Parameters:</b> encoder/recurrent latent dynamics/readout weights learned end-to-end; SLM equations are not supplied.</p><p><b>Role:</b> tests whether SLM-like coordinates emerge and what extra prospective state exists. It is a world/dynamics model, not another name for SLM.</p></div>
</div>
<div class="model-contract"><strong>Terminology used throughout.</strong> <b>Policy</b> = probability/rule for choosing Observe before the sampled outcome. <b>APE</b> = action-prediction error for whether sampled social information changes the learner toward Active; it is pre-reward and is not an RPE. <b>RPE</b> = reward/value prediction error after outcome; classical Q/RPE is therefore mainly a post-outcome comparator. <b>Social credit</b> = source/outcome-specific update assigned after the sampled outcome; JAWS tests this credit assignment. Linear/nonlinear describes function class; policy/RPE/APE describes the computed variable. They are orthogonal labels, not competing model names.</div>
"""
zh="""
<div class="model-contract"><strong>同一个 model zoo，不同的检验 contract。</strong> 全页使用一套冻结的模型注册表，但不同科学问题的预测目标并不相同。一个模型可以擅长<em>行为预测</em>，却不适合做<em>机制解释</em>；也可以只作为<em>容量上限</em>。因此只有在目标、held-animal split、可见输入和评价指标一致时才比较。“最佳模型”只表示在当前 contract 下最佳，不表示全局最佳。</div>
<div class="model-map">
<div class="model-family"><div class="model-tag">0 · 空模型 / 线性读出</div><h4>Prevalence、clock、current state、logistic readout</h4><p><b>原理：</b>不学习隐状态，直接对可观测变量做加权求和。</p><p><b>参数：</b>截距、特征权重；正则化只在训练 fold 内选择。</p><p><b>用途：</b>回答“不需要学习和非线性记忆，本身能预测多少”。</p></div>
<div class="model-family"><div class="model-tag">1 · 经典学习规则</div><h4>RW / WSLS / Q / forgetting-Q / choice kernel</h4><p><b>原理：</b>用少数标量 value 随 outcome 更新；Q/RPE 的核心误差为 δ=r+γV′−V。</p><p><b>参数：</b>学习率/遗忘率、reward/value 权重、inverse temperature 或 logistic readout；choice-kernel 的衰减和权重。</p><p><b>用途：</b>可解释的 RL 替代模型与 choice persistence 对照。</p></div>
<div class="model-family"><div class="model-tag">2 · 机制假说</div><h4>SLM core → default SLM</h4><p><b>原理：</b>多时间尺度 social memory 与 source/outcome-specific credit 决定 <b>Observe policy</b>；采样后、奖赏前产生 <b>APE</b>，奖赏后产生 source-specific value/credit update。</p><p><b>默认模型：</b>SLM core + 一个通用 choice-persistence 项，用于行为预测。</p><p><b>用途：</b>在 VTA/JAWS 结果之前先定义 policy、APE、post-outcome credit，使神经结果成为预先定义变量的检验。</p></div>
<div class="model-family"><div class="model-tag">3 · 灵活非线性对照</div><h4>Full-history MLP / TinyRNN / generic recurrent agent</h4><p><b>原理：</b>非线性 hidden units 自由学习 history interaction，不强制 SLM 的机制结构。</p><p><b>参数：</b>hidden-state/hidden-layer 权重和正则化在训练数据内选择；不预设 SLM latent 的生物学含义。</p><p><b>用途：</b>容量上限、identifiability 压力测试和独立收敛验证；默认不作为机制参照系。</p></div>
<div class="model-family"><div class="model-tag">4 · 动力学模型</div><h4>SWM（Social World Model）</h4><p><b>原理：</b>recurrent latent state 预测未来行为/社会动力学，并支持 counterfactual perturbation。</p><p><b>参数：</b>encoder、recurrent latent dynamics 与 readout 端到端学习；训练时不提供 SLM 方程。</p><p><b>用途：</b>检验 SLM-like coordinates 是否自行涌现，以及还存在什么额外 prospective state。SWM 是 world/dynamics model，不是 SLM 的另一个名字。</p></div>
</div>
<div class="model-contract"><strong>后文统一术语。</strong> <b>Policy</b> = outcome 发生前选择 Observe 的概率/规则。<b>APE</b> = 采样到的社会信息是否把 learner 推向 Active 的 action-prediction error，发生在 reward 前，因此与 RPE 不同。<b>RPE</b> = outcome 后的 reward/value prediction error，所以经典 Q/RPE 主要是 post-outcome comparator。<b>Social credit</b> = sampled outcome 后分配给特定信息来源/结果的更新，JAWS 检验的是这个 credit assignment。linear/nonlinear 描述模型的函数形式；policy/RPE/APE 描述模型内部计算的变量，两者是正交概念，不应混成不同“模型名”。</div>
"""

for fn,block in [("index.html",en),("index-zh.html",zh)]:
    p=R/fn;s=p.read_text(encoding="utf-8")
    if 'id="model-explainer-v66"' not in s:
        s=s.replace("</head>",css+"</head>",1)
    marker='<div class="reader-guide" data-guide="slm">'
    i=s.find(marker)
    if i<0: raise RuntimeError((fn,"marker missing"))
    # insert after reader-guide closing div
    j=s.find("</div></div>",i)
    if j<0: raise RuntimeError((fn,"reader close missing"))
    j+=12
    s=s[:j]+block+s[j:]
    p.write_text(s,encoding="utf-8")
print("inserted unified model-zoo explainer EN/ZH")
