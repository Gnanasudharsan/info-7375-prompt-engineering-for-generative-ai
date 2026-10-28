# FRICTIONAL — honest build log (Final Project Pitch Film)

Dates are local. Each entry: what I tried → what broke or changed → what I did instead.

## 2026-10-11
- First direction: build the pitch on my Reallocation Engine recipe (PR #28, `swe-network-targets`),
  since its own TODO list was a ready roadmap.

## 2026-10-14
- **Deadline moved up to tonight 23:59.** The brief's five-day shape is compressed into one evening.
- **Changed the project** (the brief allows this): from the Reallocation Engine extension to
  **Source Check for Support AI**, a workflow that checks a support bot's policy answers against current
  policy before they are sent. Reason: I wanted a project that applies to companies in general, not
  only to the course's engine.
- **Researched real problems before choosing.** Most search results for "automation pain points" were
  vendor marketing, which the honesty rule doesn't let me use as evidence. I kept only sources I could
  stand behind: the *Moffatt v. Air Canada* tribunal ruling (Feb 2024), and the alternatives' own public
  pages, checked 2026-10-14.
- **Zendesk:** I could only find third-party guides describing Zendesk AI agents, not Zendesk's own
  docs, so the brief says that explicitly instead of making a claim about the product.
- My project folders were reorganised (`Week_1/`, `Reallocation_Engine/`), so I re-pointed the tooling
  copied from Week 1.
- **Kokoro audio padding hung.** `ffmpeg` waits on stdin when run in the background; I had left out
  `-nostdin`. Killed it and re-padded with `-nostdin`.
- **Disk at 92% again (16 GB free)** — the condition that made iCloud offload the toolkit last time.
  Noted; the run completed.
- **Gate B** rejected a strike-through line drawn across a label (B11). Replaced it with an ✕ beside it.
- **GATE T blocked the final three times** (B06 overlapping prop plates; BOUT terracotta contrast;
  BDEFS a row caught mid-animation, then 40 px lowercase words). Fixed each in the content, not by
  loosening the gate: the toolkit exempts its own outro by name, and I chose not to add my copy to that list.
- **My own frame check caught what no gate did:** the "proposed design" tag also sat on beats showing
  real things (alternatives, my skills, what exists today). Removed it there.

## 2026-10-14 — submitting
- The toolkit patch failed to apply to the newest upstream (`4115560`): upstream had changed the two
  smoke-test files. They now contain the same fix I had made, so I dropped those hunks; the scene changes
  still apply cleanly.
- My name still comes out "Mayunk" in Kokoro. Accepted for today; noted for later films.

## 2026-10-22 — resubmission (v3)

### In my own words
_Written by Mayank on 2026-10-25, in his words (typos fixed). The fourth answer was assembled by Claude from Mayank's own messages that day, at his request, and confirmed by him: AI organized the notes, the experience is his._

- **Why I switched from the Reallocation Engine to Source Check:** I wanted my final project to stand out in the real world and not be another project for my portfolio. One thing I noticed is that AI is making people lazy (I've encountered myself to be one of them). As this AI age progresses, I wanted to make sure the source I'm blindly trusting is trustworthy.
- **What I thought when I read the 41/50 feedback, and what I agree or disagree with:** Displaying my name (@Mayank) in the video at all times is an important point, as viewers should know the name of the creator. On making it more detailed: I feel it lacked a few details, which made it a little hard to understand. From the TA's review: I missed that FRICTIONAL.md should have been in my own words, and that there should be 2 more cases along with the Air Canada case for better understanding.
- **What I decided in this resubmission, and what I let Claude do:** I rewrote FRICTIONAL.md in my own words, brought all the feedback to Claude and asked it to edit the video again for more details and an easy explanation. I also gave it the HyperFrames edit kit (Claude Code skills to edit videos), and started building the final project. Claude built the narration, the scenes, the checker and the tests. The full list of changes, and my verdict on each, is in the table below.
- **What I checked myself (the cut, the slice code), and what I still don't understand:** I watched the v3 cut and asked for three changes: remove "solo project" and "aiming for AI engineering roles", expand on Intercom Fin and Zendesk AI agents, and cut short the irrelevant explanation. I reviewed checker.py with Claude walking me through it function by function. I would fix these two: the contract was not fully enforced (the code checked for missing fields but did not reject extra fields, even though the comment says "exactly these fields"), and current_version picked the newest policy even if it had not taken effect yet. Both are fixed now, with tests (21 pass).

### Claude's record of the build (facts, for traceability)
- The feedback was mapped to beats (SHOTLIST.md). Every professor and TA point has a beat or a file.
- The TA's next step was built first, in `slice/`. Expected: the Air Canada case returns HOLD. Happened: 15/15 tests pass (`slice/evidence/pytest_2026-10-22.txt`).
- **Checked that the tests can fail:** a deliberate break (ignore the relation word and the anchor) made 6 tests fail and 9 pass (`slice/evidence/mutation_2026-10-22.txt`). Without this check, a checker that passed everything could have looked fine.
- **Narration too long:** the first v3 script was 847 words (~4:35). It was cut to 744 words (239 s), keeping every feedback point.
- **Pronunciation:** Kokoro read "Bhadrasen" as "Bad-ray-sun". It is now respelled "Buh-druh-sen" in `runtime/pronunciation/mayank.json`. Whisper now hears "my young Bud Rusen", still imperfect. Mayank's voice clone (Chatterbox) is too slow on this Mac (about 4 h for 4 min), so Kokoro stays.
- **A shell quirk broke the beat renumbering once:** zsh does not word-split `set -- $p`, so the first rename did nothing. It was redone under `bash -c`.
- **Two renderers wrote the same beat sheet:** the HyperFrames render overwrote the Remotion provenance. `hyperframes_scenes.py` now re-reads the sheet before writing. The bookends were re-stamped.
- **Layout check on draft frames:** content sat in the top half, the "wrong" stamp covered the bubble text, and a terminal comment wrapped. Fixed before the high-quality render.

### Every change to the film, v1 → v3 (Claude's record; the last column is Mayank's)

| # | Change | Asked for by | Made by | Mayank's verdict (accepted / changed / rejected) |
|---|---|---|---|---|
| 1 | @Mayank shown bottom-right on every frame, done in the toolkit so all future videos get it | Professor (points 1 and 4) | Claude | no change requested after reviewing the v3 cut |
| 2 | New narration: 17 beats, 744 words, about 4 min (cut down from an 847-word first draft for length) | Professor (more detail), TA (concise) | Claude | no change requested after reviewing the v3 cut |
| 3 | New "Who is doing it" beat: my name, degree, solo project, me vs Claude | TA (who is doing it) | Claude | no change requested after reviewing the v3 cut |
| 4 | New "The idea, simply" beat (robot helper, checker at the door, rule book); the terms card was removed | TA (explain it to a five-year-old) | Claude | no change requested after reviewing the v3 cut |
| 5 | Air Canada case drawn as the chatbot's words beside the policy line, with "after" and "before" marked | TA (P6, shown not asserted) | Claude | no change requested after reviewing the v3 cut |
| 6 | New "why it matters" beat: one wrong rule repeated to every customer, transcripts reviewed only afterwards | Professor (why is it a problem) | Claude | no change requested after reviewing the v3 cut |
| 7 | Technical beats: five-step architecture, the JSON claim contract, the field-by-field check, pass/hold with a Slack mock-up | Professor (more detail), TA (full technical detail) | Claude | no change requested after reviewing the v3 cut |
| 8 | The TA's next step built and shown with real output: Air Canada case + two condition flips + 4 more cases, 15/15 tests pass, deliberate break makes 6 fail | TA (next step) | Claude (code, tests, runs) | no change requested after reviewing the v3 cut |
| 9 | Every body beat labelled `real case`, `real output` or `proposed design` | Claude (keeps the honesty rule visible) | Claude | no change requested after reviewing the v3 cut |
| 10 | Body scenes rebuilt in HyperFrames instead of the generic Manim props | Mayank (asked to use HyperFrames) | Claude | no change requested after reviewing the v3 cut |
| 11 | Captions burned in | Claude (for non-technical and muted viewers) | Claude | no change requested after reviewing the v3 cut |
| 12 | "Bhadrasen" respelled so the Kokoro voice says it closer to right; still the Kokoro voice, not mine | Claude (my voice clone was too slow) | Claude | no change requested after reviewing the v3 cut |
| 13 | Fixes found by the toolkit checks: a low-contrast box border (B02), a stamp covering text (BKID), the @Mayank chip vanishing after the first beat | Toolkit gates / frame checks | Claude | no change requested after reviewing the v3 cut |
| 14 | Loudness raised from -24.5 to -16 LUFS | Claude (the first master was too quiet) | Claude | no change requested after reviewing the v3 cut |
| 15 | v3.1: removed "solo project" and "aiming for AI automation engineer roles" from the video | Mayank | Claude | asked for it |
| 16 | v3.1: expanded the Intercom Fin and Zendesk explanation (Zendesk now from its own docs) | Mayank | Claude | asked for it |
| 17 | v3.1: cut the "why me" self-promotion line and shortened "what it will prove"; kept "who opens it" because the pitch requires it | Mayank (cut irrelevant parts) | Claude (chose which parts) | asked for it; result in v3.1 |
| 18 | v3.1: checker rejects extra fields and ignores future-dated policies; 21 tests; three deliberate breaks shown in B07 | Mayank (found the two gaps in review) | Claude (code and tests) | asked for it |

### 2026-10-25 — v3.1 (Claude's record)
- Mayank reviewed `checker.py` with a function-by-function walkthrough and picked two gaps to fix: extra fields in a claim were not rejected, and `current_version` treated a future-dated policy as current.
- Fixed in `checker.py`: `check_claim` now rejects missing **or extra** fields; `current_version` takes today's date and ignores versions not yet in effect; a claim matching a not-yet-effective version is held with its own reason. Two cases added (`extra_field`, `future_policy`) and a March 2027 refund policy. Tests pin the date. Result: 21/21 pass (`slice/evidence/pytest_2026-10-25.txt`).
- Checked that the new tests can fail: three deliberate breaks made 6, 6 and 2 tests fail (`slice/evidence/mutation_2026-10-25.txt`).
- Video v3.1 (Mayank's requests): removed "solo project" and the target role from BWHO; expanded B08 with what Intercom Fin and Zendesk's AI agents actually do, re-reading fin.ai and Zendesk's own help center (v1 could only cite a third-party guide for Zendesk); left out the vendors' resolution-rate figures as unverified marketing claims; shortened B10 and B12; B07 now shows 21 tests and the three breaks.
