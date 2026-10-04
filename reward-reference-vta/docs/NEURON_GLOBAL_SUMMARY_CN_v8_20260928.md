# Reward-reference：Neuron 全局总结 v8 — 2026-09-28


这篇文章现在真正要回答的，已经不是“dopamine 会不会影响吃东西”。这一点在之前的 Science 工作里已经有完整的 circuit 和因果结果。现在的问题更靠前：动物为什么会把同一个 reward 看成不同的 value？过去吃过什么，怎样改变了此刻 reward 在 VTA dopamine 中的表示？

最直接的数据其实不需要模型。同样的 20E 或 100E reward，只因为之前经历过的 reward 不同，行为和 2–5 s sustained dopamine 都跟着变，而且 matched-history effect 在 9/9 animals 中方向一致。当前 reward 的物理大小不能单独决定它的 neural value。神经系统显然还在拿它和 recent history 中形成的某种 reference 比较。

后面的模型分析都应该围绕这个 reference 到底是什么来组织，而不是围绕“哪个算法分数最高”来组织。

一个自然解释是时间适应：reward switch 发生以后，reference 随时间自己漂移。但在动物第一次真正采样新 reward 之前，把 elapsed time 从 5 s 扫到 640 s，对 sustained dopamine 增加的解释量几乎为零。反过来，一旦动物开始吃，实际 consumption dose 在相同 bout stage 下仍然有额外信息。lick count 和 feeding duration 太相关，目前还不能说哪一个才是生物学上的基本 update unit；不过 reference 的更新显然更接近实际获得的 reward evidence，而不是单纯由时间或 bout number 推进。

H/L/N/S 这样的实验条件也不够。把 animal、current reward 和 categorical context 固定以后，continuous history state 仍然解释 sustained dopamine。更直观地说，在同一个 animal、同一种 reward、同一个 nominal context 内，把 history state 从低到高分成四档，dopamine residual 还是从负值一路升到正值；7/7 animals 的 within-context slope 都是正的。context 只是粗粒度标签，同一个 block 里面的 value 仍然会随着动物真实经历过的 reward 连续移动。

再往前一步，把更近的 history 尽量拿干净：当前 reward、第几个 bout、block 内时间、session progression、上一 block 吃了多少、当前 block 已经吃了多少，都进入 nuisance model。剩下的 cumulative-history component 仍然解释 sustained dopamine，delta R2=0.02686，conditional P=0.00670。FullHistory 多出来的信息不是“更准确地知道 switch 后已经吃了几次”，而是保留了一段更长 reward trajectory 的痕迹。

这也是现在 model comparison 真正有意义的地方。ReferenceRW、BeliefState、BlockSampling、TwoStage 都不是弱 baseline，它们和 FullHistory 的 state correlation 大约都在 0.90 左右，大家都知道发生过 switch，也都知道 local exposure。严格的双向 horse-race 中，FullHistory 放在这些模型和 raw-history controls 后仍保留约 0.025 的 unique sustained-DA R2，P 大约 0.010–0.012；反过来，competitor 放在 FullHistory 后面基本没有剩余信息，P 大约 0.80–0.97。真正的区别是 cumulative reward trajectory 和 local switch-centered adaptation，而不是 adaptive model 和 non-adaptive model 谁更复杂。

这并不等于大脑实现了某一个 RW equation。held-out animal prediction 没有稳定选出 universal winner；alpha 更像 history 的有效 recency scale，而不是可以直接对应某种 synaptic learning rate 的常数。high-to-low 和 low-to-high 拆成两个 alpha 也没有可靠改善 held-out prediction。模型在这里的作用，是约束 biological computation 必须具备哪些性质，而不是宣布大脑使用某一行公式。

