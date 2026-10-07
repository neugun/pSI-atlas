# -*- coding: utf-8 -*-
from pathlib import Path
import pandas as pd

R=Path(__file__).resolve().parents[1]

ZH_MAIN='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_social_sampling_specificity_v92.png" rel="noopener" target="_blank"><img alt="有效社会观察状态对 VTA 多巴胺的选择性招募" loading="lazy" src="assets/SOE_FP_social_sampling_specificity_v92.png"/></a><figcaption><strong>VTA 多巴胺在动物真正进入有效社会信息采样状态时被选择性招募。</strong>A，观察区内真实观察相对同一区域随机“不观察”时刻产生明显的结果后上升，0–6 秒为 8/9 动物同方向，P=.0078，因此空间位置本身不足以解释信号。B，真实观察区内相对观察区外在 0–2 秒和 0–6 秒均为 9/9 动物更高（P=.0039）。C，这个差异贯穿真实 observation bout，整段为 8/9，P=.0078。D，单纯示范鼠状态转换相对同区域随机时刻没有产生对应信号（inside P=1.0；outside P=.910）。这组控制把观察期 VTA 活动定位到有效社会信息采样，而非一般位置、时间或同伴动作变化。</figcaption></figure>'''

EN_MAIN='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_social_sampling_specificity_v92.png" rel="noopener" target="_blank"><img alt="Selective recruitment of VTA dopamine during effective social observation" loading="lazy" src="assets/SOE_FP_social_sampling_specificity_v92.png"/></a><figcaption><strong>VTA dopamine is selectively recruited when the learner enters an effective social-information-sampling state.</strong>A, real observation inside the observation zone exceeds random no-observation moments in the same zone (8/9 animals over 0–6 s, P=.0078), arguing against location alone. B, inside observation exceeds outside observation in 9/9 animals over both 0–2 s and 0–6 s (P=.0039). C, the difference persists across the real observation bout (8/9, P=.0078). D, demonstrator transitions alone do not reproduce the response relative to matched random moments (inside P=1.0; outside P=.910). Together these controls localize the VTA signal to effective social sampling rather than generic location, time, or demonstrator movement.</figcaption></figure>'''

ZH_SUPPORT='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_additional_events_v91.png" rel="noopener" target="_blank"><img alt="示范鼠事件和学习者自身进食在固定时间与真实行为时长中的 VTA 多巴胺" loading="lazy" src="assets/SOE_FP_PSTH_additional_events_v91.png"/></a><figcaption><strong>额外事件给出阴性和阳性时间控制。</strong>A–B，示范鼠 triggered 与 untriggered 事件在事件后的固定窗口及真实 bout 全程都没有形成稳定差异（P=.129），说明单纯示范鼠事件类别不能复制主要观察/结果信号。C–D，学习者自身进食提供清楚的阳性对照：进食开始后 0–2 秒相对自身前状态为 8/9 动物升高（P=.0117），真实 feeding bout 全程 9/9 高于零（P=.0039）。</figcaption></figure>'''

