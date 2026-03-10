#!/usr/bin/env python3
"""
Generate v3 r3.1-r3 MagSafe form-factor printable STL assets.

Design goals:
- Flat MagSafe back with production-leaning exterior polish
- Larger edge rounds and light side contouring for better in-hand ergonomics
- Alignment bossing in the MagSafe pocket for insert repeatability
- Bambu-ready print pair with minimized support requirements
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from meshlib import mrmeshpy as mr


OUT_DIR = Path("prototype/v3/r3-2-mid")

# Envelope
LENGTH = 78.0
WIDTH = 64.0
HEIGHT = 16.0
WALL = 2.4
SPLIT_Z = 9.2

# Body shaping: rounded-rectangle core + large offset, then clipped to flat back
CORE_X = 58.0
CORE_Y = 43.6
CORE_Z = 8.2
BODY_RADIUS = 13.2

# Assembly features
LIP_WIDTH = 1.0
LIP_HEIGHT = 1.0
LIP_CLEARANCE = 0.12

SNAP_WIDTH = 4.8
SNAP_LENGTH_Z = 7.2
SNAP_ENGAGE = 0.80
SNAP_TAB_THICK = 1.42
SNAP_SLOT_DEPTH = 1.72
SNAP_NOTCH_EXTRA = 0.70

# Apple-leaning ergonomic contour set: less boxy, smoother in-hand transitions.
SIDE_SCALLOP_DEPTH = 3.65
SIDE_SCALLOP_RADIUS = 46.0
SHOULDER_SCALLOP_DEPTH = 2.75
SHOULDER_SCALLOP_RADIUS = 50.0
CORNER_BLEND_DEPTH = 3.25
CORNER_BLEND_RADIUS = 38.0
DRAFT_SIDE_DEPTH = 2.45
DRAFT_SIDE_RADIUS = 32.0
DRAFT_SIDE_Z = HEIGHT * 0.52
DRAFT_SHOULDER_DEPTH = 1.75
DRAFT_SHOULDER_RADIUS = 30.0
DRAFT_SHOULDER_Z = HEIGHT * 0.54
GLOBAL_DRAFT_BOTTOM_SCALE = 1.22
GLOBAL_DRAFT_TOP_SCALE = 0.68
GLOBAL_DRAFT_BANDS = 72
GLOBAL_DRAFT_EXP = 0.54

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


def scale_xy(mesh: mr.Mesh, sx: float, sy: float) -> mr.Mesh:
    out = copy_mesh(mesh)
    xf = mr.AffineXf3f()
    xf.A = mr.Matrix3f(vec(sx, 0, 0), vec(0, sy, 0), vec(0, 0, 1))
    xf.b = vec(0, 0, 0)
    out.transform(xf)
    return out


def apply_global_draft(body: mr.Mesh) -> mr.Mesh:
    bands = max(4, int(GLOBAL_DRAFT_BANDS))
    slices: list[mr.Mesh] = []
    for i in range(bands):
        z0 = HEIGHT * i / bands
        z1 = HEIGHT * (i + 1) / bands
        band = boolean(
            body,
            slab(max(-0.5, z0 - 0.25), min(HEIGHT + 0.5, z1 + 0.25)),
            mr.BooleanOperation.Intersection,
            f"draft_band_{i}",
        )
        t = ((z0 + z1) * 0.5) / HEIGHT
        t_curve = pow(max(0.0, min(1.0, t)), GLOBAL_DRAFT_EXP)
        s = GLOBAL_DRAFT_BOTTOM_SCALE + (GLOBAL_DRAFT_TOP_SCALE - GLOBAL_DRAFT_BOTTOM_SCALE) * t_curve
        band = scale_xy(band, s, s)
        slices.append(band)

    drafted = fuse_union(slices, "global_draft")
    # Smooth out any band artifacts from piecewise scaling.
    drafted = offset_mesh(drafted, 0.24, 0.12)
    drafted = offset_mesh(drafted, -0.24, 0.12)
    drafted = offset_mesh(drafted, 0.0, 0.14)
    drafted = boolean(drafted, slab(0.0, HEIGHT), mr.BooleanOperation.Intersection, "global_draft_clip")
    return drafted


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

    body = apply_global_draft(body)
    body = apply_hand_ergonomics(body)
    return apply_button_flat_island(body)


def apply_hand_ergonomics(body: mr.Mesh) -> mr.Mesh:
    cutters: list[mr.Mesh] = []

    # Primary draft sculpt to create a cleaner trapezoidal side profile.
    draft_side_len = WIDTH + 30.0
    draft_side_x = LENGTH / 2 + DRAFT_SIDE_RADIUS - DRAFT_SIDE_DEPTH
    for x in (draft_side_x, -draft_side_x):
        cutters.append(cyl_axis(DRAFT_SIDE_RADIUS, draft_side_len, x, 0.0, DRAFT_SIDE_Z, "y", 112))

    draft_shoulder_len = LENGTH + 30.0
    draft_shoulder_y = WIDTH / 2 + DRAFT_SHOULDER_RADIUS - DRAFT_SHOULDER_DEPTH
    for y in (draft_shoulder_y, -draft_shoulder_y):
        cutters.append(cyl_axis(DRAFT_SHOULDER_RADIUS, draft_shoulder_len, 0.0, y, DRAFT_SHOULDER_Z, "x", 112))

    # Comfort scallops so the profile stays soft in-hand.
    side_len = WIDTH + 24.0
    side_x = LENGTH / 2 + SIDE_SCALLOP_RADIUS - SIDE_SCALLOP_DEPTH
    for x in (side_x, -side_x):
        cutters.append(cyl_axis(SIDE_SCALLOP_RADIUS, side_len, x, 0.0, HEIGHT * 0.58, "y", 96))

    shoulder_len = LENGTH + 24.0
    shoulder_y = WIDTH / 2 + SHOULDER_SCALLOP_RADIUS - SHOULDER_SCALLOP_DEPTH
    for y in (shoulder_y, -shoulder_y):
        cutters.append(cyl_axis(SHOULDER_SCALLOP_RADIUS, shoulder_len, 0.0, y, HEIGHT * 0.60, "x", 96))

    # Top-view corner softening for a less boxy silhouette.
    corner_len = HEIGHT + 10.0
    corner_z = HEIGHT / 2.0
    corner_x = LENGTH / 2 + CORNER_BLEND_RADIUS - CORNER_BLEND_DEPTH
    corner_y = WIDTH / 2 + CORNER_BLEND_RADIUS - CORNER_BLEND_DEPTH
    for sx in (1.0, -1.0):
        for sy in (1.0, -1.0):
            cutters.append(cyl_z(CORNER_BLEND_RADIUS, corner_len, sx * corner_x, sy * corner_y, corner_z, 128))

    return subtract_many(body, cutters, "ergonomic")


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
    # Six-point snap layout for sturdier seam load distribution.
    pts = [
        (30.0, 24.0),
        (30.0, -24.0),
        (-30.0, 24.0),
        (-30.0, -24.0),
        (0.0, 26.0),
        (0.0, -26.0),
    ]
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
            SNAP_TAB_THICK,
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
            SNAP_SLOT_DEPTH,
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
            SNAP_ENGAGE + SNAP_NOTCH_EXTRA,
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


def magsafe_alignment_bosses() -> mr.Mesh:
    ribs: list[mr.Mesh] = []
    for deg in (0.0, 120.0, 240.0):
        a = math.radians(deg)
        nx, ny = math.cos(a), math.sin(a)
        ix, iy = -nx, -ny
        tx, ty = -ny, nx
        ribs.append(
            oriented_box(
                nx * 27.0,
                ny * 27.0,
                0.35,
                2.2,
                2.6,
                0.7,
                tx,
                ty,
                ix,
                iy,
            )
        )

    # A small anti-rotation key near the bottom of the ring pocket.
    ribs.append(box_mesh(BoxSpec(4.6, 1.2, 0.7, 0.0, -25.6, 0.35)))
    return fuse_union(ribs, "mag_bosses")


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
    holes = []
    for y in (-9.0, -3.0, 3.0, 9.0):
        holes.append(cyl_axis(0.55, 10.0, 39.5, y, 12.0, "x", 48))
    return merge(holes)


def _speaker_slot(y: float, z: float) -> mr.Mesh:
    body = box_mesh(BoxSpec(10.0, 2.4, 1.2, 39.5, y, z))
    c1 = cyl_axis(0.6, 10.0, 39.5, y - 1.2, z, "x", 48)
    c2 = cyl_axis(0.6, 10.0, 39.5, y + 1.2, z, "x", 48)
    return fuse_union([body, c1, c2], f"spk_{y}_{z}")


def neg_speaker_grill() -> mr.Mesh:
    parts = []
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
    bottom_print = boolean(bottom_print, magsafe_alignment_bosses(), mr.BooleanOperation.Union, "add_mag_boss")

    top_print_scr = subtract_many(top_print, [neg_scr], "top_print_s")
    bottom_print_scr = subtract_many(bottom_print, [neg_scr], "bottom_print_s")

    # Stabilize and keep slice-friendly sizes.
    meshes = {
        "shell-top.stl": decimate_if_needed(regularize_mesh(top), 110000),
        "shell-bottom.stl": decimate_if_needed(regularize_mesh(bottom), 110000),
        "shell-top-print.stl": decimate_if_needed(regularize_mesh(top_print), 110000),
        "shell-bottom-print.stl": decimate_if_needed(regularize_mesh(bottom_print), 110000),
        "shell-top-print-screws.stl": decimate_if_needed(regularize_mesh(top_print_scr), 110000),
        "shell-bottom-print-screws.stl": decimate_if_needed(regularize_mesh(bottom_print_scr), 110000),
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
        """# v3 R3.2 Mid (MagSafe)

Generated print assets for the v3.2 holistic redesign: smooth bottom-led taper, deeper edge recess, and stronger corner softness.

## What Changed vs R3
- Maintains R3 exterior polish, ergonomics, and MagSafe alignment bossing
- Mid seam tuning between r3-loose and r3-tight for balanced retention
- Moderate insertion force for daily open/close testing

## Files
- `shell-top.stl`, `shell-bottom.stl`
- `shell-top-print.stl`, `shell-bottom-print.stl`
- `shell-top-print-screws.stl`, `shell-bottom-print-screws.stl`
- `neg-magsafe-ring.stl`, `neg-led-window.stl`, `neg-button.stl`
- `neg-usbc-bottom.stl`, `neg-mic-array.stl`, `neg-speaker-grill.stl`
- `neg-screw-holes-4x.stl`

## Print Orientation
- Top: seam-down (open cavity up, split plane on bed)
- Bottom: upright (flat back on bed)

## Bambu Slicer Baseline
- Layer height: `0.16` or `0.20`
- Walls: `4`
- Top/Bottom layers: `6`
- Supports: `off` (enable only if your machine/profile bridges poorly near side I/O)
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
