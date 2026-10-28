# BUILD-PROMPT — Agentic Retrieval Lab (final project pitch film)

**Author:** Rithika Sankar Rajeswari.

This file holds the prompts Rithika gave Claude Code (in order, 2026-10-10 to 2026-10-11) and the commands to rebuild the film from source. Claude Code drafted this file.

**Film inputs that the prompts reference:** the beat sheet (`beat_sheet.json`), the scene code (`scenes.py` in the reel folder), the fact-check (`FACTCHECK.md`) and the gate reports in `gate-reports/`.

---

## 1. Rebuild the film from source (free pipeline: no keys, no paid services)

```bash
# 1. toolkit
git clone https://github.com/nikbearbrown/brutalist.art ~/brutalist-v2
cd ~/brutalist-v2
git checkout b21f625                       # the toolkit commit this film was built on
/opt/homebrew/bin/python3.12 -m venv .venv # any Python 3.12; 3.14 is too new for manim 0.18 / Pillow<11
source .venv/bin/activate
./setup --install                          # pip deps, Remotion node deps, fonts, Kokoro model (~340 MB)
                                           # (setup exits 1 at its ElevenLabs text guard on youtube/ reel files;
                                           #  every install step still completes — see gate-reports/README.md)

# 2. local toolkit patch (moves the beat-1 name stamp inside title-safe; not committed upstream)
git apply /path/to/final-project-film/toolkit-local-patch.diff

# 3. reel folder (the course book's youtube/ folder)
R=~/info-7375-prompt-engineering-for-generative-ai/youtube/rithika-final-project-pitch
#    it needs: make_sheet.py, beat_sheet.json, scenes.py, word_times.json, FACTCHECK.md, SHOTLIST.md,
#    PROMPTS.md, SOURCES.md (beat_sheet.json in this folder is the exact sheet used, with measured durations)
#    This submission folder is self-contained: copy scenes.py, make_sheet.py, word_times.json, beat_sheet.json,
#    FACTCHECK.md, SHOTLIST.md, PROMPTS.md and SOURCES.md from it into $R.

# 4. audio (only if re-voicing; the sheet already carries the measured durations)
python3 runtime/scripts/generate_audio_kokoro.py $R --speed 1.04
ffmpeg -y -i $R/mp3/beat-BOUT.mp3 -af apad=pad_dur=1.0 $R/mp3/beat-BOUT.pad.mp3 && mv $R/mp3/beat-BOUT.pad.mp3 $R/mp3/beat-BOUT.mp3
#    then write the ffprobe durations back to actual_duration_s for every beat

# 5. review cut (Gates F-paperwork, L, A, W, B, V) and the clean master (GATE T, then compile)
./art run   $R --height 2160
./art final $R --height 2160 --out $R/exports/landscape
```

Extra gate commands, run by hand for this film (reports in `gate-reports/`):

```bash
python3 runtime/qc/factcheck_check.py $R          # Gate F (content)
python3 runtime/scripts/bookend_check.py $R       # Gate F (bookends)
python3 runtime/qc/beat_lint.py $R/beat_sheet.json
python3 runtime/qc/manim_layout_audit.py $R/scenes.py --class <Scene> --curve-strict
python3 runtime/scripts/type_check.py $R          # GATE T
```

---

## 2. The prompts, verbatim

Shown here in the order Rithika sent them.

### Prompt 1 — setup

> This is a fresh clone of brutalist.art. Set it up for the FREE pipeline only: no API keys, no paid services, no uploads.
> 1. Read README.md and HOW-TO.md and follow their setup instructions (create/activate the venv if they say to, then run the setup/install step).
> 2. Run `./art --list` (or the equivalent shown in the README) and confirm the show-tell skill is listed.
> 3. Confirm Kokoro TTS and Manim work with the smallest test the docs offer.
> 4. List the available Kokoro voices.
> 5. Report anything that failed, with the exact error. Do not create any film or reel yet.

### Prompt 2 — the film brief

