# -*- coding: utf-8 -*-
from pathlib import Path
p=Path(__file__).resolve().parent/"qa_fp_psth_story_v84.py"
s=p.read_text(encoding="utf-8")
old='''    ck(fn+"_event_selection_figure",s.count("SOE_FP_PSTH_event_selection_v86.png")==2)
    ck(fn+"_clean",all(x not in s for x in ["???","�","Ã","â€"]))
'''
new='''    ck(fn+"_event_selection_figure",s.count("SOE_FP_PSTH_event_selection_v86.png")==2)
    ck(fn+"_model_psth_figure",s.count("SOE_FP_PSTH_model_variables_v88.png")==2)
    ck(fn+"_model_psth_source","SOE_FP_PSTH_MODEL_VARIABLES_v88.csv" in s)
    ck(fn+"_clean",all(x not in s for x in ["???","�","Ã","â€"]))
'''
if old not in s: raise RuntimeError("qa page block missing")
s=s.replace(old,new,1)
old2='''"SOE_FP_next_observe_memory_v83.png","SOE_FP_next_observe_memory_v83.pdf","SOE_FP_next_observe_memory_v83.svg","SOE_FP_next_observe_memory_v83_mobile.png"]:
'''
new2='''"SOE_FP_next_observe_memory_v83.png","SOE_FP_next_observe_memory_v83.pdf","SOE_FP_next_observe_memory_v83.svg","SOE_FP_next_observe_memory_v83_mobile.png",
"SOE_FP_PSTH_model_variables_v88.png","SOE_FP_PSTH_model_variables_v88.pdf","SOE_FP_PSTH_model_variables_v88.svg","SOE_FP_PSTH_model_variables_v88_mobile.png"]:
'''
if old2 not in s: raise RuntimeError("qa asset block missing")
s=s.replace(old2,new2,1)
s += '''
modelsrc=R/"data"/"SOE_FP_PSTH_MODEL_VARIABLES_v88.csv"
ck("model_psth_source_exists",modelsrc.exists() and modelsrc.stat().st_size>1000,modelsrc.stat().st_size if modelsrc.exists() else "missing")
'''
p.write_text(s,encoding="utf-8")
print("qa updated for v88")
