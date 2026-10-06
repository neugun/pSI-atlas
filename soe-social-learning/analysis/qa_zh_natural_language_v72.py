from pathlib import Path
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import re,collections,sys

R=Path(__file__).resolve().parents[1]
p=R/"index-zh.html"
raw=p.read_text(encoding="utf-8")
fail=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fail.append(name)

HTMLParser().feed(raw)
ck("no_control_chars",not any(ord(ch)<32 and ch not in "\n\r\t" for ch in raw))
for pat in ["不是","而不是","并不是","不只是"]:
    ck("no_"+pat,pat not in raw,raw.count(pat))

s=BeautifulSoup(raw,"html.parser")
ck("lede_exists",s.select_one(".lede") is not None)
ck("glossary_present","主要术语｜" in raw and "社会学习模型（SLM）" in raw and "社会世界模型（SWM）" in raw and "动作预测误差（APE）" in raw and "奖励预测误差（RPE）" in raw)

texts=[]
texts += [s.find("h1").get_text(" ",strip=True),s.select_one(".lede").get_text(" ",strip=True)]
for c in s.select("#overview .hero-grid .card,#overview .cards-4 .card"):
    texts.append(c.get_text(" ",strip=True))
for sid in ["phenotype","information","dynamics","slm","swm","feed","agent","vta","architecture","causality","generalization","crossspecies","resources"]:
    sec=s.find("section",id=sid)
    ck("section_"+sid,sec is not None)
    if not sec: continue
    for sel in [".section-head",".section-significance",".reader-guide"]:
        x=sec.select_one(sel)
        if x:texts.append(x.get_text(" ",strip=True))
    for c in sec.select(".card"):
        if c.find_parent("details") is None:texts.append(c.get_text(" ",strip=True))
    for x in sec.select(".model-contract,.model-family,.callout,.bio-logic"):
        if x.find_parent("details") is None:texts.append(x.get_text(" ",strip=True))
    for f in sec.find_all("figure"):
        if f.find_parent("details") is None:
            fc=f.find("figcaption")
            if fc:texts.append(fc.get_text(" ",strip=True))

visible="\n".join(texts)
whitelist={
"SLM","SWM","APE","RPE","VTA","JAWS","SOE","SRI","SEM","Brier","AUC","NLL","RMSE",
"Q","RW","WSLS","TinyRNN","MLP","LDN","Aeon","Rescorla","Wagner","Noritake","Isoda","A","B","C","D","P","r","V",
"SLM-RPE","Q-RPE"
}
words=re.findall(r"\b[A-Za-z][A-Za-z0-9_+\-]*\b",visible)
unknown=sorted(set(w for w in words if w not in whitelist))
ck("visible_english_only_whitelisted",not unknown,unknown)
ck("no_ai_heading","AI" not in visible)
ck("no_authority_word","Authority" not in visible)

# Core headline should foreground the contribution in natural Chinese.
h1=s.find("h1").get_text(" ",strip=True)
ck("natural_hero","社会学习闭环" in h1 and "小鼠如何决定何时观察同伴" in h1,h1)

# Numeric/statistical evidence remains in bodies/figures, not as big card metrics.
for i,c in enumerate(s.select(".hero-grid .card")):
    m=c.select_one(".metric").get_text(" ",strip=True)
    numeric=bool(re.match(r"^[+−\-]?\.?\d",m)) or "P=" in m or "AUC" in m or "Brier" in m
    ck(f"hero_metric_{i}_semantic",not numeric,m)

print("FAILURES",fail)
sys.exit(1 if fail else 0)
