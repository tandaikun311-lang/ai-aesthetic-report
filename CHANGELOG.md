# 更新日志 / Changelog

本项目的所有重要变更都记录在此文件。
版本遵循语义化版本（主版本.次版本.修订号）。

## [1.1.0] - 2026-06-12

### 新增
- `scripts/build_handoff_sheet.py`：自动生成「含四图的网资沟通总表」（补齐第 08 号智能体缺失的交付物）。
  - 默认输出可打印的 HTML 总表（原图 / 客户 AI 效果图 / 效果标记图 / 报告图 + 话术）。
  - `--docx` / `--xlsx` 可选导出可编辑的 Word / Excel（需 python-docx / openpyxl）。
  - `--screenshot` 可选导出 PNG。
  - 话术支持通过 manifest 的 `handoff` 字段自定义，否则按项目映射自动生成默认话术。
- `pyproject.toml`：项目元数据、锁定依赖、可选依赖分组（screenshot / handoff / dev）。
- `tests/`：pytest 单元测试（18 项），覆盖 manifest 解析、默认值合并、裁剪坐标、浏览器探测、话术生成。
- `LICENSE`：私有商业「保留所有权利」声明。
- `.github/workflows/ci.yml`：GitHub Actions CI（依赖安装、单元测试、自检渲染、隐私扫描）。

### 改进
- `render_sales_v2.py`：
  - 浏览器路径跨平台探测（`BROWSER_PATH` 环境变量 → PATH → 常见安装位置 → Playwright 内置），不再写死 macOS Chrome 路径。
  - 收紧异常处理：区分文件缺失、读取失败、JSON 解析错误。
  - 新增 `logging` 与 `--verbose` 进度日志。
- `requirements.txt`：锁定 `Pillow>=10.0,<12` 主版本上界，避免依赖漂移；补充可选依赖安装说明。
- `self_check.py`：自检流程新增 handoff 总表渲染校验。
- `validate_install.py`：把 `build_handoff_sheet.py` 纳入必检与编译检查。

## [1.0.0] - 2026-06-03

### 新增
- AI 美学升级报告核心工作流：`render_sales_v2.py`、`render_report.py`。
- 10 智能体分工定义、报告规范、网资沟通文案与跟进表模板。
- 脱敏 demo manifest 与合成 SVG 占位图，`self_check.py` 一键自检。
- 安装 / 卸载脚本、协作者 3 分钟验收说明、隐私规则。
