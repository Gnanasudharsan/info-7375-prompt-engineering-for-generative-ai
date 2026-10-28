# Layout audit (Gate B), Gate A static pre-flight, Gate W contrast/margins: all 16 scenes

Re-run over every scene on 2026-10-13 after the last scene change (draft 3), so this covers the final version.

## Layout audit (`runtime/qc/manim_layout_audit.py`, safe area ±6.3 x / ±3.4 y)
- B00_WhatItIs: errors: 0  ·  warnings: 0
- B01_Repo: errors: 0  ·  warnings: 0
- B02_Why: errors: 0  ·  warnings: 0
- B03_Alternatives: errors: 0  ·  warnings: 0
- B04_Different: errors: 0  ·  warnings: 0
- B05_FirstMinute: errors: 0  ·  warnings: 0
- B06_Loop: errors: 0  ·  warnings: 0
- B07_Control: errors: 0  ·  warnings: 0
- B08_Gate: errors: 0  ·  warnings: 0
- B09_Eval: errors: 0  ·  warnings: 0
- B10_Stack: errors: 0  ·  warnings: 0
- B11_Boundary: errors: 0  ·  warnings: 0
- B12_FirstPiece: errors: 0  ·  warnings: 0
- B13_Swap: errors: 0  ·  warnings: 0
- B14_Shelves: errors: 0  ·  warnings: 0
- B15_ExistsWill: errors: 0  ·  warnings: 0

## Gate A (`runtime/qc/static_scene_check.py`)
- B00_WhatItIs [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B01_Repo [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B02_Why [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B03_Alternatives [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B04_Different [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B05_FirstMinute [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B06_Loop [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B07_Control [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B08_Gate [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B09_Eval [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B10_Stack [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B11_Boundary [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B12_FirstPiece [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B13_Swap [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B14_Shelves [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
- B15_ExistsWill [static-check] 1 scene(s): 1 clean · 0 warn · 0 error

## Gate W (`runtime/qc/wcag_margin_check.py`)
- [gateW] B00_WhatItIs clean
- [gateW] B01_Repo clean
- [gateW] B02_Why clean
- [gateW] B03_Alternatives clean
- [gateW] B04_Different clean
- [gateW] B05_FirstMinute clean
- [gateW] B06_Loop clean
- [gateW] B07_Control clean
- [gateW] B08_Gate clean
- [gateW] B09_Eval clean
- [gateW] B10_Stack clean
- [gateW] B11_Boundary clean
- [gateW] B12_FirstPiece clean
- [gateW] B13_Swap clean
- [gateW] B14_Shelves clean
- [gateW] B15_ExistsWill clean

## Earlier blocks, fixed before the final render
- Gate B warning: B05 "one command" outside the safe area (x = -6.53). Moved in.
- Gate B error: B11 cross drawn over the `>_` label. Moved beside the shell.
- Gate T fail: B08 wavy lines read as overlapping text. Replaced with bars.
- Gate T fail (draft 3): B07 label 1 px under the minimum, then wavy lines in its claim cards read as text. Label enlarged; lines replaced with bars.
