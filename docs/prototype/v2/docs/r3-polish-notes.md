# v2 R3 Polish Notes

This pass upgrades the v2 handled form factor with a cleaner industrial design while keeping the locked envelope at `85 x 35 x 14 mm`.

## What changed
- Increased exterior rounding (`FILLET = 5.2`) for a softer, more premium silhouette.
- Added subtle side and shoulder contouring to improve hand comfort and reduce hard edge feel.
- Kept the existing two-shell architecture and seam strategy:
  - `1.0 mm` tongue-and-groove
  - `4x` end-arc snap tabs
- Added three retention variants for fast physical A/B testing:
  - `r3-loose`
  - `r3-mid`
  - `r3-tight`

## Retention tuning values
| Variant | Lip Clearance | Snap Engage | Tab Thick | Slot Depth | Notch Extra |
|---|---:|---:|---:|---:|---:|
| r3-loose | 0.18 | 0.58 | 1.20 | 2.15 | 1.05 |
| r3-mid   | 0.12 | 0.80 | 1.35 | 1.85 | 0.82 |
| r3-tight | 0.08 | 0.98 | 1.50 | 1.55 | 0.52 |

## Print artifacts
Each variant includes:
- `shell-top.stl`, `shell-bottom.stl`
- `shell-top-print.stl`, `shell-bottom-print.stl`
- `shell-top-print-screws.stl`, `shell-bottom-print-screws.stl`
- matching `neg-*.stl` cutters

## Post-generation cleanup
Run once after any regeneration to strip detached micro-components:

`.venv/bin/python prototype/v2/scripts/cleanup-shell-components.py prototype/v2/r3-loose prototype/v2/r3-mid prototype/v2/r3-tight`

## Sheet files
Single-file sheet STLs are generated at `prototype/v2/sheets/` via:

`.venv/bin/python prototype/v2/scripts/build-r3-sheets.py`

Bundle:
- `prototype/v2/r3-sheets.zip`

## Orientation baseline (Bambu)
- Top shell: upside-down (hero side on bed)
- Bottom shell: upright (cavity up)
