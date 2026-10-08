from pathlib import Path
R=Path(__file__).resolve().parents[1]
warnings="> **SOURCE CORRECTION (2026-10-07; v126):** Earlier references below to “real action-bout DA” or genuine real-bout social-credit coding are superseded. The field DA_ActionBout_AUCperSec measures an extended post-anchor model interval (median 28.85 s), not the actual observed 2.40-s observation bout. The historical n=1371 9/9 model-comparator result is preserved solely as a documented prior estimate. See [source-level correction and current 821-event triple-readout results](VTA_TRUE_BOUT_SOURCE_CORRECTION_v126_20261007.md). The frozen Early/Middle estimates and separate JAWS causal experiment have independent statistical contracts.\n\n"
for n in ["VTA_EARLY_MIDDLE_POST_CAUSAL_AUTHORITY_v113_20261007.md","SLM_DOPAMINE_MULTIPERSPECTIVE_AUDIT_v1_20261006.md"]:
 p=R/"docs"/n
 if not p.exists():print("MISSING",n);continue
 s=p.read_text(encoding="utf-8")
 if "SOURCE CORRECTION (2026-10-07; v126)" not in s:
  p.write_text(warnings+s,encoding="utf-8")
  print("FLAGGED",n)
