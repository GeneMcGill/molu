# 墨炉 molu

一条**从洞察到复盘**的中文内容生产引擎。装 1 个包，用 11 个模块。

```
  墨炉 molu —— 从洞察到复盘的内容生产引擎

  ░ 原料层 ░  Corpus Source（可插拔换源，引擎零改动）
     写作方法论(4A·咨询框架) · 本地素材库 · 实时热榜
                ↓
         kb.py · 统一数据层
                ↓
  ░ 主管道 ░  Pipeline（①→⑤ 顺序执行，不可跳步）
     ① 洞察 insight  →  ② 策略 strategy  →  ③ 雷达 radar
     → ④ 选题 topic/reuse  →  ⑤ 生产 writer/video
                ↓
  ░ 收束层 ░
     ⑥ 审核 guard  →  ⑦ 拆解 teardown  ⇄ 反馈回 ①
     ⑧ lens ◈ 视角 —— 贯穿全程
```

## 安装

```bash
cp -r molu ~/.agents/skills/molu     # 通用 Agents
cp -r molu ~/.claude/skills/molu     # Claude Code
cp -r molu ~/.codex/skills/molu      # Codex
```

**不用逐个装**：11 个模块在同一个包里，agent 递归发现（排序即管道顺序）。
也可只装单个模块：`cp -r molu/writer ~/.claude/skills/`

## 使用

```
/console  这套东西能干嘛
/writer   帮我写一篇
/guard    这篇能发吗
/topic    帮我想选题
```

## 数据层 kb.py

模块不自带数据副本，统一经 kb.py 查询当前接入的语料源：

```bash
python3 molu/kb.py stats             # 概览
python3 molu/kb.py get GLD 10        # 取 10 条高复用金句
python3 molu/kb.py search TGT 稳定 5 # 靶子检索
python3 molu/kb.py install <id>      # 接入语料源（带口径校验）
```

> 本仓库**不携带语料**。完整数据层需要一个本地语料源（`molu/inlets/`，
> 含 manifest / vocabulary(冻结) / stats / provenance 四份声明），接入方式见
> `molu/scripts/inlet_check.py`。口径与词表规则见 ADR-0001。

## 边界

**不做**：流量预测 / 账号代运营 / 投放策略 / 用户调研执行 / 法律意见。
**不适用**：新闻报道 / 调查 / 非虚构 / 学术写作 / 时政 / 真实悲剧的情绪化加工。

## 许可

方法论（各 SKILL.md / 脚本）以 **CC BY-NC 4.0** 提供；不含任何逐字语料。
收录进你导出的产出时请替换为原创表述。

## 模块速览

| # | 模块 | 中文 | 一句话 |
|---|---|---|---|
| 0 | console | 总控台 | 管道图 + 调度 |
| 1 | insight | 洞察 | 读者是谁、卡在哪 |
| 2 | strategy | 策略 | 定位/人群/节奏/形式 |
| 3 | radar | 雷达 | 当下能写什么 |
| 4 | topic / reuse | 选题/复用 | 20 个选题 / 榨干一个主题 |
| 5 | writer / video | 写稿/短视频 | 长文图文 / 口播脚本 |
| 6 | guard | 把关 | 发布前三层审核（只读） |
| 7 | teardown | 拆解 | 为什么爆：12 指标 |
| 8 | lens | 视角 | 审视写作决策，贯穿全程 |

v1.0.0
