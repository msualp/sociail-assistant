#!/usr/bin/env python3
"""
Generate centered PCB keepout templates for v3 r3 cavity.

Outputs (per size):
- STL board placeholder (1.6 mm thick)
- Dimensioned DXF (board + cavity reference + centerlines)
"""

from __future__ import annotations

from pathlib import Path

import ezdxf
import trimesh
from ezdxf.enums import TextEntityAlignment


OUT_DIR = Path("prototype/v3/templates")

# Derived from r3 cavity analysis.
CAVITY_X = 71.606
CAVITY_Y = 58.368
CAVITY_Z = 11.204
BOTTOM_CAVITY_Z = 6.810
TOP_CAVITY_Z = 4.414

BOARD_THICKNESS = 1.6
SIZES = [(60.0, 46.0), (62.0, 48.0)]


def add_rect(msp, w: float, h: float, layer: str) -> None:
    x0, x1 = -w / 2.0, w / 2.0
    y0, y1 = -h / 2.0, h / 2.0
    msp.add_line((x0, y0), (x1, y0), dxfattribs={"layer": layer})
    msp.add_line((x1, y0), (x1, y1), dxfattribs={"layer": layer})
    msp.add_line((x1, y1), (x0, y1), dxfattribs={"layer": layer})
    msp.add_line((x0, y1), (x0, y0), dxfattribs={"layer": layer})


def add_centerlines(msp) -> None:
    span = max(CAVITY_X, CAVITY_Y) / 2.0 + 16.0
    msp.add_line((-span, 0.0), (span, 0.0), dxfattribs={"layer": "CENTER"})
    msp.add_line((0.0, -span), (0.0, span), dxfattribs={"layer": "CENTER"})


def add_arrow_x(msp, x: float, y: float, size: float, layer: str, inward: bool) -> None:
    dx = size if inward else -size
    msp.add_line((x, y), (x + dx, y + size * 0.55), dxfattribs={"layer": layer})
    msp.add_line((x, y), (x + dx, y - size * 0.55), dxfattribs={"layer": layer})


def add_arrow_y(msp, x: float, y: float, size: float, layer: str, inward: bool) -> None:
    dy = size if inward else -size
    msp.add_line((x, y), (x + size * 0.55, y + dy), dxfattribs={"layer": layer})
    msp.add_line((x, y), (x - size * 0.55, y + dy), dxfattribs={"layer": layer})


def add_dim_x(msp, width: float, y_ref: float, y_dim: float, label: str) -> None:
    x0, x1 = -width / 2.0, width / 2.0
    layer = "DIM"
    msp.add_line((x0, y_ref), (x0, y_dim), dxfattribs={"layer": layer})
    msp.add_line((x1, y_ref), (x1, y_dim), dxfattribs={"layer": layer})
    msp.add_line((x0, y_dim), (x1, y_dim), dxfattribs={"layer": layer})
    add_arrow_x(msp, x0, y_dim, 1.8, layer, inward=True)
    add_arrow_x(msp, x1, y_dim, 1.8, layer, inward=False)
    t = msp.add_text(label, dxfattribs={"layer": layer, "height": 2.4})
    t.set_placement((0.0, y_dim + 2.0), align=TextEntityAlignment.MIDDLE_CENTER)


def add_dim_y(msp, height: float, x_ref: float, x_dim: float, label: str) -> None:
    y0, y1 = -height / 2.0, height / 2.0
    layer = "DIM"
    msp.add_line((x_ref, y0), (x_dim, y0), dxfattribs={"layer": layer})
    msp.add_line((x_ref, y1), (x_dim, y1), dxfattribs={"layer": layer})
    msp.add_line((x_dim, y0), (x_dim, y1), dxfattribs={"layer": layer})
    add_arrow_y(msp, x_dim, y0, 1.8, layer, inward=True)
    add_arrow_y(msp, x_dim, y1, 1.8, layer, inward=False)
    t = msp.add_text(label, dxfattribs={"layer": layer, "height": 2.4, "rotation": 90.0})
    t.set_placement((x_dim + 2.2, 0.0), align=TextEntityAlignment.MIDDLE_CENTER)


