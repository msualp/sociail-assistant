Sociail Button Module 22/24 (v1)

Default prototype size: 24mm
Alternate size: 22mm

Files (each size):
- plunger_concave_XXmm.stl       -> print in TPU 95A
- bezel_guard_XXmm.stl           -> print in PLA/PETG (recommended) or TPU
- neg_button_cutout_XXmm.stl     -> use as a Negative Part to cut top-shell opening
- Plunger STLs are single-body, watertight meshes for clean slicer import.

Mechanical strategy:
- Bezel guard sits 0.8-1.2mm above plunger rim.
- Plunger top sits 0.3-0.7mm below bezel top.
- Add firmware press-hold debounce (150-250ms).
- For curved tops, create a local flat island under the bezel to avoid plunger rocking.

Recommended stack:
- Switch: Adafruit Soft Silicone Top 6mm push-button (4183)
- Plunger: TPU 95A
- Bezel: rigid PLA/PETG for anti-press behavior
- Feel tuning: 1mm foam disk or 6mm silicone bumper between stem and switch

Suggested print settings (Bambu P1S):
- TPU plunger: 0.16-0.20mm, 3-4 walls, 15-25% gyroid, slow TPU profile
- Bezel: 0.16-0.20mm, 3 walls, 10-15% infill

First-print shortcuts (Bambu Studio):
- Print the 24mm set first: plunger_concave_24mm + bezel_guard_24mm.
- Right-click each part and choose "Place on face" before slicing.
- TPU plunger: add a 3-5mm brim for better bed hold.
- Keep supports OFF for plungers and bezels.
- Use the cutout STL only as a Negative Part in shell projects.

Assembly notes:
- Cut opening using neg_button_cutout as Negative Part.
- Attach bezel around opening (prototype glue or designed seat).
- Mount switch beneath opening so plunger stem contacts switch.
