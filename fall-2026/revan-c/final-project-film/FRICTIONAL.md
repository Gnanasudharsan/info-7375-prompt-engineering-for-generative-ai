# FRICTIONAL — what went wrong, and what I did

## In my words — why I made each decision (Revan, answered 2026-10-25)

*Note by Claude: after grading, Claude asked me these questions in our session and I typed the answers.
The answers are mine. Claude fixed only spelling, capitals and four small grammar slips ("working or
created" → "working on or created", "this upcoming" → "these upcoming", "it will again would save" → "it
would again save", "amount of to be sent" → "the amount to be sent"), and set each answer under its question. For the last two answers (end card and feedback), Claude first offered example
reasons; I then answered in my own words on 2026-10-25, and Claude added only punctuation.
The decisions themselves were made on 2026-10-14 unless marked otherwise.*

**2026-10-14 · Voice: why a synthetic Kokoro voice instead of recording my own?**
Easier and faster, I didn't want to record, and also Claude suggested it and I went with it because it is easier.

**2026-10-14 · Why I removed the "I'll ask MIT DCI first" part**
Because I don't need to ask them, as I was the one who was working on or created this project, and it is kind of open sourced.

**2026-10-14 · Why I added researchers and policymakers as people who'd open it**
Because this kind of data is very relevant to them in these upcoming payments networks, and stuff like keeping track of upcoming stablecoin payments.

**2026-10-14 · Why I switched from my full name to "Revan C" before pushing**
I switched because the course repo's `fall-2026/README.md` says "No IDs and no full names are stored here."

**2026-10-14 · Why I pushed straight to `main` instead of opening a pull request**
I didn't think about it much and followed what I did in Week 01.

**2026-10-14 · The toolkit's end card always shows the instructor's handle, so the film ends on my own card and the toolkit's bookend check fails. Do I agree with that trade-off?**
I agree. I feel like ending with my name makes it much more clear and who is gonna build that project, and you know, like the name of the agent and stuff makes more sense.

**2026-10-14 · Why this project: why Remnix, and why build on Money Map?**
Since I have built Money Map, I think if we build something like this, Remnix, it would again save time for somebody who would have to select countries and the amount to be sent and everything. They can just know what are the amounts of payments they can make to other countries and stuff. It would be an interesting way to use the data of Money Map.

**2026-10-25 · The TA's feedback: is there anything I'd push back on, and what do I think of it?**
No. I think the authorship comment is also kind of fair because the film, like, indicated that the words are mine, but actually Claude helped me to script it, yeah. Also, I may be using the next step given there and start building on it afterwards, later, soon.

---

## Build log (drafted by Claude from the session's logs, 2026-10-14)

*These entries were written by Claude, not by me. They record what happened in the build session on
**2026-10-14** (times are local EDT, from file timestamps and logs). Nothing is invented. "I" in them means
me (Revan), but the wording is Claude's. Claude Code ran the commands and wrote the fixes in my session,
as described in SOURCES.md.*

---

**2026-10-14 · ~16:10 — `./setup` fails on a fresh clone.**
I ran the toolkit's readiness check right after cloning, and it stopped with "ElevenLabs reference found —
this toolkit is Kokoro-only" and exit code 1. The ten flagged files are example films inside the toolkit's own
`youtube/brutalist/` folder, not mine. It happened again after `./setup --install` (16:26): every download
finished, but the readiness table never printed. **What I did:** checked readiness by hand instead, with the
Python imports (Manim 0.20.1, ManimPango 0.6.1, kokoro-onnx, faster-whisper) and the toolkit's own Kokoro smoke test.

**2026-10-14 · ~16:20 — My brief claimed something Money Map already does.**
The first draft of the brief said a sender "can't ask a follow-up like 'what if I pay by debit card?'". The
Money Map screenshot shows a **Debit Card** filter, so that was wrong. **What I did:** replaced it with a
plain-words "why" question, in the brief and in beat B01, before anything was rendered. Logged in
`FACTCHECK.md` row 5.

**2026-10-14 · ~16:20 — Prices moved while I was making the film.**
Money Map's stablecoin route cost $7.42 for $1,000 when the page was first read (stablecoin prices "updated
15:10 EST"). In the screenshot taken at 16:20 EDT it was $8.99, and Wise ($7.54) had become cheapest. **What I
did:** kept the mock-up's numbers tied to the one dated screenshot. I then used the change itself as the
evidence for my project risk (beat B12): live prices make "known answers" go stale.

**2026-10-14 · 16:26 — Kokoro could not speak.**
The Kokoro smoke test failed with `Error processing file '/Users/runner/work/espeakng-loader/…/phontab'`. The
pip package `espeakng-loader` 0.2.4 looks for its data at a path from the machine it was built on. Two fixes
did not work: setting `ESPEAK_DATA_PATH`, and copying the data to a folder with no spaces and pointing
phonemizer at it. **What worked:** `brew install espeak-ng` (16:27) plus
`PHONEMIZER_ESPEAK_LIBRARY=/opt/homebrew/lib/libespeak-ng.dylib`, saved in `build/env.sh`. The smoke test then
passed (mean volume −21.7 dB).

**2026-10-14 · ~16:30 — First narration was 4:05, over the 4-minute limit.**
**What I did:** trimmed nine lines (612 words), which got it to 3:56, still too close. Then I used Kokoro's own
`--speed 1.05` option, which gave 3:49.

**2026-10-14 · ~16:30 — The show-tell template conflicts with the assignment.**
The skill's default bookends open with the instructor's stand-in narrator greeting, end on a spoken outro
with the instructor's channel handle, and use the instructor's portraits for any person. The outro card
(`ClaudeTitleOutro`) hard-codes the handle, with no way to change it. **What I did:** opened with my own
first-person greeting ("Hola. I'm Revan…"), drew my own end card in Manim, and showed no people.
I also dropped the Claude.ai "Your Turn" composer, so the film shows no Claude interface at all.
**Cost:** the toolkit's bookend check reports 2 failures on the outro. I left them failing rather than
editing data to satisfy the checker; see `gate-reports/GATE-SUMMARY.md`.

**2026-10-14 · ~16:36 — Layout audit caught two problems before rendering.**
B05's source label ran past the safe area, and B09's "step 1" label sat on a moving shape. **What I did:**
moved both, and re-audited until clean.

**2026-10-14 · 16:42 — Gate V failed the first full build.**
Two blocking defects: B00's screenshot filled 55% of the safe area (just under the minimum), and B07's World
Bank tag crossed the right safe edge. **What I did:** enlarged the screenshot, moved the tag, archived the
old clips in `_superseded/`, and re-rendered only those two beats. Gate V passed at 16:45 (0 blockers, 0 majors).

**2026-10-14 · 16:45 — The "synthetic voice" note was too small to read.**
I had put it in the opening card's banner, which the component draws at 18 px and 62% opacity. **What I did:**
moved it to the same component's 28 px full-ink label ("Synthetic voice (Kokoro) · words by Revan") and
re-rendered the opening (16:47).

**2026-10-14 · ~16:50 — Project change: data access is settled; three answers were missing.**
The film had said I would "ask the MIT Digital Currency Initiative first" whether I could use Money Map's
data. I can use it, so I removed that beat. Checking the film against the seven questions showed gaps:
- Q4 never said what a reviewer could conclude or what evidence would back it, so B13 was rewritten to say it.
- Q2 named alternatives but not the benefit to a sender, so B07 now says it.
- Q7 said "a mix" without why I picked the project, so B14 now says it, in a line I confirmed.

Five beats were re-voiced and re-rendered (17:03).

**2026-10-14 · ~17:10 — Second audience added.**
I added researchers and policymakers who study remittance costs as readers (B08 and brief Q3). The first
wording pushed the film to 3:57, so I shortened it to stay at 3:56. I did not claim Remnix covers other corridors:
it covers USD→Mexico only.

**2026-10-14 · 17:24 — The master check skipped its duration test.**
`master_check.py` passed, but its notes say the duration test was skipped because
`runtime/scripts/clock_check.py` is missing from the toolkit checkout. **What I did:** checked by hand. The
master was 235.8 s vs 235.5 s of measured narration, the last 0.9 s is silent (−91 dB), and every clip is
within 0.05 s of its audio.

**2026-10-14 · ~17:30 — Honesty pass found lines that made Remnix sound built.**
Reading every narration sentence turned up:
- 7 lines that sounded built: present tense or no verb in B04, B07, B09, B10, B11 and B13, and B01's "senders
  *often* ask…", which is a claim about users with no data behind it.
- 2 drawings with check marks that looked like results (B09, B13).

**What I did:** changed them to "will", "might", "planned" and "how you'd know". Then I re-voiced 9 beats,
re-drew 8, rebuilt the master (17:36, 3:56) and re-ran every gate. All pass except the 2 intentional bookend items.

**2026-10-14 — Pronunciation was checked by ear, not by machine.**
The skill suggests a Whisper transcript to catch Kokoro mispronunciations. I didn't download a Whisper model.
I watched the review cut myself and asked for no pronunciation fixes.

**2026-10-14 · ~17:50 — My full name was in a folder that stores none.**
Before pushing, I read the course repo's `fall-2026/README.md`: "No IDs and no full names are stored here."
The film said and showed my full name (opening line, terms card, end card) and so did four documents. **What I
did:** switched everything to "Revan C", re-voiced and re-rendered the three beats that carry my name, rebuilt
the master and re-ran the gates, so the Canvas and GitHub copies stay identical. Only the Canvas zip's file
name keeps my last name, because the assignment requires it.

---

## Resubmission log (drafted by Claude, 2026-10-25)

*Written by Claude, not by me; "I" means me (Revan).*

**2026-10-25 — Grades came back with two deductions.** P6 (−0.5): the film said "the words are mine" and the
opening card said "words by Revan", but SOURCES.md said Claude drafted the narration. Frictional (−2): the log
was drafted by Claude, not in my own words. The TAs' class note also asked every film to say who is doing it,
explain the project simply, stay concise, and give full technical detail. **What I did:** removed the spoken
"the words are mine", changed the on-screen label to "written with Claude, reviewed by Revan", and answered
Claude's questions about my decisions in my own words at the top of this file. (A spoken version of the
credit was tried first; I chose to keep it on screen only so the opening could start with the project.)

**2026-10-25 — Some decisions had no reason from me yet.** For the voice, push route, bookend gate and the
feedback, my first answers were "idk", and for the push route I asked Claude to make something up. Claude
refused, because a made-up reason would repeat the problem the TA graded down. It showed me what the session
record said I had chosen, and I answered each one myself.

**2026-10-25 — Adding "who" and plain language pushed the film over 4:00.** The first rewrite was estimated at
about 4:05. **What I did:** dropped the terms card (its words are explained where they first come up), merged
the old B01 into B02, and trimmed seven lines. Measured runtime 3:50 before rendering; the master is 3:51.

**2026-10-25 — Layout audit caught one new problem before rendering.** In the new $500 beat, the "$500" label sat
on the top of the bill stack. Moved it up, re-audited clean, then rendered. Gate V passed on the first full run
(0 blockers, 0 majors).
