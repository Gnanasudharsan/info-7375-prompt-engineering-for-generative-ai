# The Reallocation Engine — Final Project Pitch Film

**Course:** INFO7375 Prompt Engineering & Agentic AI  
**Author:** Isaac Tai  
**Project:** The Reallocation Engine CLI (`tisaac-swe-stem-opt`)  
**Duration:** 126.2 seconds (2m 06s, 4K UHD 3840×2160 @ 24fps)  
**Deliverable File:** `Tai_HsuanHung_INFO7375_FinalProjectFilm.zip`  

---

## Executive Summary
This submission presents the final project pitch film for **The Reallocation Engine CLI**, an evidence-first, automated job-application filtering tool engineered for F-1 STEM OPT international students.

The film was authored using **Brutalist** (`brutalist.art`), rendered via Remotion, narrated by an on-device Kokoro TTS neural voice (`am_puck`), and verified through an automated quality gate harness.

### Key Highlights
1. **The 7 Pitch Questions**: Fully answered in [PROJECT-BRIEF.md](PROJECT-BRIEF.md) and demonstrated across the 9 beats.
2. **The Honesty Rule**: Past tense only for the prototype recipe `tisaac-swe-stem-opt` (2026-10-03) and its one run (`role-scores.md`, 2026-10-04). Everything else says "will".
3. **Labels on screen**: every card is stamped `REAL OUTPUT`, `REAL CSV ROWS · LAYOUT CONSTRUCTED`, or `CONSTRUCTED MOCK-UP`. Constructed example values are listed in [SOURCES.md](SOURCES.md).
4. **All Verification Gates Passed**:
   - **Gate L (Beat Lint)**: Clean beat-mix structure.
   - **Gate T (Typography & OCR)**: All 9 beats pass WCAG 4.5:1 contrast, text-floor sizing, and bounding-box overlap checks ([TYPECHECK.md](TYPECHECK.md)).
   - **Gate V (Visual QC)**: 18-frame inspection reports 0 Blockers, 0 Majors (`_qc/REPORT.md`).

---

## Revision (2026-10-25)
Re-cut after instructor feedback. Baseline is what existed on 2026-10-10; nothing built later was added.
- **What and who (P1):** the opening now says who I am and what the tool is first; B01 says the form it will take and who opens it.
- **Unique value (P2):** names the real tool I tried (ChatGPT) and the specific difference: one company per chat and every answer checked by hand, versus a fixed script that reads DOL/SEC records, with AI only reading the job description.
- **Tense (P3, P5):** everything not built yet says "will".
- **Risk (P5):** changed from duplicate postings to company-name mismatch, shown with real CSV rows. Logged in FRICTIONAL.md.
- **Why this project (P4):** I'm an F-1 student and face this check myself.
- **Shown, not asserted (P6):** B01 and B07 show real rows from the 2026-10-04 prototype run; every mock-up is labelled CONSTRUCTED on screen.
- **GitHub matches Canvas:** the `.mp4` is now committed, and the GitHub folder holds the same files as the zip.

---

## Submission Package Contents
The submission archive `Tai_HsuanHung_INFO7375_FinalProjectFilm.zip` contains:
- `README.md`: This project overview and execution summary.
- `final-project-pitch.mp4`: Verified 4K master pitch film (126.2s).
- `PROJECT-BRIEF.md`: Complete answers to the 7 mandatory pitch questions.
- `beat_sheet.json`: Machine-readable beat sheet with audio timings and shot definitions.
- `BUILD-PROMPT.md`: Exact prompt logs and CLI reproduction commands.
- `SOURCES.md`: Full provenance of local engines, models, and public datasets.
- `FRICTIONAL.md`: Complete development friction log documenting architectural choices.
- `TYPECHECK.md` & `_qc/`: Automated quality gate validation reports.

---

## Reproduction Quick Start
To reproduce the film from source:
```bash
# In brutalist.art directory:
python3 runtime/scripts/generate_audio_kokoro.py ../film/youtube/final-project-pitch-film
./art final ../film/youtube/final-project-pitch-film --height 2160 --out ../film/youtube/final-project-pitch-film/exports/landscape
```
