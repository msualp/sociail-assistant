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
