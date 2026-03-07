#!/usr/bin/env python3
"""
Generate polished v3 MagSafe form-factor printable STL assets.

Design goals:
- Flat MagSafe back, modern rounded perimeter, soft top crown
- Comfortable in hand and robust enough for frequent attach/detach demos
- Bambu-ready print pair with optional screw-hole variants
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from meshlib import mrmeshpy as mr


OUT_DIR = Path("prototype/v3/polished-r1")

# Envelope
LENGTH = 78.0
WIDTH = 64.0
HEIGHT = 16.0
WALL = 2.4
SPLIT_Z = 9.2

# Body shaping: rounded-rectangle core + large offset, then clipped to flat back
CORE_X = 62.0
CORE_Y = 48.0
CORE_Z = 8.0
BODY_RADIUS = 8.0

# Assembly features
LIP_WIDTH = 1.0
LIP_HEIGHT = 1.0
LIP_CLEARANCE = 0.12

SNAP_WIDTH = 4.5
SNAP_LENGTH_Z = 7.0
SNAP_ENGAGE = 0.80

# 24mm center button module defaults (22mm remains alternate).
BUTTON_CENTER_X = 0.0
BUTTON_CENTER_Y = -8.0
BUTTON_PLUNGER_OD = 24.0
BUTTON_CUTOUT_OD = BUTTON_PLUNGER_OD + 0.6
BUTTON_BEZEL_OD = BUTTON_PLUNGER_OD + 4.0
BUTTON_ISLAND_OD = BUTTON_BEZEL_OD + 2.0
BUTTON_ISLAND_RECESS = 0.6


@dataclass
class BoxSpec:
    sx: float
    sy: float
    sz: float
    cx: float
    cy: float
    cz: float


def vec(x: float, y: float, z: float) -> mr.Vector3f:
    return mr.Vector3f(float(x), float(y), float(z))


def copy_mesh(mesh: mr.Mesh) -> mr.Mesh:
    return mr.Mesh(mesh)


def save_mesh(mesh: mr.Mesh, path: Path) -> None:
    mesh.packOptimally(True)
    mr.saveMesh(mesh, str(path))


def box_mesh(spec: BoxSpec) -> mr.Mesh:
    base = vec(spec.cx - spec.sx / 2, spec.cy - spec.sy / 2, spec.cz - spec.sz / 2)
    size = vec(spec.sx, spec.sy, spec.sz)
    return mr.makeCube(size, base)


def cyl_z(radius: float, length: float, cx: float, cy: float, cz: float, res: int = 96) -> mr.Mesh:
    m = mr.makeCylinder(radius, length, res)
    m.transform(mr.AffineXf3f.translation(vec(cx, cy, cz - length / 2)))
    return m


def cyl_axis(
    radius: float,
    length: float,
    cx: float,
    cy: float,
    cz: float,
    axis: str,
    res: int = 64,
) -> mr.Mesh:
    m = mr.makeCylinder(radius, length, res)
    m.transform(mr.AffineXf3f.translation(vec(0, 0, -length / 2)))

    if axis == "y":
        rot = mr.Matrix3f(vec(1, 0, 0), vec(0, 0, 1), vec(0, -1, 0))
        xf = mr.AffineXf3f()
        xf.A = rot
        xf.b = vec(0, 0, 0)
        m.transform(xf)
    elif axis == "x":
        rot = mr.Matrix3f(vec(0, 0, 1), vec(0, 1, 0), vec(-1, 0, 0))
        xf = mr.AffineXf3f()
        xf.A = rot
        xf.b = vec(0, 0, 0)
        m.transform(xf)
    elif axis != "z":
        raise ValueError(f"Unsupported axis: {axis}")

    m.transform(mr.AffineXf3f.translation(vec(cx, cy, cz)))
    return m


def oriented_box(
    cx: float,
    cy: float,
    cz: float,
    size_t: float,
    size_i: float,
    size_z: float,
    tx: float,
    ty: float,
    ix: float,
    iy: float,
) -> mr.Mesh:
    m = box_mesh(BoxSpec(size_t, size_i, size_z, 0, 0, 0))
    A = mr.Matrix3f(vec(tx, ix, 0), vec(ty, iy, 0), vec(0, 0, 1))
    xf = mr.AffineXf3f()
    xf.A = A
    xf.b = vec(cx, cy, cz)
    m.transform(xf)
    return m


def merge(parts: list[mr.Mesh]) -> mr.Mesh:
    out = copy_mesh(parts[0])
    for p in parts[1:]:
        out.addMesh(p)
    return out


def _voxel_subtract(a: mr.Mesh, b: mr.Mesh, voxel_size: float = 0.15, max_error: float = 0.08) -> mr.Mesh:
    m = mr.voxelBooleanSubtract(a, b, voxel_size)
    dec = mr.DecimateSettings()
    dec.maxError = max_error
    dec.maxDeletedFaces = m.topology.numValidFaces()
    mr.decimateMesh(m, dec)
    return m


def boolean(a: mr.Mesh, b: mr.Mesh, op: mr.BooleanOperation, label: str) -> mr.Mesh:
    res = mr.boolean(a, b, op)
    if res.valid():
        return res.mesh

    if op == mr.BooleanOperation.DifferenceAB:
        return _voxel_subtract(a, b)
    if op == mr.BooleanOperation.Union:
        return mr.voxelBooleanUnite(a, b, 0.15)
    if op == mr.BooleanOperation.Intersection:
        return mr.voxelBooleanIntersect(a, b, 0.15)

    raise RuntimeError(f"Boolean failed for {label}: {res.errorString}")


def fuse_union(parts: list[mr.Mesh], label: str) -> mr.Mesh:
    out = copy_mesh(parts[0])
    for i, p in enumerate(parts[1:], start=2):
        out = boolean(out, p, mr.BooleanOperation.Union, f"{label}_u{i}")
    return out


def subtract_many(base: mr.Mesh, cutters: list[mr.Mesh], label: str) -> mr.Mesh:
    out = copy_mesh(base)
    for i, c in enumerate(cutters, start=1):
        out = boolean(out, c, mr.BooleanOperation.DifferenceAB, f"{label}_{i}")
    return out


def offset_mesh(mesh: mr.Mesh, delta: float, voxel: float = 0.2) -> mr.Mesh:
    params = mr.OffsetParameters()
    params.voxelSize = voxel
    return mr.offsetMesh(mr.MeshPart(mesh), delta, params)


def slab(z_min: float, z_max: float) -> mr.Mesh:
    return box_mesh(BoxSpec(240, 240, z_max - z_min, 0, 0, (z_min + z_max) / 2))


def build_outer_body() -> mr.Mesh:
    core = box_mesh(BoxSpec(CORE_X, CORE_Y, CORE_Z, 0, 0, CORE_Z / 2))
    params = mr.OffsetParameters()
    params.voxelSize = 0.2
    rounded = mr.offsetMesh(mr.MeshPart(core), BODY_RADIUS, params)

    # Clip to flat back and fixed final height.
    body = boolean(rounded, slab(0.0, HEIGHT), mr.BooleanOperation.Intersection, "body_clip")

    # Normalize center and dimensions.
    bbox = body.getBoundingBox()
    cx = (bbox.min.x + bbox.max.x) / 2
    cy = (bbox.min.y + bbox.max.y) / 2
    dz = -bbox.min.z
    body.transform(mr.AffineXf3f.translation(vec(-cx, -cy, dz)))
    return apply_button_flat_island(body)


def apply_button_flat_island(body: mr.Mesh) -> mr.Mesh:
    island_r = BUTTON_ISLAND_OD / 2.0
    cutter_h = 6.0
    island_z = HEIGHT - BUTTON_ISLAND_RECESS
    cutter = cyl_z(
        island_r,
        cutter_h,
        BUTTON_CENTER_X,
        BUTTON_CENTER_Y,
        island_z + cutter_h / 2.0,
        128,
    )
    return boolean(body, cutter, mr.BooleanOperation.DifferenceAB, "button_island_flat")


def split_shells(outer: mr.Mesh, inner: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    eps = 0.01
    bottom_outer = boolean(outer, slab(-30, SPLIT_Z + eps), mr.BooleanOperation.Intersection, "bottom_outer")
    bottom_inner = boolean(inner, slab(-30, SPLIT_Z + eps), mr.BooleanOperation.Intersection, "bottom_inner")
    bottom = _voxel_subtract(bottom_outer, bottom_inner, voxel_size=0.12, max_error=0.04)

    top_outer = boolean(outer, slab(SPLIT_Z - eps, 40), mr.BooleanOperation.Intersection, "top_outer")
    top_inner = boolean(inner, slab(SPLIT_Z - eps, 40), mr.BooleanOperation.Intersection, "top_inner")
    top = _voxel_subtract(top_outer, top_inner, voxel_size=0.12, max_error=0.04)
    return top, bottom


def add_tongue_groove(top: mr.Mesh, bottom: mr.Mesh, inner: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    lip_outer = offset_mesh(inner, LIP_WIDTH, 0.18)
    groove_outer = offset_mesh(inner, LIP_WIDTH + LIP_CLEARANCE, 0.18)

    lip_ring = boolean(lip_outer, inner, mr.BooleanOperation.DifferenceAB, "lip_ring")
    groove_ring = boolean(groove_outer, inner, mr.BooleanOperation.DifferenceAB, "groove_ring")

    lip = boolean(lip_ring, slab(SPLIT_Z - 0.02, SPLIT_Z + LIP_HEIGHT), mr.BooleanOperation.Intersection, "lip_clip")
    groove = boolean(
        groove_ring,
        slab(SPLIT_Z - 0.2, SPLIT_Z + LIP_HEIGHT + 0.3),
        mr.BooleanOperation.Intersection,
        "groove_clip",
    )

    bottom2 = boolean(bottom, lip, mr.BooleanOperation.Union, "add_lip")
    top2 = boolean(top, groove, mr.BooleanOperation.DifferenceAB, "sub_groove")
    return top2, bottom2


def snap_locations() -> list[tuple[float, float, float, float, float, float]]:
    # four corner-biased positions
    pts = [(30.0, 24.0), (30.0, -24.0), (-30.0, 24.0), (-30.0, -24.0)]
    locs = []
    for x, y in pts:
        nlen = math.hypot(x, y)
        nx, ny = x / nlen, y / nlen
        ix, iy = -nx, -ny
        tx, ty = -ny, nx
        locs.append((x, y, tx, ty, ix, iy))
    return locs


def add_snap_tabs(top: mr.Mesh, bottom: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    tabs: list[mr.Mesh] = []
    slots: list[mr.Mesh] = []
    notches: list[mr.Mesh] = []

    tab_cz = (SPLIT_Z + (SPLIT_Z - SNAP_LENGTH_Z)) / 2
    for i, (px, py, tx, ty, ix, iy) in enumerate(snap_locations(), start=1):
        tab = oriented_box(
            px + ix * 0.9,
            py + iy * 0.9,
            tab_cz,
            SNAP_WIDTH,
            1.4,
            SNAP_LENGTH_Z,
            tx,
            ty,
            ix,
            iy,
        )
        hook = oriented_box(
            px + ix * 2.0,
            py + iy * 2.0,
            SPLIT_Z - 0.5,
            SNAP_WIDTH,
            SNAP_ENGAGE,
            1.0,
            tx,
            ty,
            ix,
            iy,
        )
        tabs.append(boolean(tab, hook, mr.BooleanOperation.Union, f"tab_{i}"))

        slot = oriented_box(
            px + ix * 1.9,
            py + iy * 1.9,
            SPLIT_Z - 3.4,
            SNAP_WIDTH + 1.0,
            1.8,
            5.2,
            tx,
            ty,
            ix,
            iy,
        )
        slots.append(slot)

        notch = oriented_box(
            px + ix * 2.0,
            py + iy * 2.0,
            SPLIT_Z + 0.85,
            SNAP_WIDTH + 0.9,
            SNAP_ENGAGE + 0.7,
            1.8,
            tx,
            ty,
            ix,
            iy,
        )
        notches.append(notch)

    tabs_u = fuse_union(tabs, "tabs")
    slots_u = fuse_union(slots, "slots")
    notches_u = fuse_union(notches, "notches")

    b2 = boolean(bottom, tabs_u, mr.BooleanOperation.Union, "add_tabs")
    b3 = boolean(b2, slots_u, mr.BooleanOperation.DifferenceAB, "sub_slots")
    t2 = boolean(top, notches_u, mr.BooleanOperation.DifferenceAB, "sub_notches")
    return t2, b3


def reopen_bottom_cavity(bottom: mr.Mesh, inner: mr.Mesh) -> mr.Mesh:
    # Some boolean fallback paths can leave a thin seam cap over the bottom cavity.
    # Re-cut with inner geometry to guarantee an open shell at the split plane.
    cutter = boolean(
        inner,
        slab(SPLIT_Z - 0.35, HEIGHT + 6.0),
        mr.BooleanOperation.Intersection,
        "reopen_cavity_clip",
    )
    return boolean(bottom, cutter, mr.BooleanOperation.DifferenceAB, "reopen_bottom_cavity")


def neg_magsafe_ring() -> mr.Mesh:
    outer = cyl_z(28.0, 1.8, 0, 0, 0.9, 128)
    inner = cyl_z(23.0, 2.2, 0, 0, 1.1, 128)
    return boolean(outer, inner, mr.BooleanOperation.DifferenceAB, "magsafe_ring")


def neg_led_window() -> mr.Mesh:
    depth = 3.0
    zc = HEIGHT - depth / 2
    yc = 8.0
    center = box_mesh(BoxSpec(30.0, 4.0, depth, 0.0, yc, zc))
    left = cyl_z(2.0, depth, -15.0, yc, zc, 72)
    right = cyl_z(2.0, depth, 15.0, yc, zc, 72)
    return fuse_union([center, left, right], "led")


def neg_button() -> mr.Mesh:
    cutout = cyl_z(
        BUTTON_CUTOUT_OD / 2.0,
        10.0,
        BUTTON_CENTER_X,
        BUTTON_CENTER_Y,
        HEIGHT - 5.0,
        128,
    )
    return cutout


def neg_usbc_bottom() -> mr.Mesh:
    # opening centered on -Y edge, slightly recessed
    return box_mesh(BoxSpec(12.2, 14.0, 4.4, 0.0, -32.0 - 7.0, 5.0))


def neg_mic_array() -> mr.Mesh:
    holes=[]
    for y in (-9.0, -3.0, 3.0, 9.0):
        holes.append(cyl_axis(0.55, 10.0, 39.5, y, 12.0, "x", 48))
    return merge(holes)


def _speaker_slot(y: float, z: float) -> mr.Mesh:
    body = box_mesh(BoxSpec(10.0, 2.4, 1.2, 39.5, y, z))
    c1 = cyl_axis(0.6, 10.0, 39.5, y - 1.2, z, "x", 48)
    c2 = cyl_axis(0.6, 10.0, 39.5, y + 1.2, z, "x", 48)
    return fuse_union([body, c1, c2], f"spk_{y}_{z}")


def neg_speaker_grill() -> mr.Mesh:
    parts=[]
    for z in (4.6, 6.6):
        for y in (-10.0, -5.0, 0.0, 5.0, 10.0):
            parts.append(_speaker_slot(y, z))
    return fuse_union(parts, "speaker")


def neg_screw_holes() -> mr.Mesh:
    pts = [(-24.0, -20.0), (-24.0, 20.0), (24.0, -20.0), (24.0, 20.0)]
    return merge([cyl_z(1.5, 24.0, x, y, HEIGHT / 2, 48) for x, y in pts])


def regularize_mesh(mesh: mr.Mesh, voxel: float = 0.12) -> mr.Mesh:
    return offset_mesh(mesh, 0.0, voxel)


def decimate_if_needed(mesh: mr.Mesh, max_faces: int, max_error: float = 0.04) -> mr.Mesh:
    faces = mesh.topology.numValidFaces()
    if faces <= max_faces:
        return mesh
    out = copy_mesh(mesh)
    s = mr.DecimateSettings()
    s.maxError = max_error
    s.maxDeletedFaces = max(0, faces - max_faces)
    mr.decimateMesh(out, s)
    return out


def validate(label: str, mesh: mr.Mesh) -> None:
    b = mesh.getBoundingBox()
    print(
        f"{label}: faces={mesh.topology.numValidFaces()} closed={mesh.topology.isClosed()} "
        f"valid={mesh.topology.checkValidity()} bbox=({b.min.x:.2f},{b.min.y:.2f},{b.min.z:.2f})-({b.max.x:.2f},{b.max.y:.2f},{b.max.z:.2f})"
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    outer = build_outer_body()
    inner = offset_mesh(outer, -WALL, 0.2)
    top, bottom = split_shells(outer, inner)
    top, bottom = add_tongue_groove(top, bottom, inner)
    top, bottom = add_snap_tabs(top, bottom)
    bottom = reopen_bottom_cavity(bottom, inner)

    neg_ring = neg_magsafe_ring()
    neg_led = neg_led_window()
    neg_btn = neg_button()
    neg_usb = neg_usbc_bottom()
    neg_mic = neg_mic_array()
    neg_spk = neg_speaker_grill()
    neg_scr = neg_screw_holes()

    top_print = subtract_many(top, [neg_led, neg_btn], "top_print")
    bottom_print = subtract_many(bottom, [neg_ring, neg_usb, neg_mic, neg_spk], "bottom_print")

    top_print_scr = subtract_many(top_print, [neg_scr], "top_print_s")
    bottom_print_scr = subtract_many(bottom_print, [neg_scr], "bottom_print_s")

    # Stabilize and keep slice-friendly sizes.
    meshes = {
        "shell-top.stl": decimate_if_needed(regularize_mesh(top), 90000),
        "shell-bottom.stl": decimate_if_needed(regularize_mesh(bottom), 90000),
        "shell-top-print.stl": decimate_if_needed(regularize_mesh(top_print), 90000),
        "shell-bottom-print.stl": decimate_if_needed(regularize_mesh(bottom_print), 90000),
        "shell-top-print-screws.stl": decimate_if_needed(regularize_mesh(top_print_scr), 90000),
        "shell-bottom-print-screws.stl": decimate_if_needed(regularize_mesh(bottom_print_scr), 90000),
        "neg-magsafe-ring.stl": neg_ring,
        "neg-led-window.stl": neg_led,
        "neg-button.stl": neg_btn,
        "neg-usbc-bottom.stl": neg_usb,
        "neg-mic-array.stl": neg_mic,
        "neg-speaker-grill.stl": regularize_mesh(neg_spk, 0.08),
        "neg-screw-holes-4x.stl": neg_scr,
    }

    for name, mesh in meshes.items():
        save_mesh(mesh, OUT_DIR / name)

    (OUT_DIR / "README.md").write_text(
        """# v3 Polished R1 (MagSafe)

