# 仓库管理规则（Claude Code 与 Codex 共管）

这个仓库由 **Claude Code** 和 **Codex** 两个 AI 工具共同管理。任何一方进入仓库后，先读本文件，再开始工作。

## 通用规则

- 默认用中文沟通和说明。
- 修改前先读 `README.md`、本文件和项目结构。
- 一切改动都通过 Git 记录，保持可回滚，不绕过 Git 直接乱改、乱删、乱传。
- 不删除用户未确认的文件；不确定能否删除时，先问用户。
- 不把内部工作过程（报价、分润、客户名单等）写进公开内容。

## 分工

- **Claude Code**：主要修改、重构、整理结构、补文档、连续改多个文件，并负责 commit 和 push。
- **Codex**：检查仓库状态、补充文档/脚本/测试、安全扫描、发布、清理、整理交付说明。

两个工具不要同时改同一个文件。推荐顺序：Claude Code 先做主要修改并提交 → Codex 再检查、补充、发布。

## 每次动手前

```bash
git status
git remote -v
git branch
```

如果发现有未提交改动，先确认是谁做的，不要直接覆盖；发现别的工具留下的未提交改动时，先汇报再处理。

## 提交与推送

```bash
git status
git add .
git commit -m "说清这次改了什么"
git push
```

提交信息要具体，不要用 `fix`、`update` 这种含糊词。重要修改后先跑基本检查（见下）。

## 隐私红线（本仓库特别重要）

这是医美美学报告工作流，**绝对不能提交**以下内容到 GitHub：

- 客户原图、AI 效果图、效果标记图、报告截图。
- 含客户姓名、电话、微信、门店信息的 Word/Excel/文档。
- 真实案例原图、未授权客户照片。
- 内部报价、合同、分润规则。
- `.env`、`.pem`、`.key`、`cookies.json`、`storage_state.json`、GitHub token、API key、私钥、cookie、浏览器登录态。

`.gitignore` 默认已忽略常见图片格式和 `outputs/`、`客户资料/`、`客户照片/`。真实客户项目请复制 `sample/manifest.example.json`，改成本机路径后在本机输出目录渲染，不要进仓库。

推送前可以扫一遍：

```bash
git status
find . -name ".env" -o -name "*.pem" -o -name "*.key" -o -name "cookies.json" -o -name "storage_state.json"
```

## 改动后的基本检查

```bash
python3 -m pip install -r requirements.txt
python3 scripts/self_check.py
open outputs/self-check-demo/report-v2.html
```

能看到 `report-v2.html`，说明仓库文件、脚本、依赖和 demo 渲染链路仍然正常。

## 内容免责

报告内容仅做美学沟通参考，不构成医学诊断、治疗建议或效果承诺；不写保证效果、不伪造真实案例，AI 效果图标注为示意，强调个体差异。
