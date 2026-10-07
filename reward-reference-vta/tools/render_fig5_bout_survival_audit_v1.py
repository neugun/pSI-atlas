#!/usr/bin/env python3
"""Render Fig5 sensitivity summary as two editable, square vector panels.

Uses aggregate audits only, not raw animal traces.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; OUT=ROOT/'assets'
TEAL='#166a78'; ORANGE='#bf7d39'; DARK='#243645'; GREY='#7a8490'
plt.rcParams.update({
    'font.family':'DejaVu Sans','font.size':12,
    'axes.titlesize':15,'axes.labelsize':13,
    'xtick.labelsize':12,'ytick.labelsize':12,
    'axes.linewidth':1.0,'svg.fonttype':'none',
    'savefig.facecolor':'white','figure.facecolor':'white'
})
def setup():
    fig,ax=plt.subplots(figsize=(6.2,6.2))
    fig.subplots_adjust(left=.19,right=.96,bottom=.18,top=.87)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both',direction='out',length=4,width=.9,color=DARK)
    ax.set_box_aspect(.86)
    return fig,ax
def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=190)
    fig.savefig(OUT/(name+'.svg'))
    plt.close(fig)
    print(name,'PNG+SVG generated')
def panel_A():
    d=pd.read_csv(DATA/'FIG5_bout_duration_sensitivity_v1.csv')
    d=d.loc[d.outcome=='delta_sust_early'].sort_values('min_bout_s')
    fig,ax=setup()
    thrs=np.array([5,7,10,15,20]); xx=np.arange(len(thrs))
    for offset,adjust,color,label in [(-.09,False,TEAL,'Adjusted for task/action'),(.09,True,ORANGE,'+ bout duration')]:
        s=d[d.duration_adjusted==adjust].set_index('min_bout_s').loc[thrs]
        yy=s.beta_C.to_numpy(float);err=s.se_C_cluster.to_numpy(float)
        ax.errorbar(xx+offset,yy,yerr=err,color=color,ecolor=color,marker='o',
                    markersize=5.0,linewidth=1.8,elinewidth=1.2,capsize=3,
                    capthick=1.2,label=label)
    ax.axhline(0,color=GREY,linewidth=.9)
    ax.set_xticks(xx, [str(a) for a in thrs])
    ax.set_xlabel('Minimum bout duration (s)',labelpad=10)
    ax.set_ylabel('Contrast coefficient\n(sustained minus early DA)',labelpad=10)
    ax.set_title('Fig. 5 | Bout-selection sensitivity',pad=20)
    ax.legend(loc='upper right',bbox_to_anchor=(1.0,1.02),frameon=False,fontsize=10)
    s=d[d.duration_adjusted==False].set_index('min_bout_s').loc[thrs]
    for x,n in zip(xx,s.n_bouts):
        ax.text(x,-1.35,f'n={n}',ha='center',va='center',fontsize=9,color=GREY)
    ax.set_ylim(-1.6,3.8)
    save(fig,'Fig5_bout_selection_audit_v1')
def panel_B():
    d=pd.read_csv(DATA/'FIG5_nested_LOAO_contrast_gain_v1.csv')
    d=d.loc[d.outcome=='delta_sust_early']
    fig,ax=setup()
    thrs=np.array([5,7,10]);xx=np.arange(len(thrs))
    for offset,adjust,color,label in [(-.065,False,TEAL,'Task/action controls'),(.065,True,ORANGE,'+ bout duration')]:
        s=d[d.duration_adjusted==adjust].set_index('min_bout_s').loc[thrs]
        vals=s.relative_mse_gain_pct.to_numpy(float)
        ax.plot(xx+offset,vals,color=color,marker='o',linewidth=1.8,markersize=6,
                label=label)
        for x,y,w in zip(xx+offset,vals,s.wins_animal):
            ax.annotate(f'{int(w)}/11',(x,y),xytext=(0,9 if adjust else -15),
                        textcoords='offset points',ha='center',fontsize=10,color=color)
    ax.axhline(0,color=GREY,linewidth=.9)
    ax.set_ylim(-1.6,10.2)
    ax.set_xticks(xx,[str(a) for a in thrs])
    ax.set_xlabel('Minimum bout duration (s)',labelpad=10)
    ax.set_ylabel('LOAO MSE improvement (%)',labelpad=10)
    ax.set_title('Fig. 5 | Held-mouse generalization',pad=20)
    ax.legend(loc='upper left',frameon=False,fontsize=10)
    save(fig,'Fig5_heldmouse_increment_audit_v1')
if __name__=='__main__':
    panel_A();panel_B()
