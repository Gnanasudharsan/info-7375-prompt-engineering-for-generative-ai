# TYPECHECK.md — GATE T

Reel: `cite-and-seek-pitch`  |  Checked: 2026-10-12T20:43  |  Overall: PASS  |  Beats checked: 23  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | manim | light | min-size §8.1: min text-run height 96px >= floor 41px | PASS | — |
| B00 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| BDEFS | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 46px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B07B | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B09B | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B16 | manim | light | min-size §8.1: min text-run height 51px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| BHTF | bookend | light | min-size §8.1: hand-drawn pattern (ClaudeComposerAsk) — §8.1 hachure/crossbar fragments ar… | PASS | — |
| BOUT | manim | light | min-size §8.1: min text-run height 83px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 1 | 0 |
| min-size §8.1 | 23 | 0 |
| overflow §8.2 | 23 | 0 |
| contrast §8.3 | 23 | 0 |
| contrast-local §8.3b | 23 | 0 |
| bbox-overlap §8.6b | 23 | 0 |
| card-clip §8.13 | 23 | 0 |
| kerning §8.4 | 21 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
