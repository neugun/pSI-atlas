from pathlib import Path
import sys,csv,re,json,traceback
import numpy as np,tifffile as tf
from scipy.ndimage import binary_dilation,binary_closing,binary_fill_holes

ROOT=Path('/data/sternsonlab/Zhenggang/CaRMApipeline')
MAN=ROOT/'_slurm_fso'/'all_animals_signal_source_manifest_v1.csv'
OUT=ROOT/'_slurm_fso'/'all_animals_signal_source_v2_carmav3_suite2p'
OUT.mkdir(parents=True,exist_ok=True)

idx=int(sys.argv[1])
with open(MAN,newline='') as f:
    rows=list(csv.DictReader(f))
row=rows[idx]
animal=str(row['animal']); sid=str(row['session_id']); trial=int(row['trial'])
sout=OUT/sid; sout.mkdir(exist_ok=True)
dest=sout/f'T{trial:03d}.npz'
status=sout/f'T{trial:03d}.json'
if dest.exists() and dest.stat().st_size>1000:
    print('SKIP',sid,trial,flush=True); raise SystemExit(0)

def disk(rad):
    yy,xx=np.ogrid[-rad:rad+1,-rad:rad+1]
    return (xx*xx+yy*yy)<=rad*rad
D2=disk(2)

def norm_labels(lab,max_plane):
    lab=np.asarray(lab)
    if lab.ndim==2: lab=lab[None]
    if lab.ndim!=3: raise RuntimeError(f'label ndim {lab.shape}')
    if lab.shape[0]>=max_plane and lab.shape[0] <= 32: return lab
    if lab.shape[-1]>=max_plane and lab.shape[-1] <= 32: return np.moveaxis(lab,-1,0)
    if lab.shape[0]>=max_plane: return lab
    raise RuntimeError(f'cannot orient labels {lab.shape} maxplane={max_plane}')

def extendROI(ypix,xpix,Ly,Lx,niter=1):
    for _ in range(niter):
        yx=((ypix,ypix,ypix,ypix-1,ypix+1),(xpix,xpix+1,xpix-1,xpix,xpix))
        yx=np.array(yx).reshape((2,-1))
        yu=np.unique(yx,axis=1)
        ok=np.all((yu[0]>=0,yu[0]<Ly,yu[1]>=0,yu[1]<Lx),axis=0)
        ypix,xpix=yu[:,ok]
    return ypix,xpix

def suite_neuropil_mask(roi,cell_pix):
    Ly,Lx=roi.shape
    ypix,xpix=np.nonzero(roi)
    if len(ypix)==0: return np.zeros_like(roi,bool)
    # Suite2p-style: inner_neuropil_radius=2, then grow until >=350 usable pixels.
    y0,x0=extendROI(ypix,xpix,Ly,Lx,niter=2)
    nring=np.sum(~cell_pix[y0,x0])
    y1,x1=y0,x0
    reps=0
    while reps<100 and (np.sum(~cell_pix[y1,x1])-nring)<=350:
        y1,x1=extendROI(y1,x1,Ly,Lx,5); reps+=1
    keep=~cell_pix[y1,x1]
    m=np.zeros((Ly,Lx),bool)
    m[y1[keep],x1[keep]]=1
    m[y0,x0]=0
    return m

def carma_v3_masks(label2d,ids_plane):
    """Reproduce ExtractVOlResp_SubRing_v3 background geometry.
    Fixed ROI: fill holes + imclose(disk2), overlapping closed pixels excluded.
    Background: radius-20 disk around original ROI centroid, excluding all fixed ROIs
    dilated by disk2. Historical coefficient is 1.0.
    """
    Ly,Lx=label2d.shape
    yy,xx=np.mgrid[0:Ly,0:Lx]
    raw=[]; fixed=[]
    for rid in ids_plane:
        r=binary_fill_holes(label2d==int(rid))
        raw.append(r)
        fixed.append(binary_closing(r,structure=D2))
    fixed=np.asarray(fixed,bool)
    count=fixed.sum(axis=0)
    exclusive=fixed & (count[None,:,:]==1)
    union_fixed=np.any(fixed,axis=0)
    excluded=binary_dilation(union_fixed,structure=D2)
    bg=[]
    for r in raw:
        y,x=np.nonzero(r)
        if len(y)==0:
            bg.append(np.zeros_like(r,bool)); continue
        cy=float(y.mean()); cx=float(x.mean())
        outer=np.hypot(xx-cx,yy-cy)<=20.0
        bg.append(outer & (~excluded))
    return exclusive,np.asarray(bg,bool),union_fixed

