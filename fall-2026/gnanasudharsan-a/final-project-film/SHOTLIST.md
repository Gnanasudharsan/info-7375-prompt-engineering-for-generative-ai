# SHOTLIST — decisiontrace-pitch

| Beat | Method | Slot | Notes |
|---|---|---|---|
| B00 | Manim `B00_Title` (scenes.py) | manim/B00.mp4 | Name (large), DecisionTrace, "A pitch for a project that doesn't exist yet." Audio: Kokoro af_heart, name from IPA (tools/phoneme_name.py, variant E) |
| B01 | Manim `B01_StatusTag` | manim/B01.mp4 | ? → decided · in progress · superseded; from 7.48 s a dashed repo folder labelled PLANNED with CLI · synthetic docs · test set · eval report; complete by 15.4 s, held to the end |
| B02 | Manim `B02_TestSetup` | manim/B02.mp4 | Label: SYNTHETIC TEST DATA |
| B03 | Two composed stills in sequence | media/B03.mp4 | Real screenshots, scaled only (tools/compose_frames.py): NotebookLM summary (2 highlight boxes) → from 8.61 s the run-2 Q1 answer (highlight "uses DynamoDB as its primary datastore"). Label REAL · NotebookLM · captured 2026-10-10 on both |
| B04 | Still, composed | media/B04.png | Real screenshot, cropped (22,406,656,698) + scaled only; label + 1 highlight box drawn on the canvas |
| B05 | Manim `B05_ClaimCheck` | manim/B05.mp4 | claim → quote found ✓ / missing ✗ |
| B06 | Manim `B06_Terminal` | manim/B06.mp4 | CONSTRUCTED terminal mock-up, large label "CONSTRUCTED · NOT REAL OUTPUT"; window title "zsh — decisiontrace"; FAIL in red; typing from 3.6 s, cursor after the typed text, "→ report   eval/report.md" last; complete screen held ~5 s |
| B07 | Manim `B07_VerifyLoop` | manim/B07.mp4 | answer → verify → ✓ pass → cited answer / ✗ fail → not supported; "retry once" curve |
| B08 | Manim `B08_Scope` | manim/B08.mp4 | Out / In / First, each on its sentence; accent underline spans each full line |
| B09 | Manim `B09_OwnHomework` | manim/B09.mp4 | A hand grading its own paper; then "hand-written by me" page with ✗ on a hard case |
| B10 | Manim `B10_WhyThis` | manim/B10.mp4 | New vs have |
| B11 | Manim `B11_ExistsVsWill` | manim/B11.mp4 | Exists vs will (two-line heading) |
| B12 | Manim `B12_Outro` | manim/B12.mp4 | Name + "Narration: synthetic voice (Kokoro)". Audio: Kokoro af_heart, name from IPA (tools/phoneme_name.py, variant E) |

Audio: every beat is Kokoro af_heart. B01–B11 come from generate_audio_kokoro.py (mp3/beat-<ID>.mp3). B00 and B12 come from tools/phoneme_name.py --variant E (name IPA ɲˈɑːnɑːsˌuːdʰɚʃɑːn ɑːʃˈoʊk kuːmˈɑːɹ); their engine is "kokoro-phoneme", so generate_audio_kokoro.py skips them. Regenerate other beats only with --only <beat ids>.
