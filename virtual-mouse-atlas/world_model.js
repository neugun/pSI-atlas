(() => {
const sel=document.querySelector("#worldEventSelect"),btn=document.querySelector("#worldReplayBtn");
const video=document.querySelector("#worldRealVideo"),canvas=document.querySelector("#worldFutureMap");
const present=document.querySelector("#worldPresentCaption"),future=document.querySelector("#worldFutureCaption"),metrics=document.querySelector("#worldMetrics");
const heroStats=document.querySelector("#worldHeroStats"),strip=document.querySelector("#worldFutureStrip");
if(!sel||!video||!canvas||!strip)return;
let WM=null,A=null,current=null,endTime=null;

const fmt=(x,d=3)=>Number.isFinite(Number(x))?Number(x).toFixed(d):"n/a";
const pct=x=>Number.isFinite(Number(x))?(100*Number(x)).toFixed(1)+"%":"n/a";
const motifName=id=>{
  const m=A&&A.motifs?A.motifs.find(x=>Number(x.id)===Number(id)):null;
  return m?m.name:("Motif "+id);
};
function actualSeq(){return current.actual_future||[];}
function markovSeq(){return current.markov_closed_loop||[];}
function neuralSeq(){return (current.trajectory||[]).map(x=>({step:x.step,motif:x.base_top_motif,label:x.base_top_label}));}
function gatedSeq(){return (current.trajectory||[]).map(x=>({step:x.step,motif:x.gate_top_motif,label:x.gate_top_label}));}
function matchCount(seq){
  const act=actualSeq();let n=0,N=Math.min(act.length,seq.length);
  for(let i=0;i<N;i++){const mid=seq[i].motif??seq[i].top_motif;if(Number(mid)===Number(act[i].motif))n++;}
  return [n,N];
}
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
function selectEvent(fr){
  current=WM.events.find(x=>x.event_frame===Number(fr))||WM.events[0];
  const start=Math.max(0,current.event_time_sec-3),end=current.event_time_sec+5;endTime=end;
  const seek=()=>{video.currentTime=start;video.play().catch(()=>{});};
  if(video.readyState>=1)seek(); else video.addEventListener("loadedmetadata",seek,{once:true});
  present.innerHTML="<b>Observed present:</b> frame "+current.event_frame+" · t="+fmt(current.event_time_sec,1)+" s · "+
    (current.actual_action?"Observe":"No-observe")+" · outcome "+current.actual_outcome+" · "+motifName(current.current_motif)+".";
  renderHero();renderSequence();renderMetrics();drawFuture();
}
video.addEventListener("timeupdate",()=>{if(endTime!==null&&video.currentTime>=endTime)video.pause();});
btn.onclick=()=>selectEvent(sel.value);sel.onchange=()=>selectEvent(sel.value);

function renderHero(){
  const [nn,nN]=matchCount(neuralSeq()),[mn,mN]=matchCount(markovSeq());
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
function sequenceRow(label,kind,seq,actual){
  let chips="";
  const N=Math.min(8,seq.length||8);
  for(let i=0;i<N;i++){
    const q=seq[i]||{},id=q.motif??q.top_motif;
    const name=q.label||q.top_label||motifName(id);
    let cls="future-chip";
    let mark="";
    if(kind!=="actual"&&actual[i]){
      if(Number(id)===Number(actual[i].motif)){cls+=" match";mark="✓";}
      else {cls+=" miss";mark="×";}
    }
    chips+='<div class="'+cls+'"><span class="step">'+(i+1)+'</span><span class="motif">'+name+'</span><span class="hit">'+mark+'</span></div>';
  }
  return '<div class="future-row '+kind+'"><div class="future-row-label">'+label+'</div><div class="future-row-chips">'+chips+'</div></div>';
}
function renderSequence(){
  const act=actualSeq(),mk=markovSeq(),nw=neuralSeq(),gd=gatedSeq();
  strip.innerHTML=
    '<div class="future-strip-head"><span>Same present</span><strong>→ next 8 behavioral events</strong><span>✓ exact top-1 match to actual</span></div>'+
    sequenceRow("Actual","actual",act,act)+
    sequenceRow("Generative Markov","markov",mk,act)+
    sequenceRow("Neural world","neural",nw,act)+
    sequenceRow("Social-gated","gated",gd,act);
}
function renderMetrics(){
  const tr=current.trajectory,first=tr[0],[nn,nN]=matchCount(neuralSeq()),[mn,mN]=matchCount(markovSeq());
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
}
function drawFuture(){
  if(!A||!current)return;
  const r=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1,W=Math.max(320,r.width),H=Math.max(260,r.height);
  canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);
  const c=canvas.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);c.clearRect(0,0,W,H);c.fillStyle="#fff";c.fillRect(0,0,W,H);
  const all=A.framewise||[],xs=A.motifs.map(m=>m.x),ys=A.motifs.map(m=>m.y);
  for(const q of current.trajectory){xs.push(q.base_x,q.gate_x);ys.push(q.base_y,q.gate_y);}
  for(const q of actualSeq()){xs.push(q.x);ys.push(q.y);}
  for(const q of markovSeq()){xs.push(q.x);ys.push(q.y);}
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
  draw(actualSeq(),"#111",2.3,[3,3]);
  draw(markovSeq().map(q=>({x:q.x,y:q.y})),"#777",2.3,[7,4]);
  draw(current.trajectory.map(q=>({x:q.base_x,y:q.base_y})),"#276fbf",3,[]);
  draw(current.trajectory.map(q=>({x:q.gate_x,y:q.gate_y})),"#c84b35",3,[]);
}
window.addEventListener("resize",()=>{if(current)drawFuture();});
Promise.all([fetch("data/world_model.json").then(r=>r.json()),fetch("data/atlas.json").then(r=>r.json())]).then(([wm,a])=>{
  WM=wm;A=a;setupSelect();selectEvent(WM.default_event_frame);
}).catch(e=>{console.error(e);present.textContent="Could not load world-model rollout.";});
})();