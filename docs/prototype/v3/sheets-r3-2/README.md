# v3 R3.2 Sheet Files

Single-file plate STLs for quick Bambu Studio imports.

## Files
- `r3-2-loose-pair-sheet.stl`: top+bottom print shells for r3-2-loose
- `r3-2-mid-pair-sheet.stl`: top+bottom print shells for r3-2-mid
- `r3-2-tight-pair-sheet.stl`: top+bottom print shells for r3-2-tight
- `r3-2-loose-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-2-loose
- `r3-2-mid-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-2-mid
- `r3-2-tight-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-2-tight
- `r3-2-abc-6up-sheet.stl`: loose/mid/tight top+bottom together (6 parts)
- `r3-2-abc-6up-kit-sheet.stl`: loose/mid/tight top+bottom + 24mm button plungers/bezel guards (12 parts)
- `r3-2-abc-buttons-6up-sheet.stl`: three 24mm plungers + three 24mm bezels only (6 parts)
- `r3-2-default-cases-sheet.stl`: default case plate for multi-material workflow (alias of `r3-2-abc-6up-sheet.stl`)
- `r3-2-default-buttons-sheet.stl`: default button plate for multi-material workflow (alias of `r3-2-abc-buttons-6up-sheet.stl`)
- `r3-2-case-a-sheet.stl`: case material-test pair A (maps to r3-2-loose)
- `r3-2-case-b-sheet.stl`: case material-test pair B (maps to r3-2-mid)
- `r3-2-case-c-sheet.stl`: case material-test pair C (maps to r3-2-tight)
- `r3-2-button-a-sheet.stl`: button material-test pair A (24mm plunger + bezel)
- `r3-2-button-b-sheet.stl`: button material-test pair B (24mm plunger + bezel)
- `r3-2-button-c-sheet.stl`: button material-test pair C (24mm plunger + bezel)
- `r3-2-abc-6up-sheet-screws.stl`: loose/mid/tight top+bottom screw-hole set (6 parts)
- `r3-2-abc-bottoms-3up-sheet.stl`: loose/mid/tight bottoms only (3 parts)
- `r3-2-abc-bottoms-3up-sheet-screws.stl`: loose/mid/tight bottoms only with screw holes (3 parts)

## Notes
- Pair sheets are intended for one-variant print jobs.
- Default orientation flips top shells and button parts upside down to reduce top-surface fuzz/stringing.
- Screw pair sheets use `shell-*-print-screws.stl` sources.
- 6-up and 3-up sheets are rotated in-plane for better 256-class bed fit.
- `r3-2-abc-6up-kit-sheet.stl` adds three 24mm plungers and three 24mm bezels for one-cycle A/B/C print runs.
- Default material-first flow: import `r3-2-default-cases-sheet.stl` + `r3-2-default-buttons-sheet.stl` as separate plates, then assign different filaments.
- For AMS material trials with less purge, use `r3-2-abc-6up-sheet.stl` (cases) plus `r3-2-abc-buttons-6up-sheet.stl` (buttons) on separate plates.
- A/B/C mapping: `A=r3-2-loose`, `B=r3-2-mid`, `C=r3-2-tight`.
- Fast AMS workflow: import `r3-2-case-a/b/c-sheet.stl` and `r3-2-button-a/b/c-sheet.stl` together, then assign filament by object name.
- In Bambu Studio, keep as-is or use "Split to Objects" for per-part controls.
