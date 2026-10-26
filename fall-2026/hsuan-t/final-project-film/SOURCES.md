# SOURCES & PROVENANCE — The Reallocation Engine Pitch Film

All components of this film were synthesized, rendered, and verified locally without paid generation, proprietary clouds, or commercial video APIs.

## 1. Narration & Audio
* **Engine**: Local Kokoro TTS v0.19 running on Apple Silicon Metal acceleration.
* **Voice Model**: `am_puck` (American Male, authoritative & clean conversational tone).
* **Source Script**: Written by Isaac Tai under the assignment's Honesty Rule: past tense only for the prototype recipe (2026-10-03) and its one run (2026-10-04); "will" for everything else.

## 2. Visuals & Animation
* **Animation Framework**: Brutalist (`brutalist.art`), built on Remotion v4 + React 18 with TypeScript.
* **Typography & Palette**:
  - Claude Brutalist palette: Stage `#F2F0E9`, Ink `#3D3929`, Dark `#1F1E1B`, Terracotta Spark `#D97757`, Slate Bar `#2E4057`.
  - Type Stack: EB Garamond (Serif), Inter (Sans), JetBrains Mono (Mono).
* **Components Used**:
  - `BrutalistHesitantWriter`: Cold-open typing & backspace animation.
  - `ShowTellCard`: Product demo scenes (Search, Tabs, Workspace, Layout, Stack, Dashboard).
  - `ClaudeTitleOutro`: Minimalist dark outro with creator signature.

## 3. Data & Ground Truth
* **Underlying Project**: *The Reallocation Engine* (`tisaac-swe-stem-opt` recipe).
* **Immigration Data**: Department of Labor (DOL) Office of Foreign Labor Certification (OFLC) H-1B LCA Disclosure Data (FY2024 / FY2025 public records).
* **Corporate Filings**: SEC EDGAR Form D Regulation D Exemption Filings API.
* **On-screen labels (revision 2026-10-25)**: every card carries a stamp saying what it is.
  - `REAL OUTPUT · role-scores.md · 2026-10-04` (B01, B07): rows copied verbatim from `reallocation-engine/the-reallocation-engine/scripts/contrib/2026fa/tisaac-swe-stem-opt/role-scores.md`, commit `98a46a1`.
  - `REAL CSV ROWS · LAYOUT CONSTRUCTED` (B06): TOAST INC / TOAST HOLDINGS INC / MOONTOAST INC values read from `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (in the repo since 2026-08-17).
  - `CONSTRUCTED MOCK-UP` (B02 to B05): sketches of the planned tool. The B02 values (`15 Approved`, `$24M Raised`) are constructed examples, not real records.

## 4. Quality & Gate Verification
* **Gate L (Beat Lint)**: Checked beat duration, transition pacing, and shot diversity.
* **Gate T (Typography & OCR)**: Automated WCAG 4.5:1 contrast, text run bounding-box overlap, and 1.9% frame-height floors verified across 3840x2160 native frames (`TYPECHECK.md`).
* **Gate V (Visual QC)**: 18-frame automated contact sheet and visual check (`_qc/REPORT.md`, `BLOCKER=0, MAJOR=0`).
