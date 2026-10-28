# REQUIREMENTS AUDIT — Cite & Seek pitch film (FINAL render)

Audited by Claude Code on 2026-10-12 against `ASSIGNMENT.md`, re-read in full (102 lines). That file is the only authority; quotes cite its line numbers (`A:16` = ASSIGNMENT.md line 16). This version replaces the earlier audit of the review cut. It reflects Meena's approvals of 2026-10-12 (P1–P7, P9–P14) and the final render.

**Audited film:** `film/cite-and-seek-pitch.mp4`, the **FINAL render**, written 2026-10-12 20:41:17, sha256 `b08dbb34a8ef1cabbd871916be7f71512ab36180aa80fc10abe641697f5938a2`. The toolkit's receipt `cite-and-seek-pitch.verified.json` has `"status": "ready"` with the same sha256. Rendered with the Brutalist toolkit at commit `5a00f54` and Manim Community 0.20.1, which is what the toolkit pins at that commit (`manim>=0.20,<0.21`).

**Timestamps** are beat start times from `film/_qc/audit-frames-final/timeline.tsv`. Mid-beat frames of all 23 beats from the final are in `film/_qc/audit-frames-final/`; I looked at every one. None has a review overlay.

**Status key:** MET · PARTLY MET · MISSING · UNVERIFIED (could not be established from files or command output).

## A. The film

