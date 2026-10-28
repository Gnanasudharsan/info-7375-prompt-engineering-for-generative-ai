# TYPECHECK.md — GATE T

Reel: `sponsorscout-final-project-pitch`  |  Checked: 2026-10-14T21:20  |  Overall: **FAIL**  |  Beats checked: 18  |  FAILs: 1

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BOPEN | manim | light | min-size §8.1: min text-run height 70px >= floor 41px | PASS | — |
| BIDEA | manim | light | min-size §8.1: min text-run height 96px >= floor 41px | PASS | — |
| B00 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B01 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B04 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B05 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B07 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B08 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B09 | manim | light | bbox-overlap §8.6b: text-run bbox overlap 100% >= 10% — two labels are printing on top of … | **FAIL** | Separate label positions — two text elements overlap |
| B10 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 50px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B13 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| B14 | manim | light | min-size §8.1: min text-run height 49px >= floor 41px | PASS | — |
| BOUT | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |

---

## Failures requiring action before cut

### B09 (manim)
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(511,631)–(2088,1528) ∩ blob@(1629,660)–(1715,710) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(511,631)–(2088,1528) h=897px (17.9×med)
- **Fix:** Separate label positions — two text elements overlap

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 1 | 0 |
| min-size §8.1 | 18 | 0 |
| overflow §8.2 | 18 | 0 |
| contrast §8.3 | 18 | 0 |
| contrast-local §8.3b | 18 | 0 |
| bbox-overlap §8.6b | 18 | 1 |
| card-clip §8.13 | 18 | 0 |
| kerning §8.4 | 17 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
