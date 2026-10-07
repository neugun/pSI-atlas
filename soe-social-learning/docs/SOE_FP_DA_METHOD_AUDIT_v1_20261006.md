# SOE：Fiber photometry → 多巴胺数值的双定义审计

日期：2026-10-06

## 这里比较的是什么

这里比较的是**同一条 fiber-photometry 信号如何压成一个事件级多巴胺数值**，不是后续 RPE/APE 模型本身。

两种定义都来自同一套处理后的 FP trace，只改变事件内积分的时间范围：

- **固定 0–6 s（Post06）**：每个事件统一取结果后 0–6 s，多巴胺 AUC/秒。
- **真实行动 bout（ActionBout）**：从真实行动起点积分到真实 bout 终点，再除以真实 bout 时长；<0.05 s 的近零 bout 排除。

## 公平比较

为避免两种 readout 因纳入事件不同产生假差异，主审计只保留两种 target 都有效的共同事件：

- 1,371 个事件
- 9 只 principal FP animals
- 每只动物中两种 DA 数值均正相关
- Spearman ρ 范围 0.520–0.944，中位数 0.785

因此两种算法主要抓住同一底层多巴胺过程，只是对事件内部时间段的加权不同。

## 行为→神经归因映射跨两种算法成立

Passive social-credit 参数先完全由行为数据选择，神经数据不参与调参，然后冻结参数去预测多巴胺。

相对固定 credit=0.75：

- ActionBout：9/9 动物 behavior-selected 更好，P=.00391
- 0–6 s：7/9 更好，P=.0273
- 同一动物的模型增益跨 readout 相关：ρ=.733，P=.0246
- 7/9 动物在两种 readout 中同时为正
- 两种 readout 的归一化 credit-gain 差异：P=.0977

相对固定 credit=1.0：

- ActionBout：9/9 更好，P=.00391
- 0–6 s：7/9 更好，P=.0391
- 模型增益跨 readout 相关：ρ=.800，P=.00963
- 7/9 动物在两种 readout 中同时为正
- 两种 readout 的归一化 credit-gain 差异：P=.0977

所以最强结论是：**行为中学到的 source-specific social credit 能跨两种 FP→DA 定义直接迁移到 VTA。**

## 结果后误差项：固定窗统计证据更强，但方向跨算法保留

actor |RPE|：

- 0–6 s：8/9 动物改善，P=.0391
- ActionBout：7/9 动物方向改善，P=.164
- 7/9 动物在两种 readout 中同时改善
- 按各自 baseline MSE 归一化后，中位增益约为 1.76% vs 0.69%
- readout 间直接差异：P=.164

因此当前数据支持：**固定 0–6 s 对部分结果后误差/更新成分具有更高灵敏度**，但并不足以证明两种窗口对应两套不同机制。

## 解释边界

- 不把“一个 readout 显著、另一个未显著”直接当作显著 interaction。
- 主要结论优先使用跨两种定义重复的结果。
- 单一 readout 更强的结果只用于描述时间敏感性。
- 当前最稳健的新结果是行为→神经 social-credit bridge 对 FP 积分窗口不敏感。

## Source data

- data/fp_da_common_event_v1/actor_common_event_metrics.csv
- data/fp_da_common_event_v1/actor_common_event_contrasts.csv
- data/fp_da_common_event_v1/passive_credit_common_event_metrics.csv
- data/fp_da_common_event_v1/passive_credit_common_event_contrasts.csv
- data/fp_da_common_event_v1/target_agreement_per_animal.csv
- data/SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv
- data/SLM_FP_DA_CROSS_READOUT_PER_ANIMAL_v1.csv
