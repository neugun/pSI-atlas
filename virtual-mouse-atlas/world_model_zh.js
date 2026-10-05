(() => {
const sel=document.querySelector("#worldEventSelect"),btn=document.querySelector("#worldReplayBtn");
const video=document.querySelector("#worldRealVideo");
const present=document.querySelector("#worldPresentCaption"),future=document.querySelector("#worldFutureCaption"),metrics=document.querySelector("#worldMetrics");
const heroStats=document.querySelector("#worldHeroStats"),strip=document.querySelector("#worldFutureStrip"),eventNote=document.querySelector("#worldEventNote");
const viewToggle=document.querySelector("#worldViewToggle");
if(!sel||!video||!strip)return;
let WM=null,EW=null,A=null,current=null,endTime=null,view="motif";
const MOTIF_ZH_WM={1:"社会朝向-转身",2:"社会朝向-远",3:"近距离社会朝向",4:"社会朝向-近",5:"远距离移动",6:"远距离静止",7:"朝向示范鼠-远",8:"spout 周围移动",9:"spout 附近静止",10:"spout 极近静止",11:"社会朝向-近距离静止",12:"社会朝向-近距离互动静止"};

const fmt=(x,d=3)=>Number.isFinite(Number(x))?Number(x).toFixed(d):"n/a";
const pct=x=>Number.isFinite(Number(x))?(100*Number(x)).toFixed(1)+"%":"n/a";
const motifName=id=>{
  const m=A&&A.motifs?A.motifs.find(x=>Number(x.id)===Number(id)):null;
  return MOTIF_ZH_WM[Number(id)]||(m?m.name:("Motif "+id));
};
const EVENT_ZH={"Other":"其他","Observe":"观察","Unrewarded bout":"未获奖 bout","Active bout":"主动取食 bout","Passive bout":"被动获奖 bout"};
const eventName=id=>{const x=EW&&EW.event_names&&EW.event_names[Number(id)]?EW.event_names[Number(id)]:("事件 "+id);return EVENT_ZH[x]||x;};

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
      ?"最佳 motif 示例 · frame "+fr
      :"备选示例 "+i+" · frame "+fr+" · ΔActive "+fmt(e.delta_active_any,3);
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
  present.innerHTML="<b>当前真实状态：</b> frame "+current.event_frame+" · t="+fmt(current.event_time_sec,1)+" s · "+
    (current.actual_action?"观察":"未观察")+" · 结果 "+current.actual_outcome+" · "+motifName(current.current_motif)+".";
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
      ["闭环示例","SWM "+nn+"/"+nN,"历史 Markov "+mn+"/"+mN],
      ["5事件准确率",pct(n.event5_acc),"线性 "+pct(lin.event5_acc)+" · Markov "+pct(m.event5_acc)+" · 全局 "+pct(g.event5_acc)],
      ["5事件 NLL",fmt(n.event5_nll,3),"线性 "+fmt(lin.event5_nll,3)+" · Markov "+fmt(m.event5_nll,3)+" · 全局 "+fmt(g.event5_nll,3)],
      ["SWM vs 线性模型",t.neural_better+"/27","更低 NLL · P="+Number(t.p_one_sided).toExponential(1)]
    ];
    heroStats.innerHTML=cards.map(c=>'<div class="world-hero-stat"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    return;
  }
  const act=motifActual(),nw=motifNeural(),mk=motifMarkov();
  const [nn,nN]=matchCount(nw,act,"motif"),[mn,mN]=matchCount(mk,act,"motif");
  const best=WM.best_example&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);
  let cards=[
    ["SWM 精确未来步骤",nn+"/"+nN,"top-1 motif 命中"],
    ["Markov 精确未来步骤",mn+"/"+mN,"同一留出真实未来"]
  ];
  if(best){
    const s=WM.best_example.summary;
    cards.push(["未来 NLL",fmt(s.neural_nll,2)+" vs "+fmt(s.markov_nll,2),"SWM vs Markov · 越低越好"]);
    cards.push(["总体社会信息对照","0.620 → 0.561 / 0.572","效能 AUC · 匹配替换 / 无社会信息重训"]);
  }else{
    cards.push(["总体效能 AUC","0.620","严格同状态 ΔActive"]);
    cards.push(["社会信息依赖","26/27","匹配替换和无社会信息重训后均下降"]);
  }
  heroStats.innerHTML=cards.map(c=>'<div class="world-hero-stat"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
}

