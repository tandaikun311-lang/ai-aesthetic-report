"""Unit tests for the V2 sales report renderer."""

import json
from pathlib import Path

import pytest

import render_sales_v2 as r


def test_esc_escapes_html():
    assert r.esc('<a href="x">&') == "&lt;a href=&quot;x&quot;&gt;&amp;"
    assert r.esc(None) == ""


def test_load_manifest_valid(tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"title": "Hi"}), encoding="utf-8")
    assert r.load_manifest(p)["title"] == "Hi"


def test_load_manifest_missing(tmp_path):
    with pytest.raises(SystemExit):
        r.load_manifest(tmp_path / "nope.json")


def test_load_manifest_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(SystemExit):
        r.load_manifest(p)


def test_load_manifest_not_object(tmp_path):
    p = tmp_path / "arr.json"
    p.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(SystemExit):
        r.load_manifest(p)


def test_render_rejects_missing_clean_effect_without_creating_output(tmp_path):
    manifest = tmp_path / "manifest.json"
    case = json.loads((Path(__file__).resolve().parents[1] / "sample" / "manifest.demo.json").read_text(encoding="utf-8"))
    case.pop("effect_image")
    manifest.write_text(json.dumps(case), encoding="utf-8")
    output = tmp_path / "report"
    with pytest.raises(SystemExit, match="separate clean effect_image"):
        r.main(["--manifest", str(manifest), "--out", str(output), "--no-screenshot"])
    assert not output.exists()


def test_render_rejects_generic_default_diagnosis(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"before_image": "before.png", "effect_image": "effect.png", "after_image": "annotated.png"}), encoding="utf-8")
    with pytest.raises(SystemExit, match="case-specific content"):
        r.main(["--manifest", str(manifest), "--out", str(tmp_path / "report"), "--no-screenshot"])


def test_defaults_has_core_keys():
    d = r.defaults()
    for key in ("client_label", "title", "diagnosis", "project_mappings", "advice"):
        assert key in d
    assert len(d["project_mappings"]) >= 1


def test_merged_overrides_and_keeps_defaults():
    merged = r.merged({"title": "自定义标题", "subtitle": ""})
    assert merged["title"] == "自定义标题"          # overridden
    assert merged["subtitle"] == r.defaults()["subtitle"]  # empty string ignored -> default kept
    assert merged["diagnosis"] == r.defaults()["diagnosis"]  # missing -> default


def test_merged_rejects_empty_lists():
    merged = r.merged({"diagnosis": []})
    assert merged["diagnosis"] == r.defaults()["diagnosis"]


def test_resolve_input_path_relative(tmp_path):
    resolved = r.resolve_input_path("a/b.png", tmp_path)
    assert resolved == (tmp_path / "a" / "b.png").resolve()


def test_resolve_input_path_none():
    assert r.resolve_input_path(None, None) is None


def test_find_browser_env_override(tmp_path, monkeypatch):
    fake = tmp_path / "mychrome"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setenv("BROWSER_PATH", str(fake))
    assert r.find_browser() == str(fake)


def test_render_html_contains_images_and_titles():
    data = r.merged({"title": "Demo标题"})
    html = r.render_html(data, "assets/before.png", "assets/after.png", [])
    assert "Demo标题" in html
    assert "assets/before.png" in html
    assert "assets/after.png" in html


def test_crop_asset_writes_cropped_image(tmp_path):
    from PIL import Image

    src = tmp_path / "src.png"
    Image.new("RGB", (100, 100), "white").save(src)
    assets = tmp_path / "assets"
    assets.mkdir()
    rel = r.crop_asset(str(src), assets, [0.0, 0.0, 0.5, 0.5], "crop1", tmp_path)
    out = assets / "crop1.jpg"
    assert rel == "assets/crop1.jpg"
    assert out.exists()
    assert Image.open(out).size == (50, 50)
