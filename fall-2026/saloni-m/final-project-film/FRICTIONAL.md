# FRICTIONAL.md

Saloni Mathure — INFO 7375, Final Project Pitch Film (OPT Countdown)

A dated log of what I tried, what I expected, what went wrong and what changed. The hands-on work was done by Claude Code in a session I directed. Each entry says who decided what.

---

## 2026-10-13 — Choosing the project

I chose to grow my Reallocation Engine recipe (opt-countdown) into the final project. The assignment lists "a recipe for your own domain in the Reallocation Engine" as a valid project, and this one already has a prototype I can show. That means the film can point at real output instead of mock-ups.

**Privacy decision:** the film and the repo describe the tool's user as "a student on OPT" and use the fictional persona from the prototype. They do not state my own visa status.

## 2026-10-13 — Re-running the prototype before filming

**Expected:** the 12 tests still pass, and the worked run gives the same decisions as on 2026-10-03.
**Observed:** 12/12 pass on Node 20.20.2. The run printed the same decisions (Apply 1 · Consider 2 · Skip 3 · Blocked 2, runway 53 days). It also rewrote four committed report files. `git diff` showed that each changed in exactly one line, the timestamp. I restored them with `git checkout -- course/`.
**Changed:** the film's B01 tag says "real run · 2026-10-13", and the output is saved in `evidence/rerun-2026-10-13.txt`.

**Friction:** the default `node` on my machine is 18.10. The prototype and Remotion need Node 20, so every command uses `~/.nvm/versions/node/v20.20.2/bin`.

## 2026-10-13 — The toolkit's default narrator is the instructor's persona

The show-tell skill narrates as "Liam, in for Bear" (Kokoro `am_onyx`), opens with "This is Liam, in for Bear", and ends with "At Nik Bear Brown". The assignment says to narrate as myself and not use the instructor's name, persona or credit line.
**Changed:** I chose the Kokoro voice `af_heart`, and the narration opens with "Hi, I'm Saloni." Nothing in the film says Liam or Bear.

## 2026-10-13 — The stock outro hardcodes the instructor's handle

`ClaudeTitleOutro.tsx` line 19: `const HANDLE = '@NikBearBrown'`, with "HARDCODED — no prop, no lookup, no override". There is no way to use it without the instructor's credit line.
**Changed:** the outro (BOUT) is my own Manim card: the title, my name, the course and the date. Because of this, the toolkit's optional `bookend_check.py` reports the outro as non-standard. I ran it and kept its report (see the gates entry). This is a deliberate deviation, not a render failure. `bookend_check.py` isn't called by `art run` at this toolkit commit.

## 2026-10-13 — Show-tell's "key terms" card doesn't exist at this toolkit commit

The skill says the second beat is `ClaudeDefinitions`. `grep -rl ClaudeDefinitions runtime/` found nothing at commit `cd4bf20`, because it was added in a later commit.
**Changed:** I dropped that beat and define each term in the narration the first time it's used ("H one B record, which is its history of sponsoring work visas"). I kept commit `cd4bf20` rather than updating the toolkit, because my Week 1 film was built and rebuilt byte-identically on it.

## 2026-10-13 — Existing skills: the prototype can't be my evidence

The prototype's own FRICTIONAL says Claude Code did most of the hands-on work. So "I already know Node, look at the prototype" would overclaim.
**Changed:** I named JavaScript/Node as an existing skill and used my public INFO 6150 team project, CodeBuddies (Node/Express), as the evidence. The film says aloud that Claude Code did most of the typing on the prototype.

## 2026-10-13 — Pronunciation

I spelled out acronyms in the narration: "O P T", "H one B", "D S O", "read me", "four oh four". The skill recommends a Whisper transcript to check them, but no Whisper model was downloaded on this machine and I did not download one. **Not done:** an automated pronunciation check. Instead, I listen to the whole film myself before submitting (see the last entry).

## 2026-10-13 — Stills and pre-audits

The first contact sheet of last-frame stills showed four layout problems: "not proven" overlapping "no record → blocked" in B07, checks touching their labels in B08, a stray card in B09, and the outro rule running through the title. All four were fixed before the 4K render.
Pre-audit after the fixes: Gate A (`static_scene_check.py`) was clean on 12/12 scenes, and the layout audit (`manim_layout_audit.py --curve-strict`) was clean on 12/12.

## 2026-10-13 — First 4K render: Gate V failed

**Expected:** clean, because the pre-audits were clean.
**Observed:** `art run` compiled the film (225.7 s), but Gate V reported 4 MAJOR defects: low contrast at the midpoint of B05 (0.22 < 0.30) and of B07 (0.26 and 0.30), and an "empty frame" at the midpoint of B09. Gate V averages every non-background pixel. B05's pale 90-day bar and B07's pale report page pulled the average down. B09 had only one line of text on screen at its midpoint, because the axis waited for the narration.
**Changed:** darker bar fills in B05; a dark title bar on the report page and darker pills in B07; B09's axis is drawn from the first second. I re-rendered only those three scenes. I did **not** use `ART_STRICT=0` to wave the defects through.
**Result:** Gate V `BLOCKER=0 MAJOR=0`.

## 2026-10-13 — The opener's correction never fired

**Observed:** frames from the first master showed the opener still reading "Which jobs can I apply to?" at the end of the beat. The correction to "start in time" never happened. `BrutalistHesitantWriter.tsx` matches triggers **one word at a time** (`triggers.indexOf(core)`), so the two-word trigger "apply to" could never match. No gate caught this. I found it only by looking at frames.
**Changed:** the question is now "Which jobs can I get?", with the trigger "get" corrected to "start in time". I updated the narration to match and re-voiced only that beat (`--only BIDEA`, 16.85 s).
**Result:** the opener now ends on "Which jobs can I start in time?". The correction happens before the narration reaches that line, which I accepted as a small mismatch.

## 2026-10-13 — Final gates

- Gate A (static pre-flight): 12/12 clean.
- Layout audit: clean (`reel/layout_audit.md`).
- Gate V / render integrity (`final_frame_check.py`, 26 frames): BLOCKER 0, MAJOR 0 (`reel/_qc/REPORT.md`).
- GATE T (type check): PASS, 13/13 beats, 0 FAILs (`reel/TYPECHECK.md`).
- Master: `status: ready`, 3840×2160, 225.25 s, sha256 `66f6cf5d…` matches `video.mp4` (`reel/_qc/opt-countdown-pitch.verified.json`).
- `bookend_check.py`: **fails on purpose**, two failures, both about the outro not being the stock `ClaudeTitleOutro` (`reel/bookend_check.txt`). See the outro entry above.
- Skin lint warnings (advisory): the opener isn't `ClaudeComposerAsk` and the outro isn't `ClaudeTitleOutro`. Both are deliberate.

## 2026-10-13 — Before submitting (my checklist)

- [ ] Watch and listen to the whole film once, and check that the acronyms sound right ("O P T", "H one B", "D S O").
- [ ] Re-read PROJECT-BRIEF.md and confirm every sentence is mine to defend.
- [ ] Push the GitHub folder, then put the folder link and the commit hash in Canvas.
