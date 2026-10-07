# Reward Contrast 全局研究审计与执行总纲 v2

**日期：2026-10-07。状态：研究证据与执行计划；不是新增实验数据。**
**代码 authority：GitHub pSI-atlas；进入本次审计时为 e51220c。**
**原则：保留 Fig.0–7 / ED1–10 全面证据；不把阴性结果隐去，不把模型预测排名误写为机制证明。**

## 一、研究的中心问题与统一假说

中心问题不是“哪种奖赏本身好”，而是“近期采样形成的内部奖赏参照怎样改变同一个当前奖赏的神经意义和行为意义”。Science 2025 建立持续性 VTA-DA、periLC→VTA 和摄食因果基础；Reward Contrast 要解释持续信号包含哪些计算成分、存在哪里、如何影响动作，并问这些成分能否跨食物与社会奖赏泛化。

工作性架构：实际采样历史 → 潜在参照 R → 在当前采样后显现历史相对价值 / 更广义的状态相关误差信号 → VTA-DA → 动作持续性。**其中间完整中介链尚未通过逐节点因果干预建立。** 数学表征 C=U−R 是紧凑的候选计算，不等于已经发现了唯一生物算法。

## 二、Fig.0–7 证据清单与缺口

| 图 | 已完成、可引用的结果 | 不能升级的结论 | 继续执行 |
|---|---|---|---|
| Fig.0 | 明确 H/L 稳态与 S/N 交替任务、进食段 >5 s 间隔定义、局部 DA 记录、队列重叠、分析时窗 | cohort/条件不全部独立；H/L 与 S/N 并非随机交叉同一个历史因素 | 重建 session 与动物 manifest，逐图对照 |
| Fig.1 | 同当前奖赏的方向对齐效应在 9/9 小鼠为正；DA、feeding 各 P≈.00391 | 不等于完全随机操纵 R；稳定与交替 session 仍可能有差异 | exact session、order、deprivation、bout-level 改善 |
| Fig.2 | Passive-time first-sample 对 DA 的增量很弱（最大 ΔR²=.00385；P>.55）；先前舔舐数/摄食时长额外解释（ΔR²≈.0321/.0451） | 不能仅凭相关数据判断“每舔一次就是一次 R 更新”；剂量四分位呈非单调 | 按 actual sample number/volume/time 分解 |
| Fig.3 | 留一动物预测：U R²≈.038、类别情境≈.123、C≈.175、context+C≈.178；更深采样历史 ΔR²≈.027、P≈.0067 | α=.15/.20 不是唯一生物时间常数 | 严格 nested CV、检查 state 构造与时间泄漏 |
| Fig.4 | 模型库已整理至 31 family；FullHistory 对 belief/HMM/reward-rate/Value-RNN 仍有独立增量；continuous-time HMM 的原始预测最好之一（relative MAE≈.923） | 31 类不等于全部 31 个独立实测比较；包含不可辨识模型、任务不匹配和历史恢复项 | 单独展示 tested / boundary / recovery；冻结主检验及双向增量 |
| Fig.5 | 11 鼠、192 个适用进食段；持续期 C 比早期强 +1.458，11/11 方向一致；U 正、R 负 | 不能把 pre-bout 的 C 系数当成已采样当前效用；不能忽略 >5 s 存活者选择 | 原始 DA、行动协变量、风险集分析；审计不同 U/R 模型尺度 |
| Fig.6 | QE 跨质量转移：7 鼠、ΔR²≈.0254、P≈.00141；不同价值干预方向有一致性 | 跨任务具有不同时间波形；不证明每种 manipulation 都更新同一种 R | 同一冻结 α / 冻结模型跨任务；独立讨论神经历史和行为 |
| Fig.7 | Acute VTA-DA 激活减少终止（OR≈.690），contingent Jaws 增加终止（OR≈1.341）；Stim13 显著神经历史 ΔR²≈.002524，P=5e-5，边际时长 P≈.742 | Jaws/activation 证明 DA 对 persistence 有因果作用，不等于已证明 R→DA→行为完整中介 | 编码期 vs 探测期的时序因果干预；保持 acute 与 history 分开 |

ED1–10 继续保留：行动控制、Stim13 历史、正负不对称、原始 DA/非线性控制、疾病/生理状态、时间尺度、history proxy、记忆/表达分层和 local-history gate。**有统计结论就保留对应图及 n、P、检验；没有证据支持时明确标 NULL/PROVISIONAL，而不是删图。**

## 三、对三种任务的统一判断

Natural：当前奖赏 potency、神经历史、行为历史均有支持。当前奖赏可能调制历史敏感性，但在 local-history×current 竞争后，独立 deep-reference identity gate **未建立**。Natural deep R 主效应在神经端仍支持（exact-wild P≈.0083）。

