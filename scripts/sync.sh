#!/bin/bash
# sync.sh - 从 GitHub 拉取最新配置并同步到 ~/.config/opencode/
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$HOME/.config/opencode"

echo "=== 同步 OpenCode 配置 ==="
echo ""

# Agents
echo "[1/3] Agents → ~/.config/opencode/agents/"
mkdir -p "$TARGET/agents"
for f in "$SCRIPT_DIR/agents/"*.md; do
    [ -f "$f" ] && cp "$f" "$TARGET/agents/" && echo "  $(basename "$f")"
done

# Skills
echo "[2/3] Skills → ~/.config/opencode/skills/"
mkdir -p "$TARGET/skills"
for d in "$SCRIPT_DIR/skills/"*/; do
    [ -d "$d" ] && cp -r "$d" "$TARGET/skills/" && echo "  $(basename "$d")"
done
for f in "$SCRIPT_DIR/skills/"*.skill; do
    [ -f "$f" ] && cp "$f" "$TARGET/skills/" && echo "  $(basename "$f")"
done

# Config files
echo "[3/3] 配置文件 → ~/.config/opencode/"
mkdir -p "$TARGET"
[ -f "$SCRIPT_DIR/AGENTS.md" ] && cp "$SCRIPT_DIR/AGENTS.md" "$TARGET/" && echo "  AGENTS.md"
[ -f "$SCRIPT_DIR/opencode.json" ] && cp "$SCRIPT_DIR/opencode.json" "$TARGET/" && echo "  opencode.json"
[ -f "$SCRIPT_DIR/oh-my-opencode.json" ] && cp "$SCRIPT_DIR/oh-my-opencode.json" "$TARGET/" && echo "  oh-my-opencode.json"
[ -f "$SCRIPT_DIR/tui.json" ] && cp "$SCRIPT_DIR/tui.json" "$TARGET/" && echo "  tui.json"

echo ""
echo "=== 完成 ==="
