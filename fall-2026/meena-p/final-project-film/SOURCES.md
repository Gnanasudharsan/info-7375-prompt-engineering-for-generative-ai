# SOURCES — Cite & Seek pitch film

What was used, what Meena made, what Claude contributed, and every third-party asset with its licence. Licence statements are quoted from the installed files, checked 2026-10-12. Anything that couldn't be checked is marked UNVERIFIED.

## Real material shown in the film, and when it was made or obtained

| Shown | Beats | What it is | Made or obtained |
|---|---|---|---|
| Citation tag `[app/api/orders.py:52-84]`, and "lines 52-84" | B00, B02, B05, B09B | A real chunk of the corpus. The baseline's chunker splits `app/api/orders.py` at 1-26, 27-51, 52-84, 85-107, 108-136, 137-145. The same chunk is result 3 (score 0.3544) in Meena's saved `search` output. | Chunker run read-only, 2026-10-11. Search output dated `Sun Oct 11 16:53:14 EDT 2026` (`evidence/v0.1-search-2026-10-11.txt`). |
| Chunk labels `orders.py 52-84`, `cart.py 27-46`, `payments.py 1-24` | B04 | Real chunk ranges from the baseline's chunker | Chunker run read-only, 2026-10-11 |
| File names `orders.py`, `cart.py`, `auth.py`, `payments.py`, `models.py`; "37 files"; "e-commerce API", "GitHub · MIT" | B03, B09, B11 | Files in the corpus (`Franklindot04/ecommerce-api`), as listed by `git ls-files corpus/` in Meena's repository | Read 2026-10-11 |
| "53 questions", "8 unanswerable", "10 synthetic incidents" | B03, B08, B14 | Counts of Meena's frozen test set (tag v0.0) | Verified by Meena, 2026-10-11 |

Everything else on screen is drawn, and labelled "constructed" or "constructed · planned". The film shows no screenshots and no Claude responses.

## Used (third-party)

| What | How it was used | Licence |
|---|---|---|
| **Brutalist toolkit** (`github.com/nikbearbrown/brutalist.art`), fork checkout at commit `5a00f54` for the final (`8b1ae22` for earlier review cuts) | Pipeline (`art run`, `art final`, `compile.py`), quality gates, Kokoro wrapper, the show-tell palette and style. Remotion components rendered in the film: `ClaudeDefinitions` (BDEFS) and `ClaudeComposerAsk` (BHTF). | **UNVERIFIED:** no LICENSE or COPYING file in the checkout's root (checked 2026-10-12) |
| **Kokoro** text-to-speech, model `kokoro-v1.0.onnx`, voice `am_michael` | All narration: a synthetic voice reading Meena's script, run locally | Python package `kokoro-onnx`: MIT ("Copyright (c) 2025 github.com/thewh1teagle", package LICENSE). Model: "Apache-2.0" per the toolkit's `generate_audio_kokoro.py` docstring. The model's own licence file was not checked: **UNVERIFIED**. |
| **Manim Community** 0.20.1 | Rendered the 21 drawn scenes in `scenes.py` | MIT (package metadata, `License-Expression: MIT`) |
| **Remotion** | Rendered the two toolkit cards (BDEFS, BHTF) | Remotion License: the Free License covers "an individual … a for-profit organization with up to 3 employees … a non-profit" (`node_modules/remotion/LICENSE.md`) |
| **ffmpeg / ffprobe** | Encoding, audio padding, measurement, checks | Not checked: **UNVERIFIED** (a tool; nothing of it appears in the film) |
| **Google Chrome** | Headless renderer for the Remotion cards (local) | Not checked: **UNVERIFIED** (a tool; nothing of it appears in the film) |
| **EB Garamond** font (`fonts/EBGaramond-Regular.ttf`) | All drawn text and labels | SIL Open Font License 1.1, "Copyright 2017 The EB Garamond Project Authors". Licence included as `fonts/EBGaramond-OFL.txt`. |
| **Franklindot04/ecommerce-api** (via Meena's repository) | File names and line ranges depicted on screen | MIT License, "Copyright (c) 2025 Ajero Franklin" (`corpus/docs/LICENSE` in Meena's repository) |

## Made by Meena

- **The project:** the Cite & Seek repository (`github.com/meenuviji/cite-and-seek`), its frozen 53-question test set and 10 synthetic incidents (tag v0.0), the baseline pipeline (tag v0.1), and its decision log.
- **The project decisions:** scope, the target role, the hypothesis, the risk, and every approval in this build.
- **Narration she wrote, verbatim or in her specified wording:** BIDEA and B00 (introduction), B01 and B02 (hypothesis), B03 (data description), B09 (the alternative), the first sentence of B10 (target role), B14 (built so far) and B16 (why this project).
- **Segment names and the B10 subheading.**
- **The retrieval evidence:** `evidence/v0.1-search-2026-10-11.txt`, saved 2026-10-11.
- **Verification** of the test-set counts (53 / 45 / 8), 2026-10-11.

## What Claude contributed

**Claude Code** (Anthropic; model Claude Opus 5.5), working under Meena's direction on 2026-10-11 and 2026-10-12:

- **Facts and audits:**
  - Extracted facts from Meena's repository read-only into `REPO-FACTS.md`.
  - Audited the Brutalist toolkit read-only.
  - Wrote this submission's `REQUIREMENTS-AUDIT.md`.
- **Drafting:**
  - Drafted `PROJECT-BRIEF.md`, which Meena then edited.
  - Drafted the narration for BDEFS, B04, B05, B06, B07, B08, the second sentence of B10, B11, B12, B13, B15, BHTF and BOUT. Meena approved each.
  - Proposed, during the requirements audit, the additions Meena approved on 2026-10-12: B07's course-terms sentence, the new beats B07B (what a reviewer could conclude) and B09B (what Cite & Seek does instead), "in their first minute" in B10, and "in a public GitHub repository" in B15.
- **Code and paperwork:**
  - Wrote `make_sheet.py`, `scenes.py` (all drawings) and `finish_audio.py`.
  - Wrote `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `README.md`, `BUILD-PROMPT.md` and this file.
- **Build:** ran the toolkit, the narration, the renders and every gate, and kept `BUILD-LOG.txt`.
- **A mistake, disclosed:** on 2026-10-11 Claude read `evaluation/README.md` in Meena's repository with a shell command. That broke the repository's read-deny rule, which covers Claude's Read tool but not shell commands. The file holds methodology and counts, not golden answers. Meena then required every deny rule to apply to every tool.

**claude.ai** drafted `PITCH-MATERIAL.md` from Meena's notes on 2026-10-11 (her statement). It was not used as a source for the film; `REPO-FACTS.md` and the repository took precedence.
