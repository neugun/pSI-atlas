from pathlib import Path
import re, html

ROOT=Path(__file__).resolve().parents[1]

EN = {
"phenotype": {
 "h2":"Mice learn not just to watch others, but to turn social observation into their own action",
 "p":"Across training, the dominant change is not simply more looking. Animals become better at converting a socially informative observation into their own successful feeding action.",
 "sig":"This identifies the core learned operation in SOE: social learning is an improvement in information-to-action conversion, not merely an increase in observation.",
 "cards":[]
},
"information": {
 "h2":"Animals seek social information when it is useful for deciding what to do next",
 "p":"The value of another animal’s state is not fixed. It depends on the observer’s own situation and on what the animal has learned, showing that social observation is used as an adaptive decision resource.",
 "sig":"This reframes social observation as active information foraging: the animal evaluates when another animal is worth consulting, rather than passively reacting to social cues.",
 "cards":[
 ("Social cues have measurable decision value","Useful when they change the next choice"),
 ("The value of social information is learned","Reliance changes with experience"),
 ("Need for social information depends on self-state","Far from food, social cues matter more")]
},
"dynamics": {
 "h2":"Social experience is integrated across seconds, minutes and days rather than stored in one memory trace",
 "p":"A single social outcome changes the next decision, recent episodes are accumulated over minutes, and part of the learned state persists into the next session.",
 "sig":"This establishes a hierarchy of social memory before fitting the final model, providing a behavioral reason for a multiscale learning state instead of adding complexity only to improve prediction.",
 "cards":[
 ("Immediate outcomes reshape the next choice","Seconds"),
 ("Recent social history is integrated","Minutes"),
 ("Experience carries across sessions","Across days")]
},
"slm": {
 "h2":"A compact Social Learning Model explains when mice seek social information and how experience changes that policy",
 "p":"The model compresses current state, recent social history, sampling policy and outcome-specific credit into variables that remain interpretable enough to test directly in neural recordings and causal perturbations.",
 "sig":"The contribution is a bridge from behavior to mechanism: the same compact variables that explain choice can be asked of dopamine activity, perturbation experiments and generative agents.",
 "cards":[
 ("Simple behavioral rules are not enough","More than clock or repetition"),
 ("Classical reward learning misses key structure","Social learning is not generic RL"),
 ("A compact SLM reaches near-ceiling prediction","Mechanistic and predictive"),
 ("Flexible black boxes add little to the main conclusion","Interpretability without losing performance"),
 ("The latent computations are recoverable","Mechanisms are identifiable")]
},
"swm": {
 "h2":"A data-driven world model independently recovers the SLM decision structure and reveals an additional prospective social-value signal",
 "p":"SWM is trained without writing the SLM equations into the model. It independently recovers a policy-relevant SLM-like subspace and also learns whether observing now is likely to improve the animal’s later feeding outcome.",
 "sig":"This is an independent validation and extension of the mechanistic model: the central SLM coordinates are not only hand-specified features, while the world model also exposes a prospective variable the original SLM did not contain.",
 "cards":[
 ("Prospective social efficacy adds beyond visible cues","Will observing now pay off later?"),
 ("The efficacy signal requires real social content","Not a generic motion signal"),
 ("SLM-like coordinates have a policy function","The shared subspace helps choose when to observe"),
 ("SWM retains dynamics beyond the SLM state","A richer representation of the future")]
},
"feed": {
 "h2":"What the demonstrator is doing—not merely being recently observed—changes the learner’s next feeding decision",
 "p":"After controlling the learner’s current state and simple observation recency, the content of the sampled social event still predicts whether the learner will feed.",
 "sig":"This closes the central behavioral loop from observation to action: specific social content is converted into the observer’s own feeding decision, rather than social observation acting as a nonspecific arousal cue.",
 "cards":[
 ("The learner cohort provides the mechanistic test","Same animals, defined learning state"),
 ("Seeing the demonstrator eat promotes the learner’s own feeding","Observed feeding becomes action"),
 ("The effect survives current-state controls","Not explained by where the learner already was"),
 ("Content-to-action transfer strengthens with experience","Learning improves conversion")]
},
"agent": {
 "h2":"When the SLM rules are run forward, they recreate the local organization of social learning",
 "p":"A predictive model can fit the next choice without capturing the process that generated learning. The closed-loop agent asks whether the fitted policy and update rules can actually regenerate the behavioral organization seen in mice.",
 "sig":"This moves the model from correlation toward generative sufficiency: the SLM is tested as a working controller that produces social-learning structure, not only as a decoder of recorded behavior.",
 "cards":[
 ("Global trajectories are not the key discriminator","Simple agents can reproduce broad trends"),
 ("SLM is strongest where social strategy matters","Local organization is reproduced"),
 ("Generated state occupancy resembles real learners","Internal behavioral organization is recovered"),
 ("Independent recurrent agents rediscover SLM coordinates","A convergent solution")]
},
"vta": {
 "h2":"VTA dopamine follows the computation of social learning in sequence—from deciding to observe to learning from the outcome",
 "p":"Before the social outcome is known, dopamine reflects the decision to sample and the surprise associated with that sampling action. After the outcome, dopamine reflects reward/value and social-credit updating.",
 "sig":"The key advance is temporal dissection. Outcome-related dopamine can look like ordinary RPE, but the full episode contains earlier computations that generic post-outcome RPE cannot explain.",
 "cards":[
 ("First: decide whether social information is worth sampling","Sampling policy"),
 ("Next: register whether the sampling action was expected","Sampling surprise"),
 ("Finally: use the outcome to update future behavior","Teaching and credit")]
},
"architecture": {
 "h2":"The study resolves a closed social-learning loop: access information, choose when to sample it, convert it into action, then learn from the outcome",
 "p":"Behavior, modeling, dopamine timing and perturbations converge on four linked operations that together explain how social information changes future behavior.",
 "sig":"This is the unifying mechanism of the work: social learning is not one signal or one brain response, but a closed computation linking information access, active sampling, action conversion and outcome-dependent teaching.",
 "cards":[
 ("Social information must first be accessible","See"),
 ("The animal chooses when it is worth sampling","Sample"),
 ("Sampled content changes the animal’s own action","Act"),
 ("Outcomes update the next sampling decision","Learn")]
},
"causality": {
 "h2":"Visual access and VTA teaching are causally distinct steps in the social-learning loop",
 "p":"Blocking useful visual-social information weakens what can be learned from the demonstrator, whereas inhibiting VTA after successful social outcomes weakens the teaching step that updates future social sampling.",
 "sig":"Two interventions therefore hit different links of the same mechanism: one limits information entering the system, the other limits how a successful social outcome is assigned credit and stored.",
 "cards":[
 ("Disrupting visual information reduces successful conversion","Information access is necessary"),
 ("Timing controls show the effect is outcome-linked","Not just light or time"),
 ("VTA inhibition suppresses social-credit updating","The affected computation is identifiable"),
 ("Repeated teaching deficits accumulate across the session","Acute disruption becomes persistent state change")]
},
"generalization": {
 "h2":"Social-learning variables carry beyond the training task into later food and threat decisions",
 "p":"The same animals were tested in new behavioral settings. Social credit predicts later food-related behavior, while sampling-prediction-error sensitivity tracks later responses to unexpected threat.",
 "sig":"These results suggest that the learned computations are reusable behavioral variables rather than task-specific fit parameters, while the strongest selection-corrected comparison remains a boundary on how broadly that claim can be made.",
 "cards":[
 ("Social credit predicts later food decisions","A learning variable transfers"),
 ("Sampling surprise tracks later threat reactivity","A second computation transfers"),
 ("Matched computations map to matched behaviors","Function-specific generalization"),
 ("Behavior-only predictors remain a serious comparator","Promising, not universal")]
},
"crossspecies": {
 "h2":"The same computational motifs recur across species and social-learning tasks",
 "p":"External datasets do not all test the same claim, so they are organized by computation: multiscale state, source-specific credit, state-gated information value, and the separation of information sampling from later action.",
 "sig":"This positions the work as a computation-level framework rather than a single mouse paradigm: the strongest external support is reserved for matched independent-unit tests, while component and architectural analogies are labeled separately.",
 "cards":[
 ("Multiscale social state generalizes beyond this mouse task","Human and rat support"),
 ("Credit depends on who supplied the information","Source identity matters"),
 ("The value of social information is state-dependent across tasks","Information value is conditional"),
 ("Information sampling and later action can be separated","A recurring two-stage architecture")]
},
"resources": {
 "h2":"Every major claim is traceable to its analysis and source data",
 "p":"The page presents the biological story; the linked authorities, source tables and audit files make each mechanistic claim reproducible and distinguish current evidence from retired or exploratory analyses.",
 "sig":"The contribution here is transparency: interpretation, quantitative evidence and analysis provenance remain connected instead of being hidden behind summary figures.",
 "cards":[]
}
}

