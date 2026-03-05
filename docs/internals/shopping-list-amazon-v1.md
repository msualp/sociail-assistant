# Sociail Assistant v2/v3 Shopping List (Amazon)

Aligned to current prototypes:
- v2/v3 snap-shell variants (`r3-loose`, `r3-mid`, `r3-tight`)
- 24mm button module (`prototype/modules/button-module-22-24-v1/`)
- XIAO ESP32S3 Sense internals path

## 1) Buy-Now Core (build 1 device + 1 backup board)

| Item | Qty | Amazon Link | Why it matches current design |
|---|---:|---|---|
| Seeed Studio XIAO ESP32S3 Sense | 2 | https://www.amazon.com/dp/B0C69FFVHH | Main MCU + built-in mic path in internals doc |
| WS2812B 5V LED strip (60 LED/m) | 1 | https://www.amazon.com/dp/B088BPGMXB | Status LED strip for top shell window |
| LiPo 3.7V ~1000mAh | 2 | https://www.amazon.com/dp/B0BNX2GWMS | Battery target matches fit/power guidance |
| MagSafe adhesive ring | 1 pack | https://www.amazon.com/dp/B09TQYTCC1 | Matches MagSafe recess assumptions |
| MAX17048 fuel gauge module | 1 | https://www.amazon.com/dp/B0B8J1V9QG | Recommended battery percentage path |
| 26AWG silicone wire | 1 | https://www.amazon.com/dp/B089D11WVN | Flexible internal wiring |
| 6x6mm tactile momentary button (through-hole) | 1 pack | https://www.amazon.com/s?k=6x6mm+tactile+switch+momentary | Electrical switch under 24mm plunger |
| 1.25mm battery pigtail / JST lead set | 1 pack | https://www.amazon.com/s?k=1.25mm+jst+battery+pigtail | Adapts LiPo leads to BAT pad workflow |

## 2) Printing Materials (4-spool friendly)

| Item | Qty | Amazon Link | Use |
|---|---:|---|---|
| TPU 95A filament (1.75mm) | 1 | https://www.amazon.com/s?k=TPU+95A+1.75mm+filament | 24mm plungers only |
| PLA+ / matte PLA filament | 2 | https://www.amazon.com/s?k=PLA+matte+filament+1.75mm | Case shells + bezels (A/B comparison) |
| PETG filament | 1 | https://www.amazon.com/s?k=PETG+filament+1.75mm | Tougher case/bezel comparison |

Suggested AMS assignment for first run:
- Spool 1: PLA matte (Case A)
- Spool 2: PLA+ or second matte color (Case B)
- Spool 3: PETG (Case C or bezels)
- Spool 4: TPU 95A (plungers; external spool feed is often more reliable than AMS)

## 3) Button Feel Tuning (recommended)

| Item | Qty | Amazon Link | Use |
|---|---:|---|---|
| 1mm adhesive foam dots | 1 pack | https://www.amazon.com/s?k=1mm+adhesive+foam+dots | Soften plunger feel + noise |
| 6mm x 2mm silicone bumper dots | 1 pack | https://www.amazon.com/dp/B016GXAZOA | Alternate elastomer nub |

## 4) Optional / Fallback Electronics

| Item | Qty | Amazon Link | When to buy |
|---|---:|---|---|
| INMP441 I2S mic | 1 | https://www.amazon.com/dp/B09B9HGVDP | Only if onboard Sense mic path is not robust |
| Mini slide power switch (SPDT) | 1 pack | https://www.amazon.com/s?k=mini+slide+switch+SPDT | True hardware power-off option |
| 220k resistor kit + 0.1uF caps | 1 kit | https://www.amazon.com/s?k=220k+resistor+0.1uF+capacitor+kit | Battery divider fallback if no MAX17048 |

## 5) Optional for Screw-Hole Shell Variants

Current screw-hole meshes use ~3.0mm through holes.

| Item | Qty | Amazon Link | Notes |
|---|---:|---|---|
| M3 machine screw assortment (6-12mm) | 1 kit | https://www.amazon.com/s?k=M3+machine+screw+assortment | For `*-screws.stl` variants |
| M3 hex nuts assortment | 1 kit | https://www.amazon.com/s?k=M3+hex+nuts+assortment | Through-bolt closure option |

## 6) First-Time Build Tools (if needed)

| Item | Qty | Amazon Link |
|---|---:|---|
| Temperature-controlled soldering iron kit | 1 | https://www.amazon.com/s?k=temperature+controlled+soldering+iron+kit |
| 63/37 solder wire + no-clean flux pen | 1 each | https://www.amazon.com/s?k=63%2F37+solder+wire+no+clean+flux+pen |
| Flush cutters + wire stripper | 1 each | https://www.amazon.com/s?k=flush+cutters+wire+stripper+electronics |
| Heat-shrink tubing assortment | 1 | https://www.amazon.com/s?k=heat+shrink+tubing+assortment |
| Digital multimeter | 1 | https://www.amazon.com/s?k=digital+multimeter |

## 7) Order Notes (important)

- XIAO ESP32S3 Sense battery wiring is BAT pad based; do not assume connector plug compatibility.
- For button safety/anti-press behavior, print bezels in rigid PLA/PETG, not TPU.
- For your new A/B/C material workflow, print:
  - `r3-case-a/b/c-sheet.stl`
  - `r3-button-a/b/c-sheet.stl`
