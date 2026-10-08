> **SOURCE CORRECTION (2026-10-07; v126):** Earlier references below to “real action-bout DA” or genuine real-bout social-credit coding are superseded. The field DA_ActionBout_AUCperSec measures an extended post-anchor model interval (median 28.85 s), not the actual observed 2.40-s observation bout. The historical n=1371 9/9 model-comparator result is preserved solely as a documented prior estimate. See [source-level correction and current 821-event triple-readout results](VTA_TRUE_BOUT_SOURCE_CORRECTION_v126_20261007.md). The frozen Early/Middle estimates and separate JAWS causal experiment have independent statistical contracts.

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

## 6. Codex FP→DA 读出对原 VTA–SLM 结论的复现

这一步的目的，是检验原有 VTA–SLM 结论能否在另一种 DA 量化方式下重现。

### 6.1 结果期可以做严格的同事件复现

固定结果后 0–6 秒与 Codex 真实行动片段 AUC/秒都有效的共同数据包括 1,371 个事件、9 只动物。行为参数、事件身份和模型比较保持不变，只替换 DA target。

- 两种 DA 数值逐动物均正相关：ρ=.520–.944，中位数 .785。
- Q-RPE+|RPE|：固定 0–6 秒中 8/9 改善，P=.00781；真实行动片段中 7/9 改善，P=.0547。
- Actor RPE+|RPE|：固定窗口 9/9，P=.00391；真实行动片段 6/9，P=.359。方向仍为正，但证据明显减弱。
- 行为数据独立选出的 Passive social credit 是最强跨方法复现：
  - 相对 fixed 0.75：固定窗口 7/9，P=.0391；真实行动片段 9/9，P=.00391。
  - 相对 fixed 1.0：固定窗口 6/9，P=.0547；真实行动片段 9/9，P=.00391。
- 标量 RPE 家族在两种读出中都强于测试的 outcome-vector PE；向量项加入标量 RPE 后均无增益：
  - 固定窗口 incremental MSE gain = −0.000354，P=1.0。
  - 真实行动片段 = −0.000587，P=.496。

这一组结果把原来的主要结果期结论分成两层。社会结果归因和标量 RPE 的组织方式跨读出稳定；RPE 效应强度受到积分时间范围影响。固定 0–6 秒包含动作结束后的结果评估，因此对持续的 outcome/update 信号更敏感。

### 6.2 Early / middle：保持原分析合同不变的 raw-FP 严格复现

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

## 7. SLM 内部变量与不同学习表型

全 40 只动物：
- |RPE| Δ vs conversion Δ：ρ=.615，P=2.43×10⁻⁵。
- late credit separation vs late Active|Observe：ρ=.558，P=.000181。
- Qdiff Δ vs SRI Δ：ρ=.556，P=.000192。
- policy Δ vs SRI Δ：ρ=.453，P=.00337。
- |APE| Δ vs late SRI：ρ=.383，P=.01463。

这些结果把 SLM 内部变量连接到不同学习表型。它们作为相关性桥梁使用；机制判别仍由模型对照、VTA 时间轴和 JAWS 因果实验完成。

来源：`SLM_all40_training_dynamics_latent_bridge_stats_v1.csv`。

## 7A. PSTH 的作用：把模型效应展开回真实时间过程

新增 PSTH 回答三个时间问题：

1. 有效社会采样何时招募 VTA？真实观察区内观察高于同区域随机不观察（0–6 秒 8/9，P=.00781），也高于观察区外（0–2 秒和 0–6 秒均 9/9，P=.00391）；示范鼠状态转换控制为阴性。
2. 不同结果的 DA 时间结构是什么？Active 更快，Passive 更持续，Unrewarded 进入负向状态；这个时间结构解释了为什么固定结果后窗口与真实行动片段对 RPE 有不同灵敏度。
3. 结果后的状态会不会进入下一次观察？下一次观察开始前，Active 和 Passive 后的 VTA 状态已经高于 Unrewarded；差异在观察开始后和真实观察片段早期继续存在。

PSTH 曲线在页面上仅作轻度高斯平滑以帮助观察趋势：固定时间曲线 σ=1.5 个 0.1 秒时间格，行为片段相位曲线 σ=2 个相位点。统计窗口、逐动物效应和 P 值全部使用未平滑数据。

这三组结果共同补足 SLM 的时间解释：有效社会采样招募 VTA，结果类型形成不同的 update state，这个状态随后进入下一次社会信息采样。

## 8. 当前整合

当前证据形成一条连续链：
1. 行为结果会在下一次决策立刻重设社会信息需求。
2. 分钟级历史与跨天先验继续塑造同一采样策略。
3. 行为模型需要动作预测成分，并保留结果依赖的更新。
4. 原始 VTA 时间分析把采样策略 → APE → 结果后更新放在正确的事件内顺序。
5. Codex 真实行动时长读出重复了结果期最关键的行为→神经映射：社会结果归因跨方法成立，标量 RPE 仍比测试的结果向量更简洁。
6. 固定结果后窗口对 RPE 更敏感，PSTH 显示其时间来源是动作结束后仍持续的结果评估与更新。
7. 有效社会观察选择性招募 VTA，而上一结果形成的 VTA 状态还能延续到下一次观察。

对应数据总表：`data/SLM_multiaxis_mechanistic_support_v75.csv`。
