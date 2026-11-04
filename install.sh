#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FULL=0
TOOL="codex"
for arg in "$@"; do
  case "$arg" in
    --full) FULL=1 ;;
    --claude) TOOL="claude" ;;
    -h|--help)
      echo "用法: bash install.sh [--full] [--claude]"
      echo "  --full    同时安装 PNG 截图组件（Playwright + Chromium，约 150MB）"
      echo "  --claude  安装为 Claude Code 技能（~/.claude/skills/），默认安装为 Codex 技能（~/.codex/skills/）"
      exit 0 ;;
    *) echo "未知参数: $arg（用 --help 查看用法）"; exit 1 ;;
  esac
done

if [ "$TOOL" = "claude" ]; then
  SKILLS_HOME="${CLAUDE_HOME:-$HOME/.claude}/skills"
else
  SKILLS_HOME="${CODEX_HOME:-$HOME/.codex}/skills"
fi
TARGET_DIR="$SKILLS_HOME/face-consultation-report"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "AI 美学升级报告安装器"
echo "仓库目录: $ROOT_DIR"
echo "安装目录: $TARGET_DIR"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "未找到 Python: $PYTHON_BIN"
  echo "请先安装 Python 3.10+，或设置 PYTHON_BIN=/path/to/python3 后重试。"
  exit 1
fi

if [ -d "$TARGET_DIR" ]; then
  BACKUP_DIR="${TARGET_DIR}.backup.$(date +%Y%m%d-%H%M%S)"
  echo "发现已存在安装目录，备份到: $BACKUP_DIR"
  mv "$TARGET_DIR" "$BACKUP_DIR"
fi

mkdir -p "$TARGET_DIR" "$BIN_DIR"

cp "$ROOT_DIR/skill/SKILL.md" "$TARGET_DIR/SKILL.md"
cp -R "$ROOT_DIR/skill/agents" "$TARGET_DIR/agents"
cp -R "$ROOT_DIR/skill/references" "$TARGET_DIR/references"
cp -R "$ROOT_DIR/scripts" "$TARGET_DIR/scripts"
cp -R "$ROOT_DIR/legacy" "$TARGET_DIR/legacy"
mkdir -p "$TARGET_DIR/knowledge"
cp "$ROOT_DIR/knowledge/README.md" "$TARGET_DIR/knowledge/README.md"
if [ -d "${BACKUP_DIR:-}/knowledge" ]; then
  cp -R "$BACKUP_DIR/knowledge/." "$TARGET_DIR/knowledge/" && echo "已保留你之前放在 knowledge/ 里的资料"
fi
cp -R "$ROOT_DIR/templates" "$TARGET_DIR/templates"
cp "$ROOT_DIR/requirements.txt" "$TARGET_DIR/requirements.txt"
cp "$ROOT_DIR/README.md" "$TARGET_DIR/README.md"
cp "$ROOT_DIR/PRIVACY.md" "$TARGET_DIR/PRIVACY.md"
cp "$ROOT_DIR/LICENSE" "$TARGET_DIR/LICENSE"

rm -rf "$TARGET_DIR/scripts/__pycache__"

echo "创建 Python 虚拟环境..."
"$PYTHON_BIN" -m venv "$TARGET_DIR/.venv"
"$TARGET_DIR/.venv/bin/python" -m pip install --upgrade pip >/dev/null
"$TARGET_DIR/.venv/bin/python" -m pip install -r "$TARGET_DIR/requirements.txt"

cat > "$BIN_DIR/face-report-v2" <<EOF
#!/usr/bin/env bash
set -euo pipefail
"$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/scripts/render_sales_v2.py" "\$@"
EOF
chmod +x "$BIN_DIR/face-report-v2"

cat > "$BIN_DIR/face-report-basic" <<EOF
#!/usr/bin/env bash
set -euo pipefail
"$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/legacy/render_report.py" "\$@"
EOF
chmod +x "$BIN_DIR/face-report-basic"

cat > "$BIN_DIR/face-report-handoff" <<EOF
#!/usr/bin/env bash
set -euo pipefail
"$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/scripts/build_handoff_sheet.py" "\$@"
EOF
chmod +x "$BIN_DIR/face-report-handoff"

"$TARGET_DIR/.venv/bin/python" "$ROOT_DIR/scripts/validate_install.py" --target "$TARGET_DIR"

if [ "$FULL" = "1" ]; then
  echo "安装 PNG 截图组件（Playwright + Chromium）..."
  if "$TARGET_DIR/.venv/bin/python" -m pip install "playwright>=1.40,<2" "python-docx>=1.0,<2" "openpyxl>=3.1,<4" \
     && "$TARGET_DIR/.venv/bin/python" -m playwright install chromium; then
    echo "截图组件安装完成，可以导出 report-v2.png。"
  else
    echo "【提示】截图组件安装失败（常见原因：网络无法下载 Chromium）。"
    echo "不影响生成 HTML 报告；网络正常后可重新运行：bash install.sh --full"
  fi
else
  echo "提示：未安装 PNG 截图组件。需要导出 report-v2.png 时运行：bash install.sh --full"
fi

echo
echo "安装完成。"
echo "技能目录（$TOOL）: $TARGET_DIR"
echo "命令行入口: $BIN_DIR/face-report-v2"
echo "          : $BIN_DIR/face-report-handoff （生成含四图的网资沟通总表）"
echo
echo "如果终端提示找不到 face-report-v2，请执行："
echo "export PATH=\"$BIN_DIR:\$PATH\""
echo
echo "渲染示例："
echo "face-report-v2 --manifest /absolute/path/manifest.json --out /absolute/path/output-folder"
