Sociail Assistant – Bar Enclosure Prototype (v1.2 FULL) – PRINT READY via Negative Volumes
Generated: 2025-12-28T14:57:58

Locked spec
- Outer size: 150.0 x 55.0 x 22.0 mm
- Two-piece shell with alignment lip
- USB-C: LEFT end (-X)
- LED window: 75.0mm (medium), offset toward FRONT (+X) by 24.0mm
- Single button centered under LED
- Mic holes: front face (+X), upper
- Speaker holes: front face (+X), lower
- Snap tabs included (bottom) + screw bosses included (top+bottom)

Main parts
- shell-top.stl
- shell-bottom.stl

NEGATIVE VOLUMES (set as "Negative part" in Bambu Studio)
- neg-usbc-left.stl
- neg-led-window.stl
- neg-button.stl
- neg-mic-array.stl
- neg-speaker-grill.stl
- neg-screw-holes-4x.stl  (optional; apply to both parts)

Bambu Studio workflow
TOP:
1) Import shell-top.stl
2) Add Part -> Load... and load as NEGATIVE:
   - neg-led-window.stl
   - neg-button.stl
   - (optional) neg-screw-holes-4x.stl
BOTTOM:
1) Import shell-bottom.stl
2) Add Part -> Load... and load as NEGATIVE:
   - neg-usbc-left.stl
   - neg-mic-array.stl
   - neg-speaker-grill.stl
   - (optional) neg-screw-holes-4x.stl

Recommended P1S settings (polish-first)
- Layer height: 0.08mm (hero) or 0.12mm (iterate)
- Walls: 4
- Top layers: 6
- Bottom layers: 6
- Infill: 12% gyroid
- Supports: NONE
- Seam: aligned (place seam on underside edge)
