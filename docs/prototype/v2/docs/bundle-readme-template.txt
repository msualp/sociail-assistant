================================================================================
SOCIAIL ASSISTANT ENCLOSURE v2.0 — CANONICAL FILE SET
================================================================================

This bundle contains the LOCKED geometry for the Sociail Assistant v2.0
pill-form enclosure. Do not use any other version.

--------------------------------------------------------------------------------
LOCKED SPECIFICATION
--------------------------------------------------------------------------------

    Dimensions:     85 mm (L) × 35 mm (W) × 14 mm (H)
    Form:           Pill/capsule (stadium profile)
    Wall thickness: 2.6 mm
    Shell split:    Z = 8.4 mm (60% bottom / 40% top)
    Edge fillets:   4 mm (G2 continuous)

--------------------------------------------------------------------------------
FILE LIST
--------------------------------------------------------------------------------

Main Printable Parts:
    shell-top.stl      Top shell (hero surface)
    shell-bottom.stl   Bottom shell (functional)

Negative Cutouts (add as Negative Parts in Bambu Studio):
    neg-usbc-left-recess.stl        USB-C recessed pocket
    neg-led-window.stl       55mm pill-shaped LED window
    neg-button-well.stl              12mm tactile button depression
    neg-mic-array.stl         5-hole microphone array
    neg-speaker-grill.stl            3×5 stadium slot speaker grill
    neg-screw-holes-4x.stl          (Optional) 4x screw locations

Source Files:
    assistant-v2.f3d            Fusion 360 parametric source
    assistant-v2.step           Universal CAD exchange format

--------------------------------------------------------------------------------
BAMBU STUDIO WORKFLOW
--------------------------------------------------------------------------------

TOP SHELL:
1. Import: shell-top.stl
2. Right-click → Add Part → Load as Negative Part:
   - neg-led-window.stl
   - neg-button-well.stl
   - (Optional) neg-screw-holes-4x.stl
3. Flip upside-down (hero surface on bed)

BOTTOM SHELL:
1. Import: shell-bottom.stl
2. Right-click → Add Part → Load as Negative Part:
   - neg-usbc-left-recess.stl
   - neg-mic-array.stl
   - neg-speaker-grill.stl
   - (Optional) neg-screw-holes-4x.stl
3. Print upright (cavity facing up)

--------------------------------------------------------------------------------
PRINT PROFILES
--------------------------------------------------------------------------------

ITERATION (fit testing):
    Layer height:   0.12 mm
    Walls:          4
    Infill:         12% gyroid
    Supports:       OFF

HERO (demo quality):
    Layer height:   0.08 mm
    Walls:          4-5
    Infill:         15% gyroid
    Top layers:     8
    Outer speed:    40 mm/s
    Ironing:        ON (top surfaces)
    Seam:           Aligned (parting line edge)
    Supports:       OFF

--------------------------------------------------------------------------------
FEATURE LOCATIONS
--------------------------------------------------------------------------------

    USB-C:      Left end (-X), recessed pocket, Z = 5 mm
    LED Bar:    Top surface, 55mm pill-shaped, offset +12mm toward front
    Button:     Top surface, centered under LED midpoint
    Mic Array:  Front face (+Y), upper region, Z = 10 mm, 5 holes
    Speaker:    Front face (+Y), lower region, Z = 4 mm, 3×5 grid

--------------------------------------------------------------------------------
ASSEMBLY
--------------------------------------------------------------------------------

1. Dry-fit: Align shells, press evenly, listen for snap click
2. Seam check: Gap should be <0.15 mm, even all around
3. (Optional) Add M2.5 screws for durability

--------------------------------------------------------------------------------
POST-PROCESSING FOR APPLE-STYLE FINISH
--------------------------------------------------------------------------------

1. Wet sand with foam blocks: 320 → 400 → 600 → 800 grit
2. Filler primer (2 light coats)
3. Spot putty any defects
4. Final primer
5. Top coat: Matte/satin spray OR 2K automotive clear for gloss
6. Colors: Space Gray, Arctic White

--------------------------------------------------------------------------------
VALIDATION CHECKLIST
--------------------------------------------------------------------------------

[ ] USB-C connector inserts smoothly
[ ] LED window aligned with top surface
[ ] Button well centered and tactile
[ ] Mic holes unobstructed
[ ] Speaker grill clear
[ ] Snap-fit engages with click
[ ] Parting line gap < 0.15 mm
[ ] No visible flat spots on curves
[ ] Feels balanced in hand

--------------------------------------------------------------------------------
VERSION HISTORY
--------------------------------------------------------------------------------

v2.0    2025-01-28    Initial pill-form design (85×35×14 mm)
                      Apple-inspired rounded aesthetics
                      Replaces v1.2 angular bar design

--------------------------------------------------------------------------------
REFERENCE DOCUMENTATION
--------------------------------------------------------------------------------

Full specifications:  design-spec.md
Workflow guide:       runbook.md
Extended guide:       runbook-extended.md

================================================================================
