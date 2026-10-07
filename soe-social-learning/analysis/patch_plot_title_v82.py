# -*- coding: utf-8 -*-
from pathlib import Path
p=Path(__file__).resolve().parent/"plot_fp_psth_biology_v82.py"
s=p.read_text(encoding="utf-8")
old='finish_time(ax,"Prior outcome → next observe")'
new='finish_time(ax,"Next-observe state")'
if old not in s:
    raise RuntimeError("target title not found")
p.write_text(s.replace(old,new,1),encoding="utf-8")
print("patched safely")
