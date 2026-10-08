# -*- coding: utf-8 -*-
from pathlib import Path
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ck(name,ok):
    print(("PASS " if ok else "FAIL ")+name)
    checks.append(bool(ok))
for fn,lang in [("index.html","en"),("index-zh.html","zh")]:
    s=(ROOT/fn).read_text(encoding="utf-8")
    if lang=="en":
        labels=["Evidence level 1 · strict re-extraction","Evidence level 2 · historical interval source audit","Evidence level 3 · temporal localization"]
        strict="Strict re-extraction replication"
        alt="Historical Post extended-interval analysis |"
        psth="Raw time course |"
        ck("en_not_independent","not an independent estimand" in s)
        ck("en_no_second_replication","Second replication |" not in s)
    else:
        labels=["证据层级 1 · 严格重提取复现","证据层级 2 · 结果期历史窗口对照","证据层级 3 · 时间与机制定位"]
        strict="严格重提取复现｜"
        alt="历史结果期延长区间分析｜"
        psth="原始时间过程｜"
        ck("zh_same_estimand","估计目标本身保持不变" in s)
        ck("zh_no_second_replication","第二层复现｜" not in s)
    for i,x in enumerate(labels,1):
        ck("%s_level%d"%(lang,i),x in s)
    pos=[s.find(x) for x in labels+[strict,alt,psth]]
    ck("%s_hierarchy_order"%lang, all(x>=0 for x in pos) and pos==sorted(pos))
ck("same_1371_en","same 1,371 events" in (ROOT/"index.html").read_text(encoding="utf-8"))
ck("same_1371_zh","同一 1,371 个事件" in (ROOT/"index-zh.html").read_text(encoding="utf-8"))
if not all(checks):
    raise SystemExit(1)
print("TOTAL",len(checks),"PASS")
