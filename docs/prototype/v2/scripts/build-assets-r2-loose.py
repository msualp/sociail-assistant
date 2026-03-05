#!/usr/bin/env python3
"""
Generate second-pass v2.0 printable STL assets from the v2.0 design spec.

This pass adds:
- explicit tongue-and-groove seam features
- explicit 4x snap-tab features with matching top-shell latch pockets
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from meshlib import mrmeshpy as mr


OUT_DIR = Path("prototype/v2/r2-loose")

# v2.0 locked parameters (mm)
LENGTH = 85.0
WIDTH = 35.0
HEIGHT = 14.0
WALL = 2.6
SPLIT_Z = 8.4

FILLET = 4.0
CORE_LENGTH = LENGTH - 2 * 17.5  # 50
CORE_WIDTH = WIDTH - 2 * FILLET  # 27
CORE_HEIGHT = HEIGHT - 2 * FILLET  # 6
CORE_END_R = 17.5 - FILLET  # 13.5

# Tongue-and-groove targets
LIP_WIDTH = 1.0
LIP_HEIGHT = 1.0
LIP_CLEARANCE = 0.18

# Snap tabs (first mechanical pass)
SNAP_WIDTH = 4.0
SNAP_LENGTH_Z = 8.0
SNAP_DEFLECTION = 0.8
SNAP_ENGAGE = 0.55

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
    return apply_button_flat_island(outer)


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


def build_inner_body(outer: mr.Mesh) -> mr.Mesh:
    return offset_mesh(outer, -WALL, 0.2)


def slab(z_min: float, z_max: float) -> mr.Mesh:
    return box_mesh(BoxSpec(260, 260, z_max - z_min, 0, 0, (z_min + z_max) / 2))


def split_shells(outer: mr.Mesh, inner: mr.Mesh) -> tuple[mr.Mesh, mr.Mesh]:
    eps = 0.01

    bottom_outer = boolean(outer, slab(-40, SPLIT_Z + eps), mr.BooleanOperation.Intersection, "bottom_outer_clip")
    bottom_inner = boolean(inner, slab(-40, SPLIT_Z + eps), mr.BooleanOperation.Intersection, "bottom_inner_clip")
    bottom_shell = boolean(bottom_outer, bottom_inner, mr.BooleanOperation.DifferenceAB, "bottom_shell")

    top_outer = boolean(outer, slab(SPLIT_Z - eps, 60), mr.BooleanOperation.Intersection, "top_outer_clip")
    top_inner = boolean(inner, slab(SPLIT_Z - eps, 60), mr.BooleanOperation.Intersection, "top_inner_clip")
    top_shell = boolean(top_outer, top_inner, mr.BooleanOperation.DifferenceAB, "top_shell")

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
            1.25,
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
            2.2,
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
            SNAP_ENGAGE + 1.0,
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


def neg_usb_c_left_recess() -> mr.Mesh:
    pocket = box_mesh(BoxSpec(3.0, 14.0, 8.0, -42.5 + 1.5, 0.0, 5.0))
    opening = box_mesh(BoxSpec(6.0, 9.5, 3.5, -42.5 + 3.0, 0.0, 5.0))
    return fuse_union([pocket, opening], "neg_usb")


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

    neg_usb = neg_usb_c_left_recess()
    neg_led = neg_led_window_rounded()
    neg_btn = neg_button_well()
    neg_mic = neg_mic_perforations()
    neg_spk = neg_speaker_grill()
    neg_scr = neg_screw_bosses_4x()

    top_print = subtract_many(top, [neg_led, neg_btn], "top_print")
    bottom_print = subtract_many(bottom, [neg_usb, neg_mic, neg_spk], "bottom_print")

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

    save_mesh(neg_usb, OUT_DIR / "neg-usbc-left-recess.stl")
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
            "Sociail Assistant v2.0 (W35) - GENERATED R2 SNAP-TUNED PRINT ASSETS\n"
            "Generated: 2026-03-04\n\n"
            "This folder contains parametric STL meshes generated from\n"
            "../docs/design-spec.md dimensions for Bambu Studio use.\n\n"
            "Implemented in this pass:\n"
            "- 1.0mm tongue-and-groove seam (0.18mm clearance target, looser fit)\n"
            "- 4x snap tabs near end arcs (+/-30deg locations), tuned for lower insertion force\n\n"
            "Canonical parts:\n"
            "- shell-top.stl\n"
            "- shell-bottom.stl\n\n"
            "Negative cutouts:\n"
            "- neg-usbc-left-recess.stl\n"
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
