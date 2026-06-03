# GitHub 发布记录

发布时间：2026-06-01

仓库地址：https://github.com/tandaikun311-lang/ai-aesthetic-report

仓库属性：Private

默认分支：`main`

本地工作副本：

`/Users/apple/Downloads/codex/交付物/AI美学升级报告_GitHub仓库`

## 本次上传内容

- `skill/`：面部美学升级报告 Codex 技能、智能体分工、报告规范。
- `scripts/`：报告渲染脚本。
- `templates/`：网资沟通文案和咨询师跟进表模板。
- `docs/`：迁移安装说明、项目功能填写入口、参考图学习记录。
- `sample/manifest.example.json`：不含客户图片的示例配置。
- `README.md`、`PRIVACY.md`、`.gitignore`：使用说明、隐私边界和忽略规则。

## 未上传内容

- 客户原图。
- 客户 AI 效果图。
- 效果标记图。
- 报告截图。
- 含客户人脸的 Word / Excel / PDF 成品。
- 任何客户姓名、电话、微信或门店隐私数据。

## 验证结果

- GitHub CLI 已登录账号：`tandaikun311-lang`。
- 仓库创建成功，远端为私有仓库。
- Python 脚本已通过 `py_compile`。
- 本地仓库已推送到 `origin/main`。

## 2026-06-03 演示自检补充

改动摘要：

- 新增 `sample/demo-inputs/` 合成 SVG demo 输入，不含真实人脸和客户隐私。
- 新增 `sample/manifest.demo.json`，collaborator 不准备客户素材也能验证渲染链路。
- 新增 `scripts/self_check.py`，一次性检查仓库结构并渲染脱敏 demo。
- 更新 `scripts/render_sales_v2.py`，manifest 内图片路径支持相对 manifest 文件解析。
- 更新 `README.md`，补充 3 分钟安装验证流程。

质检口径：

- demo 只用于安装和渲染自检，不作为真实客户效果样张。
- 正式客户原图、AI 效果图、报告截图仍不提交 GitHub。
- 最终交付路径：`/Users/apple/Downloads/codex/交付物/AI美学升级报告_GitHub仓库`。
