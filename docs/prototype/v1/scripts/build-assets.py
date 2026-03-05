#!/usr/bin/env python3
"""
Generate Bambu-ready STL meshes by pre-subtracting negative cutout parts.

Requires:
    pip install meshlib
"""

from pathlib import Path

from meshlib import mrmeshpy as mr


SRC_DIR = Path("prototype/v1/w55-negatives")
OUT_DIR = Path("prototype/v1/w55-print-ready")


def load(name: str) -> mr.Mesh:
    return mr.loadMesh(str(SRC_DIR / name))


def save(mesh: mr.Mesh, name: str) -> None:
    mesh.packOptimally(True)
    mr.saveMesh(mesh, str(OUT_DIR / name))


def boolean_subtract(base_name: str, negatives: list[str], out_name: str) -> None:
    mesh = load(base_name)
    for neg_name in negatives:
        result = mr.boolean(mesh, load(neg_name), mr.BooleanOperation.DifferenceAB)
        if not result.valid():
            raise RuntimeError(f"Boolean failed for {base_name} - {neg_name}: {result.errorString}")
        mesh = result.mesh
    save(mesh, out_name)


def voxel_subtract_with_decimation(
    base_name: str,
    neg_name: str,
    out_name: str,
    voxel_size: float = 0.12,
    max_error: float = 0.1,
) -> None:
    mesh = mr.voxelBooleanSubtract(load(base_name), load(neg_name), voxel_size)
    decimate = mr.DecimateSettings()
    decimate.maxError = max_error
    decimate.maxDeletedFaces = mesh.topology.numValidFaces()
    mr.decimateMesh(mesh, decimate)
    save(mesh, out_name)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    top_required = [
        "neg-led-window.stl",
        "neg-button.stl",
    ]
    bottom_required = [
        "neg-usbc-left.stl",
        "neg-mic-array.stl",
        "neg-speaker-grill.stl",
    ]
    screw_holes = "neg-screw-holes-4x.stl"

    boolean_subtract(
        "shell-top.stl",
        top_required,
        "shell-top-print.stl",
    )
    boolean_subtract(
        "shell-bottom.stl",
        bottom_required,
        "shell-bottom-print.stl",
    )
    boolean_subtract(
        "shell-top.stl",
        top_required + [screw_holes],
        "shell-top-print-screws.stl",
    )

    # Direct boolean subtraction fails for bottom screw holes; use voxel path.
    voxel_subtract_with_decimation(
        "shell-bottom.stl",
        screw_holes,
        "shell-bottom-print-screws.stl",
    )

    print(f"Generated meshes in: {OUT_DIR}")


if __name__ == "__main__":
    main()