> # TASK: Build my Final Project Pitch Film with the show-tell skill
>
> ## Context
> I am Rithika Sankar Rajeswari, an INFO 7375 student. This is a graded 2–4 minute pitch film for my final project, "Agentic Retrieval Lab". The audience includes complete beginners, so every technical idea must be explained through one consistent cartoon story. Free pipeline only: no API keys, no paid services, no uploads, no stock media.
>
> ## Hard rules (do not break any)
> 1. RUNTIME: target 3:40–3:55. Hard maximum 4:00. Verify the final duration with ffprobe, not the beat sheet estimate. If it runs over, shorten narration in beats 2, 3, or 10 first, and tell me what you cut.
> 2. HONESTY: Past tense only for things that exist. Everything else is "will". Any drawing that shows something that does not exist yet, or an invented example, must carry an on-screen "CONSTRUCTED" label (beats 1, 6, 9, and any mock-up).
> 3. NUMBERS: Use only the numbers in the script. Each one must be verified in FACTCHECK.md (see below).
> 4. VOICE: Kokoro af_bella, first person, as me. Use my narration wording exactly; change it only for pronunciation, and list every change.
> 5. NO INSTRUCTOR IDENTITY: no Professor Bear name, persona, portrait, voice, brand kit, or credit line. If OUTRO-LOCK.md or bookend_check requires an instructor credit or outro, STOP and tell me instead of adding it.
> 6. NO EXTERNAL MEDIA: everything is drawn in Manim. Exception: beat 5 may use a real screenshot ONLY if the show-tell skill allows images; if so, ask me to supply it rather than generating a fake one.
> 7. CHECKPOINTS: stop and wait for my approval at the two points marked "STOP" below.
>
> ## Step 0: Setup check
> With .venv active, run `./art smoke`. If it fails, stop and report the exact error.
>
> ## Step 1: Read the rules
> Read skills/make/show-tell/SKILL.md, OUTRO-LOCK.md, and the prop READMEs under icons/show-tell-originals/. Follow the skill's structure, nine laws, labelling limits (1–3 words), and card test. Where the skill's required bookends (opening writer, key terms, Your Turn, outro) conflict with this pitch, keep what the gates require, keep them short, and tell me what you did. Create the reel where the skill says reels go, named `rithika-final-project-pitch`.
>
> ## Visual system (keep the SAME objects for the whole film)
> - THE LIBRARY: endless isometric shelves = the 8.8 million passages.
> - THE KEYWORD LIBRARIAN: holds a magnifying glass; matches exact words (BM25).
> - THE MEANING LIBRARIAN: holds a glowing lightbulb; matches meaning (embedding model).
> - THE ROBOT: a small helper robot = the AI agent that rewrites questions.
> - THE ANSWER KEY: a clipboard with one check mark per question = the official labels.
> - DECOY BOOKS: grey look-alike books = distractor passages.
> - THE PILE: a stack of 100 books on a desk = the "top 100" results.
> Palette and style follow the skill's defaults. Motion must carry each beat's idea (described per beat).
> If the skill supports burned-in captions, turn them on, because they help beginners follow.
>
> ## Pronunciation (audio text only; keep on-screen labels in standard form)
> BM25 → "B M twenty-five" · MS MARCO → "M S Marco" · Q2D-Web → "Q two D Web" · 8.8 million → "eight point eight million" · RAG → "rag" · LLM → "L L M"
>
> ## Beat sheet (14 beats)
>
> BEAT 1 — The hook  [answers Q1 setup] [CONSTRUCTED example]
> Picture: a person types one question into a search box. The robot steps in, and the question splits into four smaller speech bubbles.
> Motion: one bubble splits into four, then they fly toward the library.
> Labels: "one question" → "four searches"
> Narration: Picture asking a question online. More and more, an AI assistant does the searching for you. But it doesn't type your question. It rewrites it into several searches of its own. My project asks one thing: when the AI writes the search, does the right answer still come back?
>
> BEAT 2 — Why search matters  [beginner foundation]
> Picture: the library; a librarian carries a pile of 100 books to a desk where the robot waits.
> Motion: the shelves stretch into the distance; the pile lands; one glowing book is either in the pile or left behind on a shelf.
> Labels: "8.8M books", "top 100"
> Narration: Before an AI can answer anything, a search step has to find the right page among millions, like a librarian pulling a hundred books off the shelves. If the right book isn't in that pile, the AI never sees it, however smart it is.
>
> BEAT 3 — Two kinds of librarian  [beginner foundation]
> Picture: the two librarians side by side.
> Motion: the magnifying glass matches identical words on a book spine; the lightbulb lights a book with different words but the same meaning.
> Labels: "same words", "same meaning"
> Narration: There are two kinds of librarian. One matches your exact words; it's called BM25. The other matches meaning, using an AI model called an embedding. My project tests both.
>
> BEAT 4 — What I'm building  [Q1]
> Picture: a repository folder with three drawers: pipeline, tests, results.
> Motion: the drawers slide open one by one.
> Labels: "pipeline", "tests", "results"
> Narration: I'm Rithika, and this is Agentic Retrieval Lab. When it's done, it will be a public GitHub repository: a Python pipeline, tests, dated result files, and a short write-up of where search fails. "Agentic" here means agent-written queries. I'm not building an autonomous agent.
>
> BEAT 5 — What already exists  [exists-today, past tense]
> Picture: four stacked blocks: 300 questions, 1,200 rewrites, 8.8M passages, 103 tests. Small label: "built Oct 5–9, 2026".
> Motion: blocks drop in and stack; a green check appears on "103 tests".
> Labels: as listed
> Narration: Some of it already exists. Last week I took 300 real search questions from the public MS MARCO dataset, had Claude Haiku rewrite each into four agent-style searches, indexed all 8.8 million passages with the keyword librarian, and built a 200,000-passage test set. 103 tests pass.
>
> BEAT 6 — First result, and why I don't trust it yet  [Q4 skill shown] [CONSTRUCTED illustration for the answer-key part]
> Picture: three bars, 64%, 60%, 42%. Then the robot hands over a good book, and the answer key marks it with a red question mark.
> Motion: the bars grow; a question mark pops over the 42% bar; cut to the answer-key moment.
> Labels: "human", "main rewrite", "support"
> Narration: My first result: the keyword librarian found the right passage in its top 100 for 64 percent of human questions, 60 percent of the agent's main rewrites, but only 42 percent of its support searches. I don't trust that drop yet. The answer key lists one correct book per original question, so a support search can find a good book and still be marked wrong.
>
> BEAT 7 — What already exists elsewhere  [Q2]
> Picture: a huge locked vault labelled "Q2D-Web" beside a small open box labelled "MS MARCO".
> Motion: the vault's lock rattles shut; the box lid opens, showing human silhouettes on the questions.
> Labels: "private", "human-written"
> Narration: I looked at two alternatives. Perplexity's Q2D-Web paper studies agent searches over 190 million documents, but its data is private; outsiders can only submit models to a leaderboard. MS MARCO is public, but its questions are written by humans, with about one answer each.
>
> BEAT 8 — What makes mine different  [Q2]
> Picture: the two librarians team up; the keyword librarian holds a few books the other missed. Then a laptop with an arrow from a number to a file.
> Motion: the keyword librarian adds unique books to a shared pile; the arrow traces number → file.
> Labels: "team up?", "traceable"
> Narration: That paper found something surprising: the keyword librarian scores lowest overall, yet finds the most books no one else finds. It suggests testing whether the two work better as a team. My project will run that test at small scale, on public data, on one laptop, with every number traceable to a file.
>
> BEAT 9 — Who opens it  [Q3] [CONSTRUCTED mock-up]
> Picture: a hiring manager at a README with a 60-second timer.
> Motion: the timer sweeps; three steps light up: read table → click a number → run tests.
> Labels: "60 seconds", "CONSTRUCTED"
> Narration: The person opening it is a hiring manager for ML or AI engineering roles. In the first minute, they'll read the results table, click one number through to its source file, and see one command that reruns the tests. Today that table is still empty.
>
> BEAT 10 — What it proves  [Q4]
> Picture: three badges: fair test, sourced numbers, checked code. A fourth badge, "production RAG", is crossed out.
> Motion: three badges stamp on; the fourth fades with a strike-through.
> Labels: as listed
> Narration: A reviewer should conclude that I can design a fair test, ground every number in a file, and check a pipeline with tests. Not that I've shipped a production system. I haven't.
>
> BEAT 11 — In, out, first  [Q5]
> Picture: an "in" box, an "out" box, and an arrow marked "first".
> Motion: items sort into the boxes (in: meaning librarians, human vs agent, team-up test, failure notes; out: chatbot, answer writing); the arrow points at one meaning librarian racing the keyword librarian.
> Labels: "in", "out", "first"
> Narration: In scope: meaning models against keyword search, human versus agent searches, the team-up test, and a hand-written failure analysis. Out: no chatbot, and no answer writing. First, I'll race one meaning model against the keyword librarian. I'll know it ran when a new dated results folder appears and the keyword score matches its earlier run.
>
> BEAT 12 — What could sink it  [Q6]
> Picture: a thick grey decoy book and a thin correct book on a balance scale; a lazy librarian grabbing only thin books.
> Motion: the scale tips; the lazy librarian's score bar rises suspiciously, then a "test first" stamp appears.
> Labels: "65 words", "54 words"
> Narration: What could sink it: in my test set, the decoy passages average about 65 words, and the correct ones about 54. A librarian who simply grabs short books could look smarter than it is. So first, I'll test a lazy librarian that only picks short passages. If it beats random, I'll fix the test set before trusting any ranking.
>
> BEAT 13 — Why this project  [Q7]
> Picture: two piles, "already have" (data pipelines) and "learning" (retrieval metrics, embeddings, LLM judges).
> Motion: blocks move from "learning" toward "already have" as a progress bar fills.
> Labels: "already have", "learning"
> Narration: Why this project? I want a real retrieval project for ML and AI engineering roles starting January 2027. It's mostly learning, built on data-engineering skills I already use. New to me: retrieval metrics, embedding models, and using an LLM as a judge.
>
> BEAT 14 — Close  [exists vs will]
> Picture: two columns, solid checkmarks under "exists" and dotted outlines under "will".
> Motion: the dotted outlines pulse gently, waiting to be filled.
> Labels: "exists", "will"
> Narration: Everything I said in the past tense, you can open today. Everything else is a plan, and I'll log every change as I go.
>
> ## Step 2: Supporting files
> Create the files Gate F needs (SOURCES.md, FACTCHECK.md, SHOTLIST.md, PROMPTS.md).
> - FACTCHECK.md: one row per factual claim → its evidence. You may READ (never write) ~/agentic-retrieval-lab/README.md, ~/agentic-retrieval-lab/results/, and `git -C ~/agentic-retrieval-lab log`. Claims to verify: 300 questions; 1,200 rewrites; 8.8M passages; 200,000-passage test set; 103 tests (run `uv run pytest -q` in that repo read-only, or mark "verified by Rithika's terminal, Oct 10, 2026"); 64% / 60% / 42% (pool_stats.json; note these are rounded from 63.7 / 60.3 / 41.7); 65 vs 54 words (corpus_stats.json); built Oct 5–9 (git log). Paper claims (190M documents, private data, public leaderboard, BM25 lowest recall but most unique positives, suggested team-up test) cite Schall et al., 2026, arXiv:2609.08887v2, abstract, §1, §5.1, §6. Mark anything you cannot verify as UNVERIFIED.
> - SOURCES.md: list the toolkit, Kokoro voice, the paper, MS MARCO, and the contributions: "Rithika: project, decisions, script edits, review and approval. Claude (chat): drafted the script and visual plan from Rithika's brief. Claude Code: built the reel and ran the gates." Leave a line "Rithika's script edits: [TO FILL]" for me.
>
> ## Step 3: Gates before render
> Run Gate F (factcheck_check.py, bookend_check.py), the Gate A pre-audit, and the layout audit.
> >>> STOP. Show me: FACTCHECK results, any UNVERIFIED claims, pronunciation changes, how you handled bookends/outro, and the estimated runtime. Wait for my approval. <<<
>
> ## Step 4: Review render
> After I approve, render the review cut (the skill's `art run` step). Report the ffprobe duration and any gate failures.
> >>> STOP. I will watch it before you make the final master. <<<

### Prompt 3 — smoke-test workaround

> Go with option 1, done safely:
> - Preferred: copy examples/_smoke to a scratch folder, set its slug to "smoke" there, and run the smoke test on the copy, if ./art smoke can target a different folder.
> - If it can't, make the one-line change to "smoke" in examples/_smoke/beat_sheet.json locally. Do not commit or push it. After the smoke test, revert it with `git checkout -- examples/_smoke/beat_sheet.json` and confirm `git status` is clean for that file.
> Report the smoke result. If it passes, continue with Step 1 of my original task and go until the first STOP.

### Prompt 4 — decisions after the first stop

> Decisions:
>
> OUTRO: Option B. Beat 14 becomes the BOUT outro beat, drawn in Manim, no extra narration. Title: "Agentic Retrieval Lab". channel_title: "Rithika Sankar Rajeswari · github.com/rithika-sr". No @NikBearBrown, no Claude mascot. If the gate rejects B, use option A with this narration only: "Agentic Retrieval Lab, by Rithika Sankar Rajeswari." Record the reason in the beat sheet.
>
> 1. Reel location: yes, ~/info-7375-prompt-engineering-for-generative-ai/youtube/rithika-final-project-pitch/. Do NOT git add or commit anything in that repo.
> 2. Bookends: skip the hesitant writer, key terms, and Your Turn. Record the reason (runtime limit, instructor branding, and beats 1–3 already cover them).
> 3. Voice: af_bella. Record the reason.
> 4. People: agreed, no people drawn. Use your proposed substitutes.
> 5. Captions: skip.
>
> Split beat 6 into 6a (the three bars) and 6b (the answer-key moment).
>
> NARRATION CHANGES (use these exact wordings):
> - Beat 2: delete ", however smart it is" so it ends "...the AI never sees it."
> - Beat 5: "Some of it already exists. This week I took 300 real search questions from the public MS MARCO dataset, had Claude Haiku rewrite each into four agent-style searches, indexed all 8.8 million passages, and built a 200,000-passage test set. 103 tests pass."
> - Beat 6a: "My first result: the keyword librarian found the right passage in its top 100 for 64 percent of human questions and 60 percent of main rewrites, but only 42 percent of support searches."
> - Beat 6b: "I don't trust that drop yet. The answer key lists one correct book per original question, so a support search can find a good book and still be marked wrong."
> - Beat 7: "I looked at two alternatives. Perplexity's Q2D-Web paper studies agent searches over 190 million documents, but its data is private; the public gets a leaderboard, not the data. MS MARCO is public, but its questions are written by humans, with about one answer each."
> - Beat 11: "In scope: meaning models versus keyword search, human versus agent searches, the team-up test, and a hand-written failure analysis. Out: a chatbot, or writing answers. First, I'll race one meaning model against the keyword librarian. I'll know it ran when a new dated results folder appears and the keyword score matches its earlier run."
> - Beat 12: "What could sink it: in my test set, the decoys the keyword librarian picked average about 65 words, and the correct passages about 54. A librarian who simply grabs short books could look smarter than it is. So first, I'll test a lazy librarian that only picks short passages. If it beats random, I'll fix the test set before trusting any ranking."
> - Update FACTCHECK.md for beats 7 and 12 to match these wordings.
>
> RUNTIME: recompute the estimate including animation holds and transitions. If the total estimate exceeds 3:55, stop and propose cuts before rendering.
>
> Now proceed: write the paperwork and scenes, run the gates, and stop at my first STOP with the report.

### Prompt 5 — runtime option

> Option B: apply the three cuts from A and set voice speed to 1.04.
> Yes, change "agent-written" to "agent written" in narration_text only (keep script_text as I wrote it).
> Before re-voicing everything, tell me the path to beat 4's audio file so I can listen to how "Rithika" sounds. I'll reply with "name OK" or a respelling.
> After that: re-voice, confirm the new measured runtime is at or under 3:55, write the paperwork and scenes, run the gates, and stop at my first STOP with the report.

### Prompt 6

> name ok

### Prompt 7 — honesty fixes

> Not approved yet. Two honesty fixes first (change script_text and narration_text):
>
> - Beat 6b: "I don't trust that drop yet. The answer key usually lists just one correct book per original question, so a support search can find a good book and still be marked wrong."
> - Beat 8, first sentence: "That paper found something surprising: on its main measure, the keyword librarian scores lowest, yet finds the most books no one else finds."
>
> Update FACTCHECK.md rows 15 and 22 to match. Re-voice only beats B06B and B08, rerun Gate F and the clip-vs-audio length check for those two beats, and re-measure the total runtime (must stay at or under 3:55).
>
> [ADD YOUR OWN NOTES HERE, e.g. name respelling, or a frame to simplify, or delete this line]
>
> If everything passes, you are approved to render the review cut with ./art run ... --height 2160. Report the ffprobe duration and any gate failures, then STOP so I can watch it.

### Prompt 8 — visual redesign

> Change of plan. The review cut's visuals are not good enough. Keep ALL narration audio and timing exactly as is (runtime stays 3:53). Redo the VISUALS only, and fold in the Gate V fixes.
>
> ## Gate V fixes (from your last report)
> - Option 3 for the B01 stamp: local toolkit edit to move it inside title-safe, NOT committed. Save it as toolkit-local-patch.diff in the reel folder and note it in SOURCES.md ("Local toolkit patch: moved channel_title stamp inside title-safe area; see toolkit-local-patch.diff; not committed upstream").
> - Keep every shape inside title-safe (check shapes, not only text). Fix B04 contrast. Add the sparse-by-design waiver to B06A only if still needed.
>
> ## Global visual rules
> 1. NO squiggle placeholder text anywhere. Every bubble, search box, card, screen or document shows real readable words, or is removed.
> 2. Text must be readable on a phone: use the largest label size the skill and gates allow, in full-contrast ink (never pale grey). Key-term labels should be noticeably larger than secondary labels.
> 3. Scale each beat's drawing to fill most of the title-safe area; no tiny objects in big empty frames.
> 4. KEYWORD POP-INS: when a key term is spoken, its label pops in (gentle scale-in) at that moment. Time pop-ins from the whisper word timestamps of the existing narration.
> 5. Every icon gets a label. If an icon can't be understood with its label, replace it with a clearer drawing.
> 6. On-screen text stays short (about 5 words or fewer per item), except the real example queries in beat 1.
> 7. Honesty: "CONSTRUCTED" stays on invented examples and mock-ups; real data gets a small source tag instead.
> 8. If the skill's 1–3 word label law, card test, or any gate blocks something below, use the skill's ShowTellCard kinds where they fit. If it is still blocked, tell me which rule it breaks. Never disable or exempt a gate to get past it.
>
> ## Beat-by-beat visual changes
> B01: Pick ONE short, plain, non-sensitive query from my 300 MS MARCO questions that has its 1 primary + 3 support rewrites in ~/agentic-retrieval-lab (READ ONLY). Show the real question in the search box, then the 4 real rewrites popping into 4 bubbles. Labels: "your question" → "agent's 4 searches". Source tag: "real example · MS MARCO dev · rewritten by Claude Haiku, Oct 8, 2026". Remove CONSTRUCTED from this beat. Add the query, its rewrites, and the source file path to FACTCHECK.md. Before rendering, show me which query you picked.
> B02: Labels pop in: "8.8 million passages", "top 100", "right answer". When the right book stays on the shelf: "missed = AI never sees it".
> B03: Large title chips over each cart: "BM25: keyword search" and "Embedding: meaning search". Small CONSTRUCTED example: query card "car repair cost" matches book "car repair cost" (same words) and book "fixing an automobile price" (same meaning).
> B04: Big title "Agentic Retrieval Lab". Full-contrast drawer labels: pipeline, tests, results. Chip: "agentic = agent-written queries".
> B05: Larger blocks, each with a big number and a label: "300 questions", "1,200 rewrites", "8.8M passages", "103 tests ✓". Tag: "built Oct 5–9, 2026".
> B06A: Bars labelled 64%, 60%, 42% with captions "human", "main rewrite", "support". Caption under the chart: "BM25: right passage in top 100". The "?" pops over 42% on "I don't trust that drop".
> B06B: The robot hands over a book marked "good match"; the clipboard reads "answer key: 1 per question" and marks it ✗. Caption: "good book, marked wrong". Keep CONSTRUCTED.
> B07: Vault chips: "Q2D-Web", "190M documents", "private data", plus a small leaderboard icon labelled "public leaderboard only". Box chips: "MS MARCO", "public", "human-written", "~1 answer each". The box must not be empty: show question cards inside.
> B08: Chip: "paper: BM25 finds unique books". The two carts join with label "team-up test". Laptop: "small scale · public data". Arrow from a number to a file labelled "results/…json".
> B09: README mock with a real-looking results table: columns "human | agent", rows "BM25 | embedding", every cell "—" (empty). Numbered steps pop in: "1 read table", "2 click a number", "3 rerun tests". Keep CONSTRUCTED.
> B10: Three large badges: "fair test", "sourced numbers", "tested code". A fourth, "production RAG", gets visibly struck through.
> B11: Every tray item labelled. In: "embedding vs BM25", "human vs agent", "team-up test", "failure notes". Out: "chatbot", "answer writing". First arrow: "1 embedding vs BM25". Folder: "new results/ folder".
> B12: Scale pans: "decoys (BM25-picked): 65 words" vs "correct: 54 words". Lazy cart: "grabs short books". Its score bar: "looks good?". Stamp: "test first". Keep CONSTRUCTED.
> B13: Piles labelled. Already have: "data pipelines". Learning: "retrieval metrics", "embeddings", "LLM judges".
> B14 (outro): Exists column with labelled checks: "repo + tests", "200k test set", "BM25 baseline". Will column with labelled dotted items: "embedding runs", "team-up test", "failure analysis". Then the title "Agentic Retrieval Lab" and "Rithika Sankar Rajeswari · github.com/rithika-sr", large and inside title-safe.
>
> ## Process
> 1. Show me the B01 query you picked and its 4 rewrites. STOP for my OK.
> 2. Then build the scenes and render LOW-RES stills: the midpoint and last frame of every beat, as one contact-sheet PNG. Run Gates A, W and the layout audit (shapes and text). STOP and show me the contact sheet path and gate results. No 4K render yet.
> 3. After my approval: 4K review cut, all gates including V on the full film, ffprobe runtime. STOP.

### Prompt 9 — beat-1 query and evidence

> OK, use query 951820 ("when is ski season over") and its 4 rewrites, shown exactly as stored (lowercase).
>
> Verifiability: data/processed/ is git-ignored, so also create an evidence excerpt for my film submission:
> - Write ~/final-project-film/evidence/beat1_example_951820.json containing ONLY the 5 records (the human query line and the 4 agent rewrite lines), copied verbatim, plus a header field noting: source file paths and line numbers, rewrite run folder, model (claude-haiku-4-5-20251001), date Oct 8, 2026, and "MS MARCO dev/small, public dataset".
> - Do not modify anything in ~/agentic-retrieval-lab.
> - In FACTCHECK.md, cite both the local source paths and this evidence file.
>
> Then continue: build the redesigned scenes from my visual-change prompt, render the low-res midpoint + last-frame contact sheet named contact_redesign_<HHMM>.png, run Gates A, W and the layout audit (shapes and text), and STOP with the contact sheet path and results.

### Prompt 10 — redesign fixes

> Approved with these fixes first (low-res only):
> 1. B07: move the "public" chip directly under the "MS MARCO" title, so it clearly belongs to MS MARCO (mirroring "private data" under Q2D-Web). Nothing should sit between the two titles.
> 2. B06B: add a small caption "not on the key" next to the ✗ beside "good match". Also render a still at about 1.0 s into B06B and give me its path, so I can confirm the "?" over the 42% bar is visible.
> 3. B12: move "grabs short books" directly under the lazy cart, clear of the pan string.
> 4. B13: move "retrieval metrics" (and the stack labels) so nothing is clipped by the block edge.
> 5. B11: move "new results/ folder" clear of the folder tab.
> Re-run Gates A, W, the layout audit and the title-safe pixel check on the changed beats, and update SHOTLIST/FACTCHECK if any on-screen text changed (Gate F must stay clean).
>
> If all of that passes, go straight on to: render the 4K review cut, run ALL gates including Gate V on the full film, report ffprobe duration (must be ≤ 3:55), give me the B06B 1.0 s still path and a new full contact sheet from the 4K cut, then STOP so I can watch it.

### Prompt 11 — status question

> Is the 4K review cut of the redesigned version finished? Give me the exact path and modification time of the new MP4. If it's still rendering, tell me how far along it is. If it stopped or failed, show me the error.

### Prompt 12 — beat 13 narration and cartoon cast

> Two changes to the review cut. Narration stays the same EXCEPT beat 13.
>
> ## 1. Beat 13 narration (script_text and narration_text)
> New text: "Why this project? I'm aiming for AI and ML engineering or data science roles, and I'm especially interested in RAG systems: retrieval, generation, and evaluation. It's mostly learning, built on data-engineering skills I already use. New to me: retrieval metrics, embedding models, and using an LLM as a judge."
> Pronunciation: "AI and ML" → "A I and M L"; "RAG" → "rag"; "LLM" → "L L M".
> Re-voice B13 only (af_bella, speed 1.04), whisper-check it, update word_times.json for B13, and re-measure the total runtime. It must stay at or under 3:58; if it doesn't, stop and tell me.
> Update FACTCHECK (remove the January 2027 row) and SHOTLIST. Also edit ~/final-project-film/PROJECT-BRIEF.md: in section 7, replace the "Why it matters" line with: "Why it matters: I'm aiming for AI/ML engineering and data science roles and am especially interested in RAG systems (retrieval, generation, and evaluation); this project lets me build and measure the retrieval part." Change nothing else in the brief.
>
> ## 2. Cartoon characters
> I authorize generic cartoon people for my film. The toolkit's house rule that people must be the instructor's portrait does not apply here. Do NOT use any portrait, likeness, or name of the instructor. If any GATE (not just a written rule) blocks drawn people, stop and tell me which; never disable or exempt it.
> Style: simple, friendly flat cartoon figures built from Manim shapes, matching the existing line weight and palette; same character looks identical in every beat.
> Cast:
> - ME (Rithika): friendly young woman, long dark hair, waving, speech bubble "hi!". B04: she appears beside the cabinet as I say "I'm Rithika", waving, with the "hi!" bubble. BOUT: small version waving next to my name.
> - KEYWORD LIBRARIAN (BM25): tall thin old man, round glasses, bow tie, holding the magnifying glass. Replaces the magnifier cart in B02, B03, B08, B11.
> - MEANING LIBRARIAN (embedding): shorter old man, white beard, cardigan, holding the glowing lightbulb. Replaces the lightbulb cart in B03, B08, B11.
> - LAZY LIBRARIAN: sleepy young assistant, half-closed eyes, grabbing only thin books. Replaces the lazy cart in B12.
> - SEARCHER: simple generic person typing at the search box in B01, next to the robot.
> - REVIEWER: generic person with a coffee cup looking at the README in B09 (CONSTRUCTED label stays).
> Keep the robot as the AI agent. Keep all existing labels, chips, pop-ins, source tags and CONSTRUCTED tags. Characters must stay inside title-safe and must not cover any text.
>
> ## Process
> 1. Render LOW-RES stills only: the midpoint and last frame of every changed beat (B01, B02, B03, B04, B08, B09, B11, B12, B13, BOUT) as one contact sheet named contact_cast_<HHMM>.png. Run Gates A, W, F, the layout audit and the title-safe check. STOP with the path, gate results and new runtime. No 4K yet.

### Prompt 13 — cast tweaks

> Cast looks good. Tweaks before 4K (low-res first):
> 1. B04: make my character's long dark hair clearly visible (shoulder length or longer). Move the "hi!" bubble up and to the right so it doesn't crowd the "pipeline" label.
>    [OPTIONAL: my avatar colours: hair ___, skin tone ___, top ___]
> 2. B01: enlarge the searcher and the robot about 1.5x and use the empty space; the searcher should clearly be typing on the phone.
> 3. B09: enlarge the reviewer and give them clear space beside the README, not touching CONSTRUCTED.
> 4. B11: enlarge the race track and both librarians so the race is readable at a glance.
> Keep everything inside title-safe with no text overlap. Re-run Gates A, W, F, the layout audit and the title-safe check on changed beats, and show me a small contact sheet of just B01, B04, B09, B11 (midpoint + last). Then, if everything is clean, go straight on:
>
> Render the 4K review cut, run ALL gates including Gate V on the full film, report the ffprobe duration (must be <= 3:58), give me a full contact sheet (midpoint + last frame of all 15 beats) taken from the 4K cut, and STOP.

### Prompt 14 — final polish (choreography)

> # Final polish: make the film coherent and professionally choreographed
>
> ## Step 0 — SAFETY BACKUP (do this first)
> Make a final master of the CURRENT approved cut (GATE T + art final at --height 2160), fixing GATE T issues only by moving things. Copy it to ~/final-project-film/backup/rithika-pitch-backup-master.mp4 and report its path, ffprobe duration, size and sha256. Do not change any scene until this is done.
>
> ## Goal
> Narration and timing stay EXACTLY as they are. Re-choreograph the visuals so the film flows like a polished YouTube explainer: every element appears when it's spoken about, leaves or dims when the narration moves on, and nothing looks cluttered or left over.
>
> ## Global staging rules (apply to every beat)
> 1. ENTER ON THE WORD: each element appears within ±0.2 s of the word that introduces it (use word_times.json).
> 2. EXIT WHEN DONE: when the narration moves on, elements that are no longer relevant fade out, or dim to ~35% if they are needed as context. Characters are on screen only while they are relevant.
> 3. ONE FOCUS AT A TIME: at most one highlighted focus group at any moment; everything else is dimmed or gone.
> 4. CONSISTENT MOTION: the same easing everywhere, entrances and exits of 0.4–0.6 s. Recurring characters slide or walk in and out; they never pop or teleport.
> 5. CONSISTENT CAST POSITIONS: the keyword librarian always enters from and stands on the LEFT, the meaning librarian on the RIGHT, and the robot keeps the same size in every beat.
> 6. READABLE HOLDS: each beat's final state holds at least 1 s before the beat ends.
> 7. NO OVERLAP AT ANY FRAME: check changed beats every 0.5 s, not just midpoint and last.
> 8. Keep all labels, source tags, CONSTRUCTED tags and real data as they are. Stay inside title-safe. Never disable or exempt any gate; if a gate's midpoint sampling conflicts with an animation, adjust timing and tell me.
>
> ## Beat-by-beat choreography (cue word → action)
> B01: Start with the searcher alone, typing, and the search box "when is ski season over" + "your question". On "AI assistant" the robot rolls in and the searcher slides out left (they never overlap). On "several searches" the 4 bubbles pop in one by one from the robot, with clear gaps between them, then "agent's 4 searches". Make the source tag smaller and lighter, directly under the search box; make "your question" and "agent's 4 searches" slightly smaller.
> B02: Shelves + "8.8 million passages" on "among millions". The keyword librarian walks in and stacks the pile on "a hundred books" + "top 100". On "isn't in that pile", the right book glows on the shelf, ✗ + "missed = AI never sees it". The robot waits at the desk the whole time.
> B03: Both librarians walk in on "two kinds of librarian". On "exact words": highlight the LEFT librarian + the query card + the "car repair cost" book + the "BM25: keyword search" chip, with the right side dimmed. On "meaning": highlight the RIGHT librarian + "fixing an automobile price" + the "Embedding: meaning search" chip, with the left side dimmed. On "My project tests both" (if still in the audio) or at the end: both undimmed.
> B04: On "I'm Rithika": my character slides in, waves, "hi!". On "this is Agentic Retrieval Lab": the title appears and MY CHARACTER SLIDES OUT. On "pipeline, tests, dated result files": the drawers open one by one with their labels. On "write-up": the write-up doc pops in. On "Agentic here means agent-written queries": the robot + the "agentic = agent-written queries" chip appear. On "I'm not building an autonomous agent": the robot dims.
> B05: Each block drops in on its spoken number (300, 1,200, 8.8 million, 200,000 if shown); "103 tests ✓" on "103 tests pass".
> B06A: Each bar grows on its spoken percentage.
> B06B: "?" pops on "don't trust". The chart slides out on "answer key" as the clipboard slides in. On "find a good book": the robot hands over "good match". On "marked wrong": ✗ + "not on the key".
> B07: Vault + "Q2D-Web" on "Q2D-Web"; "190M documents" on "190 million"; "private data" on "private"; the leaderboard icon on "leaderboard". Then the vault dims, and on "MS MARCO is public" the box + "MS MARCO" + "public" appear; "human-written" and "~1 answer each" on their words.
> B08: "paper: BM25 finds unique books" on "most books no one else finds"; the librarians walk together + "team-up test" on "as a team"; the laptop, arrow and results file on "public data, on one laptop… traceable". Dim the librarians when the laptop appears.
> B09: The README + reviewer on "hiring manager"; steps 1, 2, 3 each on their phrase; on "still empty" the empty table cells briefly highlight.
> B10: Each badge on its phrase; "production RAG" strikes through on "Not that I've shipped".
> B11: Each "in" item pops on its phrase; the "out" items on "Out:"; the race starts on "race one meaning model"; the folder + label on "new dated results folder"; ✓ on "matches its earlier run". Dim the trays during the race.
> B12: The scale + "65 words" / "54 words" on the numbers; the lazy librarian walks in on "grabs short books"; the bar rises on "smarter than it is"; the "test first" stamp on "So first"; on "fix the test set" the lazy librarian walks out.
> B13: Add a chip "AI/ML engineering · data science" on "roles", and "RAG: retrieval · generation · evaluation" on "RAG systems". "data pipelines" joins "already have" on "skills I already use". Each "learning" item pops on its word (retrieval metrics, embedding models, LLM as a judge). Dim the role chips when the skills appear.
> BOUT: Exists items tick on "past tense… open today"; "will" items appear on "everything else is a plan"; then the title, my name and the small waving me.
>
> ## My own viewing notes (apply these too)
> [PASTE YOUR NOTES HERE, e.g. "B07: …", or delete this line]
>
> ## Process
> 1. Rebuild the scenes. Render a LOW-RES (480p) preview of the WHOLE film with audio, plus a contact sheet of every beat at 25%, 50%, 75% and last frame. Run Gates A, W, F, L, the layout audit and the title-safe check, and check for overlaps every 0.5 s on all beats. STOP and give me the preview path, contact sheet path and gate results.
> 2. After my approval: 4K review cut, all gates including V, then the final master (GATE T + art final). Report path, ffprobe duration (must be ≤ 3:58), size, sha256. STOP.

### Prompt 15 — final render and submission assembly

> Approved. Step 2: render the 4K review cut, run all gates including Gate V, then GATE T and the final master (art final, --height 2160). Fix issues only by moving things, never by disabling or exempting a gate. Report the master path, ffprobe duration (must be <= 3:58), resolution, size in MB and sha256.
>
> Then immediately do the submission assembly:
> 1. cd ~/info-7375-prompt-engineering-for-generative-ai && git pull --rebase. Stop if there is a problem.
> 2. Create fall-2026/rithika-s/final-project-film/ with: the final master .mp4 (stop if over 95 MB); PROJECT-BRIEF.md, FRICTIONAL.md and evidence/ from ~/final-project-film/ (copy as-is, do NOT edit FRICTIONAL.md or my "script edits" line in SOURCES.md); beat_sheet.json, SOURCES.md, FACTCHECK.md, SHOTLIST.md, PROMPTS.md, toolkit-local-patch.diff from the reel folder; gate-reports/ (F, A, W, L, B, V, T, layout audit, and your 0.5 s overlap check); BUILD-PROMPT.md (the prompts I gave you plus the commands to rebuild: clone, venv, setup, apply patch, art run, art final); README.md (my name Rithika Sankar Rajeswari, working title "Agentic Retrieval Lab", target role ML/AI engineering and data science with a focus on retrieval and RAG, runtime, contents list, how to rebuild, and a note that Claude Code drafted README and BUILD-PROMPT). No backup/ folder, caches, .venv, credentials or anything from youtube/.
> 3. Search every file in that folder for "[TO FILL]", "[WRITE", "If true:", "TODO" and "[PASTE" and list any hits.
> 4. git add ONLY fall-2026/rithika-s/final-project-film/. Show `git status --short` and the staged files with sizes.
> 5. STOP. Do not commit or push.
