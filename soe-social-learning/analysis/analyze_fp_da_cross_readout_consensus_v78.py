from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, wilcoxon

R=Path(__file__).resolve().parents[1]
RAW=R/"data"/"fp_da_common_event_v1"
A=pd.read_csv(RAW/"actor_common_event_metrics.csv")
P=pd.read_csv(RAW/"passive_credit_common_event_metrics.csv")
T=pd.read_csv(RAW/"target_agreement_per_animal.csv")
POST="DA_Post06_AUCperSec"; BOUT="DA_ActionBout_AUCperSec"

def wp(x):
    x=np.asarray(x,float); x=x[np.isfinite(x)]
    return np.nan if len(x)==0 or np.allclose(x,0) else float(wilcoxon(x).pvalue)

def actor_gain(target,model):
    g=A[A.target.eq(target)].pivot(index="animal",columns="model",values="mse")
    return 100*(g["baseline_poly5"]-g[model])/g["baseline_poly5"]

def credit_gain(target,family,fixed):
    g=P[P.target.eq(target)].pivot(index="animal",columns="model",values="mse")
    return 100*(g[f"{family}_{fixed}"]-g[f"{family}_selected"])/g[f"{family}_{fixed}"]

rows=[]; per=[]
rows.append(dict(family="raw_readout",comparison="Post06_vs_ActionBout",n_animals=len(T),positive_both=np.nan,gain_rho=float(T.spearman_rho.median()),gain_rho_p=np.nan,median_post06_pct=np.nan,median_actionbout_pct=np.nan,median_delta_pct=np.nan,direct_delta_p=np.nan,note=f"raw target rho median={T.spearman_rho.median():.6f}; range={T.spearman_rho.min():.6f}-{T.spearman_rho.max():.6f}"))
for model in ["q_signed_unsigned","actor_rpe","actor_abs_rpe","actor_rpe_abs","actor_update_signed_abs","actor_full"]:
    x=actor_gain(POST,model); y=actor_gain(BOUT,model).reindex(x.index); rho,rp=spearmanr(x,y); d=x-y
    rows.append(dict(family="actor",comparison=model,n_animals=len(x),positive_both=int(((x>0)&(y>0)).sum()),gain_rho=float(rho),gain_rho_p=float(rp),median_post06_pct=float(x.median()),median_actionbout_pct=float(y.median()),median_delta_pct=float(d.median()),direct_delta_p=wp(d),note="percent MSE improvement within each readout"))
    for an in x.index: per.append(dict(animal=an,family="actor",comparison=model,post06_pct=float(x.loc[an]),actionbout_pct=float(y.loc[an])))
for family in ["update","full"]:
    for fixed in ["w0p75","w1p0"]:
        x=credit_gain(POST,family,fixed); y=credit_gain(BOUT,family,fixed).reindex(x.index); rho,rp=spearmanr(x,y); d=x-y
        rows.append(dict(family="passive_credit",comparison=f"{family}_selected_vs_{fixed}",n_animals=len(x),positive_both=int(((x>0)&(y>0)).sum()),gain_rho=float(rho),gain_rho_p=float(rp),median_post06_pct=float(x.median()),median_actionbout_pct=float(y.median()),median_delta_pct=float(d.median()),direct_delta_p=wp(d),note="percent MSE improvement of behavior-selected credit"))
        for an in x.index: per.append(dict(animal=an,family="passive_credit",comparison=f"{family}_selected_vs_{fixed}",post06_pct=float(x.loc[an]),actionbout_pct=float(y.loc[an])))
pd.DataFrame(rows).to_csv(R/"data"/"SLM_FP_DA_CROSS_READOUT_CONSENSUS_v1.csv",index=False)
pd.DataFrame(per).to_csv(R/"data"/"SLM_FP_DA_CROSS_READOUT_PER_ANIMAL_v1.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False))
