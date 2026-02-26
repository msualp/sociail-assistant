# Sociail Assistant v2.0 Design Specification
**Modern Pill-Form Enclosure with Apple-Inspired Aesthetics**

This document is the **complete design specification** for the v2.0 enclosure redesign. It provides all measurements, tolerances, and guidance needed to create the 3D models in Fusion 360.

---

## 1. Design Philosophy

### 1.1 Form Language
- **Pill/capsule shape** — stadium profile with rounded ends
- **Unified surfaces** — continuous curves, no hard transitions
- **G2 curvature continuity** — smooth highlight reflections
- **Minimal seam reveal** — tight parting line (0.1–0.15mm gap)
- **Premium proportions** — 60/40 top/bottom visual split

### 1.2 Inspiration References
- **Amazon Echo Auto** — compact oval form factor
- **Apple Magic Mouse / AirPods case** — radius language, surface quality
- **Premium consumer electronics** — recessed features, subtle details

### 1.3 Design Goals
- Feels intentional, not experimental
- Comfortable in hand (pocketable)
- Looks like a finished product, not a prototype
- Printable without supports on Bambu Lab P1S

---

## 2. Overall Dimensions

### 2.1 External Envelope

| Dimension | Value | Tolerance | Notes |
|-----------|-------|-----------|-------|
| Length (X) | 85 mm | ±0.2 mm | Matches product spec |
| Width (Y) | 35 mm | ±0.2 mm | Practical for components |
| Height (Z) | 14 mm | ±0.2 mm | Slim profile |

**Volume**: ~41,650 mm³ (77% smaller than v1.2)

### 2.2 Profile Geometry

**Plan View (Top-Down)**
```
    ┌─────────────────────────────────┐
    │  R=17.5mm                       │  R=17.5mm
    │    ╭───────────────────────╮    │
    │   (                         )   │
    │    ╰───────────────────────╯    │
    └─────────────────────────────────┘
         ←────── 85 mm ──────→

    Stadium shape: Rectangle (50mm) + Semicircles (R=17.5mm) on each end
```

**Front View (End-On)**
```
         ←─── 35 mm ───→
    ┌───────────────────────┐
    │                       │  ↑
    │  ╭─────────────────╮  │  │
    │ (                   ) │  14 mm
    │  ╰─────────────────╯  │  │
    │                       │  ↓
    └───────────────────────┘

    Stadium profile: Rectangle (7mm H) + Semicircles (R=17.5mm) on sides
```

### 2.3 Corner and Edge Radii

| Feature | Radius | Type |
|---------|--------|------|
| End radii (plan view) | 17.5 mm | Full semicircle |
| Side radii (front view) | 17.5 mm | Full semicircle |
| Top/bottom edge fillets | 3–5 mm | G2 continuous |
| Parting line edge | 1.5 mm | Smooth transition |

---

## 3. Shell Architecture

### 3.1 Two-Piece Design

| Component | Z Range | Purpose |
|-----------|---------|---------|
| Top Shell | 8.4 → 14 mm | Hero surface (LED, button) |
| Bottom Shell | 0 → 8.4 mm | Functional (USB-C, speaker, mic) |

**Split Ratio**: 60% bottom / 40% top (visual balance)

### 3.2 Wall Thickness

| Location | Thickness | Notes |
|----------|-----------|-------|
| Exterior walls | 2.6 mm | Print-reliable |
| Top roof | 2.6 mm | LED diffuser shelf area: 2.1 mm |
| Bottom floor | 2.6 mm | Standard |
| Internal ribs | 1.5 mm | Where needed |

### 3.3 Alignment Features

**Tongue-and-Groove Lip**
```
    Top Shell (interior edge)
    ───────╮
           │ 1.0 mm step
    ───────╯

    Bottom Shell (exterior lip)
    ───────╭───
           │ 1.0 mm lip height
    ───────╯
           ↔ 1.0 mm lip width
```

- Lip height: 1.0 mm
- Lip width: 1.0 mm
- Clearance: 0.1 mm (total gap = 0.1–0.15 mm)

### 3.4 Snap-Fit System

**4x Cantilever Snaps** — one at each corner arc

| Parameter | Value |
|-----------|-------|
| Snap width | 4 mm |
| Snap length | 8 mm |
| Deflection | 0.3 mm |
| Engagement depth | 0.8 mm |
| Draft angle | 3° |
| Location | Bottom shell, interior, at ±30° from X-axis |

---

## 4. Feature Specifications

### 4.1 USB-C Port (Left End, -X Face)

**Recessed Pocket Design**
```
    Side View (looking at left end)

         ┌─────────────────┐
         │                 │
         │   ┌─────────┐   │  ← Recess pocket
         │   │ ○═════○ │   │  ← USB-C opening
         │   └─────────┘   │
         │                 │
         └─────────────────┘
```

