#!/usr/bin/env python3
"""Nested leave-one-animal-out incremental prediction of Fig5 signal.

The source table is read locally; only aggregated diagnostics are written.
Fixed animals as CV groups, inner LOAO ridge tuning prevents held-mouse leakage.
"""
import argparse
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error,r2_score

PARAMS=[.1,1.,10.,100.]
BASE=['quality','session_fraction','within_block_sec','log_prior','log_local']
def model(alpha):
    return Pipeline([('impute',SimpleImputer(strategy='median')),
                     ('scale',StandardScaler()),('ridge',Ridge(alpha=alpha))])
def choose_alpha(train, columns, outcome):
    scores=[]
    animals=sorted(train.animal.unique())
    for alpha in PARAMS:
        diffs=[]
        for aid in animals:
            tr=train.loc[train.animal!=aid]; te=train.loc[train.animal==aid]
            if len(tr)<20 or len(te)<2:continue
            m=model(alpha);m.fit(tr[columns],tr[outcome])
            diffs.append(mean_squared_error(te[outcome],m.predict(te[columns])))
        scores.append(np.mean(diffs))
    return PARAMS[int(np.argmin(scores))]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    d=pd.read_csv(args.source,dtype={'animal':str})
    d=d.loc[d.block_index>0].copy()
    d['log_prior']=np.log1p(d.prior_licks)
    d['log_local']=np.log1p(d.current_block_prior_licks)
    d['log_duration']=np.log(d.bout_duration)
    d['contrast']=d['C_lick_a0.1']
    d['delta_sust_early']=d.da_delta_2to5-d.da_delta_0to2
    results=[]
    for threshold in [5,7,10]:
        z=d.loc[d.bout_duration>=threshold].copy()
        for outcome in ['da_delta_2to5','delta_sust_early']:
            for adjusted in [False,True]:
                b=BASE+(['log_duration'] if adjusted else [])
                preds=[]
                for aid in sorted(z.animal.unique()):
                    tr=z.loc[z.animal!=aid];te=z.loc[z.animal==aid]
                    row={'animal':aid,'y':te[outcome].to_numpy(),'n':len(te)}
                    for variant,cols in [('base',b),('plus_contrast',b+['contrast'])]:
                        alpha=choose_alpha(tr,cols,outcome)
                        fit=model(alpha).fit(tr[cols],tr[outcome])
                        row[variant]=fit.predict(te[cols])
                    preds.append(row)
                mse0=np.sum([((x['base']-x['y'])**2).sum() for x in preds])/len(z)
                mse1=np.sum([((x['plus_contrast']-x['y'])**2).sum() for x in preds])/len(z)
                animal_gain=np.array([np.mean((x['base']-x['y'])**2)-np.mean((x['plus_contrast']-x['y'])**2) for x in preds])
                ys=np.concatenate([x['y'] for x in preds])
                p0=np.concatenate([x['base'] for x in preds]);p1=np.concatenate([x['plus_contrast'] for x in preds])
                results.append({'min_bout_s':threshold,'outcome':outcome,'duration_adjusted':adjusted,
                'n_bouts':len(z),'n_animals':len(preds),'mse_base':mse0,'mse_plus_contrast':mse1,
                'relative_mse_gain_pct':100*(mse0-mse1)/mse0,
                'oof_r2_base':r2_score(ys,p0),'oof_r2_plus_contrast':r2_score(ys,p1),
                'wins_animal':int((animal_gain>0).sum()),
                'median_animal_delta_mse':float(np.median(animal_gain)),
                'wilcoxon_p_one_sided':float(wilcoxon(animal_gain,alternative='greater').pvalue)})
    out=pd.DataFrame(results);out.to_csv(args.output,index=False)
    print(out.to_string(index=False,float_format=lambda a:f'{a:.5g}'))
if __name__=='__main__':main()
