(() => {
const sel=document.querySelector("#worldEventSelect"),btn=document.querySelector("#worldReplayBtn");
const video=document.querySelector("#worldRealVideo"),canvas=document.querySelector("#worldFutureMap");
const eventImg=document.querySelector("#worldEventHeatmap"),legend=document.querySelector("#worldLegend"),futureEyebrow=document.querySelector("#worldFutureEyebrow");
const present=document.querySelector("#worldPresentCaption"),future=document.querySelector("#worldFutureCaption"),metrics=document.querySelector("#worldMetrics");
const heroStats=document.querySelector("#worldHeroStats"),strip=document.querySelector("#worldFutureStrip"),eventNote=document.querySelector("#worldEventNote");
const viewToggle=document.querySelector("#worldViewToggle");
if(!sel||!video||!canvas||!strip)return;
let WM=null,EW=null,A=null,current=null,endTime=null,view="motif";

const fmt=(x,d=3)=>Number.isFinite(Number(x))?Number(x).toFixed(d):"n/a";
const pct=x=>Number.isFinite(Number(x))?(100*Number(x)).toFixed(1)+"%":"n/a";
const motifName=id=>{
  const m=A&&A.motifs?A.motifs.find(x=>Number(x.id)===Number(id)):null;
  return m?m.name:("Motif "+id);
};
const eventName=id=>EW&&EW.event_names&&EW.event_names[Number(id)]?EW.event_names[Number(id)]:("Event "+id);

function motifActual(){return current.actual_future||[];}
function motifMarkov(){return current.markov_closed_loop||[];}
function motifNeural(){return (current.trajectory||[]).map(x=>({step:x.step,motif:x.base_top_motif,label:x.base_top_label}));}
function motifGate(){return (current.trajectory||[]).map(x=>({step:x.step,motif:x.gate_top_motif,label:x.gate_top_label}));}

function eventActual(){return (EW.hero.actual||[]).map((id,i)=>({step:i+1,event:id,label:eventName(id)}));}
function eventMarkov(){return (EW.hero.markov||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs}));}
function eventNeural(){return (EW.hero.neural||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs}));}
function eventGate(){return (EW.hero.gate||[]).map((x,i)=>({step:i+1,event:x.top,label:eventName(x.top),probs:x.probs}));}

