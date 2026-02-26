# Sociail Assistant Hardware Prototype Runbook (v1.2)
**From STL to Polished, Demo-Ready Prototype using Bambu Lab P1S**

This document is the **authoritative runbook** for producing a **credible, investor- and user-ready physical prototype** of the Sociail Assistant enclosure.

This is not a concept note.
This is a **do-this, then-that execution guide**.

---

## 0. Purpose & Success Criteria

### Goal
Produce a **clean, confident, physical prototype** that:
- Looks intentional (not “3D-printed”)
- Feels good in the hand
- Assembles reliably
- Can survive repeated demos and handling
- Is fast to iterate if changes are needed

### Non-goals (for v1.2)
- Injection molding readiness
- Final internal PCB geometry
- Waterproofing / IP ratings

If it looks good, feels solid, and demos well — **this runbook succeeded**.

---

## 1. Canonical Inputs (DO NOT DEVIATE)

### 1.1 Canonical STL Bundle
This is the **only** enclosure geometry you should be using:

```
sociail_assistant_enclosure_v1_2_FULL_W55_negative_cutouts.zip
```

Delete all older files. Do not mix versions.

### 1.2 What’s in the Bundle
**Main shells**
- sociail_assistant_bar_top_v1_2_W55.stl (hero surface)
- sociail_assistant_bar_bottom_v1_2_W55.stl (functional shell)

**Negative cutouts (used in Bambu Studio)**
- USB-C (left end)
- LED window (75mm, offset front)
- Single button hole
- Mic holes (front/top)
- Speaker grill (front/lower)
- Optional screw holes (4x)

These negative files are **not optional** — they are how we iterate cleanly.

---

## 2. Hardware & Material Prep

### 2.1 Printer
- **Bambu Lab P1S**
- Stock 0.4mm nozzle (hardened preferred)

### 2.2 Filament (choose ONE)
**Iteration**
- PLA+ (neutral color, matte preferred)

**Demo / Hero**
- PLA+ (best surface)
- PETG (slightly tougher feel)

Avoid ABS/ASA until geometry is locked.

### 2.3 Tools You’ll Need
- Flush cutters
- Small file set
- Sandpaper: 400 / 600 / 800 grit
- Small Phillips screwdriver
- (Optional) heat-set insert tool

---

## 3. Bambu Studio Setup (Critical Section)

### 3.1 General Settings
- Supports: **OFF**
- Infill: **12% Gyroid**
- Walls: **4**
- Seam: **Aligned** (place on underside edge)

### 3.2 Print Profiles

#### FAST ITERATION
- Layer height: **0.12mm**
- Top layers: **6**
- Bottom layers: **6**

#### HERO / DEMO
- Layer height: **0.08mm**
- Top layers: **7–8**
- Bottom layers: **6**

---

## 4. Import & Subtract Geometry

### 4.1 Top Shell
1. Import sociail_assistant_bar_top_v1_2_W55.stl
2. Add Part → Load → **Negative Part**:
   - LED window
   - Button hole
   - Optional screw holes

### 4.2 Bottom Shell
1. Import sociail_assistant_bar_bottom_v1_2_W55.stl
2. Add Part → Load → **Negative Part**:
   - USB-C opening
   - Mic holes
   - Speaker grill
   - Optional screw holes

---

## 5. Print Orientation

- **Top shell**: upside-down (hero face on bed)
- **Bottom shell**: upright, cavity up

No supports required.

---

## 6. First Print Validation

Check before assembly:
- Clean LED window edges
- Button hole centered
- USB-C fits without force
- No wall delamination
- Snap tabs intact

---

## 7. Assembly

### 7.1 Dry Fit
- Snap top into bottom
- Seam should be even

### 7.2 Fasteners
- Snaps for demos
- Screws (M2.5–M3) for durability
- Heat-set inserts optional

---

## 8. Post-Processing

### Demo Grade Finish
1. Sand 400 → 600 → 800 grit
2. Filler primer (1–2 coats)
3. Matte or satin spray

