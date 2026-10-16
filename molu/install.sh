#!/usr/bin/env bash
# 墨炉 molu 安装脚本
#
# 安装约定（跟随本机既有做法，见 dbs-install-skill）：
#   ~/.agents/skills 是「源」，放实体目录
#   其他 agent 目录放软链，指回源 —— 避免同一 skill 多入口、避免副本分叉
#
# 用法:
#   bash install.sh                  # 交互式
#   bash install.sh all              # 源 + 软链到 pi / claude / codex
#   bash install.sh pi               # 源 + 软链到 pi
#   bash install.sh agents           # 只装源（~/.agents/skills）
#   bash install.sh uninstall        # 全部卸载
#   bash install.sh status           # 查看安装状态
#   bash install.sh pi --single writer   # 只装单个模块
#   KOTO_SOURCE=/path bash install.sh agents   # 自定义源位置

set -eo pipefail   # 不用 -u：bash 3.2 兼容

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="molu-"
# 安装顺序即管道顺序：总控→洞察→策略→雷达→选题→复用→写稿→短视频→审核→拆解→视角。
# 面板按名称字典序展示，整体顺序在面板中不可控；模块在 description 开头用 ①→⑪ 标注流程位次。
MODULES="console insight strategy radar topic reuse writer video guard teardown lens"
SOURCE_DIR="${KOTO_SOURCE:-$HOME/.agents/skills}"
# 安装后的最终名：molu-<模块>，不插序号，不插序号
skill_name() { printf '%s%s' "$PREFIX" "$1"; }

# 用函数代替关联数组，兼容 bash 3.2
target_path() {
  case "$1" in
    agents) echo "$HOME/.agents/skills" ;;
    pi)     echo "$HOME/.pi/agent/skills" ;;
    claude) echo "$HOME/.claude/skills" ;;
    codex)  echo "$HOME/.codex/skills" ;;
    *)      echo "" ;;
  esac
}

log()  { printf '%s\n' "$*"; }
ok()   { printf '  [ok] %s\n' "$*"; }
warn() { printf '  [!!] %s\n' "$*" >&2; }
step() { printf '\n== %s ==\n' "$*"; }

# ---------- 装源（实体目录）
install_source() {
  mkdir -p "$SOURCE_DIR"
  install -m 644 "$SRC/kb.py" "$SOURCE_DIR/kb.py"
  if [ -d "$SRC/inlets" ]; then
    rm -rf "$SOURCE_DIR/inlets"
    cp -R "$SRC/inlets" "$SOURCE_DIR/inlets"
  fi
  rm -rf "$SOURCE_DIR/scripts"
  mkdir -p "$SOURCE_DIR/scripts"
  cp -f "$SRC/scripts/"*.py "$SOURCE_DIR/scripts/" 2>/dev/null || true

  local n=0
  for m in $USE_MODULES; do
    local target="$SOURCE_DIR/$(skill_name "$m")"
    rm -rf "$target"
    mkdir -p "$target"
    cp -R "$SRC/$m/." "$target/"
    if [ -f "$target/SKILL.md" ]; then
      python3 - "$target/SKILL.md" "$SOURCE_DIR" <<'PYEOF'
import os, sys
path, dst = sys.argv[1], sys.argv[2]
name = os.path.basename(os.path.dirname(path))
out, seen = [], False
for l in open(path, encoding='utf-8').read().split('\n'):
    st = l.strip()
    # KB_ROOT 一律写死为源目录（软链可穿透，各 agent 共用一份数据）
    if st.startswith('KB_ROOT=') or st.startswith('[ -d "$KB_ROOT/inlets" ]'):
        if seen:
            continue
        out.append(f'KB_ROOT="{dst}"')
        seen = True
    # name 与目录名一致（规范：其他 Agent Skills 实现可能强制要求匹配）
    elif st.startswith('name:'):
        out.append(f'name: {name}')
    else:
        out.append(l)
open(path, 'w', encoding='utf-8').write('\n'.join(out))
PYEOF
    fi
    n=$((n+1))
  done
  ok "共享层 + $n 个模块（实体）→ $SOURCE_DIR"
}

# ---------- 建软链（其他 agent 目录）
link_target() {
  local dst="$1" n=0
  mkdir -p "$dst"
  for m in $USE_MODULES; do
    local name; name="$(skill_name "$m")"
    local t="$dst/$name"
    [ -e "$t" ] && [ ! -L "$t" ] && rm -rf "$t"   # 清掉旧实体目录
    ln -sfn "$SOURCE_DIR/$name" "$t"
    n=$((n+1))
  done
  for f in kb.py inlets; do
    local t="$dst/$f"
    [ -e "$t" ] && [ ! -L "$t" ] && rm -rf "$t"
    ln -sfn "$SOURCE_DIR/$f" "$t"
  done
  ok "$n 个模块软链 + 共享层 → $dst"
}