| Dimension | Value | Notes |
|-----------|-------|-------|
| **Pocket** | | |
| Width | 14 mm | Finger access |
| Height | 8 mm | Vertical clearance |
| Depth | 3 mm | Recessed aesthetic |
| Corner radius | 1.5 mm | Softened edges |
| **Opening** | | |
| Width | 9.5 mm | USB-C + 0.5 mm clearance |
| Height | 3.5 mm | USB-C + 0.3 mm clearance |
| Corner radius | 1.0 mm | Standard USB-C shape |
| **Entry chamfer** | 0.5 mm × 45° | Plug guidance |
| **Z position** | 5.0 mm from bottom | Centered vertically |
| **Y position** | Centered | On Y-axis |

### 4.2 LED Light Bar (Top Surface)

**Pill-Shaped Window**
```
    Top View

              ←──── 55 mm ────→
         ╭═══════════════════════╮
        (                         )  ← 8 mm wide
         ╰═══════════════════════╯
              R=4mm        R=4mm

    ← 12 mm offset toward front (+Y) from center
```

| Dimension | Value | Notes |
|-----------|-------|-------|
| Length | 55 mm | Scaled from 75 mm |
| Width | 8 mm | Visible aperture |
| End radius | 4 mm | Pill-shaped ends |
| **Recess** | 0.5 mm | Below top surface |
| **Diffuser shelf** | 2.1 mm thick | For acrylic diffuser insert |
| X position | Centered on X-axis | |
| Y offset | +12 mm from center | Toward front |
| Edge fillet | 1.0 mm | Softened opening |

### 4.3 Button Well (Top Surface)

**Tactile Depression**
```
    Section View

    ──────╲___________╱──────  ← 1.5 mm depression
              │   │
              │   │  ← 6 mm through hole
              │   │
```

| Dimension | Value | Notes |
|-----------|-------|-------|
| Well diameter | 12 mm | Large touch target |
| Well depth | 1.5 mm | Subtle depression |
| Through hole | 6 mm diameter | Switch actuation |
| Edge radius | 2.0 mm | Soft well edges |
| X position | Centered under LED midpoint | |
| Y position | Centered on Y-axis | |

### 4.4 Microphone Array (Front Face, +Y, Upper)

**Arc Pattern**
```
    Front View

         ○   ○   ○   ○   ○      ← 5 holes in arc

         Z ≈ 10 mm from bottom
```

| Dimension | Value | Notes |
|-----------|-------|-------|
| Number of holes | 5 | Scaled from 7 |
| Hole diameter | 1.2 mm | Acoustic transparency |
| Spacing | 4 mm center-to-center | |
| Pattern width | 16 mm total | |
| Z position | 10 mm from bottom | Upper third |
| X position | Centered on X-axis | |
| Through depth | Full wall (2.6 mm) | |

### 4.5 Speaker Grill (Front Face, +Y, Lower)

**Grid Pattern**
```
    Front View

         ═  ═  ═  ═  ═
         ═  ═  ═  ═  ═      ← 3 rows × 5 columns
         ═  ═  ═  ═  ═

         Z ≈ 4 mm from bottom
```

| Dimension | Value | Notes |
|-----------|-------|-------|
| Pattern | 3 rows × 5 columns | 15 slots |
| Slot size | 2 mm × 4 mm | Stadium shape |
| Slot corner radius | 1 mm | Rounded ends |
| H spacing | 3 mm center-to-center | |
| V spacing | 2.5 mm center-to-center | |
| Grid size | 12 mm W × 5 mm H | Total area |
| Z position | 4 mm from bottom | Lower third |
| X position | Centered on X-axis | |
| Edge fillet | 0.3 mm per slot | Prevents sharp edges |
| Through depth | Full wall (2.6 mm) | |

---

## 5. Coordinate System Reference

```
    Isometric View

                    Z (up)
                    ↑
                    │    Y (front)
                    │   ╱
                    │  ╱
                    │ ╱
    ────────────────┼─────────→ X (length)
                   ╱│
                  ╱ │
                 ╱  │
```

| Axis | Direction | Reference |
|------|-----------|-----------|
| +X | Right | LED side |
| -X | Left | USB-C side |
| +Y | Front | Mic + Speaker side |
| -Y | Back | Solid wall |
| +Z | Up | Top (hero) surface |
| -Z | Down | Bottom surface |

**Origin**: Geometric center of bounding box at Z=0 (bottom surface)

---

## 6. Fusion 360 Modeling Workflow

### 6.1 Parametric Setup

Create User Parameters in Fusion 360:

```
Name                    Value       Unit
────────────────────────────────────────
overall_length          85          mm
overall_width           35          mm
overall_height          14          mm
end_radius              17.5        mm
edge_fillet             4           mm
wall_thickness          2.6         mm
split_height            8.4         mm
lip_width               1           mm
lip_height              1           mm
lip_clearance           0.1         mm
```

### 6.2 Base Body Creation

**Step 1: Profile Sketch (XY Plane)**
1. Create rectangle: 50 mm × 35 mm (centered)
2. Add semicircles at each end: R = 17.5 mm
3. Trim to create stadium shape (85 mm × 35 mm)

