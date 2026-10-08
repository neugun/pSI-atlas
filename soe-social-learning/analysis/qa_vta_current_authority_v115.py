# -*- coding: utf-8 -*-
"""Run the current VTA authority checks in one place.

Use this after any VTA page rebuild. Historical patch scripts are not authority;
the current page must satisfy all of these checks simultaneously.
"""
from pathlib import Path
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
QAS = [
    "qa_vta_matched_epoch_v158.py",
    "qa_vta_source_outcome_v149.py",
    "qa_vta_true_obs_authority_v128.py",
    "qa_vta_causal_spine_v114.py",
    "qa_vta_credit_precision_v112.py",
    "qa_vta_axis_metrics_v110.py",
    "qa_vta_signal_directionality_v108.py",
    "qa_vta_evidence_hierarchy_v106.py",
    "qa_vta_rawrecon_v103.py",
    "qa_vta_story_rebuild_v100.py",
    "qa_model_clarity_v67.py",
]

for qa in QAS:
    print(f"\n=== {qa} ===")
    r = subprocess.run([sys.executable, str(HERE / qa)])
    if r.returncode:
        raise SystemExit(r.returncode)

print("\nCURRENT VTA AUTHORITY: ALL CHECKS PASS")
