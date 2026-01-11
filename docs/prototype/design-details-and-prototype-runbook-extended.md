# Sociail Assistant Hardware Prototype Runbook (v1.2 — EXTENDED)
**A First‑Time, No‑Guesswork Guide from STL → Polished Physical Prototype**

This runbook is written as a **recipe**, not a reference.
If this is your **first time building a physical hardware prototype**, follow it **top to bottom**.
Do not skip steps.

This document assumes:
- You have never done this end‑to‑end before
- You want the result to feel *intentional*, not experimental
- You are using a **Bambu Lab P1S**

---

## How to Read This Document

- Sections are **sequential**
- Each step includes:
  - *What you are doing*
  - *Why it matters*
  - *How to do it*
  - *Common mistakes*
  - *What success looks like*

If something goes wrong, **do not improvise** — fix the step you are in.

---

# PART 1 — UNDERSTAND THE OBJECT YOU ARE MAKING

## 1. What This Device Is (Mentally)

You are not “printing a case”.
You are creating a **convincing physical artifact** that answers one question:

> “Could this be a real product?”

That means:
- Symmetry matters
- Alignment matters
- Seams matter
- Feel matters more than perfection

---

## 2. Canonical Geometry (Locked Decisions)

### 2.1 Coordinate System (Important)

All coordinates assume:
- **X axis** = length (left ↔ right)
- **Y axis** = width (front ↔ back)
- **Z axis** = height (bottom ↔ top)

Reference orientation:
- Front = **mic + speaker side**
- Left end (−X) = **USB‑C**
- Top = **LED + button**

If you rotate parts arbitrarily in the slicer, you will confuse yourself.

---

### 2.2 External Dimensions

| Dimension | Value |
|---------|------|
| Length (X) | 150 mm |
| Width (Y) | 55 mm |
| Height (Z) | 22 mm |

Split plane:
- Top shell: Z = 11 → 22
- Bottom shell: Z = 0 → 11

Wall thickness:
- Exterior walls: ~2.6 mm
- Top roof: ~2.6 mm
- Bottom floor: ~2.6 mm

These values are **intentional**:
- Thin enough to look refined
- Thick enough to print reliably

---

### 2.3 Feature Placement (Exact Intent)

**USB‑C**
- Location: Left end (−X face)
- Centered on Y
- Z ≈ 5.8 mm from bottom

**LED Window**
- Length: ~75 mm
- Orientation: parallel to X
- Offset toward front: +24 mm on X
- Located on top surface (Z max)

**Button**
- Single
- Centered on Y
- Directly below LED on X
- On top surface

**Microphones**
- Front face (+X)
- Upper region (Z ≈ 18 mm)
- 7 holes, evenly spaced across Y

**Speaker**
- Front face (+X)
- Lower region (Z ≈ 6 mm)
- 9 holes, evenly spaced across Y

These placements are chosen to:
- Read visually correct
- Avoid structural weakness
- Print without supports

---

# PART 2 — FILES & SETUP (NO MIXING)

## 3. Files You Should Have

You should have exactly **two assets**:

1. Geometry ZIP:
```
sociail_assistant_enclosure_v1_2_FULL_W55_negative_cutouts.zip
```

2. This runbook

Delete everything else.

---

## 4. Workspace Setup

Before you print anything:

- Clean build plate
- Confirm nozzle is clean
- Ensure filament is dry
- Clear enough table space for parts + assembly

Hardware work is **physical** — clutter causes mistakes.

---

# PART 3 — BAMBU STUDIO: THE HEART OF THE PROCESS

## 5. Why Negative Parts Matter

You are **not** editing CAD.
You are **subtracting volumes at slice time**.

This lets you:
- Adjust openings without re‑exporting
- Iterate fast
- Avoid CAD rabbit holes

If you forget to mark a part as **Negative**, you will ruin the print.

---

## 6. TOP SHELL — HERO PART (DO THIS SLOWLY)

### 6.1 Import
- Import: `sociail_assistant_bar_top_v1_2_W55.stl`

### 6.2 Add Negative Parts (in this order)
1. LED window
2. Button hole
3. Optional screw holes

Right‑click each → **Set as Negative Part**

### 6.3 Visual Check (DO NOT SKIP)
Rotate the model:
- LED window should fully cut through roof
- Button hole should be centered
- No thin walls (<1.2 mm) remain

If anything looks odd — stop.

---

## 7. BOTTOM SHELL — FUNCTIONAL PART

### 7.1 Import
- Import: `sociail_assistant_bar_bottom_v1_2_W55.stl`

### 7.2 Add Negative Parts
1. USB‑C opening
2. Mic holes
3. Speaker holes
4. Optional screw holes

### 7.3 Visual Check
- USB opening centered on end
- No interference with snap tabs
- Speaker holes fully penetrate wall

---

# PART 4 — PRINTING (THIS IS WHERE MOST PEOPLE FAIL)

## 8. Orientation Rules (NON‑NEGOTIABLE)

**Top shell**
- Flip upside‑down
- Outer surface against bed

**Bottom shell**
- Upright
- Cavity facing up

If you violate this, surface quality will suffer.

---

## 9. Print Profiles (Pick One)

### 9.1 Iteration Print
Use when validating fit.

- Layer height: 0.12 mm
- Walls: 4
- Infill: 12% gyroid
- Supports: OFF
- Speed: default

### 9.2 Hero Print
Use when result matters.

- Layer height: 0.08 mm
- Walls: 4–5
- Top layers: 7–8
- Seam: Aligned (underside edge)
- Supports: OFF

Do not rush hero prints.

---

# PART 5 — AFTER PRINTING (CRITICAL)

## 10. First Inspection (Before Assembly)

Check:
- No warping
- No stringing in LED window
- Snap tabs intact
- USB opening clean

If defects exist, **reprint**. Do not “hope it’s fine”.

---

## 11. Assembly — FIRST CONTACT

### 11.1 Dry Fit
- Align top and bottom
- Press evenly
- Listen for snap engagement

### 11.2 What You Want to Feel
- Resistance → click → seated
- Seam even all around

If it creaks or bows — stop.

---

## 12. Fasteners (Optional)

Only add screws if:
- You will open it repeatedly
- You travel with it
- It’s handled by many people

Suggested:
- M2.5 × 6–8 mm self‑tapping
- Heat‑set inserts only if needed

---

# PART 6 — POST‑PROCESSING (THIS IS THE MAGIC)

## 13. Why This Matters
Raw prints scream “prototype”.
Post‑processing whispers “product”.

---

## 14. Demo‑Grade Finish Recipe

1. Sand lightly (400 grit)
2. Sand again (600)
3. Final pass (800)
4. Filler primer (1–2 coats)
5. Matte or satin spray

Let cure fully before touching.

---

# PART 7 — FINAL VALIDATION

## 15. The Hand‑Off Test

Hand it to someone.
Do **not** explain it.

If they:
- Rotate it naturally
- Don’t comment on seams
- Ask what it does

You succeeded.

---

## 16. Iteration Discipline

Change **one thing at a time**.
Reprint **only the affected part**.
Never redesign everything.

---

## 17. Mental Model (Read This Last)

You are not learning 3D printing.
You are learning **physical thinking**.

This skill compounds.

Print → hold → learn → repeat.
