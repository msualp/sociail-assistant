# Sociail Assistant Parts List (Design-Locked)

This list defines the physical parts the current v2 (handheld) and v4 (MagSafe) enclosures are designed around.
If a part changes, update this file first, then regenerate the CAD assets.

## Shared Components
- **Board**: Seeed Studio XIAO ESP32S3 (21 x 17.5 mm PCB, USB-C on-board)
- **Switch**: 6 x 6 mm 4-pin tactile momentary (3.5 mm class height)
- **LED**: 6 mm wide WS2812B LED strip (single segment window)
- **Mic holes**: 0.9-1.1 mm class holes in front array (aligned to existing grill)

## v2 Handheld (r3)
- **Speaker**: Round 23–24 mm coin speaker (4Ω/1W class)
- **Battery**: Thin side-mounted LiPo approx **30 x 12 x 3–4 mm**
  - Battery tray is placed on the rear (negative Y) side to avoid speaker overlap.
  - Larger batteries (>= 20 mm width or >= 28 mm length) will collide with the speaker + XIAO cradle in this envelope.

## v4 MagSafe (r2)
- **Speaker**: Round 23–24 mm coin speaker (4Ω/1W class)
- **Battery**: LiPo pouch **40 x 30 x 5 mm** (tray included)

## Notes
- v2 and v4 intentionally use different battery sizes to fit their envelopes.
- If you want a larger v2 battery or a different speaker size, the enclosure dimensions must change or the speaker must be downsized.
