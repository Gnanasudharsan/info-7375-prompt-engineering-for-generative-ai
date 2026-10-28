# SOURCES — DayThread pitch film

**Status:** Claude fetched these pages on **2026-10-14**. Every quote below was checked word for
word against the downloaded page text. **Aditya confirmed on 2026-10-14 reading all four pages**
(Lifeline fall detection; DailyCall AI companion; DailyCall daily check-in calls; DailyCall safety
policy). That is **reading their documentation, not testing their products**. The film says "I read
their documentation" and nothing more.
Nothing here says DayThread is better, or that either product lacks a feature its pages don't
mention. These are the companies' own marketing pages, not independent evaluations, and no one
on this project tested either product.

## Alternatives (official pages)

| # | Source | Read by Aditya? |
|---|---|---|
| S1 | Lifeline, "Automatic Fall Detection Systems for Seniors" — https://www.lifeline.com/medical-alert-systems/fall-detection/ | **Yes — 2026-10-14** (Aditya's confirmation) |
| S2 | DailyCall, "AI Companion for Elderly Loved Ones" — https://dailycall.care/ai-companion-for-elderly | **Yes — 2026-10-14** (Aditya's confirmation) |
| S3 | DailyCall, "Daily Check-In Calls for Seniors" — https://dailycall.care/daily-check-in-calls-for-seniors (linked from S2) | **Yes — 2026-10-14** (Aditya's confirmation) |
| S4 | DailyCall, "Safety Policy" — https://dailycall.care/safety-policy (linked from S2's footer) | **Yes — 2026-10-14** (Aditya's confirmation) |

### What the pages say (verbatim, checked 2026-10-14)

**S1 Lifeline**
- How it works: "Our finely tuned algorithm differentiates between true falls and false alarms."
  The sensors are accelerometers and barometric sensors.
- After a fall: "our Trained Care Specialists will contact you immediately through the system's
  two-way speaker". If there is no verbal contact, one section says they "may default to calling
  emergency services". The FAQ says they "will dispatch emergency services to your location
  regardless". The two wordings differ.
- Limitation: "Fall detection technology does not detect 100% of all falls." Lifeline also
  "always recommend[s] pressing your button whenever you need help".
- Not found on this page: daily check-ins, conversation history, trends, or reports. (That is
  only what this page says, not a claim about the product.)

**S2–S4 DailyCall**
- What it does: "your loved one receives a phone call, hears a friendly voice, and can talk about
  their day…". Also: "DailyCall uses AI-generated phone calls for daily check-ins."
- Across calls: "Conversation context that can improve over time"; "Families can add interests,
  routines, names, and topics…".
- For families: "Helpful summaries after calls", "Missed-call visibility", "Conversation summaries
  and highlights" (S3). DailyCall "may send service updates, call summaries, missed-call
  information, or support follow-ups to the account owner or authorized contacts" (S4).
- Safety handling (S4): if a caller shares something that sounds urgent, DailyCall "is designed to
  encourage the caller to contact emergency services, a trusted person, or an appropriate crisis
  line". "Families and authorized contacts remain responsible for urgent follow-up…". "DailyCall
  cannot guarantee that every safety concern will be detected, interpreted correctly, or delivered
  to the right person in time." Its reviews "may include automated checks and human review where
  needed for support, safety, security, or service improvement."
- Limitation (all pages): "It is not emergency monitoring, medical advice, or a replacement for
  caregivers."

### What this means for the pitch (Claude's reading; Aditya **accepted** the cautious comparison on 2026-10-14)
- DailyCall's pages already describe context carried across calls, plus summaries for families.
  So "remembers across days" alone is **not** a difference the film can claim.
- What the film can say: DayThread's *planned* focus is narrower. Each concern links back to the
  exact earlier words. A separate check reads the original conversation, not the summary. A
  coordinator approves, refuses, or defers a proposed action, and the decision is recorded
  against what the coordinator saw. The film can't say the alternatives lack these things.

