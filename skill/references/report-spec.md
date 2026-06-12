# Face Consultation Report Spec

Use this reference when preparing a Chinese AI facial consultation report.

## Output Shape

Default deliverable:

- 16:9 premium white-blue report page.
- Center before/after portrait comparison.
- Left column: "问题诊断 DIAGNOSIS".
- Right-middle column: "美学解决方案 SOLUTION".
- Far-right column: "AI分析报告 AI ANALYSIS".
- Bottom strip: capability/trust notes.
- Footer disclaimer.

For sales-oriented medical-aesthetic reports, the core deliverable is a folder containing:

- `original.jpg` or `assets/before.*`: original customer photo.
- `ai-effect-clean.*` or `assets/effect.*`: clean customer-facing AI effect image without dense explanation, when available.
- `upgraded-ai-medical-annotated.png` or `assets/after.*`: AI effect image with numbered adjustment labels.
- `report-v2.png`: customer-facing V2 report image.
- `report-v2.html`: editable HTML source.
- `AI美学升级报告_顾问沟通SOP.docx`: consultant talk tracks, recommended project directions, and process.
- `网资咨询师承接跟进表_详细版.xlsx`: online consultant/customer-service follow-up table.
- `00_交付入口.html`: entry page linking all deliverables.

Do not create PDF by default. Only create PDF if the user explicitly asks.

Required delivery order:

1. 原图
2. 客户 AI 效果图
3. 效果标记图
4. 报告图
5. 沟通细节 / 网资咨询师承接表 / SOP

## Required Report Sections

### Header

- Client label: `03/30`, `01/20`, or a generated case number.
- Small label: `AI五官美学升级报告`.
  - For sales-facing versions, prefer: `AI 美学升级报告｜仅做参考`.
- Main title: one benefit-led sentence, for example:
  - `眼神提亮，亲和力更强`
  - `轮廓更清爽，气质更轻盈`
  - `面部更舒展，状态更自然`
- Subtitle: soft aesthetic value, for example:
  - `让眼神更有光彩，气质更温柔自然`
  - `保留真实五官，优化面部状态呈现`

### Problem Diagnosis

Use three cards. Good default titles:

- `眼神疲惫`
- `黑眼圈`
- `眼型不够舒展`
- `面部轮廓松散`
- `肤色不够均匀`
- `唇部气色不足`

Write one short body line per card. Keep wording neutral:

- `眼神略显无神，面部活力感不足。`
- `眼周暗沉明显，视觉上容易显疲惫。`
- `眼裂舒展度一般，灵动感可进一步提升。`
- `肤色均匀度一般，镜头下通透感不足。`

Avoid:

- `丑`, `老`, `垮`, `失败`, `严重`, `必须`, `病变`
- Guaranteed claims such as `年轻十岁`, `永久改善`, `一次见效`

### Solution Direction

Use two or three cards. For medical-aesthetic business scenarios, prefer project-direction titles rather than generic beauty words. Good default titles:

- `眼周精调`
- `面中支撑`
- `轮廓收紧`
- `肤质焕亮`
- `唇部气色`
- `比例协调`

Write as communication direction, not treatment order:

- `改善眼周状态，淡化细纹与暗沉。`
- `调整眼型视觉比例，让眼神更灵动自然。`
- `提升轮廓清晰度，让面部线条更干净。`
- `优化肤色均匀度，增强镜头下通透感。`

### Project Mapping

Every visible AI After improvement should map to a paid project direction. Use concise labels in the report and expand details in the Word SOP.

| Improvement | Report label | Project direction |
|---|---|---|
| Brighter eyes / less tired eye area | `眼周精调` | eye-area management, collagen/HA eye-area support, tear-trough or eye-bag evaluation |
| Softer tear trough / under-eye hollowness | `泪沟弱化` | tear-trough filler/collagen direction, eye-bag evaluation if structural |
| Fuller midface / softer nasolabial transition | `面中支撑` | midface support, apple cheek/nasolabial transition, regenerative/filler direction |
| Softer nasolabial folds | `法令纹淡化` | midface support plus nasolabial fold plan, not just line filling |
| Cleaner jawline | `轮廓收紧` | contour management, RF/HIFU/thread/tightening evaluation, lightening/fat assessment |
| More translucent skin | `肤质焕亮` | skin booster, repair booster, IPL/laser/light-based evaluation |
| Healthier lips | `唇部气色` | lip-specific filler/hydration and lip texture management |

Main report rule:

- Use short phrases like `眼周精调`, `面中支撑`, `轮廓收紧`.
- Do not crowd the visual report with full item names or prices.
- Put exact item options, sequencing, and objection handling in the paired SOP document.

