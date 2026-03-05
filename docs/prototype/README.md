# Prototype Directory

This directory is organized by hardware generation.

## Structure
- `v1/` legacy bar form factor (W55)
- `v2/` pill form factor (W35) with base and snap-tuned variants
- `v3/` MagSafe form factor with draft and polished iterations

## Modules
- `modules/button-module-22-24-v1/`: 24mm-default plunger/bezel/cutout button module

## Naming
- Main shells: `shell-top.stl`, `shell-bottom.stl`
- Direct-print shells: `shell-top-print*.stl`, `shell-bottom-print*.stl`
- Subtractive parts: `neg-*.stl`
- Build scripts: `scripts/build-assets-*.py`
- Sheet builders: `scripts/build-*-sheets.py`
- Bundle archives: `*.zip`

## v1
- Canonical negatives: `v1/w55-negatives/`
- Print-ready pair: `v1/w55-print-ready/`
- Legacy archives: `v1/zips/`

## v2
- Documentation: `v2/docs/`
- Base geometry: `v2/base/`
- Looser snap tuning: `v2/r2-loose/`
- Tighter snap tuning: `v2/r2-tight/`
- Production polish pass: `v2/r3-mid/`
- R3 A/B snap tuning: `v2/r3-loose/`, `v2/r3-tight/`
- Single-file plates: `v2/sheets/`
- Builders: `v2/scripts/`
- Quick-load bundles: `v2/*.zip`

## v3
- Original draft: `v3/draft/`
- First polished pass: `v3/polished-r1/`
- A/B snap tuning: `v3/r2-loose/`, `v3/r2-tight/`
- Production polish pass: `v3/r3/`
- R3 A/B/C snap tuning: `v3/r3-loose/`, `v3/r3-mid/`, `v3/r3-tight/`
- Internal component-fit variants: `v3/r3-internals-v1/`, `v3/r3-internals-v1-loose/`, `v3/r3-internals-v1-tight/`
- Single-file plates: `v3/sheets/`
- PCB keepout templates: `v3/templates/`
- Builder scripts: `v3/scripts/`
- Quick-load bundles: `v3/*.zip`
