# FACTCHECK — Marino Desk Assistant: A Pitch

Status: lookups and re-runs done by Claude Code (Opus 5.5) on 2026-10-13, as listed in the Source column. Shubham Bagwe reviews and signs off before submitting (FRICTIONAL.md). Every source below was opened or re-run on 2026-10-13.

Key sources:
- **REPO** = `github.com/bagwe-shubham1727/marino-rag`, commit `dd3205e` (public; single commit 2026-07-02).
- **TESTS** = `uv run --frozen pytest -q` in REPO, re-run 2026-10-13: 60 passed (`evidence/marino-rag-tests-2026-10-13.txt`).
- **SEARCH** = the site's own search (`recreation.northeastern.edu/?s=…`), run 2026-10-13 (`evidence/site-search-2026-10-13.txt`).
- **ALUMNI** = `recreation.northeastern.edu/alumni/`, fetched 2026-10-13 and passed through REPO's own parser (`evidence/alumni-page-check-2026-10-13.txt`).
- **BANK** = my project bank (a private file of my own, read locally; not submitted).

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B01 | "written with Claude and spoken by a synthetic voice" | PASS | Claude drafted the script from my decisions (SOURCES.md); Kokoro `am_michael` generated locally. The tag on screen says the same | — |
| 2 | B01 | "Will answer front-desk questions … from the public recreation website, and quote the page it used" | EXEMPT | A plan, in the future tense. The first cut said "answers"; the fresh-context review flagged the present tense, so B01 was re-voiced. Today REPO answers with citations (row 9) but indexes SharePoint exports too, and uses OpenRouter, not Claude (rows 13–14) | — |
| 3 | B02 | Finished artifact: public repo with Python/FastAPI backend, Next.js chat window, Claude answering, evaluation report | EXEMPT | A plan (future tense; tag "constructed · planned repo"). REPO today has FastAPI (`api/main.py`) and Next.js (`web/app/`); Claude and the report are "will" | — |
| 4 | B02, B15 | "A first version already exists, and its sixty tests passed today" / "60 passed" | PASS | TESTS: `60 passed` on 2026-10-13 at `dd3205e` | — |
| 5 | B03 | The Alumni page holds about eight hundred words of fee tables | PASS | ALUMNI: REPO's parser extracts 782 words from the page | — |
| 6 | B04 | Site search returns pages, not answers; "guest pass" returned five pages with the home page first | PASS | SEARCH: "guest pass" → 5 result pages, first "Home"; "alumni membership fees" → 1 page (Alumni); "pool hours" → 4 pages. No result shows answer text | — |
| 7 | B04 | "I looked at what we use now": site search and manual lookup | PASS | My choice of alternatives (2026-10-13). Manual lookup is the "today" process in REPO's `docs/PRD.md` §1 | — |
| 8 | B05 | "Mine will save … It will give one answer, quote the exact line, and link to it … it will answer: I don't know" | EXEMPT | The finished behaviour, in the future tense (re-voiced after the review; tag "constructed · planned answer"). REPO's system prompt already requires citations and the refusal line (`api/prompts.py`: "I don't know based on the training materials I have.") | — |
| 9 | B07 | "It already retrieves five passages and reranks them to three" | PASS | REPO `api/retrieval.py`: `top_k=5`, `rerank_to=3`, cross-encoder `BAAI/bge-reranker-base` | — |
| 10 | B07 | Prompt contract: answer, quoted line, link, date; a quote not in the page fails | EXEMPT | A plan (tag "planned: contract") | — |
| 11 | B08 | 50 real desk questions, my answer keys, 3 scores, every miss reported | EXEMPT | A plan (tag "constructed · planned"). "Real desk questions" means questions I will write from what members ask me at the desk, with no member names or records. REPO `eval/` holds only `__init__.py` today; no evaluation results are claimed | — |
| 12 | B09 | Not claimed: always accurate; used officially by Marino | PASS | No accuracy, latency or usage numbers anywhere in the film (BANK guardrail: "Never claim eval results, accuracy, latency, or adoption counts") | — |
| 13 | B10 | Staff documents deliberately out; "the finished repo never indexes them" | EXEMPT | A plan. Today REPO's ingest *does* read local SharePoint exports (`ingest/sharepoint.py`); they are gitignored and were never committed (`.gitignore`: `data/sharepoint/*`). The film says "finished repo" | — |
| 14 | B10 | Won't check live court availability | EXEMPT | A scope decision | — |
| 15 | B11 | First piece: public-only index + retrieval check; "you'll know it ran" when the report is in the repo with the crawl date | EXEMPT | A plan and its acceptance test | — |
| 16 | B12 | The Alumni page lists five yearly prices for the same membership, $480 (September) down to $120 (June) | PASS | ALUMNI: $480 Sep 1, $360 Dec 1, $240 Mar 1, $220 Apr 1, $120 Jun 1 (all ending Aug 31, 2027). The $150 quarterly rates are separate and not counted | — |
| 17 | B12 | A model that doesn't know today's date can quote the wrong one | EXEMPT | A stated risk, not a measured result | — |
| 18 | B13 | Contract will pass today's date and require the quoted row; date questions in the evaluation; crawl date on every answer; "only as current as the last crawl" | EXEMPT | A plan and a limitation | — |
| 19 | B14 | "I work the Marino front desk" | PASS | My statement (2026-10-13): I work as a Facility Assistant at Marino, and people there call me "Suhas" because it's easier to say. That's why REPO's `docs/PRD.md` header reads "Author: Suhas Bagwe (FA, Marino Recreation Center)". The repo's commits, including `dd3205e`, are authored by "Shubham Bagwe <bagwe.sh@northeastern.edu>" (checked 2026-10-14) | — |
| 20 | B14 | "I wrote the EventFlow Engine myself, a Node pipeline on Google Cloud" | PASS | `github.com/bagwe-shubham1727/robust-data-processor`: Node.js ingestion and worker services, Cloud Run, Pub/Sub, Firestore. Commits by me, 2025-11-30 to 2025-12-03, with no AI co-author trailers; authorship confirmed by me | — |
| 21 | B14 | "The Marino repo's current code was mostly AI-generated under my direction, so it isn't my proof" | PASS | My statement (2026-10-13). It now names the Marino repo, because "this repo" right after EventFlow was ambiguous | — |
| 22 | B09 | "I can specify, ground and evaluate an AI app, and measure where it's wrong" | CORRECTED | What the finished project will show, not a claim about today's code. The first cut said "build a full-stack AI app", which overclaimed given that marino-rag's code is mostly AI-generated, so it was reworded and re-voiced. My portfolio site was also dropped as front-end evidence (17 of its 38 commits mention Claude) | re-voiced B09 |
| 23 | B15 | Exists today: first version, retrieval and chat code, 60 passing tests, the checks in this film, all run 13 October | PASS | TESTS, SEARCH, ALUMNI (`evidence/`, 2026-10-13) | — |
| 24 | B15 | Will exist: public-only index, Claude under the contract, 50-question evaluation and report | EXEMPT | A plan (dashed outlines on screen) | — |
| 25 | B01, BOUT | My name, spoken | CORRECTED | Kokoro reads "Bagwe" as "bag-wee", so the spoken text spells it "Baag-way"; on screen and in every document it stays "Bagwe" | respelled for TTS only |
| 26 | BOUT | Link github.com/bagwe-shubham1727/marino-rag | PASS | Public repo (GitHub API 200 on 2026-10-13) | — |
| 27 | B06 | Target role new-grad full-stack engineer; reader a hiring manager or engineer; "in sixty seconds" they see the evaluation table, run one command, ask a fee question, watch it refuse off-topic | EXEMPT | Role and reader are my choice (2026-10-13). The 60-second path is planned (tag "constructed · planned repo"): no evaluation table or one-command run exists yet | — |