function matchCount(seq,act,mode){
  let n=0,N=Math.min(act.length,seq.length);
  for(let i=0;i<N;i++){
    const p=mode==="event"?(seq[i].event??seq[i].top):(seq[i].motif??seq[i].top_motif);
    const y=mode==="event"?(act[i].event??act[i].top):(act[i].motif??act[i].top_motif);
    if(Number(p)===Number(y))n++;
  }
  return [n,N];
}
function eventSummary(model){
  return EW.one_step.find(x=>x.model===model)||{};
}
function horizonSummary(h){return EW.horizons.find(x=>Number(x.horizon)===Number(h))||{};}
function setupSelect(){
  sel.innerHTML="";
  WM.top_event_frames.forEach((fr,i)=>{
    const e=WM.events.find(x=>x.event_frame===fr);if(!e)return;
    const o=document.createElement("option");o.value=String(fr);
    if(Number(fr)===Number(WM.default_event_frame))o.textContent="Best combined example · frame "+fr;
    else o.textContent="Alternative "+i+" · frame "+fr+" · ΔActive "+fmt(e.delta_active_any,3);
    sel.appendChild(o);
  });
  sel.value=String(WM.default_event_frame);
}
function seekCurrent(){
  const start=Math.max(0,current.event_time_sec-3),end=current.event_time_sec+5;endTime=end;
  const seek=()=>{video.currentTime=start;video.play().catch(()=>{});};
  if(video.readyState>=1)seek(); else video.addEventListener("loadedmetadata",seek,{once:true});
}
function selectEvent(fr){
  current=WM.events.find(x=>x.event_frame===Number(fr))||WM.events[0];
  seekCurrent();
  present.innerHTML="<b>Observed present:</b> frame "+current.event_frame+" · t="+fmt(current.event_time_sec,1)+" s · "+
    (current.actual_action?"Observe":"No-observe")+" · outcome "+current.actual_outcome+" · "+motifName(current.current_motif)+".";
  renderAll();
}
function setView(v){
  view=v;
  if(view==="event"){
    current=WM.events.find(x=>Number(x.event_frame)===Number(WM.default_event_frame))||WM.events[0];
    sel.value=String(WM.default_event_frame);seekCurrent();
  }
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
    const n=eventSummary("Neural world + event head"),m=eventSummary("Event Markov"),h5=horizonSummary(5);
    const cards=[
      ["Neural exact event steps",nn+"/"+nN,"top-1 Observe/bout matches"],
      ["Event Markov exact steps",mn+"/"+mN,"same held-out future"],
      ["One-step NLL",fmt(n.nll,3)+" vs "+fmt(m.nll,3),"Neural event-world vs Event Markov"],
      ["5-step accuracy",pct(h5.neural_acc)+" vs "+pct(h5.markov_acc),"27 held-out animals"]
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

function sequenceRow(label,kind,seq,actual,mode){
  let chips="",N=Math.min(8,seq.length||8);
  for(let i=0;i<N;i++){
    const q=seq[i]||{};
    const id=mode==="event"?(q.event??q.top):(q.motif??q.top_motif);
    const name=q.label||(mode==="event"?eventName(id):motifName(id));
    let cls="future-chip",mark="";
    if(kind!=="actual"&&actual[i]){
      const y=mode==="event"?(actual[i].event??actual[i].top):(actual[i].motif??actual[i].top_motif);
      if(Number(id)===Number(y)){cls+=" match";mark="✓";}else{cls+=" miss";mark="×";}
    }
    chips+='<div class="'+cls+'"><span class="step">'+(i+1)+'</span><span class="motif">'+name+'</span><span class="hit">'+mark+'</span></div>';
  }
  return '<div class="future-row '+kind+'"><div class="future-row-label">'+label+'</div><div class="future-row-chips">'+chips+'</div></div>';
}
function renderSequence(){
  if(view==="event"){
    const act=eventActual(),mk=eventMarkov(),nw=eventNeural(),gd=eventGate();
    strip.innerHTML=
      '<div class="future-strip-head"><span>Same present</span><strong>→ next 8 Observe / bout events</strong><span>✓ exact top-1 event match</span></div>'+
      sequenceRow("Actual","actual",act,act,"event")+
      sequenceRow("Event Markov","markov",mk,act,"event")+
      sequenceRow("Neural event-world","neural",nw,act,"event")+
      sequenceRow("Social-gated","gated",gd,act,"event");
    return;
  }
  const act=motifActual(),mk=motifMarkov(),nw=motifNeural(),gd=motifGate();
  strip.innerHTML=
    '<div class="future-strip-head"><span>Same present</span><strong>→ next 8 behavioral motifs</strong><span>✓ exact top-1 match to actual</span></div>'+
    sequenceRow("Actual","actual",act,act,"motif")+
    sequenceRow("Generative Markov","markov",mk,act,"motif")+
    sequenceRow("Neural world","neural",nw,act,"motif")+
    sequenceRow("Social-gated","gated",gd,act,"motif");
}

function renderMetrics(){
  if(view==="event"){
    const act=eventActual(),nw=eventNeural(),mk=eventMarkov(),gd=eventGate();
    const [nn,nN]=matchCount(nw,act,"event"),[mn,mN]=matchCount(mk,act,"event");
    const n=eventSummary("Neural world + event head"),m=eventSummary("Event Markov"),h3=horizonSummary(3),h5=horizonSummary(5);
    const activeIdx=4;
    const pN=nw.reduce((s,q)=>s+(q.probs?q.probs[activeIdx]:0),0)/Math.max(1,nw.length);
    const pG=gd.reduce((s,q)=>s+(q.probs?q.probs[activeIdx]:0),0)/Math.max(1,gd.length);
    const cards=[
      ["Prediction gain","Neural "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"exact event-type steps"],
      ["One-step accuracy",pct(n.accuracy)+" vs "+pct(m.accuracy),"Neural event-world vs Event Markov"],
      ["3 / 5-step accuracy",pct(h3.neural_acc)+" / "+pct(h5.neural_acc),"Markov "+pct(h3.markov_acc)+" / "+pct(h5.markov_acc)],
      ["Mean P(Active bout)",pct(pN)+" → "+pct(pG),"normal latent → social-gated latent"]
    ];
    metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    future.innerHTML="<b>Event-state version:</b> the same frozen predictive state is read out as biologically named Observe / feeding-bout events rather than 12 geometric motifs.";
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
    ? "<b>Why this example:</b> the neural world assigns substantially more probability to the recorded 8-step future than the generative Markov baseline, while social-information removal also lowers future Active probability."
    : "<b>Alternative example:</b> compare the recorded future with the two generative predictions and the social-gated counterfactual.";
  eventNote.textContent="";
}

function drawFuture(){
  if(view==="event"){
    canvas.hidden=true;eventImg.hidden=false;legend.hidden=true;
    futureEyebrow.textContent="EVENT-STATE FUTURE · SAME HELD-OUT PRESENT";
    return;
  }
  canvas.hidden=false;eventImg.hidden=true;legend.hidden=false;futureEyebrow.textContent="FOUR FUTURES FROM THE SAME PRESENT";
  if(!A||!current)return;
  const r=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1,W=Math.max(320,r.width),H=Math.max(260,r.height);
  canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);
  const c=canvas.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);c.clearRect(0,0,W,H);c.fillStyle="#fff";c.fillRect(0,0,W,H);
  const all=A.framewise||[],xs=A.motifs.map(m=>m.x),ys=A.motifs.map(m=>m.y);
  for(const q of current.trajectory){xs.push(q.base_x,q.gate_x);ys.push(q.base_y,q.gate_y);}
  for(const q of motifActual()){xs.push(q.x);ys.push(q.y);}
  for(const q of motifMarkov()){xs.push(q.x);ys.push(q.y);}
  let x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
  const mx=(x1-x0)*.10+4,my=(y1-y0)*.10+4;x0-=mx;x1+=mx;y0-=my;y1+=my;
  const sc=Math.min((W-50)/(x1-x0),(H-50)/(y1-y0)),ox=(W-(x1-x0)*sc)/2,oy=(H-(y1-y0)*sc)/2;
  const xy=(x,y)=>[ox+(x-x0)*sc,oy+(y1-y)*sc];
  c.globalAlpha=.08;c.fillStyle="#6d7377";
  for(let i=0;i<all.length;i+=22){const q=all[i],[x,y]=xy(q[0],q[1]);c.fillRect(x,y,1.1,1.1);}
  c.globalAlpha=1;c.font="600 10px system-ui";c.textAlign="center";
  for(const m of A.motifs){const [x,y]=xy(m.x,m.y);c.fillStyle="#888";c.fillText(String(m.id),x,y);}
  const cur=A.framewise[current.event_frame]||null;let start=null;
  if(cur){start=xy(cur[0],cur[1]);c.fillStyle="#111";c.beginPath();c.arc(start[0],start[1],5,0,Math.PI*2);c.fill();c.fillText("present",start[0],start[1]-11);}
  function draw(raw,stroke,width,dash){
    const pts=raw.map(q=>xy(q.x,q.y));if(!pts.length)return;
    c.strokeStyle=stroke;c.fillStyle=stroke;c.lineWidth=width;c.setLineDash(dash||[]);c.beginPath();
    if(start)c.moveTo(start[0],start[1]);else c.moveTo(pts[0][0],pts[0][1]);
    pts.forEach(p=>c.lineTo(p[0],p[1]));c.stroke();c.setLineDash([]);
    pts.forEach((p,i)=>{c.beginPath();c.arc(p[0],p[1],3.7,0,Math.PI*2);c.fill();c.fillStyle="#111";c.font="600 8px system-ui";c.fillText(String(i+1),p[0],p[1]-7);c.fillStyle=stroke;});
  }
  draw(motifActual(),"#111",2.3,[3,3]);
  draw(motifMarkov().map(q=>({x:q.x,y:q.y})),"#777",2.3,[7,4]);
  draw(current.trajectory.map(q=>({x:q.base_x,y:q.base_y})),"#276fbf",3,[]);
  draw(current.trajectory.map(q=>({x:q.gate_x,y:q.gate_y})),"#c84b35",3,[]);
}
function renderAll(){renderHero();renderSequence();renderMetrics();drawFuture();}
window.addEventListener("resize",()=>{if(current)drawFuture();});
Promise.all([
  fetch("data/world_model.json").then(r=>r.json()),
  fetch("data/event_world.json").then(r=>r.json()),
  fetch("data/atlas.json").then(r=>r.json())
]).then(([wm,ew,a])=>{
  WM=wm;EW=ew;A=a;setupSelect();selectEvent(WM.default_event_frame);
}).catch(e=>{console.error(e);present.textContent="Could not load world-model rollout.";});
})();