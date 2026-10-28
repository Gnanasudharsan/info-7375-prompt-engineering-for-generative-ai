# Gate summary — bitecheck-pitch v2 (final build 2026-10-22)

Extracted verbatim from the toolkit logs (`art run` then `art final`, brutalist.art b21f625). B00–B12 except B06 rendered 2026-10-21 (_run3), B06 re-rendered in _run5, B10 re-rendered 2026-10-22 (_run6) for the CI result; B13 re-rendered (_run7) for its tag date.

```
[run] GATE L — beat-mix lint
[run] GATE SHAPE — finance chart-shape enforcement
[gate-shape] skip — not a finance reel (beat_sheet.json)
[run] GATE A — static pre-flight
[static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[run] GATE W — WCAG contrast + margins + text-overlap (independent second check)
[gateW] B13_ExistsWill clean
[run] GATE V — frame-level visual QC on the compiled reel
[gate-v] frames=28 BLOCKER=0 MAJOR=0 → /Users/omkarsalian/Desktop/info7375-final-film/final-project-film/_qc/REPORT.md
[run] done → /Users/omkarsalian/Desktop/info7375-final-film/final-project-film  (QC gates: on)
[typecheck] wrote /Users/omkarsalian/Desktop/info7375-final-film/final-project-film/TYPECHECK.md
[typecheck] §8.10 B00: SKIP
[typecheck] §8.10 B01: SKIP
[typecheck] §8.10 B02: SKIP
[typecheck] §8.10 B03: SKIP
[typecheck] §8.10 B04: SKIP
[typecheck] §8.10 B05: SKIP
[typecheck] §8.10 B06: SKIP
[typecheck] §8.10 B07: SKIP
[typecheck] §8.10 B08: SKIP
[typecheck] §8.10 B09: SKIP
[typecheck] §8.10 B10: SKIP
[typecheck] §8.10 B11: SKIP
[typecheck] §8.10 B12: SKIP
[typecheck] §8.10 B13: SKIP
[typecheck] GATE T: PASS
[art] wrote /Users/omkarsalian/Desktop/info7375-final-film/final-project-film/final/bitecheck-pitch.mp4  (231.5s, audio: per-beat timeline (source audio preserved), drawtext: no — PIL overlays)
```

Per-scene layout audit (Gate B, `--curve-strict`): all 14 scenes CLEAN.

Bookend check: BLOCKED by design (no ClaudeTitleOutro, because the outro hard-codes the instructor's handle). See bookend_check.txt.
