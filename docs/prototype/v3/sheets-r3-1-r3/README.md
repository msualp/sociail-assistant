# v3 R3.1-r3 Sheet Files

Single-file plate STLs for quick Bambu Studio imports.

## Files
- `r3-1-r3-loose-pair-sheet.stl`: top+bottom print shells for r3-1-r3-loose
- `r3-1-r3-mid-pair-sheet.stl`: top+bottom print shells for r3-1-r3-mid
- `r3-1-r3-tight-pair-sheet.stl`: top+bottom print shells for r3-1-r3-tight
- `r3-1-r3-loose-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-1-r3-loose
- `r3-1-r3-mid-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-1-r3-mid
- `r3-1-r3-tight-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-1-r3-tight
- `r3-1-r3-abc-6up-sheet.stl`: loose/mid/tight top+bottom together (6 parts)
- `r3-1-r3-abc-6up-kit-sheet.stl`: loose/mid/tight top+bottom + 24mm button plungers/bezel guards (12 parts)
- `r3-1-r3-abc-buttons-6up-sheet.stl`: three 24mm plungers + three 24mm bezels only (6 parts)
- `r3-1-r3-default-cases-sheet.stl`: default case plate for multi-material workflow (alias of `r3-1-r3-abc-6up-sheet.stl`)
- `r3-1-r3-default-buttons-sheet.stl`: default button plate for multi-material workflow (alias of `r3-1-r3-abc-buttons-6up-sheet.stl`)
- `r3-1-r3-case-a-sheet.stl`: case material-test pair A (maps to r3-1-r3-loose)
- `r3-1-r3-case-b-sheet.stl`: case material-test pair B (maps to r3-1-r3-mid)
- `r3-1-r3-case-c-sheet.stl`: case material-test pair C (maps to r3-1-r3-tight)
- `r3-1-r3-button-a-sheet.stl`: button material-test pair A (24mm plunger + bezel)
- `r3-1-r3-button-b-sheet.stl`: button material-test pair B (24mm plunger + bezel)
- `r3-1-r3-button-c-sheet.stl`: button material-test pair C (24mm plunger + bezel)
- `r3-1-r3-abc-6up-sheet-screws.stl`: loose/mid/tight top+bottom screw-hole set (6 parts)
- `r3-1-r3-abc-bottoms-3up-sheet.stl`: loose/mid/tight bottoms only (3 parts)
- `r3-1-r3-abc-bottoms-3up-sheet-screws.stl`: loose/mid/tight bottoms only with screw holes (3 parts)

## Notes
- Pair sheets are intended for one-variant print jobs.
- Default orientation flips top shells and button parts upside down to reduce top-surface fuzz/stringing.
- Screw pair sheets use `shell-*-print-screws.stl` sources.
- 6-up and 3-up sheets are rotated in-plane for better 256-class bed fit.
- `r3-1-r3-abc-6up-kit-sheet.stl` adds three 24mm plungers and three 24mm bezels for one-cycle A/B/C print runs.
- Default material-first flow: import `r3-1-r3-default-cases-sheet.stl` + `r3-1-r3-default-buttons-sheet.stl` as separate plates, then assign different filaments.
- For AMS material trials with less purge, use `r3-1-r3-abc-6up-sheet.stl` (cases) plus `r3-1-r3-abc-buttons-6up-sheet.stl` (buttons) on separate plates.
- A/B/C mapping: `A=r3-1-r3-loose`, `B=r3-1-r3-mid`, `C=r3-1-r3-tight`.
- Fast AMS workflow: import `r3-1-r3-case-a/b/c-sheet.stl` and `r3-1-r3-button-a/b/c-sheet.stl` together, then assign filament by object name.
- In Bambu Studio, keep as-is or use "Split to Objects" for per-part controls.
