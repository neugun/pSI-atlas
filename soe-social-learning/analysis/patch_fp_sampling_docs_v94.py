# -*- coding: utf-8 -*-
from pathlib import Path
R=Path(__file__).resolve().parents[1]

# Biological note
p=R/"docs"/"SOE_FP_PSTH_BIOLOGICAL_READOUT_v1_20261006.md"
s=p.read_text(encoding="utf-8")
sec='''## 2C. 观察期 VTA 信号属于有效社会信息采样状态

新增位置和事件控制后，观察期信号的来源更清楚：

- **真实观察 vs 同一区域随机不观察**：观察区内，真实观察开始后 0–2 秒为 7/9 动物更高，P=.0273；0–6 秒为 8/9，P=.00781。空间位置本身不能解释观察相关 VTA 上升。
- **观察区内 vs 观察区外**：0–2 秒和 0–6 秒均为 9/9 动物观察区内更高，P=.00391。
- **真实观察 bout**：把每次观察按真实持续时间归一化，观察区内相对观察区外的差异贯穿整个 bout；整段 8/9 同方向，P=.00781，前 25% 也成立，P=.0195。
- **示范鼠状态转换控制**：inside transition 相对同区域随机时刻，0–2 秒 P=1.0；outside transition P=.910。单纯同伴状态变化不能复制观察期 VTA 信号。

这组结果支持一个更具体的解释：**VTA 在动物真正进入有效社会信息采样状态时被选择性招募。** 它与 SLM 的结果前采样策略形成直接的生理对应，同时位置匹配和同伴转换控制排除了两个简单解释。

学习者自身进食提供独立阳性控制：进食开始后 0–2 秒相对自身前状态为 8/9 升高，P=.0117；按真实 feeding bout 归一化后，整段 9/9 高于零，P=.00391。

示范鼠触发与未触发事件在事件后固定时间和真实 bout 全程均没有稳定差异（P=.129），因此这一事件类别本身不足以解释主要观察和结果信号。

'''
if "## 2C. 观察期 VTA 信号属于有效社会信息采样状态" not in s:
    s=s.replace("## 3. 上一次结果会延续到下一次观察",sec+"## 3. 上一次结果会延续到下一次观察",1)
# extend source/figure list
s=s.replace("- data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv",
            "- data/SOE_FP_NEXT_OBSERVE_STATE_STATS_v83.csv\n- data/SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv\n- data/SOE_FP_EVENT_CONTROL_STATS_v90.csv\n- data/SOE_FP_EVENT_CONTROL_ANIMAL_CURVES_v90.csv\n- data/SOE_FP_ADDITIONAL_BOUT_EVENT_STATS_v91.csv\n- data/SOE_FP_ADDITIONAL_EVENT_CURVES_v91.csv",1)
s=s.replace("- assets/SOE_FP_next_observe_memory_v83.*",
            "- assets/SOE_FP_next_observe_memory_v83.*\n- assets/SOE_FP_social_sampling_specificity_v92.*\n- assets/SOE_FP_PSTH_event_controls_v90.*\n- assets/SOE_FP_PSTH_additional_events_v91.*",1)
p.write_text(s,encoding="utf-8")

# Add source cards to reader pages.
for fn,zh in [("index-zh.html",True),("index.html",False)]:
    p=R/fn; s=p.read_text(encoding="utf-8")
    if "SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv" not in s:
        if zh:
            old='<div class="download-card"><a href="data/SOE_FP_PSTH_MODEL_VARIABLES_v88.csv">SLM 变量分层 PSTH 源数据</a><p>采样策略、|RPE| 和更新幅度高低条件下的动物级平均时间曲线。</p></div>'
            new=old+'<div class="download-card"><a href="data/SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv">有效社会采样特异性统计</a><p>真实观察、位置匹配随机时刻、观察区内外和示范鼠状态转换的逐动物检验。</p></div><div class="download-card"><a href="data/SOE_FP_EVENT_CONTROL_ANIMAL_CURVES_v90.csv">额外事件 PSTH 源数据</a><p>示范鼠事件、随机不观察、状态转换和学习者自身进食的逐动物时间曲线。</p></div>'
        else:
            old='<div class="download-card"><a href="data/SOE_FP_PSTH_MODEL_VARIABLES_v88.csv">SLM-stratified PSTH source data</a><p>Animal-level curves for high versus low sampling policy, |RPE| and actor update magnitude.</p></div>'
            new=old+'<div class="download-card"><a href="data/SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv">Social-sampling specificity statistics</a><p>Animal-level tests for real observation, location-matched random moments, inside/outside observation and demonstrator transitions.</p></div><div class="download-card"><a href="data/SOE_FP_EVENT_CONTROL_ANIMAL_CURVES_v90.csv">Additional-event PSTH source data</a><p>Animal-level curves for demonstrator events, random no-observation controls, transitions and the learner\'s own feeding.</p></div>'
        if old not in s: raise RuntimeError("download marker missing "+fn)
        s=s.replace(old,new,1)
    p.write_text(s,encoding="utf-8")
print("updated v94 docs and source cards")
