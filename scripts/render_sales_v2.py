#!/usr/bin/env python3
"""Render a sales-facing AI medical-aesthetic report V2 from a JSON manifest."""

from __future__ import annotations

import argparse
import html
import json
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from PIL import Image

logger = logging.getLogger("face_report")


def find_browser() -> str | None:
    """Locate a Chromium/Chrome executable across platforms.

    Resolution order:
    1. BROWSER_PATH environment variable (explicit override).
    2. Common executable names on PATH (chromium, chrome, etc.).
    3. Well-known install locations on macOS / Windows.
    Returns None so Playwright can fall back to its bundled browser.
    """
    override = os.environ.get("BROWSER_PATH")
    if override:
        if Path(override).exists():
            return override
        logger.warning("BROWSER_PATH=%s not found, falling back to auto-detect.", override)

    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome"):
        found = shutil.which(name)
        if found:
            return found

    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return None


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"Manifest not found: {path}") from exc
    except OSError as exc:
        raise SystemExit(f"Failed to read manifest {path}: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Manifest is not valid JSON ({path}): {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Manifest must be a JSON object.")
    return data


def resolve_input_path(src_value: str | None, base_dir: Path) -> Path | None:
    if not src_value:
        return None
    src = Path(os.path.expanduser(src_value))
    if not src.is_absolute():
        src = base_dir / src
    return src.resolve()


def copy_asset(src_value: str | None, assets_dir: Path, fallback_name: str, base_dir: Path) -> str:
    src = resolve_input_path(src_value, base_dir)
    if not src:
        return ""
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


def crop_asset(src_value: str | None, assets_dir: Path, box: list[Any] | None, name: str, base_dir: Path) -> str:
    src = resolve_input_path(src_value, base_dir)
    if not src:
        return ""
    if not src.exists():
        raise SystemExit(f"Image not found for crop: {src}")
    if not box or len(box) != 4:
        return copy_asset(str(src), assets_dir, name, base_dir)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x1, y1, x2, y2 = [float(v) for v in box]
    px = (int(w * x1), int(h * y1), int(w * x2), int(h * y2))
    out = assets_dir / f"{name}.jpg"
    im.crop(px).save(out, quality=94)
    return f"assets/{out.name}"


def defaults() -> dict[str, Any]:
    return {
        "client_label": "03/30",
        "label": "AI 美学升级报告｜仅做参考",
        "title": "疲态下去，精致感上来",
        "subtitle": "保留本人五官，提升眼周、轮廓与气色",
        "visual_age": "-5~7 岁",
        "visual_age_note": "仅代表视觉状态参考，不构成医学效果承诺。",
        "diagnosis": [
            {"title": "眼周疲态", "body": "眼下暗沉与泪沟感明显，精神度被削弱。"},
            {"title": "面中支撑不足", "body": "苹果肌饱满度不够，面中立体感偏弱。"},
            {"title": "法令纹阴影", "body": "鼻翼至嘴角阴影明显，中下面部显疲态。"},
            {"title": "轮廓不清晰", "body": "下颌缘不够干净，精致感被拉低。"},
        ],
        "project_mappings": [
            {
                "label": "眼周提亮",
                "project": "眼周管理 / 熊猫针 / 胶原眼周",
                "solves": "疲态、泪沟、黑眼圈",
                "details": ["眼周明亮有神", "告别暗沉"],
                "crop_box": [0.18, 0.36, 0.83, 0.55],
            },
            {
                "label": "面中支撑",
                "project": "中大分子玻尿酸 / 再生材料 / 胶原支撑",
                "solves": "苹果肌、法令纹支撑",
                "details": ["填补流失容积", "苹果肌饱满上提"],
                "crop_box": [0.25, 0.46, 0.78, 0.69],
            },
            {
                "label": "轮廓收紧",
                "project": "轮廓管理 / 紧致提升 / 轻薄针评估",
                "solves": "下颌缘、口周松散",
                "details": ["紧致下颌线条", "轮廓更清晰"],
                "crop_box": [0.16, 0.58, 0.83, 0.82],
            },
            {
                "label": "肤质焕亮",
                "project": "水光 / 光子 / 修复屏障 / 泡泡针",
                "solves": "暗沉、毛孔、肤色不均",
                "details": ["肤色均匀通透", "细腻有光泽"],
                "crop_box": [0.53, 0.45, 0.89, 0.69],
            },
            {
                "label": "唇部气色",
                "project": "唇部玻尿酸 / 唇部水润管理",
                "solves": "唇色弱、唇纹、气色差",
                "details": ["唇色自然红润", "水润饱满"],
                "crop_box": [0.29, 0.60, 0.70, 0.78],
            },
        ],
        "design_thinking": {
            "goal": "不换脸，保留本人五官和亲和感，只做状态型精调。",
            "path": "先把眼周疲态降下来，再补面中支撑，让脸从“累”变成“柔和、有精神”。",
            "result": "轮廓更干净、肤质更通透、唇部气色更好，整体呈现更精致的自然感。",
        },
        "advice": [
            {
                "title": "建议一：眼周精调",
                "why": "眼周是第一眼最容易显疲惫的位置。原图主要问题不是眼睛小，而是眼下暗沉、泪沟和眼袋阴影让精神感被拉低。",
                "direction": "先做眼周管理、熊猫针/胶原眼周方向，必要时做眼袋评估。这个变化客户最容易看见，也最适合作为第一成交入口。",
            },
            {
                "title": "建议二：面中支撑",
                "why": "法令纹和疲态很多时候不是单独一条纹的问题，而是面中支撑不足导致鼻翼到嘴角过渡不顺。",
                "direction": "围绕苹果肌、鼻基底、法令纹做联合设计。面中撑起来后，年轻感、柔和度和脸部立体度会一起提升。",
            },
            {
                "title": "建议三：肤质轮廓维护",
                "why": "肤质和轮廓决定精致度，但它们更适合在眼周、面中状态改善后做加分项，效果更完整。",
                "direction": "用水光/光子改善通透度，再配合下颌缘收紧和唇部气色管理，做精致感加购和后续复购维护。",
            },
        ],
        "footer": "本报告为 AI 医美效果模拟与方案沟通材料，最终项目以医生面诊评估为准。",
    }


