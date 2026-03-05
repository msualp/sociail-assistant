#!/usr/bin/env python3
"""
Generate sheet-style combined STLs for r3 variants.

Outputs:
- prototype/v3/sheets/r3-loose-pair-sheet.stl
- prototype/v3/sheets/r3-mid-pair-sheet.stl
- prototype/v3/sheets/r3-tight-pair-sheet.stl
- prototype/v3/sheets/r3-loose-pair-sheet-screws.stl
- prototype/v3/sheets/r3-mid-pair-sheet-screws.stl
- prototype/v3/sheets/r3-tight-pair-sheet-screws.stl
- prototype/v3/sheets/r3-abc-6up-sheet.stl
- prototype/v3/sheets/r3-abc-6up-sheet-screws.stl
- prototype/v3/sheets/r3-internals-v1-abc-6up-sheet.stl
- prototype/v3/sheets/r3-internals-v1-abc-6up-sheet-screws.stl
- prototype/v3/sheets/r3-internals-v1-bottoms-3up-sheet.stl
- prototype/v3/sheets/r3-internals-v1-bottoms-3up-sheet-screws.stl

These are single-file imports for Bambu Studio.
"""

from __future__ import annotations

import math
from pathlib import Path

import trimesh


ROOT = Path("prototype/v3")
OUT = ROOT / "sheets"
VARIANTS = ["r3-loose", "r3-mid", "r3-tight"]
VARIANTS_INTERNALS = ["r3-internals-v1-loose", "r3-internals-v1", "r3-internals-v1-tight"]


def load_mesh(path: Path) -> trimesh.Trimesh:
    # Use processed load so shared vertices are welded and adjacency is retained.
    m = trimesh.load_mesh(path, process=True)
    if not isinstance(m, trimesh.Trimesh):
        raise RuntimeError(f"Expected Trimesh at {path}")
    return m


def placed(mesh: trimesh.Trimesh, x: float, y: float) -> trimesh.Trimesh:
    out = mesh.copy()
    b = out.bounds
    cx = (b[0, 0] + b[1, 0]) / 2.0
    cy = (b[0, 1] + b[1, 1]) / 2.0
    min_z = b[0, 2]
    out.apply_translation([x - cx, y - cy, -min_z])
    return out


def extent_xy(mesh: trimesh.Trimesh) -> tuple[float, float]:
    b = mesh.bounds
    return float(b[1, 0] - b[0, 0]), float(b[1, 1] - b[0, 1])


def write_mesh(path: Path, meshes: list[trimesh.Trimesh]) -> tuple[float, float, float]:
    combined = trimesh.util.concatenate(meshes)
    combined.merge_vertices()
    combined.remove_infinite_values()
    combined.update_faces(combined.unique_faces())
    combined.update_faces(combined.nondegenerate_faces())
    combined.remove_unreferenced_vertices()
    combined.export(path)
    b = combined.bounds
    return (
        float(b[1, 0] - b[0, 0]),
        float(b[1, 1] - b[0, 1]),
        float(b[1, 2] - b[0, 2]),
    )


def support_area_score(mesh: trimesh.Trimesh, nz_threshold: float = -0.35) -> float:
    # Approximate support-demanded area using downward-facing triangles.
    n = mesh.face_normals
    a = mesh.area_faces
    return float(a[n[:, 2] < nz_threshold].sum())


