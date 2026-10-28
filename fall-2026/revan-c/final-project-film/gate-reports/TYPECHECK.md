# TYPECHECK.md — GATE T

Reel: `remnix-agent-pitch`  |  Checked: 2026-10-25T22:50  |  Overall: PASS  |  Beats checked: 18  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| BPLAIN | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B00 | manim | — | no video | SKIP | — |
| B02 | manim | light | min-size §8.1: min text-run height 97px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 57px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 64px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 41px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 331px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 43px >= floor 41px | PASS | — |
| BOUT | manim | light | min-size §8.1: min text-run height 137px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 17 | 0 |
| overflow §8.2 | 17 | 0 |
| contrast §8.3 | 17 | 0 |
| contrast-local §8.3b | 17 | 0 |
| bbox-overlap §8.6b | 17 | 0 |
| card-clip §8.13 | 17 | 0 |
| kerning §8.4 | 16 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
