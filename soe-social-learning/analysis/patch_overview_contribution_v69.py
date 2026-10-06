from pathlib import Path
import re, html
R=Path(__file__).resolve().parents[1]
maps={
"index.html":[
("01","Mice learn to turn social observation into their own action"),
("02","Social information is sampled when it is useful"),
("03","Social learning keeps memory on several timescales"),
("04","A compact mechanistic model explains the sampling policy"),
("05","A data-driven world model independently validates and extends the mechanism"),
("06","What is observed changes the learner’s own feeding"),
("07","Dopamine follows the social-learning computation in real time"),
("08","Vision and dopamine play different causal roles"),
("09","The results form one closed-loop learning architecture"),
("10","The same rules can generate social-learning behavior"),
("11","The learned variables predict behavior in new tasks"),
("12","Related computations recur across species and social tasks"),
],
"index-zh.html":[
("01","小鼠学会把社会观察真正转成自己的行动"),
("02","社会信息只有在有用时才被主动利用"),
("03","社会学习同时保留多个时间尺度的记忆"),
("04","一个紧凑机制模型解释动物何时选择观察"),
("05","数据驱动 world model 独立验证并扩展这套机制"),
("06","看到什么会直接改变 learner 自己的进食"),
("07","Dopamine 实时跟随社会学习的计算过程"),
("08","视觉信息进入与 dopamine teaching 承担不同因果作用"),
("09","所有结果汇成一个闭环社会学习架构"),
("10","同一套规则能够生成社会学习行为"),
("11","学到的 computation 可以预测新任务中的行为"),
("12","相关 computation 在其他物种和社会任务中重复出现"),
]}
for fn,items in maps.items():
 p=R/fn; s=p.read_text(encoding="utf-8")
 s=s.replace('<div class="section-kicker" style="margin-top:34px">Current result atlas</div>',
             '<div class="section-kicker" style="margin-top:34px">The contribution in one page</div>') if fn=="index.html" else s.replace('<div class="section-kicker" style="margin-top:34px">当前结果图谱</div>',
             '<div class="section-kicker" style="margin-top:34px">一页看懂这项工作的贡献</div>')
 for idx,title in items:
  pat=r'(<div class="series-index">'+re.escape(idx)+r'</div>\s*<h3>).*?(</h3>)'
  s,n=re.subn(pat,lambda m:m.group(1)+html.escape(title)+m.group(2),s,count=1,flags=re.S)
  if n!=1: raise RuntimeError(f"{fn} {idx} not patched")
 p.write_text(s,encoding="utf-8")
 print(fn,"atlas titles patched")
