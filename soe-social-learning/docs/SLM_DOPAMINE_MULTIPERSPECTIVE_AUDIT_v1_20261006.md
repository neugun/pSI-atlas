# SLM 多角度机制支持与多巴胺计算审计 v1

日期：2026-10-06

## 1. 秒级结果：从“停止观察”改写为“社会信息需求被立即重设”

旧页面把秒级效应写成“主动成功或被动结果之后更容易停止观察”，生物学含义太弱。更合适的解释是：**一次结果会立刻改变下一步是否还需要继续从同伴那里获取信息。**

当前 authority：
- Active vs Unrewarded，No-observe→Observe：−9.0 个百分点。
- Passive vs Unrewarded，No-observe→Observe：−8.3 个百分点。
- Active vs Unrewarded，Observe→No-observe：+10.0 个百分点。
- Passive vs Unrewarded，Observe→No-observe：+12.9 个百分点。
- 学习者中 Active 驱动的快速切换从 D1–4 的 +4.3 个百分点增强到 D10–14 的 +10.8 个百分点，P=.041。

因此最重要的结论是：未奖赏保留继续寻找社会信息的需求；得到 Active 或 Passive 结果后，动物暂时降低再次采样。这个局部规则还会随训练增强。

来源：`SOE_memory_multiscale_support_v2.csv`；`SOE_RL_Results_and_Figure_Legends_v3_20260921`。

## 2. 行为层面的 RPE/APE 双通路

UCL/Greenstreet-style transplant 分开建模：
- RPE：结果相对价值预期的误差。
- APE：动作相对动作概率的误差。
- Dual：两条更新同时进入行为。

整只动物留出：
- RPE-only：Brier=.227295。
- APE-only：Brier=.191108。
- RPE+APE：Brier=.189423。
- APE 在 27/27 动物优于 RPE，mean Brier gain=.03381，P=1.49×10⁻⁸。
- Dual 在 24/27 动物进一步优于 APE-only，额外 gain=.00193，P=4.92×10⁻⁷。

行为层面因此需要很强的动作预测/动作重复成分，同时保留较小但稳定的 reward-dependent update。这里不直接把行为 APE 指认为 VTA APE；神经归属必须由独立时间分析判定。

来源：`ModelZoo_Atlas_v9_20260930`；本地实现 `soe_ucl_ape_rpe_v1.py`。

## 3. VTA 时间顺序：当前最强的 SLM 神经判别

固定时间轴 authority：
- Early / Actor policy：effect=.810，P=.046875。
- Middle / APE：effect=.667，P=.041566。
- Post / Actor-Critic RPE：effect=.867，P=.019531。

SLM 三个预设轴全部为正且显著。Q-all：
- Early=.048，P=1.0。
- Middle=−.357，P=.820。
- Post=.867，P=.019531。

通用 Q/RPE 可以解释结果后信号；它没有恢复结果前策略和中段 APE 的时间结构。这是当前区分完整 SLM 与单纯 post-outcome RPE 的主要神经证据。

来源：`DA_global_temporal_model_adjudication_v4_authority.csv`。

## 4. 结果后误差表示：标量 RPE 与结果向量 PE

在相同 Core-v2 历史基线和整只动物留出条件下，n=9：
- signed RPE + |RPE|：mean held-out MSE gain=.01518；6/9 改善；median improvement=3.50%；P=.074。
- signed outcome-vector PE：mean gain=.00544。
- vector PE + |PE|：mean gain=.00871。
- 在 scalar RPE 之后再加入 vector terms：incremental gain=−.00035，P=1.0。

当前数据在简洁性和留出表现上更支持结果后的标量 RPE-like 表示；n=9 的直接 scalar-vs-vector 配对仍然功效有限，因此 outcome-specific PE 保留为开放问题。

来源：`SOE_RL_Results_and_Figure_Legends_v3_20260921`。

## 5. 行为参数直接迁移到多巴胺

Passive credit 先完全由行为外层交叉验证选择，fold-level 权重为 0.75 或 1.0；神经数据不参与参数选择。

把这些行为参数直接带入 ActionBout dopamine：
- behavior-selected mapping > fixed credit=.75：9/9，P=.0039。
- behavior-selected mapping > fixed credit=1.0：9/9，P=.0039。

Post06 方向相同但配对证据更弱。

这条结果特别重要，因为它检验的是**行为模型参数能否在不利用神经数据调参的条件下迁移到 VTA**。

来源：`SOE_RL_Results_and_Figure_Legends_v3_20260921`。

## 6. 旧 Codex 3.2/3.3 的两条多巴胺计算路线

### 路线 A：State + Value + RPE / Full RL

旧 `v24Aligned` 神经回归：
- State：R²=.131；animal holdout=.029。
- State+RPE：.185；holdout=.071。
- State+Value+RPE：.195；holdout=.093。
- Full RL：.196；holdout=.092。
- RPE-only：.014；holdout=−.293。

旧结果的主要信息是当前状态承担大量可泛化多巴胺结构，RPE 在状态基础上增加解释量；RPE 单独跨动物泛化失败。它与现在 SLM 的“state representation + temporally localized update”方向一致。

### 路线 B：same-day fast update + cross-day slow prior

旧行为/DA bridge 输出包括：
- `day_prior_qdiff`
- `fast_qdiff_pre`
- `slow_qdiff_pre`
- `fast_rpe`
- `slow_rpe`

Day 1 的 fast Q 在 33/39 动物改善选择预测（P≈3.1×10⁻⁶）；Days 2–14 再加入 day-start prior 继续提高预测（P≈.004）。对应神经解释为：
- observation/view period：结果前 policy/value/belief；
- outcome period：当前事件 RPE/surprise/update。

这套旧分解与当前“多时间尺度行为状态 + 事件内 VTA 时间顺序”可以互相对照。旧结果作为历史审计保留；主结论继续由当前严格 held-animal authority 决定。

## 7. SLM 内部变量与不同学习表型

全 40 只动物：
- |RPE| Δ vs conversion Δ：ρ=.615，P=2.43×10⁻⁵。
- late credit separation vs late Active|Observe：ρ=.558，P=.000181。
- Qdiff Δ vs SRI Δ：ρ=.556，P=.000192。
- policy Δ vs SRI Δ：ρ=.453，P=.00337。
- |APE| Δ vs late SRI：ρ=.383，P=.01463。

这些结果把 SLM 内部变量连接到不同学习表型。它们作为相关性桥梁使用；机制判别仍由模型对照、VTA 时间轴和 JAWS 因果实验完成。

来源：`SLM_all40_training_dynamics_latent_bridge_stats_v1.csv`。

## 8. 当前整合

现在 SLM 获得六个互补方向的支持：
1. 行为结果会在下一次决策立刻重设社会信息需求。
2. 分钟级历史与跨天先验继续塑造同一采样策略。
3. 行为模型需要动作预测成分，并保留较小 reward-dependent update。
4. VTA 按 policy → APE → post-outcome update 的顺序表达计算。
5. 结果后误差表示目前以 scalar RPE-like 最简洁；这定义了 SLM 的边界，而不削弱事件内时间结构。
6. 行为中独立学到的 Passive credit 能直接迁移到 VTA，多巴胺参数无需重新拟合。

对应数据总表：`data/SLM_multiaxis_mechanistic_support_v75.csv`。
