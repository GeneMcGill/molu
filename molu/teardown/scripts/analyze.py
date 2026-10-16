#!/usr/bin/env python3
"""拆解一篇内容：算 12 个指标并与 899 篇基线做百分位对比。

设计原则：结论必须自我限定。偏离基线 ≠ 有缺陷。
用法: python3 analyze.py <文章.md>
"""
import csv, json, os, sys, re, statistics, bisect

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.normpath(os.path.join(HERE, "..", "references"))
DIST = json.load(open(os.path.join(REF, "dist.json"), encoding='utf-8')) \
    if os.path.exists(os.path.join(REF, "dist.json")) else None

BASE = {'字数': (2423, 1895, 2778), '段落数': (88, 68, 107), '段落中位长度': (22, 19, 25),
        '≤15字段落占比': (0.29, 0.23, 0.36), '≤30字段落占比': (0.70, 0.62, 0.78),
        '问句段落占比': (0.06, 0.03, 0.09), '对话段落占比': (0.01, 0.00, 0.02),
        '数字分段数': (0, 0, 0), '脏话密度/万字': (7.60, 0.00, 17.72),
        '第二人称密度/万字': (82.15, 51.53, 128.40), '第一人称密度/万字': (173.50, 118.37, 262.03),
        '标题长度': (16, 13, 18)}
DIRTY = ['特么', '妈的', '老子', '牛逼', '傻逼', '妈蛋', '装逼', '我擦']
PUNCT_END = tuple('。！？…”"')


def feats(paras, title=''):
    ps = [p.strip() for p in paras if p.strip()]
    txt = ''.join(ps); n = max(len(ps), 1); L = len(txt)
    return {'字数': L, '段落数': n,
            '段落中位长度': statistics.median([len(p) for p in ps]) if ps else 0,
            '≤15字段落占比': sum(1 for p in ps if len(p) <= 15) / n,
            '≤30字段落占比': sum(1 for p in ps if len(p) <= 30) / n,
            '问句段落占比': sum(1 for p in ps if p.rstrip().endswith('？')) / n,
            '对话段落占比': sum(1 for p in ps if p.startswith('“') or p.startswith('"')) / n,
            '数字分段数': sum(1 for p in ps if re.match(r'^\d{1,2}[.、．)）]', p)),
            '脏话密度/万字': 10000 * sum(txt.count(w) for w in DIRTY) / max(L, 1),
            '第二人称密度/万字': 10000 * txt.count('你') / max(L, 1),
            '第一人称密度/万字': 10000 * txt.count('我') / max(L, 1),
            '标题长度': len(title)}


def pct(key, val):
    if not DIST or key not in DIST:
        return None
    return 100 * bisect.bisect_left(DIST[key], val) / len(DIST[key])


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    raw = open(sys.argv[1], encoding='utf-8').read()
    lines = raw.split('\n')
    title = ''
    for l in lines[:3]:
        if l.strip():
            title = re.sub(r'^#+\s*', '', l.strip()); break
    paras = [l for l in lines if not l.strip().startswith('#')]
    f = feats(paras, title)

    print("# 拆解诊断\n")
    print(f"**标题**：{title or '(未识别)'}  （{f['标题长度']} 字）\n")
    print("## 指标对比（对照 899 篇基线）\n")
    print("| 指标 | 本文 | 基线中位 | 百分位 | 位置 |")
    print("|---|---|---|---|---|")
    for k in BASE:
        v = f[k]; med = BASE[k][0]
        vs = f"{v:.2f}" if isinstance(v, float) else str(v)
        p = pct(k, v)
        if p is None:
            print(f"| {k} | **{vs}** | {med} | — |")
            continue
        band = ('p90以上·极端值' if p > 90 else 'p75-p90·特征突出' if p > 75
                else 'p25-p75·常见区间' if p >= 25 else 'p10-p25·偏另一端' if p >= 10
                else 'p10以下·极端值')
        print(f"| {k} | **{vs}** | {med} | 第 {p:.0f} | {band} |")

    is_list = f['数字分段数'] >= 3
    print("\n## 解读\n")
    notes = []
    if is_list:
        notes.append(f"- **识别为清单型**（{f['数字分段数']} 个编号段）→ 段落长度类指标"
                     f"（段落中位长度 / ≤15字占比 / ≤30字占比）**不参与诊断**。"
                     f"清单文每个条目是「编号+小标题+解释」，段落天然长。全库只有 12% 这么写。")
    p = pct('段落中位长度', f['段落中位长度'])
    if not is_list and p is not None and p > 90:
        notes.append(f"- **段落中位 {f['段落中位长度']:.0f} 字**（第 {p:.0f} 百分位）→ "
                     f"比 90% 的样本都厚，手机端会累。建议拆段")
    elif not is_list and p is not None and p > 75:
        notes.append(f"- 段落中位 {f['段落中位长度']:.0f} 字（第 {p:.0f} 百分位）→ 偏厚，"
                     f"但仍在她 25% 的正常范围里。**不是缺陷，是特征**")
    p2 = pct('第二人称密度/万字', f['第二人称密度/万字'])
    if p2 is not None and p2 < 10:
        notes.append(f"- **第二人称密度 {f['第二人称密度/万字']:.0f}/万字**（第 {p2:.0f} 百分位）→ "
                     f"极端偏低，代入感会明显弱")
    if f['标题长度'] > 20:
        notes.append(f"- **标题 {f['标题长度']} 字** → 小红书硬限 20 字，会发不出去")
    if not notes:
        notes.append("- 各项指标都在她的常见区间内，没有需要改的")
    print("\n".join(notes))
    print("\n> 提醒：偏离基线**不等于**有问题。落在 p75–p90 说明这项是特征，不是缺陷。"
          "只有 p90 以上 / p10 以下的极端值才值得动手。")
    print("> 若某个极端值你无法解释，**直接说「这项我不知道原因」**，不要编造理由"
          "（例如说「数据被污染了」）。基线来自 899 篇全量，可信。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
