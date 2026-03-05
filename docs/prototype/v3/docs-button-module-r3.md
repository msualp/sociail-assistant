# v3 Button Module R3 Integration

This pass integrates the `prototype/modules/button-module-22-24-v1/` button system into v3 build scripts.

## Defaults
- Default plunger size: `24mm`
- Alternate size: `22mm`
- Shell cutout OD used in scripts: `24.6mm` (`24 + 0.6` clearance)

## Placement and Ergonomics
- Button center: `x=0`, `y=-8` on top shell.
- Rationale: reachable in-hand with thumb while still comfortable when attached to phone via MagSafe.
- Added a local flat island around the button on curved top surfaces to reduce plunger rocking and improve bezel seating.

## Mechanical Assumptions
- Bezel is rigid PLA/PETG for anti-press behavior.
- TPU remains for plunger only.
- Firmware press-and-hold gating remains recommended (`150-250ms`).

## Updated Script Families
- `prototype/v3/scripts/build-assets-polished-r1.py`
- `prototype/v3/scripts/build-assets-r2-loose.py`
- `prototype/v3/scripts/build-assets-r2-tight.py`
- `prototype/v3/scripts/build-assets-r3.py`
- `prototype/v3/scripts/build-assets-r3-loose.py`
- `prototype/v3/scripts/build-assets-r3-mid.py`
- `prototype/v3/scripts/build-assets-r3-tight.py`
- `prototype/v3/scripts/build-assets-r3-internals-v1.py`
- `prototype/v3/scripts/build-assets-r3-internals-v1-loose.py`
- `prototype/v3/scripts/build-assets-r3-internals-v1-tight.py`