function modelLine(label,kind,q,a,mode){
  const match=kind==="actual"?"":(isMatch(q,a,mode)?" ✓":" ×");
  const cls=kind==="actual"?"":" "+(isMatch(q,a,mode)?"match":"miss");
  const pr=kind!=="actual"&&Number.isFinite(Number(q.prob_actual))
    ? '<span class="future-model-prob">P(真实) '+pct(q.prob_actual)+'</span>' : '';
  return '<div class="future-model-line '+kind+cls+'><span class="future-model-name">'+label+'</span><span class="future-model-value">'+getName(q,mode)+pr+'</span><span class="future-model-hit">'+match+'</span></div>';
}
function renderStepGrid(rows,mode,title){
  const actual=rows.find(r=>r.kind==="actual").seq;
  const N=Math.min(8,...rows.map(r=>r.seq.length));
  let cards="";
  for(let i=0;i<N;i++){
    cards+='<article class="future-step-card"><div class="future-step-number">步骤 '+(i+1)+'</div>';
    for(const r of rows)cards+=modelLine(r.label,r.kind,r.seq[i],actual[i],mode);
    cards+='</article>';
  }
  strip.innerHTML='<div class="future-strip-head"><strong>'+title+'</strong><span>✓ 与真实未来 top-1 精确匹配</span></div><div class="future-step-grid">'+cards+'</div>';
}
function renderSequence(){
  if(view==="event"){
    renderStepGrid([
      {label:"真实",kind:"actual",seq:eventActual()},
      {label:"SWM",kind:"neural",seq:eventNeural()},
      {label:"历史 Markov",kind:"markov",seq:eventMarkov()}
    ],"event","接下来 8 个语义事件 = 同一当前状态下 4 个动作→bout trial");
    return;
  }
  renderStepGrid([
    {label:"真实",kind:"actual",seq:motifActual()},
    {label:"SWM",kind:"neural",seq:motifNeural()},
    {label:"Markov",kind:"markov",seq:motifMarkov()}
  ],"motif","同一当前状态下接下来的 8 个真实行为 motif");
}

function renderMetrics(){
  if(view==="event"){
    const act=eventActual(),nw=eventNeural(),mk=eventMarkov();
    const [nn,nN]=matchCount(nw,act,"event"),[mn,mN]=matchCount(mk,act,"event");
    const n=eventSummary("Neural social world"),lin=eventSummary("Full-history linear"),m=eventSummary("History Markov");
    const cards=[
      ["闭环序列","SWM "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"精确语义事件步骤"],
      ["采样动作 NLL",fmt(n.action_nll,3)+" vs "+fmt(lin.action_nll,3),"SWM vs 完整历史线性模型"],
      ["Bout 结果 NLL",fmt(n.outcome_nll,3)+" vs "+fmt(lin.outcome_nll,3),"这里线性模型略好"],
      ["汇总 5 事件","Acc "+pct(n.event5_acc)+" · NLL "+fmt(n.event5_nll,3),"Markov "+pct(m.event5_acc)+" · "+fmt(m.event5_nll,3)]
    ];
    metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
    future.innerHTML="<b>如何阅读：</b>奇数步是 bout 前采样状态（其他或观察）；偶数步是随后 bout 结果（未获奖、主动取食或被动获奖）。";
    eventNote.innerHTML='<b>五事件字典。</b> '+EW.definition+'<div class="event-dict">'+EW.dictionary.map(x=>'<span>'+x.event_name+' · n='+Number(x.count).toLocaleString()+'</span>').join("")+'</div>';
    return;
  }
  const act=motifActual(),nw=motifNeural(),mk=motifMarkov();
  const [nn,nN]=matchCount(nw,act,"motif"),[mn,mN]=matchCount(mk,act,"motif");
  const cards=[
    ["预测增益","SWM "+nn+"/"+nN+" · Markov "+mn+"/"+mN,"精确未来 motif 步骤"],
    ["观察效能","AUC 0.620","严格同状态 ΔActive · 27 只留出动物"],
    ["匹配社会轨迹替换","0.561","26/27 效能 AUC 下降 · P=1.49×10⁻⁸"],
    ["无社会信息重训","0.572","26/27 效能 AUC 下降 · P=2.29×10⁻⁶"]
  ];
  metrics.innerHTML=cards.map(c=>'<div class="world-metric"><div class="k">'+c[0]+'</div><div class="v">'+c[1]+'</div><div class="d">'+c[2]+'</div></div>').join("");
  const best=WM.best_example&&Number(current.event_frame)===Number(WM.best_example.summary.event_frame);
  future.innerHTML=best
    ? "<b>为何选这个示例：</b>这是刻意选择的最清晰留出 rollout 可视化：SWM 命中 8 个真实未来 motif 中的 6 个，而生成式 Markov 基线为 0/8。下方总体留出动物结果才是推断依据。"
    : "<b>其他留出示例：</b>上方每一步都比较同一真实当前状态下的记录未来与模型 top-1 预测。";
  eventNote.textContent="";
}

function renderAll(){renderHero();renderSequence();renderMetrics();}
Promise.all([
  fetch("data/world_model.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json()),
  fetch("data/event5_world.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json()),
  fetch("data/atlas.json?v=20261004v7",{cache:"no-store"}).then(r=>r.json())
]).then(([wm,ew,a])=>{
  WM=wm;EW=ew;A=a;setupSelect();selectEvent(WM.default_event_frame);
}).catch(e=>{console.error(e);present.textContent="无法加载世界模型 rollout。";});
})();

