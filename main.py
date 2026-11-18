#!/usr/bin/env python3
"""
make.fun entry — "Sum up 18 November's world news in one image".

The generated front page is committed next to this file as entry.png.
At run time there is no network and no third-party package, so the only
job of the program is to place those committed bytes at /output/entry.png.
Standard library only, deterministic across both grading runs.
"""
import os
import shutil
from pathlib import Path

# Where the grader tells us to write the single output image.
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT = OUT_DIR / "entry.png"


def locate_source() -> Path:
    """Find the committed image relative to this script (/bot at grading)."""
    here = Path(__file__).resolve().parent
    candidates = [here / "entry.png", Path("/bot/entry.png")]
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("entry.png is missing from the repository root")


def main() -> None:
    src = locate_source()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # copyfile writes identical bytes on every run; no timestamps, no RNG.
    with src.open("rb") as fsrc, OUT.open("wb") as fdst:
        shutil.copyfileobj(fsrc, fdst)
    # Guard the gate: the image must be a whole, non-empty PNG under 1 MiB.
    size = OUT.stat().st_size
    if size == 0 or size > 1048576:
        raise RuntimeError(f"entry.png has invalid size: {size} bytes")


if __name__ == "__main__":
    main()
