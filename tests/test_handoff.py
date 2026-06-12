"""Unit tests for the handoff sheet builder."""

import build_handoff_sheet as h


def test_handoff_defaults_derive_from_mappings():
    data = {
        "project_mappings": [
            {"label": "眼周提亮", "project": "眼周管理", "solves": "疲态"},
        ]
    }
    sections = h.handoff_defaults(data)
    titles = [s["title"] for s in sections]
    assert any("发图" in t for t in titles)
    assert any("拆点" in t for t in titles)
    breakdown = next(s for s in sections if "拆点" in s["title"])
    assert any("眼周提亮" in line for line in breakdown["lines"])


def test_resolve_talk_track_uses_custom_when_valid():
    custom = [{"title": "自定义环节", "lines": ["要点一"]}]
    assert h.resolve_talk_track({"handoff": custom}) == custom


def test_resolve_talk_track_falls_back_on_invalid():
    # Missing 'lines' -> not a valid custom track -> defaults used.
    sections = h.resolve_talk_track({"handoff": [{"title": "x"}]})
    assert len(sections) == 5


def test_render_handoff_html_includes_images_and_sections():
    data = {"client_label": "TEST", "project_mappings": []}
    images = [
        {"label": "01 原图", "src": "assets/a.png"},
        {"label": "02 客户 AI 效果图", "src": "assets/b.png"},
    ]
    sections = h.handoff_defaults(data)
    html = h.render_handoff_html(data, images, sections)
    assert "assets/a.png" in html
    assert "assets/b.png" in html
    assert "TEST" in html
    assert html.count('class="shot"') == 2
    assert html.count('class="talk"') == len(sections)


def test_collect_images_skips_missing(tmp_path):
    assets = tmp_path / "assets"
    assets.mkdir()
    # No image files exist on disk and manifest provides none -> empty list.
    images = h.collect_images({}, assets, tmp_path, None)
    assert images == []
