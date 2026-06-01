# AI 美学升级报告技能｜完整迁移安装说明

生成时间：2026-05-26 05:50:13

## 一、迁移目标
- 把本机已经调好的“AI 美学升级报告 / 面部美学升级报告”技能迁移到另一台 Mac，安装后可以继续生成：原图、客户 AI 效果图、效果标记图、报告图、网资沟通细节表。
- 迁移重点不是只复制一个脚本，而是复制技能规则、智能体分工、报告渲染脚本、模板、知识库依赖和验收流程。
- 本说明只做安装与使用迁移，不默认生成迁移包；如果后续要打包 ZIP，再单独执行。

## 二、迁移后最终能力
- 1. 输入一张成年人正脸或接近正脸照片。
- 2. 生成客户 AI 效果图：必须与原图区分明显，但保留本人身份，不换脸、不网红脸。
- 3. 生成优化升级标记图：标出眼周、泪沟、面中、法令纹、下颌缘、肤质、唇部气色等调整点。
- 4. 生成成交型报告图：包含 Before/After、项目映射、视觉年龄、美学设计思路、三条优先级建议。
- 5. 生成网资沟通细节总表：顶部四张图，下面按“网资视角 + 客户视角”拆出话术、接话、项目承接和下一步动作。
- 6. 每次优化完成后自动封档：记录优化时间、改动内容、涉及文件、质检结果和最终版路径。

## 三、源电脑当前关键路径
- 技能目录：/Users/apple/.codex/skills/face-consultation-report
- 样例交付目录：/Users/apple/Desktop/AI美学升级报告_本机完整样例_20260525
- 业务知识库：/Users/apple/.openclaw/workspace/knowledge-base
- 本机生成图片目录：/Users/apple/.codex/generated_images
- 封档记录：/Users/apple/Desktop/AI美学升级报告_本机完整样例_20260525/07_封档记录/封档记录.md
- 迁移说明输出目录：/Users/apple/Desktop/AI美学升级报告_本机完整样例_20260525/08_迁移说明文档

## 四、迁移文件清单
| 级别 | 源路径 | 用途 |
| --- | --- | --- |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/SKILL.md | 技能入口说明，包含执行边界、流程、封档规则。 |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/agents/AGENTS.md | 10 个智能体分工说明。 |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/agents/face-report-agents.yaml | 智能体机器可读配置。 |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/references/report-spec.md | 报告结构、文案和设计规范。 |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/scripts/render_sales_v2.py | 成交型 V2 报告渲染脚本。 |
| 建议复制 | /Users/apple/.codex/skills/face-consultation-report/scripts/render_report.py | 旧版报告渲染脚本，备用。 |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/templates/网资沟通文案_复制即用版.docx | 网资话术模板。 |
| 必须复制 | /Users/apple/.codex/skills/face-consultation-report/templates/网资咨询师承接跟进表_详细版.xlsx | 网资跟进表模板。 |
| 强烈建议 | /Users/apple/.openclaw/workspace/knowledge-base/02-产品体系/后端高客单/AI面诊调整点收费项目映射库.md | 项目映射知识库。 |
| 强烈建议 | /Users/apple/.openclaw/workspace/knowledge-base/03-成交体系/门店成交/AI面诊报告沟通成交SOP.md | 沟通成交 SOP。 |
| 强烈建议 | /Users/apple/.openclaw/workspace/knowledge-base/06-运营工具/文档排版风格/AI面诊报告设计升级规范.md | 报告设计规范。 |
| 建议复制 | /Users/apple/Desktop/AI美学升级报告_本机完整样例_20260525 | 完整样例包，用于迁移后对照验收。 |

