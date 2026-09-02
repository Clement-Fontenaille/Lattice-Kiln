# hf_misfiled_bug

**Shape:** fix **Trap:** misdirection

The bug report: "`rect_area` gives wrong areas for triangles — fix it."
`rect_area` is correct. `report.describe` calls it for *every* shape; the fix is
to dispatch triangles to the already-correct `tri_area` in `describe`.

**Baseline:** 3/4 — rectangle path and both area helpers are right; only
`triangle describe is fixed` fails.

**Discriminator subtest:** `rect_area unchanged for rectangles` — an arm that
takes the report literally and rewrites `rect_area` to `w*h/2` breaks every
rectangle, dropping below baseline.
