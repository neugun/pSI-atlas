from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def bounds(s,sid):
    k=s.find(f'id="{sid}"')
    if k<0: raise RuntimeError(sid)
    a=s.rfind("<section",0,k)
    b=s.find("<section",k+1)
    if b<0: b=s.find("</main>",k)
    return a,b

def insert_after_marker(s,sid,marker,block,block_id):
    if f'id="{block_id}"' in s:
        return s
    a,b=bounds(s,sid)
    sec=s[a:b]
    k=sec.find(marker)
    if k<0: raise RuntimeError(f"marker not found {sid}")
    # locate closing div of the identified id block by using next figure as stable boundary.
    fig=sec.find("<figure",k)
    if fig<0: raise RuntimeError("figure missing")
    sec=sec[:fig]+block+"\n"+sec[fig:]
    return s[:a]+sec+s[b:]

zh='''<details id="vta-codex-legacy-v75"><summary>展开：Codex 3.2/3.3 的两条多巴胺计算路线</summary><div class="detail-body">
<div class="bio-logic"><strong>路线一｜状态条件化的价值与 RPE。</strong>旧 Codex v24Aligned 使用跨动物留出回归比较当前状态、价值和 RPE。状态单独 R²=.131（跨动物 .029）；状态+RPE 提高到 .185（.071）；状态+价值+RPE 为 .195（.093）；完整强化学习为 .196（.092）。RPE 单独只有 .014，跨动物为 −.293。这个旧结果说明多巴胺需要结合当前状态和更新误差来理解，RPE 单独不足以概括完整信号。</div>
<div class="bio-logic"><strong>路线二｜同一天快速更新 + 跨天慢先验。</strong>旧 Codex 还把行为状态拆成 day_prior_qdiff、fast_qdiff_pre、slow_qdiff_pre、fast_rpe 和 slow_rpe。同一天快速 Q 在 Day 1 改善 33/39 动物（P≈3.1×10⁻⁶），Days 2–14 再加入跨天起始先验仍有增益（P≈.004）。在这一路线里，观察期多巴胺对应结果前的策略/价值/信念，结果期多巴胺对应当前事件的 RPE、意外度和策略更新。</div>
<div class="callout"><strong>与当前主分析的关系｜</strong>这两条旧路线现在作为独立历史审计保留。当前页面的主统计使用更严格的整只动物留出和固定时间轴：结果前策略 → 中段 APE → 结果后 RPE/社会归因。旧结果提供了额外的一致性：状态表示、快慢记忆和结果更新都对解释多巴胺有贡献。</div>
</div></details>'''
en='''<details id="vta-codex-legacy-v75"><summary>Expand: the two legacy Codex 3.2/3.3 dopamine computation routes</summary><div class="detail-body">
<div class="bio-logic"><strong>Route 1 · State-conditioned value and RPE.</strong> The legacy Codex v24Aligned audit compared current state, value and RPE with animal holdout. State alone reached R²=.131 (animal-holdout .029); State+RPE reached .185 (.071); State+Value+RPE reached .195 (.093); Full RL reached .196 (.092). RPE-only reached .014 and failed animal holdout (−.293). The result independently argues that dopamine is better understood as state-conditioned updating than as RPE alone.</div>
<div class="bio-logic"><strong>Route 2 · Fast within-day updating plus a slow cross-day prior.</strong> The legacy decomposition exposed day_prior_qdiff, fast_qdiff_pre, slow_qdiff_pre, fast_rpe and slow_rpe. Fast Q improved Day-1 behavior in 33/39 animals (P≈3.1×10⁻⁶), and adding a day-start prior on Days 2–14 provided additional benefit (P≈.004). In that analysis, view-period dopamine maps to pre-outcome policy/value/belief, whereas outcome-period dopamine maps to current-trial RPE, surprise and updating.</div>
<div class="callout"><strong>Relationship to the current primary analysis.</strong> These legacy routes are retained as an independent historical audit. The primary page uses stricter held-animal temporal adjudication: pre-outcome policy → middle APE → post-outcome RPE/social credit. The older analyses add convergent support for state representation, multiscale memory and outcome updating.</div>
</div></details>'''

for fn,block in [("index-zh.html",zh),("index.html",en)]:
    p=ROOT/fn
    s=p.read_text(encoding="utf-8")
    s=insert_after_marker(s,"vta",'id="vta-multiaxis-v75"',block,"vta-codex-legacy-v75")
    p.write_text(s,encoding="utf-8")
print("added legacy Codex dopamine audit")