# ---------- 卸载
uninstall_from() {
  local dst="$1" n=0
  [ -d "$dst" ] || return 0
  for m in $MODULES; do
    # 兼容清理：旧版 molu-console（无序号）与现有编号命名
    local t="$dst/$PREFIX$m"
    if [ -L "$t" ]; then rm -f "$t"; n=$((n+1))
    elif [ -d "$t" ]; then rm -rf "$t"; n=$((n+1)); fi
    t="$dst/$(skill_name "$m")"
    if [ -L "$t" ]; then rm -f "$t"; n=$((n+1))
    elif [ -d "$t" ]; then rm -rf "$t"; n=$((n+1)); fi
  done
  for f in kb.py inlets scripts; do
    local t="$dst/$f"
    if [ "$dst" = "$SOURCE_DIR" ]; then rm -rf "$t"
    elif [ -L "$t" ]; then rm -f "$t"; fi
  done
  ok "$n 个模块"
}

# ---------- 状态
show_status() {
  log "源目录: $SOURCE_DIR"
  if [ -d "$SOURCE_DIR" ]; then
    local c=0
    for m in $MODULES; do [ -e "$SOURCE_DIR/$(skill_name "$m")" ] && c=$((c+1)); done
    log "  实体模块: $c / $(echo $MODULES | wc -w | tr -d ' ')"
  else
    log "  （未安装）"
  fi
  for k in agents pi claude codex; do
    local dst; dst="$(target_path "$k")"
    [ -d "$dst" ] || { printf '  %-10s ⬜ 目录不存在\n' "$k"; continue; }
    local c=0 r=0
    for m in $MODULES; do
      local t="$dst/$(skill_name "$m")"
      if [ -L "$t" ]; then c=$((c+1)); elif [ -d "$t" ]; then r=$((r+1)); fi
    done
    printf '  %-10s %s 软链 %s / 实体 %s\n' "$k" "$dst" "$c" "$r"
  done
}

# ---------- 主流程
TARGET="${1:-}"
SINGLE=""
[ "${2:-}" = "--single" ] && SINGLE="${3:-}"

if [ -z "$TARGET" ]; then
  log "选择操作："
  log "  1) all        源 + 软链到 pi / claude / codex"
  log "  2) agents     只装源（~/.agents/skills）"
  log "  3) pi         源 + 软链到 pi"
  log "  4) status     查看状态"
  log "  5) uninstall  卸载"
  printf '> '
  read -r choice
  case "$choice" in
    1) TARGET="all";; 2) TARGET="agents";; 3) TARGET="pi";;
    4) TARGET="status";; 5) TARGET="uninstall";;
    *) warn "无效选择"; exit 1;;
  esac
fi

[ "$TARGET" = "status" ] && { step "安装状态"; show_status; exit 0; }

[ "$TARGET" = "uninstall" ] && {
  step "卸载"
  for k in pi claude codex agents; do
    printf '[%s]\n' "$k"
    uninstall_from "$(target_path "$k")"
  done
  exit 0
}

# 模块集（支持 --single）
USE_MODULES="$MODULES"
if [ -n "$SINGLE" ]; then
  if echo " $MODULES " | grep -q " $SINGLE "; then
    USE_MODULES="$SINGLE"
  else
    warn "未知模块: $SINGLE"
    log "  可用: $MODULES"
    exit 1
  fi
fi

# 目标展开
case "$TARGET" in
  all)             LINKS="pi claude codex" ;;
  agents)          LINKS="" ;;
  pi|claude|codex) LINKS="$TARGET" ;;
  *) warn "未知目标: $TARGET"; exit 1 ;;
esac

step "安装源: $SRC"
step "源目录: $SOURCE_DIR"
install_source

for k in $LINKS; do
  dst="$(target_path "$k")"
  step "软链: $k → $dst"
  link_target "$dst"
done

step "完成"
log ""
log "调用方式（输入 /molu 过滤面板；管道位置见各模块 description 开头的 ①→⑪）："
log "  /molu-console  这套东西能干嘛"
log "  /molu-writer   帮我写一篇"
log "  /molu-guard    这篇能发吗"
log ""
log "数据层: ${SOURCE_DIR}/kb.py + inlets（所有 agent 共用一份）"
log "查看状态: bash install.sh status"
