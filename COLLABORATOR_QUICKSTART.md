# Collaborator Quickstart

目标：不准备任何客户照片，先确认仓库能安装、命令能运行、demo 报告能渲染。

## 1. 克隆仓库

```bash
cd ~/Downloads
git clone https://github.com/tandaikun311-lang/ai-aesthetic-report.git
cd ai-aesthetic-report
```

如果仓库是 Private，需要先确认你已经被加入 collaborator，并且本机 GitHub 登录有权限。

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