## Course and toolkit

- Final project brief (build, due 2026-12-20): `Final Project — An Agentic System You Choose` (Canvas PDF, read 2026-10-14).
- Frictional rubric: https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/frictional.md (fetched 2026-10-14)
- GitHub posting rubric: https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/github-submission.md (fetched 2026-10-14)
- brutalist.art toolkit: local clone, `main` at `519fcbb96e9e1898d374c8794117cab494ffc5cb`; skill `show-tell`.
  See `TOOLKIT-CHANGES.md`.

Aditya's instruction (2026-10-14): describe the three items as DayThread's *proposed focus*, not as
features the alternatives are proven to lack. Keep the intended benefit clear (a coordinator understands
changes without manually reconstructing several conversations), and frame it as intended, not measured.
Aditya confirmed reading S1–S4 on 2026-10-14 (documentation only; no product was tested).

## Third-party software, assets and licenses

| What | Used for | License | How verified |
|---|---|---|---|
| brutalist.art toolkit (Nik Bear Brown / Humanitarians AI) | build pipeline, gates; `iso_kit.py` and 11 prop geometries **copied into** `film/scenes.py` | **No LICENSE file in the local clone. License unknown; flagged.** | `ls` of the clone root, 2026-10-14 |
| Manim Community v0.20.1 | drawing and rendering every scene | MIT | installed `manim-0.20.1.dist-info` METADATA (`License-Expression: MIT`) |
| kokoro-onnx 0.6.1 | running the TTS model locally | MIT | installed dist-info LICENSE ("MIT License … thewh1teagle") |
| Kokoro v1.0 model weights + voices (`kokoro-v1.0.onnx`, `voices-v1.0.bin`), voice `am_onyx` | the synthesized narration | Apache-2.0 per the Kokoro-82M project | **not re-verified from a local file** (no license file beside the model) |
| EB Garamond (Regular, Italic) | all on-screen type | SIL Open Font License 1.1 | font files in `~/Library/Fonts`; OFL per the font project, not re-read locally |
| FFmpeg 9.0.2 (Homebrew) | encoding and probing | LGPL/GPL depending on build | used as a tool; not redistributed |
| faster-whisper 1.2.1 (`base.en`, `small.en`) | machine transcripts for pronunciation and cue checks only; no output appears in the film | MIT | installed METADATA |
| Lifeline and DailyCall pages (S1–S4) | short quotations for commentary in SOURCES/FACTCHECK; the film names them and paraphrases two facts | © their owners | no logos, screenshots or page images are used |

No stock images, no music, no generated images or video, and no Professor Bear portraits.

## Who contributed what

**Aditya Raj**
- The project idea (DayThread) and all seven answers.
- The choice of alternatives (Lifeline, DailyCall) and reading S1–S4 (2026-10-14).
- The design decisions on permissions, executor, review page and transcript check.
- The film decisions: identity, narrator, no people on screen, no key terms or Your Turn, outro
  content, preview first, keeping the native 4K settings.
- Every wording revision listed in `FRICTIONAL.md`, and approval of the 15-second preview.
- Watched the finished film and approved it (2026-10-14).
- Confirmed the film's new-skills list (2026-10-14).
- **Other AI tools:** none. Aditya used no AI tool other than Claude for this film (confirmed by
  Aditya, 2026-10-14).

**Claude (Claude Code, model Opus 5.5, this session, 2026-10-14)**
- Inspected the toolkit and ran setup.
- Fetched the four pages and checked the quotes, and drafted the narrowed comparison (Aditya
  accepted it).
- Compressed Aditya's answers into the script (v1–v3).
- Wrote all film code: `make_sheet.py`, `audio_post.py`, `assemble_scenes.py`, `scenes_body.py`
  (18 drawn scenes), and the preview's equivalents.