EN_SUPPORT='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_additional_events_v91.png" rel="noopener" target="_blank"><img alt="Demonstrator events and observer feeding in fixed-time and real-bout dopamine views" loading="lazy" src="assets/SOE_FP_PSTH_additional_events_v91.png"/></a><figcaption><strong>Additional events provide negative and positive temporal controls.</strong>A–B, demonstrator-triggered versus untriggered events do not form a stable post-event or whole-bout difference (P=.129), so demonstrator event class alone does not reproduce the main observation/outcome signal. C–D, the learner's own feeding provides a clear positive control: dopamine rises after feeding onset in 8/9 animals (P=.0117) and remains above zero across the real feeding bout in 9/9 animals (P=.0039).</figcaption></figure>'''

for fn,main,support in [("index-zh.html",ZH_MAIN,ZH_SUPPORT),("index.html",EN_MAIN,EN_SUPPORT)]:
    p=R/fn; s=p.read_text(encoding="utf-8")
    if "SOE_FP_social_sampling_specificity_v92.png" not in s:
        anchor='<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_biological_story_v82.png"'
        if anchor not in s: raise RuntimeError("main anchor missing "+fn)
        s=s.replace(anchor,main+"\n"+anchor,1)
    if "SOE_FP_PSTH_additional_events_v91.png" not in s:
        anchor='<figure class="figure evidence-figure"><a class="figure-zoom" href="assets/SOE_FP_PSTH_trial_heatmaps_v82.png"'
        if anchor not in s: raise RuntimeError("support anchor missing "+fn)
        s=s.replace(anchor,support+"\n"+anchor,1)
    if fn=="index-zh.html":
        old='<div class="bio-logic"><strong>两种多巴胺读法回答两个互补问题｜</strong>固定结果后 0–6 秒强调结果出现后的评估与更新；真实行为时长归一化强调行为执行期间的多巴胺。把两种时间表示放在同一批事件上，可以直接看到哪些结果跨方法保留，哪些计算更依赖结果后的持续信号。</div>'
        new='<div class="bio-logic"><strong>先定位观察期信号，再解释结果后的学习｜</strong>有效观察开始后 VTA 多巴胺选择性升高；同一区域随机不观察、观察区外以及单纯示范鼠状态转换都不能复制这一变化。结果出现后，再用固定 0–6 秒与真实行为时长两种表示区分行为执行期信号和持续的结果评估与更新。</div>'
    else:
        old='<div class="bio-logic"><strong>The two readouts answer complementary biological questions.</strong> The fixed 0–6 s window emphasizes evaluation and updating after an outcome appears; actual-bout normalization emphasizes dopamine expressed while the behavior is being executed. Applying both views to the same events reveals which effects are method-invariant and which depend on sustained post-outcome activity.</div>'
        new='<div class="bio-logic"><strong>First localize the observation signal, then resolve outcome learning in time.</strong> VTA dopamine rises selectively when effective observation begins; random no-observation moments in the same location, outside-zone observation, and demonstrator transitions do not reproduce the response. After an outcome occurs, fixed 0–6 s and actual-bout views separate execution-period activity from sustained evaluation and updating.</div>'
    if old in s: s=s.replace(old,new,1)
    p.write_text(s,encoding="utf-8")

# Add strong observations to the mechanistic authority.
p=R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv"
m=pd.read_csv(p)
extra=pd.DataFrame([
["fp_social_sampling","Observe_inside_vs_random_inside_post06","paired_DA_contrast",0.346703,9,0.0078125,"观察区内真实观察高于同区域随机不观察时刻，8/9 动物同方向；位置本身不足以解释 VTA 招募","SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv"],
["fp_social_sampling","Observe_inside_vs_outside_post02","paired_DA_contrast",0.301634,9,0.00390625,"观察开始后 0–2 秒 inside 高于 outside，9/9 动物同方向","SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv"],
["fp_social_sampling","Observe_inside_vs_outside_whole_bout","paired_DA_contrast",0.294520,9,0.0078125,"inside 相对 outside 的 VTA 差异贯穿真实观察 bout，8/9 动物同方向","SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv"],
["fp_social_sampling_control","Dem_transition_inside_vs_random_post02","paired_DA_contrast",-0.000296,9,1.0,"示范鼠状态转换本身在 inside 条件下不能复制观察相关 VTA 信号","SOE_FP_SOCIAL_SAMPLING_SPECIFICITY_v92.csv"],
["fp_positive_control","Observer_feeding_post_vs_pre","paired_DA_change",0.347997,9,0.01171875,"学习者自身进食开始后 VTA 多巴胺相对自身前状态升高，8/9 动物同方向","SOE_FP_EVENT_CONTROL_STATS_v90.csv"],
["fp_positive_control","Observer_feeding_whole_bout","one_sample_DA",0.349109,9,0.00390625,"学习者自身进食真实 bout 全程 VTA 多巴胺高于零，9/9 动物同方向","SOE_FP_ADDITIONAL_BOUT_EVENT_STATS_v91.csv"],
],columns=m.columns)
for key in extra.test: m=m[m.test.astype(str)!=key]
m=pd.concat([m,extra],ignore_index=True); m.to_csv(p,index=False)
print("patched v91-v93 specificity story")
