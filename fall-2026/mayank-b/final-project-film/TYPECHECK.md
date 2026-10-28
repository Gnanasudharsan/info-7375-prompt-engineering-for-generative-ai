# TYPECHECK.md — GATE T

Reel: `source-check-pitch`  |  Checked: 2026-10-25T16:53  |  Overall: PASS  |  Beats checked: 17  |  FAILs: 0

Spec: `skills/make/kerning/reference/type-spec.md` §8.  Floor: 1.9% frame-height.  Contrast: 4.5:1 WCAG.  Kern threshold: 3.5× expected advance.  Wordy budget: 2 elements.

| beat | lane | polarity | worst finding | status | fix |
|------|------|----------|---------------|--------|-----|
| BIDEA | bookend | light | min-size §8.1: min text-run height 59px >= floor 41px | PASS | — |
| BWHO | hyperframes | light | min-size §8.1: min text-run height 20px >= floor 20px (individual-char fallback at 1×) | PASS | — |
| BKID | hyperframes | light | min-size §8.1: min text-run height 20px >= floor 20px (individual-char fallback at 1×) | PASS | — |
| B00 | hyperframes | light | min-size §8.1: min text-run height 61px >= floor 20px | PASS | — |
| B01 | hyperframes | light | min-size §8.1: min text-run height 34px >= floor 20px | PASS | — |
| B02 | hyperframes | light | min-size §8.1: min text-run height 32px >= floor 20px | PASS | — |
| B03 | hyperframes | light | min-size §8.1: min text-run height 20px >= floor 20px | PASS | — |
| B04 | hyperframes | light | min-size §8.1: min text-run height 34px >= floor 20px | PASS | — |
| B05 | hyperframes | light | min-size §8.1: min text-run height 61px >= floor 20px | PASS | — |
| B06 | hyperframes | light | min-size §8.1: min text-run height 32px >= floor 20px | PASS | — |
| B07 | hyperframes | light | min-size §8.1: min text-run height 61px >= floor 20px | PASS | — |
| B08 | hyperframes | light | min-size §8.1: min text-run height 21px >= floor 20px | PASS | — |
| B09 | hyperframes | light | min-size §8.1: min text-run height 61px >= floor 20px | PASS | — |
| B10 | hyperframes | light | min-size §8.1: min text-run height 34px >= floor 20px | PASS | — |
| B11 | hyperframes | light | min-size §8.1: min text-run height 61px >= floor 20px | PASS | — |
| B12 | hyperframes | light | min-size §8.1: min text-run height 34px >= floor 20px | PASS | — |
| BOUT | bookend | light | no-wordy-card §8.5: no prose payload found | PASS | — |

---

## Failures requiring action before cut

*None — GATE T PASS.*
---

## Check summary

| Check | Beats checked | FAILs |
|-------|---------------|-------|
| no-wordy-card §8.5 | 1 | 0 |
| min-size §8.1 | 17 | 0 |
| overflow §8.2 | 17 | 0 |
| contrast §8.3 | 17 | 0 |
| contrast-local §8.3b | 17 | 0 |
| bbox-overlap §8.6b | 17 | 0 |
| card-clip §8.13 | 17 | 0 |
| kerning §8.4 | 0 | 0 |
| redundancy §8.10 (advisory) | 0 | 0 (advisory — no exit effect) |

---

*GATE T: any FAIL blocks `./art run` and `./art final`. Fix the flagged beats and re-run `scripts/type_check.py` until green.*
