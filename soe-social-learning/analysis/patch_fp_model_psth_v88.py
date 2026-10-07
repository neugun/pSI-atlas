# -*- coding: utf-8 -*-
from pathlib import Path

R=Path(__file__).resolve().parents[1]

ZH='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_model_variables_v88.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_PSTH_model_variables_v88_mobile.png"/><img alt="SLM 内部变量高低条件下的结果对齐与真实行为时长多巴胺 PSTH" loading="lazy" src="assets/SOE_FP_PSTH_model_variables_v88.png"/></picture></a><figcaption><strong>SLM 内部变量对应可见的多巴胺时间结构。</strong>A–B，按每只动物内部的结果前采样策略高低分组，固定结果后时间与真实行为时长两种表示都能看到状态差异。C–D，较大的行动者奖励预测误差（|RPE|）对应更高、更持续的结果后 VTA 多巴胺。E–F，行动者更新幅度得到相似的时间结构。这张图用于显示模型变量对应的神经时间位置；由于分组变量与结果类型本身相关，正式的机制判别仍由整只动物留出预测和固定时间轴模型比较完成。</figcaption></figure>'''
EN='''<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_FP_PSTH_model_variables_v88.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_FP_PSTH_model_variables_v88_mobile.png"/><img alt="Dopamine PSTHs stratified by SLM internal variables" loading="lazy" src="assets/SOE_FP_PSTH_model_variables_v88.png"/></picture></a><figcaption><strong>SLM internal variables occupy visible temporal structure in VTA dopamine.</strong>A–B, within-animal high versus low pre-outcome sampling policy shows state-dependent differences in both fixed-time and actual-bout views. C–D, larger actor |RPE| is associated with a stronger and more sustained post-outcome VTA response. E–F, actor update magnitude shows a similar temporal organization. This visualization localizes model variables in time; because the stratifying variables covary with outcome identity, formal mechanistic adjudication remains the held-animal prediction and fixed temporal-model comparison.</figcaption></figure>'''

for fn,block in [("index-zh.html",ZH),("index.html",EN)]:
    p=R/fn
    s=p.read_text(encoding="utf-8")
    if "SOE_FP_PSTH_model_variables_v88.png" not in s:
        marker='<div class="download-grid"><div class="download-card"><a href="data/SOE_FP_PSTH_ANIMAL_CURVES_v82.csv">'
        if marker not in s:
            raise RuntimeError("download marker missing "+fn)
        s=s.replace(marker,block+"\n"+marker,1)
    # add source-data card once
    if "SOE_FP_PSTH_MODEL_VARIABLES_v88.csv" not in s:
        if fn=="index-zh.html":
            old='<div class="download-card"><a href="data/SOE_FP_PSTH_EVENT_COUNTS_v82.csv">结果事件清单</a><p>全部结果事件与 1,371 个共同事件的数量和真实持续时间。</p></div>'
            new=old+'<div class="download-card"><a href="data/SOE_FP_PSTH_MODEL_VARIABLES_v88.csv">SLM 变量分层 PSTH 源数据</a><p>采样策略、|RPE| 和更新幅度高低条件下的动物级平均时间曲线。</p></div>'
        else:
            old='<div class="download-card"><a href="data/SOE_FP_PSTH_EVENT_COUNTS_v82.csv">PSTH event inventory</a><p>Counts and real durations for all authoritative outcomes and the 1,371 common events.</p></div>'
            new=old+'<div class="download-card"><a href="data/SOE_FP_PSTH_MODEL_VARIABLES_v88.csv">SLM-stratified PSTH source data</a><p>Animal-level curves for high versus low sampling policy, |RPE| and actor update magnitude.</p></div>'
        if old not in s:
            raise RuntimeError("event-count card missing "+fn)
        s=s.replace(old,new,1)
    p.write_text(s,encoding="utf-8")
print("patched v88 model-stratified PSTH into both pages")
