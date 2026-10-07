# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd, re
R=Path(__file__).resolve().parents[1]

p=R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv"
m=pd.read_csv(p)
new=pd.DataFrame([
["codex_exact_replication","Q_RPE_signed_abs_both_readouts","median_MSE_gain_pct","4.097_fixed__2.672_bout",9,0.0546875,"Q-RPE+|RPE| 在两种 DA 读出中方向一致；真实行为时长证据减弱，固定结果后窗口更敏感","SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv"],
["codex_exact_replication","Actor_RPE_abs_both_readouts","median_MSE_gain_pct","2.722_fixed__1.785_bout",9,0.359375,"Actor RPE+|RPE| 在两种读出中保持正向，固定结果后窗口更强","SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv"],
["codex_exact_replication","Passive_credit_vs_fixed075_both","animals_better","7_of_9_fixed__9_of_9_bout",9,0.00390625,"行为独立学到的社会归因在两种 DA 读出中均迁移到 VTA","SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv"],
["codex_exact_replication","Passive_credit_vs_fixed100_both","animals_better","6_of_9_fixed__9_of_9_bout",9,0.00390625,"行为独立学到的社会归因在两种 DA 读出中均保持优势","SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv"],
["codex_exact_replication","Vector_after_scalar_both","incremental_MSE_gain","-0.000354_fixed__-0.000587_bout",9,0.49609375,"结果向量误差在两种读出中加入标量 RPE 后均无额外收益","SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv"],
["codex_temporal_boundary","Whole_observation_bout_policy","median_within_animal_rho",0.186066,6,0.4375,"整个观察片段平均会稀释原本局限于 early window 的采样策略信号","SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv"],
["codex_temporal_boundary","Whole_observation_bout_APE_x_SRI","spearman_rho",-0.119048,8,0.778886,"整个观察片段平均不能替代 middle-window APE 时间定位","SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv"],
],columns=m.columns)
for key in new.test:
    m=m[m.test.astype(str)!=str(key)]
m=pd.concat([m,new],ignore_index=True)
m.to_csv(p,index=False)

p=R/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md"
s=p.read_text(encoding="utf-8")
sec='''## 6. Codex FP→DA 读出对原 VTA–SLM 结论的复现

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

### 6.2 Early / middle 不能用整个 observation bout 的平均值直接替代

原来的 early policy 和 middle APE 是时间定位后的计算。Codex 的 whole-observation-bout AUC/秒回答的是整个观察片段平均有多少 DA，它改变了 estimand。

把整个 observation bout 直接拿来做镜像检查时：
- 原 early-policy 动物集：whole-bout policy association 的中位数 ρ=.186，P=.438。
- 原 middle-APE 动物集：animal-level APE coupling 与 SRI 的关系 ρ=−.119，P=.779；原 middle-window authority 为 ρ=.667，P=.0416。

因此 whole-bout averaging 会稀释事件内部短暂计算。结果期可以进行严格的同事件双读出复现；结果前和中段仍应使用时间分辨分析。这也是 PSTH 和原 temporal adjudication 必须保留的原因。

来源：data/SOE_VTA_CODEX_EXACT_REPLICATION_v96.csv；data/SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv。

'''
s=re.sub(r'## 6\. .*?(?=## 7\.)',sec,s,flags=re.S)

psth='''## 7A. PSTH 的作用：把模型效应展开回真实时间过程

新增 PSTH 回答三个时间问题：

1. 有效社会采样何时招募 VTA？真实观察区内观察高于同区域随机不观察（0–6 秒 8/9，P=.00781），也高于观察区外（0–2 秒和 0–6 秒均 9/9，P=.00391）；示范鼠状态转换控制为阴性。
2. 不同结果的 DA 时间结构是什么？Active 更快，Passive 更持续，Unrewarded 进入负向状态；这个时间结构解释了为什么固定结果后窗口与真实行动片段对 RPE 有不同灵敏度。
3. 结果后的状态会不会进入下一次观察？下一次观察开始前，Active 和 Passive 后的 VTA 状态已经高于 Unrewarded；差异在观察开始后和真实观察片段早期继续存在。

PSTH 曲线在页面上仅作轻度高斯平滑以帮助观察趋势：固定时间曲线 σ=1.5 个 0.1 秒时间格，行为片段相位曲线 σ=2 个相位点。统计窗口、逐动物效应和 P 值全部使用未平滑数据。

这三组结果共同补足 SLM 的时间解释：有效社会采样招募 VTA，结果类型形成不同的 update state，这个状态随后进入下一次社会信息采样。

'''
if "## 7A. PSTH 的作用" not in s:
    s=s.replace("## 8. 当前整合",psth+"## 8. 当前整合",1)

old='''现在 SLM 获得六个互补方向的支持：
1. 行为结果会在下一次决策立刻重设社会信息需求。
2. 分钟级历史与跨天先验继续塑造同一采样策略。
3. 行为模型需要动作预测成分，并保留较小 reward-dependent update。
4. VTA 按 policy → APE → post-outcome update 的顺序表达计算。
5. 结果后误差表示目前以 scalar RPE-like 最简洁；这定义了 SLM 的边界，而不削弱事件内时间结构。
6. 行为中独立学到的 Passive credit 能直接迁移到 VTA，多巴胺参数无需重新拟合。
'''
newtxt='''当前证据形成一条连续链：
1. 行为结果会在下一次决策立刻重设社会信息需求。
2. 分钟级历史与跨天先验继续塑造同一采样策略。
3. 行为模型需要动作预测成分，并保留结果依赖的更新。
4. 原始 VTA 时间分析把采样策略 → APE → 结果后更新放在正确的事件内顺序。
5. Codex 真实行动时长读出重复了结果期最关键的行为→神经映射：社会结果归因跨方法成立，标量 RPE 仍比测试的结果向量更简洁。
6. 固定结果后窗口对 RPE 更敏感，PSTH 显示其时间来源是动作结束后仍持续的结果评估与更新。
7. 有效社会观察选择性招募 VTA，而上一结果形成的 VTA 状态还能延续到下一次观察。
'''
if old in s:
    s=s.replace(old,newtxt,1)
p.write_text(s,encoding="utf-8")
print("v99 authority/docs updated")
