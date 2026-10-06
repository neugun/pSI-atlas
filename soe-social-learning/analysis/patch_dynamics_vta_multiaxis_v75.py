from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace_once(text, old, new):
    if old not in text:
        return text
    return text.replace(old, new, 1)

def section_bounds(text, sid):
    k = text.find(f'id="{sid}"')
    if k < 0:
        raise RuntimeError(f"missing section: {sid}")
    a = text.rfind("<section", 0, k)
    b = text.find("<section", k + 1)
    if b < 0:
        b = text.find("</main>", k)
    return a, b

def insert_before_first_figure(text, sid, block, block_id):
    if f'id="{block_id}"' in text:
        return text
    a, b = section_bounds(text, sid)
    sec = text[a:b]
    k = sec.find("<figure")
    if k < 0:
        raise RuntimeError(f"no figure in section: {sid}")
    sec = sec[:k] + block + "\n" + sec[k:]
    return text[:a] + sec + text[b:]

def patch_page(filename, zh=False):
    p = ROOT / filename
    s = p.read_text(encoding="utf-8")

    if zh:
        s = replace_once(
            s,
            "一次结果会立即改变下一次决策，最近多次社会经验会在数分钟内累积，而部分学习状态还能延续到下一场次。",
            "一次结果会立即重设下一步是否还需要继续获取社会信息；最近多次社会经验会在数分钟内累积，部分学习状态还能延续到下一场次。",
        )
        s = replace_once(
            s,
            '<div class="card good"><div class="metric-label">一次结果立即改变下一步选择</div><div class="metric">秒级记忆</div><p>主动成功或被动结果之后，动物下一次更容易停止观察，同时重新进入观察的概率下降。</p></div>',
            '<div class="card good"><div class="metric-label">一次结果会立即重设下一步社会信息需求</div><div class="metric">结果立刻改变是否继续找信息</div><p>相对未奖赏，主动成功使下一次重新启动观察下降 9.0 个百分点，被动结果下降 8.3 个百分点；在学习者中，主动成功驱动的快速切换效应从训练早期 4.3 增至晚期 10.8 个百分点（P=.041）。</p></div>',
        )
        s = replace_once(
            s,
            '<div class="callout">这组结果先于最终 SLM，因而给出了模型需要多时间尺度状态的行为依据：快速选择调整、分钟级历史整合、跨天初始状态连续性分别承担不同功能。</div>',
            '<div class="callout"><strong>秒级效应的生物学含义｜</strong>结果会立刻改变“还需不需要继续从同伴那里取样”。未奖赏保留了继续寻求社会信息的需求，得到主动成功或被动结果后则暂时降低再次采样；这条快速规则还会随学习增强。分钟级历史和跨天先验继续在更慢时间尺度上塑造同一采样策略。</div>',
        )
        slm_block = '''<div id="slm-learning-axis-bridge-v75">
<div class="section-kicker" style="margin-top:28px">SLM 的内部变量分别对齐不同学习表型</div>
<div class="cards-4" style="margin-top:12px">
<div class="card good"><div class="metric-label">采样策略随学习一起改变</div><div class="metric">策略变化跟随 SRI 增益</div><p>40 只动物中，采样策略的训练变化与 SRI 增益相关：ρ=.453，P=.00337。</p></div>
<div class="card info"><div class="metric-label">动作预测误差对应晚期社会学习程度</div><div class="metric">APE 变化跟随晚期表型</div><p>|APE| 的训练变化与晚期 SRI 相关：ρ=.383，P=.0146。</p></div>
<div class="card violet"><div class="metric-label">结果误差对应信息到行动的转化</div><div class="metric">RPE 变化跟随转化增益</div><p>|RPE| 的训练变化与观察后成功行动的转化增益相关：ρ=.615，P=2.43×10⁻⁵。</p></div>
<div class="card good"><div class="metric-label">社会结果归因对应成功利用社会信息</div><div class="metric">归因分离跟随主动成功</div><p>晚期社会归因分离度与观察后的主动成功概率相关：ρ=.558，P=.000181。</p></div>
</div>
<div class="callout"><strong>这组关系为什么重要｜</strong>SLM 内部的策略、APE、RPE 和社会结果归因分别对应不同的学习表型。它们提供相互补充的计算坐标；相关性本身不用于宣称因果，后面的 VTA 时间判别和 JAWS 扰动继续检验这些坐标的神经与因果含义。</div>
</div>'''
        vta_block = '''<div id="vta-multiaxis-v75">
<div class="section-kicker" style="margin-top:28px">四条独立证据把 SLM 与多巴胺连接起来</div>
<div class="cards-4" style="margin-top:12px">
<div class="card good"><div class="metric-label">行为层先分离奖励误差与动作误差</div><div class="metric">APE 主导，RPE 再提供小幅增益</div><p>整只动物留出中，仅 APE 的 Brier=.1911，仅 RPE=.2273；APE 在 27/27 动物优于 RPE（P=1.49×10⁻⁸）。加入 RPE 的双通路在 24/27 动物继续改善（P=4.92×10⁻⁷）。</p></div>
<div class="card info"><div class="metric-label">神经时间顺序提供机制判别</div><div class="metric">SLM 的 3/3 时间轴成立</div><p>结果前采样策略 P=.0469，中段 APE P=.0416，结果后 RPE P=.0195；通用 Q/RPE 只在结果后时段得到支持。</p></div>
<div class="card violet"><div class="metric-label">结果后的误差表示还可以继续拆解</div><div class="metric">当前更符合标量 RPE 描述</div><p>9 只动物中，带符号 RPE+|RPE| 的平均留出均方误差增益=.01518；二维结果向量误差为 .00544，加入向量幅度后为 .00871。标量 RPE 已进入后，结果向量项没有额外收益（−.00035，P=1.0）。</p></div>
<div class="card good"><div class="metric-label">行为中学到的被动结果归因可迁移到多巴胺</div><div class="metric">无需用神经数据重新调参</div><p>只用行为数据选出的被动结果归因直接用于行动时段多巴胺后，相对固定 0.75 和 1.0 的归因权重都在 9/9 动物更好（两项 P=.0039）。</p></div>
</div>
<div class="callout"><strong>四条证据回答四个不同问题｜</strong>行为层的 RPE/APE 双通路说明选择更新含有很强的动作预测成分；VTA 的 APE 归属再由神经时间顺序单独检验。结果后时段目前更适合用简洁的标量 RPE 描述，而行为中独立得到的被动结果归因参数还能直接迁移到多巴胺。行为结构、时间顺序、误差表示和行为→神经参数迁移因此形成四个彼此独立的检验。</div>
</div>'''
    else:
        s = replace_once(
            s,
            "A single social outcome changes the next decision, recent episodes are accumulated over minutes, and part of the learned state persists into the next session.",
            "A single outcome immediately resets the need for further social-information sampling, recent episodes accumulate over minutes, and part of the learned state persists into the next session.",
        )
        s = replace_once(
            s,
            '<div class="card good"><div class="metric-label">Immediate outcomes reshape the next choice</div><div class="metric">Seconds</div><p>After Active or Passive outcomes, stopping rises immediately; re-entry falls by about 8–9 pp.</p></div>',
            '<div class="card good"><div class="metric-label">One outcome immediately resets the need for more social information</div><div class="metric">Outcome controls re-sampling</div><p>Relative to Unrewarded, the next re-entry into Observe falls by 9.0 pp after Active and 8.3 pp after Passive. In learners, the Active-driven fast-switch contrast grows from 4.3 pp early to 10.8 pp late in training (P=.041).</p></div>',
        )
        slm_block = '''<div id="slm-learning-axis-bridge-v75">
<div class="section-kicker" style="margin-top:28px">Different SLM coordinates track different aspects of learning</div>
<div class="cards-4" style="margin-top:12px">
<div class="card good"><div class="metric-label">Sampling policy changes with learning</div><div class="metric">Policy change tracks SRI gain</div><p>Across all 40 animals, training-related policy change correlates with SRI gain: Spearman ρ=.453, P=.00337.</p></div>
<div class="card info"><div class="metric-label">Action prediction error tracks the learned phenotype</div><div class="metric">APE change tracks late SRI</div><p>Training-related change in |APE| correlates with late SRI: ρ=.383, P=.0146.</p></div>
<div class="card violet"><div class="metric-label">Outcome error tracks social-to-action conversion</div><div class="metric">RPE change tracks conversion gain</div><p>Training-related change in |RPE| correlates with the gain in observation-to-successful-action conversion: ρ=.615, P=2.43×10⁻⁵.</p></div>
<div class="card good"><div class="metric-label">Social credit tracks successful use of sampled information</div><div class="metric">Credit separation tracks Active success</div><p>Late social-credit separation correlates with the probability of Active success after observation: ρ=.558, P=.000181.</p></div>
</div>
<div class="callout"><strong>Why this matters.</strong> Policy, APE, RPE and social credit align with different learning phenotypes. These correlations provide complementary computational coordinates; neural timing and JAWS perturbation below provide separate tests of their neural and causal meaning.</div>
</div>'''
        vta_block = '''<div id="vta-multiaxis-v75">
<div class="section-kicker" style="margin-top:28px">Four independent tests connect SLM to dopamine</div>
<div class="cards-4" style="margin-top:12px">
<div class="card good"><div class="metric-label">Behavior first separates reward and action errors</div><div class="metric">APE dominates; RPE adds a smaller increment</div><p>Held-animal behavior gives Brier=.1911 for APE-only versus .2273 for RPE-only; APE beats RPE in 27/27 animals (P=1.49×10⁻⁸). The dual RPE+APE model improves further in 24/27 animals (P=4.92×10⁻⁷).</p></div>
<div class="card info"><div class="metric-label">Neural timing provides the mechanistic adjudication</div><div class="metric">SLM succeeds on 3/3 temporal axes</div><p>Pre-outcome policy P=.0469, middle APE P=.0416, and post-outcome RPE P=.0195; generic Q/RPE is supported only at Post.</p></div>
<div class="card violet"><div class="metric-label">Post-outcome error representation can be adjudicated separately</div><div class="metric">Current data favor a scalar RPE description</div><p>Across nine animals, signed RPE+|RPE| gives mean held-out MSE gain=.01518 versus .00544 for signed outcome-vector PE and .00871 with vector magnitudes. Vector terms add no gain after scalar RPE (−.00035, P=1.0).</p></div>
<div class="card good"><div class="metric-label">Behavior-derived Passive credit transfers to dopamine</div><div class="metric">No neural retuning is required</div><p>Passive credit selected from behavior alone outperforms fixed credit=.75 and 1.0 for ActionBout dopamine in 9/9 animals for both comparisons (P=.0039 each).</p></div>
</div>
<div class="callout"><strong>Four tests answer four different questions.</strong> The behavioral RPE/APE family establishes a strong action-prediction component in choice updating; neural attribution of APE is then tested independently by timing. Post-outcome dopamine is currently more parsimoniously summarized by scalar RPE, while a behavior-derived Passive-credit parameter transfers directly to dopamine. Behavioral architecture, temporal order, error representation and behavior-to-neural parameter transfer therefore provide independent constraints on the same SLM framework.</div>
</div>'''

    s = insert_before_first_figure(s, "slm", slm_block, "slm-learning-axis-bridge-v75")
    s = insert_before_first_figure(s, "vta", vta_block, "vta-multiaxis-v75")
    p.write_text(s, encoding="utf-8")

patch_page("index-zh.html", zh=True)
patch_page("index.html", zh=False)
print("v75 dynamics/SLM/VTA patch applied or already present")