memory depth 的结果也符合这个理解。把 prev1、prev2、prev3、prev4 block 的 consumption 拆开，没有哪一个 lag 给出清晰、独立的 cutoff；最好的 conditional P 仍约 0.16。可是把这些 lag、total prior consumption、global history 等一大套 multiblock summaries 全部放进 baseline 后，continuous recency-weighted state 仍然显著，P=0.00620。现有数据更像一个平滑压缩过去经历的 memory trace，而不是“大脑固定记住前两个或三个 block”。

目前文章最强的新机制结果来自 Fig.5。分析限制在完全相同的 192 个、持续至少 5 s 的 bouts，11 animals 都同时贡献 pre-bout、0–2 s 和 2–5 s，因此三个 epoch 不是由不同 bouts 组成。U-R contrast 在 bout 前是负的，beta=-0.485；刚开始吃的 0–2 s 基本没有，beta=+0.294；到 2–5 s 才变成明显的正向 relative-value code，beta=+1.752。0–2 到 2–5 s 的 interaction 是 +1.458，P=9.02e-08。11/11 animals 自己的 sustained slope 都比 early slope 大，exact P=0.000977。

这个变化也不是因为后半段 photometry 信号整体更“好看”。正交的 U+R component 在 0–2 到 2–5 s 没有相同增强，interaction P=0.511；pre 到 2–5 s 的 U+R change 也不显著。current reward U 和 learned reference R 只有到了 sustained window 才真正分开：U 变成正系数，R 变成负系数。

另一个重要 control 是原来的 0–2 和 2–5 指标都减了 pre-bout mean，因此必须排除“负 pre signal 被减掉后人为制造正 contrast”。直接分析未经 pre subtraction 的 raw z-signal，0–2 s 的 U-R 仍不显著，beta=-0.191，P=0.718；2–5 s 的 raw signal 自己已经出现正向 contrast，beta=+1.267，P=0.0399。这个结果支持真正的 temporal emergence，而不是 baseline-subtraction artifact。

现在更合理的 biological picture 不是“reference 一直存在于 dopamine baseline 里，吃东西以后只是把它读出来”。更像是 recent reward history 被保存在 VTA dopamine 之外——可能是 upstream input，也可能是 distributed network state——真正开始 consumption 后，current reward 和 history-dependent reference 在几秒内被组合，随后形成 sustained VTA dopamine 中的 relative-value representation。

这个 representation 接近一个 U-R axis。标准化以后，current reward 对 sustained dopamine 是正的，learned reference 是负的，大小也接近；额外的 U+R information 很弱。但这还不足以说神经元在字面上做 subtraction。divisive-normalization family 做了 nested held-out test，11/11 folds 都把 normalization strength 推到最弱的一端，prediction 也没有优于简单 U-R；再加 reference-dependent nonlinear gain terms，同样没有显著增益。最稳妥的结论是 comparison-dominated code；目前没有证据要求一个更强的 divisive normalization，但 subtraction 和 near-linear normalization 仍不能被完全区分。

行为在这个故事里应该放在最后，而不是拿来选模型。history scale 先从 dopamine 中确定并 freeze，再看 behavior。这个 frozen state 预测 bout duration 和 termination，因此提供的是 biological consequence：这个 neural reference state 和动物继续吃还是停下来有关。与此同时，behavior 还保留明显的 U+R information，因此也不是简单把 dopamine 的 U-R signal 原封不动复制过去。

cohort robustness 也要克制。leave-one-cohort-out 时 FullHistory unique effect size 始终为正，但 reduced subsets 的显著性随样本量变化；animal-level exact cohort-label permutation P=0.474。现在既不能说完全 cohort invariant，也没有依据把 VGLUT2 定义成另一套 biological mechanism。

这和 Science 的关系已经比较清楚。Science 解决的是 consumption-period VTA dopamine 属于 hedonic feeding circuit，而且干预它会改变摄食。这里问的是这个 dopamine signal 在自然情况下为什么会有当前这个值。以前的 causality 是 downstream functional context，不应该再做这篇文章的 climax。新文章真正的新东西是 value construction。

