# v3 Sheet Files

Single-file plate STLs for quick Bambu Studio imports.

## Files
- `r3-loose-pair-sheet.stl`: top+bottom print shells for r3-loose
- `r3-mid-pair-sheet.stl`: top+bottom print shells for r3-mid
- `r3-tight-pair-sheet.stl`: top+bottom print shells for r3-tight
- `r3-loose-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-loose
- `r3-mid-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-mid
- `r3-tight-pair-sheet-screws.stl`: top+bottom screw-hole print shells for r3-tight
- `r3-abc-6up-sheet.stl`: loose/mid/tight top+bottom together (6 parts)
- `r3-abc-6up-sheet-screws.stl`: loose/mid/tight top+bottom screw-hole set (6 parts)
- `r3-internals-v1-abc-6up-sheet.stl`: internals loose/base/tight top+bottom together (6 parts)
- `r3-internals-v1-abc-6up-sheet-screws.stl`: internals loose/base/tight screw-hole set (6 parts)
- `r3-internals-v1-bottoms-3up-sheet.stl`: internals loose/base/tight bottoms only (3 parts)
- `r3-internals-v1-bottoms-3up-sheet-screws.stl`: internals loose/base/tight bottoms only with screw holes (3 parts)

## Notes
- Pair sheets are intended for one-variant print jobs.
- Screw pair sheets use `shell-*-print-screws.stl` sources.
- 6-up sheets are intended for larger beds (roughly 256x256 class).
- 6-up top rows are auto-oriented to reduce support demand.
- For internals fit A/B testing without cantilever warnings, use bottoms-only 3-up sheets.
- In Bambu Studio, you can keep as-is or use "Split to Objects" for per-part controls.
