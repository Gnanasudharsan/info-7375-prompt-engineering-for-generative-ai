# TYPECHECK.md — GATE T

Reel: `rithika-reallocation-mode-video`  |  Checked: 2026-10-21T18:36  |  Overall: PASS  |  Beats checked: 8  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B01 | manim | light | min-size §8.1: min text-run height 72px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 93px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 58px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| BOUT | manim | light | min-size §8.1: min text-run height 68px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 8 | 0 |
| overflow §8.2 | 8 | 0 |
| contrast §8.3 | 8 | 0 |
| contrast-local §8.3b | 8 | 0 |
| bbox-overlap §8.6b | 8 | 0 |
| card-clip §8.13 | 8 | 0 |
| kerning §8.4 | 8 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