目前最稳的中心表述是：

**Recent consumption history builds a continuously updated reward reference, and the current reward becomes relative to that reference over the first seconds of consumption, producing a sustained VTA dopamine value signal that predicts feeding persistence.**

time-resolved trajectory 现在也已经跑通，而且 raw reconstruction 与 strict authority 达到 10^-15 量级的机器精度。用 0.5 s bins 看同一批 192 bouts，U-R 在 bout 前明显为负，0–2 s 逐渐接近零，大约在 1.5–2 s 后跨过零，3–5 s 的 pointwise 95% CI 连续位于零以上；U+R 没有对应的时间演化。这里的“约 3 s”只应当作为描述性的时间尺度，正式统计仍以预先定义的 0–2 versus 2–5 s interaction 和 11/11 animal pairing 为主。这样 Fig.5 已经不依赖人为选出的固定窗口，而是能直接看到 relative-value code 在 consumption 中逐渐形成。

接下来不需要再扩大 model zoo。更值得做的是把当前六张主图和正文按这条逻辑收紧，检查 time-resolved dynamics 的 animal/cohort visualization 是否需要放 Extended Data；真正还留给未来实验的问题是 reference storage site、实际 update variable，以及执行 comparison 的 circuit。


## 2026-09-27 新增：多情景 value-context 扩展（新增验证层，不替代上面的模型主线）

这一轮新数据的作用不是重新定义文章，也不是把 reward-contrast 模型主线改成“很多 manipulation 的集合”。原来的核心仍然是：recent consumption history 如何形成 continuous reward reference、为什么 FullHistory 比 local switch-centered adaptive states 保留更多 cumulative trajectory 信息、以及 U-R comparison 如何在 consumption 的数秒内形成。新数据只解决一个更高层的 generalization 问题：这个 internally constructed value coordinate 是否只存在于 100E/20E reward-contrast task，还是能和其他独立的 value manipulations 对齐。

### 1. Quinine：固定 100E concentration，只改变 reward quality

已经锁定真正的 quinine authority，而不是依赖误导性的旧文件名。数据来自 FE_VTADA/RecordingTestQE/group_analysis，7只动物 001/002/003/006/007/018/019。旧 Beh_100E_20E_Fig1E-G.mat 文件名虽然写着 100E/20E，但 checksum 和逐动物复现确认它实际上是 100E versus 100E + 3 mM quinine。

重新从逐动物 bout-level Feeding_OFF_signals_EE/QE 文件构建后，共 172 bouts。纯 100E 到 100E+quinine 时，平均 bout duration 从 41.0 s 降到 5.08 s，7/7 animals 同方向，exact paired P=0.015625；total DA AUC 从 79.0 降到 3.06，7/7 同方向，P=0.015625；sustained AUC_S 从 1.68 降到 0.878，7/7 同方向，P=0.015625。bout-level fixed-animal、animal-clustered 分析分别给出 duration P=1.15e-19、AUC P=1.79e-4、AUC_S P=1.43e-6。

quinine temporal trace 已用原 MAT 的 basal_time、odor_time 和 FP sampling interval 重新校准。正确结果是 pre-bout 差异不显著（P=0.219），0-2 s 开始出现 reward-quality separation（7/7，P=0.0156），2-5 s 更强（7/7，P=0.0156）。因此 quinine 更像 consumption-onset 后较快形成的 reward-quality valuation，而不是一个已经存在的 pre-bout offset。

### 2. 20E stimulation：固定 reward，因果地向高-value 方向移动

现在确认有两套彼此独立的 stimulation dataset，不能混成一套。

第一套是 Science Chrimson contingent cohort：13 animals，1 mW / 25 ms，固定 20E，共 1,833 bouts。stimulation 将平均 bout duration 从 6.61 s 提高到 9.36 s，12/13 animals 同方向，paired P=0.00806；total DA AUC 从 -1.51 提高到 19.40，13/13 animals，exact P=0.000244；AUC_S 从 -0.361 提高到 1.926，13/13 animals，P=0.000244。bout-level clustered P 分别为 duration 1.74e-6、AUC 8.10e-9、AUC_S 3.45e-13。

