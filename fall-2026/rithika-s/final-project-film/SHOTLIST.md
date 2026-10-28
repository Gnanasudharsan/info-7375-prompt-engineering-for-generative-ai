# SHOTLIST — rithika-final-project-pitch (visual v2, 2026-10-11)

Typed work order. Every slot is drawn in Manim (`scenes.py`). No pantry media, captures or generated clips.

- **Cards:** none. No `ShowTellCard` was needed, because every v2 request fit a drawing with labels.
- **Pop-ins:** key-term labels pop in on the spoken word, timed from `word_times.json` (faster-whisper small.en word timestamps of the existing narration). Audio and timing are unchanged.
- **Label sizes:** key terms 46–72, secondary labels 36–44, source tags 32 (the skill's type floor). All labels are full ink.
- **Skill doctrine broken on purpose:** many labels exceed the skill's 1–3 word law (rule 2), because Rithika's v2 brief asks for them. No gate enforces word count; every gate that runs passes.
- **Bookends:** BIDEA, BDEFS and BHTF are skipped (`metadata.bookend_exempt`). BOUT is beat 14.
- **Cartoon people** (Rithika, 2026-10-11): one builder per character (`me`, `keyword_librarian`, `meaning_librarian`, `lazy_librarian`, `searcher`, `reviewer`), so each looks identical in every beat. No instructor portrait, likeness or name. The robot is still the AI agent.

| Beat | Audio s | Manim class | Picture and motion | On-screen text | Honesty |
|---|---|---|---|---|---|
| B01 | 16.49 | `B01_Hook` | A searcher types the real question; robot arrives; the 4 real rewrites pop into bubbles | your question · agent's 4 searches · source tag | real data (tag) |
| B02 | 10.37 | `B02_Pile` | Library shelves, right book glows; the keyword librarian (BM25) pulls the pile onto the desk; right book left behind, ✗ | 8.8 million passages · top 100 · right answer · missed = AI never sees it | real figure (tag) |
| B03 | 10.28 | `B03_Librarians` | Query card; the keyword librarian's magnifier matches the same-words book; the meaning librarian's bulb lights the same-meaning book | BM25: keyword search · Embedding: meaning search · same words · same meaning | CONSTRUCTED |
| B04 | 17.92 | `B04_Repo` | Title; Rithika waves ('hi!') on 'I'm Rithika'; cabinet drawers open; write-up file; robot + chip | Agentic Retrieval Lab · pipeline · tests · results · write-up · agentic = agent-written queries | plan |
| B05 | 19.84 | `B05_Built` | Four blocks drop in, each with a big number | 300 questions · 1,200 rewrites · 8.8M passages · 103 tests ✓ · built Oct 5–9, 2026 | real data (tag) |
| B06A | 12.99 | `B06A_Bars` | Three bars grow on the spoken numbers | 64% · 60% · 42% · human · main rewrite · support · BM25: right passage in top 100 | real data (tag) |
| B06B | 9.88 | `B06B_AnswerKey` | '?' lands on 42%; answer key, one tick per question; robot's good book marked ✗ | answer key: 1 per question · good match · not on the key · good book, marked wrong | CONSTRUCTED |
| B07 | 18.79 | `B07_Alternatives` | Vault locks; leaderboard icon; open MS MARCO box with real question cards | Q2D-Web · 190M documents · private data · public leaderboard only · MS MARCO · public · human-written · ~1 answer each | real (paper, dataset) |
| B08 | 19.73 | `B08_Team` | Keyword librarian finds unique books; the two librarians join; laptop number → results file | paper: BM25 finds unique books · team-up test · small scale · public data · results/…json | plan + real figure |
| B09 | 15.96 | `B09_Reader` | A reviewer with coffee reads a README mock with an empty results table; timer; numbered steps pop | 60 seconds · 1 read table · 2 click a number · 3 rerun tests | CONSTRUCTED |
| B10 | 9.56 | `B10_Badges` | Three badges stamp on; production RAG crossed out | fair test · sourced numbers · tested code · production RAG (struck) | self-assessment |
| B11 | 21.50 | `B11_Scope` | In/out trays fill with labelled cards; the two librarians race on a track; new results folder + check | in · out · embedding vs BM25 · human vs agent · team-up test · failure notes · chatbot · answer writing · 1 embedding vs BM25 · new results/ folder | plan |
| B12 | 22.29 | `B12_Decoys` | Balance tips; a sleepy lazy librarian grabs short books; suspicious score bar; test-first stamp | decoys (BM25-picked) 65 words · correct 54 words · grabs short books · looks good? · test first | real figures (tag) + CONSTRUCTED |
| B13 | 21.06 | `B13_Learning` | Already-have pile; learning blocks turn solid as the bar fills | already have · data pipelines · learning · retrieval metrics · embeddings · LLM judges | plan |
| BOUT | 8.40 | `BOUT_Close` | Exists checks; will boxes pulse; title + name with small waving Rithika | exists: repo + tests · 200k test set · BM25 baseline · will: embedding runs · team-up test · failure analysis | outro |
