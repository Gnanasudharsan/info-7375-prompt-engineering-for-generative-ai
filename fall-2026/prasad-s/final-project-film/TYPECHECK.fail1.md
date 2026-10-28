# TYPECHECK.md — GATE T

Reel: `gistgap-pitch`  |  Checked: 2026-10-10T21:58  |  Overall: **FAIL**  |  Beats checked: 14  |  FAILs: 1

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B01 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B11 | manim | light | bbox-overlap §8.6b: text-run bbox overlap 59% >= 10% — two labels are printing on top of e… | **FAIL** | Separate label positions — two text elements overlap |
| B12 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 75px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### B11 (manim)
- **bbox-overlap §8.6b**: text-run bbox overlap 59% >= 10% — two labels are printing on top of each other: blob@(871,912)–(1888,1559) ∩ blob@(762,1212)–(1997,1695) (59% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(871,912)–(1888,1559) h=647px (9.2×med), blob@(762,1212)–(1997,1695) h=483px (6.9×med)
- **Fix:** Separate label positions — two text elements overlap

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 14 | 0 |
| overflow §8.2 | 14 | 0 |
| contrast §8.3 | 14 | 0 |
| contrast-local §8.3b | 14 | 0 |
| bbox-overlap §8.6b | 14 | 1 |
| card-clip §8.13 | 14 | 0 |
| kerning §8.4 | 14 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
