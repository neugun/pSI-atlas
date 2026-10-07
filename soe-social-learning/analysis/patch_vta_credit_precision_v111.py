# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def replace_once(path,old,new):
    p=ROOT/path
    s=p.read_text(encoding="utf-8")
    if new in s:
        print(path,"already current"); return
    if old not in s:
        raise RuntimeError("missing anchor in %s: %s"%(path,old[:100]))
    p.write_text(s.replace(old,new,1),encoding="utf-8")
    print(path,"updated")

replace_once("analysis/build_vta_codex_replication_v96.py",
'["social_credit","replicated","behavior-selected passive credit beats fixed 0.75/1.0 under both readouts"],',
'["social_credit","readout-robust with boundary","vs fixed 0.75: fixed 0-6 s 7/9 P=.0391, real bout 9/9 P=.0039; vs fixed 1.0: fixed 0-6 s 6/9 P=.0547 (borderline), real bout 9/9 P=.0039"],')

replace_once("data/SOE_VTA_CODEX_REPLICATION_SUMMARY_v96.csv",
"social_credit,replicated,behavior-selected passive credit beats fixed 0.75/1.0 under both readouts",
'social_credit,readout-robust with boundary,"vs fixed 0.75: fixed 0-6 s 7/9 P=.0391, real bout 9/9 P=.0039; vs fixed 1.0: fixed 0-6 s 6/9 P=.0547 (borderline), real bout 9/9 P=.0039"')

replace_once("index.html",
'<div class="card good"><div class="metric-label">Strongest cross-method replication</div><div class="metric">Social credit transfers to VTA</div><p>Passive credit selected entirely from behavior outperforms fixed credit under both DA definitions, with no neural retuning.</p></div>',
'<div class="card good"><div class="metric-label">Behavior-to-neural transfer</div><div class="metric">Social credit is readout-robust</div><p>Passive credit selected entirely from behavior requires no neural retuning. Versus fixed 0.75 it is significant in both readouts; versus 1.0 it is positive but borderline in fixed 0–6 s (6/9, P=.0547) and 9/9 in real-bout DA (P=.0039).</p></div>')

replace_once("index-zh.html",
'<div class="card good"><div class="metric-label">最强的跨方法复现</div><div class="metric">社会归因直接迁移到 VTA</div><p>行为数据独立选出的被动结果归因，在固定结果后窗口和真实行动时长中都优于固定归因权重。同一规则无需用神经数据重新调参。</p></div>',
'<div class="card good"><div class="metric-label">行为参数→神经信号迁移</div><div class="metric">社会归因跨读出保持方向</div><p>行为数据独立选出的被动结果归因无需用神经数据重新调参。相对 0.75，两种读出均显著；相对 1.0，固定 0–6 秒为 6/9、P=.0547，真实行动片段为 9/9、P=.0039。</p></div>')

# The detailed reader-guide and figure-caption precision edits are also required.
for fn,checks in {
"index.html":[
("beats fixed weights under both readouts","behavior-selected Passive credit versus fixed 0.75 is positive in 7/9 animals for fixed 0–6 s"),
("outperforms fixed credit under both DA definitions","versus 1.0 the fixed-window result is borderline while real-bout DA is significant")],
"index-zh.html":[
("在两种读出中都优于固定权重","相对 0.75 在固定窗口为 7/9（P=.0391）"),
("在固定结果后窗口和真实行动时长中都优于固定归因权重","相对 1.0，固定 0–6 秒为边缘结果")]
}.items():
    s=(ROOT/fn).read_text(encoding="utf-8")
    for old,new_marker in checks:
        if old in s:
            raise RuntimeError("%s still contains overclaim: %s"%(fn,old))
        if new_marker not in s:
            raise RuntimeError("%s missing precision marker: %s"%(fn,new_marker))
print("credit precision patch complete")
