# Sources

**Film:** Terraform Docs, Quoted (final project pitch)
**Author:** Varnika M · INFO 7375
**Status:** final film rendered 2026-10-14.

## 1. Disclosures

**Narration.** A synthetic computer voice (Kokoro, generated locally, free), chosen by me on
2026-10-11. It is not my voice or any real person's. Voice: Kokoro `am_onyx`, the same stock voice as my Week 01 video. The toolkit also uses this voice for the instructor's "Liam" narrator; this film uses none of that persona (no name, greeting or credit line). The narration is first person, as me. It
does not use the instructor's name, persona, or credit line.

**Claude output.** Beat B07 shows one real Claude reply: claude.ai, Sonnet 5.5 (Medium), Free
plan, 2026-10-11, to the question "Is the bucket argument required on aws_s3_bucket in
Terraform?" It is my own screenshot, cropped to remove my chat sidebar; the reply text is
unchanged (`evidence/alternatives/2026-10-11_claude-ai_sonnet-5-5_answer_cropped.png`). It is
shown with its date on screen. No other Claude reply appears.

**Constructed material.** Every drawing of the planned tool, repository, tests and evaluation is
labelled PLANNED · CONSTRUCTED on screen. The docs lines in B03, B04 and B11 are real and carry a
source tag.

## 2. Sources used

| Source | Used for |
|---|---|
| Terraform AWS provider docs, `website/docs/r/s3_bucket.html.markdown`, `hashicorp/terraform-provider-aws` commit `f4a1d213000a2032755ac7f05bbfd46f8b909255` (identical to tag `v6.68.0`), fetched 2026-10-11. https://github.com/hashicorp/terraform-provider-aws | Lines 54, 70, 221 shown in B03, B04, B11 |
| GitHub repository metadata for `hashicorp/terraform`, `hashicorp/terraform-provider-aws`, `hashicorp/web-unified-docs`, `opentofu/opentofu`, fetched 2026-10-11 | The licence check (`evidence/licence-check.txt`) |
| Assignment brief, "Final Project Pitch Film — Show What You Will Build" (Canvas) | The seven questions, honesty rule and submission list |
| Brutalist toolkit, https://github.com/nikbearbrown/brutalist.art, revision `b21f6253a336098f3f55847a9525ae6868ccbdb7`, used unmodified | Show-tell format, the drawing kit pasted into `scenes.py`, narration audio, rendering, and the quality gates |

## 3. What I made

- `PROJECT-BRIEF.md`: the seven answers. Drafted by Claude Code; the facts in questions 2 and 7 (my trials of the alternatives, my experience) are mine
- `beat_sheet.json`: narration and visual plan
- `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`: the toolkit's required paperwork
- `make_sheet.py` (writes `beat_sheet.json`) and `scenes.py`: all 16 scenes, drawn in Manim. The kit block at the top is pasted from the toolkit's `skills/make/show-tell/templates/iso_kit.py`; the cast and scenes were written for this film
- The rendered film, `final/varnika-final-project-pitch.mp4`

## 4. Contributions

**Me:** chose the target role (AI Software Developer / Software Engineer), chose Terraform docs as
the topic after considering several document-Q&A ideas, asked for the brief to be drafted, tried
both alternatives myself on 2026-10-11 (the Registry page and claude.ai) and took the screenshots,
gave the facts for question 7 (my co-op and course experience), chose the voice, approved the
B07 narration and the fairer wording about the docs site menu, and asked for the "drafted by
Claude" notes to be removed from the brief. I watched the final cut on 2026-10-14 and approved it.

**Claude Code (NEU-provisioned):** explained the assignment in plain English; suggested project
ideas; checked the Terraform licences and saved the pinned docs page as evidence; found the
line 54 / line 221 `bucket` conflict used as the project's risk; checked Claude's reply line by line
against the docs and cropped my screenshot; drafted `PROJECT-BRIEF.md`,
`beat_sheet.json` and the supporting files in this folder; updated my Brutalist checkout on my
go-ahead; generated the narration; wrote `make_sheet.py` and `scenes.py`; rendered the film, ran
the toolkit's gates, and fixed what failed (details in `FRICTIONAL.md`).

No conversation transcripts are included.

## 5. Third-party material and licences

| Material | Licence |
|---|---|
| `evidence/aws-provider-docs/s3_bucket.html.markdown` | Mozilla Public License 2.0; licence text kept beside it in `evidence/aws-provider-docs/LICENSE`. Unmodified. |
| Brutalist toolkit (brutalist.art, `b21f625`) | No licence file in the repository (checked 2026-10-14). Used locally as the assignment directs; not copied into this folder, except the show-tell drawing-kit block pasted at the top of `scenes.py`, as the toolkit's show-tell instructions require. |
| Manim Community 0.18.1 | MIT |
| Kokoro-82M voice model via `kokoro-onnx` (voice `am_onyx`), run locally | Apache-2.0 (per the toolkit's `generate_audio_kokoro.py`) |
| faster-whisper 1.2.1, `base.en` model (pronunciation check only; not in the film) | MIT |
| FFmpeg 9.0.2 | LGPL/GPL |
| EB Garamond font | SIL Open Font License |