| # | Requirement (quoted) | Status | Evidence | Fix / note |
|---|---|---|---|---|
| A1 | "Length: 2–4 minutes." (A:13) | MET | `ffprobe` on the final: `duration=239.333000` (3 min 59.3 s). The render-integrity timeline is 239.333 s. | Inside the limit by 0.67 s. Any added narration needs a matching cut. |
| A2.1 | Q1 "One sentence." (A:16) | MET | BIDEA 0:00.00 "It's called Cite and Seek." + B00 0:11.50 "A tool that answers questions about a codebase with citations to the exact files, and refuses when the code doesn't say." | — |
| A2.2 | Q1 "…the artifact and its form (repository, …)" (A:16) | MET | B15 3:40.71 "Next, I will build the scoring harness, run the experiments, and write it up in a public GitHub repository." On screen: "public GitHub repository" (`audit-frames-final/B15.png`). | — |
| A2.3 | Q2 "What does it do for the person who uses it, and what makes it different…" (A:17) | MET | B01 0:44.17 and B02 0:54.92 (hypothesis: help a new engineer without pulling a senior engineer away; "I haven't tested that with real engineers yet"). B08 2:04.83 (test questions written before retrieval code). | — |
| A2.4 | Q2 "Name one or two real alternatives you actually looked at (… a manual process)" (A:17) | MET | B09 2:16.62 "The alternative today is reading the code by hand. That's how I checked every answer in my test set." | — |
| A2.5 | Q2 "…and say what yours does that they do not." (A:17) | MET | B09 "…nothing tells you when you've missed the right file", then B09B 2:28.00 "Cite and Seek points to the exact lines, and its tests will measure how often retrieval misses the right file." | — |
| A2.6 | Q3 "The target role and the reader" (A:18) | MET | B10 0:59.96 "It's for someone hiring an entry-level AI engineer." Subheading "Target reader: hiring manager for an entry-level AI Engineer role". | — |
| A2.7 | Q3 "What do they do in the first sixty seconds?" (A:18) | MET | B10 "Once it's written up, in their first minute, they will open the README, compare the baseline with each experiment, and check any cited line themselves." | — |
| A2.8 | Q4 "Which skills, tied to what this course teaches (prompt contracts, verification, agent loops, evaluation, source grounding)." (A:19) | MET | B07 1:42.62 "…retrieval, citation, abstention, and evaluation … In course terms: source grounding, prompt contracts and evaluation." The subheading says the same. | Verification and agent loops aren't named in the film; the brief covers them (section 4). |
| A2.9 | Q4 "What could a reviewer fairly conclude…" (A:19) | MET | B07B 2:00.04 "A reviewer could fairly conclude I can design the test before the system." B11 2:35.00 "small on purpose, not production scale." | — |
| A2.10 | Q4 "…and what evidence will back it?" (A:19) | MET | B12 2:47.67 (scoring harness, LLM judge checked against my own labels, results rebuild with one command); B10 (README comparison). | — |
| A2.11 | Q5 "One thing it will deliberately not do." (A:20) | MET | B11 2:35.00 "Out of scope: agents, fine-tuning, and orchestration frameworks…" | — |
| A2.12 | Q5 "The first piece you will make run, and how someone would know it ran." (A:20) | MET | B12 2:47.67 "The first thing I will build is the scoring harness … You'll know it ran when its results rebuild with one command." | — |
| A2.13 | Q6 "One concrete risk … and what you would do about it." (A:21) | MET | B13 2:59.83 sample size; "I will report raw counts and confidence intervals." | — |
| A2.14 | Q7 "Say which skills are new to you and which you already have" (A:22) | MET | B16 3:15.54 "Evaluating models on held-out data isn't new to me; retrieval, embeddings, and using one model to judge another are. This project is how I learn them…" | — |
| A2.15 | Q7 "…for the ones you already have, what you can point to as evidence." (A:22) | MISSING | Meena chose to drop the IEEE mention (P6, 2026-10-12). The film gives no evidence for the existing skill. The brief (section 7) names her internship forecasting work, which is her statement, not a document. | Meena's decision. Grading (A:88) asks for "existing ones backed by something real". |
| A3 | "Stack is your choice — name it." (A:46) | MET | Brief line 3 (Python 3.12, uv, sentence-transformers, numpy, Anthropic API). The film names MiniLM (B04) and Claude Haiku 4.5 (B05); README names the film's own stack. | — |
| A4.1 | "Past tense only for things that exist and that you can show. Everything else is 'will.'" (A:26) | MET | `claim_status` per beat; `FACTCHECK.md` has 44 rows, all PASS or EXEMPT (`factcheck_check.py`: "every row resolved"). Past tense covers only the test set (v0.0), the code (v0.1) and retrieval (evidence file); the rest says "will". | No `ask` output is saved, so the film says citation and abstention exist in the code and prompt, never that they ran. |
| A4.2 | "Label what ran, label what is proposed…" (A:26) | MET | "constructed · planned" on every future-work drawing (B07, B09B, B10, B12, B13, B15); "Built so far" and "Will build" are separate. | — |
| A4.3 | "No invented users, employers, metrics, testimonials, or results." (A:28) | MET | No results are claimed. The hypothesis is labelled as untested. The "about 6 / 17 points" figure is a design calculation (decision 17), spoken with "will". | — |
| A4.4 | "Screenshots, repositories, and data samples you show are real — say when you made or got them." (A:29) | MET | `SOURCES.md`, "Real material shown", gives a date for every real item: the citation tag, chunk ranges, file names and counts. | — |
| A4.5 | "Mock-ups and sketches are labelled constructed on screen." (A:30) | MET | All 19 sketches carry the tag (`audit-frames-final`). BHTF shows "CONSTRUCTED" and "· constructed". BIDEA and BOUT are title cards with no tag (Meena's decision); BDEFS is a text card. | — |
| A4.6 | "Any Claude response you show is one you actually got, with the date." (A:31) | MET | No Claude response is shown (`audit-frames-final/BHTF.png`: the invitation only). | — |
| A5.1 | "Do not use the instructor's name, persona, or credit line." (A:54) | MET | No instructor strings in the narration, sheet or scenes; all 23 final frames checked. The `make_sheet.py` comment naming the persona was reworded (P7). | Remaining mentions are outside the film: Meena's FRICTIONAL.md entries (her choice, P8) and the toolkit's repository address in SOURCES, README and BUILD-PROMPT, which the assignment itself gives (A:49). |
| A5.2 | "Narrate as yourself." (A:54) | UNVERIFIED | First person as Meena, in a synthetic Kokoro voice (`am_michael`). Meena chose to keep it (P14); SOURCES.md discloses it. Whether that satisfies "as yourself" is the grader's interpretation. | — |
| A5.3 | Frames match the narration | MET | 23 mid-beat frames from the final, each checked against its narration. | — |
| A6 | "No real résumé, contacts, application tracker, or conversation transcripts…" (A:44) | MET | A private-data scan of the submission folder found nothing. BUILD-PROMPT summarises prompts and is not a transcript. | — |
| A7.1 | "Run the toolkit's own quality gates and include their reports." (A:52) | MET | Every gate was run on this exact final (gate table below). Reports are in `final-project-film/gate-reports/`. | SRT skipped (no captions); content_default_check fails on toolkit source only. |
| A7.2 | "Fix a film that fails its render-integrity check; do not submit over it." (A:52) | MET | `_qc/RENDER-INTEGRITY.md`: all five checks PASS, including the sha256 match with the toolkit's receipt. | — |
| A7.3 | Grading: "the film passes its own quality checks" (A:88) | MET | Gate T PASS (0 failures across 23 beats); Gates V, B, A, W, L, F and the rest PASS on the final. | — |
| A7.4 | "Free pipeline only — narration and rendering run locally…" (A:50) | MET | Local Kokoro, Manim, Remotion (installed Chrome) and ffmpeg; no API key used to build the film. | — |
| A7.5 | Show-tell format (A:50) | MET | One drawing per drawn beat; labels and segment headings only. | — |

### Gate results on the final (sha256 `b08dbb34…`)

| Gate | Result | Report |
|---|---|---|
| T, in `art final` and standalone (pixels) | PASS, 0 failures | `gate-reports/TYPECHECK.md` |
| V on the final | PASS: 46 frames, 0 blocking, 0 major | `gate-reports/GATE-V-REPORT.md`, `GATE-V-contact_sheet.png` |
| Render integrity | PASS (5/5) | `gate-reports/RENDER-INTEGRITY.md` |
| A, W, B (all 21 drawn scenes) | PASS | `gate-reports/art-run-scenes.log`, `art-run-scenes-2.log`, `console-gates.txt` |
| F, L, SHAPE | PASS, PASS, skipped (finance only) | logs, `console-gates.txt` |
| Sharpness | PASS (median 350.6) | `gate-reports/SHARPNESS.md` (run on the final through a scratch folder, so only the final was visible) |
| Master | PASS (3840×2160, 24 fps, H.264, 239.3 s) | `gate-reports/MASTERCHECK.md` |
| Loudness | PASS (−23.97 LUFS, true peak −3.88 dBTP) | `gate-reports/LOUDNESS.md` |
| Fact-check, bookend, frame, content, lane (cut=master), banned-card, placeholder | PASS | `console-gates.txt` |
| SRT | SKIP: no `.srt` (made only by the toolkit's publishing step) | `gate-reports/SRTCHECK.md` |
| content_default_check | FAIL on toolkit source (`ClaudeComposerAsk.tsx` defaults "Hola, Bear" and "running simulation…"); the film's sheet sets both props, so neither reaches the film | `console-gates.txt` |

## B. The deliverables

| # | Requirement (quoted) | Status | Evidence | Fix / note |
|---|---|---|---|---|
| B8.1 | "README.md — your name, the project's working title, the target role, the runtime, and how to rebuild the film" (A:68) | MET | `final-project-film/README.md` | — |
| B8.2 | "the rendered film (.mp4)" (A:69) | MET | `final-project-film/cite-and-seek-pitch.mp4` (copy of the final, same sha256) | — |
| B8.3 | "PROJECT-BRIEF.md — one page answering the seven questions in text, ending with two lists: exists today and will exist" (A:70) | UNVERIFIED | Seven sections plus both lists. Trimmed to 697 words including Markdown (P9). Whether it fits one page depends on how it is rendered. | — |
| B8.4 | "beat_sheet.json — your narration and visual plan" (A:71) | MET | 23 beats | — |
| B8.5 | "BUILD-PROMPT.md — the prompts and commands that rebuild it" (A:72) | MET | `final-project-film/BUILD-PROMPT.md` | — |
| B8.6 | "SOURCES.md — what you used, what you made, what Claude contributed, and any third-party asset with its licence" (A:73) | MET | `final-project-film/SOURCES.md`; two licences stay marked UNVERIFIED inside it (Brutalist has no licence file; the Kokoro model card wasn't checked) | — |
| B8.7 | "the toolkit's gate reports, if it produced them" (A:74) | MET | `final-project-film/gate-reports/` | — |
| B8.8 | "FRICTIONAL.md — dated entries as you worked" (A:75) | PARTLY MET | Copy of Meena's notes: 15 entries, all under 2026-10-11. Nothing logged for 2026-10-12. | Meena to add entries (event list in Claude's summary). |
| B9 | PROJECT-BRIEF.md agrees with the film | MET | Both now carry the artifact, hypothesis, alternative, reader and first sixty seconds, course concepts, reviewer conclusion, scope, risk, the internship-only Q7 and the dated retrieval run. The brief has more detail (k-values, MRR, dates); the film omits dates by decision. | — |
| B10.1 | "Canvas file name: LastName_FirstName_INFO7375_FinalProjectFilm.zip" (A:66) | MET (planned) | `Periasamy_Meena_INFO7375_FinalProjectFilm.zip` (README) | Create at final assembly. |
| B10.2 | "GitHub folder: fall-2026/first-name-last-initial/final-project-film/" (A:66) | MET (planned) | `fall-2026/meena-p/final-project-film/` in Meena's fork, not touched yet (her instruction) | Push at final assembly. |
| B10.3 | "Include the GitHub folder link and your final commit hash in the Canvas submission." (A:76) | MISSING | Not created yet | After the push. |
| B10.4 | "Leave out caches, credentials, private data, and private conversation transcripts." (A:76) | MET | `final-project-film/` is copies only, with no caches, mp3s, renders, toolkit state, `FILM-PLAN.md`, `.env` or credentials (scan) | — |

## Grading: "The pitch (30)" (A:88)

| Component | Covered by | Weak spot |
|---|---|---|
| What and who (7) | BIDEA, B00, B15 (artifact), B10 | — |
| Unique value (5) | B01, B02, B08, B09, B09B | The value is a hypothesis, honestly labelled untested |
| What it proves (5) | B07, B07B, B12, B11 | — |
| Why this project (4) | B16 | **Existing skill not backed by something real** (A2.15; Meena's choice) |
| Scope and honest risk (5) | B11, B12, B13, B14, B15 | — |
| Shown, not asserted (4) | 19 tagged drawings; FACTCHECK.md; evidence file; all gates pass | — |
| Frictional (5) | FRICTIONAL.md | No entries for 2026-10-12 yet |
| GitHub matching Canvas (5) | — | Push, link and commit hash pending |

## Counts (mechanical, from the table rows)
**45 rows:** 40 MET (including 2 'MET (planned)') · 1 PARTLY MET · 2 MISSING · 2 UNVERIFIED.