ZH = {
"phenotype": {
 "h2":"小鼠学到的不是“多看同伴”，而是把社会观察更有效地变成自己的行动",
 "p":"训练中最关键的变化并不是观察次数简单增加，而是一次有用的社会观察越来越能够转化成观察者自己的成功进食行动。",
 "sig":"这一步确定了 SOE 真正被学习的基本操作：社会学习的核心是“信息→行动”的转化效率，而不是单纯增加对同伴的注意。",
 "cards":[
 ("这套策略在大多数动物中被学会","多数小鼠获得社会学习"),
 ("学习提高观察到行动的转化","看见之后更会行动"),
 ("转化能力与总体学习同步增强","转化越好，学习越强")]
},
"information": {
 "h2":"小鼠会在社会信息真正有助于下一步决策时主动利用它",
 "p":"同伴状态的价值不是固定的，它取决于观察者自己的状态，也会随学习改变，说明社会观察是一种主动的信息采样。",
 "sig":"这把社会观察从“看到同伴后的反应”推进成主动 information foraging：动物会判断什么时候值得参考另一个个体。",
 "cards":[
 ("社会线索确实具有决策价值","能改变下一步选择才有用"),
 ("社会信息的价值会被学习重塑","经验改变依赖程度"),
 ("是否需要社会信息取决于自身状态","离食口更远时更依赖同伴")]
},
"dynamics": {
 "h2":"社会经验不是存在一条记忆痕迹里，而是同时跨越秒、分钟和跨天时间尺度",
 "p":"一次 outcome 会立即改变下一次决策，最近多次社会经验会在数分钟内累积，而部分学习状态还能延续到下一次 session。",
 "sig":"这些时间尺度在最终模型之前就由行为数据独立得到，因此 multiscale memory 是生物学结果，不是为了提高拟合而事后添加的复杂度。",
 "cards":[
 ("一次结果立即改变下一步选择","秒级记忆"),
 ("近期社会经历会被连续整合","分钟级记忆"),
 ("部分学习状态延续到下一次 session","跨天记忆")]
},
"slm": {
 "h2":"一个紧凑的社会学习模型解释小鼠什么时候主动获取社会信息，以及经验如何改变这种策略",
 "p":"SLM 把当前状态、近期社会经历、采样策略和 outcome-specific credit 压缩成一组仍然可以被神经记录和因果实验直接检验的变量。",
 "sig":"这项工作的核心贡献是把行为描述推进成机制变量：同一组计算既解释选择，又可以继续去问 VTA、JAWS 和生成式 agent 是否真的实现这些步骤。",
 "cards":[
 ("简单行为规则解释不够","不只是时间或重复选择"),
 ("经典 reward-learning 仍缺少关键结构","社会学习不等于普通 RL"),
 ("紧凑 SLM 已接近灵活模型的预测上限","既能解释，也能预测"),
 ("黑箱模型没有改变核心机制结论","保留可解释性而不明显损失性能")]
},
"swm": {
 "h2":"一个不预先写入 SLM 方程的世界模型，独立恢复了相同决策结构，并发现额外的前瞻性社会价值信号",
 "p":"SWM 自己学习行为序列后，出现了参与 Observe policy 的 SLM-like subspace；同时它还学到“现在去观察，之后是否更可能成功进食”的 prospective social efficacy。",
 "sig":"这提供了对 SLM 的独立数据驱动验证，也把模型向前推进：核心坐标不是单纯人工指定，而 SWM 还揭示了原始 SLM 没有显式包含的新变量。",
 "cards":[
 ("前瞻性社会效益超出当前可见线索","现在观察以后是否会更有用"),
 ("这个信号依赖真实的社会内容","不是普通运动或视觉信号"),
 ("SLM-like 坐标真的参与采样决策","共同 subspace 帮助决定何时观察"),
 ("SWM 还保留 SLM 之外的未来动力学","更丰富的未来状态表示")]
},
"feed": {
 "h2":"真正改变 learner 下一步进食的，是它看到同伴正在做什么，而不只是“刚刚看过同伴”",
 "p":"控制 learner 当前状态和简单 observation recency 后，采样到的具体社会内容仍然决定之后是否更容易 Feed。",
 "sig":"这一步闭合了整项工作的行为链条：特定社会内容能够被观察者转化成自己的进食行动，而不是社会观察只产生一个非特异性的 arousal 效应。",
 "cards":[
 ("机制检验来自同一套 learner cohort","在明确学习状态下检验"),
 ("看到示范鼠进食会促进 learner 自己进食","社会内容变成自己的行动"),
 ("控制当前状态后效应仍然存在","不是因为动物本来就处在易进食状态"),
 ("信息到行动的转化会随经验增强","学习提高 content-to-action transfer")]
},
"agent": {
 "h2":"把 SLM 真正运行起来后，同一套规则可以重新生成社会学习的局部组织结构",
 "p":"只预测下一次选择并不能证明模型抓住了学习过程。closed-loop agent 让 outcome 持续回写内部状态，再检验它是否自己生成真实小鼠那样的社会学习轨迹与策略。",
 "sig":"这把 SLM 从相关性预测推进到生成充分性：它被检验为一个能够运行并产生行为组织的 controller，而不只是事后读取行为的 decoder。",
 "cards":[
 ("全局轨迹不是最能区分机制的指标","简单 agent 也能复制总体趋势"),
 ("SLM 的优势集中在真正的社会策略组织","局部社会策略被重建"),
 ("生成出的状态占据接近真实 learner","内部行为组织被重建"),
 ("独立 recurrent agent 也重新找到 SLM 坐标","不同优化路径得到收敛解")]
},
"vta": {
 "h2":"VTA dopamine 按社会学习真实发生的顺序编码：先决定要不要观察，再评估采样是否出乎预期，最后根据结果学习",
 "p":"在社会 outcome 出现之前，dopamine 已经包含采样决策和采样动作误差；outcome 出现后，才进入 reward/value 与 social-credit updating。",
 "sig":"真正的新意是把 dopamine 放回一次完整 social-learning episode 的时间顺序。只看 outcome 后可以得到普通 RPE；加入更早的两个阶段后，单一 RPE 已不足以解释整段 computation。",
 "cards":[
 ("第一步：判断社会信息值不值得采样","是否去观察"),
 ("第二步：判断这次采样动作是否符合预期","采样动作的 surprise"),
 ("第三步：用 outcome 更新之后的行为","teaching 与 credit")]
},
"architecture": {
 "h2":"整项工作解析出一个闭环社会学习机制：看到信息、选择采样、转成行动，再用结果更新下一次采样",
 "p":"行为、模型、dopamine timing 和 causal perturbation 最终收敛到四个彼此相连的操作，共同解释社会信息如何真正改变未来行为。",
 "sig":"这是整项工作的统一机制：社会学习不是一个单独信号，而是 information access、active sampling、action conversion 和 outcome-dependent teaching 连成的闭环计算。",
 "cards":[
 ("首先必须获得可用的社会信息","看见"),
 ("动物主动选择什么时候值得采样","采样"),
 ("采到的内容改变自己的行为","行动"),
 ("结果再更新下一次采样策略","学习")]
},
"causality": {
 "h2":"视觉信息进入和 VTA teaching 是社会学习闭环中两个可以被分别破坏的因果步骤",
 "p":"Visual Block 限制有用社会内容进入系统；而在成功社会 outcome 后抑制 VTA，则削弱把这次 outcome 写入未来行为的 teaching step。",
 "sig":"两个 manipulation 因而击中同一机制链的不同位置：一个限制“能学到什么”，另一个限制“学到以后如何分配 credit 并保存”。",
 "cards":[
 ("破坏视觉社会信息会降低成功转化","信息进入是必要的"),
 ("时间控制说明效应与 outcome 配对有关","不只是光刺激或时间本身"),
 ("VTA 抑制直接削弱 social-credit updating","受影响的 computation 可以被定位"),
 ("反复 teaching 缺陷会累积成 session-level 状态改变","急性扰动形成持续后果")]
},
"generalization": {
 "h2":"社会学习中得到的计算变量可以带到新任务，预测之后的食物选择和威胁反应",
 "p":"同一批动物后来进入新的 behavioral context。social credit 与之后的 food-related behavior 对应，而 sampling-prediction-error sensitivity 与之后对意外威胁的反应对应。",
 "sig":"这些结果支持 SLM variables 是可复用的行为计算，而不只是原任务的拟合参数；同时 selection-corrected comparator 也明确限制了目前可以把泛化结论说到多强。",
 "cards":[
 ("Social credit 预测之后的食物决策","一个学习变量跨任务保留"),
 ("采样 surprise 对应之后的威胁反应","第二种 computation 也能迁移"),
 ("不同 computation 映射到功能匹配的行为","功能特异的泛化"),
 ("纯行为 predictor 仍然是重要强对照","有泛化，但不是无条件胜出")]
},
"crossspecies": {
 "h2":"相同的社会学习计算在其他物种和任务中反复出现",
 "p":"不同 external dataset 能回答的问题并不相同，因此这里按 computation 来组织：multiscale state、source-specific credit、state-gated information value，以及 information sampling 与 later action 的分离。",
 "sig":"这使工作不再局限于一个 mouse paradigm，而成为一个 computation-level framework；最强的 external support 只来自真正 matched 的 independent-unit test，其余证据继续明确标注为 component 或 architecture analogue。",
 "cards":[
 ("多时间尺度社会状态不只存在于这套 mouse task","Human 与 Rat 提供独立支持"),
 ("credit assignment 会保留信息来源身份","是谁提供信息很重要"),
 ("社会信息的价值在不同任务中都受状态门控","信息价值是条件性的"),
 ("信息采样与之后的行动可以被分成两个阶段","反复出现的两阶段架构")]
},
"resources": {
 "h2":"每一个主要结论都可以追溯到对应分析和源数据",
 "p":"网页负责讲清楚生物学故事；authority、source table 与 audit file 负责把机制解释、统计证据和分析来源保持连接，并区分当前证据与已经淘汰的探索结果。",
 "sig":"这部分的贡献是可追溯性：读者看到的不只是漂亮 summary，而是可以回到具体数据与分析 contract 的完整证据链。",
 "cards":[]
}
}