第二套是独立 10 mW GRAB matched cohort：5 animals / 774 bouts。5/5 animals 在 duration、AUC、AUC_S、PeakF 上全部同方向增加；bout-level clustered P 分别约 5.30e-12、1.36e-9、3.83e-9、5.91e-9。两套 stimulation 数据因此构成 replication，而不是一套数据的不同画法。

### 3. Hunger：固定 20E，只改变 motivational state

FE_VTADA/20E_Hunger 中同样7只动物具有逐 bout photometry authority，共851 bouts。food restriction 将 20E bout duration 从 7.22 s 提高到 17.84 s，6/7 animals 同方向，paired P=0.03125；total AUC 在 6/7 animals 中上升，paired P=0.046875。AUC_S 没有形成和 quinine/stimulation 一样整齐的统一 shift，因此主文中只使用明确的 positive readouts，不用它来定义 sustained-DA mechanism。

### 4. LiCl 与 semaglutide：作为额外 state axes，而不是抢主线

LiCl 数据提供 fixed-100E 的 sickness/devaluation axis：pre-LiCl 相比 post-LiCl，7/7 animals bout duration 更长，mean paired difference 7.68 s，P=0.015625；AUC 6/7 更高，mean difference 12.54，P=0.03125。Semaglutide 则是 slow pharmacological-state extension，仍然保留为 Extended Data / bridge to prior Science，而不是当前 reward-reference paper 的 climax。

### 5. 新数据如何进入文章

最重要的逻辑不是“我们有很多条件都显著”，而是把不同 manipulation 分层：current reward magnitude；self-generated history/reference；reward quality；motivational state；sickness/devaluation state；causal circuit state；slow pharmacological state。

其中只有 reward-history 模型回答“reference 是什么、保留多深 history、何时变成 U-R comparison”这个核心计算问题。其他 context 的作用，是证明这个计算处在一个更一般的 ongoing-value space 里，而不是 100E/20E 特定任务的统计产物。

因此主图编号不应因为新增 context 被整体改写。原 Fig1-6 reward-reference 架构继续作为 authority；新增 multicontext panel 暂定为 Fig4X / cross-context validation，插在 cumulative-history 与 temporal-comparison 之间，等最后投稿架构再决定是否并入主图或 Extended Data。


### 6. Frozen natural-reward neural axis：新 context 真正投影回原 value geometry

为了避免“很多条件都显著”这种弱叙事，进一步用自然 100E versus 20E 的 neural difference 定义一个完全冻结的二维 value axis，只使用 total AUC 与 AUC/s。两个维度在轴中的权重几乎相等（约 0.710 与 0.704）。然后不重新拟合地投影其他 context。

quinine 在 leave-one-animal-out 条件下仍然 7/7 animals 沿该轴向低-value 方向移动，exact P=0.015625，平均 cosine≈0.894。独立的 13-animal 1-mW stimulation cohort 则 13/13 沿同一轴向高-value 方向移动，exact P=0.000244，平均 cosine≈0.881；另一套 5-animal 10-mW cohort 也是 5/5 同方向，平均 cosine≈0.928。

这条结果的重要性在于：natural reward magnitude 先定义 neural value direction，而 quinine 和 stimulation 都没有参与定义这个方向，却分别向下和向上移动。它把新增 context 从“额外实验条件”升级成了对原 reward-value geometry 的 zero-shot generalization / causal validation。

### 7. 外部 manipulation 映射到 FullHistory 的 behavioral-state 尺度

