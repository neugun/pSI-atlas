from pathlib import Path
import numpy as np,csv,json

ROOT=Path('/data/sternsonlab/Zhenggang/CaRMApipeline/_slurm_fso/all_animals_signal_source_v2_carmav3_suite2p')
OUT=Path('/data/sternsonlab/Zhenggang/CaRMApipeline/_slurm_fso/all_animals_signal_source_summary_v3_carmav3_suite2p')
OUT.mkdir(parents=True,exist_ok=True)
PILOT={'113_test5'}

def corr(a,b):
    a=np.asarray(a,float).ravel(); b=np.asarray(b,float).ravel()
    m=np.isfinite(a)&np.isfinite(b)
    if m.sum()<5:return np.nan
    aa=a[m]-a[m].mean(); bb=b[m]-b[m].mean()
    den=np.sqrt(np.sum(aa*aa)*np.sum(bb*bb))
    return float(np.sum(aa*bb)/den) if den>0 else np.nan
def med(v):
    q=np.asarray(v,float); q=q[np.isfinite(q)]
    return float(np.median(q)) if q.size else np.nan
def pct(v,p):
    q=np.asarray(v,float); q=q[np.isfinite(q)]
    return float(np.percentile(q,p)) if q.size else np.nan
def stdratio(a,b):
    return float(np.nanstd(np.asarray(a,float))/(np.nanstd(np.asarray(b,float))+1e-12))
def scalar(z,k):
    if k not in z.files:return np.nan
    try:return float(np.asarray(z[k]).item())
    except:return np.nan

files=[]; cellacc={}; trial_checkpoint={}
for sd in sorted([p for p in ROOT.iterdir() if p.is_dir()]):
    if sd.name in PILOT: continue
    for fp in sorted(sd.glob('T*.npz')):
        try:
            z=np.load(str(fp),allow_pickle=True)
            req=['ids','raw','carma_bg_v3','carma_sub_v3','suite_neu','suite_sub']
            miss=[k for k in req if k not in z.files]
            if miss:
                files.append([sd.name,fp.name,0,'missing:'+','.join(miss)]); continue
            ids=z['ids'].astype(int)
            raw=z['raw'].astype(float); cb=z['carma_bg_v3'].astype(float); cs=z['carma_sub_v3'].astype(float)
            sn=z['suite_neu'].astype(float); ss=z['suite_sub'].astype(float)
            animal=str(np.asarray(z['animal']).item()) if 'animal' in z.files else sd.name.split('_')[0]
            trial=int(np.asarray(z['trial']).item()) if 'trial' in z.files else int(''.join(c for c in fp.stem if c.isdigit()) or 0)
            cnp=z['carma_bg_npix'].astype(float) if 'carma_bg_npix' in z.files else np.full(len(ids),np.nan)
            snp=z['suite_neu_npix'].astype(float) if 'suite_neu_npix' in z.files else np.full(len(ids),np.nan)
            rnp=z['roi_npix'].astype(float) if 'roi_npix' in z.files else np.full(len(ids),np.nan)
            trial_checkpoint.setdefault((animal,sd.name),[]).append({
              'carma_raw':scalar(z,'checkpoint_carma_raw_r'),
              'carma_bg':scalar(z,'checkpoint_carma_bg_r'),
              'carma_sub':scalar(z,'checkpoint_carma_sub_r'),
              'suite_sub':scalar(z,'checkpoint_suite_sub_r'),
              'old2_sub':scalar(z,'checkpoint_old2_sub_r')})
            for i,rid in enumerate(ids):
                key=(animal,sd.name,int(rid))
                a=cellacc.setdefault(key,{'animal':animal,'session_id':sd.name,'roi_id':int(rid),'trials':set(),
                   'method_r':[],'raw_carma_bg_r':[],'raw_suite_neu_r':[],'carma_resid_bg_r':[],'suite_resid_neu_r':[],
                   'carma_std_ratio':[],'suite_std_ratio':[],'carma_bg_npix':[],'suite_neu_npix':[],'roi_npix':[]})
                a['trials'].add(trial)
                a['method_r'].append(corr(cs[i],ss[i]))
                a['raw_carma_bg_r'].append(corr(raw[i],cb[i]))
                a['raw_suite_neu_r'].append(corr(raw[i],sn[i]))
                a['carma_resid_bg_r'].append(corr(cs[i],cb[i]))
                a['suite_resid_neu_r'].append(corr(ss[i],sn[i]))
                a['carma_std_ratio'].append(stdratio(cs[i],raw[i]))
                a['suite_std_ratio'].append(stdratio(ss[i],raw[i]))
                a['carma_bg_npix'].append(float(cnp[i])); a['suite_neu_npix'].append(float(snp[i])); a['roi_npix'].append(float(rnp[i]))
            files.append([sd.name,fp.name,1,''])
        except Exception as e:
            files.append([sd.name,fp.name,0,repr(e)])