def flip_x_180(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    out = mesh.copy()
    xf = trimesh.transformations.rotation_matrix(math.pi, [1.0, 0.0, 0.0])
    out.apply_transform(xf)
    return out


def rotate_y_90(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    out = mesh.copy()
    xf = trimesh.transformations.rotation_matrix(math.pi / 2.0, [0.0, 1.0, 0.0])
    out.apply_transform(xf)
    return out


def orient_top_for_less_support(mesh: trimesh.Trimesh) -> tuple[trimesh.Trimesh, bool]:
    keep = mesh.copy()
    flip = flip_x_180(mesh)
    keep_score = support_area_score(keep)
    flip_score = support_area_score(flip)
    if flip_score + 1e-6 < keep_score:
        return flip, True
    return keep, False


def build_pair_sheet(
    variant: str,
    top_file: str,
    bottom_file: str,
    suffix: str,
    gap: float = 14.0,
) -> tuple[str, tuple[float, float, float]]:
    base = ROOT / variant
    top = load_mesh(base / top_file)
    bottom = load_mesh(base / bottom_file)

    top_w, _ = extent_xy(top)
    bottom_w, _ = extent_xy(bottom)

    total = top_w + gap + bottom_w
    top_x = -total / 2.0 + top_w / 2.0
    bottom_x = total / 2.0 - bottom_w / 2.0

    meshes = [placed(top, top_x, 0.0), placed(bottom, bottom_x, 0.0)]
    out_file = OUT / f"{variant}-{suffix}.stl"
    dims = write_mesh(out_file, meshes)
    return out_file.name, dims


def build_6up_sheet(
    variants: list[str],
    top_file: str,
    bottom_file: str,
    out_name: str,
    gap_x: float = 10.0,
    gap_y: float = 12.0,
    optimize_tops: bool = False,
    force_flip_tops: bool = False,
    rotate_all_y_90: bool = False,
) -> tuple[str, tuple[float, float, float]]:
    if len(variants) != 3:
        raise ValueError("6-up sheet expects exactly 3 variants")

    tops: list[trimesh.Trimesh] = []
    flipped = 0
    for v in variants:
        tm = load_mesh(ROOT / v / top_file)
        if force_flip_tops:
            tm = flip_x_180(tm)
            flipped += 1
        elif optimize_tops:
            tm, was_flipped = orient_top_for_less_support(tm)
            if was_flipped:
                flipped += 1
        if rotate_all_y_90:
            tm = rotate_y_90(tm)
        tops.append(tm)

    bottoms = []
    for v in variants:
        bm = load_mesh(ROOT / v / bottom_file)
        if rotate_all_y_90:
            bm = rotate_y_90(bm)
        bottoms.append(bm)
    all_meshes = tops + bottoms

    max_w = max(extent_xy(m)[0] for m in all_meshes)
    max_h = max(extent_xy(m)[1] for m in all_meshes)
    pitch_x = max_w + gap_x
    pitch_y = max_h + gap_y

    xs = [-pitch_x, 0.0, pitch_x]
    y_top = pitch_y / 2.0
    y_bottom = -pitch_y / 2.0

    placed_meshes: list[trimesh.Trimesh] = []
    for i, m in enumerate(tops):
        placed_meshes.append(placed(m, xs[i], y_top))
    for i, m in enumerate(bottoms):
        placed_meshes.append(placed(m, xs[i], y_bottom))

    out_file = OUT / out_name
    dims = write_mesh(out_file, placed_meshes)
    if optimize_tops:
        print(f"{out_name}: top orientation optimized (flipped {flipped}/3)")
    return out_file.name, dims


def build_3up_row_sheet(
    variants: list[str],
    mesh_file: str,
    out_name: str,
    gap_x: float = 10.0,
) -> tuple[str, tuple[float, float, float]]:
    if len(variants) != 3:
        raise ValueError("3-up row expects exactly 3 variants")

    meshes = [load_mesh(ROOT / v / mesh_file) for v in variants]
    max_w = max(extent_xy(m)[0] for m in meshes)
    pitch_x = max_w + gap_x
    xs = [-pitch_x, 0.0, pitch_x]

    placed_meshes: list[trimesh.Trimesh] = []
    for i, m in enumerate(meshes):
        placed_meshes.append(placed(m, xs[i], 0.0))

    out_file = OUT / out_name
    dims = write_mesh(out_file, placed_meshes)
    return out_file.name, dims


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    summary: list[str] = []
    for variant in VARIANTS:
        name, dims = build_pair_sheet(
            variant,
            "shell-top-print.stl",
            "shell-bottom-print.stl",
            "pair-sheet",
        )
        summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

        name, dims = build_pair_sheet(
            variant,
            "shell-top-print-screws.stl",
            "shell-bottom-print-screws.stl",
            "pair-sheet-screws",
        )
        summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    name, dims = build_6up_sheet(
        VARIANTS,
        "shell-top-print.stl",
        "shell-bottom-print.stl",
        "r3-abc-6up-sheet.stl",
        optimize_tops=True,
        rotate_all_y_90=True,
    )
    summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    name, dims = build_6up_sheet(
        VARIANTS,
        "shell-top-print-screws.stl",
        "shell-bottom-print-screws.stl",
        "r3-abc-6up-sheet-screws.stl",
        force_flip_tops=True,
    )
    summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    name, dims = build_6up_sheet(
        VARIANTS_INTERNALS,
        "shell-top-print.stl",
        "shell-bottom-print.stl",
        "r3-internals-v1-abc-6up-sheet.stl",
        optimize_tops=True,
    )
    summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    name, dims = build_6up_sheet(
        VARIANTS_INTERNALS,
        "shell-top-print-screws.stl",
        "shell-bottom-print-screws.stl",
        "r3-internals-v1-abc-6up-sheet-screws.stl",
        optimize_tops=True,
    )
    summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    name, dims = build_3up_row_sheet(
        VARIANTS_INTERNALS,
        "shell-bottom-print.stl",
        "r3-internals-v1-bottoms-3up-sheet.stl",
    )
    summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    name, dims = build_3up_row_sheet(
        VARIANTS_INTERNALS,
        "shell-bottom-print-screws.stl",
        "r3-internals-v1-bottoms-3up-sheet-screws.stl",
    )
    summary.append(f"{name}: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    readme = OUT / "README.md"
    readme.write_text(
        """# v3 Sheet Files

Single-file plate STLs for quick Bambu Studio imports.

## Files
- `r3-loose-pair-sheet.stl`: top+bottom print shells for r3-loose
- `r3-mid-pair-sheet.stl`: top+bottom print shells for r3-mid
- `r3-tight-pair-sheet.stl`: top+bottom print shells for r3-tight
- `r3-loose-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-loose
- `r3-mid-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-mid
- `r3-tight-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-tight
- `r3-abc-6up-sheet.stl`: loose/mid/tight top+bottom together (6 parts)
- `r3-abc-6up-sheet-screws.stl`: loose/mid/tight top+bottom screw-hole set (6 parts)
- `r3-internals-v1-abc-6up-sheet.stl`: internals loose/base/tight top+bottom together (6 parts)
- `r3-internals-v1-abc-6up-sheet-screws.stl`: internals loose/base/tight screw-hole set (6 parts)
- `r3-internals-v1-bottoms-3up-sheet.stl`: internals loose/base/tight bottoms only (3 parts)
- `r3-internals-v1-bottoms-3up-sheet-screws.stl`: internals loose/base/tight bottoms only with screw holes (3 parts)

## Notes
- Pair sheets are intended for one-variant print jobs.
- Screw pair sheets use `shell-*-print-screws.stl` sources.
- 6-up sheets are intended for larger beds (roughly 256x256 class).
- `r3-abc-6up-sheet.stl` is side-oriented to reduce floating-cantilever warnings.
- Other 6-up top rows are auto-oriented to reduce support demand.
- For internals fit A/B testing without cantilever warnings, use bottoms-only 3-up sheets.
- In Bambu Studio, you can keep as-is or use "Split to Objects" for per-part controls.
""",
        encoding="utf-8",
    )

    print("Sheet build summary:")
    for line in summary:
        print(line)


if __name__ == "__main__":
    main()
