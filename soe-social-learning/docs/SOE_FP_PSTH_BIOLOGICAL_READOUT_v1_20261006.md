# SOE fiber photometry：两种多巴胺时间读法与跨事件状态

日期：2026-10-06

## 1. 两种 FP→DA 读法看到的是同一底层过程

固定结果后 0–6 秒和真实行为时长归一化在同一批 1,371 个事件、9 只动物中高度相关。逐动物相关范围为 ρ=.520–.944，中位数 .785。

固定窗口更强调结果出现后的持续评估和更新；真实行为时长强调行为执行期间的多巴胺。两种表示一起看，比单独挑一个窗口更容易解释时间结构。

## 2. 结果事件的 PSTH

固定 0–6 秒：
- Active success 在结果附近出现较快的正向峰值。
- Passive outcome 在稍晚时段出现更持续的正向信号。
- Unrewarded 在结果后转为持续负向。

真实 bout 时长归一化：
- Passive 在真实行为期间保持较高的多巴胺。
- Active 更偏向行为早期。
- Unrewarded 在大部分行为阶段保持较低，接近 bout 结束时回升。

这些结果说明两种 readout 的差异主要来自时间权重，而没有改变 Active / Passive / Unrewarded 的总体排序结构。

## 2A. PSTH 事件数量

结果事件的权威身份来自 RL event table，用它去除 legacy passive row 中重复出现的 33 个 Active anchors：

- 全部结果事件：Active 442、Passive 420、Unrewarded 861，共 1,723 个。
- 两种 FP→DA 方法都有效的共同结果事件：Active 259、Passive 257、Unrewarded 855，共 1,371 个。
- 观察事件：Inside 541、Outside 2,183、All-observation 2,724。
- 从一个结果到下一次重新观察且发生在下一结果之前：Active 后 327、Passive 后 298、Unrewarded 后 665，共 1,290 个；最长间隔 54.4 s。

## 2B. 哪些结果成分真正受时间读法影响

逐动物比较固定结果后 0–6 秒和真实行为时长：

- **主动成功 − 未奖赏**：固定窗口 8/9 为正，P=.0117；真实行为片段 8/9 为正，P=.0547。固定窗口的对比更大，直接配对 P=.0273。主动成功后的 VTA 区分因此有一部分延续到行为结束以后。
- **被动结果 − 未奖赏**：固定窗口 9/9 为正，P=.00391；真实行为片段 8/9 为正，P=.0195。两种读法都保留这一结果，直接差异 P=.0547。
- **被动结果 − 主动成功**：固定窗口 P=.203；真实行为片段 8/9 为正，P=.0391。读法间直接差异 P=.570，因此它提示被动结果在行为执行期更持续，但当前数据不支持显著的读法交互。

这组结果把“窗口选择”转化为时间结构问题：主动成功相对未奖赏的区分明确从行为执行期延续到结果后；被动结果相对未奖赏则跨两个时间范围都很稳定。

## 3. 上一次结果会延续到下一次观察

只看结果后 60 秒内第一次重新观察的事件：

观察开始前 −1–0 秒：
- Active vs Unrewarded：n=9，8/9 同方向，P=.0273。
- Passive vs Unrewarded：n=9，8/9 同方向，P=0.0195。
- Active vs Passive：P=0.0273；方向为 Passive 高于 Active。

观察开始后 0–2 秒：
- Active vs Unrewarded：8/9，P=.00781。
- Passive vs Unrewarded：8/9，P=0.00781。
- Active vs Passive：P=0.4961。

因此，上一次社会结果留下的 VTA 状态在下一次观察真正开始之前已经可以看到，并在新观察开始后进一步拉开。

## 4. 真实观察 bout 内仍保留上一次结果

把每次观察按真实持续时间归一化：

前 25%：
- Active vs Unrewarded：9/9，P=.00391。
- Passive vs Unrewarded：9/9，P=.00391。

中间 25–75%：
- Active vs Unrewarded：P=.0195。
- Passive vs Unrewarded：P=.0391。

整段观察：
- Active vs Unrewarded：P=.0195。
- Passive vs Unrewarded：P=.0391。

这说明跨事件状态并未在观察开始瞬间消失，而是延续到新的社会采样过程。

## 5. 与行为“快速记忆”的关系

行为上，Active / Passive 结果之后下一次重新观察概率下降；Unrewarded 保留更强的继续采样倾向。

神经上，在那些确实再次观察的事件里，Unrewarded 后的下一次观察处于更低的 VTA 状态，而 Active / Passive 后的下一次观察更高。这个结果适合解释为前一结果建立了一个跨事件状态，并在新的社会采样开始前持续存在。

这项分析条件化在“已经发生重新观察”，所以它用于证明神经状态的跨事件延续；重新观察概率本身仍由独立行为分析给出。

## 6. Source data

- data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv
- data/SOE_FP_NEXT_OBSERVE_POST02_PER_ANIMAL_v82.csv
- data/SOE_FP_NEXT_OBSERVE_POST02_STATS_v82.csv
- data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv
- data/fp_da_common_event_v1/method_difference_events.csv.gz

## 7. Figures

- assets/SOE_FP_PSTH_biological_story_v82.*
- assets/SOE_FP_PSTH_observation_context_v82.*
- assets/SOE_FP_PSTH_trial_heatmaps_v82.*
- assets/SOE_FP_next_observe_memory_v83.*
