from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]

css=r'''
<style id="model-framework-v66">
.model-framework{margin:18px 0 24px;padding:18px;border:1px solid #d9dee5;border-radius:14px;background:#fbfcfd}
.model-framework h3{margin:0 0 8px;font-size:1.08rem}.model-framework .lead{margin:0 0 13px;color:#39424e}
.model-layers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.model-layer{padding:11px;border-left:3px solid #c6ccd3;background:#fff}.model-layer.primary{border-left-color:#b51f2b}
.model-layer b{display:block;margin-bottom:4px}.model-layer small{display:block;color:#56606c;line-height:1.42}
.model-contract{margin-top:12px;padding-top:11px;border-top:1px solid #e1e5e9;font-size:.91rem;line-height:1.5}
.model-role{display:inline-block;padding:2px 7px;margin-right:4px;border-radius:999px;background:#eef1f4;font-size:.78rem}
@media(max-width:720px){.model-layers{grid-template-columns:1fr 1fr}}@media(max-width:480px){.model-layers{grid-template-columns:1fr}}
</style>
'''

en=r'''
<div class="model-framework" id="model-framework">
<h3>Model map: four different questions, one fixed vocabulary</h3>
<p class="lead">The names below are not interchangeable “models.” They occupy different levels of the analysis. We first define the biological computation, then ask whether extra flexibility improves prediction, then use neural models to identify which computation dopamine carries.</p>
<div class="model-layers">
<div class="model-layer primary"><b>1 · Mechanistic SLM</b><small><span class="model-role">interpretable</span>Explicit state variables for current state, multiscale memory, Observe policy, action-prediction error (APE), and source/outcome-specific social credit. These variables are the mechanistic authority used for causal and neural predictions.</small></div>
<div class="model-layer"><b>2 · Predictive controls</b><small><span class="model-role">model zoo</span>Linear/logistic current-state models, choice-kernel/history models, Q/RL families, nonlinear MLPs and TinyRNN. Their job is to test whether SLM wins because of social-learning structure rather than generic memory, nonlinearity, or recurrent capacity.</small></div>
<div class="model-layer"><b>3 · SWM / flexible latent model</b><small><span class="model-role">nonlinear recurrent</span>A recurrent world model learns latent state without imposing the SLM equations. It tests whether SLM coordinates emerge in a flexible representation and whether additional variables such as prospective social efficacy remain.</small></div>
<div class="model-layer"><b>4 · Neural encoding models</b><small><span class="model-role">VTA readout</span>Policy, APE, RPE/Q and belief-surprise are candidate regressors for dopamine, not competing behavioral agents. They ask what DA represents at Early, Middle and Post-outcome epochs.</small></div>
</div>
<div class="model-contract"><b>Fixed comparison contract.</b> For the main behavioral model zoo, all models use the same 27 held animals, the same event target and held-animal evaluation; Brier is the primary calibration-sensitive score, with AUC/log loss as supporting metrics. “Linear vs nonlinear” refers to function class; “policy / APE / RPE” refers to computational variables. These are orthogonal distinctions. A different zoo is used only when the scientific question changes, and each such figure must state its comparator set and why.</div>
</div>
'''

zh=r'''
<div class="model-framework" id="model-framework">
<h3>模型地图：四类问题，统一一套术语</h3>
<p class="lead">这里出现的名称属于不同分析层级，需要按其角色分别理解。它们处在不同分析层级：先定义动物可能执行的生物学计算，再检验增加通用非线性或记忆能力是否足以解释行为，最后用神经编码模型判断多巴胺在不同时间段携带哪一种计算量。</p>
<div class="model-layers">
<div class="model-layer primary"><b>1 · Mechanistic SLM</b><small><span class="model-role">可解释机制</span>显式表示当前状态、多时间尺度记忆、Observe policy、action-prediction error（APE）以及来源/结果特异的 social credit。这一层是因果操控和神经预测所使用的机制主体。</small></div>
<div class="model-layer"><b>2 · Predictive controls</b><small><span class="model-role">model zoo</span>包括线性/Logistic 当前状态模型、choice-kernel/history、Q/RL、非线性 MLP 和 TinyRNN。它们作为控制模型，用来逐项排除“只是记忆”“只是非线性”“只是循环网络容量”这些替代解释。</small></div>
<div class="model-layer"><b>3 · SWM / flexible latent model</b><small><span class="model-role">非线性循环模型</span>循环 world model 不预先写入 SLM 方程，自行学习 latent state。这里检验 SLM 坐标能否在更灵活的表征中自然出现，以及是否还存在 prospective social efficacy 等 SLM 之外的信息。</small></div>
<div class="model-layer"><b>4 · Neural encoding models</b><small><span class="model-role">VTA readout</span>policy、APE、RPE/Q、belief-surprise 在这里是解释 dopamine 的候选计算变量，这里分别作为神经信号候选量使用；问题是 Early、Middle、Post-outcome 的 DA 分别更像哪一种量。</small></div>
</div>
<div class="model-contract"><b>统一比较规则。</b>主行为 model zoo 固定使用同一批 27 只 held animals、同一事件预测目标和 held-animal evaluation；Brier 为主要的 calibration-sensitive 指标，AUC/log loss 为辅助指标。“线性/非线性”描述函数形式；“policy / APE / RPE”描述计算变量，两者属于两个正交维度。只有科学问题改变时才允许换 model zoo，而且每张图都必须写明本图比较哪些模型、为什么需要这组 comparator。</div>
</div>
'''