QE：神经历史跨任务支持；边际行为历史和 current-conditioned 结构是 **provisional**；不同潜伏期不能当作失败。六只 common-support 小鼠的交互项不足以升级为普遍机制。

Stim13：过去 ON/OFF 历史稳定影响后续神经 DA（全控制独立 ΔR²≈.002524、P=5e-5），但边际时长历史并不显著。current-conditioned duration 结构会被近期局部历史吸收；不能称为通用深层参照行为门控。**没有检出 ≠ 已证明等效或完全无效。**

## 四、需要立即纠正的计算可辨识性错误（最高优先级）

C=U−R：只要定义如此，U、R、C 就不能同时作为三个自由回归列；如果 E 是显式期待值，δ=U−E 也不能和 U、E 同时作为独立自由列。完全交叉历史×当前奖赏可以改善 U 与 R 的共同支持与独立估计，**不能解除这些代数恒等式**。

正确竞争：
- M1：自由系数 βU U + βR R，与固定比例/反号约束的 βC(U−R) 比较；不在同一个自由矩阵中硬加三列。
- M2：当前奖赏 U、外显线索 E、历史 R 可按独立操纵估计；经典 cue-RPE = U−E 与广义 state-TD / recurrent learner 做冻结的跨动物/跨 session 预测比较。
- M3：same-current/same-cue history effect，在 nuisance licking、bout stage、session progression、动物、感觉、饱腹等控制后是否仍存在。
- M4：cue / first-sample / 0–2s / 2–5s / post-bout 分窗，同时重算是否被“只有持续超过 5 s 才进入 2–5 s”选择偏差驱动。
- “相同预测 probe 的 cue-RPE ≈0”只能作为经过行为期待验证的操作性目标；历史可能改变隐含期待，因此不能声称所有 generalized RPE≈0。

主推的新范式应为 **历史（高/低）× 显式线索期待（高/低）× 实际当前奖赏（高/低）** 的交叉/含 catch/omission 设计，保留足够每个动物每个组合的 trials 和共同支持；刺激和状态变化作为后续独立因子，而不是一开始无限叠加。

## 五、Hedonic contrast：下一代实验的可执行路径

短尺度：保留原 120-s 交替范式作为连续历史形成范例；增加真正随机、同当前探测奖赏的 history manipulation，精确打散采样次数、采样体积、未采样的经过时间与奖励线索。

长尺度：**30 分钟基线 → 60 分钟 rich/neutral/lean induction → 30 分钟完全相同 8% 蔗糖 probe**。先检验 induction 是否真正改变参照而非单纯饱腹或感觉适应：需配对热量/实际摄入量、相同 reward identity 控制、线索暴露、未摄入但可感知的对照、状态和时序反平衡。

区分“想要/动作”与“喜欢”：平行自由进食和口腔内给液。记录 DA、lick microstructure、接受/拒绝、口面味觉反应（taste reactivity）、re-engagement、终止危险率和延迟变化。单独的 lick count 或 bout duration 不足以作为 pure pleasure 的证明。

增益/损失对称：正负通道 [U−R]+ / [R−U]+ 在 Natural 与 Stim13 不能声称显著不对称（交互 P≈.216/.197），QE 有更强证据（P≈.000527）。新实验需要平衡 upward/downward shift 的 current distribution 与统计功效。

## 六、单细胞与分子实现：已有基础和具体缺口

D1–D9：D3 100E，D4/D9 20E，D5 100E↔20E，D6 100E↔100E+quinine，D7 50E，D8 100E↔50E，D1/D2 trace conditioning。这些记录已建立从多个奖励质量/浓度到 same-cell 长程追踪的基础，但没有完全交叉独立的 R 与 U，因此不能从单一偏好直接宣称专门 contrast neurons。

信号来源 QC：对每一 ROI/试次同时保留 raw ROI、CaRMA v3 corrected、Suite2p neuropil corrected、background、frame movie、mask、定位和跨天身份。即使两种校正方法彼此高度一致，也不能排除二者共同减掉 condition-locked 生物信号。每个生物结论至少需要 raw vs corrected 敏感性；不得让旧的 sub1 独占生物 authority。

解析顺序：trial/cell/session manifest → motion/ROI/source QC → raw/corrected event PSTH → same-cell D1–D9 identities → cross-validated U/R/C/RPE/action/state models → population axes 跨日稳定性 → 跨 reward identity transfer → retrospective EASI/EASEQ-FISH（>100 基因）与 projection enrichment → targeted causal double dissociation。

要判“专门细胞类群”，至少需要同细胞稳定、held-out generalization、分子/投射富集、选择性因果；群体轴稳定但参与单细胞变化，则支持分布式 manifold。二者都不应先验预设。

## 七、Social contrast / SOE / 动作阈值：第二条主线