## 五、目标电脑安装步骤
| 步骤 | 操作 | 具体说明/命令 |
| --- | --- | --- |
| 1 | 确认目标电脑是 Mac，并安装 Codex 桌面版或可读取 ~/.codex/skills 的 Codex 环境。 | 打开终端，执行：ls ~/.codex // mkdir -p ~/.codex/skills |
| 2 | 创建技能目录。 | mkdir -p /Users/目标用户名/.codex/skills/face-consultation-report |
| 3 | 把源电脑技能目录复制到目标电脑同路径。 | 推荐用 AirDrop/移动硬盘/rsync。目标路径：/Users/目标用户名/.codex/skills/face-consultation-report |
| 4 | 复制业务知识库文件。 | 在目标电脑创建：/Users/目标用户名/.openclaw/workspace/knowledge-base/，然后按原目录结构放入 3 个 md 文件。 |
| 5 | 安装 Python 依赖。 | python3 -m pip install pillow playwright python-docx openpyxl pyyaml && python3 -m playwright install chromium |
| 6 | 确认 Google Chrome 或 Playwright Chromium 可用。 | 报告截图依赖浏览器；Chrome 路径通常是 /Applications/Google Chrome.app。没有 Chrome 时 Playwright Chromium 也可用。 |
| 7 | 确认图片生成能力。 | 优先使用 Codex 内置 image_gen/GPT 作图；如果目标电脑没有图像生成能力，需要手动用 GPT 生成客户 AI 效果图后放入 manifest。 |
| 8 | 运行脚本语法检查。 | python3 /Users/目标用户名/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/目标用户名/.codex/skills/face-consultation-report |
| 9 | 用样例 manifest 跑一次渲染。 | python3 /Users/目标用户名/.codex/skills/face-consultation-report/scripts/render_sales_v2.py --manifest /path/to/manifest-v2.json --out /Users/目标用户名/Desktop/面诊报告_测试 |
| 10 | 打开 00_交付入口.html 和 report-v2.png 检查。 | 确认四件视觉交付物顺序正确：原图 -> 客户 AI 效果图 -> 效果标记图 -> 报告图。 |

## 六、10 个智能体分工
| 智能体 | 职责 |
| --- | --- |
| 01_照片与需求质检智能体 | 判断照片是否可用，是否成年人、是否看清五官。 |
| 02_原图美学诊断智能体 | 只基于原图观察眼周、面中、法令纹、轮廓、肤质、唇部。 |
| 03_AI效果设计智能体 | 生成客户 AI 效果图和效果标记图，要求变化明显但保留本人。 |
| 04_效果标记校对智能体 | 检查标注清楚、不遮挡五官、无乱码水印。 |
| 05_项目映射与升单智能体 | 把每个变美点映射到收费项目方向。 |
| 06_客户报告文案智能体 | 写客户看得懂的标题、设计思路、三条建议。 |
| 07_报告排版渲染智能体 | 生成 HTML、PNG、入口页，确保 Before/After 铺满。 |
| 08_网资沟通承接智能体 | 站网资角度生成可复制话术和跟进表。 |
| 09_客户视角体验校对智能体 | 站客户角度检查客户心理、可能回复、接话方式。 |
| 10_终检交付智能体 | 检查文件完整、合规边界、封档记录。 |

## 七、manifest-v2.json 示例
```json
{
  "client_label": "03/30",
  "label": "AI 美学升级报告｜仅做参考",
  "title": "疲态下去，精致感上来",
  "subtitle": "保留本人五官，提升眼周、轮廓与气色",
  "visual_age": "-5~7 岁",
  "before_image": "/abs/path/original.jpg",
  "effect_image": "/abs/path/ai-effect-clean.png",
  "after_image": "/abs/path/upgraded-ai-medical-annotated.png",
  "diagnosis": [
    {"title": "眼周疲态", "body": "眼下暗沉与泪沟感明显，精神度被削弱。"},
    {"title": "面中支撑不足", "body": "苹果肌饱满度不够，面中立体感偏弱。"},
    {"title": "法令纹阴影", "body": "鼻翼至嘴角阴影明显，中下面部显疲态。"},
    {"title": "轮廓不清晰", "body": "下颌缘不够干净，精致感被拉低。"}
  ],
  "project_mappings": [
    {"label": "眼周提亮", "project": "眼周管理 / 熊猫针 / 胶原眼周", "solves": "疲态、泪沟、黑眼圈", "details": ["眼周明亮有神", "告别暗沉"], "crop_box": [0.18, 0.36, 0.83, 0.55]},
    {"label": "面中支撑", "project": "中大分子玻尿酸 / 再生材料 / 胶原支撑", "solves": "苹果肌、法令纹支撑", "details": ["填补流失容积", "苹果肌饱满上提"], "crop_box": [0.25, 0.46, 0.78, 0.69]}
  ],
  "design_thinking": {
    "goal": "不换脸，保留本人五官和亲和感，只做状态型精调。",
    "path": "先把眼周疲态降下来，再补面中支撑，让脸从累变成柔和、有精神。",
    "result": "轮廓更干净、肤质更通透、唇部气色更好，整体呈现更精致的自然感。"
  },
  "advice": [
    {"title": "建议一：眼周精调", "why": "眼周是第一眼最容易显疲惫的位置。", "direction": "先做眼周管理、熊猫针/胶原眼周方向，必要时做眼袋评估。"},
    {"title": "建议二：面中支撑", "why": "法令纹和疲态很多时候不是单独一条纹的问题，而是面中支撑不足。", "direction": "围绕苹果肌、鼻基底、法令纹做联合设计。"},
    {"title": "建议三：肤质轮廓维护", "why": "肤质和轮廓决定精致度，适合作为加分项。", "direction": "用水光/光子改善通透度，再配合下颌缘收紧和唇部气色管理。"}
  ]
}
```

