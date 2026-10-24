<div align="center">

<a href="https://github.com/Guislabert/molu">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img alt="molu 墨炉" src="assets/hero-light.svg" width="820">
  </picture>
</a>

</div>

<h1 align="center">molu 墨炉</h1>

<div align="center">

> A **Chinese-language content production engine** packaged as AI Agent Skills — one package, eleven modules, from insight to review. Works with Claude Code, Codex, WorkBuddy and other Skills-compatible Agents.

</div>

<div align="center">

[![CI](https://img.shields.io/badge/CI-passing-34A853.svg)][ci]
[![Version](https://img.shields.io/badge/Version-1.0.3-4285F4.svg)][vlg]
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License%3A%20CC%20BY--NC%204.0-FBBC05.svg)][osi]

`#content-engine` `#ai-skills` `#11-modules` `#deep-first` `#中文内容`

</div>

> [!NOTE]
> Distilled from 899 public WeChat Official Account articles (2015-09 ~ 2018-12, 2.13M characters) — 16,227 content units verified against source text with a 100% match rate.

<div align="center">

English | [简体中文](README.zh-CN.md)

</div>

---

## Why

Producing Chinese content today is a sequence of isolated, re-invented decisions: who are you writing for, how does the trend connect to a timeless pain point, what structure carries the story, is it safe to publish, why did that piece break out. Writing tools help you *type faster*; almost none help you *decide better*.

> **molu 墨炉 is a decision pipeline, not a text generator.** Depth over speed: it turns a content task into a checkable pipeline from insight to review.

## What

molu is a **Chinese-language content production engine** packaged as 11 AI Agent Skills. It covers insight research, strategy positioning, trending-topic selection, writing, pre-publish review, and viral teardown — installable into any Skills-capable AI Agent.

Core belief: **depth over speed**. When you catch a trending topic, first ask what timeless pain point sits underneath it; before generating topics, confirm who you're writing for; after writing, the draft must pass review. It is not a traffic predictor — it delivers checkable methods, not promises.

## Pipeline

```
  原料层  Corpus Source (pluggable — swap sources without touching the engine)
    方法论(4A·咨询框架) · 素材库(16,227 单元) · 实时热榜
                ↓
         kb.py · unified data layer
                ↓
  主管道  Pipeline (①→⑤ in order)
     ① 洞察 insight → ② 策略 strategy → ③ 雷达 radar
     → ④ 选题 topic/reuse → ⑤ 生产 writer/video
                ↓
  收束层  Closing
     ⑥ 审核 guard → ⑦ 拆解 teardown ⇄ back to ①
     ⑧ lens ◈ 视角 — runs throughout
```

## Modules

| # | Module | Purpose |
|---|---|---|
| ① | [`/molu-console`](molu/console/SKILL.md) | Show pipeline map, diagnose stage, dispatch modules |
| ② | [`/molu-insight`](molu/insight/SKILL.md) | Separate observation from insight; analyze reader blockage in four layers |
| ③ | [`/molu-strategy`](molu/strategy/SKILL.md) | Define positioning, audience, cadence, format — including "what NOT to do" |
| ④ | [`/molu-radar`](molu/radar/SKILL.md) | Collect real-time hot lists, filter compliance risks, output writable angles |
| ⑤ | [`/molu-topic`](molu/topic/SKILL.md) | 20 topics, each with target reader and rationale |
| ⑤ | [`/molu-reuse`](molu/reuse/SKILL.md) | Ten different angles, five angle-swapping methods |
| ⑥ | [`/molu-writer`](molu/writer/SKILL.md) | Produce publishable drafts to platform specs |
| ⑥ | [`/molu-video`](molu/video/SKILL.md) | First-3-seconds hook, shot rhythm, caption splitting |
| ⑦ | [`/molu-guard`](molu/guard/SKILL.md) | Legal / ethical / platform three-layer check, three verdict tiers, read-only |
| ⑧ | [`/molu-teardown`](molu/teardown/SKILL.md) | 12 metrics + percentile positioning, based on a measured baseline |
| ◈ | [`/molu-lens`](molu/lens/SKILL.md) | Stress-test writing decisions with practitioner standards, runs throughout |

## Install

Choose a method in your terminal (never send install commands to an Agent as chat content).

### Skills CLI

```bash
npx -y skills add Guislabert/molu -g --all
```

`-g` installs globally; `--all` installs into every Agent the CLI recognises. To target one Agent, drop `--all`.

### install.sh

```bash
bash install.sh agents           # source into ~/.agents/skills
bash install.sh all              # source + symlinks to pi / claude / codex
```

After installing, enter in the Agent chat:

```text
/molu-console what does this do
```

## Quick start

1. **First run** — learn the entry point:

   ```text
   /molu-console what does this do
   ```
   The console maps the pipeline, lists all 11 modules, identifies where you're stuck, and suggests the smallest next step.

2. **Already know what you need** — invoke a module directly:

   ```text
   /molu-topic  I write about money-saving for young professionals. Give me 20 ready-to-write topics, each with an angle and rationale.
   /molu-writer Here's my topic and material. Write a publishable piece to WeChat specs.
   /molu-guard  This piece is going to WeChat. Run the pre-publish review and flag risk spots.
   /molu-teardown Break down why this 100k+ article went viral and show my gaps.
   ```

3. **Connect a corpus source (optional)** — methodology works out of the box; with a source connected, topic / reuse / teardown can cite verified material:

   ```bash
   python3 molu/kb.py stats
   python3 molu/kb.py install <id>
   ```

4. **Refine in the same conversation** — provide new facts; any finished piece goes through `/molu-guard` before publishing.

## Adopting / Contributing

Full engine documentation lives in [`molu/README.md`](molu/README.md). version discipline follows [SemVer 2.0.0](https://semver.org/) and is guarded by `tools/version-check.mjs`.

Methodology provenance and framework acknowledgements (including [dontbesilent2025/dbskill](https://github.com/dontbesilent2025/dbskill)) are detailed under **License**.

## Feedback

Raise an issue for a bug, a module idea, or a question about the method.

[ci]: https://github.com/Guislabert/molu/actions
[vlg]: CHANGELOG.md
[osi]: https://creativecommons.org/licenses/by-nc/4.0/

## License

This project's methodology is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use for personal learning and research must credit the source; commercial use requires contacting the author.

**Content boundary**: this repo contains no verbatim corpus. When using this engine to create content, replace output with your own original phrasing; do not fabricate cases, and do not promise traffic numbers.