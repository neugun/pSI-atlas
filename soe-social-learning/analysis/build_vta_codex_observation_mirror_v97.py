# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import spearmanr, wilcoxon

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"
SRC=Path(r"D:\7_Grantwriting\K99\Figures\Manuscript\module25\current\module25_v5_le10s_prec_20260820\learning_models\rl_rebuild_20260915\neural_da\dudman_policy_update_v1\analysis_events_with_policy_latents.csv.gz")
d=pd.read_csv(SRC,low_memory=False)
q=d[np.isfinite(pd.to_numeric(d.DA_ObsBout_AUCperSec,errors="coerce"))].copy()
rows=[]
for an,g in q.groupby("AnmID"):
    g=g[np.isfinite(g.DA_ObsBout_AUCperSec)&np.isfinite(g.direct_action_residual)&np.isfinite(g.actor_p_internal)]
    rows.append(dict(
        AnmID=int(an),SRI=float(g.SRI.iloc[0]),n_events=len(g),
        rho_APE=float(spearmanr(g.DA_ObsBout_AUCperSec,g.direct_action_residual).statistic),
        rho_policy=float(spearmanr(g.DA_ObsBout_AUCperSec,g.actor_p_internal).statistic)))
R=pd.DataFrame(rows)
R.to_csv(OUT/"SOE_VTA_CODEX_OBSERVATION_BOUT_PER_ANIMAL_v97.csv",index=False)

def safe_w(x):
    x=np.asarray(x,float); x=x[np.isfinite(x)]
    return np.nan if len(x)==0 or np.allclose(x,0) else float(wilcoxon(x).pvalue)

tests=[]
# Mirror the exact animal sets used by the current early and middle authorities.
early_ids=[4,5,6,18,27,35]
middle_ids=[1,4,5,6,18,19,27,35]
e=R[R.AnmID.isin(early_ids)].copy()
m=R[R.AnmID.isin(middle_ids)].copy()
tests.append(dict(test="whole_obs_bout_policy",n=len(e),effect=float(np.median(e.rho_policy)),
                  p=safe_w(e.rho_policy),positive=int((e.rho_policy>0).sum()),
                  reference="old early ActorPolicy used a temporally localized early observation window",
                  interpretation="whole-bout averaging does not reproduce the early localized policy signal"))
rho,p=spearmanr(m.SRI,m.rho_APE)
tests.append(dict(test="whole_obs_bout_APE_x_SRI",n=len(m),effect=float(rho),p=float(p),
                  positive=int((m.rho_APE>0).sum()),
                  reference="old middle APE x SRI: rho=0.667, P=0.0416",
                  interpretation="whole-observation-bout averaging does not reproduce the middle localized APE relationship"))
T=pd.DataFrame(tests)
T.to_csv(OUT/"SOE_VTA_CODEX_OBSERVATION_BOUT_MIRROR_v97.csv",index=False)
print(R.to_string(index=False))
print(T.to_string(index=False))
