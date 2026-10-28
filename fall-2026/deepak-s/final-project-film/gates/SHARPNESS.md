# SHARPNESS GATE — cuegate-pitch

Compiled master: `cuegate-pitch-slate.mp4`
Median Laplacian variance: **204.2**
Failure threshold: 102.1 (50% of median)

> Soft beats = rotation applied to `crispEdges` pixel-art.
> Fix: use translation/scale only — never rotate. See PIXEL-ART LAW in
> `ClaudeMascotScene.tsx`.

| Beat | LV | % of median | Status |
|------|----|-------------|--------|
| B00 | 545.7 | 267% | SKIP (exempt — no pixel-art rotation possible) |
| B01 | 249.7 | 122% | PASS — 122% |
| B02 | 257.2 | 126% | PASS — 126% |
| B03 | 155.5 | 76% | PASS — 76% |
| B04 | 186.7 | 91% | PASS — 91% |
| B05 | 172.1 | 84% | PASS — 84% |
| B06 | 293.9 | 144% | PASS — 144% |
| B07A | 360.5 | 177% | PASS — 177% |
| B07B | 216.8 | 106% | PASS — 106% |
| B08 | 217.9 | 107% | PASS — 107% |
| B09 | 245.8 | 120% | PASS — 120% |
| B10 | 175.7 | 86% | PASS — 86% |
| B11 | 170.6 | 84% | PASS — 84% |
| B12 | 191.5 | 94% | PASS — 94% |
| B13 | 156.7 | 77% | PASS — 77% |
| BOUT | 164.6 | 81% | PASS — 81% |
