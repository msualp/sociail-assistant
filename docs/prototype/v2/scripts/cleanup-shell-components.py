#!/usr/bin/env python3
"""Keep only the largest connected component in generated shell STLs.

This removes tiny detached islands that can appear after heavy boolean ops and
trigger slicer warnings or extra floating parts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import trimesh


DEFAULT_FILES = [
    "shell-top.stl",
    "shell-bottom.stl",
    "shell-top-print.stl",
    "shell-bottom-print.stl",
    "shell-top-print-screws.stl",
    "shell-bottom-print-screws.stl",
]


def clean_file(path: Path) -> int:
    mesh = trimesh.load_mesh(path, process=True)
    parts = mesh.split(only_watertight=False)
    if len(parts) <= 1:
        return 0

    main = max(parts, key=lambda p: abs(float(p.volume)))
    if "bottom" in path.name:
        main.apply_translation([0.0, 0.0, -float(main.bounds[0, 2])])
    main.export(path)
    return len(parts) - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs="+", help="Variant directories to clean")
    args = parser.parse_args()

    for d in args.dirs:
        root = Path(d)
        for name in DEFAULT_FILES:
            p = root / name
            if not p.exists():
                continue
            removed = clean_file(p)
            if removed:
                print(f"{p}: removed {removed} detached components")


if __name__ == "__main__":
    main()
