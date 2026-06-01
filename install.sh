#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
TARGET_DIR="$CODEX_HOME/skills/face-consultation-report"
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
cp -R "$ROOT_DIR/templates" "$TARGET_DIR/templates"
cp "$ROOT_DIR/requirements.txt" "$TARGET_DIR/requirements.txt"
cp "$ROOT_DIR/README.md" "$TARGET_DIR/README.md"
cp "$ROOT_DIR/PRIVACY.md" "$TARGET_DIR/PRIVACY.md"

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
"$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/scripts/render_report.py" "\$@"
EOF
chmod +x "$BIN_DIR/face-report-basic"

"$TARGET_DIR/.venv/bin/python" "$ROOT_DIR/scripts/validate_install.py" --target "$TARGET_DIR"

echo
echo "安装完成。"
echo "Codex skill: $TARGET_DIR"
echo "命令行入口: $BIN_DIR/face-report-v2"
echo
echo "如果终端提示找不到 face-report-v2，请执行："
echo "export PATH=\"$BIN_DIR:\$PATH\""
echo
echo "渲染示例："
echo "face-report-v2 --manifest /absolute/path/manifest.json --out /absolute/path/output-folder"