为了进一步把新增数据接回原模型，把 FullHistory 对 log bout duration 的 beta=+0.502 和对 termination hazard 的 beta=-0.830 当成自然 state 的行为单位。quinine 的 effect 相当于大约 -3.14 个 duration-state units、-2.67 个 hazard-state units；13-animal stimulation 相当于 +0.49 / +0.42；独立 5-animal stimulation 相当于 +0.81 / +0.63。两个行为 readout 对每个 manipulation 给出的等价位移方向和量级都很一致。

这个换算是 descriptive calibration，不表示 quinine 或 stimulation 真的在直接修改 FullHistory latent variable。它的价值是说明：新增的 sensory/circuit manipulations 不仅沿 frozen neural value axis 移动，在 feeding persistence 的自然 state 坐标上也可以得到一致的正负位移。

### 6. 当前升级后的中心表述

Recent consumption history builds a continuous, recency-weighted reward reference that preserves cumulative trajectory beyond local adaptation. During consumption, current reward is transformed relative to that reference over seconds to generate sustained VTA dopamine value. Independent manipulations of reward quality, motivational state, sickness state, and causal dopamine drive move ongoing neural value and persistence along the same broader value space, showing that the history-defined reference is one computational component of a general value-construction architecture.


## 2026-09-27 深入：FullHistory computation 在独立 quinine task 内部重新出现

这一结果比“quinine 也改变 DA/behavior”更重要，因为它直接测试原 reward-reference computation 是否跨 task 泛化。

首先做了严格 provenance audit。EE 和 QE 两类 condition-specific lick streams 在每只动物中都 0 overlap，但两者 union 恰好 100% 覆盖 global lick stream；因此 quality label 不是重复标记。所有 172 个 selected bouts 都能唯一并按时间顺序映射回 Feed_info 的 absolute bout start。FullHistory state 只使用 current bout 开始之前的 licks 构建，当前 bout 不进入 reference。

随后把自然 100E/20E 数据中确定的 alpha=0.20 完全冻结，不在 QE 数据里重新调参。只保留 pure100E bouts，使 current reward 完全固定。66 个 pure100E bouts / 7 animals 中，FullHistory state 对 whole-bout DA AUC 的新增解释量为 delta R2=0.0254，animal-clustered P=0.00141；6/7 animals 的 slope 为正，exact Wilcoxon P=0.03125；within-animal circular-shift null P=0.00205。

这个 effect 具有明确的时间方向性。past-history state 单独显著；time-reversed future control 不显著（P=0.356）。past 与 future 同时进入模型时，past 仍显著（P=0.000325），future 不显著（P=0.216）。因此这不是单纯的 session drift。

FullHistory 也保留了超出 local-history summaries 的信息。控制 last20、last40、last80 或 cumulative-history summary 后，FullHistory 仍有显著 unique delta R2；反过来 local competitor 加在 FullHistory 后大多没有独立贡献。last5/last10 和 FullHistory 高度共线，因此这两个窗口不能用于强区分，但更深的 local-history controls 可以。

recency profile 也支持 transfer 而不是重新拟合。自然 reward-contrast 的 profile 最优约 alpha=0.15-0.20；QE pure100 profile 更宽、最高点约 0.30，但 frozen alpha=0.20 已经显著，而且 .15-.40 都位于高性能平台。正确表述是两个 task 的 recency range 有实质重叠，而不是声称精确共享一个学习率。

QE task 的 neural expression 时标与原 task 不同。固定时间窗显示前 0-5 s 较弱，而 10-20 s 的 state association 更一致。只看同一批 duration>=20 s 的 40 个 pure100 bouts，10-15 s clustered P=0.042，15-20 s 时 7/7 animal slopes positive（exact P=0.0156）。不过 late-versus-early interaction 本身尚未形成显著差异，因此目前最稳妥的表述是：同一个 history rule 跨 task 泛化，但其 DA readout 的表达时标随 value context 改变。

### 新的最高层意义

