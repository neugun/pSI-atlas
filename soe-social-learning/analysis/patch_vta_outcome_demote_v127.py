# -*- coding: utf-8 -*-
"""Replace remaining causal overstatements after true observation-time audit."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
for name in ("index.html","index-zh.html"):
 p=R/name;s=p.read_text(encoding="utf-8")
 if name=="index.html":
  old=r'<div class="model-contract" id="vta-readout-explained-v116">.*?</div>'
  replacement='''<div class="model-contract" id="vta-readout-explained-v116"><strong>Historical readout provenance, now corrected.</strong> The previously named action-bout mean (median 28.85 s) is an extended post-anchor interval. Genuine observation bouts (median 2.40 s) are short and usually pre-anchor; the fixed 0–6 s readout starts at the outcome anchor. The exact 1,371-event extended-interval result (9/9, P=.0039 against each frozen fixed-credit weight) is retained for audit but is NOT proof of DA social-credit encoding during actual observation. See the source-verified 821-event, three-readout comparison above. Neither the early sampling stage, outcome stage nor post-bout offset should be conflated.</div>'''
  s,n=re.subn(old,lambda x:replacement,s,count=1,flags=re.S);assert n==1
  s=s.replace("Post-stage mechanistic readout | use bout-matched DA for social credit, retain fixed 0–6 s as the frozen reference","Historical Post extended-interval analysis | corrected source labels and frozen fixed-window comparison")
  s=s.replace("Real-bout credit → VTA","Exploratory interval → VTA")
  s=s.replace("Extended-interval credit → VTA","Exploratory interval → VTA")
  s=s.replace("Primary mechanistic Post readout plus the frozen fixed-window reference.","Historical extended-interval model comparison, not real observation-bout DA.")
  s=s.replace("Real-bout DA gives the clearest social-credit result:","Historical extended-interval DA shows a model-comparator difference:")
  s=s.replace("Extended-interval DA gives the clearest social-credit result:","Historical extended-interval DA shows a model-comparator difference:")
  s=s.replace("Why the frozen fixed-window result stays visible.","Why the historical fixed-window result stays visible.")
  s=s.replace("the current mechanistic Post readout is the bout-matched social-credit analysis","the historical long-interval comparison is exploratory and not an actual observation-bout test")
  s=s.replace("At Post, bout-matched DA gives the clearest source-specific credit result:","At Post, the historical extended-interval comparison was directionally favorable for selected credit:")
  s=s.replace("The most direct raw-FP reconstruction keeps", "The original raw-FP reconstruction keeps")
 else:
  old=r'<div class="model-contract" id="vta-readout-explained-v116">.*?</div>'
  replacement='''<div class="model-contract" id="vta-readout-explained-v116"><strong>旧读出的数据来源，现已纠正。</strong>以前称为真实行动片段的平均信号，其实来自中位 28.85 秒的结果锚点后延长区间；真正观察 bout 中位为 2.40 秒，大多数发生在结果锚点之前。原先 1,371 个事件中 9/9 动物、P=.0039 的结果保留为历史模型比较，无法证明真实观察期多巴胺直接编码 social credit。上方严格匹配 821 个事件的三读出重新分析，才是当前正确的比较依据。</div>'''
  s,n=re.subn(old,lambda x:replacement,s,count=1,flags=re.S);assert n==1
  s=s.replace("结果期主机制读出｜社会归因采用模型延长区间多巴胺，同时保留固定 0–6 秒原始参照","历史结果期延长区间分析｜已核查真实观察片段，并保留固定 0–6 秒原始参照")
  s=s.replace("结果期主机制读出与冻结固定窗口参照。","历史延长区间分析与冻结固定窗口参照，并非真实观察片段。")
  s=s.replace("真实行动片段归因 → VTA","延长区间模型比较 → VTA")
  s=s.replace("模型延长区间归因 → VTA","延长区间模型比较 → VTA")
  s=s.replace("结果期主机制读出","结果期历史窗口对照")
  s=s.replace("结果期的主机制展示采用与模型延长区间对齐的多巴胺读出","结果期的延长区间分析保留为探索性历史比较")
  s=s.replace("主叙事优先模型延长区间来自生物学理由","原先将模型延长区间作为主读出的做法需要纠正")
 p.write_text(s,encoding="utf-8")
 print("UPDATED",name)
