from pathlib import Path
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
for fn in ["index.html","index-zh.html"]:
 s=(R/fn).read_text(encoding="utf-8");HTMLParser().feed(s)
 print(fn,"map",s.count('id="model-framework"'),"css",s.count('id="model-framework-v66"'),"swm",s.count("SWM"),"policy",s.count("policy"),"RPE",s.count("RPE"))
 if fn=="index.html":
  assert "Model map: four different questions" in s and "Why the model set changes here" in s and "Why SWM is not another row" in s
 else:
  assert "模型地图：四类问题" in s and "为什么这里的 model set 会改变" in s and "为什么 SWM 不直接作为同一个 model zoo" in s
  for t in ["不是","而不是","不只是","而非","并非"]: assert t not in s,t
 assert s.count('id="model-framework"')==1
print("PASS")