这一步把文章从“同一 reward-contrast task 内找到一个漂亮模型”推进为：**一个从 natural reward history 发现并冻结的 reference rule，可以 zero-shot 跨到独立的 reward-quality task，在固定 current reward 的情况下重新预测 VTA dopamine。** 这比单纯加入 quinine/stimulation 条件更直接地支持 reward-reference computation 的一般性。


## 2026-09-28 新增：alpha=0.20 的跨任务泛化不是事后挑选
QE 数据现在又增加了一层真正的 held-out 验证。逐动物 leave-one-animal-out prediction 中，alpha=0.20 的平均 normalized MAE=0.5453，是所有测试 alpha 中最低；nested LOAO 的 modal alpha 也为 0.20。更重要的是，把 natural task 和 QE task 放到同一个公平尺度上，alpha=0.20 是 maximin shared scale：它保留 natural task 自身峰值的 91.1% 和 QE 峰值的 97.9%。因此目前最强的说法已经不只是“两个 task 的 recency range 有重叠”，而是：一个接近 0.20 的有效 recency rule 可以在两个独立 task 间同时保持接近最优，并且在 QE held-out animals 中独立被选中。natural 的最佳点仍约 0.15、QE 的 in-sample 峰值约 0.3，所以不能把它包装成完全相同的 biological learning rate。


## 2026-09-28 新增：跨情景共同 value direction 很稳，但不能把所有 temporal dynamics 都解释成同一个 U-R mechanism

进一步把行为和 VTA dopamine 放到同一个二维 value space 后，natural 100E-versus-20E 定义的高-value 方向对 axis 构造方式并不敏感。用 SD 或 MAD 做尺度标准化、用 mean 或 median 定义 natural axis，一共四种定义下，quinine、hunger、LiCl、13-animal stimulation 和 5-animal stimulation 的平均 cosine 全部保持正值。quinine 的范围为 0.961-0.975，stim13 为 0.833-0.882，stim5 为 0.952-0.988；hunger 和 LiCl 也保持正方向，但对 robust scaling 更敏感。这个结果使“broader ongoing-value space”不再依赖某一种任意 normalization。

但是 temporal geometry 的结果必须分层解释。对 quinine 和 13-animal stimulation，observed trajectory 都明显更接近 history-derived U-R than orthogonal U+R（quinine paired P=0.03125；stim13 P=0.00024414）。然而 U-R 并没有优于 generic linear ramp / onset step；quinine 对 linear ramp 的差异 P=0.57812，stim13 的 U-R 甚至比 generic ramp/step 更差。正确结论因此是：external manipulations 支持 shared value direction 和 comparison-like organization，但不能单独证明它们复制了 reward-history task 中那个特异的 temporal U-R construction。

这个边界反而让主线更清楚：**跨情景 generality 属于 value geometry；真正的 temporal computation 仍由 matched-history experiment 中同一批 bouts 的 U-R emergence 来识别。** 这两层证据互相补强，而不是互相替代。


## 2026-09-28 新增：QE whole-bout AUC 不是靠“只在长 bout 中 state effect 特别强”才能成立

pure100 的核心 replication 本来已经用 flexible log-duration spline 控制了 bout length。现在又进一步允许 FullHistory state 本身和 log(duration) 发生 interaction。AUC 上，interaction 的 clustered P=0.382，没有证据支持 state effect 随 bout length 系统性增强；与此同时，在 mean duration 处的 centered FullHistory 主效应仍为正（beta=65.91，clustered P=0.0114）。因此这可以作为一个很直接的 reviewer control：whole-bout AUC replication 并不依赖于“只有长 bout 才有 history effect”这种解释。它不用于证明 temporal readout 与 duration 无关，只用于排除一个最直接的 duration-dependent alternative。


## 2026-09-28：从“模型排行榜”改成“科学理论判别”

当前最重要的变化不是又多了几个模型，而是已经可以回答“这个 latent reference 到底是什么、又不是什么”。

