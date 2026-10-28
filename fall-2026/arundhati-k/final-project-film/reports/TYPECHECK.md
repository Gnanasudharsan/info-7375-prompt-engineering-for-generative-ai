# TYPECHECK.md — GATE T

Reel: `coop-sponsor-check-pitch`  |  Checked: 2026-10-25T20:58  |  Overall: PASS  |  Beats checked: 22  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BNAME | bookend | light | min-size §8.1: min text-run height 61px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| BBUILD | bookend | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| BIDEA | bookend | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| BWHAT | manim | light | min-size §8.1: min text-run height 67px >= floor 41px | PASS | — |
| B00 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 72px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 218px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 549px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B05A | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B07A | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B07B | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B09P | manim | light | min-size §8.1: min text-run height 88px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 66px >= floor 41px | PASS | — |
| B11A | manim | light | min-size §8.1: min text-run height 66px >= floor 41px | PASS | — |
| BOUT | bookend | light | min-size §8.1: min text-run height 43px >= floor 41px (individual-char fallback at 2×) | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 22 | 0 |
| overflow §8.2 | 22 | 0 |
| contrast §8.3 | 22 | 0 |
| contrast-local §8.3b | 22 | 0 |
| bbox-overlap §8.6b | 22 | 0 |
| card-clip §8.13 | 22 | 0 |
| kerning §8.4 | 18 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
