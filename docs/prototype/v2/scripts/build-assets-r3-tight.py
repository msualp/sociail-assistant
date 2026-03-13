#!/usr/bin/env python3
"""
Generate third-pass polished v2.0 printable STL assets from the v2.0 design spec.

This pass adds:
- larger continuous edge rounds for a sleeker hero surface
- subtle side/shoulder ergonomic contouring for improved hand feel
- tuned tongue-and-groove and snap-tab features for repeatable assembly
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from meshlib import mrmeshpy as mr


OUT_DIR = Path("prototype/v2/r3-tight")

# v2.0 locked parameters (mm)
LENGTH = 85.0
WIDTH = 35.0
HEIGHT = 14.0
WALL = 2.6
SPLIT_Z = 8.4

FILLET = 5.2
CORE_LENGTH = LENGTH - 2 * 17.5  # 50
CORE_WIDTH = WIDTH - 2 * FILLET  # 24.6
CORE_HEIGHT = HEIGHT - 2 * FILLET  # 3.6
CORE_END_R = 17.5 - FILLET  # 12.3

# Tongue-and-groove targets
LIP_WIDTH = 1.0
LIP_HEIGHT = 1.0
LIP_CLEARANCE = 0.08

# Snap tabs (first mechanical pass)
SNAP_WIDTH = 4.0
SNAP_LENGTH_Z = 8.0
SNAP_DEFLECTION = 0.8
SNAP_ENGAGE = 0.98
SNAP_TAB_THICK = 1.50
SNAP_SLOT_DEPTH = 1.55
SNAP_NOTCH_EXTRA = 0.52

# 24mm button module defaults (22mm remains alternate).
BUTTON_CENTER_X = 0.0
BUTTON_CENTER_Y = 0.0
BUTTON_PLUNGER_OD = 24.0
BUTTON_CUTOUT_OD = BUTTON_PLUNGER_OD + 0.6
BUTTON_BEZEL_OD = BUTTON_PLUNGER_OD + 4.0
BUTTON_ISLAND_OD = BUTTON_BEZEL_OD + 2.0
BUTTON_ISLAND_RECESS = 0.6

# LED moved forward and narrowed to clear 24mm center button.
LED_LENGTH = 40.0
LED_WIDTH = 3.2
LED_END_R = 1.6
LED_Y = 14.5

FLOOR_Z = WALL

# Internal XIAO board cradle (21 x 17.5 mm class).
BOARD_X = 21.0
BOARD_Y = 17.5
BOARD_CLEAR = 0.30
BOARD_BASE_H = 0.9
BOARD_RAIL_T = 1.05
BOARD_RAIL_H = 3.0
BOARD_REAR_STOP_T = 1.0
BOARD_NUB_X = 0.25
BOARD_NUB_Y = 4.8
BOARD_NUB_Z = 1.0
BOARD_CX = -30.5
BOARD_CY = 0.0

# Switch mount (6x6mm tact)
SWITCH_FOOTPRINT = 6.0
SWITCH_CLEAR = 0.2
SWITCH_TOTAL_H = 3.5
SWITCH_TOP_CLEAR = 0.4
SWITCH_BASE_H = 1.0
SWITCH_WALL_H = 1.6
SWITCH_CX = BUTTON_CENTER_X
SWITCH_CY = BUTTON_CENTER_Y

SWITCH_LIP_T = 0.6
SWITCH_LIP_Z = 0.6
SWITCH_BACK_STOP_T = 0.8

# LED strip channel (WS2812B class)
LED_STRIP_LEN = 42.0
LED_STRIP_W = 6.0
LED_STRIP_DEPTH = 1.6
LED_STRIP_Z = HEIGHT - 2.4
LED_STRIP_Y = LED_Y

LED_END_STOP_W = 2.4
LED_END_STOP_H = 1.2

SPK_OD = 23.0
SPK_CLEAR = 0.25
SPK_SEAT_H = 1.0
SPK_TAB_W = 3.0
SPK_TAB_T = 1.0
SPK_TAB_H = 1.2
SPK_CX = 18.0
SPK_CY = 0.0

MIC_GUIDE_T = 0.8
MIC_GUIDE_H = 1.2
MIC_GUIDE_Z = 10.0

USB_COLLAR_X = 16.0
USB_COLLAR_Y = 14.0
USB_COLLAR_Z = 4.6

# Subtle body contouring for better hand comfort while preserving the v2 envelope.
SIDE_SCALLOP_DEPTH = 0.70
SIDE_SCALLOP_RADIUS = 56.0
SHOULDER_SCALLOP_DEPTH = 0.50
SHOULDER_SCALLOP_RADIUS = 62.0
CORNER_BLEND_DEPTH = 0.40
CORNER_BLEND_RADIUS = 78.0


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
    # local axes: X=tangent, Y=inward, Z=global Z
    m = box_mesh(BoxSpec(size_t, size_i, size_z, 0, 0, 0))
    A = mr.Matrix3f(vec(tx, ix, 0), vec(ty, iy, 0), vec(0, 0, 1))
    xf = mr.AffineXf3f()
    xf.A = A
    xf.b = vec(cx, cy, cz)
    m.transform(xf)
    return m


def merge_components(parts: list[mr.Mesh]) -> mr.Mesh:
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
        out = boolean(out, c, mr.BooleanOperation.DifferenceAB, f"{label}#{i}")
    return out


def offset_mesh(mesh: mr.Mesh, delta: float, voxel: float = 0.2) -> mr.Mesh:
    params = mr.OffsetParameters()
    params.voxelSize = voxel
    return mr.offsetMesh(mr.MeshPart(mesh), delta, params)


def build_outer_body() -> mr.Mesh:
    rect = box_mesh(BoxSpec(CORE_LENGTH, CORE_WIDTH, CORE_HEIGHT, 0, 0, CORE_HEIGHT / 2))
    left = cyl_z(CORE_END_R, CORE_HEIGHT, -CORE_LENGTH / 2, 0, CORE_HEIGHT / 2)
    right = cyl_z(CORE_END_R, CORE_HEIGHT, CORE_LENGTH / 2, 0, CORE_HEIGHT / 2)

    core = boolean(rect, left, mr.BooleanOperation.Union, "core_union_left")
    core = boolean(core, right, mr.BooleanOperation.Union, "core_union_right")

    params = mr.OffsetParameters()
    params.voxelSize = 0.25
    outer = mr.offsetMesh(mr.MeshPart(core), FILLET, params)

    # Normalize to spec frame: centered in XY, bottom at Z=0.
    bbox = outer.getBoundingBox()
    cx = (bbox.min.x + bbox.max.x) / 2
    cy = (bbox.min.y + bbox.max.y) / 2
    dz = -bbox.min.z
    outer.transform(mr.AffineXf3f.translation(vec(-cx, -cy, dz)))
    outer = apply_hand_ergonomics(outer)
    outer = apply_button_flat_island(outer)
    return normalize_outer_envelope(outer)


def apply_hand_ergonomics(body: mr.Mesh) -> mr.Mesh:
    cutters: list[mr.Mesh] = []

    # Light long-side thumb scallops for a more comfortable in-hand grip.
    side_len = WIDTH + 20.0
    side_x = LENGTH / 2 + SIDE_SCALLOP_RADIUS - SIDE_SCALLOP_DEPTH
    for x in (side_x, -side_x):
        cutters.append(cyl_axis(SIDE_SCALLOP_RADIUS, side_len, x, 0.0, HEIGHT * 0.56, "y", 96))

    # Soft shoulder blend at +/-Y to reduce hard edge feel near the top crown.
    shoulder_len = LENGTH + 18.0
    shoulder_y = WIDTH / 2 + SHOULDER_SCALLOP_RADIUS - SHOULDER_SCALLOP_DEPTH
    for y in (shoulder_y, -shoulder_y):
        cutters.append(cyl_axis(SHOULDER_SCALLOP_RADIUS, shoulder_len, 0.0, y, HEIGHT * 0.58, "x", 96))

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


def normalize_outer_envelope(body: mr.Mesh) -> mr.Mesh:
    bbox = body.getBoundingBox()
    size_x = bbox.max.x - bbox.min.x
    size_y = bbox.max.y - bbox.min.y

    sx = LENGTH / size_x if size_x > 0 else 1.0
    sy = WIDTH / size_y if size_y > 0 else 1.0

    out = copy_mesh(body)
    xf = mr.AffineXf3f()
    xf.A = mr.Matrix3f(vec(sx, 0, 0), vec(0, sy, 0), vec(0, 0, 1))
    xf.b = vec(0, 0, 0)
    out.transform(xf)

    b2 = out.getBoundingBox()
    cx = (b2.min.x + b2.max.x) / 2
    cy = (b2.min.y + b2.max.y) / 2
    dz = -b2.min.z
    out.transform(mr.AffineXf3f.translation(vec(-cx, -cy, dz)))
    return out


def build_inner_body(outer: mr.Mesh) -> mr.Mesh:
    return offset_mesh(outer, -WALL, 0.2)


def slab(z_min: float, z_max: float) -> mr.Mesh:
    return box_mesh(BoxSpec(260, 260, z_max - z_min, 0, 0, (z_min + z_max) / 2))


def split_shells(outer: mr.Mesh, inner: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    eps = 0.01

    bottom_outer = boolean(outer, slab(-40, SPLIT_Z + eps), mr.BooleanOperation.Intersection, "bottom_outer_clip")
    bottom_inner = boolean(inner, slab(-40, SPLIT_Z + eps), mr.BooleanOperation.Intersection, "bottom_inner_clip")
    bottom_shell = _voxel_subtract(bottom_outer, bottom_inner, voxel_size=0.12, max_error=0.04)

    top_outer = boolean(outer, slab(SPLIT_Z - eps, 60), mr.BooleanOperation.Intersection, "top_outer_clip")
    top_inner = boolean(inner, slab(SPLIT_Z - eps, 60), mr.BooleanOperation.Intersection, "top_inner_clip")
    top_shell = _voxel_subtract(top_outer, top_inner, voxel_size=0.12, max_error=0.04)

    return top_shell, bottom_shell


def add_tongue_and_groove(top: mr.Mesh, bottom: mr.Mesh, inner: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    # Build seam rings from the inner shell outward so exterior cosmetics remain untouched.
    lip_outer = offset_mesh(inner, LIP_WIDTH, 0.18)
    groove_outer = offset_mesh(inner, LIP_WIDTH + LIP_CLEARANCE, 0.18)

    lip_ring = boolean(lip_outer, inner, mr.BooleanOperation.DifferenceAB, "lip_ring")
    groove_ring = boolean(groove_outer, inner, mr.BooleanOperation.DifferenceAB, "groove_ring")

    lip_clip = boolean(
        lip_ring,
        slab(SPLIT_Z - 0.02, SPLIT_Z + LIP_HEIGHT),
        mr.BooleanOperation.Intersection,
        "lip_clip",
    )
    groove_clip = boolean(
        groove_ring,
        slab(SPLIT_Z - 0.2, SPLIT_Z + LIP_HEIGHT + 0.3),
        mr.BooleanOperation.Intersection,
        "groove_clip",
    )

    bottom2 = boolean(bottom, lip_clip, mr.BooleanOperation.Union, "bottom_add_lip")
    top2 = boolean(top, groove_clip, mr.BooleanOperation.DifferenceAB, "top_sub_groove")
    return top2, bottom2


def snap_locations() -> list[tuple[float, float, float, float, float, float]]:
    # 4 positions around the two end arcs at +/-30deg (from +/-X end centers).
    locs: list[tuple[float, float, float, float, float, float]] = []
    end_cx = LENGTH / 2 - WIDTH / 2  # 25mm
    inner_r = WIDTH / 2 - WALL + 0.1

    for sx in (-1.0, 1.0):
        cx = sx * end_cx
        base = 0.0 if sx > 0 else 180.0
        for a in (-30.0, 30.0):
            th = math.radians(base + a)
            nx = math.cos(th)
            ny = math.sin(th)
            ix = -nx
            iy = -ny
            tx = -ny
            ty = nx
            px = cx + nx * inner_r
            py = ny * inner_r
            locs.append((px, py, tx, ty, ix, iy))
    return locs


def add_snap_tabs(top: mr.Mesh, bottom: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    tab_parts: list[mr.Mesh] = []
    slot_parts: list[mr.Mesh] = []
    notch_parts: list[mr.Mesh] = []

    tab_z0 = SPLIT_Z - SNAP_LENGTH_Z
    tab_z1 = SPLIT_Z
    tab_cz = (tab_z0 + tab_z1) / 2

    for idx, (px, py, tx, ty, ix, iy) in enumerate(snap_locations(), start=1):
        # Main vertical tab.
        tab = oriented_box(
            px + ix * 0.7,
            py + iy * 0.7,
            tab_cz,
            SNAP_WIDTH,
            SNAP_TAB_THICK,
            SNAP_LENGTH_Z,
            tx,
            ty,
            ix,
            iy,
        )

        # Engagement bump near the top of each tab.
        hook = oriented_box(
            px + ix * 1.8,
            py + iy * 1.8,
            SPLIT_Z - 0.5,
            SNAP_WIDTH,
            SNAP_ENGAGE,
            1.0,
            tx,
            ty,
            ix,
            iy,
        )
        tab_full = boolean(tab, hook, mr.BooleanOperation.Union, f"snap_tab_{idx}")
        tab_parts.append(tab_full)

        # Relief slot to allow elastic deflection (keeps ~0.8mm wall at base side).
        slot = oriented_box(
            px + ix * 1.7,
            py + iy * 1.7,
            SPLIT_Z - 4.0,
            SNAP_WIDTH + 1.0,
            SNAP_SLOT_DEPTH,
            6.0,
            tx,
            ty,
            ix,
            iy,
        )
        slot_parts.append(slot)

        # Matching notch in top shell for latch engagement.
        notch = oriented_box(
            px + ix * 1.8,
            py + iy * 1.8,
            SPLIT_Z + 0.9,
            SNAP_WIDTH + 0.8,
            SNAP_ENGAGE + SNAP_NOTCH_EXTRA,
            1.8,
            tx,
            ty,
            ix,
            iy,
        )
        notch_parts.append(notch)

    tabs = fuse_union(tab_parts, "snap_tabs")
    slots = fuse_union(slot_parts, "snap_slots")
    notches = fuse_union(notch_parts, "snap_notches")

    bottom2 = boolean(bottom, tabs, mr.BooleanOperation.Union, "bottom_add_tabs")
    bottom3 = boolean(bottom2, slots, mr.BooleanOperation.DifferenceAB, "bottom_sub_slots")
    top2 = boolean(top, notches, mr.BooleanOperation.DifferenceAB, "top_sub_notches")
    return top2, bottom3


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


def neg_usb_c_left_recess() -> mr.Mesh:
    # Guided USB-C tunnel: outer opening + internal alignment tunnel.
    opening = box_mesh(BoxSpec(6.0, 9.5, 3.5, -LENGTH / 2.0 + 2.0, 0.0, 5.0))
    tunnel = box_mesh(BoxSpec(12.2, 12.0, 4.4, -LENGTH / 2.0 + 6.5, 0.0, 5.0))
    return fuse_union([opening, tunnel], "neg_usb_tunnel")


def neg_led_window_rounded() -> mr.Mesh:
    depth = 3.0
    zc = HEIGHT - depth / 2
    yc = LED_Y

    center_len = LED_LENGTH - 2.0 * LED_END_R
    center = box_mesh(BoxSpec(center_len, LED_WIDTH, depth, 0.0, yc, zc))
    left = cyl_z(LED_END_R, depth, -center_len / 2.0, yc, zc, 96)
    right = cyl_z(LED_END_R, depth, center_len / 2.0, yc, zc, 96)
    return fuse_union([center, left, right], "neg_led")


def neg_button_well() -> mr.Mesh:
    cutout = cyl_z(BUTTON_CUTOUT_OD / 2.0, 10.0, BUTTON_CENTER_X, BUTTON_CENTER_Y, HEIGHT - 5.0, 128)
    return cutout


def led_end_stops() -> mr.Mesh:
    zc = LED_STRIP_Z
    left_x = -LED_STRIP_LEN / 2.0 + LED_END_STOP_W / 2.0
    right_x = LED_STRIP_LEN / 2.0 - LED_END_STOP_W / 2.0
    stops = [
        box_mesh(BoxSpec(LED_END_STOP_W, LED_STRIP_W, LED_END_STOP_H, left_x, LED_STRIP_Y, zc)),
        box_mesh(BoxSpec(LED_END_STOP_W, LED_STRIP_W, LED_END_STOP_H, right_x, LED_STRIP_Y, zc)),
    ]
    return fuse_union(stops, "led_stops")


def neg_led_channel() -> mr.Mesh:
    channel = box_mesh(BoxSpec(LED_STRIP_LEN, LED_STRIP_W, LED_STRIP_DEPTH, 0.0, LED_STRIP_Y, LED_STRIP_Z))
    return boolean(channel, led_end_stops(), mr.BooleanOperation.DifferenceAB, "led_channel")


def pry_notch() -> mr.Mesh:
    # Small external notch for pry-tool access at the seam.
    return box_mesh(BoxSpec(3.8, 2.0, 1.6, LENGTH / 2.0 - 2.0, 0.0, SPLIT_Z + 0.4))


def neg_mic_perforations() -> mr.Mesh:
    holes: list[mr.Mesh] = []
    for x in (-8.0, -4.0, 0.0, 4.0, 8.0):
        holes.append(cyl_axis(0.6, 6.0, x, 17.5, 10.0, "y", 48))
    return merge_components(holes)


def _speaker_slot(cx: float, cz: float) -> mr.Mesh:
    center = box_mesh(BoxSpec(2.0, 6.0, 2.0, cx, 17.5, cz))
    lcap = cyl_axis(1.0, 6.0, cx - 1.0, 17.5, cz, "y", 48)
    rcap = cyl_axis(1.0, 6.0, cx + 1.0, 17.5, cz, "y", 48)
    return fuse_union([center, lcap, rcap], f"speaker_slot_{cx}_{cz}")


def neg_speaker_grill() -> mr.Mesh:
    parts: list[mr.Mesh] = []
    xs = (-6.0, -3.0, 0.0, 3.0, 6.0)
    zs = (1.5, 4.0, 6.5)
    for z in zs:
        for x in xs:
            parts.append(_speaker_slot(x, z))
    return fuse_union(parts, "neg_speaker")


def neg_screw_bosses_4x() -> mr.Mesh:
    pts = [(-28.0, -11.0), (-28.0, 11.0), (28.0, -11.0), (28.0, 11.0)]
    holes = [cyl_z(1.5, 20.0, x, y, 7.0, 48) for (x, y) in pts]
    return merge_components(holes)

def board_guides() -> mr.Mesh:
    slot_x = BOARD_X + 2.0 * BOARD_CLEAR
    slot_y = BOARD_Y + 2.0 * BOARD_CLEAR
    base = box_mesh(
        BoxSpec(
            slot_x + 2.0 * BOARD_RAIL_T + 2.0,
            slot_y + 1.8,
            BOARD_BASE_H,
            BOARD_CX,
            BOARD_CY,
            FLOOR_Z + BOARD_BASE_H / 2.0,
        )
    )
    rail_cz = FLOOR_Z + BOARD_RAIL_H / 2.0
    rail_len = slot_y + 1.0
    lx = BOARD_CX - slot_x / 2.0 - BOARD_RAIL_T / 2.0
    rx = BOARD_CX + slot_x / 2.0 + BOARD_RAIL_T / 2.0
    rails = [
        box_mesh(BoxSpec(BOARD_RAIL_T, rail_len, BOARD_RAIL_H, lx, BOARD_CY, rail_cz)),
        box_mesh(BoxSpec(BOARD_RAIL_T, rail_len, BOARD_RAIL_H, rx, BOARD_CY, rail_cz)),
    ]
    stop_cy = BOARD_CY + slot_y / 2.0 + BOARD_REAR_STOP_T / 2.0
    rear_stop = box_mesh(
        BoxSpec(
            slot_x + 2.0 * BOARD_RAIL_T,
            BOARD_REAR_STOP_T,
            BOARD_RAIL_H - 0.2,
            BOARD_CX,
            stop_cy,
            FLOOR_Z + (BOARD_RAIL_H - 0.2) / 2.0,
        )
    )
    nub_cz = FLOOR_Z + BOARD_RAIL_H - BOARD_NUB_Z / 2.0
    nubs = [
        box_mesh(
            BoxSpec(
                BOARD_NUB_X,
                BOARD_NUB_Y,
                BOARD_NUB_Z,
                BOARD_CX - slot_x / 2.0 + BOARD_NUB_X / 2.0,
                BOARD_CY,
                nub_cz,
            )
        ),
        box_mesh(
            BoxSpec(
                BOARD_NUB_X,
                BOARD_NUB_Y,
                BOARD_NUB_Z,
                BOARD_CX + slot_x / 2.0 - BOARD_NUB_X / 2.0,
                BOARD_CY,
                nub_cz,
            )
        ),
    ]
    lead_x = BOARD_CX - slot_x / 2.0 - 0.5
    leads = [
        box_mesh(BoxSpec(2.0, 2.8, 1.6, lead_x, BOARD_CY - slot_y / 2.0 - 0.4, FLOOR_Z + 0.8)),
        box_mesh(BoxSpec(2.0, 2.8, 1.6, lead_x, BOARD_CY + slot_y / 2.0 + 0.4, FLOOR_Z + 0.8)),
    ]
    return fuse_union([base, rear_stop] + rails + nubs + leads, "board_guides")


def switch_mount() -> mr.Mesh:
    slot = SWITCH_FOOTPRINT + 2.0 * SWITCH_CLEAR
    base_top = SPLIT_Z - SWITCH_TOP_CLEAR - SWITCH_TOTAL_H
    base_cz = base_top - SWITCH_BASE_H / 2.0
    base = box_mesh(BoxSpec(slot + 1.6, slot + 1.6, SWITCH_BASE_H, SWITCH_CX, SWITCH_CY, base_cz))
    wall_cz = base_top + SWITCH_WALL_H / 2.0
    wall_t = 0.8
    lx = SWITCH_CX - slot / 2.0 - wall_t / 2.0
    rx = SWITCH_CX + slot / 2.0 + wall_t / 2.0
    walls = [
        box_mesh(BoxSpec(wall_t, slot + 0.8, SWITCH_WALL_H, lx, SWITCH_CY, wall_cz)),
        box_mesh(BoxSpec(wall_t, slot + 0.8, SWITCH_WALL_H, rx, SWITCH_CY, wall_cz)),
    ]

    lip_z = base_top + SWITCH_WALL_H - SWITCH_LIP_Z / 2.0
    lip_y = SWITCH_CY
    lip_len = slot - 0.6
    left_lip = box_mesh(
        BoxSpec(
            SWITCH_LIP_T,
            lip_len,
            SWITCH_LIP_Z,
            SWITCH_CX - slot / 2.0 + SWITCH_LIP_T / 2.0 - 0.1,
            lip_y,
            lip_z,
        )
    )
    right_lip = box_mesh(
        BoxSpec(
            SWITCH_LIP_T,
            lip_len,
            SWITCH_LIP_Z,
            SWITCH_CX + slot / 2.0 - SWITCH_LIP_T / 2.0 + 0.1,
            lip_y,
            lip_z,
        )
    )

    back_stop = box_mesh(
        BoxSpec(
            slot + 1.2,
            SWITCH_BACK_STOP_T,
            SWITCH_WALL_H,
            SWITCH_CX,
            SWITCH_CY + slot / 2.0 + SWITCH_BACK_STOP_T / 2.0,
            wall_cz,
        )
    )

    return fuse_union([base, back_stop] + walls + [left_lip, right_lip], "switch_mount")


def speaker_seat() -> mr.Mesh:
    seat_r = SPK_OD / 2.0 + SPK_CLEAR
    seat = cyl_z(seat_r, SPK_SEAT_H, SPK_CX, SPK_CY, FLOOR_Z + SPK_SEAT_H / 2.0, 96)

    tab_z = FLOOR_Z + SPK_SEAT_H + SPK_TAB_H / 2.0
    tab_r = SPK_OD / 2.0 - SPK_TAB_T / 2.0
    tabs = [
        box_mesh(BoxSpec(SPK_TAB_W, SPK_TAB_T, SPK_TAB_H, SPK_CX + tab_r, SPK_CY, tab_z)),
        box_mesh(BoxSpec(SPK_TAB_W, SPK_TAB_T, SPK_TAB_H, SPK_CX - tab_r, SPK_CY, tab_z)),
        box_mesh(BoxSpec(SPK_TAB_T, SPK_TAB_W, SPK_TAB_H, SPK_CX, SPK_CY + tab_r, tab_z)),
    ]
    return fuse_union([seat] + tabs, "speaker_seat")


def mic_guides() -> mr.Mesh:
    y = WIDTH / 2.0 - WALL - MIC_GUIDE_T / 2.0
    guides = []
    for x in (-8.0, -4.0, 0.0, 4.0, 8.0):
        guides.append(cyl_axis(1.1, MIC_GUIDE_T, x, y, MIC_GUIDE_Z, "y", 48))
    return fuse_union(guides, "mic_guides")


def usb_collar() -> mr.Mesh:
    cx = -LENGTH / 2.0 + 6.5
    cy = 0.0
    cz = 5.0
    return box_mesh(BoxSpec(USB_COLLAR_X, USB_COLLAR_Y, USB_COLLAR_Z, cx, cy, cz))

def internal_wire_channels() -> mr.Mesh:
    return fuse_union(
        [
            box_mesh(BoxSpec(2.6, 22.0, 0.9, -8.0, 0.0, FLOOR_Z + 0.45)),
            box_mesh(BoxSpec(2.6, 20.0, 0.9, 8.0, 0.0, FLOOR_Z + 0.45)),
            box_mesh(BoxSpec(4.0, 8.0, 0.9, -20.0, 0.0, FLOOR_Z + 0.45)),
        ],
        "wire_channels",
    )


def add_internal_fit_pack(bottom: mr.Mesh) -> mr.Mesh:
    mounts = fuse_union([board_guides(), switch_mount(), speaker_seat(), usb_collar()], "internal_pack")
    return boolean(bottom, mounts, mr.BooleanOperation.Union, "add_internal_pack")




def regularize_mesh(mesh: mr.Mesh, voxel: float = 0.12) -> mr.Mesh:
    # Zero-offset voxel remesh cleans tiny non-manifold artifacts after stacked booleans.
    return offset_mesh(mesh, 0.0, voxel)

def decimate_if_needed(mesh: mr.Mesh, max_faces: int, max_error: float = 0.03) -> mr.Mesh:
    faces = mesh.topology.numValidFaces()
    if faces <= max_faces:
        return mesh

    out = copy_mesh(mesh)
    settings = mr.DecimateSettings()
    settings.maxError = max_error
    settings.maxDeletedFaces = max(0, faces - max_faces)
    mr.decimateMesh(out, settings)
    return out


def validate_and_report(label: str, mesh: mr.Mesh) -> None:
    bbox = mesh.getBoundingBox()
    print(
        f"{label}: faces={mesh.topology.numValidFaces()} "
        f"closed={mesh.topology.isClosed()} valid={mesh.topology.checkValidity()} "
        f"bbox=({bbox.min.x:.2f},{bbox.min.y:.2f},{bbox.min.z:.2f})-({bbox.max.x:.2f},{bbox.max.y:.2f},{bbox.max.z:.2f})"
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    outer = build_outer_body()
    inner = build_inner_body(outer)
    top, bottom = split_shells(outer, inner)
    top, bottom = add_tongue_and_groove(top, bottom, inner)
    top, bottom = add_snap_tabs(top, bottom)
    top = boolean(top, mic_guides(), mr.BooleanOperation.Union, "mic_guides")
    top = boolean(top, pry_notch(), mr.BooleanOperation.DifferenceAB, "pry_notch")
    bottom = reopen_bottom_cavity(bottom, inner)

    neg_usb = neg_usb_c_left_recess()
    neg_led = neg_led_window_rounded()
    neg_btn = neg_button_well()
    neg_mic = neg_mic_perforations()
    neg_spk = neg_speaker_grill()
    neg_scr = neg_screw_bosses_4x()

    top_print = subtract_many(top, [neg_led, neg_btn, neg_led_channel()], "top_print")
    bottom_print = subtract_many(bottom, [neg_usb, neg_mic, neg_spk], "bottom_print")
    bottom_print = add_internal_fit_pack(bottom_print)
    bottom_print = boolean(bottom_print, internal_wire_channels(), mr.BooleanOperation.DifferenceAB, "sub_wire_channels")

    top_print_scr = subtract_many(top_print, [neg_scr], "top_print_screws")
    bottom_print_scr = subtract_many(bottom_print, [neg_scr], "bottom_print_screws")

    # Normalize final shells through zero-offset remeshing for manifold reliability.
    top = regularize_mesh(top, 0.12)
    bottom = regularize_mesh(bottom, 0.12)
    top_print = regularize_mesh(top_print, 0.12)
    bottom_print = regularize_mesh(bottom_print, 0.12)
    top_print_scr = regularize_mesh(top_print_scr, 0.12)
    bottom_print_scr = regularize_mesh(bottom_print_scr, 0.12)

    # Keep STL sizes practical for slicer import while preserving shape.
    top = decimate_if_needed(top, 80000, 0.04)
    bottom = decimate_if_needed(bottom, 70000, 0.04)
    top_print = decimate_if_needed(top_print, 80000, 0.04)
    bottom_print = decimate_if_needed(bottom_print, 70000, 0.04)
    top_print_scr = decimate_if_needed(top_print_scr, 80000, 0.04)
    bottom_print_scr = decimate_if_needed(bottom_print_scr, 70000, 0.04)

    # Canonical main shells and negatives.
    save_mesh(top, OUT_DIR / "shell-top.stl")
    save_mesh(bottom, OUT_DIR / "shell-bottom.stl")

    save_mesh(neg_usb, OUT_DIR / "neg-usbc-left-tunnel.stl")
    save_mesh(neg_led, OUT_DIR / "neg-led-window.stl")
    save_mesh(neg_btn, OUT_DIR / "neg-button-well.stl")
    save_mesh(neg_mic, OUT_DIR / "neg-mic-array.stl")
    save_mesh(neg_spk, OUT_DIR / "neg-speaker-grill.stl")
    save_mesh(neg_scr, OUT_DIR / "neg-screw-holes-4x.stl")

    # Direct printable variants.
    save_mesh(top_print, OUT_DIR / "shell-top-print.stl")
    save_mesh(bottom_print, OUT_DIR / "shell-bottom-print.stl")
    save_mesh(top_print_scr, OUT_DIR / "shell-top-print-screws.stl")
    save_mesh(bottom_print_scr, OUT_DIR / "shell-bottom-print-screws.stl")

    with open(OUT_DIR / "README.txt", "w", encoding="utf-8") as f:
        f.write(
            "Sociail Assistant v2.0 (W35) - GENERATED R3-TIGHT POLISHED PRINT ASSETS\n"
            "Generated: 2026-03-05\n\n"
            "This folder contains parametric STL meshes generated from\n"
            "../docs/design-spec.md dimensions for Bambu Studio use.\n\n"
            "Implemented in this pass:\n"
            "- 5.2mm continuous body rounds with subtle side/shoulder contouring\n"
            "- 1.0mm tongue-and-groove seam (0.08mm clearance target, tighter fit)\n"
            "- 4x snap tabs near end arcs (+/-30deg locations), tuned for lower insertion force and easier hand assembly\n"
            "- Internal-fit pack: board rails, snap-switch cradle, speaker seat, mic guides, USB collar, LED end stops\n\n"
            "Canonical parts:\n"
            "- shell-top.stl\n"
            "- shell-bottom.stl\n\n"
            "Negative cutouts:\n"
            "- neg-usbc-left-tunnel.stl\n"
            "- neg-led-window.stl\n"
            "- neg-button-well.stl\n"
            "- neg-mic-array.stl\n"
            "- neg-speaker-grill.stl\n"
            "- neg-screw-holes-4x.stl (optional)\n\n"
            "Direct print-ready variants:\n"
            "- shell-top-print.stl\n"
            "- shell-bottom-print.stl\n"
            "- shell-top-print-screws.stl\n"
            "- shell-bottom-print-screws.stl\n\n"
            "Bambu orientation:\n"
            "- Top shell: upside-down (hero side on bed)\n"
            "- Bottom shell: upright (cavity up)\n"
        )

    print("\nValidation summary:")
    validate_and_report("top_raw", top)
    validate_and_report("bottom_raw", bottom)
    validate_and_report("top_print", top_print)
    validate_and_report("bottom_print", bottom_print)
    validate_and_report("top_print_screws", top_print_scr)
    validate_and_report("bottom_print_screws", bottom_print_scr)


if __name__ == "__main__":
    main()
