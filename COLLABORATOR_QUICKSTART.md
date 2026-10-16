# Collaborator Quickstart

目标：不准备任何客户照片，先确认仓库能安装、命令能运行、标准 V2 版式的合成 demo 能渲染。使用范围见 `LICENSE`。

## 1. 克隆仓库

```bash
cd ~/Downloads
git clone https://github.com/tandaikun311-lang/ai-aesthetic-report.git
cd ai-aesthetic-report
```

当前仓库公开可访问。作者授权的协作者可按此流程安装使用；公开可访问不等于允许任意再分发。

## 2. 一键自检

这一步不安装到 Codex，只验证当前仓库文件、依赖和 demo 渲染：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/self_check.py
open outputs/self-check-demo/report-v2.html
```

看到 `report-v2.html`，说明以下链路已通过：

- 仓库文件完整。
- Python 脚本可编译。
- Pillow 可导入。
- `sample/manifest.demo.json` 可读取。
- 合成 demo 输入可复制到输出目录。
- V2 HTML 报告可生成。

## 3. 安装后验证

```bash
bash install.sh
~/.local/bin/face-report-v2 \
  --manifest sample/manifest.demo.json \
  --out outputs/demo-install-check \
  --no-screenshot
open outputs/demo-install-check/report-v2.html
```

看到安装后的 demo 报告，说明 `face-report-v2` 命令行入口可用。

## 4. 预期输出

自检输出：

```text
outputs/self-check-demo/
  00_交付入口.html
  report-v2.html
  assets/
```

安装后验证输出：

```text
outputs/demo-install-check/
  00_交付入口.html
  report-v2.html
  assets/
```

默认不生成 PNG，避免第一次验证被 Playwright 或浏览器安装卡住。需要 PNG 时再运行：

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/self_check.py --with-screenshot
```

生成的合成 `report-v2.png` 应保留原版 V2 页头、左侧四条观察、两张大人像、右侧项目映射，以及底部设计思路和三条建议。宽度应为 3200 像素；具体标准见 `skill/references/canonical-v2-layout.md`。此 demo 只检验版式与程序链路，不代表真人报告已经完成。

## 5. 隐私边界

`sample/demo-inputs/` 是合成 SVG 占位图，不对应任何真实人物。

不要提交以下内容到 GitHub：

- 客户原图。
- AI 效果图。
- 效果标记图。
- 报告截图。
- 含客户姓名、电话、微信、门店信息的文件。

真实客户项目请复制 `sample/manifest.example.json`，改成本机图片路径后在本机输出目录渲染。

## 6. 常见问题

如果提示 `Pillow is not installed`：

```bash
python3 -m pip install -r requirements.txt
```

如果提示找不到 `face-report-v2`：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

如果 PNG 导出失败，但 HTML 已生成，先打开 HTML 验证安装；PNG 依赖 Playwright 和浏览器环境。

如果是用安装后的 `face-report-v2` 命令导出 PNG，Playwright 要装在该技能自己的虚拟环境中：

```bash
~/.codex/skills/face-consultation-report/.venv/bin/python -m pip install playwright
~/.codex/skills/face-consultation-report/.venv/bin/python -m playwright install chromium
```