HERO_EN=("A mechanistic account of social learning: how mice decide when to observe, turn social information into action, and learn from the outcome",
"Social learning emerges here as a closed computation rather than a single response: animals decide when another animal is worth observing, integrate social experience across time, convert sampled content into their own feeding, and use VTA-dependent outcome signals to update future sampling. SLM provides an interpretable mechanism, SWM independently tests and extends it, and causal and external datasets probe how far the computation holds.")

HERO_ZH=("一个社会学习的闭环机制：小鼠如何决定什么时候观察同伴、把社会信息变成自己的行动，并从结果中继续学习",
"这项工作把社会学习从一个行为现象推进成一套闭环 computation：动物先判断同伴是否值得观察，把社会经验跨时间整合，把采到的内容转成自己的进食，再利用 VTA-dependent outcome signal 更新下一次社会信息采样。SLM 提供可解释机制，SWM 做独立数据驱动验证与扩展，因果实验和外部数据继续检验这套 computation 的边界。")

OVERVIEW_CARDS_EN=[
("A compact mechanistic model reaches flexible-model performance","Mechanism without a black box"),
("An independent world model recovers and extends the same computation","Hypothesis meets data-driven learning"),
("Dopamine follows the sequence of social learning","Decide → sample → learn"),
("VTA activity is required for post-outcome social teaching","A causal teaching signal"),
("Observed feeding changes the learner’s own feeding","Social content becomes action"),
("Core computations recur beyond this mouse task","Cross-task convergence")]
OVERVIEW_CARDS_ZH=[
("紧凑机制模型达到接近灵活黑箱的预测能力","不用黑箱也能解释行为"),
("独立 world model 重新找到并扩展同一 computation","假说与数据驱动模型收敛"),
("Dopamine 跟随社会学习的真实计算顺序","决定 → 采样 → 学习"),
("VTA activity 对 outcome 后的社会 teaching 是必要的","因果 teaching signal"),
("看到同伴进食会改变 learner 自己的进食","社会内容真正变成行动"),
("核心 computation 超出单一 mouse task","跨任务收敛")]

