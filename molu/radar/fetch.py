#!/usr/bin/env python3
"""抓取实时热点，过滤红线，转成选题原料。

设计原则：
- 热榜（--hot）无需登录，是最稳定的入口
- 主题检索需要登录态，抓不到明确报错，不静默失败
- 绝不编造：拿不到就说拿不到

用法:
    python3 fetch.py hot [--limit N]
    python3 fetch.py topic "关键词"
    python3 fetch.py check
"""
import argparse, json, os, re, subprocess, sys, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
REF = os.path.join(ROOT, "radar", "references")
L30 = os.path.expanduser("~/.pi/agent/skills/last30days-cn/scripts/last30days.py")
if not os.path.exists(L30):
    for cand in ["~/.claude/skills/last30days-cn/scripts/last30days.py",
                 "~/.agents/skills/last30days-cn/scripts/last30days.py"]:
        p = os.path.expanduser(cand)
        if os.path.exists(p):
            L30 = p
            break

QUOTES = chr(0x201c) + chr(0x201d) + chr(0x2018) + chr(0x2019) + chr(0x22) + chr(0x27)
REDLINES = [
    ("真实悲剧/伤亡", r'死亡|遇难|身亡|事故|火灾|坠|溺|自杀|殉|重伤|尸体|遗体|被害|凶'),
    ("司法案件",      r'案|宣判|判刑|获刑|起诉|逮捕|拘留|警方|通报|调查|一审|二审|无期'),
    ("时政/官方",      r'新闻联播|国务院|中央|部委|主席|总理|省委|市委|政府|长征|党建|总书记|政策'),
    ("军事/国防",      r'解放军|国防部|军事|军队|导弹|核力量|军舰|战机|军演|部队'),
    ("外交/国际",      r'中方|外交部|菲方|美方|俄方|日方|韩方|领土|主权|制裁|关税|会谈|访华'),
    ("宏观经济/政策",   r'GDP|央行|财政部|发改|社保|医保|养老金'),
    ("医疗/疾病",      r'癌|中毒|疫情|患者|疫苗'),
    ("灾害",          r'地震|洪水|台风|暴雨|塌|爆炸|泥石流'),
    ("未成年受害",      r'幼儿|儿童|小学|未成年|婴儿|幼儿园'),
    ("性别对立",       r'女拳|男拳|田园女权'),
    ("体育赛事",       r'KPL|世界赛|世界杯|奥运|冠军|联赛|战胜|夺金|决赛'),
    ("娱乐八卦",       r'开播|定档|杀青|官宣|塌房'),
]
TOPIC_KW = {
 '两性关系': ['男','女','婚','恋','爱','分手','前任','渣','嫁','娶','情','相亲','彩礼'],
 '婚姻家庭': ['婚','家','婆','夫','妻','老公','老婆','父母','妈','爸'],
 '亲子育儿': ['孩子','娃','育儿','教育','家长','幼儿','作业','教师','学区'],
 '金钱观':   ['钱','存','工资','薪','存款','利率','消费','买','贵','省','穷','富','股','房'],
 '阶层与贫富': ['阶层','贫','房价','内卷','打工','小镇','下沉'],
 '职场':     ['工作','职','公司','老板','员工','加班','辞职','失业','裁员','面试','上班'],
 '自我成长':  ['努力','成长','自律','进步','学习','改变','迷茫','坚持'],
 '外貌与身材': ['胖','瘦','美','丑','颜','身材','化妆','减肥','穿搭'],
 '情绪与心理': ['焦虑','抑郁','情绪','压力','崩溃','内耗','孤独','失眠','熬夜'],
 '社交与人际': ['朋友','社交','关系','同事','圈子','人际','断交'],
 '社会热点':  ['热','爆','网友','热议','刷屏'],
 '生活方式':  ['生活','习惯','旅行','日常','躺平','退货','零食','手机'],
}


def run(args, timeout=300):
    if not os.path.exists(L30):
        return None, f"未找到 last30days-cn（期望 {L30}）"
    try:
        p = subprocess.run([sys.executable, L30] + args,
                           capture_output=True, text=True, timeout=timeout)
        return p.stdout, None
    except subprocess.TimeoutExpired:
        return None, f"超时 {timeout}s"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def parse_hot(text):
    items = []
    for m in re.finditer(r'^\d+\.\s+\*\*(.+?)\*\*\s+—\s+(.+)$', text, re.M):
        items.append({"title": m.group(1).strip(), "platforms": m.group(2).strip(), "cross": True})
    cur = None
    for line in text.split("\n"):
        h = re.match(r'^##\s+(.+?)(热搜|热榜)$', line.strip())
        if h:
            cur = h.group(1); continue
        m = re.match(r'^\d+\.\s+(.+?)(?:\s+\[[^\]]*\])?(?:\s+([\d.]+万))?$', line.strip())
        if m and cur:
            items.append({"title": m.group(1).strip(), "platform": cur,
                          "heat": m.group(2), "cross": False})
    return items


