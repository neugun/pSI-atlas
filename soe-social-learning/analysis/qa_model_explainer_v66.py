from pathlib import Path
from html.parser import HTMLParser
import sys,re
R=Path(__file__).resolve().parents[1];fail=[]
def ck(n,c):
 print(("PASS" if c else "FAIL"),n)
 if not c:fail.append(n)
for fn in ["index.html","index-zh.html"]:
 s=(R/fn).read_text(encoding="utf-8");HTMLParser().feed(s)
 ck(fn+"_one_explainer",s.count('id="model-explainer-v66"')==1)
 ck(fn+"_families",all(x in s for x in ["RW","forgetting-Q","SLM core","Full-history MLP","TinyRNN","SWM"]))
 ck(fn+"_terms",all(x in s for x in ["Policy","APE","RPE","Social credit"]))
 ck(fn+"_contract","contract" in s and "held-animal" in s)
 if fn.endswith("zh.html"):
  ck(fn+"_chinese","同一个 model zoo" in s and "后文统一术语" in s)
  ck(fn+"_banned",all(x not in s for x in ["不是","而不是","不只是","而非","并非"]))
print("FAIL",fail);sys.exit(bool(fail))
