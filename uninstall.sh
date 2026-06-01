#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
TARGET_DIR="$CODEX_HOME/skills/face-consultation-report"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

echo "卸载 AI 美学升级报告"

if [ -d "$TARGET_DIR" ]; then
  rm -rf "$TARGET_DIR"
  echo "已删除: $TARGET_DIR"
else
  echo "未找到安装目录: $TARGET_DIR"
fi

rm -f "$BIN_DIR/face-report-v2" "$BIN_DIR/face-report-basic"
echo "已删除命令行入口。"
