# SOURCES: ProductLens AI pitch film (resubmission)

Who made what, what was used, and under which licence. Everything is local and free: no paid generation, no API keys,
no media account.

## Who ran which test (one consistent record)
| Date | Test | Who ran it | Where |
|---|---|---|---|
| 2026-10-14 (00:18 UTC Oct 15) | Plain Claude ×3, CampusFit idea, planted "68%" stat | **Claude Code**, at Aditya's direction (CLI, `claude -p`) | `research/baseline-claude-run*.md` |
| 2026-10-14 (00:24 UTC Oct 15) | Logged-out ChatGPT ×1, same prompt | **Claude Code**, at Aditya's direction (the Claude app's built-in browser) | `research/baseline-chatgpt.md` |
| **2026-10-25, 6:24 PM** | **ChatGPT (Aditya's Plus account), shoe-store checkout idea, planted Baymard claim** | **Aditya, himself, in his own browser** | `research/baseline-v2-*` |

The first FRICTIONAL log wrongly said Aditya ran the Oct 14 ChatGPT test; that log was drafted by Claude and is now
`BUILD-LOG.md`. This table is the correct record.

## What Aditya made
- **Both project ideas:** AI Product Failure Lab (first pitch) and ProductLens AI (this pitch).
- **The ProductLens script:** written by Aditya and refined with ChatGPT (`ProductLens_AI_Video_Pitch_Script.docx`).
- **The Oct 25 ChatGPT test** and its five screenshots.
- **FRICTIONAL.md:** his own answers, typed in chat on Oct 25 and arranged by Claude without rewording (verbatim:
  `research/frictional-answers-raw.md`).
- **Every decision:** the pivot, the merge, approving the final script, the voice, and his name's pronunciation.

## What ChatGPT contributed
- Refining Aditya's ProductLens script; the first pitch's blueprint and storyboard docs (Oct 14).
- The answers it gave in the tests above (real responses, dated).

## What Claude (Claude Code, model claude-opus-5-5) contributed
- **Review** of Aditya's ProductLens script against the assignment and the grader's feedback, plus the **merged script v2**
  (`SCRIPT-v2.md`), which Aditya approved on Oct 25.
- **Designing the planted Baymard claim** and checking Baymard's real article (Apr 26, 2011, baymard.com/blog/one-page-checkout).
- **Running the Oct 14 tests** (table above), and recording the **factual results** of Aditya's Oct 25 run from his screenshots
  (labelled as Claude's reading in `research/baseline-v2-prompt.md`).
- **Cropping the screenshots** (`prepare_crops.py`): cut to the conversation, colours inverted, enlarged. Nothing retouched.
  The crops leave out the ChatGPT sidebar, which shows private chat titles.
- **Code and docs:** `make_sheet.py`, `scenes_body.py`, `prepare_crops.py`, PROJECT-BRIEF.md, FACTCHECK.md, SHOTLIST.md,
  README.md, BUILD-PROMPT.md and BUILD-LOG.md. Aditya reviewed them.

## Alternatives cited
- **DimeADozen**: dimeadozen.ai homepage and example-reports page, read 2026-10-14.
- **ValidatorAI**: validatorai.com homepage, read 2026-10-25 ("validate startup, product and small business ideas").
- Neither tool's paid report was bought, so the film makes no claim about their quality.

## Toolkit and assets (third party)
| What | Source | Licence / terms |
|---|---|---|
| Brutalist toolkit (show-tell skill, iso drawing kit, 25 original props, Remotion bookends, QC gates) | github.com/nikbearbrown/brutalist.art, commit `519fcbb` | Course toolkit, used per the assignment. The instructor's persona, name and credit line are **not** used. |
| Kokoro-82M voice model, voice `am_michael` | kokoro-onnx model files v1.0 | Apache-2.0 |
| Manim Community 0.18.1 | manim.community | MIT |
| Remotion 4 | remotion.dev | Remotion licence (free for individuals) |
| EB Garamond, Lato fonts | bundled with the toolkit | SIL Open Font License |
| faster-whisper (transcript check only) | github.com/SYSTRAN/faster-whisper | MIT |
| ChatGPT screenshot crops | Aditya's own screenshots of his own chat, 2026-10-25 | Aditya's own material |

**The voice is synthetic.** A local Kokoro voice reads Aditya's approved script in the first person; it isn't his recorded voice.

## Not included
No résumé, contacts, application tracker or private transcripts. The uncropped screenshots (with the private sidebar) are
kept outside the repo. The shoe store, CampusFit and both planted claims are made up on purpose and labelled as such.

## Correction to the first submission
The v1 film's outro card showed the instructor's handle "@NikBearBrown". The toolkit card hard-codes it, and Claude
didn't catch it before the first submission. This film uses its own outro with Aditya's name (`reports/bookend-check.txt`).