### AI Analysis

Use four stacked modules:

- `眼部分析`: `眼裂长度`, `眼距分析`, `黑眼圈程度`, `卧蚕饱满度`
- `鼻部分析`: `鼻梁高度`, `鼻头形态`, `鼻翼宽度`, `鼻部对称度`
- `唇部分析`: `唇形比例`, `唇部饱满度`, `唇色状态`, `唇周对称度`
- `皮肤分析`: `肤质状态`, `毛孔粗细`, `肤色均匀度`, `皮肤光泽度`

If close-up crops are available, include them. If not, omit module images or reuse softly cropped regions.

### Before/After Callouts

Use two or three labels. Good defaults:

- `眼裂更舒展`
- `卧蚕更自然`
- `眼周更轻盈`
- `轮廓更清晰`
- `气色更通透`
- `亲和力提升`

Callouts should point to the after image only.

### Bottom Strip

Use four capability cards:

- `个性化分析`: `基于AI人脸识别技术，结合个人五官特征，进行多维度美学评估。`
- `科学评估`: `量化美学标准，提供客观、清晰的分析结果。`
- `AI模拟`: `预览自然优化效果，辅助制定个性化美学方案。`
- `安全建议`: `结合医学原则，提供安全、合理的美学沟通建议。`

### Footer

Default:

`本报告由AI智能分析生成，仅供美学沟通参考，具体方案请咨询专业医美顾问。`

Use a stricter version when needed:

`本报告为AI视觉模拟与美学沟通材料，不构成医学诊断、治疗建议或效果承诺。`

## Image Upgrade Prompt Pattern

Use this as a base and adapt to the specific portrait when the user wants a natural upgrade:

```text
以提供的素人正脸照片为基础，保留同一个人的身份、五官结构、脸型、发型、姿态、服装和真实皮肤质感。做轻度自然美学升级：眼神更明亮有神，眼周暗沉略微减轻，眼型视觉上更舒展，卧蚕自然但不过度，肤色更均匀通透，唇部气色更好，整体亲和力和精致度提升。保持真实商业摄影质感，不要夸张医美感，不要变成另一个人，不要磨皮塑料感，不要大眼怪，不要尖下巴，不要过度瘦脸，不要改变年龄感过多。
```

For a paid consultation / medical-aesthetic sales report, use a stronger After prompt:

```text
基于用户提供的正脸照片进行图像编辑，生成高质量医美面诊“优化后效果示意图”。保留同一个成年人、身份特征、脸型基础、发型、服装、拍摄角度和真实人像质感，但让变美效果明显可见。整体效果高级、干净、仙气、精致、亲和，有真实医美案例对比感。

从医美维度呈现调整逻辑：眼周提亮、泪沟/眼袋弱化、面中支撑提升、法令纹淡化、下颌缘收紧、肤质焕亮、唇部气色提升。请使用干净蓝色细线、编号圆点和中文短标签标注具体调整部位，不遮挡眼睛、鼻子和嘴巴主体。标注风格专业、克制、高端。

不要换人，不要变网红脸，不要大眼怪，不要尖下巴，不要塑料皮肤，不要浓妆，不要夸张整容感，不要错误五官，不要杂乱文字，不要水印。
```

Negative prompt ideas:

```text
different person, changed identity, exaggerated surgery, plastic skin, waxy face, huge eyes, sharp V-shaped chin, over-smoothed skin, uncanny expression, distorted facial symmetry, heavy makeup, text artifacts, watermark
```

## Reference Image Set Learning

When using customer-provided Before/After reference sets, follow these rules for the AI effect image:

- Treat paired, front-facing reference images as guidance for the customer AI effect image, not as a report layout template.
- Keep Before and After composition highly consistent: centered face, similar camera angle, complete face, visible shoulder/upper-body context.
- For sales-facing reports, the AI effect image must create a clear visual gap from the original. Do not accept an After that is only slightly brighter or lightly smoothed.
- Make at least four visible improvements when the source photo supports them: brighter eyes, softer tear trough/eye bag area, stronger midface support, softer nasolabial/口周 shadows, cleaner jawline, more translucent skin, healthier lip color.
- The target result is 状态型精调: cleaner, brighter, more refined, more camera-ready, but still the same person.
- Light natural makeup, cleaner hairline/hair arrangement, and improved lighting are allowed when they support the medical-aesthetic communication effect.
- Avoid over-learning extreme reference traits: huge eyes, sharp V chin, plastic skin, heavy makeup, over-changed hairstyle/clothing, or loss of identity.
- The clean customer AI effect image builds desire first. The marked effect image and report then explain where it changed and which project directions can be discussed in person.

