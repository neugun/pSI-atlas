(() => {
const sel=document.querySelector("#worldEventSelect"),btn=document.querySelector("#worldReplayBtn");
const video=document.querySelector("#worldRealVideo"),canvas=document.querySelector("#worldFutureMap");
const present=document.querySelector("#worldPresentCaption"),future=document.querySelector("#worldFutureCaption"),metrics=document.querySelector("#worldMetrics");
if(!sel||!video||!canvas)return;
let WM=null,A=null,current=null,endTime=null;

const fmt=(x,d=3)=>Number.isFinite(Number(x))?Number(x).toFixed(d):"n/a";
const pct=x=>Number.isFinite(Number(x))?(100*Number(x)).toFixed(1)+"%":"n/a";

function setupSelect(){
  sel.innerHTML="";
  for(const fr of WM.top_event_frames){
    const e=WM.events.find(x=>x.event_frame===fr); if(!e)continue;
    const o=document.createElement("option");o.value=String(fr);
    o.textContent="frame "+fr+" · t="+fmt(e.event_time_sec,1)+" s · ΔActive "+fmt(e.delta_active_any,3);
    sel.appendChild(o);
  }
  sel.value=String(WM.default_event_frame);
}
function selectEvent(fr){
  current=WM.events.find(x=>x.event_frame===Number(fr))||WM.events[0];
  const start=Math.max(0,current.event_time_sec-3),end=current.event_time_sec+5;endTime=end;
  const seek=()=>{video.currentTime=start;video.play().catch(()=>{});};
  if(video.readyState>=1)seek(); else video.addEventListener("loadedmetadata",seek,{once:true});
  present.innerHTML="<b>Observed event:</b> frame "+current.event_frame+" · t="+fmt(current.event_time_sec,1)+" s · action "+(current.actual_action?"Observe":"No-observe")+" · outcome "+current.actual_outcome+" · current motif "+current.current_motif+".";
  renderMetrics();drawFuture();
}
video.addEventListener("timeupdate",()=>{if(endTime!==null&&video.currentTime>=endTime)video.pause();});
btn.onclick=()=>selectEvent(sel.value);sel.onchange=()=>selectEvent(sel.value);

function renderMetrics(){
  const tr=current.trajectory,first=tr[0];
  const cards=[
    ["Future Active (≥1)","Normal "+pct(current.base_active_any)+" · Gated "+pct(current.gate_active_any),"Δ "+fmt(current.delta_active_any,3)],
    ["Step-1 P(Active)","Normal "+pct(first.base_p_active)+" · Gated "+pct(first.gate_p_active),"Δ "+fmt(first.delta_p_active,3)],
    ["Future Observe count","Normal "+fmt(current.base_obs_count,2)+" · Gated "+fmt(current.gate_obs_count,2),"Δ "+fmt(current.delta_obs_count,3)],
    ["Terminal state shift","Motif JS "+fmt(current.terminal_motif_js,4),"latent RMS "+fmt(current.terminal_latent_rms,3)]
  ];
  metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
  const actual=(current.actual_future||[]).map(x=>x.label).join(" → ")||"not available";
  const markov=(current.markov_closed_loop||[]).map(x=>x.top_label).join(" → ")||"not available";
  future.innerHTML="<b>Actual:</b> "+actual+
    "<br><b>Generative Markov:</b> "+markov+
    "<br><b>Neural world:</b> "+tr.map(x=>x.base_top_label).join(" → ")+
    "<br><b>Social-gated:</b> "+tr.map(x=>x.gate_top_label).join(" → ");
}
function drawFuture(){
  if(!A||!current)return;
  const r=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1,W=Math.max(320,r.width),H=Math.max(260,r.height);
  canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);
  const c=canvas.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);c.clearRect(0,0,W,H);c.fillStyle="#fff";c.fillRect(0,0,W,H);
  const all=A.framewise||[];
  const xs=A.motifs.map(m=>m.x),ys=A.motifs.map(m=>m.y);
  for(const q of current.trajectory){xs.push(q.base_x,q.gate_x);ys.push(q.base_y,q.gate_y);}
  for(const q of current.actual_future||[]){xs.push(q.x);ys.push(q.y);}
  for(const q of current.markov_closed_loop||[]){xs.push(q.x);ys.push(q.y);}
  let x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
  const mx=(x1-x0)*.12+5,my=(y1-y0)*.12+5;x0-=mx;x1+=mx;y0-=my;y1+=my;
  const sc=Math.min((W-52)/(x1-x0),(H-52)/(y1-y0));
  const ox=(W-(x1-x0)*sc)/2,oy=(H-(y1-y0)*sc)/2;
  const xy=(x,y)=>[ox+(x-x0)*sc,oy+(y1-y)*sc];
  c.globalAlpha=.10;c.fillStyle="#6d7377";
  for(let i=0;i<all.length;i+=18){const q=all[i],[x,y]=xy(q[0],q[1]);c.fillRect(x,y,1.2,1.2);}
  c.globalAlpha=1;c.font="600 11px system-ui";c.textAlign="center";
  for(const m of A.motifs){const [x,y]=xy(m.x,m.y);c.fillStyle="#777";c.fillText(String(m.id),x,y);}
  const fr=current.event_frame,cur=all[fr]||null;let start=null;
  if(cur){start=xy(cur[0],cur[1]);c.fillStyle="#111";c.beginPath();c.arc(start[0],start[1],5,0,Math.PI*2);c.fill();c.fillText("present",start[0],start[1]-11);}
  function drawPts(raw,stroke,width=2.5,dash=[]){
    const pts=raw.map(q=>xy(q.x,q.y)); if(!pts.length)return;
    c.strokeStyle=stroke;c.fillStyle=stroke;c.lineWidth=width;c.setLineDash(dash);c.beginPath();
    if(start)c.moveTo(start[0],start[1]);else c.moveTo(pts[0][0],pts[0][1]);
    pts.forEach(p=>c.lineTo(p[0],p[1]));c.stroke();c.setLineDash([]);
    pts.forEach((p,i)=>{c.beginPath();c.arc(p[0],p[1],3.8,0,Math.PI*2);c.fill();c.fillStyle="#111";c.font="600 8px system-ui";c.fillText(String(i+1),p[0],p[1]-7);c.fillStyle=stroke;});
  }
  drawPts(current.actual_future||[],"#111111",2.2,[3,3]);
  drawPts((current.markov_closed_loop||[]).map(q=>({x:q.x,y:q.y})),"#777777",2.2,[7,4]);
  drawPts(current.trajectory.map(q=>({x:q.base_x,y:q.base_y})),"#276fbf",3);
  drawPts(current.trajectory.map(q=>({x:q.gate_x,y:q.gate_y})),"#c84b35",3);
}
window.addEventListener("resize",()=>{if(current)drawFuture();});
Promise.all([fetch("data/world_model.json").then(r=>r.json()),fetch("data/atlas.json").then(r=>r.json())]).then(([wm,a])=>{
  WM=wm;A=a;setupSelect();selectEvent(WM.default_event_frame);
}).catch(e=>{console.error(e);present.textContent="Could not load world-model rollout.";});
})();