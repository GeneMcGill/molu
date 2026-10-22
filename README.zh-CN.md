# molu 墨炉

[English](README.md) · 简体中文

**molu 墨炉**是中文内容生产引擎 Skill 包，包含洞察研究、策略定位、热点选题、写稿、发布审核与爆款拆解等能力，可安装到支持 Skills 的 AI Agent 中使用

[![Version](https://img.shields.io/badge/version-1.0.3-2563EB.svg?style=flat-square)](https://github.com/GeneMcGill/molu/releases)
[![Skills](https://img.shields.io/badge/skills-11%20modules-7C3AED.svg?style=flat-square)](#按任务查找-skill)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-16A34A.svg?style=flat-square)](#许可证)

支持 Claude Code、Codex、WorkBuddy 和其他兼容 Skills 的 Agent。方法论由 899 篇公开公众号原文（2015-09 ~ 2018-12，213 万字）蒸馏而来，经实测提取 16,227 个内容单元，逐字校验命中率 100%

**本次更新：** v1.0.3——install.sh 拓扑自检：目标目录解析后与源目录相同时（如 ~/.claude/skills 为整目录软链形态）跳过软链写入并提示改用 'install.sh agents' 实体安装，杜绝 molu-* 自指死链。v1.0.2——模块名保持 `molu-<模块>` 干净命名（无编号）；面板排序为 agent 字典序，主管道位次以 description 开头 ①→⑪ 标注；模块说明收紧为短句；徽章只留 Version / Skills / License

## 目录

- [molu 是什么](#molu-是什么)
- [安装](#安装)
- [开始使用](#开始使用)
- [怎样提供任务材料](#怎样提供任务材料)
- [按任务查找 Skill](#按任务查找-skill)
- [仓库资料](#仓库资料)
- [更新、问题与支持](#更新问题与支持)
- [许可证](#许可证)

## molu 是什么

Skill 是一套针对某类任务编写的 Agent 指令。安装 molu 后，可以在 Agent 对话中调用 `/molu-console` 或某个具体模块，例如 `/molu-writer`

如果你还不知道从哪里开始，把问题交给 `/molu-console`。它显示完整管道图、读取你当前所处的环节，判断现在适合先做洞察、出选题、写稿，还是先过审核；需要时调用对应模块并在同一对话中推进

molu 的主张是**深优先于快**：抓到热点先问背后的永恒痛点，出选题先确认写给谁，写完必须过审核。它不是流量预测器——不承诺数据，只交付可检查的方法与结构

molu 常用于这些工作：

- 搞清读者是谁、卡在哪、未被满足的需求是什么
- 定位、人群、节奏、形式的内容策略
- 抓取实时热点，过滤红线，转成可写的选题
- 一个主题拆出十个角度，形成持续产出
- 产出公众号长文、图文与短视频口播脚本
- 发布前法律、伦理、平台三层审核
- 拆解一篇内容为什么爆或为什么不爆

## 安装

选择与你的 Agent 相符的一种安装方式。以下安装命令都在终端运行，不要把它们作为聊天内容发送给 Agent

### 使用 Skills CLI 安装到支持的 Agent

终端需要能够运行 `npx`。执行：

```bash
npx -y skills add GeneMcGill/molu -g --all
```

`-g` 表示全局安装，`--all` 表示安装到 Skills CLI 识别的所有 Agent。只想安装到某一个 Agent 时，可以删除 `--all`，然后按 CLI 提示选择目标

安装后，在目标 Agent 的对话中输入：

```text
/molu-console 这套东西能干嘛
```

### 手动复制安装

不使用 CLI 时，把 `molu/` 整个目录复制到 Agent 的 skills 目录：

```bash
cp -r molu ~/.agents/skills/molu     # 通用 Agents
cp -r molu ~/.claude/skills/molu     # Claude Code
cp -r molu ~/.codex/skills/molu      # Codex
```

也可以只装单个模块：`cp -r molu/writer ~/.claude/skills/`

### 安装后没有看到命令

先确认安装命令成功，并确认安装目标是当前正在使用的 Agent。Skill 的入口名称以所在 Agent 实际显示的为准；面板按名称字典序展示模块；主管道位次在各模块 description 开头用 ①→⑪ 标注（①总控 → ②洞察 → ③策略 → ④雷达 → ⑤选题 → ⑥复用 → ⑦写稿 → ⑧短视频 → ⑨审核 → ⑩拆解 → ⑪视角）

## 开始使用

### 第一次使用：先了解入口

在 Agent 对话框输入：

```text
/molu-console 这套东西能干嘛
```

总控台会输出管道图、列出 11 个模块（01→11 即管道顺序）、判断你卡在哪一环，并给出最小可行动作

### 不确定从哪里开始：把问题交给 `/molu-console`

把当前情况和问题写在命令后面。可以说得不完整，Agent 会先判断环节再推进：

```text
/molu-console 我在做职场类公众号，写了三个月，单篇阅读一直停在 800 左右。帮我看看先解决定位、选题还是写法。
```

### 已经知道要做什么：直接调用模块

在命令后附上问题、材料和希望得到的结果：

```text
/molu-topic 我写职场省钱方向。给我 20 个可直接写的选题，每条带切入角度和依据。
```

```text
/molu-writer 这是我的选题和素材。按公众号规格写一篇可发布的稿子。
```

```text
/molu-guard 这篇内容准备发公众号。帮我做发布前审核，标出风险位置。
```

```text
/molu-teardown 拆解这篇 10 万+ 为什么能爆，并对比我的差距。
```

### 接入语料源（可选但推荐）

模块的方法论开箱即用；接上语料源后，选题、复用、拆解模块可以引用经过实测校验的素材库。语料源是**可插拔的**：换语料源不影响引擎。完整流程见 [数据层说明](molu/README.md)：

```bash
python3 molu/kb.py stats             # 查看当前数据
python3 molu/kb.py install <id>      # 接入语料源（带口径校验）
```

### 收到结果后：继续当前任务

如果结果还需要补充，直接在当前对话中提供新事实、材料或修改意见，当前模块会接着处理。写完的内容在发布前一律过 `/molu-guard`，它有权说「别发」

## 怎样提供任务材料

结果会受到你提供的事实、材料和 Agent 工具权限影响。不需要为了填满模板而回答无关问题：

| 任务类型 | 建议提供的信息 | 可以提出的要求 |
| --- | --- | --- |
| 洞察与策略 | 账号现状、内容领域、目标人群、数据表现 | 给出洞察、定位方案、排期建议 |
| 热点与选题 | 领域、发布平台、近期关注方向 | 转成可写选题、每条给依据 |
| 写稿 | 完整选题或文稿、平台、受众、素材材料 | 产出可发布稿、按平台换算 |
| 发布审核 | 准备发布的完整内容与平台 | 标出风险位置并给最小改法 |
| 爆款拆解 | 对标爆文、自己的文稿、账号定位 | 说明差距、给可复用结构结论 |
| 复用 | 已验证的选题或稿子 | 拆出十个不同角度 |

例如，选题问题可以这样描述：

```text
/molu-topic 做面向刚入职场人群的号，关注方向是存钱与副业。给我 20 个选题，每条带靶子、切入角度和为什么有人看的依据。
```

如果任务需要本地文件、联网抓取或外部服务，Agent 还必须具备相应的工具或凭证。

## 按任务查找 Skill

> 排序依据：本表按主管道 flow 顺序排，不是面板的字典序；面板里的实际展示位次见各模块 description 开头的 ①→⑪。

| 当前要做的事 | 入口 | 用途 |
| --- | --- | --- |
| 不确定该从哪一步开始 | [`/molu-console`](molu/console/SKILL.md) | 显示管道图、判断环节、调度模块 |
| 搞清读者是谁、痛点在哪 | [`/molu-insight`](molu/insight/SKILL.md) | 区分观察与洞察，四层拆解读者的卡点 |
| 定账号定位、节奏与形式 | [`/molu-strategy`](molu/strategy/SKILL.md) | 定位置、人群、节奏、形式，含「不做什么」 |
| 抓热点并转成选题 | [`/molu-radar`](molu/radar/SKILL.md) | 采集实时热榜，红线过滤，给出可写角度 |
| 生成一批选题 | [`/molu-topic`](molu/topic/SKILL.md) | 20 个选题，每条带靶子与依据 |
| 一个主题持续产出 | [`/molu-reuse`](molu/reuse/SKILL.md) | 十个不同角度，五种换角度方式 |
| 写长文或图文 | [`/molu-writer`](molu/writer/SKILL.md) | 按平台规格产出可发布稿 |
| 写口播脚本 | [`/molu-video`](molu/video/SKILL.md) | 前 3 秒钩子、分镜、字幕切分 |
| 发布前审核 | [`/molu-guard`](molu/guard/SKILL.md) | 法律/伦理/平台三层排查，三档结论，只读 |
| 拆解爆款与诊断 | [`/molu-teardown`](molu/teardown/SKILL.md) | 12 指标 + 百分位定位，基于实测基线 |
| 审视写作决策 | [`/molu-lens`](molu/lens/SKILL.md) | 用内容从业者判断标准审视决策，贯穿全程 |

## 仓库资料

安装 Skills 与阅读仓库资料是两种不同的使用方式。方法论与脚本可在仓库中直接查阅；语料素材不入库。

| 资料 | 用途 |
| --- | --- |
| [数据层 kb.py](molu/kb.py) | 语料查询与语料源接入的实现入口（脚本内含使用说明） |
| [方法论正本](molu/references/外部方法论库.md) | 4A / STP / JTBD 等外部框架的章节索引 |
| [拆解基线](molu/teardown/references/dist.json) | 899 篇实测分布，供偏离度诊断 |
| [语料源接入校验](molu/scripts/inlet_check.py) | 自建语料源的接入口径与拒绝规则 |
| [更新记录](https://github.com/GeneMcGill/molu/commits/main) | 查看提交历史与版本变更 |

## 更新、问题与支持

### 更新

已安装 molu 时，在 Agent 对话中说：

```text
更新 molu
```

或重新执行安装命令覆盖。版本与变更见 [Releases](https://github.com/GeneMcGill/molu/releases)

### 获取帮助

- [提交问题或建议](https://github.com/GeneMcGill/molu/issues)
- 引擎完整文档：[molu/README.md](molu/README.md)

## 数据与方法来源（致谢）

本引擎不是凭空设计，来源分三类，全部显式说明：

**语料与方法归纳**

- 咪蒙自述与公开公众号原文（899 篇，2015-09 ~ 2018-12）。本仓库方法论中的中文情绪写作规律（结构、钩子、转折、情绪放大等）**由这批公开文本归纳而来**，原始版权属于作者及原公众号，本包不含任何逐字引用
- 语料蒸馏的操作规范与质量控制方法（单元冻结、词表唯一真源、逐字校验）为本项目独立实践

**框架借鉴**

方法论不是纯经验，与以下公开方法体系交叉验证过：

- 4A 工作流（Account Planning / Brand Strategy / SPJ 伦理原则）
- STP 定位模型与 Aaker 品牌资产模型
- JTBD（Jobs to Be Done）用户任务视角
- 金字塔原理（结构化表达）
- 发布安全参考：IAB Brand Safety / GARM 12 类、Fact-checking 流程
- 分析视角：AARRR、HEART、高低语境等（详见 [外部方法论库](molu/references/外部方法论库.md)）

**结构与生态**

- README 结构与“ Skill 包 + 数据层”的分发形态参考了 [dontbesilent2025/dbskill](https://github.com/dontbesilent2025/dbskill)（CC BY-NC 4.0），并修复了我们已经证实的原子化截断等问题

以上列举仅为说明方法论来源与关联，不意味着这些组织或作者自身为本项目背书。若任何来源希望被调整引用或删除，可开 issue，我们会快速处理。

## 许可证

本项目方法论采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.zh) 许可证。个人学习、研究和非商业使用请注明来源；商业用途请联系作者获取授权

**内容边界**：本仓库不含任何逐字语料。使用本引擎创作并发出的内容，请替换为自己的原创表述；不编造案例、不承诺流量
