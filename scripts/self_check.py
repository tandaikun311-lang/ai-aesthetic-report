#!/usr/bin/env python3
"""Run a repository self-check and render the synthetic demo manifest."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"[FAIL] missing expected output: {path}")
    print(f"[OK] generated: {path}")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Validate layout and render the privacy-safe demo.")
    parser.add_argument("--out", type=Path, default=repo / "outputs" / "self-check-demo")
    parser.add_argument("--with-screenshot", action="store_true", help="Also export report-v2.png. Requires Playwright and a browser.")
    args = parser.parse_args()

    out_dir = args.out.expanduser().resolve()
    outputs_root = (repo / "outputs").resolve()
    if out_dir.exists() and (out_dir == outputs_root or outputs_root in out_dir.parents):
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    run([sys.executable, "scripts/validate_install.py", "--repo", str(repo)], repo)

    render_cmd = [
        sys.executable,
        "scripts/render_sales_v2.py",
        "--manifest",
        "sample/manifest.demo.json",
        "--out",
        str(out_dir),
    ]
    if not args.with_screenshot:
        render_cmd.append("--no-screenshot")
    run(render_cmd, repo)

    require(out_dir / "report-v2.html")
    require(out_dir / "00_交付入口.html")
    require(out_dir / "assets" / "before.svg")
    require(out_dir / "assets" / "effect.svg")
    require(out_dir / "assets" / "after.svg")
    if args.with_screenshot:
        require(out_dir / "report-v2.png")

    html = (out_dir / "report-v2.html").read_text(encoding="utf-8")
    if "状态更亮，轮廓更干净" not in html:
        raise SystemExit("[FAIL] demo report title not found in rendered HTML")
    print("[OK] demo manifest rendered successfully")
    print(f"[DONE] open {out_dir / 'report-v2.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