**1. Hidden-state / belief 解释了一部分局部 adaptation，但解释不掉 cumulative path。**  
Babayan/Uchida/Gershman 风格的 Bayesian belief-state 在 held-out animal 中是可信的竞争模型：平均 relative MAE=0.971，11只动物中9只优于 current-reward baseline，但 animal-level exact P=0.240。真正有判别力的是双向 unique-information test：FullHistory 在 belief 之外仍有 ΔR²=0.02541，permutation P=0.0124；belief 在 FullHistory 之外只剩 ΔR²=0.000465，P=0.726。因此不能把 history effect 简单解释成“动物猜自己目前在哪一个 block”；cumulative reward trajectory 还保留额外的 dopamine-relevant 信息。

**2. Niv average reward-rate 也不是核心 reference。**  
reward-rate state 的 held-out mean relative MAE=0.938，9/11 animals 优于 baseline，但 P=0.240。FullHistory | reward-rate 仍为 ΔR²=0.02565，P=0.0122；反向 reward-rate | FullHistory 只有 ΔR²=0.000432，P=0.722。说明当前 reference 不是简单 tonic average reward。

**3. Adaptive gain / uncertainty 不能解释掉 signed history value。**  
Tobler-style variance-normalized adaptive gain 之外，scalar history TD/RW 仍保留 ΔR²=0.01563，P=0.0494；反方向只有 ΔR²=0.000467，P=0.687。Fiorillo/Gershman-style belief entropy 和 posterior variance 在 FullHistory+belief value 之后分别只增加 ΔR²=0.00192（P=0.476）和 0.00271（P=0.404）。

**4. Sustained 2–5 s 信号更像 signed value/RPE，而不是 unsigned salience。**  
0–2 s 时 signed 与 unsigned 尚未明显分开；2–5 s 时 signed beyond unsigned 为 ΔR²=0.01867，P=0.0328，而 unsigned beyond signed 为 ΔR²=0.00320，P=0.375。这和 U−R 在约3 s以后形成稳定正向编码的时间进程吻合。

**5. Distributional RL 在 bulk population 层面不需要额外 spread 维度。**  
5-expectile distributional history 的 mean 与 FullHistory 极其接近（r=0.993）；distributional spread 在 FullHistory+distributional mean 之后只增加 ΔR²=0.000012，P=0.941。这不能否定单细胞 dopamine 的 distributional coding，只说明当前 fiber-photometry sustained signal 主要需要 history-dependent central reference。

**6. 更广泛 model zoo 的意义是画边界，不是选“冠军”。**  
Pearce-Hall adaptive learning rate、Kalman filter、asymmetric learning、multi-timescale history analogue 等没有在 held-out animals 中稳定显著击败 scalar cumulative-history family。Masset 2025 的原模型关注 future discount timescales；当前任务没有独立 future-delay manipulation，因此这里只能测试过去 reward integration 的 task-adapted multi-timescale analogue，不能声称直接实现并否定 Masset 模型。

**7. Value-RNN 已完成：learned latent state 没有吃掉 cumulative history。**  
Titan 上三层分析都已完成：第一层是 reward-only / reward+elapsed-time × hidden size 2/5/10/20/50/100 × 3 seeds；第二层固定 H=50、每种输入跑 12 seeds，作为更接近 Hennig 官方默认 capacity/多模型设置的 confirmatory test；第三层专门固定 H=2 再跑 12 seeds，用来检验 full-grid 里唯一的低容量 nominal exception。第一版 aggregator 曾错误地在 RNN-only held-out prediction 前先与 FullHistory 表取交集，导致少数动物出现假性外推；这个 bug 已在 corrected evaluator 中修正，以下只使用 corrected results。

