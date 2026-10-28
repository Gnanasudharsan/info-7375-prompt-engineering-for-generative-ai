## Executive summary

This is a dated log of what went wrong and what was decided while making a short video about a job-screening tool for a fictional international student. Read it to see why the video is built the way it is. Most of the friction came from the gap between a short script and a target length, from the voice mispronouncing names, and from text that would not fit on screen. None of it came from the facts, which were all traced to files before anything was drawn.


## 2026-10-21 — mode video

1. **Finding the right folders.** Two toolkit checkouts exist. `~/brutalist-v2` is the working one, at `b21f625`. `~/Downloads/brutalist` is the old one, with 8,445 tracked files showing as deleted. The video used `brutalist-v2` only. Two course-repo clones exist too. The current one, `~/info-7375-prompt-engineering-for-generative-ai`, holds my Week 1 and final-project folders, so this video sits next to them.
2. **Changes panel.** The app's Changes panel showed −293,890 lines on "main". That is the old `~/Downloads/brutalist` checkout (the session's starting folder), not anything this video touched. Nothing was committed, discarded or reverted there.
3. **Conventions.** I followed my final-project film rather than the skill defaults:
   - Kokoro `af_bella` in the first person, not the instructor's Liam voice;
   - no instructor bookends, with beat 8 as a drawn outro;
   - the same drawing kit, copied into `scenes.py`.
4. **The script was too short for the target.** At speed 1.04 the eight beats measured 2:50.5, and the target was 3:45–3:55. Filling that with pauses only between beats would have meant about 7 s of silence at each boundary. I chose sentence pauses instead. Measured results:
   - speed 1.0 with 1.0 s pauses: 3:30.8;
   - speed 0.962 with 1.2 s pauses: 3:38.6;
   - speed 0.962 with 1.35 s pauses: 3:42.7, which went into the film.

   Every pause stays under the 1.5 s gap check.
5. **Pronunciation.** Whisper heard "Risica" for my name, "in-stack art" for Instacart, "airbim" for Airbnb, "repose" for repo's and "to DOS" for TODOs. Audio-only respellings fixed most of them. "repo's" still transcribes as "repose", which needs a human listen.
6. **Glyphs.** The film's only font has no ✓, ✗ or ✅, so they are drawn shapes. The checker's "✅ active" is drawn as a terracotta square with a white check.
7. **Text that did not fit.** The first layouts overlapped: the persona stamp sat on the name, the URLs ran into the checker column, and the status line ran off both edges. Rows are now laid out from measured widths. Every scene checks itself against the safe area when it renders. The Airbnb redirect chain is shown unabbreviated, so its checker verdict moved to the top row.
8. **Gates.**
   - Gate A runs scenes against a stub with estimated text widths, so my own layout checks now run only under real Manim.
   - Gate B's safe area (±6.3 × ±3.4) is tighter than my first guess, so every scene was re-fitted to it.
   - Gate B with `--curve-strict` was then clean on all eight scenes (221 snapshots).
9. **Gate T blocked the first master.**
   - It read the terracotta outlines around stamps and highlighted text as terracotta *text* at 2.74:1 contrast. My final-project film hit the same rule, so those outlines are now kraft-deep. Terracotta stays only on shapes, never touching text.
   - It also read a crossed-out eye as two overlapping labels. The "can't see" icon is now a closed eye.
   - The lit gate beams in beat 3 were the last terracotta bars it flagged; lit gates are now dark ink.
10. **Stale clips.** `./art run` skips any beat whose clip already exists, so my first fix was checked against the old renders. I moved the old clips into `_scratch/` and re-rendered.
11. **An empty box.** The 12-second frame check caught the outro's status board showing empty for about a second. It now appears together with its first words.
12. **Silence.** 15 of the 44 silences measure 1.50–1.59 s at −35 dB. The planned pauses are 1.35–1.4 s; the quiet tail of each sentence's last syllable adds the rest. Shortening the pauses further would have pushed the film under 3:40.

## My reflection

- The first narration came out at 2:50, almost a minute short, because the voice reads faster than we estimated. I chose short pauses after each sentence instead of long silences, so viewers have time to read the terminal text on screen.
- The toolkit's checks caught problems I would not have noticed by watching once: low-contrast outlines around text, overlapping labels, and old clips being re-checked instead of the new ones.
- Every number on screen traces back to a file in my worked run, so the video does not claim more than the evidence shows.
