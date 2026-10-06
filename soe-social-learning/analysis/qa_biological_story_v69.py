from pathlib import Path
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import re,sys

R=Path(__file__).resolve().parents[1]
ids=["phenotype","information","dynamics","slm","swm","feed","agent","vta","architecture","causality","generalization","crossspecies","resources"]
fail=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fail.append(name)

for fn in ["index.html","index-zh.html"]:
    raw=(R/fn).read_text(encoding="utf-8")
    HTMLParser().feed(raw)
    s=BeautifulSoup(raw,"html.parser")
    ck(fn+"_meaning_style",raw.count('id="section-meaning-v69"')==1,raw.count('id="section-meaning-v69"'))
    ck(fn+"_hero_contribution",len(s.select('#overview .section-significance'))==1,len(s.select('#overview .section-significance')))
    h1=s.find("h1").get_text(" ",strip=True)
    ck(fn+"_hero_not_metric",not re.match(r'^[+−\-]?[\d.]+',h1),h1)
    for sid in ids:
        sec=s.find("section",id=sid)
        ck(fn+"_"+sid+"_exists",sec is not None)
        if sec is None: continue
        h=sec.find("h2")
        sig=sec.select(".section-significance")
        ck(fn+"_"+sid+"_claim_heading",h is not None and len(h.get_text(" ",strip=True))>20,h.get_text(" ",strip=True) if h else "")
        ck(fn+"_"+sid+"_one_significance",len(sig)==1,len(sig))
        # visible, non-details metric cards should now use semantic phrases rather than naked statistics
        for i,c in enumerate(sec.select(".card")):
            if c.find_parent("details") is not None: continue
            m=c.select_one(".metric")
            if not m: continue
            t=m.get_text(" ",strip=True)
            numeric=bool(re.match(r'^[+−\-]?(?:\d|\.\d)',t)) or ("P=" in t) or ("Brier ." in t) or ("ρ=" in t) or ("r=" in t)
            ck(f"{fn}_{sid}_card{i}_semantic_metric",not numeric,t)
    atlas=s.select("#overview .series-index + h3")
    ck(fn+"_12_contribution_titles",len(atlas)==12,len(atlas))
    ck(fn+"_atlas_titles_sentence_like",all(len(x.get_text(" ",strip=True))>8 for x in atlas),[x.get_text(" ",strip=True) for x in atlas])
    ck(fn+"_no_bad_nesting","<p><div" not in raw)

print("FAILURES",fail)
sys.exit(1 if fail else 0)
