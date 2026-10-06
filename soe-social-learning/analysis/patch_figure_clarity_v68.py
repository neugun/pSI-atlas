from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
en=ROOT/"index.html"
zh=ROOT/"index-zh.html"

def patch_en(s):
    # Feed specificity: replace legacy summary-bar figure with animal-level V68.
    s=s.replace("SOE_feed_content_specificity_v52","SOE_feed_content_specificity_v68")
    old='<figcaption><strong>What was observed matters.</strong> On Feed decisions following demonstrator feeding, the dem-feed content term improves held-out log probability in 26/26 informative animals; near-spout content alone does not reproduce this effect.</figcaption>'
    new='<figcaption><strong>Observed content adds information beyond recency, and the effect is content-specific.</strong> A, simply adding recent-Observe recency to the current-state model does not improve held-animal log loss (n=27, P=.679). B, adding what was observed improves log loss (P=.0386). C, the same observed-content model improves Brier score in 21/27 animals (P=.0123). D, trial-level OOF predictions are aggregated within animal: the dem-feed term increases log probability for Feed after demonstrator feeding in 26/26 animals, but decreases log probability for Feed after no demonstrator feeding and for No-Feed after demonstrator feeding. Points are animals; large symbols are mean ± SEM.</figcaption>'
    s=s.replace(old,new)
    # Add feed source download next to session progression.
    needle='<div class="download-grid"><div class="download-card"><a href="data/SLM_native_feed_demfeed_session_progression_v2.csv">Feed session-progression sensitivity</a><p class="small">Paired first→second analyzed-session raw and state-residualized dem-feed hazard contrasts.</p></div></div>'
    repl='<div class="download-grid"><div class="download-card"><a href="data/SLM_native_feed_demfeed_session_progression_v2.csv">Feed session-progression sensitivity</a><p class="small">Paired first→second analyzed-session raw and state-residualized dem-feed hazard contrasts.</p></div><div class="download-card"><a href="data/SOE_feed_content_specificity_per_animal_v68.csv">Observed-content specificity, animal level</a><p class="small">Animal-level log-probability gains for Feed|Dem+, Feed|Dem− and No-Feed|Dem+.</p></div></div>'
    s=s.replace(needle,repl)

    # Keep the older scalar/uncertainty summary available, but move it out of the main narrative.
    pat=r'(<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_simple_alternatives_multiscale_v52\.png".*?</figure>)'
    m=re.search(pat,s,flags=re.S)
    if m and '<details><summary>Supporting simple alternatives' not in s:
        block=m.group(1)
        wrapped='<details><summary>Supporting simple alternatives to the multiscale state</summary><div class="detail-body">'+block+'</div></details>'
        s=s[:m.start()]+wrapped+s[m.end():]

    # The six-panel autonomous lesion summary is useful provenance but redundant with the cleaner VB/JAWS animal-level panels.
    pat=r'(<figure class="figure manuscript-square"><a class="figure-zoom" href="assets/SOE_AutonomousSLM_CausalLesions_v52\.png".*?</figure>)'
    m=re.search(pat,s,flags=re.S)
    if m and '<details><summary>Supporting autonomous lesion summary' not in s:
        block=m.group(1)
        wrapped='<details><summary>Supporting autonomous lesion summary</summary><div class="detail-body">'+block+'</div></details>'
        s=s[:m.start()]+wrapped+s[m.end():]
    return s

def patch_zh(s):
    # Chinese page did not previously expose the content-specificity panel; add the same animal-level evidence.
    if "SOE_feed_content_specificity_v68.png" not in s:
        marker='<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_feed_conversion_learning_v64.png"'
        start=s.find(marker)
        if start<0:
            raise RuntimeError("Chinese feed conversion figure not found")
        end=s.find('</figure>',start)
        if end<0:
            raise RuntimeError("Chinese feed conversion figure end not found")
        end+=len('</figure>')
        block='''\n<figure class="figure evidence-figure manuscript-square"><a class="figure-zoom" href="assets/SOE_feed_content_specificity_v68.png" rel="noopener" target="_blank"><picture><source media="(max-width:620px)" srcset="assets/SOE_feed_content_specificity_v68_mobile.png"/><img alt="observed-content 对自身 Feed 的逐动物特异性" loading="lazy" src="assets/SOE_feed_content_specificity_v68.png"/></picture></a><figcaption><strong>看到什么，比“最近看过”更重要。</strong>A，只加入 recent-Observe recency 并不能提高 held-animal log loss（n=27，P=.679）。B，加入 sampled content 后 log loss 改善（P=.0386）。C，同一个 observed-content model 的 Brier score 在 21/27 动物改善（P=.0123）。D，把 trial-level OOF prediction 聚合到每只动物：dem-feed term 在 26/26 动物中提高 Feed|Dem+ 的 log probability，同时降低 Feed|Dem− 与 No-Feed|Dem+ 的 log probability。灰点为动物，大点为 mean ± SEM。</figcaption></figure>'''
        s=s[:end]+block+s[end:]
    needle='<div class="download-grid"><div class="download-card"><a href="data/SLM_native_feed_demfeed_session_progression_v2.csv">Feed session progression</a><p>第一→第二 analyzed session 的 raw / state-residualized dem-feed hazard sensitivity。</p></div></div>'
    repl='<div class="download-grid"><div class="download-card"><a href="data/SLM_native_feed_demfeed_session_progression_v2.csv">Feed session progression</a><p>第一→第二 analyzed session 的 raw / state-residualized dem-feed hazard sensitivity。</p></div><div class="download-card"><a href="data/SOE_feed_content_specificity_per_animal_v68.csv">Observed-content specificity</a><p>Feed|Dem+、Feed|Dem−、No-Feed|Dem+ 的逐动物 log-probability gain。</p></div></div>'
    s=s.replace(needle,repl)
    return s

for path,fn in [(en,patch_en),(zh,patch_zh)]:
    s=path.read_text(encoding="utf-8")
    out=fn(s)
    if out==s:
        raise RuntimeError(f"No changes applied: {path.name}")
    path.write_text(out,encoding="utf-8")
    print(path.name, len(s), "->", len(out))
