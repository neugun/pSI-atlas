# -*- coding: utf-8 -*-
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPL={
"index.html":[
('<tr><td>TinyRNN</td><td>−0.867 · P=.0195</td><td>−0.548 · P=.924</td><td>+0.733 · P=.0547</td><td>0/3</td></tr>','<tr><td>TinyRNN</td><td>−0.867 · P=.0195 <strong>(opposite)</strong></td><td>−0.548 · P=.924</td><td>+0.733 · P=.0547</td><td>0/3</td></tr>'),
('<tr><td>History MLP</td><td>−0.378 · P=.359</td><td>+0.024 · P=.488</td><td>−0.911 · P=.0117</td><td>0/3</td></tr>','<tr><td>History MLP</td><td>−0.378 · P=.359</td><td>+0.024 · P=.488</td><td>−0.911 · P=.0117 <strong>(opposite)</strong></td><td>0/3</td></tr>'),
('<p class="small"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">Frozen temporal authority CSV</a>. TinyRNN and History MLP are flexible capacity comparators; Q-all and choice-kernel rows test classical value/persistence alternatives.</p>','<p class="small"><strong>P-value convention.</strong> Each cell preserves its frozen axis-specific inferential contract; P magnitudes should not be read as one omnibus leaderboard. SLM Early uses the pre-specified directional test, while alternative and flexible comparators retain their frozen source conventions. <strong>Positive &amp; significant</strong> requires effect &gt; 0 and authority P &lt; .05; significant negative cells are marked <strong>opposite</strong>.</p><p class="small"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">Frozen temporal authority CSV</a>. TinyRNN and History MLP are flexible capacity comparators; Q-all and choice-kernel rows test classical value/persistence alternatives.</p>')
],
"index-zh.html":[
('<tr><td>TinyRNN</td><td>−0.867 · P=.0195</td><td>−0.548 · P=.924</td><td>+0.733 · P=.0547</td><td>0/3</td></tr>','<tr><td>TinyRNN</td><td>−0.867 · P=.0195 <strong>（反向）</strong></td><td>−0.548 · P=.924</td><td>+0.733 · P=.0547</td><td>0/3</td></tr>'),
('<tr><td>History MLP</td><td>−0.378 · P=.359</td><td>+0.024 · P=.488</td><td>−0.911 · P=.0117</td><td>0/3</td></tr>','<tr><td>History MLP</td><td>−0.378 · P=.359</td><td>+0.024 · P=.488</td><td>−0.911 · P=.0117 <strong>（反向）</strong></td><td>0/3</td></tr>'),
('<p class="small"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">冻结时间轴数据表</a>。TinyRNN 与 History MLP 提供灵活容量对照；Q-all 与选择惯性检验经典价值和持续性解释。</p>','<p class="small"><strong>P 值约定｜</strong>本表沿用各时间轴冻结的统计合同，不把不同检验的 P 值当作统一排行榜。SLM 早期使用预设方向检验；经典替代模型和灵活模型沿用各自冻结的比较约定。<strong>正向且显著</strong>仅计 effect &gt; 0 且 authority P &lt; .05；显著负向单元格标记为<strong>反向</strong>。</p><p class="small"><a href="data/DA_global_temporal_model_adjudication_v4_authority.csv">冻结时间轴数据表</a>。TinyRNN 与 History MLP 提供灵活容量对照；Q-all 与选择惯性检验经典价值和持续性解释。</p>')
]
}
for fn,pairs in REPL.items():
    p=ROOT/fn
    s=p.read_text(encoding="utf-8")
    changed=0
    for old,new in pairs:
        if new in s: continue
        if old not in s: raise RuntimeError("missing patch anchor in %s: %s"%(fn,old[:80]))
        s=s.replace(old,new,1); changed+=1
    p.write_text(s,encoding="utf-8")
    print(fn,"changed",changed)
