# v3 R3 Internals V1 Tight Fit (MagSafe)

Generated print assets for a modern, rounded MagSafe-friendly enclosure with production-oriented geometry tuning.

## What Changed vs R3 Internals V1
- Tighter XIAO cradle tuning: reduced side clearance and stronger nubs
- Tighter LiPo tray tuning: slightly reduced tray with taller front lip
- Preserves the same exterior, cutouts, and seam behavior as r3-internals-v1

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
