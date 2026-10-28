> **Superseded 2026-10-21.** This is the 2026-10-19 script as approved then. Beats B01, B03, B05, B06,
> B08, B10, B11, B13 and B15 were re-narrated for the resubmission; the current narration is in
> `make_sheet.py` / `beat_sheet.json`, and `FACTCHECK.md` lists each change.

# Ground Truth SQL — pitch film v2 script (DRAFT for Riya's approval)

## Executive summary

This is the new narration for the redone final-project pitch film, with what appears on
screen for each line. It answers the professor's feedback: the film now opens by *showing*
the problem with a real wrong number, explains it with one real invoice, gives four real
examples, explains why this happens in real life, and only then introduces the tool and who it helps. Every number below was produced by
`evidence/run_slice.py` or a direct read-only query on Chinook (checked 2026-10-19).
Captions will show this exact text. Written in plain everyday words: SQL is explained once, and no other technical terms are used. Target length: under 4:00 (the limit).

**Voice:** Kokoro `af_bella` (American female), same as v1.

**Honesty rule kept:** no model has been run. The wrong queries were written by Riya to copy
common text-to-SQL mistakes, and the film says so out loud (beat 3) and on screen.

---

| # | Beat | Narration (spoken + captioned) | On screen (animated) |
|---|---|---|---|
| 1 | Title | Ground Truth SQL. I'm Riya Kapadnis, and this is my final project pitch for INFO seventy-three seventy-five. The problem: AI can write database code that runs with no errors, but gives the wrong answer. | Title card: **Ground Truth SQL** (large) · **Riya Kapadnis** (clearly under it) · INFO 7375 Final Project Pitch · one-line problem statement fades in. |
| 2 | The problem | Picture an analyst asking an AI: what is our revenue by country? The AI writes SQL, the language for asking a database questions. It runs. No errors. It says the USA made four thousand six hundred sixty seven dollars. The real answer is five hundred twenty three. | Question typed into a chat box → SQL types itself out → green "no errors" → USA $4,667 → drops into a slide → red stamp: **real answer $523**. Small tag: *SQL written by Riya to copy a common AI mistake*. |
| 3 | Why it went wrong | I wrote that SQL myself to copy a common mistake, on a free sample music-store database. One Reno order cost three ninety six, for four songs. The SQL joined the order to its songs, so the three ninety six was counted four times. Do that for every US order, and the total is almost nine times too high. | Order card ($3.96) → four song rows slide out (Longview, Basket Case, She, Geek Stink Breath) → $3.96 copies onto each song → counter adds up to $15.84 ("counted 4 times") → zoom out: every US order → $523 becomes $4,667. |
| 4 | More examples | It's not the only mistake. Mix up milliseconds and seconds: three thousand five hundred long songs, not one thousand sixty nine. Count purchases, not people: eight hundred thirty five rock buyers, in a store with fifty nine customers. Link the wrong columns: no answer at all. And no errors. | Three cards flip in, each: the question · wrong number (red) · right number (green) · the mistake in 3–4 plain words. All three get a green "no errors" tick, which is the point. |
| 5 | Why it happens in real life (new) | Why does this happen? People ask data questions in plain English, so most never see the SQL. The AI doesn't know your data, like one order having many songs. And wrong SQL doesn't crash. It just gives a number people trust. | Three reasons build up: (1) a person who sees only the answer, the SQL hidden; (2) the AI looking at a database with "?" marks; (3) a confident number landing in a meeting. |
| 6 | Other tools | Other tools don't do this on your data. BIRD tests AI only on its own databases. Vanna writes SQL, but I found no way in it to check that SQL against right answers. | Two panels: BIRD ("its data, not yours"), Vanna ("writes SQL, doesn't check it"). A gap opens between them. |
| 7 | What it is | That's the gap my project fills. Ground Truth SQL is a testing tool. Give it your database and questions with checked answers. It runs the AI's SQL and the checked SQL, compares the results, and gives a report card: what the AI got wrong, and why. | Simple flow: question → AI's SQL + checked SQL → both run on the database → two results compared → report card line "Revenue by country · WRONG · counted orders 4 times". Label *planned · AI step not built yet*. |
| 8 | Where it will be used + who it helps (new) | Where will it be used? Anywhere people ask data questions in plain English: store sales, finance, hospitals, marketing, and any company building an AI data assistant. Analysts learn what to double check. Teams test an AI tool before buying it. Engineers see what to fix first. | Uses light up one at a time around the report card: store sales, finance dashboard, hospital board, marketing team, AI data assistant. Then three people, each with a plain takeaway: "double-check these", "test before you buy", "fix this first". |
| 9 | How it judges | How does it judge? By results, not wording, since one answer can be written many ways. These two look different, but both give five hundred twenty three. Comparing wording got six of nine right. Comparing results: all nine. | Two different SQL snippets → both turn into 523.06 → "compare wording ✗" vs "compare results ✓" → score bars 6/9 vs 9/9. |
| 10 | It works today | This part already works. Eight questions, nine test cases, every one judged the way I judged it myself. | Real terminal recording of `python3 run_slice.py`, ending on the 9/9 line, with the key lines highlighted. |
| 11 | It caught me | It even caught my own mistake. One question asked about twenty twenty three, but the data ends in twenty thirteen. The right answer was empty, so broken SQL returning nothing looked correct. Now the tool rejects empty right answers. | Timeline 2009–2013, "2023" lands off the end → empty box = empty box → red cross → new rule card. |
| 12 | Who looks first + what it shows | Who looks first? Hiring managers for AI engineers. They can read the report card, rerun it with one command, and open one mistake. It shows I test AI instead of trusting it. | Report card page (planned) → one mistake opens up: AI's SQL next to the checked SQL. |
| 13 | Scope and risk | Included: one sample database, about fifty questions, and Claude. Not included: a chat app, or changing data. The risk: I write both questions and answers, so the test could be too easy. So a classmate checks some answers, and each question runs three times. | "Included" / "Not included" lists fill in → risk card → two fixes stamp on. |
| 14 | Why me | Why this project? I already use SQL, Python and AI at my co-op. Testing AI and understanding why it fails is what I want to learn. | Two columns: "already use" / "want to learn". |
| 15 | Conclusion | To wrap up. The problem: AI can give wrong answers that look right, and most people can't tell. My solution, Ground Truth SQL, tests the AI on your own data and shows which answers are wrong, and why. The checker already works, and already caught one of my own mistakes. Next, a real AI model. AI that writes SQL is easy to find. Knowing when to trust it is the project. | Recap builds in three rows (Problem → Solution → Today/Next), each with its icon from earlier in the film; then everything clears and the final line types out alone: "Knowing when to trust it is the project." |

## Facts behind each number (all re-run 2026-10-19, read-only)

| Claim | Value | Source |
|---|---|---|
| USA revenue, wrong join / correct | 4,667.06 / 523.06 | `run_slice.py` Q03 |
| Ratio | 8.92× ("almost nine") | computed |
| Invoice 16 | Reno, 2009-03-05, total 3.96, 4 lines at 0.99 (Longview, Basket Case, She, Geek Stink Breath) | direct query |
| US invoices / joined rows | 91 / 494 | direct query |
| Tracks > 5 min, ms-as-seconds / correct | 3,503 / 1,069 | `run_slice.py` Q06 |
| Rock buyers, COUNT / COUNT DISTINCT | 835 / 59 (store has 59 customers) | `run_slice.py` Q04, Q01 |
| Wrong join key | empty / Jane Peacock, 21 | `run_slice.py` Q05 |
| Text vs row agreement | 6/9 vs 9/9 | `run_slice.py` last lines |
| BIRD | 12,751 pairs, 95 databases | bird-bench.github.io (SOURCES.md, checked 2026-10-09) |
