from pathlib import Path
import ast, re
from bs4 import BeautifulSoup, NavigableString

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/"index-zh.html"
CFGFILE=ROOT/"analysis"/"zh_story_config_v74.py"

def load_literal(name):
    tree=ast.parse(CFGFILE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id==name:
                    return ast.literal_eval(node.value)
    raise KeyError(name)

hero_cards=load_literal("hero_cards")
atlas=load_literal("atlas")
SECTIONS=load_literal("SECTIONS")

raw=HTML.read_text(encoding="utf-8")
orig_links=set(re.findall(r'(?:href|src|srcset)="([^"]+)"',raw))
soup=BeautifulSoup(raw,"html.parser")

def set_html(tag, html):
    frag=BeautifulSoup(html,"html.parser")
    tag.clear()
    for child in list(frag.contents):
        tag.append(child)

def visible_cards(sec):
    out=[]
    for c in sec.find_all("div",class_="card"):
        if c.find_parent("details") is None and c.find("div",class_="metric-label") and c.find("div",class_="metric"):
            out.append(c)
    return out

def visible_figcaptions(sec):
    out=[]
    for f in sec.find_all("figure"):
        if f.find_parent("details") is None:
            fc=f.find("figcaption")
            if fc: out.append(fc)
    return out

# Hero.
hero=soup.find("section",id="overview")
hero.find("h1").string="一个社会学习闭环：小鼠如何决定何时观察同伴、如何把社会信息转化为自身行动，并根据结果继续学习"
hero.find("p",class_="lede").string="这项工作把社会学习拆成一条可检验的闭环：小鼠先判断同伴是否值得观察，把短期和跨天经验整合成采样策略；观察到的具体内容会改变自身进食；结果出现后，腹侧被盖区多巴胺参与更新未来的社会信息采样。社会学习模型（SLM）给出可解释机制，社会世界模型（SWM）提供独立的数据驱动检验和扩展。"

if not hero.find(string=lambda x:isinstance(x,str) and "主要术语｜" in x):
    glossary=BeautifulSoup('''<div class="bio-logic"><strong>主要术语｜</strong>社会观察进食（SOE）；社会学习模型（SLM）；社会世界模型（SWM）；腹侧被盖区（VTA）；多巴胺（DA）；动作预测误差（APE）；奖励预测误差（RPE）；强化学习（RL）；社会反应指数（SRI）。JAWS 指本研究使用的红移光遗传抑制工具。预测指标中，AUC 表示曲线下面积，Brier 表示概率校准误差，NLL 表示负对数似然，RMSE 表示均方根误差，SEM 表示均值标准误。</div>''',"html.parser").div
    hero.find("div",class_="hero-grid").insert_before(glossary)

hgrid=hero.find("div",class_="hero-grid")
hcards=[x for x in hgrid.find_all("div",recursive=False) if "card" in (x.get("class") or [])]
for c,(lab,metric,body) in zip(hcards,hero_cards):
    c.find("div",class_="metric-label").string=lab
    c.find("div",class_="metric").string=metric
    c.find("p").string=body

sig=hero.find("div",class_="section-significance")
set_html(sig,'<strong>核心贡献 · </strong>这项工作把社会学习从一个现象推进成可检验的闭环机制：主动信息采样、社会内容到自身行动的转化，以及结果依赖的教学过程被连成同一条因果计算链。')
eq=hero.find("div",class_="equation")
set_html(eq,'社会状态 → 主动选择观察 → 采到的社会内容 → 自身进食<span class="sub">反馈：社会结果 → 结果后的来源特异归因与价值更新 → 未来观察策略</span>')
hero.find("p",class_="prepub").string="页面按照生物学问题顺序展开：行为获得 → 信息价值 → 多时间尺度记忆 → 社会学习模型 → 数据驱动世界模型 → 社会内容到自身行动的转化 → 神经实现 → 因果拆解 → 机制综合 → 后续泛化 → 跨任务证据。"

# Overview contribution cards.
kickers=hero.find_all("div",class_="section-kicker")
for k in kickers:
    if "当前结果图谱" in k.get_text() or "一页看懂" in k.get_text():
        k.string="一页看懂这项工作的贡献"
acards=[c for c in hero.find_all("div",class_="card") if c.find("div",class_="series-index")]
for c,(title,body) in zip(acards,atlas):
    c.find("h3").string=title
    c.find("p").string=body

# Main section narrative.
for sid,cfg in SECTIONS.items():
    sec=soup.find("section",id=sid)
    if not sec: continue
    head=sec.find("div",class_="section-head")
    if head:
        h2=head.find("h2")
        if h2: h2.string=cfg["h2"]
        p=head.find("p")
        if p: p.string=cfg["p"]
    sig=sec.find("div",class_="section-significance")
    if sig:
        set_html(sig,'<strong>这项工作推进了什么 · </strong>'+cfg["sig"])
    guide=sec.find("div",class_="reader-guide")
    if guide and cfg.get("guide"):
        spans=guide.find_all("span")
        for sp,txt in zip(spans,cfg["guide"]):
            sp.string=txt
    cards=visible_cards(sec)
    for c,(lab,metric,body) in zip(cards,cfg.get("cards",[])):
        c.find("div",class_="metric-label").string=lab
        c.find("div",class_="metric").string=metric
        c.find("p").string=body
    figs=visible_figcaptions(sec)
    for fc,cap in zip(figs,cfg.get("caps",[])):
        set_html(fc,cap)

# Natural section kickers.
soup.find("section",id="agent").find("div",class_="section-kicker").string="生成充分性 / 人工智能"
soup.find("section",id="resources").find("div",class_="section-kicker").string="权威版本与源数据"

# Three remaining top-level explanatory boxes.
extra_bio={
"information":'''<strong>为什么下一步必须看记忆｜</strong>状态门控解释当前时刻何时值得采样社会信息；真正的学习还要求一次观察的结果能够影响之后的选择。因此下一节直接测量这种内部状态能保留多久，从下一次决策、约五分钟一直到跨天。''',
"dynamics":'''<strong>核心问题｜</strong>一次社会结果会影响之后多久？数据给出三个可分离尺度：下一次决策的快速调整、约 4.5–7.5 分钟的近期历史，以及延续到下一天且在场次早期最强的短暂先验。'''
}
for sid,html in extra_bio.items():
    x=soup.find("section",id=sid).find("div",class_="bio-logic")
    if x:set_html(x,html)
arch=soup.find("section",id="architecture")
x=arch.find("div",class_="callout")
if x:set_html(x,'''<strong>机制综合｜</strong>SLM 组织社会信息的获取、记忆和来源特异的社会归因；自身进食由很强的自身状态控制器主导，同时接受刚刚采样事件带来的短时内容信号。视觉阻断主要作用于信息进入；JAWS 主要作用于结果后的教学更新。''')

# SLM model explainer.
slm=soup.find("section",id="slm")
contracts=slm.find_all("div",class_="model-contract")
contract_html=[
'''<strong>先分清三个层次。</strong> <b>函数形式</b>看线性/逻辑回归还是非线性/循环网络；<b>学习架构</b>看模型内部维护什么状态，例如经典价值、选择惯性、结构化 SLM 状态或数据驱动潜在状态；<b>计算读出</b>看某个时间点读取采样策略、APE、RPE 或社会结果归因。三者回答的问题不同，不能混成同一个模型列表。''',
'''<strong>行为比较约定。</strong> 主要紧凑模型比较固定同一批 27 只留出动物、同一预测目标和逐动物留出评估；Brier 作为主要概率校准指标，AUC 和对数损失作为辅助。经典强化学习模型使用较窄的状态输入；检验“相同当前输入下 SLM 结构是否仍有价值”时，强对照复用同一当前状态骨架。多层感知机和循环网络只作为容量上限，不直接获得机制解释。''',
'''<strong>后文统一术语。</strong> <b>采样策略</b>是结果出现前选择观察的概率或规则。<b>动作预测误差（APE）</b> = 实际采样动作 − 动作前采样概率，在采样动作发生后、当前社会结果可用前计算。<b>奖励预测误差（RPE）</b>是结果后的奖赏/价值预测误差；Q 学习中 δ = r + γV′ − V。<b>社会结果归因</b>是结果出现后、带有信息来源和结果类别标签的更新。这些量属于不同时间点的计算读出。'''
]
for t,h in zip(contracts,contract_html):set_html(t,h)

family_html=[
'''<div class="model-tag">0 · 直接读出</div><h4>基础发生率 / 时间进程 / 当前状态线性或非线性读出</h4><p><b>原理：</b>直接由可观测当前状态预测选择，不维护学习状态。</p><p><b>关键参数：</b>截距、特征权重、训练数据内选择的正则化；非线性版本额外允许特征交互。</p><p><b>用途：</b>建立没有学习规则时的预测基线。</p>''',
'''<div class="model-tag">1 · 经典学习规则</div><h4>RW / WSLS / Q 学习 / 非对称 Q / 遗忘 Q / 选择惯性</h4><p><b>原理：</b>维护少量价值或选择惯性状态，并在选择或结果之后更新。</p><p><b>关键参数：</b>学习率 α；需要时加入折扣/价值项 γ；非对称 Q 使用正负结果各自的学习率；遗忘 Q 加入遗忘率；选择惯性包含衰减和权重。</p><p><b>用途：</b>提供奖赏学习和重复选择倾向的可解释替代模型；Q 系列在结果后产生 RPE。</p>''',
'''<div class="model-tag">2 · 机制假说</div><h4>SLM 组成模块 → SLM 核心 → 默认 SLM</h4><p><b>原理：</b>当前状态和多时间尺度记忆共同决定观察策略；采样动作后产生 APE；结果出现后更新来源/结果特异的社会归因和价值。</p><p><b>关键参数：</b>多时间尺度状态及衰减、策略读出权重、社会归因和价值学习项；默认行为 SLM 再加入通用选择惯性分支。</p><p><b>用途：</b>作为主要机制模型；策略、APE、社会归因和价值在 VTA 与 JAWS 检验之前已经定义。</p>''',
'''<div class="model-tag">3 · 灵活非线性对照</div><h4>历史多层感知机（MLP） / 完整历史 MLP / 小型循环网络（TinyRNN） / 线性动态网络（LDN）</h4><p><b>原理：</b>不预设 SLM 语义，自由学习非线性历史交互。</p><p><b>关键参数：</b>隐藏层或循环网络权重、隐藏维度、正则化和训练超参数，全部只在训练数据内选择。</p><p><b>用途：</b>作为容量上限和压力测试，检验通用记忆与非线性是否足以解释同一行为。</p>''',
'''<div class="model-tag">4 · 动力学模型</div><h4>社会世界模型（SWM）</h4><p><b>原理：</b>不提供 SLM 方程，直接学习循环潜在状态来预测未来行为和社会动力学。</p><p><b>关键参数：</b>编码器、循环潜在动力学以及未来状态/行为读出，端到端训练。</p><p><b>用途：</b>检验与 SLM 对齐的坐标能否自行出现，并寻找 SLM 没有显式包含的前瞻性社会效益状态。</p>'''
]
for t,h in zip(slm.find_all("div",class_="model-family"),family_html):set_html(t,h)

# Main explanatory boxes by section.
boxes={
"slm":{
 "bio":["""<strong>SLM 回答什么问题｜</strong>SLM 描述当前状态、多时间尺度记忆、社会信息采样和结果特异的社会归因怎样共同决定未来选择。行为预测使用“机制 SLM + 通用选择惯性”的默认版本；神经和因果实验读取机制核心中的策略、APE 和社会归因变量。"""],
 "call":["""<strong>为什么默认 SLM 仍保留选择惯性？</strong> 选择惯性负责吸收通用的重复选择倾向；机制解释主要来自采样策略、APE 和社会结果归因。这些变量随后分别接受 VTA 时间过程和 JAWS 因果实验的独立检验。"""]},
"swm":{
 "bio":["""<strong>什么证据才算独立验证｜</strong>单纯“能从 SWM 潜在状态中解码出 SLM 变量”证据有限，因为不同编码器也可能恢复同一任务信息。更强的检验是从留出 SWM 潜在状态中删除与 SLM 对齐的子空间，并与匹配随机子空间比较行为损失；前瞻性社会效益则另外接受当前线索基线和社会内容扰动检验。"""],
 "call":["""<strong>为什么 SWM 需要单独作为数据驱动验证层？</strong>多层感知机和小型循环网络检验的是“在同一监督预测目标下，通用非线性容量能否解释行为”；SWM 的任务是先学习循环潜在状态，再检验其中的表征、未来预测和潜在子空间功能。因此这里使用 SLM/当前线索基线、社会内容对照和匹配随机子空间删除作为主要对照。""",
 """<strong>整合后的解释｜</strong>当前证据支持两个可分离成分。与 SLM 对齐的坐标构成参与观察选择的任务子空间；SWM 还学到一个前瞻性社会效益变量，表示“现在选择观察会给之后成功进食概率带来多少增量”。这个变量在 SLM 事件前状态和全部当前社会线索之外仍有信息，并且依赖正确的社会内容。"""]},
"feed":{
 "bio":["""<strong>核心问题｜</strong>动物能够看见示范鼠，并不代表它一定使用了其中的信息。关键检验是内容到行动的转化：采样瞬间示范鼠正在进食时，观察者接下来几秒内自身进食的概率是否上升。"""],
 "call":["""<strong>训练阶段边界｜</strong>当前主效应来自学习者组中已经重建的两个自身进食场次。第一到第二场次的原始示范鼠进食效应增强，提供了随训练变化的证据；更严格的预先定义晚期训练网格仍值得在完整自身进食数据重建后单独检验。"""]},
"agent":{
 "bio":["""<strong>为什么需要智能体｜</strong>单步预测只检验下一次选择。生成式检验把候选控制器固定后放进同一个经验社会觅食环境，再比较它们自己产生的学习轨迹、局部策略和行为状态组织。""",
 """<strong>为什么下一步进入 VTA｜</strong>生成充分性说明这些变量足以组织行为，随后还需要检验生物系统在什么时间表达这些计算。因此下一节沿一次完整观察事件的顺序检验采样策略、APE 和结果后的社会归因。"""],
 "call":["""<strong>生物学意义｜</strong>SLM 的主要生成优势出现在局部社会学习策略和行为状态占据；全局学习轨迹更容易被简单 Q 学习或结果信念智能体捕捉。独立循环学习器提供收敛证据：灵活优化得到的策略也能被同一套 SLM 坐标紧凑描述。"""]},
"vta":{
 "bio":["""<strong>三个读出的定义｜</strong>模型先给出观察的动作前概率。APE = 实际采样动作 − 动作前采样概率，描述实际采样相对预期倾向的偏差。观察结果出现后，奖赏/价值和来源特异的社会归因才开始更新。这三个读出对应一次观察事件中连续发生的计算。"""],
 "call":["""<strong>为什么这里的模型集合会变化？</strong>前面的行为模型库比较完整的选择预测系统；VTA 部分比较这些系统产生的候选计算信号。采样策略出现在结果前，APE 出现在采样动作后但结果可用前，RPE 和社会归因出现在结果后。因此结果后 RPE 拟合较好，只能说明它解释结果后的部分多巴胺变化，无法覆盖更早的采样计算。""",
 """<strong>对审稿问题的核心回应｜</strong>这里不要求所有奖赏相关多巴胺都唯一对应 SLM。总体结果后多巴胺可以属于更广泛的奖赏更新过程。真正区分机制的是按事件时间展开后的“结果前采样策略 → 采样 APE → 结果后更新”序列。"""]},
"causality":{
 "bio":["""<strong>术语统一｜</strong>JAWS 的场次内终点统一称为“结果后的主动社会归因更新”；多次更新累积成场次尺度的主动社会归因状态。APE 位于更早的采样阶段，表示“实际动作 − 动作前策略概率”。"""],
 "call":["""<strong>选择性的准确含义｜</strong>通用主动 Q 值的累积也会变慢，因此因果结论落在分支层面：VTA 抑制对成功主动结果后的社会归因教学损害最清楚，同时总体社会信息采样仍然保留。这里不把结论限定为只有一个数学变量发生变化。"""]},
"generalization":{
 "bio":["""<strong>两条不同的生物学预测｜</strong>社会归因的维持程度应与既往社会经验如何改变陌生食物行动的启动相关；APE 敏感性则应与之后遇到意外社会事件时的反应强度相关。强对照模型分别检验这些潜在变量能否提供简单 SOE 行为之外的额外信息。"""],
 "call":["""<strong>结论分层｜</strong>食物分支支持超出简单 SOE 行为的增量预测；恐惧分支支持较强的功能匹配机制关联；2×2 映射支持计算表型的模块化。当前 6 只小鼠的样本仍不足以证明跨领域的独立潜在变量具有唯一解释力，下一批前瞻性动物应在分析前冻结变量定义和后续行为终点。"""]},
"crossspecies":{
 "bio":["""<strong>怎样判断保守计算｜</strong>当一个计算在独立留出动物或受试者上超过匹配替代模型时，证据等级最高。组成检验说明某一个操作可以迁移；嵌套的灵长类结果说明同一数据集内部的一致性；架构类比说明任务分解方式相近。"""],
 "call":["""<strong>当前跨任务结论｜</strong>任务匹配的多时间尺度状态在人类和大鼠中得到最强的群体层面外部支持。来源标记的社会归因和状态门控的信息价值在多个社会任务中得到收敛的组成证据。信息采样与后续行动的分离目前以 SOE 的直接证据最强，外部数据主要提供架构类比。猕猴冻结核心迁移提示 SOE 循环动力学具有可复用性，但灵长类群体层面确认仍需要更多独立动物。""",
 """<strong>灵长类 RPE 审计｜</strong>Noritake/Isoda 公开数据提供的是已经按 RPE 分类的人群对象；再用同一批已筛选细胞估计 RPE 斜率会形成选择循环。因此目前只把来源标记的社会归因保留为文献/审计支持，等待逐试次数据进行半样本或独立留出验证。"""]}
}
for sid,d in boxes.items():
    sec=soup.find("section",id=sid)
    bios=[x for x in sec.find_all("div",class_="bio-logic") if x.find_parent("details") is None]
    calls=[x for x in sec.find_all("div",class_="callout") if x.find_parent("details") is None]
    for t,h in zip(bios,d.get("bio",[])):set_html(t,h)
    for t,h in zip(calls,d.get("call",[])):set_html(t,h)

# Technical appendix: original model identifiers may remain in English; explain this explicitly.
for det in slm.find_all("details"):
    sm=det.find("summary")
    if sm and "behavioral model zoo" in sm.get_text():
        sm.string="完整行为模型库（全部已审计模型）"
        p0=det.find("p")
        if p0:p0.string="表中模型原名保留，用于与代码和结果文件逐项对应。奖励预测误差（RPE）属于模型产生的计算信号；RPE、采样策略和 APE 的神经比较在 VTA 部分单独展开。"

vta=soup.find("section",id="vta")
for det in vta.find_all("details"):
    sm=det.find("summary")
    if sm and "VTA signal zoo" in sm.get_text():
        sm.string="完整 VTA 候选信号库（固定时间轴）"
        p0=det.find("p")
        if p0:p0.string="这里比较各类行为模型产生的候选计算信号，重点是不同时间点的神经计算读出；模型类别原名保留，用于与分析文件对应。"
        th=det.find_all("th")
        labels=["候选模型类别","结果前早期","中段","结果后","正且显著"]
        for t,l in zip(th,labels):t.string=l

# Translate role labels in the model audit table, without touching exact model identifiers.
role_map={
"main comparator":"主要对照",
"main low-complexity RL baseline":"主要低复杂度强化学习基线",
"mechanistic ablation/component":"机制消融/组成模型",
"primary model":"主要模型",
"Extended Data strong alternative; mechanistic adjudication":"扩展数据强对照；机制判别",
"optional behavioral head; SLM latent branch remains mechanistic authority":"可选行为读出；SLM 潜在状态分支仍作为机制依据",
"flexible capacity ceiling":"灵活容量上限",
"secondary biologically motivated comparator":"次级生物学启发对照",
}
for txt in soup.find_all(string=True):
    if txt.parent and txt.parent.name=="td" and str(txt) in role_map:
        txt.replace_with(role_map[str(txt)])

# Safe, text-node-only cleanup. Never touches classes, hrefs, filenames or CSS.
phrase_map={
"生成充分性 / AI":"生成充分性 / 人工智能",
"Authority 与源数据":"权威版本与源数据",
"content-to-action conversion":"社会内容到自身行动的转化",
"outcome-dependent teaching":"结果依赖的教学",
"social state":"社会状态",
"adaptive Observe sampling":"主动选择观察",
"sampled content":"采到的社会内容",
"native Feed conversion":"自身进食",
"feedback：social outcome":"反馈：社会结果",
"post-outcome source-specific credit / value update":"结果后的来源特异归因与价值更新",
"future Observe policy":"未来观察策略",
"default SLM":"默认 SLM",
"data-driven SWM":"数据驱动 SWM",
"SLM+当前线索":"SLM 加当前线索",
}
for txt in list(soup.find_all(string=True)):
    if not isinstance(txt,NavigableString):continue
    if txt.parent and txt.parent.name in {"style","script"}:continue
    st=str(txt)
    ns=st
    for a,b in phrase_map.items():ns=ns.replace(a,b)
    ns=ns.replace("而不是","，重点在于").replace("不只是","还包括")
    if ns!=st:txt.replace_with(ns)

# Ensure no forbidden contrast construction remains in reader-facing Chinese.
for txt in list(soup.find_all(string=True)):
    if txt.parent and txt.parent.name in {"style","script"}:continue
    st=str(txt)
    ns=st.replace("并不是","并非").replace("不是","并非")
    if ns!=st:txt.replace_with(ns)

out=str(soup)
new_links=set(re.findall(r'(?:href|src|srcset)="([^"]+)"',out))
if orig_links!=new_links:
    missing=sorted(orig_links-new_links)[:20]
    added=sorted(new_links-orig_links)[:20]
    raise RuntimeError(f"link set changed; missing={missing}, added={added}")

HTML.write_text(out,encoding="utf-8")
print("clean Chinese reader layer written; links preserved",len(orig_links))