def add_style(s):
    css='''\n<style id="section-meaning-v69">\n.section-significance{margin:14px 0 20px;padding:13px 16px;border-radius:12px;background:#f6f2ed;border:1px solid #eadfd2;color:#334b60;font-size:14px;line-height:1.55}\n.section-significance strong{color:#8a4f2b}\n.metric{font-size:clamp(18px,2vw,25px)!important;line-height:1.18!important;letter-spacing:-.02em!important}\n.metric-label{text-transform:none!important;letter-spacing:.02em!important;font-size:11.5px!important;line-height:1.35!important}\n@media(max-width:620px){.section-significance{font-size:13px}.metric{font-size:19px!important}}\n</style>\n'''
    if 'section-meaning-v69' not in s:
        s=s.replace('</head>',css+'</head>')
    return s

def section_bounds(s,sid):
    m=re.search(r'<section\b[^>]*\bid="'+re.escape(sid)+r'"[^>]*>',s)
    if not m: raise RuntimeError("section not found "+sid)
    start=m.start()
    n=re.search(r'<section\b',s[m.end():])
    end=(m.end()+n.start()) if n else s.find('</main>',m.end())
    return start,end

def patch_section(s,sid,cfg,lang):
    start,end=section_bounds(s,sid)
    block=s[start:end]
    # heading + section intro + standalone significance statement
    pat=r'<div class="section-head">\s*<div>\s*<div class="section-kicker">(.*?)</div>\s*<h2>.*?</h2>\s*</div>\s*<p>.*?</p>\s*</div>'
    sig_label="Why this matters" if lang=="en" else "这项工作推进了什么"
    def repl_head(m):
        head='<div class="section-head"><div><div class="section-kicker">'+m.group(1)+'</div><h2>'+html.escape(cfg["h2"])+'</h2></div><p>'+html.escape(cfg["p"])+'</p></div>'
        sig='<div class="section-significance"><strong>'+sig_label+' · </strong>'+html.escape(cfg["sig"])+'</div>'
        return head+'\n'+sig
    block,n=re.subn(pat,repl_head,block,count=1,flags=re.S)
    if n!=1: raise RuntimeError(f"head patch failed {sid} {n}")
    # patch first N metric cards in visible order
    cards=cfg.get("cards",[])
    pos=0
    for lab,metric in cards:
        cm=re.search(r'<div class="card(?: [^"]*)?">\s*<div class="metric-label">.*?</div>\s*<div class="metric">.*?</div>\s*<p>.*?</p>\s*</div>',block[pos:],flags=re.S)
        if not cm: raise RuntimeError(f"card patch failed {sid} at {lab}")
        a=pos+cm.start(); b=pos+cm.end()
        old=block[a:b]
        new=re.sub(r'(<div class="metric-label">).*?(</div>)',r'\1'+html.escape(lab)+r'\2',old,count=1,flags=re.S)
        new=re.sub(r'(<div class="metric">).*?(</div>)',r'\1'+html.escape(metric)+r'\2',new,count=1,flags=re.S)
        block=block[:a]+new+block[b:]
        pos=a+len(new)
    return s[:start]+block+s[end:]