**Step 2: Extrude**
- Height: `overall_height` (14 mm)
- Direction: +Z

**Step 3: Edge Fillets**
- Select all vertical edges
- Radius: `edge_fillet` (4 mm)
- Type: G2 (curvature continuous) if available

**Step 4: Shell**
- Select bottom face
- Thickness: `wall_thickness` (2.6 mm)
- Direction: Inside

### 6.3 Shell Split

**Step 5: Split Body**
1. Create offset plane at Z = `split_height` (8.4 mm)
2. Use Split Body tool
3. Result: Top shell + Bottom shell as separate bodies

**Step 6: Add Alignment Lip**
- On bottom shell: extrude lip at parting edge
  - Width: `lip_width` (1.0 mm)
  - Height: `lip_height` (1.0 mm)
- On top shell: create matching groove
  - Add `lip_clearance` (0.1 mm)

### 6.4 Snap-Fit Features

**Add to Bottom Shell (4 locations)**:
1. Sketch cantilever beam: 4 mm W × 8 mm L
2. Add hook geometry: 0.8 mm engagement
3. Pattern at ±30° from X-axis (4 corners)

### 6.5 Feature Cutouts

Model each cutout as a separate body, then Boolean subtract OR export as negative STL.

**Recommended: Export as separate negative STLs** for flexibility in Bambu Studio.

### 6.6 Export Settings

| Parameter | Value |
|-----------|-------|
| Format | Binary STL |
| Units | Millimeters |
| Refinement | High |
| Surface deviation | 0.01 mm |

---

## 7. File Naming Convention

```
sociail_assistant_enclosure_v2_0_W35/
│
├── Main Parts
│   ├── sociail_assistant_pill_top_v2_0_W35.stl
│   └── sociail_assistant_pill_bottom_v2_0_W35.stl
│
├── Negative Cutouts
│   ├── neg_usb_c_left_recess_v2_0.stl
│   ├── neg_led_window_rounded_v2_0.stl
│   ├── neg_button_well_v2_0.stl
│   ├── neg_mic_perforations_v2_0.stl
│   ├── neg_speaker_grill_v2_0.stl
│   └── neg_screw_bosses_4x_v2_0.stl (optional)
│
├── Source
│   ├── sociail_assistant_v2_0.f3d
│   └── sociail_assistant_v2_0.step
│
└── README.txt
```

---

## 8. Material Recommendations

### 8.1 Prototype Material

| Material | Use Case | Notes |
|----------|----------|-------|
| PLA+ | Iteration prints | Best surface quality |
| PETG | Demo prints | Slightly tougher |
| PLA Matte | Hero prints | Hides layer lines better |

**Avoid ABS/ASA** until geometry is locked (warping risk).

### 8.2 Target Production Colors

| Color | Description | Reference |
|-------|-------------|-----------|
| Space Gray | Dark gunmetal gray | Apple Space Gray |
| Arctic White | Bright clean white | Apple White |

---

## 9. Tolerance and Fit Guidelines

### 9.1 Clearances

| Interface | Clearance | Notes |
|-----------|-----------|-------|
| Shell seam | 0.1–0.15 mm | Tight visual fit |
| Snap engagement | 0.8 mm | Secure hold |
| USB-C opening | 0.3–0.5 mm | Easy insertion |
| Button through-hole | 0.2 mm | Smooth actuation |

### 9.2 Print Shrinkage Compensation

PLA typically shrinks ~0.2–0.5%. For critical fits:
- Increase holes by 0.2 mm
- Test fit with actual USB-C connector

---

## 10. Comparison: v1.2 vs v2.0

| Aspect | v1.2 | v2.0 |
|--------|------|------|
| Dimensions | 150 × 55 × 22 mm | 85 × 35 × 14 mm |
| Form | Rectangular bar | Pill/capsule |
| Edges | Sharp/minimal fillets | 4mm continuous radii |
| Volume | ~181,500 mm³ | ~41,650 mm³ |
| Split ratio | 50/50 | 60/40 |
| USB-C | Flat cutout | Recessed pocket |
| LED window | Rectangle 75mm | Pill-shape 55mm |
| Button | Simple hole | Tactile well |
| Aesthetic | Functional | Apple-inspired premium |

---

## 11. Validation Checklist

Before approving design for iteration prints:

- [ ] Overall dimensions within spec (85 × 35 × 14 mm ±0.2)
- [ ] Wall thickness ≥ 2.6 mm everywhere
- [ ] No overhangs > 45° (support-free printing)
- [ ] USB-C pocket dimensions verified
- [ ] LED window centered and offset correctly
- [ ] Button well centered under LED
- [ ] Mic holes evenly spaced
- [ ] Speaker grill pattern complete
- [ ] Snap-fits at correct locations
- [ ] Alignment lip geometry correct
- [ ] No thin walls < 1.2 mm
- [ ] STL export without errors

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2025-01-28 | Initial v2.0 specification (pill form) |
