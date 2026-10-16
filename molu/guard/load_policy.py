#!/usr/bin/env python3
"""加载审核立场配置并判定内容档位。

用法:
    python3 load_policy.py                    列出所有立场
    python3 load_policy.py <立场>               查看该立场规则
    python3 load_policy.py <立场> --check "文本"  预判档位
"""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "config", "guard-policy.json")
POLICY = json.load(open(CFG, encoding='utf-8'))

TIER_PATTERNS = {
    "B": [r'养老金', r'社保', r'医保', r'政策', r'国务院', r'省委', r'市委',
          r'军演', r'军事', r'外交部', r'制裁', r'领土', r'宗教',
          r'历史虚无', r'长征', r'党建', r'新闻联播'],
    "C": [r'我朋友.{0,6}(说|讲|经历)', r'我有个朋友', r'我同事', r'我邻居',
          r'我知道一个人', r'跳楼', r'自杀', r'猝死', r'遇害', r'身亡',
          r'去世', r'病逝'],
}
STANCE_EXTRA = {
    "parent":  {"C": [r'(儿童|孩子|幼儿|宝宝).{0,10}(正脸|面部|照片)', r'展示.{0,6}儿童',
                      r'育儿焦虑放大', r'别人家孩子.{0,6}都', r'这样养(孩|孩子|娃)']},
    "finance": {"B": [r'承诺收益率', r'年化\s*\d', r'稳赚', r'保本', r'荐股',
                      r'无资质.{0,6}(理财|投资)', r'制造投资恐慌', r'崩盘']},
    "health":  {"B": [r'具体用药剂量', r'疗效承诺', r'替代就医', r'包治', r'根治']},
    "creator": {"C": [r'用编造的他人经历', r'把读者情绪当燃料但不给出口']},
    "b2b":     {"C": [r'点名竞品并贬低', r'虚构客户案例', r'比竞品强',
                      r'竞品.{0,6}(垃圾|不行|差)', r'他们根本不懂', r'同行.{0,4}(垃圾|废物|不行)']},
}


def load(stance="general"):
    if stance not in POLICY["perspectives"]:
        raise SystemExit(f"未知立场「{stance}」。可选：{', '.join(POLICY['perspectives'])}")
    p = POLICY["perspectives"][stance]
    return {"stance": stance, "label": p["label"], "note": p.get("note", ""),
            "extra_redlines": p.get("extra_redlines", []),
            "relaxed": p.get("relaxed", []), "tiers": POLICY["tiers"]}


def judge(text, stance="general"):
    cfg = load(stance)
    hits = []
    for tier, pats in TIER_PATTERNS.items():
        for p in pats:
            m = re.search(p, text)
            if m:
                hits.append((tier, m.group(0)[:20]))
    for tier, pats in STANCE_EXTRA.get(stance, {}).items():
        for p in pats:
            m = re.search(p, text)
            if m:
                hits.append((tier, m.group(0)[:20]))
    if not hits:
        return {"verdict": "A", "reason": "未命中任何红线",
                "action": cfg["tiers"]["A"]["default_action"], "hits": [], "stance": stance}
    top = "C" if "C" in {t for t, _ in hits} else "B"
    return {"verdict": top, "reason": cfg["tiers"][top]["name"],
            "action": cfg["tiers"][top]["default_action"], "hits": hits, "stance": stance}


def main():
    args = sys.argv[1:]
    if not args:
        print("可用立场：")
        for k, v in POLICY["perspectives"].items():
            print(f"  {k:10s} {v['label']}")
            if v.get("note"):
                print(f"             {v['note']}")
        return 0
    # 抽出 --check（可出现在立场前或后）
    # 事故：`load_policy.py --check "文本"` 曾把 --check 当成立场名，报「未知立场 --check」
    check_text = None
    if "--check" in args:
        i = args.index("--check")
        if i + 1 >= len(args):
            print("用法错误：--check 后面要跟待审文本", file=sys.stderr)
            return 2
        check_text = args[i + 1]
        args = args[:i] + args[i + 2:]
    stance = args[0] if args else "general"   # 不写立场时默认 general
    if check_text is not None:
        print(json.dumps(judge(check_text, stance), ensure_ascii=False, indent=1))
        return 0
    cfg = load(stance)
    print(f"立场：{cfg['label']}（{stance}）")
    if cfg["note"]:
        print(f"说明：{cfg['note']}")
    print("\n档位规则：")
    for t, v in cfg["tiers"].items():
        print(f"  {t} {v['name']:6s} → {v['default_action']}")
    print("\n本立场加严：")
    for r in cfg["extra_redlines"] or ["（无）"]:
        print(f"  · {r}")
    print("\n本立场放宽：")
    for r in cfg["relaxed"] or ["（无）"]:
        print(f"  · {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
