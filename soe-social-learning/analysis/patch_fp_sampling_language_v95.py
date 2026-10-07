# -*- coding: utf-8 -*-
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/"index-zh.html"; s=p.read_text(encoding="utf-8")
reps={
"这个差异贯穿真实 observation bout，整段为 8/9，P=.0078。":"这个差异贯穿整个真实观察片段，整段为 8/9，P=.0078。",
"（inside P=1.0；outside P=.910）":"（观察区内 P=1.0；观察区外 P=.910）",
"这组控制把观察期 VTA 活动定位到有效社会信息采样，而非一般位置、时间或同伴动作变化。":"这组控制把观察期 VTA 活动定位到有效社会信息采样，同时排除了普通位置、时间和同伴动作变化这些简单解释。",
"并在真实观察 bout 内逐步升高":"并在真实观察片段内逐步升高",
"示范鼠 triggered 与 untriggered 事件":"示范鼠触发与未触发事件",
"及真实 bout 全程":"及真实行为片段全程",
"真实 feeding bout 全程":"整个真实进食片段",
}
for a,b in reps.items():
    if a not in s: print("WARN missing",a)
    s=s.replace(a,b,1)
# Full control-event PSTHs live in the supporting layer.
if "SOE_FP_PSTH_event_controls_v90.png" not in s:
    anchor='<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_additional_events_v91.png"'
    block='''<figure class="figure evidence-figure"><a class="figure-zoom" href="assets/SOE_FP_PSTH_event_controls_v90.png" rel="noopener" target="_blank"><img alt="多类观察和控制事件的 VTA 多巴胺时间过程" loading="lazy" src="assets/SOE_FP_PSTH_event_controls_v90.png"/></a><figcaption><strong>完整事件控制说明观察期信号具有选择性。</strong>A，观察区内真实观察高于同一区域随机不观察时刻。B，观察区外没有对应的事件后上升。C–D，示范鼠状态转换在观察区内外都与匹配随机时刻接近。E，示范鼠触发与未触发事件在事件后没有形成稳定差异。F，学习者自身进食产生清楚的正向多巴胺反应。完整控制集因此把有效社会观察与位置、同伴转换和一般信号质量区分开。</figcaption></figure>
'''
    if anchor not in s: raise RuntimeError("zh support anchor missing")
    s=s.replace(anchor,block+anchor,1)
p.write_text(s,encoding="utf-8")

p=R/"index.html"; s=p.read_text(encoding="utf-8")
if "SOE_FP_PSTH_event_controls_v90.png" not in s:
    anchor='<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_additional_events_v91.png"'
    block='''<figure class="figure evidence-figure"><a class="figure-zoom" href="assets/SOE_FP_PSTH_event_controls_v90.png" rel="noopener" target="_blank"><img alt="VTA dopamine time courses across observation and control events" loading="lazy" src="assets/SOE_FP_PSTH_event_controls_v90.png"/></a><figcaption><strong>The full event-control set shows that the observation signal is selective.</strong>A, real observation inside the zone exceeds random no-observation moments in the same location. B, outside-zone observation lacks the corresponding post-onset rise. C–D, demonstrator transitions inside or outside closely follow matched random moments. E, triggered versus untriggered demonstrator events do not produce a stable post-event difference. F, the learner's own feeding produces a clear positive dopamine response. Together these controls separate effective social observation from location, demonstrator transitions and general signal quality.</figcaption></figure>
'''
    if anchor not in s: raise RuntimeError("en support anchor missing")
    s=s.replace(anchor,block+anchor,1)
p.write_text(s,encoding="utf-8")
print("v95 language/control figure patch complete")
