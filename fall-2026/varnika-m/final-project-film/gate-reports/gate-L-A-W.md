# Gates L, A, W — final scenes.py, run directly on all 16 scenes (2026-10-14T22:59:37Z)

Gate A runs on a scratch copy holding only `scenes.py`, as `art run` does. Gate W is run here on every scene by calling `wcag_margin_check.py` directly, because `art run` reported only 11 of 16 (it skipped B07A, B07B, B12A, B12B and BOUT).

```text
[L] [beat-lint] clean — beat mix OK (beat_sheet.json)
[A] B01_Ask: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B02_Repo: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B03_Optional: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B04_Deprecated: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B05_Conveyor: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B06_NotFound: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B07A_Registry: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B07B_Chat: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B08_FirstMinute: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B09_Proves: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B10_Scope: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B11_Risk: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B12A_Have: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B12B_New: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] B13_Ledger: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[A] BOUT_Title: [static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[W] B01_Ask: [gateW] B01_Ask clean
[W] B02_Repo: [gateW] B02_Repo clean
[W] B03_Optional: [gateW] B03_Optional clean
[W] B04_Deprecated: [gateW] B04_Deprecated clean
[W] B05_Conveyor: [gateW] B05_Conveyor clean
[W] B06_NotFound: [gateW] B06_NotFound clean
[W] B07A_Registry: 
[W] B07B_Chat: 
[W] B08_FirstMinute: [gateW] B08_FirstMinute clean
[W] B09_Proves: [gateW] B09_Proves clean
[W] B10_Scope: [gateW] B10_Scope clean
[W] B11_Risk: [gateW] B11_Risk clean
[W] B12A_Have: 
[W] B12B_New: 
[W] B13_Ledger: [gateW] B13_Ledger clean
[W] BOUT_Title: 
```

## Gate W for the five skipped scenes

Gate W selects classes with the pattern `[A-Z]+\d+_`, so `B07A_`, `B07B_`, `B12A_`, `B12B_` and `BOUT_` never match. These five were checked on a scratch copy of `scenes.py` with only those class names changed (B71, B72, B121, B122, B99); the scene code is identical. Output, with the original names restored:

```text
[gateW] B07A_Registry clean
[gateW] B07B_Chat clean
[gateW] B12A_Have clean
[gateW] B12B_New clean
[gateW] BOUT_Title clean
```
