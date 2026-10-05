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

function eventActual(){return (EW.hero.actual||[]).map((id,i)=>({step:i+1,event:id,label:eventName(id)}));}
function eventGlobal(){return (EW.hero.global_frequency||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs}));}
function eventAction(){return (EW.hero.action_only||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs,prob_actual:x.prob_actual}));}
function eventMarkov(){return (EW.hero.markov||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs,prob_actual:x.prob_actual}));}
function eventNeural(){return (EW.hero.neural||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs,prob_actual:x.prob_actual}));}
function eventGate(){return (EW.hero.gate||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs,prob_actual:x.prob_actual}));}

function getId(q,mode){return mode==="event"?(q.event??q.top):(q.motif??q.top_motif);}
function getName(q,mode){return q.label||(mode==="event"?eventName(getId(q,mode)):motifName(getId(q,mode)));}
function isMatch(q,a,mode){return q&&a&&Number(getId(q,mode))===Number(getId(a,mode));}
function matchCount(seq,act,mode){
  let n=0,N=Math.min(act.length,seq.length);
  for(let i=0;i<N;i++)if(isMatch(seq[i],act[i],mode))n++;
  return [n,N];
}
function eventSummary(model){return EW.one_step.find(x=>x.model===model)||{};}
function horizonSummary(h){return EW.horizons.find(x=>Number(x.horizon)===Number(h))||{};}

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
    const act=eventActual(),nw=eventNeural(),mk=eventMarkov(),ao=eventAction(),gl=eventGlobal();
    const [nn,nN]=matchCount(nw,act,"event"),[mn,mN]=matchCount(mk,act,"event"),[an,aN]=matchCount(ao,act,"event"),[gn,gN]=matchCount(gl,act,"event");
    const n=eventSummary("Neural world + event head"),m=eventSummary("Event Markov"),a=eventSummary("Action-only"),g=eventSummary("Global frequency"),h5=horizonSummary(5);
    const cards=[
      ["Hero exact steps","Neural "+nn+"/"+nN,"Action "+an+"/"+aN+" · Markov "+mn+"/"+mN+" · Global "+gn+"/"+gN],
      ["One-step accuracy",pct(n.accuracy),"Action "+pct(a.accuracy)+" · Markov "+pct(m.accuracy)+" · Global "+pct(g.accuracy)],
      ["One-step NLL",fmt(n.nll,3),"Linear "+fmt(eventSummary("Full-history linear").nll,3)+" · Markov "+fmt(m.nll,3)],
      ["5-step accuracy",pct(h5.neural_acc),"Action "+pct(h5.action_acc)+" · Markov "+pct(h5.markov_acc)+" · Global "+pct(h5.global_acc)]
    ];
    heroStats.innerHTML=cards.map(c=>'<div class="world-hero-stat"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    return;
  }
  const act=motifActual(),nw=motifNeural(),mk=motifMarkov();
  const [nn,nN]=matchCount(nw,act,"motif"),[mn,mN]=matchCount(mk,act,"motif");
  const best=WM.best_example&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);
  let cards=[
    ["Neural exact future steps",nn+"/"+nN,"top-1 motif matches"],
    ["Markov exact future steps",mn+"/"+mN,"same held-out future"]
  ];
  if(best){
    const s=WM.best_example.summary;
    cards.push(["Future NLL",fmt(s.neural_nll,2)+" vs "+fmt(s.markov_nll,2),"Neural vs Markov · lower is better"]);
    cards.push(["Social-gate Active",pct(s.base_active_any)+" → "+pct(s.gate_active_any),"P(≥1 Active) across 8 steps"]);
  }else{
    cards.push(["Future Active",pct(current.base_active_any)+" → "+pct(current.gate_active_any),"normal → social-gated"]);
    cards.push(["Counterfactual shift",fmt(current.terminal_motif_js,4),"terminal motif JS"]);
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
      {label:"Neural",kind:"neural",seq:eventNeural()},
      {label:"Action-only",kind:"action",seq:eventAction()},
      {label:"Markov",kind:"markov",seq:eventMarkov()},
      {label:"Social-gated",kind:"gated",seq:eventGate()}
    ],"event","Next 8 real event types from the same present");
    return;
  }
  renderStepGrid([
    {label:"Actual",kind:"actual",seq:motifActual()},
    {label:"Neural",kind:"neural",seq:motifNeural()},
    {label:"Markov",kind:"markov",seq:motifMarkov()},
    {label:"Social-gated",kind:"gated",seq:motifGate()}
  ],"motif","Next 8 real behavioral motifs from the same present");
}

