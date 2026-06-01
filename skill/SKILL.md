---
name: face-consultation-report
description: Create AI facial consultation and aesthetic upgrade reports from a user-provided portrait. Use when the user asks for 面诊分析报告, AI面诊, 五官美学分析, 素人照片升级, before/after facial aesthetics report, 医美咨询报告, 医美升单报告, 美学升级报告, or wants a customer-facing report with AI After, adjustment labels, project mapping, visual age, and prioritized recommendations.
---

# Face Consultation Report

Use this skill to turn one clear portrait into a Chinese aesthetic consultation deliverable: original photo, AI upgraded effect image, face/feature observations, project mapping, customer-facing design thinking, and a premium report image.

## Required Business Knowledge

Before generating a report for a medical-aesthetic business scenario, read these local knowledge-base files when available:

- `/Users/apple/.openclaw/workspace/knowledge-base/02-产品体系/后端高客单/AI面诊调整点收费项目映射库.md`
- `/Users/apple/.openclaw/workspace/knowledge-base/03-成交体系/门店成交/AI面诊报告沟通成交SOP.md`
- `/Users/apple/.openclaw/workspace/knowledge-base/06-运营工具/文档排版风格/AI面诊报告设计升级规范.md`

Use them to map every visible improvement in the AI After image to a project direction, a consultant explanation, and a next-step face-to-face consultation prompt.

## Operating Boundaries

- Treat the output as aesthetic communication and consultation support, not medical diagnosis.
- Do not claim disease, pathology, surgical necessity, guaranteed effect, age reversal, permanence, or exact treatment outcomes.
- Prefer wording such as "观察到", "可关注", "可优化方向", "视觉上", "气质呈现" instead of "缺陷", "问题严重", "必须做".
- Keep upgrades natural: preserve identity, face shape, pose, expression, skin texture, and ethnicity. Avoid plastic skin, exaggerated V-face, doll eyes, obvious surgery, or changing the person.
- If the portrait appears to be a minor or the task requests sexualized beauty framing, stop and ask for a suitable adult, non-sexualized portrait.
- Save final task artifacts under a clear descriptive folder on `/Users/apple/Desktop/`; do not prefix new folders with `新建文件夹`.

## Workflow

## Multi-Agent Execution

This skill must be executed as a multi-agent workflow by default. Load `agents/AGENTS.md` and `agents/face-report-agents.yaml` before producing a complete report.

Required agent order:

1. `01_照片与需求质检智能体`
2. `02_原图美学诊断智能体`
3. `03_AI效果设计智能体`
4. `04_效果标记校对智能体`
5. `05_项目映射与升单智能体`
6. `06_客户报告文案智能体`
7. `07_报告排版渲染智能体`
8. `08_网资沟通承接智能体`
9. `09_客户视角体验校对智能体`
10. `10_终检交付智能体`

Default delivery order:

1. 原图
2. 客户 AI 效果图
3. 效果标记图
4. 报告图
5. 沟通细节 / 网资表

Each step must produce handoff material for the next agent. The final answer should come only after `10_终检交付智能体` confirms that all required deliverables exist and the report stays within aesthetic communication boundaries.

Archive rule: after every optimization or revision of this skill's reports, communication documents, tables, prompts, or agent rules, create/update a local archive record before final response. The archive record must include the optimization time, changed files, change summary, QA result, and final deliverable path. This is a local archive/version record only; do not create or update a migration package unless the user explicitly asks for one.

1. **Collect input**
   - If no portrait is provided, ask for a clear front-facing or near-front-facing adult portrait.
   - Prefer one person, neutral expression, visible eyes/nose/lips/skin, no heavy filters, no extreme angle.
   - If a local path is provided, inspect it before editing.

2. **Create visual analysis**
   - Analyze visible aesthetics only: eye vitality, periocular dullness, eye shape openness, nose proportion, lip contour/fullness, face contour, skin texture/evenness, overall temperament.
   - Separate "problem diagnosis" from "solution direction"; keep both concise and non-alarming.
   - Use the section schema in `references/report-spec.md` when drafting report copy.
   - Create an adjustment-to-project list. Each clear improvement must map to at least one project direction, for example: eye brightening -> eye-area management; tear trough softening -> eye-area filler/collagen/eye-bag evaluation; midface support -> midface support/regenerative/filler direction; jawline cleanup -> contour/tightening direction; skin glow -> skin booster/light-based treatment direction.

3. **Generate the upgraded image**
   - Use image editing/generation capability available in the environment. For Chinese portrait/poster work, prefer the local Jimeng path when available; for general faithful photo editing, use imagegen.
   - Prompt for a clearly visible medical-aesthetic upgrade, not a simple beauty filter: brighter eyes, softened tear troughs/eye bags, better midface support, softer nasolabial shadows, cleaner jawline, more luminous skin, healthier lips, and a refined high-end medical-aesthetic temperament.
   - When the user wants sales/consultation material, prefer an AI After image with numbered medical-aesthetic callouts directly on the image.
   - Preserve identity and photo realism. Keep changes plausible and non-invasive.

4. **Compose the report**
   - For customer-facing medical-aesthetic sales work, use `scripts/render_sales_v2.py`.
   - V2 must include and deliver in this order: `原图` -> `客户 AI 效果图` -> `效果标记图` -> `报告图` -> `沟通细节/网资表`.
   - Use `before_image` for the original, optional `effect_image` for the clean customer-facing AI effect image, and `after_image` for the numbered/callout annotated effect image used inside the report.
   - V2 must include: complete Before image, complete AI After image, adjustment labels/project mapping cards, visual age estimate, `美学设计思路`, and three prioritized recommendations with detailed reasons.
   - V2 layout must prioritize the Before/After images as the main selling visual: make the two portraits large and visually filled, compress side panels first, and avoid obvious empty gutters around the portraits.
   - Use customer-facing outcome titles such as `不换脸，也能明显变精致`; do not expose internal wording such as `每一个变美点都对应一个项目`.
   - Keep the main report visually clean. Put short project directions in the report; put detailed recommended projects and talk tracks in the paired `网资沟通文案_复制即用版` and `网资咨询师承接跟进表_详细版`.
   - When delivering a complete sales package, include the consultant materials after the four visual files: `网资沟通文案_复制即用版.docx/.md` and `网资咨询师承接跟进表_详细版.xlsx`.
   - Use `scripts/render_report.py` only for the older general report layout.
   - Render HTML first and screenshot to PNG for sharing. Do not export PDF unless the user explicitly asks for PDF, printing, or archive delivery.

5. **Return**
   - Show or provide the final report path.
   - Mention that it is an AI aesthetic visualization/report for communication reference, not a professional medical diagnosis.
   - Keep the response short unless the user asks for the full analysis text inline.

## Script Quick Start: V2 Sales Report

Create a manifest after producing the AI After image:

```json
{
  "client_label": "03/30",
  "title": "疲态下去，精致感上来",
  "subtitle": "保留本人五官，提升眼周、轮廓与气色",
  "visual_age": "-5~7 岁",
  "before_image": "/abs/path/original.jpg",
  "effect_image": "/abs/path/ai-after-clean.png",
  "after_image": "/abs/path/ai-after-annotated.png",
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

Run:

```bash
python3 /Users/apple/.codex/skills/face-consultation-report/scripts/render_sales_v2.py \
  --manifest /abs/path/manifest.json \
  --out /Users/apple/Desktop/面诊报告_YYYYMMDD-HHMM
```

Open `00_交付入口.html` or `report-v2.png` to review. The script does not create PDF.

## References

- Read `references/report-spec.md` for the exact report schema, wording bank, visual layout, and prompt snippets.
