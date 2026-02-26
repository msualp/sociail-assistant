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
    sociail_assistant_pill_top_v2_0_W35.stl      Top shell (hero surface)
    sociail_assistant_pill_bottom_v2_0_W35.stl   Bottom shell (functional)

Negative Cutouts (add as Negative Parts in Bambu Studio):
    neg_usb_c_left_recess_v2_0.stl        USB-C recessed pocket
    neg_led_window_rounded_v2_0.stl       55mm pill-shaped LED window
    neg_button_well_v2_0.stl              12mm tactile button depression
    neg_mic_perforations_v2_0.stl         5-hole microphone array
    neg_speaker_grill_v2_0.stl            3×5 stadium slot speaker grill
    neg_screw_bosses_4x_v2_0.stl          (Optional) 4x screw locations

Source Files:
    sociail_assistant_v2_0.f3d            Fusion 360 parametric source
    sociail_assistant_v2_0.step           Universal CAD exchange format

--------------------------------------------------------------------------------
BAMBU STUDIO WORKFLOW
--------------------------------------------------------------------------------

TOP SHELL:
1. Import: sociail_assistant_pill_top_v2_0_W35.stl
2. Right-click → Add Part → Load as Negative Part:
   - neg_led_window_rounded_v2_0.stl
   - neg_button_well_v2_0.stl
   - (Optional) neg_screw_bosses_4x_v2_0.stl
3. Flip upside-down (hero surface on bed)

BOTTOM SHELL:
1. Import: sociail_assistant_pill_bottom_v2_0_W35.stl
2. Right-click → Add Part → Load as Negative Part:
   - neg_usb_c_left_recess_v2_0.stl
   - neg_mic_perforations_v2_0.stl
   - neg_speaker_grill_v2_0.stl
   - (Optional) neg_screw_bosses_4x_v2_0.stl
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

Full specifications:  sociail_assistant_v2_0_design_spec.md
Workflow guide:       design-details-and-prototype-runbook.md
Extended guide:       design-details-and-prototype-runbook-extended.md

================================================================================
