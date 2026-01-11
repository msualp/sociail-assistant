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