def patch_overview(s,h1,lede,cards,lang):
    start,end=section_bounds(s,"overview")
    block=s[start:end]
    block=re.sub(r'(<h1>).*?(</h1>)',r'\1'+html.escape(h1)+r'\2',block,count=1,flags=re.S)
    block=re.sub(r'(<p class="lede">).*?(</p>)',r'\1'+html.escape(lede)+r'\2',block,count=1,flags=re.S)
    central=("This work turns social learning into a testable closed-loop mechanism linking active information sampling, content-to-action conversion and outcome-dependent teaching."
             if lang=="en" else
             "这项工作把社会学习从一个现象推进成可检验的闭环机制：主动信息采样、content-to-action conversion 与 outcome-dependent teaching 被连成同一条因果计算链。")
    hero_sig='<div class="section-significance"><strong>'+("Central contribution" if lang=="en" else "核心贡献")+' · </strong>'+central+'</div>'
    eq=block.find('<div class="equation chain">')
    if eq>0 and 'Central contribution' not in block and '核心贡献' not in block:
        block=block[:eq]+hero_sig+'\n'+block[eq:]
    # Hero grid only
    hg=block.find('<div class="hero-grid">')
    he=block.find('</div>',hg)
    # Need full grid block; find before equation.
    eqpos=block.find('<div class="equation chain">')
    grid=block[hg:eqpos]
    pos=0
    for lab,metric in cards:
        cm=re.search(r'<div class="card(?: [^"]*)?">\s*<div class="metric-label">.*?</div>\s*<div class="metric">.*?</div>\s*<p>.*?</p>\s*</div>',grid[pos:],flags=re.S)
        if not cm: raise RuntimeError("overview card failed "+lab)
        a=pos+cm.start(); b=pos+cm.end(); old=grid[a:b]
        new=re.sub(r'(<div class="metric-label">).*?(</div>)',r'\1'+html.escape(lab)+r'\2',old,count=1,flags=re.S)
        new=re.sub(r'(<div class="metric">).*?(</div>)',r'\1'+html.escape(metric)+r'\2',new,count=1,flags=re.S)
        grid=grid[:a]+new+grid[b:]; pos=a+len(new)
    block=block[:hg]+grid+block[eqpos:]
    return s[:start]+block+s[end:]

for fn,CFG,HERO,OCARDS,lang in [
    ("index.html",EN,HERO_EN,OVERVIEW_CARDS_EN,"en"),
    ("index-zh.html",ZH,HERO_ZH,OVERVIEW_CARDS_ZH,"zh")]:
    path=ROOT/fn
    s=path.read_text(encoding="utf-8")
    s=add_style(s)
    s=patch_overview(s,HERO[0],HERO[1],OCARDS,lang)
    for sid,cfg in CFG.items():
        s=patch_section(s,sid,cfg,lang)
    path.write_text(s,encoding="utf-8")
    print(fn,"patched",len(s))
