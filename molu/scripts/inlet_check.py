#!/usr/bin/env python3
"""进气阀接入口径对齐检查。

拒绝词表不一致的进气阀 —— 这是 dbskill 踩过的坑
（同一批语料出现三套互不对齐的主题体系）。

用法: python3 inlet_check.py <进气阀目录> [--baseline inlets/current]
"""
import argparse, json, os, sys, collections, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
REQUIRED = ["manifest.json", "vocabulary.json", "stats.json", "provenance.json"]
MIN_UNITS = 100

def chk(cond, name, detail="", F=None):
    F.append(cond)
    print(f"  {'✅' if cond else '❌'} {name}" + (f"  → {detail}" if detail and not cond else ""))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inlet")
    ap.add_argument("--baseline", default=os.path.join(ROOT, "inlets", "current"))
    a = ap.parse_args(); d = a.inlet; F = []
    print("=" * 66); print(f"进气阀接入检查：{os.path.basename(d)}"); print("=" * 66)

    print("\n[1] 必需文件")
    for f in REQUIRED:
        chk(os.path.exists(f"{d}/{f}"), f"{f} 存在", "", F)
    if not all(F):
        print("\n拒绝接入。缺文件。"); return 1

    mf = json.load(open(f"{d}/manifest.json", encoding='utf-8'))
    vc = json.load(open(f"{d}/vocabulary.json", encoding='utf-8'))
    st = json.load(open(f"{d}/stats.json", encoding='utf-8'))
    pv = json.load(open(f"{d}/provenance.json", encoding='utf-8'))

    print("\n[2] 元信息")
    for k in ["id", "name", "version", "schema"]:
        chk(bool(mf.get(k)), f"manifest.{k}", "", F)
    chk(mf.get("unit_count", 0) >= MIN_UNITS, f"单元数 ≥{MIN_UNITS}", str(mf.get("unit_count")), F)

    print("\n[3] 词表对齐（对齐失败 → 拒绝接入）")
    bp = f"{a.baseline}/vocabulary.json"
    if not os.path.exists(bp):
        print(f"  基线不存在，跳过")
    else:
        bv = json.load(open(bp, encoding='utf-8'))
        for key in ["topics", "axioms", "unit_types"]:
            mine, base = set(vc.get(key, [])), set(bv.get(key, []))
            chk(mine == base, f"{key} 与基线一致（{len(base)} 项）",
                f"多:{sorted(mine-base)[:3]} 少:{sorted(base-mine)[:3]}", F)

    print("\n[4] 统计特征")
    for k in ["paragraph_median_len", "gld_median_len", "units_per_article_median", "type_distribution"]:
        chk(k in st, f"stats.{k}", "", F)

    print("\n[5] 合规声明")
    chk("distribution_allowed" in pv, "provenance.distribution_allowed", "", F)
    chk(bool(pv.get("redlines")), "红线清单非空", str(pv.get("redlines")), F)

    print("\n[6] 声明与实际一致")
    uj = f"{d}/units.jsonl"
    if os.path.exists(uj):
        n = sum(1 for _ in open(uj, encoding='utf-8'))
        chk(n == mf.get("unit_count"), "行数 = unit_count", f"{n} vs {mf.get('unit_count')}", F)
        bad = collections.Counter()
        top = set(vc.get("topics", []))
        for line in open(uj, encoding='utf-8'):
            for t in json.loads(line).get('topics') or []:
                if t not in top:
                    bad[t] += 1
        chk(not bad, "实际 topics 未越界", str(dict(list(bad.items())[:3])), F)

    npass = sum(1 for x in F if x)
    print("\n" + "=" * 66)
    print(f"通过 {npass} / 失败 {len(F)-npass}")
    if not all(F):
        print("\n拒绝接入。")
        return 1
    print("\n接入检查通过")
    return 0

if __name__ == "__main__":
    sys.exit(main())
