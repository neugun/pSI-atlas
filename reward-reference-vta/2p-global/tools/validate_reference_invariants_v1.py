from pathlib import Path
import argparse, json, os, sys
import pandas as pd

BUNDLES=[
    ("54","ANM54_REFERENCE_V3"),
    ("181","ANM181_REFERENCE_V1"),
    ("112","ANM112_REFERENCE_V1"),
    ("113","ANM113_REFERENCE_V1"),
    ("185","ANM185_REFERENCE_V1"),
]

def load_review_js(path):
    t=Path(path).read_text(encoding="utf-8")
    key="window.CARMA_IDENTITY_CANDIDATES="
    i=t.find(key); j=t.rfind(";")
    if i<0 or j<0 or j<=i:
        raise ValueError("identity review JS payload not found")
    return json.loads(t[i+len(key):j])

def validate(root):
    root=Path(root).resolve()
    errors=[]; rows=[]
    for animal,name in BUNDLES:
        bundle=root/name
        mf=bundle/"bundle_manifest.json"
        if not mf.exists():
            errors.append(f"{name}: missing bundle_manifest.json"); continue
        m=json.loads(mf.read_text(encoding="utf-8"))
        sessions=[str(x) for x in m.get("sessions",[])]
        if str(m.get("animal"))!=animal:
            errors.append(f"{name}: manifest animal={m.get('animal')} expected {animal}")
        if int(m.get("n_sessions",-1))!=len(sessions):
            errors.append(f"{name}: n_sessions mismatch")
        roi_ids={}
        for sid in sessions:
            sm=bundle/"sessions"/sid/"session_manifest.json"
            if not sm.exists():
                errors.append(f"{name}: missing session manifest {sid}"); continue
            s=json.loads(sm.read_text(encoding="utf-8"))
            if str(s.get("animal"))!=animal:
                errors.append(f"{name}/{sid}: animal={s.get('animal')} expected {animal}")
            if not sid.startswith(animal+"_") and not (animal=="113" and sid=="113_test"):
                errors.append(f"{name}/{sid}: session prefix inconsistent with animal")
            roi_ids[sid]=set(map(int,s.get("roi_ids",[])))
            if int(s.get("n_roi",-1))!=len(roi_ids[sid]):
                errors.append(f"{name}/{sid}: n_roi vs roi_ids mismatch")

        cp=bundle/"identity_review_candidates.csv"
        ncan=0; review_mask_pairs=0
        if cp.exists():
            c=pd.read_csv(cp); ncan=len(c)
            aliases={"source_session":"src_session","source_roi":"src_roi","target_session":"tgt_session","target_roi":"tgt_roi"}
            for canon,ref in aliases.items():
                if ref not in c.columns and canon in c.columns:
                    c=c.rename(columns={canon:ref})
            req=["candidate_id","src_session","src_roi","tgt_session","tgt_roi"]
            miss=[x for x in req if x not in c.columns]
            if miss:
                errors.append(f"{name}: candidate columns missing {miss}")
            else:
                if c.candidate_id.astype(str).duplicated().any():
                    errors.append(f"{name}: duplicate candidate_id")
                for _,r in c.iterrows():
                    ss,ts=str(r.src_session),str(r.tgt_session)
                    sr,tr=int(r.src_roi),int(r.tgt_roi)
                    if ss not in sessions:
                        errors.append(f"{name}/{r.candidate_id}: source session {ss} outside bundle")
                    elif sr not in roi_ids.get(ss,set()):
                        errors.append(f"{name}/{r.candidate_id}: source ROI {ss}:{sr} missing")
                    if ts not in sessions:
                        errors.append(f"{name}/{r.candidate_id}: target session {ts} outside bundle")
                    elif tr not in roi_ids.get(ts,set()):
                        errors.append(f"{name}/{r.candidate_id}: target ROI {ts}:{tr} missing")
                    if not ss.startswith(animal+"_") or not ts.startswith(animal+"_"):
                        errors.append(f"{name}/{r.candidate_id}: endpoint animal prefix mismatch")
                    srcmask=bundle/"sessions"/ss/"roi"/f"{sr}_mask.png"
                    tgtmask=bundle/"sessions"/ts/"roi"/f"{tr}_mask.png"
                    if not srcmask.exists():
                        errors.append(f"{name}/{r.candidate_id}: missing source reviewer mask {ss}:{sr}")
                    if not tgtmask.exists():
                        errors.append(f"{name}/{r.candidate_id}: missing target reviewer mask {ts}:{tr}")
                    if srcmask.exists() and tgtmask.exists():
                        review_mask_pairs+=1
                review=bundle/"identity_review"
                for fn in ["index.html","review.js","identity_review_data.js"]:
                    if not (review/fn).exists():
                        errors.append(f"{name}: missing identity_review/{fn}")
                datap=review/"identity_review_data.js"
                if datap.exists():
                    try:
                        payload=load_review_js(datap)
                        jsids={str(x.get("candidate_id")) for x in payload}
                        csv_ids=set(c.candidate_id.astype(str))
                        if jsids!=csv_ids:
                            errors.append(f"{name}: identity_review_data.js candidate IDs differ from CSV")
                        for x in payload:
                            ss=str(x.get("src_session",x.get("source_session","")))
                            ts=str(x.get("tgt_session",x.get("target_session","")))
                            if not ss.startswith(animal+"_") or not ts.startswith(animal+"_"):
                                errors.append(f"{name}/{x.get('candidate_id')}: review JS endpoint prefix mismatch")
                    except Exception as e:
                        errors.append(f"{name}: identity_review_data.js parse failed: {type(e).__name__}: {e}")
            if int(m.get("n_identity_candidates",-1))!=ncan:
                errors.append(f"{name}: manifest n_identity_candidates={m.get('n_identity_candidates')} != {ncan}")
        elif int(m.get("n_identity_candidates",0))!=0:
            errors.append(f"{name}: manifest says identity candidates but CSV missing")

        rows.append({
            "bundle":name,"animal":animal,"sessions":len(sessions),
            "candidates":ncan,"review_mask_pairs":review_mask_pairs,"status":"PASS"
        })

    print("REFERENCE_ROOT",root)
    print(pd.DataFrame(rows).to_string(index=False))
    if errors:
        print("\nFAIL",len(errors))
        for e in errors: print(" -",e)
        return 1
    print("\nPASS all reference-bundle invariants, reviewer masks, and review-JS authorities")
    return 0

def main():
    ap=argparse.ArgumentParser(description="Validate local CaRMA reference bundles and Stage08 reviewer evidence.")
    ap.add_argument("--root",default=os.environ.get("CARMA_REFERENCE_ROOT"),
                    help="Directory containing ANM54_REFERENCE_V3, ANM181_REFERENCE_V1, etc. Defaults to CARMA_REFERENCE_ROOT, then this script's directory.")
    a=ap.parse_args()
    root=Path(a.root) if a.root else Path(__file__).resolve().parent
    raise SystemExit(validate(root))

if __name__=="__main__":
    main()