def merged(manifest: dict[str, Any]) -> dict[str, Any]:
    data = defaults()
    data.update({k: v for k, v in manifest.items() if v not in (None, "")})
    for key in ("diagnosis", "project_mappings", "advice"):
        if not isinstance(data.get(key), list) or not data[key]:
            data[key] = defaults()[key]
    if not isinstance(data.get("design_thinking"), dict):
        data["design_thinking"] = defaults()["design_thinking"]
    return data


def render_html(data: dict[str, Any], before: str, after: str, project_images: list[str]) -> str:
    diagnosis_html = ""
    for item in data["diagnosis"][:4]:
        diagnosis_html += (
            '<article class="problem"><div class="dot"></div><div>'
            f'<h3>{esc(item.get("title"))}</h3><p>{esc(item.get("body"))}</p>'
            "</div></article>"
        )

    mappings_html = ""
    for idx, item in enumerate(data["project_mappings"][:5]):
        img = project_images[idx] if idx < len(project_images) else after
        details = item.get("details") if isinstance(item.get("details"), list) else []
        details_html = "".join(f'<span class="detail-line">{esc(x)}</span>' for x in details[:2])
        mappings_html += (
            f'<article class="map-card"><img src="./{esc(img)}" alt="">'
            "<div>"
            f'<h3>{esc(item.get("label"))}</h3>'
            f'<p>{esc(item.get("project"))}</p>'
            f'<div class="detail-lines">{details_html}</div>'
            f'<span class="price-tag">解决：{esc(item.get("solves"))}</span>'
            "</div></article>"
        )

    design = data["design_thinking"]
    advice_html = ""
    for idx, item in enumerate(data["advice"][:3], start=1):
        advice_html += (
            '<article class="advice">'
            f'<span class="pri">{idx}</span>'
            f'<h3>{esc(item.get("title"))}</h3>'
            f'<p><strong>为什么{"先做" if idx == 1 else "第二步" if idx == 2 else "放后面"}：</strong>{esc(item.get("why"))}</p>'
            f'<p><strong>建议方向：</strong>{esc(item.get("direction"))}</p>'
            "</article>"
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(data["title"])}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #e9eef5; color: #0c1c35; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; }}
    .page {{ width: 1600px; margin: 20px auto; padding: 22px 28px 10px; background: linear-gradient(180deg, #fbfdff, #f4f8fc); border: 1px solid #d7e0eb; border-radius: 18px; box-shadow: 0 22px 64px rgba(18,38,70,.16); overflow: hidden; }}
    .top {{ display: grid; grid-template-columns: 245px 1fr 245px; align-items: start; gap: 18px; height: 152px; }}
    .badge {{ padding: 15px 22px; border-radius: 0 50px 50px 0; background: #f1f6fb; border: 1px solid #dce5f0; border-left: 0; }}
    .badge .num {{ font-size: 31px; color: #60718a; letter-spacing: 1px; }}
    .badge .small {{ margin-top: 5px; font-size: 13px; color: #61728b; }}
    h1 {{ margin: 0; text-align: center; font-size: 52px; letter-spacing: 4px; line-height: 1.08; font-weight: 800; color: #071936; }}
    .sub {{ text-align: center; margin-top: 15px; font-size: 19px; letter-spacing: 7px; color: #657891; }}
    .age-box {{ justify-self: end; width: 226px; padding: 15px 16px 14px; border-radius: 10px; background: transparent; color: #0c1c35; border: 1px solid #dce6f1; box-shadow: none; }}
    .age-box span {{ display: block; font-size: 12px; color: #657891; }}
    .age-box strong {{ display: block; margin-top: 4px; font-size: 35px; letter-spacing: 1px; }}
    .age-box p {{ margin: 4px 0 0; font-size: 12px; color: #657891; line-height: 1.4; }}
    .hero {{ display: grid; grid-template-columns: 210px 445px 445px 400px; gap: 14px; height: 630px; }}
    .panel {{ background: rgba(255,255,255,.82); border: 1px solid #dce6f1; border-radius: 10px; overflow: hidden; }}
    .panel-title {{ padding: 13px 14px 8px; display: flex; align-items: baseline; gap: 8px; }}
    .panel-title h2 {{ margin: 0; font-size: 21px; }}
    .panel-title span {{ font-size: 10px; color: #8090a7; letter-spacing: .6px; }}
    .problem-list {{ padding: 0 9px 10px; display: grid; gap: 9px; }}
    .problem {{ min-height: 132px; display: grid; grid-template-columns: 43px 1fr; gap: 9px; align-items: center; padding: 11px; border: 1px solid #e1e9f2; border-radius: 8px; background: #f9fcff; }}
    .dot {{ width: 38px; height: 38px; border-radius: 50%; background: radial-gradient(circle at center, #0e2a4f 0 24%, transparent 25% 45%, #8aa0bd 46% 52%, transparent 53%); border: 1px solid #8aa0bd; }}
    .problem h3 {{ margin: 0 0 6px; font-size: 16px; }}
    .problem p {{ margin: 0; color: #63728a; line-height: 1.5; font-size: 11px; }}
    .photo {{ position: relative; background: #f5f7fa; border: 1px solid #dce6f1; border-radius: 10px; overflow: hidden; }}
    .photo img {{ width: 100%; height: 100%; object-fit: cover; object-position: center center; display: block; }}
    .label {{ position: absolute; top: 16px; left: 16px; z-index: 2; padding: 6px 17px; border-radius: 18px; color: #fff; background: rgba(60,67,78,.78); font-weight: 800; font-size: 18px; }}
    .after .label {{ background: #176bc5; }}
    .map-list {{ padding: 0 10px 10px; display: grid; gap: 6px; }}
    .map-card {{ display: grid; grid-template-columns: 88px 1fr; gap: 9px; padding: 7px; min-height: 102px; border: 1px solid #e0e8f2; border-radius: 8px; background: #fbfdff; }}
    .map-card img {{ width: 88px; height: 78px; object-fit: cover; border-radius: 6px; }}
    .map-card h3 {{ margin: 0 0 3px; font-size: 14px; color: #0d2444; }}
    .map-card p {{ margin: 0; color: #5f718c; line-height: 1.25; font-size: 10px; }}
    .detail-lines {{ display: grid; gap: 0; margin-top: 2px; }}
    .detail-line {{ display: block; color: #41536e; font-size: 9px; line-height: 1.18; }}
    .price-tag {{ margin-top: 3px; display: inline-block; color: #176bc5; font-size: 10px; font-weight: 700; }}
    .bottom {{ margin-top: 12px; display: grid; grid-template-columns: 1.15fr 1fr 1fr 1fr; gap: 12px; align-items: stretch; }}
    .summary {{ padding: 15px 18px 13px; background: transparent; border: 1px solid #dce6f1; border-radius: 10px; color: #0c1c35; }}
    .summary h2 {{ margin: 0 0 9px; font-size: 21px; }}
    .summary p {{ margin: 0 0 8px; color: #5f718c; font-size: 13px; line-height: 1.48; }}
    .summary strong {{ color: #0d2444; }}
    .advice {{ padding: 14px 16px 12px; border: 1px solid #dce6f1; border-radius: 10px; background: #fff; }}
    .advice .pri {{ display: inline-flex; width: 29px; height: 29px; border-radius: 50%; align-items: center; justify-content: center; background: #176bc5; color: #fff; font-weight: 800; margin-bottom: 8px; }}
    .advice h3 {{ margin: 0 0 7px; font-size: 17px; }}
    .advice p {{ margin: 0 0 7px; color: #61718a; font-size: 12px; line-height: 1.5; }}
    .advice strong {{ color: #0d2444; }}
    .footer {{ margin-top: 10px; text-align: center; color: #7888a0; font-size: 13px; letter-spacing: 1px; }}
  </style>
</head>
<body>
  <main class="page">
    <section class="top">
      <div class="badge"><div class="num">{esc(data["client_label"])}</div><div class="small">{esc(data["label"])}</div></div>
      <div><h1>{esc(data["title"])}</h1><div class="sub">{esc(data["subtitle"])}</div></div>
      <div class="age-box"><span>AI 视觉观感评估</span><strong>{esc(data["visual_age"])}</strong><p>{esc(data["visual_age_note"])}</p></div>
    </section>
    <section class="hero">
      <aside class="panel"><div class="panel-title"><h2>原图问题</h2><span>BEFORE</span></div><div class="problem-list">{diagnosis_html}</div></aside>
      <section class="photo before"><img src="./{esc(before)}" alt="Before"><div class="label">Before</div></section>
      <section class="photo after"><img src="./{esc(after)}" alt="After"><div class="label">After</div></section>
      <aside class="panel"><div class="panel-title"><h2>项目映射</h2><span>PROJECT</span></div><div class="map-list">{mappings_html}</div></aside>
    </section>
    <section class="bottom">
      <div class="summary">
        <h2>美学设计思路</h2>
        <p><strong>设计目标：</strong>{esc(design.get("goal"))}</p>
        <p><strong>视觉路径：</strong>{esc(design.get("path"))}</p>
        <p><strong>审美结果：</strong>{esc(design.get("result"))}</p>
      </div>
      {advice_html}
    </section>
    <div class="footer">{esc(data["footer"])}</div>
  </main>
</body>
</html>
"""


def render_entry(before: str, effect: str, after: str) -> str:
    effect_card = (
        f'<a class="card" href="./{esc(effect)}"><div class="tag">02 客户效果</div><h2>客户 AI 效果图</h2><p>不带项目解释的美学升级效果图，适合先给客户建立直观感受。</p></a>'
        if effect
        else f'<a class="card" href="./{esc(after)}"><div class="tag">02 客户效果</div><h2>客户 AI 效果图</h2><p>未单独提供无标注效果图时，可先使用 AI 升级标注图承接。</p></a>'
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 美学升级报告交付入口</title>
  <style>
    body {{ margin: 0; background: #eef3f8; color: #10213d; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; }}
    main {{ max-width: 1040px; margin: 36px auto; padding: 32px; background: #fff; border: 1px solid #dbe4ef; border-radius: 12px; box-shadow: 0 18px 50px rgba(20,40,70,.12); }}
    h1 {{ margin: 0 0 8px; font-size: 34px; }}
    .sub {{ margin: 0 0 28px; color: #667892; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 16px; }}
    a.card {{ display: block; padding: 18px 20px; border: 1px solid #dce6f2; border-radius: 8px; background: #f9fbfe; color: #10213d; text-decoration: none; }}
    a.card:hover {{ border-color: #2c74c9; background: #f3f8ff; }}
    .tag {{ font-size: 12px; color: #2c74c9; font-weight: 700; }}
    h2 {{ margin: 8px 0; font-size: 20px; }}
    p {{ margin: 0; color: #62738d; line-height: 1.55; font-size: 14px; }}
    .preview {{ margin-top: 24px; border-radius: 8px; overflow: hidden; border: 1px solid #dce6f2; }}
    .preview img {{ display: block; width: 100%; height: auto; }}
    .note {{ margin-top: 18px; padding-top: 16px; border-top: 1px solid #e5edf6; color: #708098; font-size: 13px; }}
  </style>
</head>
<body>
  <main>
    <h1>AI 美学升级报告交付入口</h1>
    <p class="sub">固定交付顺序：原图 -> 客户 AI 效果图 -> 效果标记图 -> 报告图 -> 沟通细节。</p>
    <section class="grid">
      <a class="card" href="./{esc(before)}"><div class="tag">01 原图</div><h2>客户原图</h2><p>用于核对原始状态，先让客户看到自己的真实基础。</p></a>
      {effect_card}
      <a class="card" href="./{esc(after)}"><div class="tag">03 标记图</div><h2>效果标记图</h2><p>带编号标注，用于解释哪里变了、为什么变。</p></a>
      <a class="card" href="./report-v2.png"><div class="tag">04 报告图</div><h2>美学升级报告图</h2><p>包含 Before/After、项目映射、视觉年龄和优先级建议。</p></a>
      <a class="card" href="./report-v2.html"><div class="tag">05 可编辑</div><h2>HTML 源文件</h2><p>沟通细节与后续修改使用，可改文案、项目和版式后重新截图。</p></a>
    </section>
    <div class="preview"><img src="./report-v2.png" alt="AI 美学升级报告 V2 预览"></div>
    <p class="note">本报告为 AI 医美效果模拟与方案沟通材料，不构成医学诊断、治疗建议或效果承诺。</p>
  </main>
</body>
</html>
"""


def screenshot_png(html_path: Path, png_path: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "Playwright is required for PNG export. Install it with "
            "`pip install playwright && playwright install chromium`, or use --no-screenshot to skip."
        ) from exc

    browser_path = find_browser()
    launch_kwargs: dict[str, Any] = {"headless": True}
    if browser_path:
        logger.info("Using browser for screenshot: %s", browser_path)
        launch_kwargs["executable_path"] = browser_path
    else:
        logger.info("No system browser found; using Playwright's bundled Chromium.")

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": 1640, "height": 1200}, device_scale_factor=2)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.locator(".page").screenshot(path=str(png_path))
        browser.close()
    logger.info("Wrote PNG: %s", png_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render AI aesthetic sales report V2.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--no-screenshot", action="store_true", help="Only write HTML/assets, skip PNG export.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed progress logs.")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(message)s",
    )

    manifest_path = args.manifest.expanduser().resolve()
    logger.info("Loading manifest: %s", manifest_path)
    manifest = load_manifest(manifest_path)
    manifest_dir = manifest_path.parent
    data = merged(manifest)
    out_dir = args.out.expanduser().resolve()
    assets_dir = out_dir / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    before = copy_asset(data.get("before_image"), assets_dir, "before", manifest_dir)
    effect = copy_asset(data.get("effect_image") or data.get("ai_effect_image"), assets_dir, "effect", manifest_dir)
    after = copy_asset(data.get("after_image"), assets_dir, "after", manifest_dir)
    if not before or not after:
        raise SystemExit("Manifest requires before_image and after_image.")

    project_images = []
    for idx, item in enumerate(data["project_mappings"][:5], start=1):
        project_images.append(crop_asset(data.get("after_image"), assets_dir, item.get("crop_box"), f"project-{idx}", manifest_dir))

    html_path = out_dir / "report-v2.html"
    html_path.write_text(render_html(data, before, after, project_images), encoding="utf-8")
    logger.info("Wrote HTML report: %s", html_path)
    entry_path = out_dir / "00_交付入口.html"
    entry_path.write_text(render_entry(before, effect, after), encoding="utf-8")
    logger.info("Wrote delivery entry page: %s", entry_path)

    if not args.no_screenshot:
        screenshot_png(html_path, out_dir / "report-v2.png")

    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
