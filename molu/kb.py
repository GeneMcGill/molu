#!/usr/bin/env python3
"""墨炉 molu · 统一数据层（Knowledge Base）

模块通过本脚本查询当前语料源的数据，不各自携带数据副本。
换语料源 = `kb.py install <name>`，模块零改动。

**路径无关**：用 `__file__` 定位引擎根，从任何 cwd 调用都能跑。

## 命令

    python3 kb.py stats                    数据概览
    python3 kb.py get <类型> [条数]          取某一类
    python3 kb.py search <类型> <关键词…>   按类型+关键词过滤
    python3 kb.py find <关键词…>            跨类型检索
    python3 kb.py topics | axioms | emotion | structure | years
    python3 kb.py inlets                   语料源列表
    python3 kb.py install <name>           切换语料源（先校验口径）

## 输出

默认人读。加 `--json` 输出结构化，供程序消费。
"""
import json, os, sys, re, collections

# 用 __file__ 定位，与 cwd 无关
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
INLETS = os.path.join(ROOT, "inlets")

UNIT_NAMES = {
    "GLD": "金句", "CAS": "故事节拍", "VOI": "观点断言", "QOT": "引语",
    "TUR": "转折", "EMO": "情绪放大器", "PER": "人设", "HOK": "钩子",
    "REC": "收束", "TGT": "靶子", "OPS": "运营话术",
}
CONF_ORDER = {"high": 0, "medium": 1, "low": 2}


def current_inlet():
    active = os.path.join(INLETS, ".active")
    if os.path.exists(active):
        name = open(active).read().strip()
        p = os.path.join(INLETS, name)
        if os.path.isdir(p):
            return p
    if not os.path.isdir(INLETS):
        return None
    subs = [d for d in sorted(os.listdir(INLETS))
            if os.path.isdir(os.path.join(INLETS, d))]
    return os.path.join(INLETS, subs[0]) if subs else None


def load(keep_only=True):
    d = current_inlet()
    if not d or not os.path.exists(f"{d}/units.jsonl"):
        return []
    out = []
    for line in open(f"{d}/units.jsonl", encoding='utf-8'):
        u = json.loads(line)
        if keep_only and not u.get("keep", True):
            continue
        out.append(u)
    return out


def manifest():
    d = current_inlet()
    p = f"{d}/manifest.json"
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def fmt_unit(u, with_meta=True):
    rh = '/'.join(u.get('rhetoric') or [])
    head = f"[{u['unit']}] 「{u['text']}」"
    meta = []
    if u.get('confidence'):
        meta.append(u['confidence'])
    meta.append(f"{len(u['text'])}字")
    if rh:
        meta.append(rh)
    if u.get('structure'):
        meta.append(f"结构:{u['structure']}")
    if u.get('self_contained') is False:
        meta.append("依赖前文")
    if with_meta and u.get('topics'):
        meta.append('/'.join(u['topics']))
    if with_meta and u.get('date'):
        meta.append(u['date'])
    if with_meta and u.get('article'):
        meta.append(f"《{u['article'][:22]}》")
    return head + "  " + " · ".join(meta)


# --------------------------------------------------------------- 命令
def cmd_stats(a):
    d = current_inlet()
    mf = manifest()
    u = load()
    if a.json:
        print(json.dumps({
            "inlet": d.split("/")[-1] if d else None,
            "manifest": mf, "usable": len(u),
            "types": dict(collections.Counter(x['unit'] for x in u)),
            "topics": dict(collections.Counter(t for x in u for t in (x.get('topics') or []))),
            "confidence": dict(collections.Counter(x.get('confidence') for x in u)),
        }, ensure_ascii=False, indent=1))
        return 0
    print("=" * 66)
    print(f"语料源：{d.split('/')[-1] if d else '（未找到）'}   {mf.get('name','')}")
    print("=" * 66)
    if mf:
        print(f"规模 {mf.get('unit_count','?'):,} 单元 / {mf.get('article_count','?')} 篇"
              if isinstance(mf.get('unit_count'), int) else "")
        print(f"时间 {' ~ '.join(mf.get('time_range', ['?','?']))}   "
              f"v{mf.get('version','?')}  {mf.get('schema','?')}")
    if not u:
        print("\n无可用单元")
        return 1
    print(f"\n入库 {len(u):,} 条\n")
    print(f"{'类型':<8}{'含义':<8}{'条数':>8}")
    for k, v in collections.Counter(x['unit'] for x in u).most_common():
        print(f"{k:<8}{UNIT_NAMES.get(k,''):<8}{v:>8,}")
    return 0


def cmd_get(a):
    u = [x for x in load() if x['unit'] == a.kind]
    u.sort(key=lambda x: (CONF_ORDER.get(x.get('confidence'), 3), -len(x['text'])))
    if a.json:
        print(json.dumps(u[:a.limit], ensure_ascii=False, indent=1)); return 0
    print(f"{a.kind}（{UNIT_NAMES.get(a.kind,'')}）{len(u)} 条，显示前 {min(a.limit,len(u))} 条\n")
    for x in u[:a.limit]:
        print(fmt_unit(x)); print()
    return 0


