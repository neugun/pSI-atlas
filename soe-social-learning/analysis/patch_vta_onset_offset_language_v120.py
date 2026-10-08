# -*- coding: utf-8 -*-
"""Resolve all v113/v82 legacy wording that confused onset-locked with offset-locked DA."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EDITS={
"index.html":[
("real-bout AUC/s isolates the actual action/outcome episode, whereas fixed 0–6 s also includes later evaluation",
 "real-bout AUC/s averages the complete action bout, whereas fixed 0–6 s usually samples its early portion (94.4% of bouts exceed 6 s)"),
("stronger in the broader fixed window","stronger in the shorter fixed 0–6 s window"),
("Updating extends after action","Earlier versus full-bout integration"),
("RPE-family effects keep the same direction in the real action bout but are usually stronger in the fixed 0–6 s window, consistent with post-action evaluation and teaching.",
 "RPE-family evidence is generally stronger in the first six seconds. This does not establish activity after the action ended; the full-bout readout includes a much longer duration."),
("Active is faster, Passive is more sustained, and Unrewarded becomes negative; post-action activity boosts the fixed-window update signal.",
 "Active, Passive and Unrewarded have different time courses; the first-6-s signal may weight these responses differently from a full-bout average. An offset-locked analysis is still needed."),
("Real-bout DA emphasizes execution; fixed post-outcome DA also retains evaluation and updating after the behavior ends. This explains why the direction is shared while RPE sensitivity differs.",
 "Real action-bout DA averages the ongoing action, whereas fixed 0–6 s predominantly samples its beginning. Their different RPE sensitivity cannot on its own identify evaluation after the action ends.")
],
"index-zh.html":[
("在较宽的固定窗口中更敏感","在较短的固定 0–6 秒窗口中更敏感"),
("在较宽的固定窗口中通常更强","在较短的固定 0–6 秒窗口中通常更强"),
("结果后持续更新</div><p>RPE 家族在真实行动片段中方向仍保留，但固定 0–6 秒通常更强，提示结果评估和教学更新可延续到动作结束之后。",
 "早期与整段行动的窗口差异</div><p>RPE 家族在真实行动片段中方向仍保留，但固定前 6 秒更敏感。绝大多数行动仍未结束，因而这一对比尚不能证明行动结束后的评价或教学更新。"),
("结果后持续部分使固定窗口对更新信号更敏感。",
 "两种窗口对不同时程的结果反应赋予不同权重，结束时刻后的独立信号仍需另外检验。"),
("原始时间过程解释了为什么固定结果后窗口对部分 RPE/更新 项更敏感。",
 "原始时间过程显示不同时段的信号异质性，但尚不能直接定位行动结束后的评价。"),
("真实行动时长主要读取行为执行阶段；固定结果后窗口还保留动作结束后的评估和更新。因此两种方法的方向一致，同时对 RPE 的灵敏度不同，这个差异有明确的时间结构来源。",
 "真实行动片段平均整个行动过程；固定前 6 秒主要读取行动早期。两种读出的模型灵敏度不同，但独立的行动结束后评价仍待以真实结束时刻重新对齐检验。")
]}
for name,edits in EDITS.items():
 p=ROOT/name;s=p.read_text(encoding="utf-8")
 for old,new in edits:
  n=s.count(old)
  if n==0 and new not in s:raise RuntimeError(f"Missing {name} pattern {len(old)}")
  s=s.replace(old,new)
  print("OK",name,n,len(old))
 p.write_text(s,encoding="utf-8")
