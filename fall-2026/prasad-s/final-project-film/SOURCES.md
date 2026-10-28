# SOURCES

## What I produced (with Claude's help; details in the next section)
PROJECT-BRIEF.md, beat_sheet.json, make_sheet.py, scenes.py (apart from the
drawing kit listed below), FACTCHECK.md, SHOTLIST.md, PROMPTS.md, GATE-LOG.md,
FRICTIONAL.md, README.md, BUILD-PROMPT.md, SOURCES.md, and the film. No images,
music, stock footage or other media files were imported; every picture is drawn
in code. All mandates and examples shown are constructed, with no real payment
data. The narration voice is synthetic.

## What Claude contributed
Claude (Anthropic) contributed: project brainstorming and web research; first
drafts of PROJECT-BRIEF.md, the FRICTIONAL.md entries (the three dated 10/08,
the prediction entry and the later entries), the beat outline and narration
text, FACTCHECK.md, SHOTLIST.md, PROMPTS.md, GATE-LOG.md, README.md, SOURCES.md
and BUILD-PROMPT.md (reviewed, edited and approved by me); the code in
make_sheet.py and scenes.py, written by Claude Code after the toolkit's drawing
kit; and Claude Code actions for file setup, git staging, commits and builds.
Commits made through Claude Code carry a Co-Authored-By trailer. I made the
decisions on the project, its scope and the wording, and reviewed each result.
No Claude response is shown in the film.

## Sources I read
- Google, "Powering AI commerce with the new Agent Payments Protocol (AP2)",
  Sept 16, 2025. Read Oct 8-9, 2026 (exact day not recorded).
- PayPal, "Agent Payments Protocol: Building Verifiable Trust for Agentic
  Commerce" (Prakhar Mehrotra), Sept 16, 2025. Read Oct 8-9, 2026 (exact day
  not recorded).
- AP2 specification, v0.2 main page, at ap2-protocol.org. Opened 10/08/2026.
  I did not read the spec's other pages.
- The README of AP2's GitHub repository (code samples and demos). Read only; no
  code from it is used.
- github.com/shruti-khomne-7/razorpay-mandate-mirror, "Mandate Mirror", a
  project built for the Razorpay AI Buildathon 2026. README only, opened
  10/08/2026; I did not read the code. Licence: not checked.
- The course repository, for my own Assignment 1 commits shown in B12.

## Third-party tools and assets (and licences)
- Brutalist toolkit: github.com/nikbearbrown/brutalist.art, revision
  22264a332f6bf8825cdd639bcd33864563801f55 (Oct 3, 2026), the course toolkit.
  Licence: no LICENSE file found; the toolkit's own docs say "No LICENSE".
  My local checkout has changes from Assignment 1: a patch to
  runtime/scripts/compile.py (not needed for this film, which ran with strict
  gates and no overrides), a regenerated package-lock.json, and ten deleted
  example files that trip ./setup's ElevenLabs guard. The film does not use
  any of them.
- Drawing kit: the first 144 lines of scenes.py are the toolkit's
  skills/make/show-tell/templates/iso_kit.py, pasted unchanged. Licence: same
  as the toolkit (none found).
- Kokoro (kokoro-onnx 0.6.1, Python package): MIT, Copyright 2025 thewh1teagle.
  Model weights (kokoro-v1.0.onnx, voices-v1.0.bin), downloaded by the
  toolkit's setup from the kokoro-onnx releases. Weights licence: none stated
  in the toolkit's docs; I did not check the model's release page. Voice used:
  af_bella, a synthetic text-to-speech voice running locally. The toolkit's
  README and HOW-TO.md disagree on whether the model ships in the repo.
- Manim 0.18.1 (MIT, from the installed package's metadata).
- Font: EB Garamond, bundled in the toolkit, SIL Open Font License 1.1,
  Copyright 2017 The EB Garamond Project Authors.
- Installed by the toolkit but not used in the film: Remotion 4.0.486 (its
  licence is not open source; it is free for individuals and small
  organisations), and the Oswald font. The final film has no Remotion scenes.
- ffmpeg and Node 20, used as build tools.
