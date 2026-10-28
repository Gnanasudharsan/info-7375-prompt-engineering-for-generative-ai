# TYPECHECK.md — GATE T

Reel: `marino-desk-assistant-pitch`  |  Checked: 2026-10-13T15:35  |  Overall: **FAIL**  |  Beats checked: 16  |  FAILs: 3

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| B01 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| B02 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B03 | manim | light | min-size §8.1: min text-run height 121px >= floor 41px | PASS | — |
| B04 | manim | light | bbox-overlap §8.6b: text-run bbox overlap 100% >= 10% — two labels are printing on top of … | **FAIL** | Separate label positions — two text elements overlap |
| B05 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| B06 | manim | light | min-size §8.1: min text-run height 83px >= floor 41px | PASS | — |
| B07 | manim | light | min-size §8.1: smallest text run 40px < floor 41px (1.9% of 2160px logical); likely a capt… | **FAIL** | Increase font_size in scenes.py or Remotion component |
| B08 | manim | light | min-size §8.1: min text-run height 47px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B09 | manim | light | min-size §8.1: min text-run height 120px >= floor 41px | PASS | — |
| B10 | manim | light | min-size §8.1: min text-run height 94px >= floor 41px | PASS | — |
| B11 | manim | light | min-size §8.1: min text-run height 159px >= floor 41px | PASS | — |
| B12 | manim | light | min-size §8.1: min text-run height 59px >= floor 41px (individual-char fallback at 2×) | PASS | — |
| B13 | manim | light | bbox-overlap §8.6b: text-run bbox overlap 100% >= 10% — two labels are printing on top of … | **FAIL** | Separate label positions — two text elements overlap |
| B14 | manim | light | min-size §8.1: min text-run height 60px >= floor 41px | PASS | — |
| B15 | manim | light | min-size §8.1: min text-run height 61px >= floor 41px | PASS | — |
| BOUT | manim | light | min-size §8.1: min text-run height 70px >= floor 41px | PASS | — |

---

## Failures requiring action before cut

### B04 (manim)
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(1321,494)–(2788,720) ∩ blob@(1579,584)–(2233,629) (100% of smaller); separate label positions in scenes.py or Remotion component
- **Fix:** Separate label positions — two text elements overlap

### B07 (manim)
- **min-size §8.1**: smallest text run 40px < floor 41px (1.9% of 2160px logical); likely a caption/label too small — increase font_size or check if this is a data label needing §7 treatment
- **Fix:** Increase font_size in scenes.py or Remotion component

### B13 (manim)
- **bbox-overlap §8.6b**: text-run bbox overlap 100% >= 10% — two labels are printing on top of each other: blob@(808,1399)–(2707,1786) ∩ blob@(1363,1570)–(1665,1611) (100% of smaller); separate label positions in scenes.py or Remotion component | §8.6c ADVISORY: possible fused run(s) — blob@(808,1399)–(2707,1786) h=387px (1.8×med)
- **Fix:** Separate label positions — two text elements overlap

---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 0 | 0 |
| min-size §8.1 | 16 | 1 |
| overflow §8.2 | 16 | 0 |
| contrast §8.3 | 16 | 0 |
| contrast-local §8.3b | 16 | 0 |
| bbox-overlap §8.6b | 16 | 2 |
| card-clip §8.13 | 16 | 0 |
| kerning §8.4 | 16 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
