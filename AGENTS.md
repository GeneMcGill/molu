# AGENTS.md — AI working contract

> Generated following [Readme Harness](https://github.com/Guislabert/readme-harness) conventions.
> An AI coding agent reads this file when it starts work in this repository.

## Project

- **Name**: `molu`
- **Kind**: AI Agent Skills pack (Chinese-language content production engine)
- **Version**: `1.0.3`
- **CI**: GitHub Actions (`.github/workflows/ci.yml`)

## README discipline (enforced, not optional)

- Keep `README.md` in **English (en-GB)**; other languages live in separate
  `README.<lang>.md` files (e.g. `README.zh-CN.md`), never inline.
- Keep every README **Version badge** in sync:
  `package.json.version` === `CHANGELOG newest section` === `README badges`
  (run `node tools/version-check.mjs`).
- Version bumps are release points (SemVer): fix → PATCH, backward-compatible
  feature → MINOR, breaking change → MAJOR.

## Badge row

The header badge row follows the `badges-google` semantic palette:
CI `#34A853` · Version `#4285F4` · License `#FBBC05`. Order:
built → versioned → published → licensed → meta. Centered inside a
`<div align="center">` below the hero image.

## Structure

- `molu/` — the 11 Skill modules (`console`, `insight`, `strategy`, `radar`,
  `topic`, `reuse`, `writer`, `video`, `guard`, `teardown`, `lens`), each with
  its own `SKILL.md`.
- `molu/kb.py` — unified data layer (corpus queries, source connection).
- `molu/install.sh` — installer (`agents` / `all` / per-agent).
- `assets/hero-*.svg` — readme-harness hero image (light / dark).

## Content boundary

- This repo contains **no verbatim corpus**. When using the engine to create
  and publish content, replace output with original phrasing; never fabricate
  cases; never promise traffic numbers.

## Testing

- Run `node tools/version-check.mjs` before relying on a change.
- Any user-facing example in a README must reflect a real, runnable module
  interaction.