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

# Config files（不含密钥的配置可以同步，含密钥的跳过）
echo "[3/3] 配置文件 → ~/.config/opencode/"
mkdir -p "$TARGET"
[ -f "$SCRIPT_DIR/AGENTS.md" ] && cp "$SCRIPT_DIR/AGENTS.md" "$TARGET/" && echo "  AGENTS.md"
if [ -f "$SCRIPT_DIR/opencode.json" ]; then
    echo "  opencode.json (跳过，含 API Key，避免覆盖本地密钥)"
    echo "  如需同步，手动执行: cp $SCRIPT_DIR/opencode.json ~/.config/opencode/"
fi
[ -f "$SCRIPT_DIR/oh-my-opencode.json" ] && cp "$SCRIPT_DIR/oh-my-opencode.json" "$TARGET/" && echo "  oh-my-opencode.json"
[ -f "$SCRIPT_DIR/tui.json" ] && cp "$SCRIPT_DIR/tui.json" "$TARGET/" && echo "  tui.json"

echo ""
echo "=== 完成 ==="