## Layout Rules

- Use clean white background with pale blue-gray panels and navy typography.
- Keep cards at 8px radius or less.
- Avoid cheap gradient blobs, decorative clutter, and unreadable AI-generated Chinese text.
- For reliable Chinese text, compose final report with HTML/CSS or design tools after images are generated.
- Use exact human-written Chinese text in the final layout.
- Prioritize the AI After image. In the main Before/After comparison, images should visually fill their frames. Use a cover-style crop when needed to remove large side gutters, while keeping the full face, key hairline/chin area, and callout labels readable.
- Keep the main report short. Move detailed explanation, recommended items, and step-by-step talk track to the Word SOP.
- Add an entry page when delivering a folder: `00_交付入口.html`.
- Do not export PDF by default. Only create PDF if the user explicitly asks for PDF/printing/archive.

## Sales Report V2 Required Blocks

When the goal is consultation conversion, upsell, project mapping, or “升单赚钱”, use the sales-facing V2 report structure:

- Header: `AI 美学升级报告｜仅做参考`.
- Main title: customer-facing outcome language, not internal project-mapping language. Avoid titles like `每一个变美点，都对应一个项目`. Prefer titles such as `疲态下去，精致感上来`, `不换脸，也能明显变精致`, or `保留本人五官，升级整体状态`.
- Before image: the original portrait.
- Customer AI effect image: a separately generated clean upgraded image for the client to feel the result first, without overwhelming project explanation.
- AI marked effect image: a separately generated or edited upgraded image with numbered medical-aesthetic callouts. Use this image inside the report when explaining adjustment points.
- Project mapping panel: each row uses a small crop, one improvement label, the matching project direction, and the customer problem it solves.
- Each project mapping should also include two concrete visual-detail lines, matching the premium annotated-image style, for example `眼周明亮有神 / 告别暗沉` or `填补流失容积 / 苹果肌饱满上提`.
- Visual age card: use a bounded visual estimate such as `-5~7 岁`, plus a clear non-guarantee note.
- Before and AI After must both show the complete face and enough upper body for comparison, not a cropped forehead or partial face. The image should still fill the comparison frame; avoid obvious empty side gutters. Mild top/bottom crop is acceptable only when it preserves face integrity and readable labels.
- In V2 sales reports, the Before/After comparison is the main selling visual. The two image columns should take more than half of the main content width whenever possible; compress side panels before shrinking the comparison images.
- Use `美学设计思路` for the bottom-left explanation card instead of `成交逻辑` in customer-facing reports. Explain `设计目标`, `视觉路径`, and `审美结果`.
- Bottom explanation and advice cards should follow content height. Do not use tall fixed cards that leave large empty lower areas; tighten padding and line-height first, then expand copy only when it adds real consultation value.
- Bottom advice: exactly three prioritized suggestions:
  1. First fix the most visible tired-state issue.
  2. Then improve structure/support and face balance.
  3. Finally add skin, contour, lip, or maintenance items for refinement and repeat purchase.
- Each advice card must include a concrete reason: why this priority comes first/second/third, how it relates to the original issue, and what project direction it supports.

Default V2 project mapping:

| Visual adjustment | Report label | Project direction | Customer-facing problem |
|---|---|---|---|
| brighter eyes / less tired eye area | `眼周提亮` | 眼周管理 / 熊猫针 / 胶原眼周 | 疲态、泪沟、黑眼圈 |
| softer tear trough / eye bags | `泪沟眼袋弱化` | 泪沟填充 / 眶周年轻化 / 眼袋评估 | 眼下显累、显老 |
| fuller midface | `面中支撑` | 苹果肌 / 鼻基底 / 中大分子玻尿酸 / 再生材料 | 面中扁平、法令纹支撑弱 |
| softer nasolabial folds | `法令纹淡化` | 面中支撑联合 / 法令纹精调 | 中下面部疲态 |
| cleaner jawline | `轮廓收紧` | 轮廓管理 / 紧致提升 / 轻薄针评估 | 下颌缘不清、口周松散 |
| brighter skin | `肤质焕亮` | 水光 / 光子 / 修复屏障 / 泡泡针 | 暗沉、毛孔、肤色不均 |
| healthier lips | `唇部气色` | 唇部玻尿酸 / 唇部水润管理 | 唇色弱、唇纹、气色差 |

## Final Response Pattern

Keep final response concise:

`做好了，产出在 ~/Desktop/面诊报告_YYYYMMDD-HHMM/，包含 00_交付入口.html / report-v2.png / report-v2.html / 原图与AI升级图。本报告是AI美学沟通参考，不是医学诊断。`
