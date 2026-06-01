#!/usr/bin/env python3
"""Render a Chinese facial consultation report from a JSON manifest.

The script creates a deterministic HTML report and copies referenced images
into the output folder. It intentionally avoids non-stdlib dependencies.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Failed to read manifest: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Manifest must be a JSON object.")
    return data


def copy_asset(src_value: str | None, assets_dir: Path, fallback_name: str) -> str:
    if not src_value:
        return ""
    src = Path(os.path.expanduser(src_value)).resolve()
    if not src.exists():
        raise SystemExit(f"Image not found: {src}")
    suffix = src.suffix.lower() or ".png"
    dest_name = f"{fallback_name}{suffix}"
    dest = assets_dir / dest_name
    counter = 2
    while dest.exists():
        dest_name = f"{fallback_name}-{counter}{suffix}"
        dest = assets_dir / dest_name
        counter += 1
    shutil.copy2(src, dest)
    return f"assets/{dest_name}"


def card(title: str, body: str = "", klass: str = "") -> str:
    return (
        f'<article class="card {klass}">'
        f'<div class="card-icon" aria-hidden="true"></div>'
        f'<div><h3>{esc(title)}</h3><p>{esc(body)}</p></div>'
        "</article>"
    )


def list_items(items: list[Any]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def normalize_list(data: Any, defaults: list[dict[str, Any]], allow_empty: bool = False) -> list[dict[str, Any]]:
    if allow_empty and isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, list) and data:
        return [x for x in data if isinstance(x, dict)]
    return defaults


def render_html(manifest: dict[str, Any], assets_dir: Path) -> str:
    before = copy_asset(manifest.get("before_image"), assets_dir, "before")
    after = copy_asset(manifest.get("after_image"), assets_dir, "after")

    defaults_diagnosis = [
        {"title": "眼神疲惫", "body": "眼神略显无神，面部活力感不足。"},
        {"title": "黑眼圈", "body": "眼周暗沉明显，视觉上容易显疲惫。"},
        {"title": "眼型不够舒展", "body": "眼裂舒展度一般，灵动感可进一步提升。"},
    ]
    defaults_solutions = [
        {"title": "眼周年轻化", "body": "改善眼周状态，淡化细纹与暗沉。"},
        {"title": "眼型优化", "body": "调整眼型比例，眼神更灵动自然。"},
        {"title": "气质提升", "body": "优化整体状态，提升亲和力与精致度。"},
    ]
    defaults_ai = [
        {"title": "眼部分析", "items": ["眼裂长度", "眼距分析", "黑眼圈程度", "卧蚕饱满度"]},
        {"title": "鼻部分析", "items": ["鼻梁高度", "鼻头形态", "鼻翼宽度", "鼻部对称度"]},
        {"title": "唇部分析", "items": ["唇形比例", "唇部饱满度", "唇色状态", "唇周对称度"]},
        {"title": "皮肤分析", "items": ["肤质状态", "毛孔粗细", "肤色均匀度", "皮肤光泽度"]},
    ]
    defaults_bottom = [
        {"title": "个性化分析", "body": "基于AI人脸识别技术，结合个人五官特征，进行多维度美学评估。"},
        {"title": "科学评估", "body": "量化美学标准，提供客观、清晰的分析结果。"},
        {"title": "AI模拟", "body": "预览自然优化效果，辅助制定个性化美学方案。"},
        {"title": "安全建议", "body": "结合医学原则，提供安全、合理的美学沟通建议。"},
    ]

    diagnosis = normalize_list(manifest.get("diagnosis"), defaults_diagnosis)
    solutions = normalize_list(manifest.get("solutions"), defaults_solutions)
    ai_sections = normalize_list(manifest.get("ai_sections"), defaults_ai)
    bottom_items = normalize_list(manifest.get("bottom_items"), defaults_bottom)
    callouts = normalize_list(
        manifest.get("callouts"),
        [
            {"label": "眼裂更舒展", "top": "30%", "left": "77%"},
            {"label": "卧蚕更自然", "top": "48%", "left": "77%"},
            {"label": "亲和力提升", "top": "66%", "left": "77%"},
        ],
        allow_empty=True,
    )

    diagnosis_html = "".join(card(x.get("title", ""), x.get("body", "")) for x in diagnosis[:4])
    solutions_html = "".join(card(x.get("title", ""), x.get("body", ""), "solution-card") for x in solutions[:4])

    ai_html_parts = []
    for idx, section in enumerate(ai_sections[:4], start=1):
        img = copy_asset(section.get("image"), assets_dir, f"analysis-{idx}") if section.get("image") else ""
        img_html = f'<img src="{esc(img)}" alt="{esc(section.get("title", ""))}">' if img else '<div class="mini-placeholder"></div>'
        items = section.get("items") if isinstance(section.get("items"), list) else []
        ai_html_parts.append(
            '<section class="analysis-card">'
            f'<h3>{esc(section.get("title", ""))}</h3>'
            f'<div class="analysis-row">{img_html}<ul>{list_items(items[:5])}</ul></div>'
            '</section>'
        )
    ai_html = "".join(ai_html_parts)

    callout_html = ""
    for callout in callouts[:4]:
        style = f'top:{esc(callout.get("top", "30%"))};left:{esc(callout.get("left", "77%"))};'
        callout_html += f'<div class="callout" style="{style}"><span>{esc(callout.get("label", ""))}</span></div>'

    bottom_html = "".join(card(x.get("title", ""), x.get("body", ""), "bottom-card") for x in bottom_items[:4])

    portrait_fit = esc(manifest.get("portrait_fit", "cover"))
    before_img = f'<img class="portrait-img {portrait_fit}" src="{esc(before)}" alt="Before portrait">' if before else '<div class="portrait-placeholder">Before</div>'
    after_img = f'<img class="portrait-img {portrait_fit}" src="{esc(after)}" alt="After portrait">' if after else '<div class="portrait-placeholder">After</div>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(manifest.get("title", "AI五官美学升级报告"))}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #e9edf3;
      color: #10213d;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
    }}
    .page {{
      width: 1600px;
      min-height: 900px;
      margin: 24px auto;
      padding: 24px 28px 12px;
      border: 1px solid #d5dde9;
      border-radius: 18px;
      background: linear-gradient(180deg, #fbfdff 0%, #f5f8fc 100%);
      box-shadow: 0 22px 70px rgba(22, 39, 64, .18);
      overflow: hidden;
    }}
    .header {{
      display: grid;
      grid-template-columns: 220px 1fr 220px;
      align-items: start;
      gap: 18px;
      height: 130px;
    }}
    .case-badge {{
      height: 88px;
      padding: 16px 24px;
      border-radius: 0 52px 52px 0;
      background: linear-gradient(135deg, #eef3f9, #ffffff);
      box-shadow: inset -1px -1px 0 #dfe7f2;
    }}
    .case-badge strong {{ display: block; font-size: 32px; letter-spacing: 2px; font-weight: 500; color: #63728b; }}
    .case-badge span {{ display: block; margin-top: 6px; font-size: 13px; color: #6c7890; }}
    .title-area {{ text-align: center; padding-top: 4px; }}
    h1 {{ margin: 0; font-size: 55px; line-height: 1.05; letter-spacing: 8px; color: #071936; font-weight: 750; }}
    .subtitle {{ margin-top: 18px; font-size: 20px; letter-spacing: 10px; color: #65748c; }}
    .subtitle:before, .subtitle:after {{ content: ""; display: inline-block; width: 46px; height: 1px; background: #9bacbf; vertical-align: middle; margin: 0 20px; }}
    .main {{
      display: grid;
      grid-template-columns: 220px 1fr 170px 285px;
      gap: 14px;
      height: 575px;
    }}
    .panel {{
      border: 1px solid #dce4ee;
      border-radius: 12px;
      background: rgba(255,255,255,.72);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.78);
      overflow: hidden;
    }}
    .panel-title {{
      display: flex;
      align-items: baseline;
      gap: 9px;
      padding: 16px 18px 10px;
    }}
    .panel-title h2 {{ margin: 0; font-size: 23px; font-weight: 650; color: #12213b; }}
    .panel-title span {{ font-size: 10px; color: #8090a7; letter-spacing: .5px; text-transform: uppercase; }}
    .stack {{ display: grid; gap: 12px; padding: 0 10px 14px; }}
    .card {{
      min-height: 125px;
      display: grid;
      grid-template-columns: 72px 1fr;
      align-items: center;
      gap: 10px;
      padding: 14px 14px;
      border: 1px solid #e3e9f2;
      border-radius: 8px;
      background: linear-gradient(180deg, #fbfdff, #f7fafd);
    }}
    .card h3 {{ margin: 0 0 8px; font-size: 18px; color: #152540; font-weight: 650; }}
    .card p {{ margin: 0; font-size: 13px; line-height: 1.65; color: #65738a; }}
    .card-icon {{
      width: 60px;
      height: 60px;
      border-radius: 50%;
      border: 2px solid #8291a7;
      background:
        radial-gradient(circle at 50% 48%, #1d2c45 0 17%, transparent 18%),
        radial-gradient(circle at 50% 50%, transparent 0 40%, #8998ac 41% 44%, transparent 45%),
        linear-gradient(135deg, #f7faff, #dbe4ef);
    }}
    .compare {{
      position: relative;
      display: grid;
      grid-template-columns: 1fr 1fr;
      border: 1px solid #dce4ee;
      border-radius: 12px;
      background: #fff;
      overflow: hidden;
    }}
    .portrait {{
      position: relative;
      min-height: 575px;
      overflow: hidden;
      background: #f1f4f8;
    }}
    .portrait + .portrait {{ border-left: 3px solid #fff; }}
    .portrait-img {{ width: 100%; height: 100%; object-position: center top; display: block; }}
    .portrait-img.cover {{ object-fit: cover; }}
    .portrait-img.contain {{ object-fit: contain; background: #f5f7fa; }}
    .label {{
      position: absolute;
      z-index: 3;
      top: 16px;
      left: 18px;
      padding: 5px 15px;
      border-radius: 16px;
      color: #fff;
      font-size: 17px;
      font-weight: 650;
      letter-spacing: 1px;
      background: rgba(65, 70, 78, .72);
    }}
    .label.after {{ left: auto; right: 72px; background: #1266bf; }}
    .arrow {{
      position: absolute;
      z-index: 4;
      left: 50%;
      top: 50%;
      width: 46px;
      height: 46px;
      transform: translate(-50%, -50%);
      border-radius: 50%;
      background: rgba(255,255,255,.9);
      color: #8392a7;
      display: grid;
      place-items: center;
      font-size: 44px;
      font-weight: 700;
      line-height: 1;
    }}
    .callout {{
      position: absolute;
      z-index: 5;
      width: 160px;
      height: 32px;
      border: 1px solid #3b82d5;
      border-radius: 18px;
      background: rgba(255,255,255,.9);
      color: #235fa8;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 20px rgba(30, 96, 170, .10);
    }}
    .callout:before {{ content: "✓"; margin-right: 6px; width: 17px; height: 17px; border-radius: 50%; background: #1d6ec8; color: white; display: inline-grid; place-items: center; font-size: 12px; }}
    .solution-card {{ min-height: 135px; grid-template-columns: 58px 1fr; }}
    .solution-card .card-icon {{ width: 48px; height: 48px; }}
    .analysis-wrap {{ padding: 0 8px 8px; display: grid; gap: 7px; }}
    .analysis-card {{ border: 1px solid #e0e7f1; border-radius: 8px; background: #fbfdff; padding: 6px; }}
    .analysis-card h3 {{ margin: 0 0 4px; font-size: 15px; color: #172741; }}
    .analysis-row {{ display: grid; grid-template-columns: 130px 1fr; gap: 6px; align-items: center; }}
    .analysis-row img, .mini-placeholder {{ width: 130px; height: 64px; object-fit: cover; border-radius: 7px; background: linear-gradient(135deg, #f2d7c9, #fff3ec); }}
    .analysis-row ul {{ margin: 0; padding-left: 15px; color: #5f718c; font-size: 11px; line-height: 1.55; }}
    .bottom {{
      height: 120px;
      margin-top: 14px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0;
      border: 1px solid #dce4ee;
      border-radius: 12px;
      background: rgba(255,255,255,.72);
      overflow: hidden;
    }}
    .bottom-card {{
      min-height: 118px;
      border: 0;
      border-radius: 0;
      border-right: 1px solid #d1dae7;
      background: transparent;
      grid-template-columns: 82px 1fr;
      padding: 18px 24px;
    }}
    .bottom-card:last-child {{ border-right: 0; }}
    .bottom-card .card-icon {{ width: 68px; height: 68px; background: linear-gradient(135deg, #26364d, #53657f); }}
    .bottom-card h3 {{ font-size: 20px; margin-bottom: 8px; }}
    .bottom-card p {{ font-size: 13px; }}
    .footer {{ margin-top: 8px; text-align: center; color: #708098; font-size: 14px; letter-spacing: 2px; }}
    .portrait-placeholder {{ height: 100%; display: grid; place-items: center; color: #8291a7; font-size: 28px; }}
  </style>
</head>
<body>
  <main class="page">
    <header class="header">
      <div class="case-badge"><strong>{esc(manifest.get("client_label", "03/30"))}</strong><span>{esc(manifest.get("small_label", "AI五官美学升级报告"))}</span></div>
      <div class="title-area">
        <h1>{esc(manifest.get("title", "眼神提亮，亲和力更强"))}</h1>
        <div class="subtitle">{esc(manifest.get("subtitle", "让眼神更有光彩，气质更温柔自然"))}</div>
      </div>
      <div></div>
    </header>
    <section class="main">
      <aside class="panel">
        <div class="panel-title"><h2>问题诊断</h2><span>DIAGNOSIS</span></div>
        <div class="stack">{diagnosis_html}</div>
      </aside>
      <section class="compare">
        <div class="portrait">{before_img}<div class="label">Before</div></div>
        <div class="portrait">{after_img}<div class="label after">After</div></div>
        <div class="arrow">›</div>
        {callout_html}
      </section>
      <aside class="panel">
        <div class="panel-title"><h2>美学解决方案</h2><span>SOLUTION</span></div>
        <div class="stack">{solutions_html}</div>
      </aside>
      <aside class="panel">
        <div class="panel-title"><h2>AI分析报告</h2><span>AI ANALYSIS</span></div>
        <div class="analysis-wrap">{ai_html}</div>
      </aside>
    </section>
    <section class="bottom">{bottom_html}</section>
    <div class="footer">{esc(manifest.get("footer_note", "本报告由AI智能分析生成，仅供美学沟通参考，具体方案请咨询专业医美顾问。"))}</div>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render facial consultation report HTML.")
    parser.add_argument("--manifest", required=True, help="Path to report manifest JSON.")
    parser.add_argument("--out", required=True, help="Output directory.")
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest).expanduser().resolve())
    out_dir = Path(args.out).expanduser().resolve()
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    html_text = render_html(manifest, assets_dir)
    (out_dir / "index.html").write_text(html_text, encoding="utf-8")
    print(out_dir / "index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
