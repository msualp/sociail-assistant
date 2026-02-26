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

---

# PART 8 — v2.0 CURVED SURFACE HANDLING (NEW)

The v2.0 design uses a **pill/capsule form** with continuous rounded surfaces. This section covers specific techniques for printing and finishing curved geometry.

---

## 18. Understanding Curved Surface Challenges

### 18.1 The Stair-Step Problem

FDM printing builds objects in horizontal layers.
On vertical surfaces: layers are invisible.
On curved/angled surfaces: layers create visible "stairs".

```
    Vertical Surface       Curved Surface
    ────────────────       ────────────────
    │████████████│         ╱███████╲
    │████████████│        ╱█████████╲
    │████████████│       ╱███████████╲
    │████████████│      ╱█████████████╲

    Layers invisible      Layers visible
```

### 18.2 The 45° Rule

- Surfaces < 45° from horizontal: stair-stepping visible
- Surfaces > 45° from vertical: layer lines less visible

The v2.0 pill shape has gentle curves (large radii) which help minimize this effect.

---

## 19. Layer Height Optimization for Pill Shape

### 19.1 Why Layer Height Matters More for v2.0

| Layer Height | Stair Step Size | Visibility |
|--------------|-----------------|------------|
| 0.20 mm | Large | Very visible |
| 0.12 mm | Medium | Acceptable |
| 0.08 mm | Small | Minimal |
| 0.04 mm | Tiny | Nearly invisible |

**Recommendation**: Use 0.08 mm for hero prints on v2.0.

### 19.2 Trade-offs

| Layer Height | Print Time | Quality |
|--------------|------------|---------|
| 0.12 mm | 1× (baseline) | Good for iteration |
| 0.08 mm | 1.5× | Production quality |
| 0.04 mm | 3× | Only for final demos |

### 19.3 When to Use Each

- **0.12 mm**: Fit checks, mechanism testing
- **0.08 mm**: Final prototypes, photography
- **0.04 mm**: Competition entries, investor samples

---

## 20. Printing the Pill Shape Without Supports

### 20.1 Design Strategy (Already Built Into v2.0)

The v2.0 design is **specifically crafted** to print support-free:

1. **Large radii** (17.5 mm ends) create gentle slopes
2. **Shell split at 60%** avoids severe overhangs
3. **No undercuts** on exterior surfaces
4. **Internal features** oriented for bridging

### 20.2 Print Orientation Reinforcement

**Top Shell (Hero Part)**
- Print upside-down
- Exterior curve faces build plate
- LED window bridges across (acceptable)
- Button well bridges (acceptable)

**Bottom Shell (Functional Part)**
- Print upright
- USB-C opening on vertical face
- Speaker/mic holes on vertical face
- No overhangs > 45°

### 20.3 Handling Internal Bridges

The LED window and button hole require bridging in the top shell.

**Bridge Settings**:
- Reduce bridge speed to 20–25 mm/s
- Enable bridge fan boost (100%)
- Bridge flow ratio: 95%

If bridging sags:
- Add thin (0.3 mm) sacrificial layer in CAD
- Remove with knife after printing

---

## 21. Sanding Techniques for Maintaining Radii

### 21.1 The Flat Spot Problem

Using flat sanding blocks on curved surfaces creates **flat spots** — areas where the curve is accidentally flattened.

```
    Ideal Curve          After Bad Sanding
    ────────────         ────────────
       ╭───╮                ╭─┬─╮
      ╱     ╲              ╱  │  ╲
     ╱       ╲            ╱   │   ╲

    Smooth               Flat spot visible
```

### 21.2 Tools for Curved Surfaces

| Tool | Use Case | Where to Buy |
|------|----------|--------------|
| **Foam sanding blocks** | General curved surfaces | Hardware store |
| **Sanding sponges** | Complex compound curves | Amazon |
| **Wet/dry sandpaper (loose)** | Wrapping around forms | Hardware store |
| **3D-printed sanding forms** | Match-sanding specific radii | Print yourself |

### 21.3 Technique: The Wrap Method

1. Cut sandpaper to 4" × 2" strip
2. Wrap around foam or sponge
3. Sand in direction of curve (lengthwise on pill)
4. Rotate part, not sanding direction
5. Check against light for flat spots

### 21.4 Technique: Wet Sanding

Wet sanding is **essential** for curved surfaces:
- Water lubricates, preventing gouges
- Slurry fills minor scratches
- Cooler cutting, less material removal

**Process**:
1. Dip sandpaper in water bowl
2. Sand with light pressure
3. Wipe and inspect frequently
4. Re-wet every 30 seconds

---

## 22. Surface Quality Inspection

### 22.1 The Raking Light Test

Hold part at arm's length.
Shine light at shallow angle (10–15° from surface).
Look for:
- Layer lines (horizontal shadows)
- Flat spots (reflections change abruptly)
- Scratches (cross-hatched shadows)

### 22.2 The Fingernail Test

Run fingernail across surface perpendicular to layer lines.
If you feel ridges → more sanding needed.
If smooth → ready for primer.

### 22.3 The Highlight Test (After Primer)

Under overhead light, rotate part slowly.
Watch highlight reflection move across surface.
- Smooth curve = highlight moves evenly
- Flat spot = highlight jumps or stretches
- Ripple = highlight wavers

---

## 23. Advanced Finishing: Apple-Style Gloss

If you want the high-gloss finish typical of Apple products:

### 23.1 Process Overview

1. Sand to 1000 grit
2. Filler primer (2 coats)
3. Wet sand 600
4. Spot putty defects
5. Sand putty 800
6. High-build primer (2 coats)
7. Wet sand 1000
8. Color coat (2–3 coats)
9. Clear coat (3–4 coats of 2K automotive clear)
10. Wet sand 2000
11. Polish with rubbing compound
12. Final polish with finishing compound

### 23.2 Time Investment

This process takes **4–6 hours** per part with cure times.
Only do this for final demo units.

### 23.3 Safety Note

2K automotive clear contains isocyanates.
**Use respirator** (not just dust mask).
Work in well-ventilated area.

---

## 24. Common v2.0 Printing Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Visible layer lines on curve | Layer height too high | Use 0.08 mm |
| Flat spots after sanding | Flat sanding block | Use foam/sponge |
| Seam visible on curve | Seam on visible surface | Move seam to parting line |
| Rough texture on curve | Print speed too high | Reduce outer wall to 40 mm/s |
| Bridging sag in LED window | Bridge settings wrong | Slow to 20 mm/s, 100% fan |
| Snap-fits too tight | No print shrink compensation | Add 0.1 mm clearance |
| Parting line gap uneven | Shells warped | Check bed adhesion, cooling |

---

## 25. v2.0 Success Criteria

When you've succeeded:

- [ ] Part feels like a pebble (smooth, no edges)
- [ ] No visible layer lines under raking light
- [ ] Curve flows continuously (no flat spots)
- [ ] Seam nearly invisible
- [ ] USB-C pocket feels intentional
- [ ] LED window aligned and clean
- [ ] Snap engagement confident
- [ ] Someone asks "where did you buy this?"

---

## 26. Iteration Workflow for v2.0

1. **First print**: 0.12 mm, test fit
2. **Fix issues**: Adjust parameters, reprint affected shell only
3. **Second print**: 0.12 mm, verify fixes
4. **Hero print**: 0.08 mm, full post-processing
5. **Validate**: Hand-off test, raking light test
6. **Refine**: Only if defects found

Average iterations to "good enough": 2–3
Average iterations to "excellent": 4–5
