# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import pandas as pd
if hasattr(sys.stdout, "reconfigure"):
 sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT=Path(__file__).resolve().parents[1]
fail=[]
def ck(name,cond,detail=""):
 print(("PASS" if cond else "FAIL"),name,detail)
 if not cond: fail.append(name)
d=pd.read_csv(str(ROOT/"data"/"DA_global_temporal_model_adjudication_v4_authority.csv"))
s=d[d.model_family.eq("SLM")].iloc[0]
ck("authority_early",abs(float(s.early_effect)-0.8095238095238095)<1e-12,s.early_effect)
ck("authority_middle",abs(float(s.middle_effect)-2.0/3.0)<1e-12,s.middle_effect)
ck("authority_post",abs(float(s.post_effect)-0.8666666666666667)<1e-12,s.post_effect)
en=(ROOT/"index.html").read_text(encoding="utf-8")
zh=(ROOT/"index-zh.html").read_text(encoding="utf-8")
ck("en_early_metric","rank-biserial=.810, P=.0469" in en)
ck("en_middle_metric","Spearman ρ=.667 vs SRI; exact one-sided permutation P=.0416" in en)
ck("en_post_metric_frozen",'<tr><td>SLM</td><td>+0.810 · P=.0469</td><td>+0.667 · P=.0416</td><td>+0.867 · P=.0195</td><td>3/3</td></tr>' in en)
ck("en_scale_note","Effect scales are axis-specific:" in en and "not directly comparable across columns" in en)
ck("en_no_generic_early","sampling policy (effect=.810" not in en)
ck("en_no_generic_middle","Middle APE remains related to learning (effect=.667" not in en)
ck("en_no_generic_post","RPE is supported (effect=.867" not in en)
ck("zh_early_metric","秩双列相关=.810，P=.0469" in zh)
ck("zh_middle_metric","Spearman ρ=.667" in zh and "P=.0416" in zh)
ck("zh_post_metric_frozen",'<tr><td>SLM</td><td>+0.810 · P=.0469</td><td>+0.667 · P=.0416</td><td>+0.867 · P=.0195</td><td>3/3</td></tr>' in zh)
ck("zh_scale_note","三列效应量使用不同统计尺度" in zh and "数值大小不做跨列比较" in zh)
ck("zh_no_generic_early","效应=.810，P=.0469" not in zh)
ck("zh_no_generic_middle","效应=.667，P=.0416" not in zh)
ck("zh_no_generic_post","效应=.867，P=.0195" not in zh)
print("FAILURES",fail)
sys.exit(1 if fail else 0)
