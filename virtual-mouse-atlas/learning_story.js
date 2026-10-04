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
fetch("data/learning_story.json").then(r=>r.json()).then(D=>{
  headline.textContent=D.headline;
  const np=D.net_productive,op=D.observe_progression,ac=D.active_conversion,gr=D.graph_rewrite_sri;
  kpis.innerHTML=
    card("Net productive flow",fmt(np.learner.early)+" → "+fmt(np.learner.late),"25/27 learners increase · group ΔΔ P="+ptxt(np.group_change_p),"strong")+
    card("Observe progression",fmt(op.learner.early)+" → "+fmt(op.learner.late),"24/27 learners increase · group ΔΔ P="+ptxt(op.group_change_p),"strong")+
    card("Active conversion",fmt(ac.learner.early)+" → "+fmt(ac.learner.late),"non-learners "+fmt(ac.non_learner.early)+" → "+fmt(ac.non_learner.late)+" · group ΔΔ P="+ptxt(ac.group_change_p))+
    card("Graph rewrite tracks learning","ρ="+fmt(gr.rho,2),"transition JS vs ΔSRI · n="+gr.n+" learners · P="+ptxt(gr.p));

  boundary.innerHTML='<div class="eyebrow">IMPORTANT BOUNDARY</div>'+
    D.boundaries.map(x=>'<p>'+x+'</p>').join("");

  const wo=D.world_stage_aware.learner;
  const tr=D.target_reallocation;
  details.innerHTML=
    '<div class="learning-detail-grid">'+
      '<div><h4>Behavior first</h4><p>The main evidence is model-free: the learner transition graph moves away from abortive returns to Other and toward sustained Observe / Active states.</p></div>'+
      '<div><h4>World-model bridge</h4><p>Against a strong stage-aware event+action+motif Markov baseline, world-model gain stays positive in learners both early ('+fmt(wo.early.mean_gain)+') and late ('+fmt(wo.late.mean_gain)+'); it does not become globally larger late.</p></div>'+
      '<div><h4>Target reallocation</h4><p>Against the stage-agnostic Event Markov, future-Observe gain shifts '+fmt(tr.Observe.early)+' → '+fmt(tr.Observe.late)+' and future-Active gain '+fmt(tr["Active bout"].early)+' → '+fmt(tr["Active bout"].late)+'.</p></div>'+
      '<div><h4>What this supports</h4><p>Learning changes the organization of social-event dynamics; the world model captures that reorganized dynamics, rather than merely exploiting an easier late-stage classification problem.</p></div>'+
    '</div>';
}).catch(e=>{
  console.error(e);
  kpis.innerHTML='<div class="learning-load-error">Learning-stage summary could not be loaded.</div>';
});
})();