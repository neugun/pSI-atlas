# -*- coding: utf-8 -*-
from pathlib import Path
import os,pandas as pd
R=Path(__file__).resolve().parents[1]
# Set SOE_FP_TIMING_AUDIT_CSV to an authorized, previously validated event-level audit CSV.
inp=pd.read_csv(Path(os.environ["SOE_FP_TIMING_AUDIT_CSV"]))
out=[]
for name,flag,col in [("fixed_0_6","FixedDAValid","FixedNextOverlap"),("historical_extended","ExtDAValid","ExtendedNextOverlap")]:
 q=inp[inp[flag].astype(str).str.lower().eq("true")]
 out.append(dict(readout=name,n_valid_with_next=len(q),n_cross_next=int(q[col].sum()),fraction_cross_next=float(q[col].mean()),event_def="next AnchorStart within last DA window"))
pd.DataFrame(out).to_csv(R/"data/SOE_VTA_next_choice_event_overlap_v131.csv",index=False)
print(pd.DataFrame(out).to_string(index=False))