- Generated the Kokoro audio, ran the gates, diagnosed and fixed gate failures, and inspected frames.
- Wrote `README.md`, `PROJECT-BRIEF.md`, `BUILD-PROMPT.md`, this file, `FACTCHECK.md`,
  `SHOTLIST.md`, the gate and check reports, and the `FRICTIONAL.md` entries. Aditya's own words
  in `FRICTIONAL.md` are quoted and attributed to Aditya.

## Resubmission additions (2026-10-25)

The two-day replay in `replay/` was built and run on 2026-10-25, during the class-wide
resubmission. It did not exist when the film was submitted on 2026-10-14. Everything above this
section describes the original film and is unchanged.

**Software and models used by the replay:**

| What | Used for | Licence / terms | How verified |
|---|---|---|---|
| Python 3.12.8 standard library (`sqlite3`, `subprocess`, `json`, …) | `replay.py`, `flags.py`, `make_review_sheet.py` | PSF License | `python3 --version` |
| SQLite 3.51.0 | the run database `daythread.sqlite` | public domain | `sqlite3 --version` |
| Claude Code CLI 2.1.241 | every experimental call (`claude -p`), logged in through Aditya's claude.ai account; no API key | Anthropic terms | `claude --version`, `claude auth status` |
| `claude-opus-5` | generated all 10 summaries and 20 day-two openings | Anthropic terms | `modelUsage` in each call's JSON |
| `claude-haiku-4-5-20251001` | called automatically by the CLI to generate session titles; its output is not used | Anthropic terms | debug log, `replay/preflight/HAIKU-TITLE-CALL.md` |

No other AI tool or model was used. The local models installed on the machine were not used.

**Data:** a synthetic fixture only (`replay/fixture/`). Peg Hollis is fictional. No real person,
conversation or record.

**Who contributed what (resubmission):**

*Aditya Raj*
- Chose to run the replay with Claude through the CLI.
- Wrote the pre-run prediction (`replay/PRE-RUN.md` §1, verbatim).
- Adopted the fixture and kept DayThread's mobility follow-up in it.
- Corrected the evaluation notes on "fussing" and "nothing's broken".
- Refined the scoring rules (ambiguous wording, omitted vs. softened vs. changed, invented
  details, generic questions, "not tested").
- Reviewed the results and the excerpts Claude presented (2026-10-25), and gave the judgments in
  `replay/runs/20261025T135900/aditya_review.json` (aggregate A1–A4, rules R1–R5). Did not
  separately re-score every cell of the review sheet.
- Stated the takeaway (preserving an event does not guarantee preserving its meaning), the
  limitation (one-sentence memory not achieved), and the proposed next test.
- Asked for the minimum film corrections. Watched the rebuilt v4 film and approved it (2026-10-25):
  "I watch the video, and I approve of it."
- Authorized pushing the updated folder to the course repo, as for the original submission.

*Claude (Claude Code, Opus 5.5, 2026-10-25)*
- Checked the repository and that the CLI works.
- Drafted the fixture transcript, the four prompts and the first version of the criteria.
- Wrote `PRE-RUN.md`, `replay.py`, `flags.py`, `make_review_sheet.py` and `replay/README.md`.
- Ran the preflight check and the 30-call experiment.
- Diagnosed the Haiku title call.
- Wrote the provisional scores (`claude_provisional.json`) and `RESULTS.md`.
- Wrote the 2026-10-25 entries in `FRICTIONAL.md`, apart from Aditya's quoted prediction and
  decisions. In the 14:59 entry, Claude organized Aditya's own review statements into first person
  with light edits.
- Applied Aditya's judgments to the matching review-sheet cells and rewrote `RESULTS.md` as final.
- Film revision: wrote the B04 and B15 narration changes in `SCRIPT.md` (v4) and the B15 drawing
  changes in `source/scenes_body.py`, regenerated the two narration clips with Kokoro, re-rendered
  the two scenes, ran the toolkit gates and the final checks, updated `README.md`,
  `PROJECT-BRIEF.md` and `FACTCHECK.md`, and built the revised ZIP.
