#!/usr/bin/env python3
"""Auditable bout-survival sensitivity for Reward Contrast Fig. 5.

Input remains on the authorized workstation; outputs are aggregate tables only.
Does NOT regenerate raw photometry or claim mediation / independent U,R,C.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import wilcoxon

def fit_ols(x, target, include_duration=False):
    covariates = 'quality + contrast + session_fraction + within_block_sec + log_prior + log_local + C(animal)'
    if include_duration:
        covariates += ' + log_duration'
    model=smf.ols(target+' ~ '+covariates, data=x).fit(cov_type='cluster', cov_kwds={'groups':x['animal']})
    return model

def slope_by_animal(x, target):
    vals=[]
    for an,g in x.groupby('animal'):
        if len(g) < 5 or g['contrast'].std()<1e-6: continue
        if g['quality'].nunique()<2: continue
        try:
            f=smf.ols(target+' ~ quality + contrast + session_fraction + within_block_sec',data=g).fit()
            vals.append((an,float(f.params['contrast']),len(g)))
        except Exception:
            pass
    return vals

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True,help='authority11_transition_local_features.csv')
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    df=pd.read_csv(args.source, dtype={'animal':str})
    required=['row_id','animal','quality','block_index','bout_duration','da_delta_0to2','da_delta_2to5','pre_da_2to0','session_fraction','within_block_sec','prior_licks','current_block_prior_licks','C_lick_a0.1']
    assert all(k in df.columns for k in required)
    assert not df[['row_id','animal']].duplicated().any()
    d=df.loc[df.block_index>0].copy()
    d['contrast']=d['C_lick_a0.1']
    d['log_prior']=np.log1p(d['prior_licks'].clip(lower=0))
    d['log_local']=np.log1p(d['current_block_prior_licks'].clip(lower=0))
    d['log_duration']=np.log(d['bout_duration'])
    d['delta_sust_early']=d['da_delta_2to5']-d['da_delta_0to2']
    d['long5']=(d.bout_duration>=5).astype(int)
    summary=[{'metric':'all_rows','value':len(df)},
             {'metric':'block_positive_rows','value':len(d)},
             {'metric':'long5_all_rows','value':int((df.bout_duration>=5).sum())},
             {'metric':'long5_block_positive','value':int(d.long5.sum())},
             {'metric':'n_animals_all','value':df.animal.nunique()},
             {'metric':'shorter_than_2s_rows','value':int((df.bout_duration<2).sum())},
             {'metric':'shorter_than_5s_rows','value':int((df.bout_duration<5).sum())}]
    rows=[]
    for thresh in [5,7,10,15,20]:
        z=d.loc[d.bout_duration>=thresh].copy()
        if len(z)<35: continue
        for adjust in [False,True]:
            for target in ['da_delta_0to2','da_delta_2to5','delta_sust_early']:
                fit=fit_ols(z,target,adjust)
                animal=slope_by_animal(z,target)
                vals=np.array([e[1] for e in animal])
                p_sign=float(wilcoxon(vals).pvalue) if len(vals)>=5 and np.any(vals !=0) else np.nan
                rows.append({'min_bout_s':thresh,'duration_adjusted':adjust,'outcome':target,
                             'n_bouts':len(z),'n_animals':z.animal.nunique(),
                             'beta_C':float(fit.params['contrast']),'se_C_cluster':float(fit.bse['contrast']),
                             'p_C_cluster':float(fit.pvalues['contrast']),
                             'beta_quality':float(fit.params['quality']),
                             'p_quality_cluster':float(fit.pvalues['quality']),
                             'n_animal_slopes':len(vals),
                             'animal_positive_C':int((vals>0).sum()),
                             'animal_wilcoxon_two_sided_p':p_sign,
                             'r2_in_sample':float(fit.rsquared)})
    sels=[]
    for y in ['long5']:
        m=smf.logit(y+' ~ quality + contrast + session_fraction + within_block_sec + log_prior + log_local + C(animal)',data=d).fit(disp=False,maxiter=300)
        robust=smf.logit(y+' ~ quality + contrast + session_fraction + within_block_sec + log_prior + log_local + C(animal)',data=d).fit(disp=False,maxiter=300,cov_type='cluster',cov_kwds={'groups':d['animal']})
        for name in ['quality','contrast','log_prior','log_local']:
            sels.append({'n_bouts':len(d),'n_long':int(d.long5.sum()),
                         'term':name,'beta_log_odds':float(robust.params[name]),
                         'odds_ratio':float(np.exp(robust.params[name])),
                         'cluster_se':float(robust.bse[name]),
                         'cluster_p':float(robust.pvalues[name])})
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'FIG5_bout_duration_sensitivity_v1.csv',index=False)
    pd.DataFrame(sels).to_csv(out/'FIG5_survival_selection_logit_v1.csv',index=False)
    pd.DataFrame(summary).to_csv(out/'FIG5_bout_sample_accounting_v1.csv',index=False)
    print('SAMPLE_ACCOUNTING')
    print(pd.DataFrame(summary).to_string(index=False))
    print('SELECTED_COEFFICIENTS (duration-unadjusted)')
    print(pd.DataFrame(rows).query('duration_adjusted == False')[['min_bout_s','outcome','n_bouts','n_animals','beta_C','se_C_cluster','p_C_cluster','animal_positive_C','n_animal_slopes']].to_string(index=False,float_format=lambda v:f'{v:.5g}'))
    print('SURVIVAL_ASSOCIATION')
    print(pd.DataFrame(sels).to_string(index=False,float_format=lambda v:f'{v:.5g}'))
    print('OUTPUTS',str(out))
if __name__=='__main__':
    main()