---

## 9. Final Validation Checklist

- USB-C inserts cleanly
- LED aligned
- Button feels deliberate
- Mic & speaker unobstructed
- Feels balanced in hand
- Comfortable to pass around

---

## 10. Iteration Rules

- Change one variable at a time
- Reprint only affected part
- Never redesign everything at once

---

## 11. Mental Model

This prototype is **evidence**, not art.

Print → hold → fix → repeat.

---

# v2.0 WORKFLOW (NEW)

## 12. v2.0 Overview

v2.0 is a **pill-shaped redesign** with Apple-inspired rounded aesthetics.
- Dimensions: 85 × 35 × 14 mm
- Form: Stadium/capsule profile
- Tools: Fusion 360 → STL → Bambu Studio

---

## 13. Fusion 360 → STL Pipeline

### 13.1 Source Files
After CAD work, you should have:
- `sociail_assistant_v2_0.f3d` (Fusion 360 source)
- `sociail_assistant_v2_0.step` (universal exchange)

### 13.2 Export Workflow
1. Open Fusion 360 project
2. For each body (top shell, bottom shell, each cutout):
   - Right-click body → Save As Mesh
   - Format: Binary STL
   - Refinement: High
   - Units: Millimeters
3. Organize into canonical folder structure

---

## 14. v2.0 Print Profiles (Curved Surfaces)

### 14.1 Settings for Pill Shape

| Setting | Iteration | Hero |
|---------|-----------|------|
| Layer height | 0.12 mm | 0.08 mm |
| Walls | 4 | 4–5 |
| Infill | 12% gyroid | 15% gyroid |
| Top layers | 6 | 8 |
| Outer wall speed | 50 mm/s | 40 mm/s |
| Ironing | OFF | ON (top surfaces) |
| Seam | Aligned | Aligned (parting edge) |
| Supports | OFF | OFF |

### 14.2 Why 0.08mm for Hero Prints
Curved surfaces show "stair-stepping" at layer boundaries.
Finer layers minimize this effect on the rounded pill profile.

---

## 15. v2.0 Print Orientation

**Top shell (pill_top)**
- Flip upside-down
- Hero surface flat against bed
- Curved profile prints without supports

**Bottom shell (pill_bottom)**
- Upright, cavity facing up
- USB-C end prints sideways (acceptable)

---

## 16. v2.0 Post-Processing (Premium Finish)

### 16.1 Sanding Curved Surfaces
Use **foam sanding blocks** to maintain radii.
Flat blocks will create flat spots on curves.

| Step | Grit | Method |
|------|------|--------|
| 1 | 320 | Wet sand, remove layer lines |
| 2 | 400 | Wet sand, smooth |
| 3 | 600 | Wet sand, pre-primer |
| 4 | 800 | Dry, light final pass |

### 16.2 Finishing
1. Filler primer (2 light coats)
2. Spot putty any defects
3. Light sand (600)
4. Final primer
5. Top coat:
   - **Matte spray** for soft premium feel
   - **2K automotive clear** for Apple-style gloss

### 16.3 Color Options
- Space Gray (dark gunmetal)
- Arctic White (bright clean)

---

## 17. v2.0 Validation Checklist

- [ ] USB-C connector inserts smoothly
- [ ] LED window aligned with top surface
- [ ] Button well centered and tactile
- [ ] Mic holes unobstructed
- [ ] Speaker grill clear
- [ ] Snap-fit engages with click
- [ ] Parting line gap < 0.15 mm
- [ ] No visible flat spots on curves
- [ ] Feels balanced in hand
- [ ] Comfortable to pass around

---

## 18. v2.0 Iteration Rules

Same principles as v1.2:
- Change one variable at a time
- Reprint only affected part
- Never redesign everything at once

For curved surfaces specifically:
- If flat spots appear → check sanding technique
- If layer lines visible → reduce layer height
- If seam visible → adjust seam position in slicer
