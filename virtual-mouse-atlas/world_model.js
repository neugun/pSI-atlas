(() => {
const sel=document.querySelector("#worldEventSelect"),btn=document.querySelector("#worldReplayBtn");
const video=document.querySelector("#worldRealVideo");
const present=document.querySelector("#worldPresentCaption"),future=document.querySelector("#worldFutureCaption"),metrics=document.querySelector("#worldMetrics");
const heroStats=document.querySelector("#worldHeroStats"),strip=document.querySelector("#worldFutureStrip"),eventNote=document.querySelector("#worldEventNote");
const viewToggle=document.querySelector("#worldViewToggle");
if(!sel||!video||!strip)return;
let WM=null,EW=null,A=null,current=null,endTime=null,view="motif";

const fmt=(x,d=3)=>Number.isFinite(Number(x))?Number(x).toFixed(d):"n/a";
const pct=x=>Number.isFinite(Number(x))?(100*Number(x)).toFixed(1)+"%":"n/a";
const motifName=id=>{
  const m=A&&A.motifs?A.motifs.find(x=>Number(x.id)===Number(id)):null;
  return m?m.name:("Motif "+id);
};
const eventName=id=>EW&&EW.event_names&&EW.event_names[Number(id)]?EW.event_names[Number(id)]:("Event "+id);

function isBestMotif(){return WM&&WM.best_example&&current&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);}
function motifActual(){
  if(isBestMotif())return WM.best_example.steps.map(x=>({step:x.step,motif:x.actual_motif,label:x.actual_label}));
  return current.actual_future||[];
}
function motifMarkov(){
  if(isBestMotif())return WM.best_example.steps.map(x=>({step:x.step,motif:x.markov_top,label:x.markov_label,prob_actual:x.p_actual_markov}));
  return current.markov_closed_loop||[];
}
function motifNeural(){
  if(isBestMotif())return WM.best_example.steps.map(x=>({step:x.step,motif:x.neural_top,label:x.neural_label,prob_actual:x.p_actual_neural}));
  return (current.trajectory||[]).map(x=>({step:x.step,motif:x.base_top_motif,label:x.base_top_label}));
}
function motifGate(){
  if(isBestMotif())return WM.best_example.steps.map(x=>({step:x.step,motif:x.gate_top,label:x.gate_label,prob_actual:x.p_actual_gate}));
  return (current.trajectory||[]).map(x=>({step:x.step,motif:x.gate_top_motif,label:x.gate_top_label}));
}

function eventActual(){return EW&&EW.hero&&EW.hero.actual?EW.hero.actual:[];}
function eventMarkov(){return EW&&EW.hero&&EW.hero.markov?EW.hero.markov:[];}
function eventNeural(){return EW&&EW.hero&&EW.hero.neural?EW.hero.neural:[];}
function eventGate(){return EW&&EW.hero&&EW.hero.gate?EW.hero.gate:[];}

function getId(q,mode){return mode==="event"?(q.event??q.top):(q.motif??q.top_motif);}
function getName(q,mode){return q.label||(mode==="event"?eventName(getId(q,mode)):motifName(getId(q,mode)));}
function isMatch(q,a,mode){return q&&a&&Number(getId(q,mode))===Number(getId(a,mode));}
function matchCount(seq,act,mode){
  let n=0,N=Math.min(act.length,seq.length);
  for(let i=0;i<N;i++)if(isMatch(seq[i],act[i],mode))n++;
  return [n,N];
}
function eventSummary(model){return (EW.model_summary||[]).find(x=>x.model===model)||{};}
function eventTest(comparator){return (EW.paired_tests||[]).find(x=>x.comparator===comparator)||{};}

function setupSelect(){
  sel.innerHTML="";
  WM.top_event_frames.forEach((fr,i)=>{
    const e=WM.events.find(x=>x.event_frame===fr);if(!e)return;
    const o=document.createElement("option");o.value=String(fr);
    o.textContent=Number(fr)===Number(WM.default_event_frame)
      ?"Best motif example · frame "+fr
      :"Alternative "+i+" · frame "+fr+" · ΔActive "+fmt(e.delta_active_any,3);
    sel.appendChild(o);
  });
  sel.value=String(WM.default_event_frame);
}
function seekCurrent(){
  const start=Math.max(0,current.event_time_sec-3),end=current.event_time_sec+5;endTime=end;
  const seek=()=>{video.currentTime=start;video.play().catch(()=>{});};
  if(video.readyState>=1)seek(); else video.addEventListener("loadedmetadata",seek,{once:true});
}
function renderPresent(){
  present.innerHTML="<b>Observed present:</b> frame "+current.event_frame+" · t="+fmt(current.event_time_sec,1)+" s · "+
    (current.actual_action?"Observe":"No-observe")+" · outcome "+current.actual_outcome+" · "+motifName(current.current_motif)+".";
}
function selectEvent(fr){
  current=WM.events.find(x=>x.event_frame===Number(fr))||WM.events[0];
  seekCurrent();renderPresent();renderAll();
}
function setView(v){
  view=v;
  const fr=view==="event"
    ? Number(EW&&EW.hero?EW.hero.frame:WM.default_event_frame)
    : Number(WM.default_event_frame);
  current=WM.events.find(x=>Number(x.event_frame)===fr)||WM.events[0];
  sel.value=String(fr);seekCurrent();renderPresent();
  if(viewToggle)viewToggle.querySelectorAll("button").forEach(b=>b.classList.toggle("active",b.dataset.view===view));
  sel.disabled=view==="event";btn.disabled=view==="event";
  renderAll();
}
video.addEventListener("timeupdate",()=>{if(endTime!==null&&video.currentTime>=endTime)video.pause();});
btn.onclick=()=>selectEvent(sel.value);
sel.onchange=()=>{if(view==="event")setView("motif");selectEvent(sel.value);};
if(viewToggle)viewToggle.addEventListener("click",e=>{const b=e.target.closest("button[data-view]");if(b)setView(b.dataset.view);});

function renderHero(){
  if(view==="event"){
    const act=eventActual(),nw=eventNeural(),mk=eventMarkov();
    const [nn,nN]=matchCount(nw,act,"event"),[mn,mN]=matchCount(mk,act,"event");
    const n=eventSummary("Neural social world"),lin=eventSummary("Full-history linear"),m=eventSummary("History Markov"),g=eventSummary("Global phase");
    const t=eventTest("Full-history linear");
    const cards=[
      ["Closed-loop hero","SWM "+nn+"/"+nN,"History Markov "+mn+"/"+mN],
      ["5-event accuracy",pct(n.event5_acc),"Linear "+pct(lin.event5_acc)+" · Markov "+pct(m.event5_acc)+" · Global "+pct(g.event5_acc)],
      ["5-event NLL",fmt(n.event5_nll,3),"Linear "+fmt(lin.event5_nll,3)+" · Markov "+fmt(m.event5_nll,3)+" · Global "+fmt(g.event5_nll,3)],
      ["SWM vs linear",t.neural_better+"/27","lower NLL · P="+Number(t.p_one_sided).toExponential(1)]
    ];
    heroStats.innerHTML=cards.map(c=>'<div class="world-hero-stat"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    return;
  }
  const act=motifActual(),nw=motifNeural(),mk=motifMarkov();
  const [nn,nN]=matchCount(nw,act,"motif"),[mn,mN]=matchCount(mk,act,"motif");
  const best=WM.best_example&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);
  let cards=[
    ["SWM exact future steps",nn+"/"+nN,"top-1 motif matches"],
    ["Markov exact future steps",mn+"/"+mN,"same held-out future"]
  ];
  if(best){
    const s=WM.best_example.summary;
    cards.push(["Future NLL",fmt(s.neural_nll,2)+" vs "+fmt(s.markov_nll,2),"SWM vs Markov · lower is better"]);
    cards.push(["Population social control","0.620 → 0.561 / 0.572","efficacy AUC · matched replacement / no-social retrain"]);
  }else{
    cards.push(["Population efficacy AUC","0.620","strict same-state ΔActive"]);
    cards.push(["Social dependence","26/27","drop under matched replacement and no-social retrain"]);
  }
  heroStats.innerHTML=cards.map(c=>'<div class="world-hero-stat"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
}

function modelLine(label,kind,q,a,mode){
  const match=kind==="actual"?"":(isMatch(q,a,mode)?" ✓":" ×");
  const cls=kind==="actual"?"":" "+(isMatch(q,a,mode)?"match":"miss");
  const pr=kind!=="actual"&&Number.isFinite(Number(q.prob_actual))
    ? '<span class="future-model-prob">P(actual) '+pct(q.prob_actual)+'</span>' : '';
  return '<div class="future-model-line '+kind+cls+'><span class="future-model-name">'+label+'</span><span class="future-model-value">'+getName(q,mode)+pr+'</span><span class="future-model-hit">'+match+'</span></div>';
}
function renderStepGrid(rows,mode,title){
  const actual=rows.find(r=>r.kind==="actual").seq;
  const N=Math.min(8,...rows.map(r=>r.seq.length));
  let cards="";
  for(let i=0;i<N;i++){
    cards+='<article class="future-step-card"><div class="future-step-number">Step '+(i+1)+'</div>';
    for(const r of rows)cards+=modelLine(r.label,r.kind,r.seq[i],actual[i],mode);
    cards+='</article>';
  }
  strip.innerHTML='<div class="future-strip-head"><strong>'+title+'</strong><span>✓ exact top-1 match to the recorded future</span></div><div class="future-step-grid">'+cards+'</div>';
}
function renderSequence(){
  if(view==="event"){
    renderStepGrid([
      {label:"Actual",kind:"actual",seq:eventActual()},
      {label:"SWM",kind:"neural",seq:eventNeural()},
      {label:"History Markov",kind:"markov",seq:eventMarkov()}
    ],"event","Next 8 semantic events = 4 action→bout trials from the same present");
    return;
  }
  renderStepGrid([
    {label:"Actual",kind:"actual",seq:motifActual()},
    {label:"SWM",kind:"neural",seq:motifNeural()},
    {label:"Markov",kind:"markov",seq:motifMarkov()}
  ],"motif","Next 8 real behavioral motifs from the same present");
}

function renderMetrics(){
  if(view==="event"){
    const act=eventActual(),nw=eventNeural(),mk=eventMarkov();
    const [nn,nN]=matchCount(nw,act,"event"),[mn,mN]=matchCount(mk,act,"event");
    const n=eventSummary("Neural social world"),lin=eventSummary("Full-history linear"),m=eventSummary("History Markov");
    const cards=[
      ["Closed-loop sequence","SWM "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"exact semantic-event steps"],
      ["Sampling action NLL",fmt(n.action_nll,3)+" vs "+fmt(lin.action_nll,3),"SWM vs full-history linear"],
      ["Bout outcome NLL",fmt(n.outcome_nll,3)+" vs "+fmt(lin.outcome_nll,3),"linear is slightly better here"],
      ["Aggregate 5-event","Acc "+pct(n.event5_acc)+" · NLL "+fmt(n.event5_nll,3),"Markov "+pct(m.event5_acc)+" · "+fmt(m.event5_nll,3)]
    ];
    metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    future.innerHTML="<b>How to read this:</b> odd steps are the pre-bout sampling state (Other or Observe); even steps are the subsequent bout outcome (Unrewarded, Active, or Passive).";
    eventNote.innerHTML='<b>Five-event dictionary.</b> '+EW.definition+'<div class="event-dict">'+EW.dictionary.map(x=>'<span>'+x.event_name+' · n='+Number(x.count).toLocaleString()+'</span>').join("")+'</div>';
    return;
  }
  const act=motifActual(),nw=motifNeural(),mk=motifMarkov();
  const [nn,nN]=matchCount(nw,act,"motif"),[mn,mN]=matchCount(mk,act,"motif");
  const cards=[
    ["Prediction gain","SWM "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"exact future motif steps"],
    ["Observe efficacy","AUC 0.620","strict same-state ΔActive · 27 held-out animals"],
    ["Matched social replacement","0.561","26/27 efficacy AUC drop · P=1.49×10⁻⁸"],
    ["No-social retrain","0.572","26/27 efficacy AUC drop · P=2.29×10⁻⁶"]
  ];
  metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
  const best=WM.best_example&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);
  future.innerHTML=best
    ? "<b>Why this example:</b> this deliberately selected held-out example is the clearest rollout visualization: SWM matches 6 of 8 recorded future motifs while the generative Markov baseline matches 0 of 8. Population-level held-animal results are reported below and are the inferential authority."
    : "<b>Alternative held-out example:</b> each step above compares the recorded future with model top-1 predictions from the same real present.";
  eventNote.textContent="";
}

function renderAll(){renderHero();renderSequence();renderMetrics();}
Promise.all([
  fetch("data/world_model.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json()),
  fetch("data/event5_world.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json()),
  fetch("data/atlas.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json())
]).then(([wm,ew,a])=>{
  WM=wm;EW=ew;A=a;setupSelect();selectEvent(WM.default_event_frame);
}).catch(e=>{console.error(e);present.textContent="Could not load world-model rollout.";});
})();

