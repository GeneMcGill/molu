#!/usr/bin/env python3
"""生成拆解用的实测基线：899 篇的特征分布，供对比诊断。"""
import json,re,collections,statistics,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTS=json.load(open(f"{ROOT}/01_原始文本/articles_clean.json",encoding='utf-8'))
U=[json.loads(l) for l in open(f"{ROOT}/13_全量/units.jsonl",encoding='utf-8')]
DST=f"{ROOT}/mimeng-skills/skills/mimeng-teardown/references"
os.makedirs(DST,exist_ok=True)
DIRTY=['特么','妈的','老子','牛逼','傻逼','妈蛋','装逼','我擦']
def feats(paras,title=''):
    ps=[p for p in paras if p and p.strip()]
    txt=''.join(ps)
    n=max(len(ps),1); L=len(txt)
    return {
      '字数': L, '段落数': n,
      '段落中位长度': statistics.median([len(p) for p in ps]) if ps else 0,
      '≤15字段落占比': sum(1 for p in ps if len(p)<=15)/n,
      '≤30字段落占比': sum(1 for p in ps if len(p)<=30)/n,
      '问句段落占比': sum(1 for p in ps if p.rstrip().endswith('？'))/n,
      '对话段落占比': sum(1 for p in ps if p.startswith('“') or p.startswith('"'))/n,
      '数字分段数': sum(1 for p in ps if re.match(r'^\d{1,2}[.、．)）]',p)),
      '脏话密度/万字': 10000*sum(txt.count(w) for w in DIRTY)/max(L,1),
      '第二人称密度/万字': 10000*txt.count('你')/max(L,1),
      '第一人称密度/万字': 10000*txt.count('我')/max(L,1),
      '标题长度': len(title),
    }
F=[feats(a['paras'],a['title']) for a in ARTS]
KEYS=list(F[0].keys())
s=["# 拆解基线（899 篇实测分布）\n\n",
   "> 用法：把待拆解文章算出同样指标，与下表对比，偏离越大越说明特征突出。\n",
   "> 全部为全量实测，非采样估算。\n\n",
   "| 指标 | p10 | p25 | 中位 | p75 | p90 | 均值 |\n|---|---|---|---|---|---|---|\n"]
for k in KEYS:
    v=sorted(f[k] for f in F)
    s.append(f"| {k} | {v[len(v)//10]:.2f} | {v[len(v)//4]:.2f} | {statistics.median(v):.2f} | "
             f"{v[3*len(v)//4]:.2f} | {v[int(len(v)*.9)]:.2f} | {statistics.mean(v):.2f} |\n")
open(f'{DST}/拆解基线.md','w',encoding='utf-8').write(''.join(s))
print("拆解基线已生成，指标数:",len(KEYS))
for k in KEYS:
    v=sorted(f[k] for f in F)
    print(f"  {k:20s} 中位 {statistics.median(v):.2f}")