def cmd_search(a):
    pool = [x for x in load() if x['unit'] == a.kind]
    hits = [x for x in pool if all(k in (x.get('text') or '') for k in a.kw)]
    hits.sort(key=lambda x: (CONF_ORDER.get(x.get('confidence'), 3), -len(x['text'])))
    if a.json:
        print(json.dumps(hits[:a.limit], ensure_ascii=False, indent=1)); return 0
    print(f"{a.kind} 命中「{' '.join(a.kw)}」：{len(hits)} 条\n")
    for x in hits[:a.limit]:
        print(fmt_unit(x)); print()
    return 0


def cmd_find(a):
    pool = load()
    hits = [x for x in pool if all(k in (x.get('text') or '') for k in a.kw)]
    hits.sort(key=lambda x: (CONF_ORDER.get(x.get('confidence'), 3), -len(x['text'])))
    if a.json:
        print(json.dumps(hits[:a.limit], ensure_ascii=False, indent=1)); return 0
    print(f"跨类型命中「{' '.join(a.kw)}」：{len(hits)} 条\n")
    for x in hits[:a.limit]:
        print(fmt_unit(x)); print()
    return 0


def cmd_dist(a):
    u = load()
    key = a.kind
    if key == 'topics':
        c = collections.Counter(t for x in u for t in (x.get('topics') or []))
    elif key == 'axioms':
        c = collections.Counter(t for x in u for t in (x.get('axioms') or []))
    elif key == 'emotion':
        c = collections.Counter(x.get('emotion') for x in u if x.get('emotion'))
    elif key == 'structure':
        c = collections.Counter(x.get('structure') for x in u if x.get('unit') == 'CAS')
    elif key == 'years':
        c = collections.Counter(x.get('date', '')[:4] for x in u if x.get('date'))
    else:
        print("用法: topics|axioms|emotion|structure|years"); return 2
    if a.json:
        print(json.dumps(dict(c.most_common()), ensure_ascii=False, indent=1)); return 0
    for k, v in c.most_common(a.limit):
        print(f"  {str(k):<14}{v:>7,}")
    return 0


def cmd_inlets(a):
    if not os.path.isdir(INLETS):
        print("未找到 inlets/"); return 1
    cur = current_inlet()
    if a.json:
        out = []
        for d in sorted(os.listdir(INLETS)):
            p = os.path.join(INLETS, d)
            if not os.path.isdir(p):
                continue
            mp = f"{p}/manifest.json"
            mf = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}
            out.append({"id": d, "units": mf.get('unit_count'), "active": p == cur,
                        "name": mf.get('name')})
        print(json.dumps(out, ensure_ascii=False, indent=1)); return 0
    cur_id = cur.split("/")[-1] if cur else None
    print("语料源\n")
    for d in sorted(os.listdir(INLETS)):
        p = os.path.join(INLETS, d)
        if not os.path.isdir(p):
            continue
        mp = f"{p}/manifest.json"
        mf = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}
        n = mf.get('unit_count', '?')
        print(f"  {d:20s} {str(n):>8} 单元  {mf.get('name','')[:26]}"
              f"{'  <- 当前' if d == cur_id else ''}")
    return 0


def cmd_install(a):
    d = os.path.join(INLETS, a.name)
    if not os.path.isdir(d):
        avail = [x for x in sorted(os.listdir(INLETS)) if os.path.isdir(os.path.join(INLETS, x))] \
                if os.path.isdir(INLETS) else []
        print(f"语料源不存在：{a.name}\n可用：{', '.join(avail) or '（无）'}")
        return 1
    checker = os.path.join(ROOT, "scripts", "inlet_check.py")
    if os.path.exists(checker):
        print("校验口径…")
        rc = os.system(f'python3 "{checker}" "{d}" > /dev/null 2>&1')
        if rc != 0:
            print(f"口径校验未通过，拒绝启用。\n   详情：python3 scripts/inlet_check.py {d}")
            return 1
    open(os.path.join(INLETS, ".active"), "w").write(a.name)
    mf = manifest()
    print(f"已启用：{a.name}（{mf.get('unit_count','?')} 单元）")
    print("模块无需改动，会自动读到新数据")
    return 0


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    argv = [x for x in argv if x != "--json"]
    if not argv:
        print(__doc__); return 2
    cmd, rest = argv[0], argv[1:]

    class A: pass
    a = A(); a.limit = 20; a.json = as_json
    n = lambda i, d=20: int(rest[i]) if len(rest) > i and rest[i].isdigit() else d

    if cmd == "stats":   return cmd_stats(a)
    if cmd == "inlets":  return cmd_inlets(a)
    if cmd == "get":
        if not rest: print("用法: kb.py get <类型> [条数]"); return 2
        a.kind = rest[0].upper(); a.limit = n(1); return cmd_get(a)
    if cmd == "search":
        if len(rest) < 2: print("用法: kb.py search <类型> <关键词…> [条数]"); return 2
        a.kind = rest[0].upper()
        a.limit = n(len(rest)-1); a.kw = rest[1:len(rest)-1] if rest[-1].isdigit() else rest[1:]
        return cmd_search(a)
    if cmd == "find":
        a.limit = n(len(rest)-1); a.kw = rest[:len(rest)-1] if rest[-1].isdigit() else rest
        if not a.kw: print("用法: kb.py find <关键词…> [条数]"); return 2
        return cmd_find(a)
    if cmd in ("topics", "axioms", "emotion", "structure", "years"):
        a.kind = cmd; a.limit = n(0, 15 if cmd != 'years' else 12); return cmd_dist(a)
    if cmd == "install":
        a.name = rest[0] if rest else "current"; return cmd_install(a)
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main())