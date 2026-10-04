(() => {
const wrap=document.querySelector("#learning-story");
if(!wrap)return;
const kpis=document.querySelector("#learningKpis");
const headline=document.querySelector("#learningHeadline");
const boundary=document.querySelector("#learningBoundary");
const details=document.querySelector("#learningDetails");
const fmt=(x,d=3)=>Number.isFinite(Number(x))?Number(x).toFixed(d):"n/a";
const ptxt=x=>Number(x)<.001?Number(x).toExponential(1):Number(x).toFixed(3);

function card(title,value,note,cls){
  cls=cls||"";
  return '<article class="learning-kpi '+cls+'"><div class="k">'+title+'</div><div class="v">'+value+'</div><div class="d">'+note+'</div></article>';
}
fetch("data/learning_story.json?v=20261004v3",{cache:"no-store"}).then(r=>r.json()).then(D=>{
  headline.textContent=D.headline;
  const R=D.robustness||{};
  const all=(R.continuous_all||{});
  const common=(R.common_cohorts||{});
  const glm=(R.observe_active_glm||{});
  const gr=D.graph_rewrite_sri||{};
  const wo=(D.world_stage_aware||{}).learner||{};

  kpis.innerHTML=
    card("Continuous net productive trend",
      "24/27 ↑",
      "all learners · P="+ptxt((all.net_productive_learner||{}).p)+" · common cohorts 11/13 ↑, P="+ptxt((common.net_learner||{}).p),"strong")+
    card("Observe→Active learning interaction",
      fmt(glm.learner_D1)+" → "+fmt(glm.learner_D14),
      "learners; non-learners "+fmt(glm.nonlearner_D1)+" → "+fmt(glm.nonlearner_D14)+" · cohort-matched P="+ptxt(glm.interaction_p),"strong")+
    card("Graph rewrite tracks learning",
      "ρ="+fmt(gr.rho,2),
      "transition JS vs ΔSRI · n="+gr.n+" learners · P="+ptxt(gr.p))+
    card("World model > stage-aware Markov",
      "+"+fmt((wo.early||{}).mean_gain)+" / +"+fmt((wo.late||{}).mean_gain),
      "early / late NLL gain · 22/27 and 23/27 learners positive");

  boundary.innerHTML='<div class="eyebrow">IMPORTANT BOUNDARY</div>'+
    (D.boundaries||[]).map(x=>'<p>'+x+'</p>').join("");

  const tr=D.target_reallocation||{};
  details.innerHTML=
    '<div class="learning-detail-grid">'+
      '<div><h4>Continuous rather than arbitrary bins</h4><p>Across all 14 training days, learner net-productive flow, Observe progression, and Observe→Active probability rise continuously. The same within-learner trends remain significant in the three cohorts represented in both groups.</p></div>'+
      '<div><h4>Cohort-matched interaction</h4><p>In Chemo / OXT / SF-Gcamp animals, clustered logistic regression gives a training×learner interaction for next Active after Observe of coefficient '+fmt(glm.interaction_coef,3)+' (P='+ptxt(glm.interaction_p)+'). Composite cross-group interactions are weaker after cohort restriction.</p></div>'+
      '<div><h4>World-model bridge</h4><p>Against a stage-aware event+action+motif Markov baseline, the world model adds information both early ('+fmt((wo.early||{}).mean_gain)+') and late ('+fmt((wo.late||{}).mean_gain)+'). The gain is not larger late.</p></div>'+
      '<div><h4>Target reallocation</h4><p>Against a stage-agnostic Event Markov, future-Observe gain shifts '+fmt((tr.Observe||{}).early)+' → '+fmt((tr.Observe||{}).late)+' and future-Active gain '+fmt((tr["Active bout"]||{}).early)+' → '+fmt((tr["Active bout"]||{}).late)+'. Treat this as computational support, not the primary learning interaction.</p></div>'+
    '</div>';
}).catch(e=>{
  console.error(e);
  kpis.innerHTML='<div class="learning-load-error">Learning-stage summary could not be loaded.</div>';
});
})();