H=50 / 12-seed ensemble 本身没有稳定改善 held-out-animal dopamine prediction：reward-only mean relative MAE≈1.011（8/11 数值更好，exact P≈0.465），reward+time≈1.013（8/11，P≈0.413）。但 cross-fitted RNN state 确实学到一部分 history-like structure；它与 FullHistory 相关约 r=0.367。真正有判别力的是双向 unique-information test：FullHistory 在 H=50 RNN 之外仍保留 ΔR²≈0.02685（reward-only P≈0.0128；reward+time P≈0.0078），而 RNN 在 FullHistory 之外只剩约 4–5×10^-5 R²，P≈0.86。H=5–100 都是同一方向。

full-grid 中唯一 nominal exception 是 reward-only H=2：三-seed ensemble 中 RNN|FullHistory 有 ΔR²≈0.0153、nominal P≈0.0226。但这个现象没有通过两个更严格的确认。首先，对 12 个 recurrent configurations 做同步 10,000-permutation max-stat correction 后，family-wise P≈0.0646，observed ΔR²≈0.01529 低于 family-wise 95% max-null threshold≈0.01659。其次，专门的 H=2 / 12-seed confirmation 中，RNN beyond FullHistory 不再显著：reward-only ΔR²≈0.00443、P≈0.186，reward+time ΔR²≈0.00038、P≈0.686；反过来 FullHistory beyond H=2 RNN 仍显著（reward-only ΔR²≈0.03124、P≈0.0018；reward+time ΔR²≈0.02473、P≈0.0120）。同时 H=2 RNN state 的 97.5–98% 已能由现有 task/history variables 解释。因此 H=2 只保留为 Extended Data sensitivity，不升级为新的 latent dimension。

实现审计也完成：custom RNN 与 Hennig 官方代码在 GRU→value head、TD target r(t+1)+γV(t+1)、γ=0.93、Adam lr=0.003、150 epochs 及默认 PyTorch initialization path 上一致。区别在于我们的输入是 irregular lick-event sequence，因此应该写成 Hennig-aligned architecture on task-adapted event history，而不是声称完全复制论文的 temporal discretization。

**8. QE 的跨任务结论需要写成“shared computation, different temporal expression”。**  
在固定 40 个 pure-100E、duration≥20 s bouts / 7 animals 的 continuous analysis 中，frozen history state 在 bout 前 -2.0 到 -0.5 s 已有 positive cluster（P≈0.0089）；bout onset 后约 0–8 s 没有稳定 positive cluster；8–12 s 再出现 cluster（P≈0.0020），13–20 s 更强（P≈0.00020）。null 是在 animal 内 circular-shift frozen state，并整条时间轴共享 shift，因此保留 temporal covariance。跨 task 真正复现的是 history-reference computation，而不是固定 latency 或固定 waveform。

**9. reference 与行为形成更完整的方向性闭环，但不要写成完整 mediation。**  
history contrast 强烈预测 bout duration（β≈+0.698，P≈3.9×10^-15）和 termination hazard（β≈−1.229，P≈1.5×10^-14）。用 dopamine 本身选择的 alpha=0.20 state 去预测行为仍成立：duration β≈+0.476，P≈0.0057；termination β≈−0.780，OR≈0.459，P≈1.8×10^-4。因果操作方向一致：dopamine activation 降低 termination hazard（OR≈0.690，P≈3.3×10^-10），contingent Jaws inhibition 提高 hazard（OR≈1.34，P≈0.0289），noncontingent inhibition 较弱且未达传统显著（P≈0.098）。最合适的表述是：**history builds the reference → reference shapes sustained dopamine value → dopamine contributes to persistence**；因为 reference 本身并未在每个链接被独立操纵，所以不称为完整 causal mediation。

**当前 model room 可以封口。**  
在当前任务能够独立识别、且真正与 dopamine/reference 问题有关的模型 family 已经测试完或有 family-level analogue。Stauffer marginal utility、Masset future-discount timescale、feature-specific RPE 等需要当前设计没有的独立 reward-level/delay/feature manipulation，因此明确列为 task boundary，而不是制造假的 negative result。后续只有出现新的生物学问题或新的实验 manipulation 时，才继续增加模型。  
