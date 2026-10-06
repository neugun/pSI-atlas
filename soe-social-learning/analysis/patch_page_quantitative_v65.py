from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
maps={
"SOE_agent_sufficiency_hierarchy_v56":"SOE_agent_sufficiency_hierarchy_v65",
"SOE_VisualBlock_information_closure_v52":"SOE_VisualBlock_information_closure_v65",
"SOE_crossspecies_evidence_hierarchy_v55":"SOE_crossspecies_evidence_hierarchy_v65",
"SOE_DA_temporal_logic_v53":"SOE_DA_temporal_logic_v65",
}
for fn in ["index.html","index-zh.html"]:
 p=ROOT/fn;s=p.read_text(encoding="utf-8")
 for old,new in maps.items():
  s=s.replace(f"assets/{old}.png",f"assets/{new}.png")
  s=s.replace(f"assets/{old}_mobile.png",f"assets/{new}_mobile.png")
 p.write_text(s,encoding="utf-8")
print("upgraded agent, VTA, Visual Block and cross-species evidence to V65 quantitative figures")