def movie_time_first(a):
    a=np.asarray(a)
    if a.ndim!=3: raise RuntimeError(f'movie shape {a.shape}')
    if a.shape[-2]==a.shape[-1] and a.shape[0]!=a.shape[-1]: return a
    if a.shape[0]==a.shape[1] and a.shape[-1]!=a.shape[0]: return np.moveaxis(a,-1,0)
    ax=int(np.argmin(a.shape))
    return np.moveaxis(a,ax,0) if ax!=0 else a

def extract(mov,masks):
    flat=mov.reshape(mov.shape[0],-1)
    out=np.full((len(masks),mov.shape[0]),np.nan,np.float32)
    for i,m in enumerate(masks):
        q=np.asarray(m,bool).ravel()
        if q.any(): out[i]=flat[:,q].mean(axis=1)
    return out

def rcorr(a,b):
    a=np.asarray(a,float).ravel(); b=np.asarray(b,float).ravel()
    m=np.isfinite(a)&np.isfinite(b)
    if m.sum()<10:return np.nan
    aa=a[m]-a[m].mean(); bb=b[m]-b[m].mean()
    den=np.sqrt(np.sum(aa*aa)*np.sum(bb*bb))
    return float(np.sum(aa*bb)/den) if den>0 else np.nan

try:
    with open(row['qc_file'],newline='') as f:
        qrows=list(csv.DictReader(f))
    qcols=list(qrows[0].keys()) if qrows else []
    pcol='plane' if 'plane' in qcols else [c for c in qcols if c.lower()=='plane'][0]
    low={c.lower():c for c in qcols}; icol=None
    for k in ['roi_id','id','cell_id']:
        if k in low: icol=low[k]; break
    if icol is None:
        cands=[c for c in qcols if c.lower().endswith('_id') and 'track' not in c.lower() and 'session' not in c.lower()]
        if cands: icol=cands[-1]
    if icol is None: raise RuntimeError('no id column '+str(qcols))
    ids=np.array([int(float(q[icol])) for q in qrows],int)
    planes=np.array([int(float(q[pcol])) for q in qrows],int)
    lab=norm_labels(tf.imread(str(row['label_file'])),int(planes.max()))

    if str(row['mode'])=='single_dir':
        tdir=Path(str(row['source_root']))
    else:
        dirs=[p for p in Path(str(row['source_root'])).iterdir() if p.is_dir() and p.name.endswith('_S')]
        def anum(p):
            m=re.search(r'_(\d+)_S$',p.name); return int(m.group(1)) if m else 10**12
        dirs=sorted(dirs,key=anum)
        if trial<1 or trial>len(dirs): raise RuntimeError(f'trial {trial} > dirs {len(dirs)}')
        tdir=dirs[trial-1]

    firstplane=int(planes[0])
    q=list(tdir.glob(f'*_S{firstplane}_C1_reg.tif'))
    if not q: raise RuntimeError(f'no registered movie plane {firstplane} in {tdir}')
    mov0=movie_time_first(tf.imread(str(q[0]))).astype(np.float32)
    T=mov0.shape[0]; n=len(ids)

    raw=np.full((n,T),np.nan,np.float32)
    carma_bg=np.full_like(raw,np.nan); carma_sub=np.full_like(raw,np.nan)
    suite_neu=np.full_like(raw,np.nan); suite_sub=np.full_like(raw,np.nan)
    old2_bg=np.full_like(raw,np.nan); old2_sub=np.full_like(raw,np.nan)
    roi_npix=np.zeros(n,int); carma_bg_npix=np.zeros(n,int); suite_neu_npix=np.zeros(n,int); old2_npix=np.zeros(n,int)

    for pl in sorted(set(planes.tolist())):
        gi=np.flatnonzero(planes==pl)
        q=list(tdir.glob(f'*_S{pl}_C1_reg.tif'))
        if not q:
            print('WARN missing plane',sid,trial,pl,flush=True); continue
        mov=mov0 if pl==firstplane else movie_time_first(tf.imread(str(q[0]))).astype(np.float32)
        if mov.shape[0]!=T:
            tt=min(T,mov.shape[0]); pad=np.full((T,mov.shape[1],mov.shape[2]),np.nan,np.float32); pad[:tt]=mov[:tt]; mov=pad
            print('WARN frame-count mismatch',sid,trial,'plane',pl,'usable',tt,'of',T,flush=True)
        label2d=lab[pl-1]
        ip=ids[gi]
        cm,cb,cell_union=carma_v3_masks(label2d,ip)
        sb=[]; old=[]
        for m in cm:
            sb.append(suite_neuropil_mask(m,cell_union))
            old.append(binary_dilation(m,structure=D2)&(~m))
        a=extract(mov,cm); b=extract(mov,cb); sn=extract(mov,sb); ob=extract(mov,old)
        raw[gi]=a; carma_bg[gi]=b; carma_sub[gi]=a-b
        suite_neu[gi]=sn; suite_sub[gi]=a-0.7*sn
        old2_bg[gi]=ob; old2_sub[gi]=a-ob
        for j,g in enumerate(gi):
            roi_npix[g]=int(cm[j].sum()); carma_bg_npix[g]=int(cb[j].sum()); suite_neu_npix[g]=int(sb[j].sum()); old2_npix[g]=int(old[j].sum())

    ck_raw=np.empty((0,0),np.float32); ck_bg=np.empty((0,0),np.float32); ck_sub=np.empty((0,0),np.float32)
    metrics={'checkpoint_carma_raw_r':np.nan,'checkpoint_carma_bg_r':np.nan,'checkpoint_carma_sub_r':np.nan,
             'checkpoint_suite_sub_r':np.nan,'checkpoint_old2_sub_r':np.nan}
    cp=str(row.get('checkpoint_dir','') or '')
    if cp:
        cps=[Path(cp)/f'T{trial:02d}.npz',Path(cp)/f'T{trial:03d}.npz']
        cpfile=next((p for p in cps if p.exists()),None)
        if cpfile:
            z=np.load(str(cpfile),allow_pickle=True)
            if 'raw' in z and z['raw'].shape==raw.shape:
                ck_raw=z['raw'].astype(np.float32); metrics['checkpoint_carma_raw_r']=rcorr(ck_raw,raw)
            if 'bg' in z and z['bg'].shape==carma_bg.shape:
                ck_bg=z['bg'].astype(np.float32); metrics['checkpoint_carma_bg_r']=rcorr(ck_bg,carma_bg)
            if 'sub' in z and z['sub'].shape==carma_sub.shape:
                ck_sub=z['sub'].astype(np.float32)
                metrics['checkpoint_carma_sub_r']=rcorr(ck_sub,carma_sub)
                metrics['checkpoint_suite_sub_r']=rcorr(ck_sub,suite_sub)
                metrics['checkpoint_old2_sub_r']=rcorr(ck_sub,old2_sub)

    np.savez_compressed(dest,animal=animal,session_id=sid,trial=trial,ids=ids,planes=planes,
        method_version='carmav3_exact_vs_suite2p_v2',source_dir=str(tdir),
        raw=raw,carma_bg_v3=carma_bg,carma_sub_v3=carma_sub,suite_neu=suite_neu,suite_sub=suite_sub,
        old2_bg=old2_bg,old2_sub=old2_sub,
        roi_npix=roi_npix,carma_bg_npix=carma_bg_npix,suite_neu_npix=suite_neu_npix,old2_bg_npix=old2_npix,
        checkpoint_raw=ck_raw,checkpoint_bg=ck_bg,checkpoint_sub=ck_sub,
        checkpoint_carma_raw_r=metrics['checkpoint_carma_raw_r'],checkpoint_carma_bg_r=metrics['checkpoint_carma_bg_r'],
        checkpoint_carma_sub_r=metrics['checkpoint_carma_sub_r'],checkpoint_suite_sub_r=metrics['checkpoint_suite_sub_r'],
        checkpoint_old2_sub_r=metrics['checkpoint_old2_sub_r'])
    st={'ok':True,'animal':animal,'session_id':sid,'trial':trial,'T':int(T),'n_cells':int(n),'source_dir':str(tdir)}
    st.update({k:(None if not np.isfinite(v) else float(v)) for k,v in metrics.items()})
    status.write_text(json.dumps(st))
    print('DONE',idx,sid,trial,'cells',n,'T',T,
          'ck_carma',metrics['checkpoint_carma_sub_r'],'ck_suite',metrics['checkpoint_suite_sub_r'],
          'ck_old2',metrics['checkpoint_old2_sub_r'],
          'carma_bg_px_med',float(np.median(carma_bg_npix[carma_bg_npix>0])) if np.any(carma_bg_npix>0) else np.nan,
          'suite_px_med',float(np.median(suite_neu_npix[suite_neu_npix>0])) if np.any(suite_neu_npix>0) else np.nan,flush=True)
except Exception as e:
    status.write_text(json.dumps({'ok':False,'animal':animal,'session_id':sid,'trial':trial,'error':repr(e),'traceback':traceback.format_exc()}))
    print('FAIL',idx,sid,trial,repr(e),flush=True)
    raise