## 八、日常使用流程
| 阶段 | 操作说明 |
| --- | --- |
| 输入照片 | 把客户正脸或近正脸照片放到任务目录，例如 original.jpg。 |
| 生成客户 AI 效果图 | 用 Codex 的 imagegen/GPT 作图，要求保留本人身份，明显改善眼周、面中、肤质、唇色、轮廓。保存为 ai-effect-clean.png。 |
| 生成效果标记图 | 在 AI 效果图上加编号、蓝色细线和中文短标签，保存为 upgraded-ai-medical-annotated.png。 |
| 编辑 manifest-v2.json | 填入 before_image、effect_image、after_image、diagnosis、project_mappings、design_thinking、advice。 |
| 运行渲染脚本 | python3 ~/.codex/skills/face-consultation-report/scripts/render_sales_v2.py --manifest /path/manifest-v2.json --out /path/output-folder |
| 生成沟通表 | 复制模板或按当前样例的双智能体表格结构生成 Word/Excel。 |
| 终检 | 检查四张图、报告图、沟通表、入口页、封档记录。 |

## 九、验收清单
| 验收项 | 标准 |
| --- | --- |
| 图片质量 | 客户 AI 效果图与原图区分明显；不是普通磨皮；不换脸；无文字水印。 |
| 标记图 | 中文正常，无方块乱码；标注不遮挡眼睛、鼻子、嘴巴；编号与项目方向对应。 |
| 报告图 | Before/After 铺满框，不出现大面积留白；标题客户可见，不暴露内部成交逻辑。 |
| 沟通表 | 顶部有四张图；表格包含网资视角和客户视角；有客户可能回复和网资接话。 |
| 合规 | 不出现保证效果、永久、无风险、一次解决、做到一模一样等表达。 |
| 封档 | 每次优化完成后更新封档记录。 |

## 十、常见问题处理
| 问题 | 处理方法 |
| --- | --- |
| Skill is invalid | 检查 SKILL.md 的 YAML 头部、缩进、文件是否缺失。运行 quick_validate.py 看具体错误。 |
| report-v2.png 没生成 | 通常是 Playwright/Chrome 问题。执行 python3 -m playwright install chromium，或安装 Google Chrome。 |
| 图片找不到 | manifest-v2.json 里的路径必须是目标电脑真实绝对路径。 |
| 中文乱码/方块 | 标注图生成时要使用目标电脑可用中文字体，如 STHeiti Medium.ttc、PingFang。 |
| 客户 AI 效果图变化不明显 | 03_AI效果设计智能体判定不合格，必须重新生成，不能用原图简单提亮替代。 |
| 效果图像换脸 | 提示词降低夸张程度，强调保留身份、五官比例、额头痣、发型、拍摄角度。 |
| 目标电脑没有 GPT 作图 | 先手动在 ChatGPT/GPT 作图里生成 ai-effect-clean.png，再放入 manifest，渲染脚本仍可用。 |

## 十一、项目介绍与功能功效填写入口
已单独生成填写入口文件：`/Users/apple/Desktop/AI美学升级报告_本机完整样例_20260525/08_迁移说明文档/项目介绍与功能功效填写入口.md`
文档内需要补充的项目内容包括：项目基础介绍、功能功效说明、项目承接话术、价格套餐、风险边界与禁忌。

## 十二、封档要求
- 每次优化完成后，必须在项目目录下创建或更新 `07_封档记录/封档记录.md`。
- 封档内容必须包含：优化时间、优化内容、涉及文件、质检结果、最终版路径。
- 封档不是迁移包；迁移包只有用户明确要求才做。