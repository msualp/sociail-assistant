#!/usr/bin/env python3
"""Fuse multi-body plunger STLs into single-body meshes for easier slicing.

Requires:
- trimesh
- manifold3d (boolean backend)
"""

from __future__ import annotations

from pathlib import Path

import trimesh


MODULE_DIR = Path(__file__).resolve().parent.parent
PLUNGERS = [
    MODULE_DIR / "plunger_concave_22mm.stl",
    MODULE_DIR / "plunger_concave_24mm.stl",
]


def load_mesh(path: Path) -> trimesh.Trimesh:
    mesh = trimesh.load(path)
    if isinstance(mesh, trimesh.Scene):
        if not mesh.geometry:
            raise RuntimeError(f"Empty scene: {path}")
        return trimesh.util.concatenate(tuple(mesh.geometry.values()))
    return mesh


def component_count(mesh: trimesh.Trimesh) -> int:
    return len(mesh.split(only_watertight=False))


def fuse(path: Path) -> tuple[int, int, bool]:
    mesh = load_mesh(path)
    before = component_count(mesh)
    if before <= 1:
        mesh.export(path)
        return before, before, bool(mesh.is_watertight)

    parts = mesh.split(only_watertight=False)
    fused = trimesh.boolean.union(parts, engine="manifold")
    if fused is None:
        raise RuntimeError(f"Boolean union returned None for {path}")

    fused.remove_unreferenced_vertices()
    fused.merge_vertices()
    after = component_count(fused)
    if after != 1:
        raise RuntimeError(f"Expected 1 component after fuse for {path}, got {after}")

    fused.export(path)
    return before, after, bool(fused.is_watertight)


def main() -> None:
    for path in PLUNGERS:
        if not path.exists():
            raise FileNotFoundError(path)

        before, after, watertight = fuse(path)
        print(f"{path.name}: components {before} -> {after}, watertight={watertight}")


if __name__ == "__main__":
    main()
