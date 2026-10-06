from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets"

maps={
"SOE_behavioral_foundations_v52":"SOE_behavioral_foundations_v64",
"SOE_adaptive_social_information_value_v52":"SOE_adaptive_social_information_value_v64",
"SOE_SLM_default_hierarchy_v53":"SOE_SLM_default_hierarchy_v64",
"SOE_feed_conversion_learning_v53":"SOE_feed_conversion_learning_v64",
"SOE_ArtificialSLM_causal_double_dissociation_v52":"SOE_ArtificialSLM_causal_double_dissociation_v64",
"SOE_JAWS_credit_logic_v53":"SOE_JAWS_credit_logic_v64",
"SOE_SWM_functional_bridge_v55":"SOE_SWM_functional_bridge_v64",
"SOE_generalization_comparator_hierarchy_v55":"SOE_generalization_comparator_hierarchy_v64",
"SOE_crossspecies_comparator_hierarchy_v52":"SOE_crossspecies_comparator_hierarchy_v64",
}

def restore_quant_mobile(s):
    # For every figure, restore the mobile source to the actual quantitative mobile PNG
    # derived from the figure's visible img source whenever that asset exists.
    def repl(m):
        block=m.group(0)
        im=re.search(r'<img[^>]+src="assets/([^"]+\.png)"',block)
        src=re.search(r'<source[^>]+srcset="assets/([^"]+)"',block)
        if not im or not src: return block
        stem=im.group(1)[:-4]
        cand=f"{stem}_mobile.png"
        if (A/cand).exists():
            block=block[:src.start(1)]+cand+block[src.end(1):]
        return block
    return re.sub(r'<figure\b.*?</figure>',repl,s,flags=re.S)

for fn in ["index.html","index-zh.html"]:
    p=ROOT/fn
    s=p.read_text(encoding="utf-8")
    s=restore_quant_mobile(s)
    for old,new in maps.items():
        s=s.replace(f"assets/{old}.png",f"assets/{new}.png")
        s=s.replace(f"assets/{old}_mobile.png",f"assets/{new}_mobile.png")
    s=s.replace(" On mobile the image is simplified for readability; tap it for the full quantitative panel.","")
    s=s.replace(" 手机端显示简化摘要，点图可打开完整定量 panel。","")
    p.write_text(s,encoding="utf-8")

print("restored all direct quantitative mobile plots; upgraded nine main figures to V64")
