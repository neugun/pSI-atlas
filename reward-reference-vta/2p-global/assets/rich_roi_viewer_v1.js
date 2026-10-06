(()=> {
const $=id=>document.getElementById(id);
const fmt=(v,d=3)=>v==null||Number.isNaN(+v)?"—":typeof v==="number"?v.toFixed(d):String(v);
function qtile(a,q){const z=a.filter(Number.isFinite).sort((x,y)=>x-y); if(!z.length)return 0; const i=(z.length-1)*q,lo=Math.floor(i),hi=Math.ceil(i); return z[lo]*(hi-i)+z[hi]*(i-lo)}
function svgTrace(time, series){
  const W=720,H=250,L=54,R=18,T=18,B=38;
  const all=series.flatMap(s=>s.v).filter(Number.isFinite), ymin=qtile(all,.02), ymax=qtile(all,.98);
  const lo=ymin===ymax?ymin-1:ymin, hi=ymin===ymax?ymax+1:ymax;
  const x=t=>L+(t-time[0])/(time[time.length-1]-time[0])*(W-L-R);
  const y=v=>T+(hi-v)/(hi-lo)*(H-T-B);
  const colors=["#111827","#9ca3af","#2563eb"];
  let out='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="ROI mean traces">';
  out+='<line x1="'+L+'" y1="'+(H-B)+'" x2="'+(W-R)+'" y2="'+(H-B)+'" stroke="#111"/><line x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(H-B)+'" stroke="#111"/>';
  [time[0],(time[0]+time.at(-1))/2,time.at(-1)].forEach(t=>{out+='<text x="'+x(t)+'" y="'+(H-12)+'" text-anchor="middle" font-size="12">'+t.toFixed(1)+'s</text>'});
  [lo,(lo+hi)/2,hi].forEach(v=>{out+='<text x="'+(L-8)+'" y="'+(y(v)+4)+'" text-anchor="end" font-size="12">'+v.toFixed(2)+'</text>'});
  series.forEach((s,si)=>{let p="";s.v.forEach((v,i)=>{if(!Number.isFinite(v))return;p+=(p?"L":"M")+x(time[i]).toFixed(1)+","+y(v).toFixed(1)});out+='<path d="'+p+'" fill="none" stroke="'+colors[si]+'" stroke-width="'+(si===2?2.2:1.5)+'" opacity="'+(si===1?.8:1)+'"/>'});
  out+='<text x="'+(W/2)+'" y="'+(H-2)+'" text-anchor="middle" font-size="12">time (s)</text></svg>'; return out;
}
function heat(canvas,mat){
  const rows=mat.length, cols=rows?mat[0].length:0; if(!rows||!cols)return;
  canvas.width=cols; canvas.height=rows;
  const ctx=canvas.getContext("2d"), im=ctx.createImageData(cols,rows);
  const vals=mat.flat().map(Number).filter(Number.isFinite); let lim=Math.max(Math.abs(qtile(vals,.02)),Math.abs(qtile(vals,.98))); if(!lim)lim=1;
  let k=0;
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){
    let v=Number(mat[r][c]); if(!Number.isFinite(v))v=0; v=Math.max(-lim,Math.min(lim,v))/lim;
    let R,G,B;
    if(v>=0){R=255;G=Math.round(255*(1-v));B=Math.round(255*(1-v));}
    else {const a=-v;R=Math.round(255*(1-a));G=Math.round(255*(1-a));B=255;}
    im.data[k++]=R;im.data[k++]=G;im.data[k++]=B;im.data[k++]=255;
  }
  ctx.putImageData(im,0,0);
}
function tableObj(obj){
  const keys=Object.keys(obj||{}); if(!keys.length)return '<span class="small">No record.</span>';
  return '<table class="data-table compact-table"><tbody>'+keys.map(k=>'<tr><th>'+k+'</th><td>'+fmt(obj[k],3)+'</td></tr>').join('')+'</tbody></table>';
}
function render(bundle,idx=0){
  const roi=bundle.rois[idx]; if(!roi)return;
  $("richStatus").textContent=bundle.session_id+" · "+bundle.n_roi+" ROIs · "+bundle.n_trials+" trials · "+bundle.n_timepoints+" time points";
  $("roiPick").innerHTML=bundle.rois.map((r,i)=>'<option value="'+i+'">ROI '+r.roi_id+' · plane '+r.plane+'</option>').join('');
  $("roiPick").value=String(idx);
  $("roiMask").src=roi.mask_png||"";
  $("roiMask").style.display=roi.mask_png?"block":"none";
  $("tracePlot").innerHTML=svgTrace(bundle.time_s,[{n:"raw",v:roi.mean_raw},{n:"bg",v:roi.mean_bg},{n:"sub",v:roi.mean_sub}]);
  heat($("trialHeat"),roi.heatmap_sub);
  const meta=bundle.trial_meta||[];
  $("heatCaption").textContent=meta.length?meta.map(x=>x.condition).filter(Boolean).length+" trial labels available · rows are trials, columns are time":"rows are trials, columns are time";
  $("roiQC").innerHTML=tableObj(roi.qc);
  $("roiModels").innerHTML=(roi.models||[]).length?'<table class="data-table compact-table"><thead><tr>'+Object.keys(roi.models[0]).map(k=>'<th>'+k+'</th>').join('')+'</tr></thead><tbody>'+roi.models.map(r=>'<tr>'+Object.keys(roi.models[0]).map(k=>'<td>'+fmt(r[k],4)+'</td>').join('')+'</tr>').join('')+'</tbody></table>':'<span class="small">No model table.</span>';
  const tm=(roi.trial_metrics||[]).slice(0,12);
  $("roiTrials").innerHTML=tm.length?'<table class="data-table compact-table"><thead><tr>'+Object.keys(tm[0]).map(k=>'<th>'+k+'</th>').join('')+'</tr></thead><tbody>'+tm.map(r=>'<tr>'+Object.keys(tm[0]).map(k=>'<td>'+fmt(r[k],3)+'</td>').join('')+'</tr>').join('')+'</tbody></table>':'<span class="small">No trial metrics.</span>';
}
window.addEventListener("DOMContentLoaded",()=>{
  const input=$("richFile"); if(!input)return;
  let bundle=null;
  input.addEventListener("change",async()=>{
    const f=input.files&&input.files[0]; if(!f)return;
    try{
      const b=JSON.parse(await f.text());
      if(b.schema!=="CARMA_RICH_ROI_BUNDLE_V1")throw new Error("Unexpected schema: "+b.schema);
      bundle=b; $("richViewer").hidden=false; render(bundle,0);
      $("sourceManifest").innerHTML='<table class="data-table compact-table"><thead><tr><th>Source</th><th>bytes</th><th>SHA256</th></tr></thead><tbody>'+b.source_manifest.map(x=>'<tr><td>'+x.name+'</td><td>'+x.bytes+'</td><td><code>'+x.sha256.slice(0,16)+'…</code></td></tr>').join('')+'</tbody></table>';
    }catch(e){$("richStatus").textContent="Could not load bundle: "+e.message;}
  });
  $("roiPick").addEventListener("change",()=>{if(bundle)render(bundle,+$("roiPick").value)});
});
})();