# -*- coding: utf-8 -*-
from pathlib import Path
import re,sys
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
fail=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fail.append(name)

d=pd.read_csv(str(ROOT/"data"/"DA_global_temporal_model_adjudication_v4_authority.csv")).set_index("model_family")
positive={"SLM":3,"Choice kernel":0,"TinyRNN":0,"History MLP":0,"Q-all":1,"Q + choice kernel":0}
wrong={"SLM":0,"Choice kernel":0,"TinyRNN":1,"History MLP":1,"Q-all":0,"Q + choice kernel":0}
for fam,n in positive.items(): ck("positive_sig_"+fam,int(d.loc[fam,"positive_sig_axes"])==n,int(d.loc[fam,"positive_sig_axes"]))
for fam,n in wrong.items(): ck("wrong_direction_"+fam,int(d.loc[fam,"wrong_direction_sig_axes"])==n,int(d.loc[fam,"wrong_direction_sig_axes"]))

en=(ROOT/"index.html").read_text(encoding="utf-8")
zh=(ROOT/"index-zh.html").read_text(encoding="utf-8")
ck("en_two_opposite",en.count("<strong>(opposite)</strong>")==2,en.count("<strong>(opposite)</strong>"))
ck("zh_two_opposite",zh.count("<strong>（反向）</strong>")==2,zh.count("<strong>（反向）</strong>"))
ck("en_tinyrnn_opposite",'TinyRNN</td><td>−0.867 · P=.0195 <strong>(opposite)</strong>' in en)
ck("en_mlp_opposite",'−0.911 · P=.0117 <strong>(opposite)</strong>' in en)
ck("zh_tinyrnn_opposite",'TinyRNN</td><td>−0.867 · P=.0195 <strong>（反向）</strong>' in zh)
ck("zh_mlp_opposite",'−0.911 · P=.0117 <strong>（反向）</strong>' in zh)
ck("en_p_contract","P-value convention." in en and "Positive &amp; significant" in en and "authority P &lt; .05" in en)
ck("zh_p_contract","P 值约定｜" in zh and "正向且显著" in zh and "authority P &lt; .05" in zh)
ck("en_directional_slm","SLM Early uses the pre-specified directional test" in en)
ck("zh_directional_slm","SLM 早期使用预设方向检验" in zh)
rows={"SLM":"3/3","Choice kernel":"0/3","TinyRNN":"0/3","History MLP":"0/3","Q-all":"1/3","Q + choice kernel":"0/3"}
for fam,count in rows.items():
    pattern=r"<tr><td>"+re.escape(fam)+r"</td>.*?<td>"+re.escape(count)+r"</td></tr>"
    ck("page_count_"+fam,re.search(pattern,en,re.S) is not None,count)
print("FAILURES",fail)
sys.exit(1 if fail else 0)
