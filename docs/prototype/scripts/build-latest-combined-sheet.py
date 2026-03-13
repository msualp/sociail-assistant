#!/usr/bin/env python3
"""Build a single combined sheet containing the latest v2 + v4 print shells and buttons."""

from __future__ import annotations

import math
from pathlib import Path

import trimesh

ROOT = Path("prototype")
OUT_DIR = ROOT / "sheets-latest"

V2_DIR = ROOT / "v2" / "r3-mid"
V4_DIR = ROOT / "v4" / "r2-mid"
BUTTONS_DIR = ROOT / "modules" / "button-module-22-24-v1"

V2_TOP = V2_DIR / "shell-top-print.stl"
V2_BOTTOM = V2_DIR / "shell-bottom-print.stl"
V4_TOP = V4_DIR / "shell-top-print.stl"
V4_BOTTOM = V4_DIR / "shell-bottom-print.stl"

PLUNGER = BUTTONS_DIR / "plunger_concave_24mm.stl"
BEZEL = BUTTONS_DIR / "bezel_guard_24mm.stl"

OUT_FILE = OUT_DIR / "latest-v2-v4-sheet.stl"


def load_mesh(path: Path) -> trimesh.Trimesh:
    mesh = trimesh.load_mesh(path, process=True)
    if not isinstance(mesh, trimesh.Trimesh):
        raise RuntimeError(f"Expected Trimesh for {path}")
    return mesh


def rotate_x_180(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    out = mesh.copy()
    xf = trimesh.transformations.rotation_matrix(math.pi, [1.0, 0.0, 0.0])
    out.apply_transform(xf)
    return out


def placed(mesh: trimesh.Trimesh, x: float, y: float) -> trimesh.Trimesh:
    out = mesh.copy()
    bounds = out.bounds
    cx = (bounds[0, 0] + bounds[1, 0]) / 2.0
    cy = (bounds[0, 1] + bounds[1, 1]) / 2.0
    zmin = bounds[0, 2]
    out.apply_translation([x - cx, y - cy, -zmin])
    return out


def extent_xy(mesh: trimesh.Trimesh) -> tuple[float, float]:
    bounds = mesh.bounds
    return float(bounds[1, 0] - bounds[0, 0]), float(bounds[1, 1] - bounds[0, 1])


def build_pair(top: trimesh.Trimesh, bottom: trimesh.Trimesh, gap: float) -> tuple[list[trimesh.Trimesh], float, float]:
    top_w, top_h = extent_xy(top)
    bottom_w, bottom_h = extent_xy(bottom)
    total = top_w + gap + bottom_w
    top_x = -total / 2.0 + top_w / 2.0
    bottom_x = total / 2.0 - bottom_w / 2.0
    meshes = [placed(top, top_x, 0.0), placed(bottom, bottom_x, 0.0)]
    return meshes, total, max(top_h, bottom_h)


def build_button_group(plunger: trimesh.Trimesh, bezel: trimesh.Trimesh, gap: float) -> tuple[list[trimesh.Trimesh], float, float]:
    p_w, p_h = extent_xy(plunger)
    b_w, b_h = extent_xy(bezel)
    group_h = p_h + gap + b_h
    p_y = group_h / 2.0 - p_h / 2.0
    b_y = -group_h / 2.0 + b_h / 2.0
    meshes = [placed(plunger, 0.0, p_y), placed(bezel, 0.0, b_y)]
    return meshes, max(p_w, b_w), group_h


def translate(mesh: trimesh.Trimesh, dx: float, dy: float) -> trimesh.Trimesh:
    out = mesh.copy()
    out.apply_translation([dx, dy, 0.0])
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    v2_top = rotate_x_180(load_mesh(V2_TOP))
    v2_bottom = load_mesh(V2_BOTTOM)
    v4_top = rotate_x_180(load_mesh(V4_TOP))
    v4_bottom = load_mesh(V4_BOTTOM)

    plunger = rotate_x_180(load_mesh(PLUNGER))
    bezel = rotate_x_180(load_mesh(BEZEL))

    gap_x = 12.0
    gap_y = 16.0
    button_gap_y = 6.0

    v4_pair, v4_pair_w, v4_pair_h = build_pair(v4_top, v4_bottom, gap_x)
    v2_pair, v2_pair_w, v2_pair_h = build_pair(v2_top, v2_bottom, gap_x)

    v4_btns, v4_btn_w, v4_btn_h = build_button_group(plunger, bezel, button_gap_y)
    v2_btns, v2_btn_w, v2_btn_h = build_button_group(plunger, bezel, button_gap_y)

    v4_row_h = max(v4_pair_h, v4_btn_h)
    v2_row_h = max(v2_pair_h, v2_btn_h)

    y_top = v2_row_h / 2.0 + gap_y / 2.0
    y_bottom = -(v4_row_h / 2.0 + gap_y / 2.0)

    v4_btn_x = v4_pair_w / 2.0 + gap_x + v4_btn_w / 2.0
    v2_btn_x = v2_pair_w / 2.0 + gap_x + v2_btn_w / 2.0

    meshes: list[trimesh.Trimesh] = []
    meshes += [translate(m, 0.0, y_bottom) for m in v4_pair]
    meshes += [translate(m, v4_btn_x, y_bottom) for m in v4_btns]
    meshes += [translate(m, 0.0, y_top) for m in v2_pair]
    meshes += [translate(m, v2_btn_x, y_top) for m in v2_btns]

    combined = trimesh.util.concatenate(meshes)
    combined.merge_vertices()
    combined.remove_infinite_values()
    combined.update_faces(combined.unique_faces())
    combined.update_faces(combined.nondegenerate_faces())
    combined.remove_unreferenced_vertices()
    combined.export(OUT_FILE)

    b = combined.bounds
    dims = (float(b[1, 0] - b[0, 0]), float(b[1, 1] - b[0, 1]), float(b[1, 2] - b[0, 2]))
    print(f"Wrote {OUT_FILE} ({dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm)")


if __name__ == "__main__":
    main()
