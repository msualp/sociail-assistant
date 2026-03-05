Sociail MagSafe AI Assistant – SLEEK Prototype (v1)
Generated: 2026-03-04T22:39:30

Design intent
- Modern, Apple-like: flat back + softly rounded perimeter + gently tapered top
- MagSafe ring recess on back for snap-on iPhone attachment
- Ergonomic in hand: no sharp edges, modest thickness, thumb-friendly button

Coordinate system (canonical)
- X: length, Y: width, Z: height
- Back face (touching iPhone): Z=0 (flat)
- Visible face: Z=H (LED + button)
- Audio face: +X (speaker lower, mics upper)
- USB-C: -Y edge (bottom edge)

Envelope
- 78.0 x 64.0 x 16.0 mm

Main parts
- shell-top.stl
- shell-bottom.stl

NEGATIVE PARTS (load in Bambu Studio as Negative Part)
- neg-magsafe-ring.stl
- neg-led-window.stl
- neg_button.stl
- neg-usbc-bottom.stl
- neg-mic-array.stl
- neg-speaker-grill.stl
- neg-screw-holes-4x.stl (optional)

Bambu Studio workflow
TOP:
1) Import shell-top.stl
2) Add Part -> Load... set as Negative Part:
   - neg-led-window.stl
   - neg_button.stl
   - (optional) neg-screw-holes-4x.stl

BOTTOM:
1) Import shell-bottom.stl
2) Add Part -> Load... set as Negative Part:
   - neg-magsafe-ring.stl
   - neg-usbc-bottom.stl
   - neg-mic-array.stl
   - neg-speaker-grill.stl
   - (optional) neg-screw-holes-4x.stl

Recommended P1S settings
- Layer height: 0.12mm (iterate) or 0.08mm (hero)
- Walls: 4
- Infill: 12% gyroid
- Supports: NONE
- Seam: aligned (put seam on underside edge)

Print orientation
- TOP: print upside-down (hero surface on bed)
- BOTTOM: print upright (flat back on bed)

Magnet note
- Ring recess sized for common MagSafe magnet rings (OD ~56, ID ~46, depth ~1.8).
- Consider a thin TPU/film between iPhone and plastic to avoid scratches.
