(()=> {
const $=id=>document.getElementById(id);
const fmt=(v,d=3)=>v==null?"—":typeof v==="number"?(Number.isFinite(v)?v.toFixed(d):"—"):String(v);
function median(a){const z=a.filter(Number.isFinite).sort((x,y)=>x-y);if(!z.length)return null;const m=z.length>>1;return z.length%2?z[m]:(z[m-1]+z[m])/2}
function renderPlane(b,i){
 const p=b.planes[i]; $("qcPlaneImg").src=p.image_png; $("qcPlaneCap").textContent="Plane "+p.plane+" · "+p.roi_count+" ROI masks · "+(p.reference_name||"mask-only fallback");
}
function render(b){
 $("qcBundleStatus").textContent=b.session_id+" · "+b.n_trials+" trials · "+b.n_roi+" ROIs · source hashes "+b.source_manifest.length;
 $("qcPlanePick").innerHTML=b.planes.map((p,i)=>'<option value="'+i+'">Plane '+p.plane+' · '+p.roi_count+' ROIs</option>').join('');
 renderPlane(b,0);
 const snr=b.rois.map(r=>Number(r.qc?.snr)).filter(Number.isFinite);
 const bg=b.rois.flatMap(r=>r.trial_metrics||[]).map(x=>Number(x.roi_bg_corr)).filter(Number.isFinite);
 const area=b.rois.map(r=>Number(r.qc?.area_rebuild ?? r.qc?.area_saved)).filter(Number.isFinite);
 const cards=[
  ["ROIs",b.n_roi],["Trials",b.n_trials],["Median SNR",fmt(median(snr),2)],
  ["Median ROI-bg corr",fmt(median(bg),3)],["Median ROI area",fmt(median(area),1)],["Source files",b.source_manifest.length]
 ];
 $("qcKpis").innerHTML=cards.map(x=>'<div class="card"><div class="small">'+x[0]+'</div><div class="kpi">'+x[1]+'</div></div>').join('');
 const rows=b.rois.map(r=>({roi:r.roi_id,plane:r.plane,snr:r.qc?.snr,area:r.qc?.area_rebuild??r.qc?.area_saved,bg:median((r.trial_metrics||[]).map(x=>Number(x.roi_bg_corr)).filter(Number.isFinite))}));
 $("qcRoiTable").innerHTML='<table class="data-table"><thead><tr><th>ROI</th><th>Plane</th><th>SNR</th><th>Area</th><th>Median bg corr</th></tr></thead><tbody>'+rows.map(r=>'<tr><td>'+r.roi+'</td><td>'+r.plane+'</td><td>'+fmt(r.snr,2)+'</td><td>'+fmt(r.area,0)+'</td><td>'+fmt(r.bg,3)+'</td></tr>').join('')+'</tbody></table>';
 $("qcSources").innerHTML='<table class="data-table compact-table"><thead><tr><th>Source</th><th>Bytes</th><th>SHA256</th></tr></thead><tbody>'+b.source_manifest.map(x=>'<tr><td>'+x.name+'</td><td>'+x.bytes+'</td><td><code>'+x.sha256.slice(0,20)+'…</code></td></tr>').join('')+'</tbody></table>';
 $("qcPrivate").hidden=false;
}
window.addEventListener("DOMContentLoaded",()=>{
 let bundle=null, input=$("qcBundleFile"); if(!input)return;
 input.addEventListener("change",async()=>{const f=input.files&&input.files[0];if(!f)return;try{const b=JSON.parse(await f.text());if(b.schema!=="CARMA_RICH_ROI_BUNDLE_V1")throw new Error("Unexpected schema "+b.schema);bundle=b;render(b)}catch(e){$("qcBundleStatus").textContent="Could not load: "+e.message}});
 $("qcPlanePick").addEventListener("change",()=>{if(bundle)renderPlane(bundle,+$("qcPlanePick").value)});
});
})();