#!/usr/bin/env python3
"""Validate repository or installed skill layout for AI aesthetic report."""

from __future__ import annotations

import argparse
import importlib.util
import py_compile
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def require(path: Path) -> None:
    if not path.exists():
        fail(f"missing: {path}")
    ok(f"exists: {path}")


def validate_common(root: Path) -> None:
    required = [
        "SKILL.md",
        "agents/AGENTS.md",
        "agents/face-report-agents.yaml",
        "references/report-spec.md",
        "scripts/render_report.py",
        "scripts/render_sales_v2.py",
        "templates/网资沟通文案_复制即用版.md",
        "templates/网资沟通文案_复制即用版.docx",
        "templates/网资咨询师承接跟进表_详细版.md",
        "templates/网资咨询师承接跟进表_详细版.xlsx",
    ]
    for item in required:
        require(root / item)

    py_compile.compile(str(root / "scripts/render_report.py"), doraise=True)
    py_compile.compile(str(root / "scripts/render_sales_v2.py"), doraise=True)
    ok("render scripts compile")

    if importlib.util.find_spec("PIL") is None:
        fail("Pillow is not installed in this Python environment")
    ok("Pillow import available")


def validate_repo(root: Path) -> None:
    required = [
        "README.md",
        "PRIVACY.md",
        "requirements.txt",
        "install.sh",
        "uninstall.sh",
        "sample/manifest.example.json",
        "sample/manifest.demo.json",
        "sample/demo-inputs/demo-before.svg",
        "sample/demo-inputs/demo-after-clean.svg",
        "sample/demo-inputs/demo-after-annotated.svg",
        "skill/SKILL.md",
        "scripts/self_check.py",
        "scripts/render_sales_v2.py",
    ]
    for item in required:
        require(root / item)

    tracked_like_images = [
        p for p in root.rglob("*")
        if p.is_file()
        and ".git" not in p.parts
        and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic"}
    ]
    if tracked_like_images:
        fail("image files found in repository working tree: " + ", ".join(str(p) for p in tracked_like_images[:10]))
    ok("no image files in repository working tree")

    skill_required = [
        "skill/SKILL.md",
        "skill/agents/AGENTS.md",
        "skill/agents/face-report-agents.yaml",
        "skill/references/report-spec.md",
        "scripts/render_report.py",
        "scripts/render_sales_v2.py",
        "templates/网资沟通文案_复制即用版.md",
        "templates/网资沟通文案_复制即用版.docx",
        "templates/网资咨询师承接跟进表_详细版.md",
        "templates/网资咨询师承接跟进表_详细版.xlsx",
    ]
    for item in skill_required:
        require(root / item)

    py_compile.compile(str(root / "scripts/render_report.py"), doraise=True)
    py_compile.compile(str(root / "scripts/render_sales_v2.py"), doraise=True)
    py_compile.compile(str(root / "scripts/self_check.py"), doraise=True)
    ok("render scripts compile")

    if importlib.util.find_spec("PIL") is None:
        fail("Pillow is not installed in this Python environment")
    ok("Pillow import available")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, help="repository root to validate")
    parser.add_argument("--target", type=Path, help="installed skill directory to validate")
    args = parser.parse_args()

    if bool(args.repo) == bool(args.target):
        fail("provide exactly one of --repo or --target")

    if args.repo:
        validate_repo(args.repo.resolve())
    else:
        validate_common(args.target.resolve())

    ok("validation complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
