# -*- coding: utf-8 -*-
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
for fn in ["SOE_VTA_READOUT_CONTRACT_v116.json","SOE_VTA_BOUT_DURATION_v118.json"]:
 p=R/"data"/fn
 d=json.loads(p.read_text(encoding="utf-8"))
 d["source_semantics_qc"]="SUPERSEDED: ActionBout is an extended event interval, not a measured observation bout"
 d["superseding_audit"]="SOE_VTA_real_obs_interval_audit_v126.json"
 d["principal_social_credit_mechanism_claim"]="ON_HOLD pending true behavior-event / outcome specific matched tests"
 if fn.endswith("v118.json"):
  d["interpretation"]="28.85s describes extended modeled post-anchor ActionBout interval; true observed ObsBout median is 2.40s. 94.4% >6s applies to modeled interval, NOT a real observation bout."
 else:
  d["interpretation"]="The 1,371 event model comparison remains a historical extended-interval association. It cannot be the primary real behavioral bout social-credit readout. Check v126 821-event triple-window audit."
 p.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
 print("ANNOTATED",fn)
