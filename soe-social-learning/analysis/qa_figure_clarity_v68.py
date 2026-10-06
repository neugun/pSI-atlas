from pathlib import Path
from html.parser import HTMLParser
import sys
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
from PIL import Image

R=Path(__file__).resolve().parents[1]
fail=[]
def ck(name,cond,detail=""):
    print(("PASS" if cond else "FAIL"),name,detail)
    if not cond: fail.append(name)

for fn in ["index.html","index-zh.html"]:
    s=(R/fn).read_text(encoding="utf-8")
    HTMLParser().feed(s)
    ck(fn+"_feed_v68", "SOE_feed_content_specificity_v68.png" in s)
    ck(fn+"_feed_v52_retired", "SOE_feed_content_specificity_v52" not in s)
    ck(fn+"_feed_source_link", "SOE_feed_content_specificity_per_animal_v68.csv" in s)
    ck(fn+"_no_bad_nesting", "<p><div" not in s)

s=(R/"index.html").read_text(encoding="utf-8")
ck("en_simple_alt_folded", '<details><summary>Supporting simple alternatives to the multiscale state</summary>' in s)
ck("en_autonomous_folded", '<details><summary>Supporting autonomous lesion summary</summary>' in s)

for ext in [".png",".pdf",".svg","_mobile.png"]:
    p=R/"assets"/f"SOE_feed_content_specificity_v68{ext}"
    ck("asset_"+ext,p.exists(),str(p))

im=Image.open(R/"assets"/"SOE_feed_content_specificity_v68.png")
ck("square_main",im.size[0]==im.size[1],im.size)

M=pd.read_csv(R/"data"/"SLM_native_feed_observed_content_per_animal_v1.csv")
W={m:M[M.model.eq(m)].set_index("animal") for m in ["self_social","plus_recency","plus_observed_content"]}
idx=W["self_social"].index.intersection(W["plus_recency"].index).intersection(W["plus_observed_content"].index)
pA=float(wilcoxon(W["self_social"].loc[idx,"logloss"],W["plus_recency"].loc[idx,"logloss"],method="auto").pvalue)
pB=float(wilcoxon(W["plus_recency"].loc[idx,"logloss"],W["plus_observed_content"].loc[idx,"logloss"],alternative="greater",method="auto").pvalue)
gain=(W["plus_recency"].loc[idx,"brier"]-W["plus_observed_content"].loc[idx,"brier"]).values
pC=float(wilcoxon(gain,alternative="greater",method="auto").pvalue)
ck("A_p",abs(pA-0.6789510101079941)<1e-12,pA)
ck("B_p",abs(pB-0.038612887263298035)<1e-12,pB)
ck("C_p",abs(pC-0.012269832193851471)<1e-12,pC)
ck("C_positive",int((gain>0).sum())==21,int((gain>0).sum()))

D=pd.read_csv(R/"data"/"SOE_feed_content_specificity_per_animal_v68.csv")
expected={
 "feed_after_demfeed":(26,26,0.1599764375901661),
 "feed_after_no_demfeed":(27,0,-0.05044211285810179),
 "nonfeed_after_demfeed":(26,0,-0.018395355294836865),
}
for sub,(n,pos,mean) in expected.items():
    q=D[D.subset.eq(sub)].mean_gain
    ck(sub+"_n",len(q)==n,len(q))
    ck(sub+"_pos",int((q>0).sum())==pos,int((q>0).sum()))
    ck(sub+"_mean",abs(float(q.mean())-mean)<1e-12,float(q.mean()))

print("FAILURES",fail)
sys.exit(1 if fail else 0)
