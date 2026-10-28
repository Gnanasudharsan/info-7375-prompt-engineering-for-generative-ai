# TYPECHECK.md — GATE T

Reel: `cuegate-pitch`  |  Checked: 2026-10-14T19:22  |  Overall: PASS  |  Beats checked: 16  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B00 | pantry | — | no video | SKIP | — |
| B01 | manim | light | min-size §8.1: min text-run height 42px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 208px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 56px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 194px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B07A | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B07B | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 52px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 462px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 70px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BOUT | bookend | dark | min-size §8.1: min text-run height 45px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 15 | 0 |
| overflow §8.2 | 15 | 0 |
| contrast §8.3 | 15 | 0 |
| contrast-local §8.3b | 15 | 0 |
| bbox-overlap §8.6b | 15 | 0 |
| card-clip §8.13 | 15 | 0 |
| kerning §8.4 | 14 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
