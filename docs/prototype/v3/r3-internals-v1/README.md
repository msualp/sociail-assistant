# v3 R3 Internals V1 (MagSafe)

Generated print assets for a modern, rounded MagSafe-friendly enclosure with production-oriented geometry tuning.

## What Changed vs R3 Mid
- Adds a centered XIAO ESP32S3 Sense cradle (21 x 17.5 mm class) with light retention nubs
- Adds a fitted LiPo tray for common 800-1000 mAh flat cells (~55 x 34 mm class)
- Adds a side auxiliary shelf for MAX17048 or divider breakout
- Adds shallow wire-routing channels to reduce top-shell interference
- Preserves the same exterior and enclosure seam behavior as r3-mid

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
