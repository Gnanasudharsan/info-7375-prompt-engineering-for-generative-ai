# SOURCES

## What I used
| Item | Use | Licence / terms |
|---|---|---|
| *Moffatt v. Air Canada*, BC Civil Resolution Tribunal (Feb 2024), as reported by [CP/Yahoo](https://ca.news.yahoo.com/air-canada-must-pay-refund-040527669.html) and [Tom's Guide](https://www.tomsguide.com/ai/air-canada-tried-to-claim-it-wasnt-responsible-for-its-chatbots-false-promises-but-that-didnt-fly-in-court) | the real case in B00 and the brief | public ruling / news reports |
| [Intercom Fin public page](https://fin.ai/) (read 2026-10-14 and again 2026-10-25) | alternative described in B07 | public web page |
| [eesel.ai guide to Zendesk AI agent escalations](https://www.eesel.ai/blog/zendesk-ai-agent-escalations) | alternative described in B07 (third-party, not Zendesk's own docs) | public web page |
| brutalist.art toolkit, show-tell skill, its approved 25 original props, `BrutalistHesitantWriter`, `ClaudeDefinitions` | pipeline, drawings, bookends, quality gates | public course toolkit; no licence file |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` | narration, generated locally | Apache-2.0 |
| Manim Community 0.18.1 | the v1 drawings (not used in v3) | MIT |
| HyperFrames 0.7.109 (HeyGen), from my herk-edit-kit install | the 15 v3 body scenes and the caption edit pass | Apache-2.0 |
| GSAP 3.14.2 | animation inside the HyperFrames scenes | GSAP Standard "no charge" license |
| Inter, JetBrains Mono (embedded by HyperFrames) | type in the v3 scenes | SIL Open Font License 1.1 |
| pytest 8.4.2 | the slice's tests | MIT |
| Remotion 4 | the bookends (BIDEA, BOUT) | Remotion licence (free for individuals) |
| faster-whisper | word timings for scene cues and captions; checking pronunciation | MIT |
| EB Garamond (bundled in the toolkit) | type | SIL Open Font License 1.1 |

No stock footage, images, music, or paid services. No real customer, company or personal data.

## What I made
- PROJECT-BRIEF.md (the seven answers), the narration, and the beat sheet (`code/make_sheet.py`)
- the 14 drawn scenes (`code/scenes_body.py`), built on the toolkit's kit and props
- the reel-local outro `TcTitleOutro` (a copy of the toolkit's `ClaudeTitleOutro` with a handle prop, from my Week 1 film)

## What Claude contributed
Claude Code (Opus 5.5), on 2026-10-11 and 2026-10-14:
- researched candidate problems and sources; **I chose the problem (support AI with outdated policy answers)**
- drafted PROJECT-BRIEF.md from my answers to its questions (my target role, stack, existing skills, the
  alternatives I looked at); I reviewed and corrected it
- wrote the narration, the beat sheet, and the scene code, ran audio, rendering and gates, and fixed what failed
- drafted README, SOURCES, FACTCHECK, SHOTLIST and FRICTIONAL

I am responsible for every claim in the film and the brief.

## v3 (resubmission, 2026-10-22): who did what

| Part | Mayank | Claude Code (Opus 5.5) |
|---|---|---|
| Deciding to resubmit and what to fix | brought the professor's and TA's feedback, asked for the changes, asked to use HyperFrames | mapped each feedback point to a beat (SHOTLIST.md) |
| Narration v3 | _pending: Mayank reviews and approves the script_ | wrote it from the brief and the feedback; cut it from 847 to 744 words |
| The slice (`slice/`) | set the rule "anything unverifiable is a HOLD" (brief §6); reviewed the code with Claude's walkthrough on 2026-10-25 and found two gaps to fix (extra fields not rejected; future-dated policies treated as current) | wrote the checker, the cases and the tests (7 cases / 15 tests on 2026-10-22; 9 / 21 after the fixes on 2026-10-25); ran them and the deliberate break; saved the output |
| Scenes | _pending: watches the cut and accepts or asks for changes_ | wrote `code/hf_scenes.py` (15 HyperFrames scenes) and `code/hf_edit.py` (captions); ran the renders and the toolkit gates |
| Toolkit (@Mayank on every video) | the professor asked for it; Mayank asked Claude to do it | added the handle stamp to `compile.py` (reads `~/.config/brutalist/profile.json`), HyperFrames as a fill method, `hyperframes_scenes.py` |
| FRICTIONAL.md | the dated entries in his own words | logged the build facts, marked as Claude's record |

What I accepted, changed or rejected from Claude: _pending, in FRICTIONAL.md in my own words._

## v3.1 additions (2026-10-25)
| Item | Use | Licence / terms |
|---|---|---|
| [Zendesk: connecting knowledge sources to AI agents](https://support.zendesk.com/hc/en-us/articles/8357749301658-Connecting-knowledge-sources-to-power-generative-replies-in-AI-agents) and [customizing the Knowledge reply (escalation)](https://support.zendesk.com/hc/en-us/articles/10448933203994-Customizing-the-Knowledge-reply-in-an-AI-agent-with-agentic-AI) | the Zendesk card in B08, from Zendesk's own docs (replaces the v1 third-party guide) | public documentation |