社会对比保留原先的核心约束：雄鼠连续暴露雌鼠；ON=可真实互动，OFF=雌鼠仍可见/存在但不可接触。检验 ON→OFF vs OFF→OFF、OFF→ON vs ON→ON；counterbalance 雌鼠身份、暴露时间、屏障和气味/视觉/听觉刺激。增加 Female A→A/B 以检验 partner-specific vs generalized social reference。

pSI 光刺激不等于“奖赏本身”；作为 attack-threshold **submaximal probe**（5/10/20/40Hz 校准后选择非 ceiling 区间），拟合 input-output/攻击阈值而非只比较有无攻击。同步记录 approach、contact attempts、USV、withdrawal、redirected behavior 和 DA/pSI，避免把单一攻击率误判为快乐程度。

SOE 观察他人摄食的数据提供第三种历史来源：self-sampled 与 observed-other reward 是否更新同一种 R？以 visibility、familiarity、demonstrator value、observer state 和独立行动 history 为因子。先冻结 food contrast 模型，后在 observed reward 中做真正外推；不要在 social 数据上重新拟合参数后就称为 common currency。把 OXT→VTA social-state、NAc/DMS DA release、learning effects 作为相邻验证项目，不假装其 reward-contrast 模型已执行。

## 八、回路与疾病状态的长期机制目标

可能的级联：periLC^VGLUT2/VTA^VGAT 与当前食物价值/摄食驱动有关；VTA 内局部 GABA/DA、BLA、insula、gustatory thalamus、PBN、pSI、NAc 与参照记忆、比较及行动读出可能分别承担不同环节。**目前不能指定哪个节点一定储存 R**。必须分开历史编码期、当前比较期和行为输出期干预。

内部状态（饥饿、GLP-1R/semaglutide、肥胖/代谢异常、LiCl、不快感/慢性压力、社会隔离）分别检验：改变当前 U、参照 R、更新速率、正负非对称、C→DA 增益还是 DA→行为增益。历史编码期和当前探测期的状态应正交操纵，不能笼统描述“DA 更低”。

## 九、执行矩阵（按科学阻碍而非工作量排序）

| 优先级 | 立即工作 | 输入与可验证产物 | 完成标准 |
|---|---|---|---|
| P0-A | 全局科学/统计 authority 审计 | 当前 Fig0–7、ED1–10、n/统计/源表/图注 | 每个结论有唯一来源，不同尺度与模型不矛盾 |
| P0-B | 修正 rank / RPE 设计与实际模型检验 | 代码中的设计矩阵、冻结模型 family、trial 对齐 | 证明 rank 与 leakage 合法；U+R 对比约束 C，不错误声称三者独立 |
| P0-C | VTA 2P 生物信号可用性 | 每只动物每一天 raw/CaRMA/Suite2p、movies、ROI masks | QC、跨日 identity、per-cell responses 和 raw/corrected 敏感性齐全 |
| P0-D | Natural/QE/Stim13 统一 gate | 同 cohort、同 α、common support、local-history 控制、动物聚类 | PASS / PROVISIONAL / NULL 按 neural/marginal/conditional/deep 分开 |
| P1 | Food factorial + identical probe 实验 | history×cue expectation×current reward；acute/long induction | RPE vs comparator 的预测性判别，预注册主终点 |
| P2 | 长期 single-cell 与 reward identity | 冻结模型、same-cell 横跨任务、投射与分子 | 区分专门细胞和分布式 manifold |
| P3 | 社会 ON/OFF、Female A/B、SOE 迁移 | 固定 sensory exposure；冻结食物模型外推 | 独立 social history 对动作阈值及 DA 的效应 |
| P4 | 编码期/探测期环路因果与 disease state | periLC/VTA/pSI 等时序干预 | R 形成、神经读出、行动表达的双重分离 |

## 十、图文发布规范与研究终点

网页分为“主线证据”“完整 source/figures/模型库”“未来实验/决策表”；中文需真正中文，不允许机器式中英杂糅。每个有统计量的句子对应原始可审的主/补图、动物数、统计量及 P；方图优先，均值±SEM，散点/配对连接合理，统一颜色、无不必要上下右框和网格，保留 SVG/editable 源图。图不应只以点击深层页面才能看见主要结果。

GitHub Pages 的 noindex 和 robots.txt **不是访问控制**：在公开仓库中增加详细未发表材料前，应检查泄露风险。需要手机端私密阅读应使用真正访问控制或加密私有入口，不能把隐藏导航当成私有。

**最终科学终点**：证明一种由实际采样建立的奖赏历史状态怎样在持续行为中进入 DA 计算；揭示它与 generalized RPE 的关系、是否由稳定功能/分子细胞类群还是分布式状态空间实现，并以食物到社会、正常到疾病的预先冻结迁移检验其泛化边界。