Generated print assets for a modern, rounded MagSafe-friendly enclosure.

## What Changed vs Draft
- Flat back maintained for MagSafe + table stability
- Softer perimeter + top crown for better in-hand feel
- Added tongue-and-groove seam and 4 snap tabs for sturdier assembly
- Normalized print-ready shells with optional screw-hole variants

## Files
- `shell-top.stl`, `shell-bottom.stl`
- `shell-top-print.stl`, `shell-bottom-print.stl`
- `shell-top-print-screws.stl`, `shell-bottom-print-screws.stl`
- `neg-magsafe-ring.stl`, `neg-led-window.stl`, `neg-button.stl`
- `neg-usbc-bottom.stl`, `neg-mic-array.stl`, `neg-speaker-grill.stl`
- `neg-screw-holes-4x.stl`

## Print Orientation
- Top: upside-down (hero face on bed)
- Bottom: upright (flat back on bed)
""",
        encoding="utf-8",
    )

    print("Validation summary:")
    for n in [
        "shell-top.stl",
        "shell-bottom.stl",
        "shell-top-print.stl",
        "shell-bottom-print.stl",
        "shell-top-print-screws.stl",
        "shell-bottom-print-screws.stl",
    ]:
        validate(n, meshes[n])


if __name__ == "__main__":
    main()
