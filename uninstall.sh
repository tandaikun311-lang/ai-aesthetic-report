#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "--claude" ]; then
  TARGET_DIR="${CLAUDE_HOME:-$HOME/.claude}/skills/face-consultation-report"
else
  TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills/face-consultation-report"
fi
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

echo "卸载 AI 美学升级报告"

if [ -d "$TARGET_DIR" ]; then
  rm -rf "$TARGET_DIR"
  echo "已删除: $TARGET_DIR"
else
  echo "未找到安装目录: $TARGET_DIR"
fi

rm -f "$BIN_DIR/face-report-v2" "$BIN_DIR/face-report-basic" "$BIN_DIR/face-report-handoff"
echo "已删除命令行入口。"
