# Design Details & Prototype Plan

This document is the **single source of truth** for turning the Sociail Assistant enclosure design into a **real, physical, demo-ready prototype** using the **Bambu Lab P1S**.

It is written to be practical, sequential, and repeatable — not theoretical.

---

## 1. Design Overview (What We Are Building)

**Form factor**
- Slim bar (Alexa Auto–style)
- Handheld + in-car compatible

**Outer dimensions**
- Length: **150 mm**
- Width: **55 mm**
- Thickness: **22 mm**

**Shell architecture**
- Two-piece enclosure
  - **Top**: hero surface (visual quality priority)
  - **Bottom**: functional surface (ports, speaker, assembly)
- Alignment lip for clean seam
- Snap-fit tabs for quick assembly
- Screw bosses for durability / fallback

**User-facing elements**
- Medium LED light bar (~75 mm), offset toward front
- Single physical button centered under LED
- USB-C on **left end**
- Microphone holes (front, upper)
- Speaker grill (front, lower)

This design is intentionally **print-first**, not injection-mold-first.

---

## 2. Files & Canonical Assets

### Canonical ZIP (keep only this)

```
sociail_assistant_enclosure_v1_2_FULL_W55_negative_cutouts.zip
```

### Inside the ZIP

**Main printable parts**
- sociail_assistant_bar_top_v1_2_W55.stl
- sociail_assistant_bar_bottom_v1_2_W55.stl

**Negative cutouts (used in Bambu Studio)**
- neg_usb_c_left_end_v1_2.stl
- neg_led_window_offset_front_v1_2.stl
- neg_button_center_under_led_v1_2.stl
- neg_mic_holes_front_top_v1_2.stl
- neg_speaker_holes_front_lower_v1_2.stl
- neg_screw_holes_4x_v1_2.stl (optional)

---

## 3. Bambu Studio Workflow (Exact)

### TOP (hero shell)
1. Import sociail_assistant_bar_top_v1_2_W55.stl
2. Add Part → Load (Negative Part):
   - LED window
   - Button hole
   - Optional screw holes

### BOTTOM (functional shell)
1. Import sociail_assistant_bar_bottom_v1_2_W55.stl
2. Add Part → Load (Negative Part):
   - USB-C opening
   - Mic holes
   - Speaker grill
   - Optional screw holes

---

## 4. Print Profiles

### Fast Iteration
- Layer height: 0.12 mm
- Walls: 4
- Infill: 12% gyroid
- Supports: none

### Hero / Demo
- Layer height: 0.08 mm
- Walls: 4–5
- Seam: aligned (underside)

---

## 5. Print Orientation

- **Top shell**: upside-down (hero face on bed)
- **Bottom shell**: upright, cavity up

---

## 6. Assembly

- Snap-fit first
- Screws optional (M2.5–M3)
- Heat-set inserts optional for durability

---

## 7. Post-Processing

- Sand 400 → 800 grit
- Filler primer
- Matte or satin spray

---

## 8. Validation Checklist

- USB-C fits cleanly
- LED aligns
- Button press feels deliberate
- Mic & speaker unobstructed
- Seam is even

---

## 9. Guiding Principle

**Print it. Hold it. Iterate.**

---

# v2.0 Design — Modern Pill Form (NEW)

## 10. v2.0 Design Overview

**Form factor**
- Pill/capsule shape (stadium profile)
- Compact, pocketable form
- Apple-inspired rounded aesthetics

**Outer dimensions**
- Length: **85 mm**
- Width: **35 mm**
- Thickness: **14 mm**

**Key changes from v1.2**
- 77% volume reduction
- Continuous 4mm edge fillets
- Recessed features (USB-C pocket, LED inset)
- 60/40 shell split (vs 50/50)
- G2 curvature continuity

---

## 11. v2.0 Files & Naming Convention

### Canonical ZIP (v2.0)

```
sociail_assistant_enclosure_v2_0_W35/
```

### Inside the ZIP

**Main printable parts**
- sociail_assistant_pill_top_v2_0_W35.stl
- sociail_assistant_pill_bottom_v2_0_W35.stl

**Negative cutouts (used in Bambu Studio)**
- neg_usb_c_left_recess_v2_0.stl
- neg_led_window_rounded_v2_0.stl
- neg_button_well_v2_0.stl
- neg_mic_perforations_v2_0.stl
- neg_speaker_grill_v2_0.stl
- neg_screw_bosses_4x_v2_0.stl (optional)

**Source files**
- sociail_assistant_v2_0.f3d (Fusion 360)
- sociail_assistant_v2_0.step (Universal exchange)

---

## 12. v2.0 CAD Workflow (Fusion 360)

### Parametric Setup
```
overall_length    = 85 mm
overall_width     = 35 mm
overall_height    = 14 mm
end_radius        = 17.5 mm
edge_fillet       = 4 mm
wall_thickness    = 2.6 mm
split_height      = 8.4 mm
```

### Modeling Steps
1. Create stadium profile sketch (rectangle + semicircle ends)
2. Extrude to target height
3. Apply 4mm G2 fillets to all edges
4. Shell with 2.6mm wall thickness
5. Split body at Z = 8.4mm
6. Add alignment tongue-and-groove lip
7. Add 4x cantilever snap-fits at corners
8. Export as separate STL files

---

## 13. v2.0 Feature Specifications

| Feature | Spec |
|---------|------|
| USB-C | Recessed pocket 14×8×3mm, opening 9.5×3.5mm |
| LED bar | 55mm pill-shaped, 0.5mm recessed |
| Button | 12mm well, 1.5mm deep, 6mm through-hole |
| Mic array | 5 holes × 1.2mm, 4mm spacing |
| Speaker | 3×5 grid, 2×4mm stadium slots |

See `sociail_assistant_v2_0_design_spec.md` for complete specifications.

---

## 14. v1.2 vs v2.0 Comparison

| Aspect | v1.2 | v2.0 |
|--------|------|------|
| Dimensions | 150×55×22 mm | 85×35×14 mm |
| Form | Rectangular bar | Pill/capsule |
| Edges | Sharp | 4mm continuous fillets |
| Volume | ~181,500 mm³ | ~41,650 mm³ |
| Aesthetic | Functional | Apple-inspired |