function renderMetrics(){
  if(view==="event"){
    const act=eventActual(),nw=eventNeural(),mk=eventMarkov(),gd=eventGate();
    const [nn,nN]=matchCount(nw,act,"event"),[mn,mN]=matchCount(mk,act,"event");
    const n=eventSummary("Neural world + event head"),m=eventSummary("Event Markov"),h3=horizonSummary(3),h5=horizonSummary(5);
    const activeIdx=2;
    const pN=nw.reduce((s,q)=>s+(q.probs?Number(q.probs[activeIdx]||0):0),0)/Math.max(1,nw.length);
    const pG=gd.reduce((s,q)=>s+(q.probs?Number(q.probs[activeIdx]||0):0),0)/Math.max(1,gd.length);
    const cards=[
      ["Prediction gain","Neural "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"exact event-type steps"],
      ["One-step accuracy",pct(n.accuracy)+" vs "+pct(m.accuracy),"Neural event-world vs Event Markov"],
      ["3 / 5-step accuracy",pct(h3.neural_acc)+" / "+pct(h5.neural_acc),"Markov "+pct(h3.markov_acc)+" / "+pct(h5.markov_acc)],
      ["Mean P(Active bout)",pct(pN)+" → "+pct(pG),"normal latent → social-gated latent"]
    ];
    metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    future.innerHTML="<b>How to read this:</b> each card above is one recorded future step. The labels are generated directly from the held-out event-world output; no illustrative trajectories are used.";
    eventNote.innerHTML='<b>Event dictionary.</b> '+EW.notes.taxonomy+'<div class="event-dict">'+EW.dictionary.map(x=>'<span>'+x.event_name+' · n='+Number(x.count).toLocaleString()+'</span>').join("")+'</div>';
    return;
  }
  const tr=current.trajectory,first=tr[0],act=motifActual(),nw=motifNeural(),mk=motifMarkov();
  const [nn,nN]=matchCount(nw,act,"motif"),[mn,mN]=matchCount(mk,act,"motif");
  const cards=[
    ["Prediction gain","Neural "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"exact future motif steps"],
    ["Step-1 P(Active)","Normal "+pct(first.base_p_active)+" · Gated "+pct(first.gate_p_active),"Δ "+fmt(first.delta_p_active,3)],
    ["8-step Active","Normal "+pct(current.base_active_any)+" · Gated "+pct(current.gate_active_any),"Δ "+fmt(current.delta_active_any,3)],
    ["Terminal state shift","Motif JS "+fmt(current.terminal_motif_js,4),"latent RMS "+fmt(current.terminal_latent_rms,3)]
  ];
  metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
  const best=WM.best_example&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);
  future.innerHTML=best
    ? "<b>Why this example:</b> the held-out neural world matches 6 of 8 recorded future motifs while the generative Markov baseline matches 0 of 8. The social-gated counterfactual uses the same real present with social inputs removed."
    : "<b>Alternative held-out example:</b> each step above compares the recorded future with model top-1 predictions from the same real present.";
  eventNote.textContent="";
}

function renderAll(){renderHero();renderSequence();renderMetrics();}
Promise.all([
  fetch("data/world_model.json?v=20261004v4",{cache:"no-store"}).then(r=>r.json()),
  fetch("data/event_world.json?v=20261004v4",{cache:"no-store"}).then(r=>r.json()),
  fetch("data/atlas.json?v=20261004v4",{cache:"no-store"}).then(r=>r.json())
]).then(([wm,ew,a])=>{
  WM=wm;EW=ew;A=a;setupSelect();selectEvent(WM.default_event_frame);
}).catch(e=>{console.error(e);present.textContent="Could not load world-model rollout.";});
})();