# Additional section-specific introductions prevent zoo switching from feeling arbitrary.
en_neural=r'''<div class="callout"><strong>Why the model set changes here.</strong> The behavioral zoo above compares complete choice-prediction systems. The VTA analysis instead compares <em>candidate computational signals</em> generated by those systems. Policy is the pre-outcome propensity to sample social information; APE is the mismatch between the expected and observed consequence of the sampling action; RPE is reward prediction error; social credit is the source-specific post-outcome update. Therefore a good RPE fit at Post does not make RPE a replacement for the behavioral SLM.</div>'''
zh_neural=r'''<div class="callout"><strong>为什么这里的 model set 会改变。</strong>前面的行为 model zoo 比较的是完整的 choice-prediction system；VTA 部分比较的则是这些系统产生的候选计算信号。policy 表示结果发生前采样社会信息的倾向；APE 表示采样动作预期结果与实际结果之间的偏差；RPE 是 reward prediction error；social credit 是结果发生后、带有信息来源标签的更新。因此 Post 阶段 RPE 拟合得好，并不等于 RPE 可以替代整个行为 SLM。</div>'''

en_swm=r'''<div class="callout"><strong>Why SWM is not another row in the same zoo.</strong> MLP/TinyRNN controls ask whether generic nonlinear capacity predicts choices better under the same supervised target. SWM has a different purpose: it learns a recurrent latent state and is interrogated for representation, prospective prediction and causal latent-subspace function. Its comparison set therefore contains SLM/current-cue baselines, social-content controls and matched latent scrubs rather than the entire behavioral zoo.</div>'''
zh_swm=r'''<div class="callout"><strong>为什么 SWM 不直接作为同一个 model zoo 的又一行。</strong>MLP/TinyRNN 的问题是：在相同监督预测目标下，通用非线性容量能不能解释行为；SWM 的任务不同，它先学习 recurrent latent state，再检验其中的表征、未来预测和 latent-subspace 的因果功能。因此这里合理的 comparator 是 SLM/current-cue baseline、social-content control 和 matched latent scrub，，对应这一问题无需机械重复整个行为 zoo。</div>'''

for fn,block,neural,swm in [("index.html",en,en_neural,en_swm),("index-zh.html",zh,zh_neural,zh_swm)]:
 p=R/fn;s=p.read_text(encoding="utf-8")
 if 'model-framework-v66' not in s:
  s=s.replace('</head>',css+'</head>',1)
 # Put map immediately before the first SLM definition.
 anchor='<div class="bio-logic"><strong>What SLM means'
 if fn.endswith('zh.html'): anchor='<div class="bio-logic"><strong>SLM 是什么'
 pos=s.find(anchor)
 if pos<0:
  # robust fallback: insert before first SLM bio-logic/card cluster
  pos=s.find('<div class="bio-logic"', s.find('id="slm"'))
 if pos>=0 and 'id="model-framework"' not in s:
  s=s[:pos]+block+s[pos:]
 # SWM and VTA introductions
 swmpos=s.find('<p>SLM starts from explicit hypotheses') if fn=="index.html" else s.find('SLM',s.find('id="swm"'))
 if swmpos>=0 and swm not in s:
  # insert after reader guide if possible, otherwise before paragraph
  s=s[:swmpos]+swm+s[swmpos:]
 # neural: before DA temporal figure / section explanatory paragraph
 marker='SOE_DA_temporal_logic_v65'
 pos=s.find(marker)
 if pos>=0 and neural not in s:
  figpos=s.rfind('<figure',0,pos)
  s=s[:figpos]+neural+s[figpos:]
 p.write_text(s,encoding="utf-8")
print("added unified model map + explicit zoo-switch explanations")
