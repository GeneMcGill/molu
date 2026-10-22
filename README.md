# molu 墨炉 (Molu)

English · [简体中文](README.zh-CN.md)

**molu** is a Chinese-language content production engine packaged as AI Agent Skills. It covers insight research, strategy positioning, trending-topic selection, writing, pre-publish review, and viral teardown — installable into any Skills-capable AI Agent.

[![Version](https://img.shields.io/badge/version-1.0.3-2563EB.svg?style=flat-square)](https://github.com/GeneMcGill/molu/releases)
[![Skills](https://img.shields.io/badge/skills-11%20modules-7C3AED.svg?style=flat-square)](#find-a-skill-by-task)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-16A34A.svg?style=flat-square)](#license)

Works with Claude Code, Codex, WorkBuddy, and other Skills-compatible Agents. The methodology is distilled from 899 public WeChat Official Account articles (2015-09 ~ 2018-12, 2.13M characters), with 16,227 content units extracted and verified against source texts with a 100% match rate.

**This release:** v1.0.3 — install.sh topology self-check: when the resolved target directory is the same as the source directory (e.g. ~/.claude/skills is itself a symlink to the repo), symlink writing is skipped with a hint to use 'install.sh agents' for a physical install, preventing molu-* self-referencing dead links. v1.0.2 — module names stay as clean `molu-<module>` (no numbering); panel ordering is alphabetical by agent; pipeline order is marked ①→⑪ at the start of each description; badges trimmed to Version / Skills / License.

## Table of Contents

- [What is molu](#what-is-molu)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Providing Task Material](#providing-task-material)
- [Find a Skill by Task](#find-a-skill-by-task)
- [Repo Resources](#repo-resources)
- [Updates, Issues & Support](#updates-issues--support)
- [License](#license)

## What is molu

A Skill is a set of Agent instructions written for a specific class of tasks. After installing molu, you can invoke `/molu-console` or any specific module in your Agent conversation, e.g. `/molu-writer`.

If you don't know where to start, hand the problem to `/molu-console`. It shows the full pipeline, identifies which stage you're at, decides whether to run insight research, topic generation, writing, or review first, then routes to the right module within the same conversation.

molu's core belief is **depth over speed**: when you catch a trending topic, first ask what timeless pain point sits underneath it; before generating topics, confirm who you're writing for; after writing, the draft must pass review. It is not a traffic predictor — it doesn't promise numbers, it delivers checkable methods and structure.

molu is commonly used to:

- Clarify who your readers are, where they get stuck, and what needs go unmet
- Set positioning, audience cadence, and format strategy
- Capture real-time trends, filter compliance risks, and turn them into writable topics
- Split one theme into ten angles for sustained output
- Produce WeChat long-form articles, image-text posts, and short-video voiceover scripts
- Run legal / ethical / platform three-layer pre-publish review
- Break down why a piece went viral — or why it didn't

## Installation

Choose the installation method that matches your Agent. All install commands run in a terminal — never send them to an Agent as chat content.

### Install with the Skills CLI

Your terminal needs `npx`. Run:

```bash
npx -y skills add GeneMcGill/molu -g --all
```

`-g` installs globally; `--all` installs into every Agent the Skills CLI recognizes. To target a single Agent, drop `--all` and pick the target when prompted.

After installing, enter in your Agent's chat:

```text
/molu-console what does this do
```

### Manual copy installation

If you don't use the CLI, copy the entire `molu/` directory into your Agent's skills directory:

```bash
cp -r molu ~/.agents/skills/molu     # generic Agents
cp -r molu ~/.claude/skills/molu     # Claude Code
cp -r molu ~/.codex/skills/molu      # Codex
```

You can also install a single module: `cp -r molu/writer ~/.claude/skills/`

### Commands not showing after install

First confirm the install command succeeded and the target is the Agent you are actually using. Skill entry names follow what each Agent displays; the panel lists modules alphabetically, and pipeline order is marked ①→⑪ at the start of each module description (①console → ②insight → ③strategy → ④radar → ⑤topic → ⑥reuse → ⑦writer → ⑧video → ⑨guard → ⑩teardown → ⑪lens).

## Getting Started

### First run: learn the entry point

Type in your Agent chat:

```text
/molu-console what does this do
```

The console outputs the pipeline map, lists all 11 modules (01→11 = pipeline order), identifies where you're stuck, and suggests the smallest actionable next step.

### Not sure where to start: hand it to `/molu-console`

Append your situation and question to the command. It doesn't need to be complete — the Agent first decides the stage, then proceeds:

```text
/molu-console I run a career-advice account, three months in, stuck at ~800 reads per post. Should I fix positioning, topic selection, or writing first?
```

### Already know what you need: invoke a module directly

Append your question, material, and desired output:

```text
/molu-topic I write about money-saving for young professionals. Give me 20 ready-to-write topics, each with an angle and supporting rationale.
```

```text
/molu-writer Here's my topic and material. Write a publishable piece to WeChat specs.
```

```text
/molu-guard This piece is going to WeChat. Run the pre-publish review and flag risk spots.
```

```text
/molu-teardown Break down why this 100k+ article went viral and show my gaps.
```

### Connecting a corpus source (optional but recommended)

Module methodology works out of the box; with a corpus source connected, the topic, reuse, and teardown modules can cite measured, verified material. The corpus layer is **pluggable**: swapping sources doesn't affect the engine. Full details in the [data-layer README](molu/README.md):

```bash
python3 molu/kb.py stats             # view current data
python3 molu/kb.py install <id>      # connect a corpus source (with caliber validation)
```

### After receiving a result: continue in the same conversation

If the output needs refinement, provide new facts, material, or revision notes directly in the current conversation — the same module picks it up. Any finished piece goes through `/molu-guard` before publishing, and it has the authority to say "don't post this."

## Providing Task Material

Output quality depends on the facts, material, and Agent tool permissions you provide. Don't answer irrelevant questions just to fill a template:

| Task type | Suggested info to provide | Requests you can make |
| --- | --- | --- |
| Insight & strategy | Account status, content niche, target audience, performance data | Deliver insights, a positioning plan, a publishing schedule |
| Trends & topics | Niche, publishing platform, current focus areas | Convert to writable topics, each with rationale |
| Writing | Full topic or draft, platform, audience, source material | Deliver a publishable piece, adapted per platform |
| Pre-publish review | Complete content and target platform | Flag risk spots with minimal fixes |
| Viral teardown | Benchmark hit piece(s), your draft, account positioning | Describe gaps, extract reusable structural conclusions |
| Reuse | A validated topic or draft | Split into ten different angles |

Example of describing a topic-generation task:

```text
/molu-topic Account targets early-career professionals, focused on saving money and side hustles. Give me 20 topics, each with the target reader, entry angle, and why it will get attention.
```

If the task needs local files, web scraping, or external services, the Agent must also have the respective tools or credentials.

## Find a Skill by Task

> Ordering note: this table follows the main pipeline flow order, not the panel's alphabetical order; each module's actual panel position is marked ①→⑪ at the start of its description.

| What you want to do | Entry | Purpose |
| --- | --- | --- |
| Not sure which step to start from | [`/molu-console`](molu/console/SKILL.md) | Show pipeline map, diagnose stage, dispatch modules |
| Understand your readers and their pain points | [`/molu-insight`](molu/insight/SKILL.md) | Separate observation from insight, analyze reader blockage in four layers |
| Set positioning, cadence, and format | [`/molu-strategy`](molu/strategy/SKILL.md) | Define positioning, audience, cadence, format — including "what NOT to do" |
| Catch trends and convert to topics | [`/molu-radar`](molu/radar/SKILL.md) | Collect real-time hot lists, filter compliance risks, output writable angles |
| Generate a batch of topics | [`/molu-topic`](molu/topic/SKILL.md) | 20 topics, each with target reader and rationale |
| Sustained output on one theme | [`/molu-reuse`](molu/reuse/SKILL.md) | Ten different angles, five angle-swapping methods |
| Write long-form or image-text pieces | [`/molu-writer`](molu/writer/SKILL.md) | Produce publishable drafts to platform specs |
| Write voiceover scripts | [`/molu-video`](molu/video/SKILL.md) | First-3-seconds hook, shot rhythm, caption splitting |
| Pre-publish review | [`/molu-guard`](molu/guard/SKILL.md) | Legal / ethical / platform three-layer check, three verdict tiers, read-only |
| Break down hits & diagnose | [`/molu-teardown`](molu/teardown/SKILL.md) | 12 metrics + percentile positioning, based on a measured baseline |
| Review writing decisions | [`/molu-lens`](molu/lens/SKILL.md) | Stress-test writing decisions with practitioner standards, runs throughout |

## Repo Resources

Installing Skills and reading repo materials are two different usage modes. Methodology and scripts can be read directly in the repo; corpus material is not committed.

| Resource | Purpose |
| --- | --- |
| [Data layer kb.py](molu/kb.py) | Implementation entry for corpus queries and source connection (usage notes inside the script) |
| [Methodology compendium](molu/references/外部方法论库.md) | Chapter index for 4A / STP / JTBD and other external frameworks |
| [Teardown baseline](molu/teardown/references/dist.json) | Measured distribution of 899 articles, for deviation diagnostics |
| [Corpus source validation](molu/scripts/inlet_check.py) | Ingestion calibers and rejection rules for self-built corpus sources |
| [Commit history](https://github.com/GeneMcGill/molu/commits/main) | View history and version changes |

## Updates, Issues & Support

### Updates

If molu is already installed, say in your Agent chat:

```text
update molu
```

Or re-run the install command to overwrite. Version and changes: [Releases](https://github.com/GeneMcGill/molu/releases)

### Getting help

- [Open issues or suggestions](https://github.com/GeneMcGill/molu/issues)
- Full engine documentation: [molu/README.md](molu/README.md)

## Data & Methodology Sources (Acknowledgments)

This engine is not designed from thin air. Sources fall into three categories, all explicitly stated:

**Corpus and method induction**

- Miaomeng (咪蒙) self-accounts and public WeChat Official Account originals (899 articles, 2015-09 ~ 2018-12). The Chinese emotional-writing patterns in this repo's methodology (structure, hooks, pivots, emotion amplification, etc.) are **induced from those public texts**; original copyright belongs to the authors and their accounts, and the package contains no verbatim quotation.
- The corpus distillation operational standards and quality-control methods (unit freezing, single-source vocabulary, verbatim verification) are independent practices of this project.

**Framework cross-referencing**

The methodology is not pure experience — it was cross-validated against these public method systems:

- 4A workflow (Account Planning / Brand Strategy / SPJ ethics principles)
- STP positioning model and Aaker brand equity model
- JTBD (Jobs to Be Done) user-task perspective
- Pyramid Principle (structured expression)
- Publishing safety references: IAB Brand Safety / GARM 12 categories, fact-checking workflow
- Analytical lenses: AARRR, HEART, high/low-context communication (see the [external methodology compendium](molu/references/外部方法论库.md) for details)

**Structure & ecosystem**

- The README structure and the "Skill package + data layer" distribution form reference [dontbesilent2025/dbskill](https://github.com/dontbesilent2025/dbskill) (CC BY-NC 4.0), with fixes for the atomic-truncation issues we have verified.

The above listings explain methodology provenance and associations only — they do not imply endorsement by these organizations or authors. If any source wishes to be adjusted or removed from the citations, open an issue and we'll act on it quickly.

## License

This project's methodology is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Non-commercial use for personal learning and research must credit the source; commercial use requires contacting the author for authorization.

**Content boundary**: this repo contains no verbatim corpus. When using this engine to create and publish content, replace output with your own original phrasing; do not fabricate cases, and do not promise traffic numbers.