def write_dxf(path: Path, board_x: float, board_y: float) -> None:
    doc = ezdxf.new("R2018")
    doc.units = ezdxf.units.MM

    layers = doc.layers
    layers.new("BOARD", dxfattribs={"color": 3})
    layers.new("CAVITY", dxfattribs={"color": 5})
    layers.new("CENTER", dxfattribs={"color": 8})
    layers.new("DIM", dxfattribs={"color": 2})
    layers.new("TEXT", dxfattribs={"color": 7})

    msp = doc.modelspace()

    add_rect(msp, CAVITY_X, CAVITY_Y, "CAVITY")
    add_rect(msp, board_x, board_y, "BOARD")
    add_centerlines(msp)

    add_dim_x(msp, board_x, board_y / 2.0, board_y / 2.0 + 8.0, f"{board_x:.1f} mm")
    add_dim_y(msp, board_y, board_x / 2.0, board_x / 2.0 + 8.0, f"{board_y:.1f} mm")

    add_dim_x(
        msp,
        CAVITY_X,
        CAVITY_Y / 2.0,
        CAVITY_Y / 2.0 + 20.0,
        f"Cavity {CAVITY_X:.1f} mm",
    )
    add_dim_y(
        msp,
        CAVITY_Y,
        CAVITY_X / 2.0,
        CAVITY_X / 2.0 + 20.0,
        f"Cavity {CAVITY_Y:.1f} mm",
    )

    margin_x = (CAVITY_X - board_x) / 2.0
    margin_y = (CAVITY_Y - board_y) / 2.0

    note = msp.add_mtext(
        (
            f"v3 r3 centered board template\\P"
            f"Board: {board_x:.1f} x {board_y:.1f} mm\\P"
            f"Side margins: {margin_x:.2f} mm (X), {margin_y:.2f} mm (Y)\\P"
            f"Cavity envelope: {CAVITY_X:.1f} x {CAVITY_Y:.1f} x {CAVITY_Z:.1f} mm\\P"
            f"Bottom/Top cavity Z: {BOTTOM_CAVITY_Z:.2f} / {TOP_CAVITY_Z:.2f} mm"
        ),
        dxfattribs={"layer": "TEXT", "char_height": 2.2},
    )
    note.set_location((-CAVITY_X / 2.0, -CAVITY_Y / 2.0 - 16.0))

    doc.saveas(path)


def write_stl(path: Path, board_x: float, board_y: float) -> None:
    mesh = trimesh.creation.box(extents=(board_x, board_y, BOARD_THICKNESS))
    mesh.apply_translation((0.0, 0.0, BOARD_THICKNESS / 2.0))
    mesh.export(path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary: list[str] = []

    for board_x, board_y in SIZES:
        stem = f"pcb-keepout-{int(board_x)}x{int(board_y)}"
        stl_path = OUT_DIR / f"{stem}.stl"
        dxf_path = OUT_DIR / f"{stem}.dxf"

        write_stl(stl_path, board_x, board_y)
        write_dxf(dxf_path, board_x, board_y)

        margin_x = (CAVITY_X - board_x) / 2.0
        margin_y = (CAVITY_Y - board_y) / 2.0
        summary.append(
            f"{stem}: margins X={margin_x:.2f} mm, Y={margin_y:.2f} mm"
        )

    (OUT_DIR / "README.md").write_text(
        """# v3 PCB Keepout Templates

Centered PCB templates for v3 r3 internals.

## Files
- `pcb-keepout-60x46.stl`
- `pcb-keepout-60x46.dxf`
- `pcb-keepout-62x48.stl`
- `pcb-keepout-62x48.dxf`

## Geometry Basis
- Cavity envelope: `71.6 x 58.4 x 11.2 mm`
- Bottom cavity: `6.81 mm`
- Top cavity: `4.41 mm`

## Notes
- STLs are board placeholders at `1.6 mm` thickness, centered at origin.
- DXFs include board outline, cavity reference outline, centerlines, and dimensions.
- For a stated `35 x 86 mm` board: not a fit in this enclosure (straight or diagonal) against the 71.6 x 58.4 mm cavity envelope.
""",
        encoding="utf-8",
    )

    print("Template summary:")
    for line in summary:
        print(line)


if __name__ == "__main__":
    main()
