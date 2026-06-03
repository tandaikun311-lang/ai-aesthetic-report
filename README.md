# AI 美学升级报告

这是一个本机可执行的医美美学升级报告工作流，用于把客户正脸照片整理成：

1. 原图
2. 客户 AI 效果图
3. 效果标记图
4. 报告图
5. 网资沟通文案与承接跟进表

本仓库只保存技能规则、渲染脚本、模板和说明文档。真实客户照片、AI 效果图、报告截图、含客户人脸的 Word/Excel 成品不要提交到 GitHub。

## 目录

| 路径 | 用途 |
|---|---|
| `skill/` | Codex 技能说明、智能体分工、报告规范 |
| `scripts/` | HTML/PNG 报告渲染脚本 |
| `templates/` | 网资沟通文案和跟进表模板 |
| `docs/` | 迁移说明、项目填写入口、参考图学习记录 |
| `sample/manifest.example.json` | 示例 manifest，不包含真实图片 |
| `sample/manifest.demo.json` | 可直接跑通的脱敏 demo manifest |
| `sample/demo-inputs/` | 合成占位图，不含真实人脸或客户隐私 |

## 3 分钟验证流程

collaborator 拿到仓库后，不需要准备客户照片，先跑脱敏 demo 验证安装成功：

```bash
cd ai-aesthetic-report
bash install.sh
~/.local/bin/face-report-v2 \
  --manifest sample/manifest.demo.json \
  --out outputs/demo-install-check \
  --no-screenshot
open outputs/demo-install-check/report-v2.html
```

看到报告 HTML 后，说明安装目录、命令行入口、manifest 读取、素材复制和 HTML 渲染已跑通。

也可以先不安装，只验证当前仓库：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/self_check.py
open outputs/self-check-demo/report-v2.html
```

如果要同时导出 `report-v2.png`，先安装 Playwright 和浏览器，再运行：

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/self_check.py --with-screenshot
```

## 下载安装到直接使用

下载安装到目标电脑：

```bash
cd ~/Downloads
git clone https://github.com/tandaikun311-lang/ai-aesthetic-report.git
cd ai-aesthetic-report
bash install.sh
```

安装后会得到：

- Codex 技能：`~/.codex/skills/face-consultation-report`
- V2 报告渲染命令：`~/.local/bin/face-report-v2`
- 基础报告渲染命令：`~/.local/bin/face-report-basic`

当前仓库是私有仓库。别人要下载，需要你先在 GitHub 里添加 collaborator，或者把仓库改成 Public。

详细步骤看：

`docs/下载安装到直接使用说明.md`

## 快速使用渲染脚本

安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

复制真实项目示例 manifest：

```bash
cp sample/manifest.example.json /tmp/manifest.json
```

把 `/tmp/manifest.json` 里的图片路径改成你本机客户图片路径后运行：

```bash
python3 scripts/render_sales_v2.py \
  --manifest /tmp/manifest.json \
  --out /Users/apple/Downloads/codex/任务输出/面诊报告_测试
```

输出目录会生成 `report-v2.html`、`report-v2.png` 和 `assets/`。PDF 不作为默认交付。

如果只是验证脚本，不想安装 Playwright 或导出 PNG，可以加 `--no-screenshot`，先检查 `report-v2.html`。

## 默认执行标准

- 必须先生成客户 AI 效果图，不能用原图充当 After。
- 客户 AI 效果图要有明显变化，但保留本人身份。
- 效果标记图要说明哪里变了，标注点能回到项目方向。
- 报告图主图要铺满，不留明显灰白边。
- 沟通文档要包含四张图、话术表、异议处理、预约面诊和复购维护。
- 所有内容仅做美学沟通参考，不构成医学诊断、治疗建议或效果承诺。

## 隐私规则

本仓库默认 `.gitignore` 会忽略常见图片格式，避免误提交客户人脸。当前 `sample/demo-inputs/` 使用的是 SVG 合成占位图，不对应任何真实人物，只用于安装和渲染自检。
