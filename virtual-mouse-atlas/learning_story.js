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
  return '<article class="learning-kpi '+(cls||"")+'"><div class="k">'+title+'</div><div class="v">'+value+'</div><div class="d">'+note+'</div></article>';
}
fetch("data/learning_story.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json()).then(D=>{
  headline.textContent=D.headline;
  const oa=D.observe_to_active||{},uo=D.unrewarded_to_observe||{},slm=D.slm_world_model||{};
  kpis.innerHTML=
    card("Observe → Active bout",
      fmt((oa.learner||{}).early)+" → "+fmt((oa.learner||{}).late),
      (oa.learner||{}).positive+"/27 learners increase · P="+ptxt((oa.learner||{}).p),"strong")+
    card("Cohort-matched interaction",
      fmt(((oa.predicted||{}).learner||{}).D1)+" → "+fmt(((oa.predicted||{}).learner||{}).D14),
      "learner predicted P(Active|Observe) · training×learner P="+ptxt((oa.clustered_interaction||{}).p),"strong")+
    card("Unrewarded bout → Observe",
      fmt((uo.learner||{}).early)+" → "+fmt((uo.learner||{}).late),
      (uo.learner||{}).positive+"/27 learners increase · P="+ptxt((uo.learner||{}).p))+
    card("SLM World Model",
      pct(slm.accuracy)+" · NLL "+fmt(slm.nll),
      "5-event held-out · "+slm.nll_better_animals+"/27 lower NLL than full-history linear · P="+ptxt(slm.p));

  boundary.innerHTML='<div class="eyebrow">IMPORTANT BOUNDARY</div>'+
    (D.boundaries||[]).map(x=>'<p>'+x+'</p>').join("");

  details.innerHTML=
    '<div class="learning-detail-grid">'+
      '<div><h4>One factorized 5-event language</h4><p>'+D.definition+' The displayed transition matrices and the 5-event SLM benchmark now use the same semantic event system.</p></div>'+
      '<div><h4>Learning changes conversion</h4><p>Learners increase P(Active bout | Observe) from '+fmt((oa.learner||{}).early)+' to '+fmt((oa.learner||{}).late)+', while non-learners move from '+fmt((oa.nonlearner||{}).early)+' to '+fmt((oa.nonlearner||{}).late)+'.</p></div>'+
      '<div><h4>Learning changes resampling</h4><p>After an unrewarded bout, learner P(next Observe) rises from '+fmt((uo.learner||{}).early)+' to '+fmt((uo.learner||{}).late)+'. This is a separate transition from Observe→Active and is visible in the 5×5 graph.</p></div>'+
      '<div><h4>Social Learning World Model</h4><p>The Social Learning World Model (SLM World Model) reaches '+pct(slm.accuracy)+' held-out 5-event accuracy and NLL '+fmt(slm.nll)+'. Its advantage over full-history linear is concentrated in predicting the sampling action rather than the bout-outcome classifier.</p></div>'+
    '</div>';
}).catch(e=>{
  console.error(e);
  kpis.innerHTML='<div class="learning-load-error">Learning-stage summary could not be loaded.</div>';
});
function pct(x){return Number.isFinite(Number(x))?(100*Number(x)).toFixed(1)+"%":"n/a";}
})();