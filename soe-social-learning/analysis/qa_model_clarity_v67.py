from pathlib import Path
from html.parser import HTMLParser
import re, sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

R=Path(__file__).resolve().parents[1]
fail=[]

def ck(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        fail.append(name)

for fn in ["index.html","index-zh.html"]:
    s=(R/fn).read_text(encoding="utf-8")
    HTMLParser().feed(s)
    zh=fn.endswith("zh.html")
    ck(fn+"_single_model_map", s.count('<div class="model-map">')==1, s.count('<div class="model-map">'))
    ck(fn+"_five_model_families", s.count('<div class="model-family">')==5, s.count('<div class="model-family">'))
    ck(fn+"_old_framework_removed", 'model-framework-v66' not in s and '<div class="model-framework"' not in s)
    ck(fn+"_three_column_model_map", 'grid-template-columns:repeat(3,minmax(0,1fr))' in s)
    ck(fn+"_ape_exact", 'actual sampling action − pre-action policy probability' in s)
    ck(fn+"_contract_27", '27 held' in s and 'Brier' in s and 'AUC' in s)
    ck(fn+"_registry_link", 'SOE_MODEL_CONTRACT_REGISTRY_v1.csv' in s)
    ck(fn+"_slm_v67", 'SOE_SLM_default_hierarchy_v67.png' in s and 'SOE_SLM_default_hierarchy_v64.png' not in s)
    ck(fn+"_vta_v67", 'SOE_DA_temporal_logic_v67.png' in s and 'SOE_DA_temporal_logic_v65.png' not in s)
    ck(fn+"_swm_contract", ('Why SWM is not another row' in s) if not zh else ('为什么 SWM 不直接作为同一个 model zoo' in s))
    ck(fn+"_no_p_div", '<p><div' not in s)
    ck(fn+"_behavior_zoo_table", ('Full behavioral model zoo' in s) if not zh else ('完整 behavioral model zoo' in s))
    ck(fn+"_vta_zoo_table", ('Full VTA signal zoo' in s) if not zh else ('完整 VTA signal zoo' in s))
    ck(fn+"_build_date", '2026-10-06' in s)

for stem in ["SOE_SLM_default_hierarchy_v67","SOE_DA_temporal_logic_v67"]:
    for ext in [".png",".pdf",".svg","_mobile.png"]:
        ck(stem+ext+"_exists", (R/"assets"/f"{stem}{ext}").exists())

for name in ["SOE_MODEL_CONTRACT_REGISTRY_v1.csv","SLM_choicekernel_stack_per_animal_v1.csv",
             "VTA_early_model_per_animal_v67.csv","VTA_middle_APE_per_animal_v67.csv",
             "VTA_post_model_per_animal_v67.csv"]:
    ck(name+"_exists",(R/"data"/name).exists())

reg=pd.read_csv(R/"data"/"SOE_MODEL_CONTRACT_REGISTRY_v1.csv")
ck("registry_six_rows",len(reg)==6,len(reg))
ck("registry_has_signals",(reg["family"]=="Computational readouts").any())

d=pd.read_csv(R/"data"/"SLM_choicekernel_stack_per_animal_v1.csv")
mods=["SLM full","Current + Choice-kernel","SLM + Choice-kernel stack"]
counts=[d[d.model.eq(m)].animal.nunique() for m in mods]
ck("slm_plot_n27",counts==[27,27,27],counts)

p=pd.read_csv(R/"data"/"VTA_post_model_per_animal_v67.csv")
w=p.pivot(index="animal",columns="model",values="mse").dropna(subset=["base","actorRPE","qAllRPE","beliefSurprise"])
ck("vta_post_n9",len(w)==9,len(w))
expected={"actorRPE":0.01953125,"qAllRPE":0.01953125,"beliefSurprise":0.005859375}
for m,ep in expected.items():
    g=100*(w["base"]-w[m])/w["base"]
    pv=float(wilcoxon(g,alternative="greater",method="auto").pvalue)
    ck("vta_post_p_"+m,abs(pv-ep)<1e-12,pv)

da=pd.read_csv(R/"data"/"DA_global_temporal_model_adjudication_v4_authority.csv")
slm=da[da.model_family.eq("SLM")].iloc[0]
q=da[da.model_family.eq("Q-all")].iloc[0]
ck("temporal_slm_3of3",int(slm.positive_sig_axes)==3,int(slm.positive_sig_axes))
ck("temporal_q_post_only",int(q.positive_sig_axes)==1,int(q.positive_sig_axes))

print("FAILURES",fail)
sys.exit(1 if fail else 0)
