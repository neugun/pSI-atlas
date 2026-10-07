# -*- coding: utf-8 -*-
from pathlib import Path
import sys, json
import pandas as pd
R=Path(__file__).resolve().parents[1]
fail=[]
def ck(n,c,d=""):
    print(("PASS" if c else "FAIL"),n,d)
    if not c: fail.append(n)
for fn in ["index-zh.html","index.html"]:
    s=(R/fn).read_text(encoding="utf-8")
    ck(fn+"_new_block",s.count('id="vta-fp-da-method-v77"')==1)
    ck(fn+"_no_wrong_codex",'id="vta-codex-legacy-v75"' not in s)
    ck(fn+"_figure",s.count("SOE_FP_DA_cross_readout_consensus_v78.png")==2)
    ck(fn+"_numbers",all(x in s for x in ["1,371",".733",".800",".164"]))
    ck(fn+"_clean",all(x not in s for x in ["???","�","Ã","â€"]))
M=json.loads((R/"data"/"fp_da_common_event_v1"/"manifest.json").read_text(encoding="utf-8"))
ck("manifest_n",M["actor_common_events"]==1371 and M["passive_common_events"]==1371,M)
S=pd.read_csv(R/"data"/"SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv")
def row(f,c):
    q=S[(S.family==f)&(S.comparison==c)]
    return q.iloc[0] if len(q)==1 else None
x=row("actor","actor_abs_rpe")
ck("actor_both",x is not None and int(x.positive_both)==7 and abs(float(x.direct_delta_p)-.1640625)<1e-9)
x=row("passive_credit","update_selected_vs_w0p75")
ck("credit075",x is not None and int(x.positive_both)==7 and abs(float(x.gain_rho)-.7333333333)<1e-8 and abs(float(x.gain_rho_p)-.0245541501)<1e-8)
x=row("passive_credit","update_selected_vs_w1p0")
ck("credit100",x is not None and int(x.positive_both)==7 and abs(float(x.gain_rho)-.8)<1e-8 and abs(float(x.gain_rho_p)-.0096279247)<1e-8)
A=pd.read_csv(R/"data"/"SLM_multiaxis_mechanistic_support_v75.csv")
ck("legacy_removed",not (A.domain.astype(str)=="legacy_codex").any())
for k in ["Passive_credit_cross_readout_fixed075","Passive_credit_cross_readout_fixed100","Actor_absRPE_positive_both"]:
    ck("authority_"+k,(A.test.astype(str)==k).sum()==1)
for f in ["SOE_FP_DA_cross_readout_consensus_v78.png","SOE_FP_DA_cross_readout_consensus_v78.pdf","SOE_FP_DA_cross_readout_consensus_v78.svg","SOE_FP_DA_cross_readout_consensus_v78_mobile.png"]:
    p=R/"assets"/f; ck("asset_"+f,p.exists() and p.stat().st_size>1000)
D=(R/"docs"/"SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md").read_text(encoding="utf-8")
ck("doc_wrong_section_removed","旧 Codex 3.2/3.3" not in D)
ck("doc_fp_section","Fiber photometry → 多巴胺数值的双定义稳健性" in D)
print("FAILURES",fail)
sys.exit(1 if fail else 0)
