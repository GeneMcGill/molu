# Changelog / 更新日志

All notable changes to **molu** are documented here. See the schema used by each version below.

The format follows **[readme-harness §5 Version discipline](https://github.com/GeneMcGill/readme-harness)**: keep release notes out of the README, reference them from a dedicated CHANGELOG linked by the version badge.

<!-- CHANGELOG-LIST: versions in this project are tagged on GitHub Releases. -->

## v1.0.3 — 2025 (unreleased tag)

### 新增 / Added
- **install.sh 拓扑自检 (install.sh topology self-check)**: when the resolved target directory is the same as the source directory (e.g. `~/.claude/skills` is itself a symlink to the repo), symlink writing is **skipped** with a hint to use `install.sh agents` for a physical install — preventing `molu-*` self-referencing dead links.

### 修复 / Fixed
- Prevent `molu-*` self-referencing dead links when the skills directory is an in-place symlink.

## v1.0.2

### 变更 / Changed
- Module names stay as clean `molu-<module>` (no numbering).
- Panel ordering is alphabetical by agent; pipeline order is marked `①→⑪` at the start of each module description.
- Descriptions tightened to short phrases.
- Badges trimmed to **Version / Skills / License**.

## v1.0.1

- `/molu` popup-list display optimized: numbered names `molu-01→11`, version badge `1.0.1`.

## v1.0.0

- **墨炉 molu v1.0.0 公开发布层**: 11 modules of methodology + `kb.py` data layer + `install.sh`.
- No verbatim corpus committed.

---

See [Releases](https://github.com/GeneMcGill/molu/releases) for the authoritative tagged versions.