PUNCT_RE = re.compile('[' + chr(92) + 's' + chr(92) + 'uff0c' + 'u3002' + 'uff1f' + 'uff01' + 'u3001' + 'uff1a' + 'uff1b' + QUOTES + '（()）' + chr(0x300a) + chr(0x300b) + chr(0x3010) + chr(0x3011) + ']')


def norm_title(t):
    t = re.sub(r'\s*[\[【][^\]】]*[\]】]\s*$', '', t)
    return re.sub(PUNCT_RE, '', t)


def dedupe(items):
    merged = {}
    for it in items:
        k = norm_title(it['title'])
        if not k:
            continue
        if k not in merged:
            merged[k] = dict(it); merged[k]['platforms_list'] = []
        m = merged[k]
        if it.get('cross'):
            m['cross'] = True; m['platforms'] = it['platforms']
        elif it.get('platform'):
            m['platforms_list'].append(it['platform'])
    for m in merged.values():
        m['platform_count'] = len(set(m['platforms_list']))
    return list(merged.values())


def filter_redline(items):
    ok, dropped = [], []
    for it in items:
        tags = [n for n, r in REDLINES if re.search(r, it['title'])]
        if tags:
            it['redline'] = tags; dropped.append(it)
        else:
            ok.append(it)
    return ok, dropped


def map_topics(items):
    for it in items:
        it['topics'] = [k for k, ws in TOPIC_KW.items() if any(w in it['title'] for w in ws)]
    return items


def heat_val(h):
    if not h:
        return 0.0
    m = re.match(r'([\d.]+)\s*万', str(h))
    if m:
        return float(m.group(1)) * 10000
    try:
        return float(h)
    except Exception:
        return 0.0


def cmd_hot(a):
    print("抓取全网热榜...", flush=True)
    out, err = run(["--hot", "--emit", "compact", "--hot-limit", str(a.limit)])
    if err:
        print(f"抓取失败：{err}"); return 1
    raw = parse_hot(out)
    if not raw:
        print(f"未解析到热点\n{out[:400]}"); return 1
    items = dedupe(raw)
    ok, dropped = filter_redline(items)
    ok = map_topics(ok)
    ok.sort(key=lambda x: (-x.get('cross', False), -x.get('platform_count', 0), -heat_val(x.get('heat'))))
    os.makedirs(REF, exist_ok=True)
    data = {"fetched_at": datetime.date.today().isoformat(), "source": "last30days-cn --hot",
            "stats": {"raw": len(raw), "deduped": len(items),
                      "writable": len(ok), "redline_dropped": len(dropped)},
            "items": ok,
            "redline_dropped": [{"title": d['title'], "tags": d['redline']} for d in dropped]}
    p = os.path.join(REF, "hot_snapshot.json")
    json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n原始 {len(raw)} → 去重 {len(items)} → 可写 {len(ok)}（红线过滤 {len(dropped)}）")
    print(f"已写入 {p}\n")
    print("=" * 66); print("可写热点（按跨平台热度排序）"); print("=" * 66)
    for it in ok[:a.show]:
        flag = "[hot]" if it.get('cross') else ("[*]" if it.get('platform_count', 0) >= 2 else " ")
        print(f"{flag} {it['title'][:44]}")
        meta = []
        if it.get('topics'):
            meta.append('/'.join(it['topics']))
        if it.get('platforms'):
            meta.append(it['platforms'][:56])
        elif it.get('platforms_list'):
            meta.append(','.join(sorted(set(it['platforms_list']))))
        if it.get('heat'):
            meta.append(it['heat'])
        print(f"    {' · '.join(meta)}")
    if dropped:
        print(f"\n已排除（红线）{len(dropped)} 条：")
        for d in dropped[:6]:
            print(f"  - {d['title'][:36]}  [{','.join(d['redline'])}]")
    return 0


def cmd_topic(a):
    print(f"检索：{a.kw}（近 {a.days} 天）...", flush=True)
    out, err = run([a.kw, "--quick", "--emit", "compact", "--days", str(a.days)])
    if err:
        print(f"检索失败：{err}"); return 1
    failed = re.findall(r'\*\*错误:\*\*\s*(.+)', out)
    if failed:
        print(f"{len(failed)} 个源需要登录态（未登录时只有微信+百度）：")
        for f in failed[:3]:
            print(f"  · {f[:100]}")
    print("=" * 66); print(out[:3500])
    return 0


def cmd_check(a):
    out, err = run(["--diagnose"], timeout=180)
    print(out if not err else f"检查失败：{err}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="实时热点 → 选题原料")
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("hot")
    h.add_argument("--limit", type=int, default=20)
    h.add_argument("--show", type=int, default=15)
    t = sub.add_parser("topic"); t.add_argument("kw"); t.add_argument("--days", type=int, default=30)
    sub.add_parser("check")
    a = ap.parse_args()
    return {"hot": cmd_hot, "topic": cmd_topic, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
