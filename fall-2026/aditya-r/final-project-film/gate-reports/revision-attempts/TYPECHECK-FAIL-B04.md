# TYPECHECK.md — GATE T

Reel: `daythread-pitch-film`  |  Checked: 2026-10-25T15:05  |  Overall: **FAIL**  |  Beats checked: 18  |  FAILs: 1

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B00 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 48px >= floor 41px | PASS | — |
| B04 | manim | light | bbox-overlap §8.6b: text-run bbox overlap 100% >= 10% — two labels are printing on top of … | **FAIL** | Separate label positions — two text elements overlap |
| B05 | manim | light | min-size §8.1: min text-run height 54px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 296px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 105px >= floor 41px | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 48px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 63px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px | PASS | — |
| BOUT | manim | light | min-size §8.1: min text-run height 53px >= floor 41px (individual-char fallback at 2×) | PASS | — |

---

## Failures requiring action before cut

### B04 (manim)
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(430,616)–(2086,1408) ∩ blob@(1579,742)–(1976,792) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(430,616)–(2086,1408) h=792px (15.8×med)
- **Fix:** Separate label positions — two text elements overlap

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 18 | 0 |
| overflow §8.2 | 18 | 0 |
| contrast §8.3 | 18 | 0 |
| contrast-local §8.3b | 18 | 0 |
| bbox-overlap §8.6b | 18 | 1 |
| card-clip §8.13 | 18 | 0 |
| kerning §8.4 | 18 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