with open(OUT/'FILE_AUDIT.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['session_id','file','ok','error']); w.writerows(files)

cellrows=[]
for a in cellacc.values():
    r={k:a[k] for k in ['animal','session_id','roi_id']}; r['n_trials']=len(a['trials'])
    for k in ['method_r','raw_carma_bg_r','raw_suite_neu_r','carma_resid_bg_r','suite_resid_neu_r',
              'carma_std_ratio','suite_std_ratio','carma_bg_npix','suite_neu_npix','roi_npix']:
        r[k]=med(a[k])
    r['suite_lower_abs_residual']=int(np.isfinite(r['suite_resid_neu_r']) and np.isfinite(r['carma_resid_bg_r']) and abs(r['suite_resid_neu_r'])<abs(r['carma_resid_bg_r']))
    cellrows.append(r)
cellfields=list(cellrows[0].keys())
with open(OUT/'ALL_CELL_METHOD_METRICS.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cellfields); w.writeheader(); w.writerows(cellrows)

sess={}
for r in cellrows:sess.setdefault((r['animal'],r['session_id']),[]).append(r)
sessrows=[]
for (animal,sid),rs in sorted(sess.items()):
    get=lambda k:[r[k] for r in rs]; ck=trial_checkpoint.get((animal,sid),[]); ckg=lambda k:[x[k] for x in ck]
    sr=dict(animal=animal,session_id=sid,n_cells=len(rs),n_trials=max(r['n_trials'] for r in rs),
      method_r=med(get('method_r')),method_r_q25=pct(get('method_r'),25),method_r_q75=pct(get('method_r'),75),
      raw_carma_bg_r=med(get('raw_carma_bg_r')),raw_suite_neu_r=med(get('raw_suite_neu_r')),
      carma_resid_bg_r=med(get('carma_resid_bg_r')),suite_resid_neu_r=med(get('suite_resid_neu_r')),
      frac_suite_lower_abs_residual=float(np.mean(get('suite_lower_abs_residual'))),
      carma_std_ratio=med(get('carma_std_ratio')),suite_std_ratio=med(get('suite_std_ratio')),
      roi_npix=med(get('roi_npix')),carma_bg_npix=med(get('carma_bg_npix')),suite_neu_npix=med(get('suite_neu_npix')),
      checkpoint_raw_r=med(ckg('carma_raw')),checkpoint_carma_bg_r=med(ckg('carma_bg')),
      checkpoint_carma_sub_r=med(ckg('carma_sub')),checkpoint_suite_sub_r=med(ckg('suite_sub')),
      checkpoint_old2_sub_r=med(ckg('old2_sub')),n_checkpoint_trials=int(np.sum(np.isfinite(np.asarray(ckg('carma_sub'),float)))))
    sessrows.append(sr)
sf=list(sessrows[0].keys())
with open(OUT/'SESSION_METHOD_SUMMARY.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=sf); w.writeheader(); w.writerows(sessrows)

ani={}
for r in sessrows:ani.setdefault(r['animal'],[]).append(r)
anirows=[]
for animal,rs in sorted(ani.items()):
    anirows.append(dict(animal=animal,n_sessions=len(rs),n_cell_sessions=sum(r['n_cells'] for r in rs),n_trials=sum(r['n_trials'] for r in rs),
      method_r=med([r['method_r'] for r in rs]),carma_resid_bg_r=med([r['carma_resid_bg_r'] for r in rs]),
      suite_resid_neu_r=med([r['suite_resid_neu_r'] for r in rs]),frac_suite_lower_abs_residual=med([r['frac_suite_lower_abs_residual'] for r in rs]),
      carma_std_ratio=med([r['carma_std_ratio'] for r in rs]),suite_std_ratio=med([r['suite_std_ratio'] for r in rs]),
      checkpoint_carma_sub_r=med([r['checkpoint_carma_sub_r'] for r in rs]),checkpoint_suite_sub_r=med([r['checkpoint_suite_sub_r'] for r in rs]),
      checkpoint_old2_sub_r=med([r['checkpoint_old2_sub_r'] for r in rs])))
af=list(anirows[0].keys())
with open(OUT/'ANIMAL_METHOD_SUMMARY.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=af); w.writeheader(); w.writerows(anirows)

summary={'method':'exact ExtractVOlResp_SubRing_v3 [2,20] vs Suite2p-style neuropil alpha=0.7',
         'n_files_total':len(files),'n_files_ok':sum(r[2] for r in files),'n_files_failed':sum(1-r[2] for r in files),
         'n_cell_session_rows':len(cellrows),'n_sessions':len(sessrows),'animals':sorted(ani.keys()),'pilot_excluded':sorted(PILOT)}
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
for r in sessrows: print(r)
