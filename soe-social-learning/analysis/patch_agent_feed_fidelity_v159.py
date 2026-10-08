from pathlib import Path
R=Path(__file__).resolve().parents[1]
blocks={
'index.html':'''<div class="model-contract" id="slm-feed-fidelity-v159"><strong>Native Feed generation: a missing biological closure.</strong> The prior Codex-trained SLM has autonomous Observe and generated Feed, evaluated on 27 held-out learners/54 sessions. However physical self/social-state covariates remain replayed. In a matched n=24 animal 3-s analysis, actual Feed after actual Observe had a DemFeed−NoDem contrast +0.0385; actual Feed at the GENERATED Observe timings was +0.00045; the model's generated Feed at the same generated opportunities was +0.04275. The generated-versus-real conditional difference is uncertain (two-sided P=.107), so generated positive SOE is not independently validated. <a href="docs/SLM_NATIVE_FEED_SAMPLING_FIDELITY_AUDIT_v159.md">Methods and limits</a> · <a href="data/SLM_agent_source_shift_tests_v159.csv">Window/cooldown tests</a>.</div>''',
'index-zh.html':'''<div class="model-contract" id="slm-feed-fidelity-v159"><strong>人工 SLM 的 Feed 生成，还缺少最后一段关键生物学闭环。</strong> 已找回 Codex 正式训练模型：27 只留出 learner、54 个 session，自主产生 Observe 和 Feed；但动物自身与同伴的连续行为状态仍使用真实录像回放。对 24 只有效配对动物，在观察后的 3 秒内，实际 Feed 在真实 Observe 后的社交内容差异为 +0.0385；在<strong>模型生成的 Observe 时刻</strong>，实际 Feed 的差异仅 +0.00045；模型自己生成的 Feed 差异却达到 +0.04275。模型与真实 Feed 在同一生成机会下的直接差异双侧 P=.107，尚未得到可靠验证。不能把生成 Feed 的阳性直接当成成功重建 SOE。<a href="docs/SLM_NATIVE_FEED_SAMPLING_FIDELITY_AUDIT_v159.md">方法与限制</a> · <a href="data/SLM_agent_source_shift_tests_v159.csv">各时间窗结果</a>。</div>'''
}
for n,b in blocks.items():
 p=R/n;s=p.read_text(encoding="utf8")
 tag='<div class="reader-guide" data-guide="agent">'
 assert tag in s,n
 if 'id="slm-feed-fidelity-v159"' not in s:
  s=s.replace(tag,b+'\n<figure class="figure evidence-figure manuscript-square" id="slm-feed-fidelity-plot-v159"><a class="figure-zoom" href="assets/SLM_agent_generated_feed_fidelity_v159.png" target="_blank" rel="noopener"><img src="assets/SLM_agent_generated_feed_fidelity_v159.png" loading="lazy" alt="Real versus generated Observe-to-Feed risk comparison"/></a><figcaption>Matched real and generated social feeding hazards: 27 held-out learners overall; 24 informative animals for 3 s. Error bars show between-animal SEM. The figure identifies a model validation gap, not a negative result about biological SOE.</figcaption></figure>\n'+tag,1)
  p.write_text(s,encoding="utf8")
 print("AGENT",n)
