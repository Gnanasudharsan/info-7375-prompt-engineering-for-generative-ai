# PROJECT-BRIEF — Marino Desk Assistant (repo: marino-rag)

Shubham Bagwe · INFO 7375 final project pitch · 2026-10-13. Past tense means it exists and was re-run on 2026-10-13 (`evidence/`, checks run by Claude Code, re-opened by me before submitting). Everything else is "will".

**1. What is it?** A chat assistant that will answer front-desk questions (fees, hours, guest rules) at the Marino Recreation Center, Northeastern University's campus gym, from the university's **public recreation website**. It will quote the page it used, and say "I don't know" when the site doesn't say. Done means a **public GitHub repo** ([`bagwe-shubham1727/marino-rag`](https://github.com/bagwe-shubham1727/marino-rag)) with a Python/FastAPI backend, a Next.js chat UI, **Claude** writing the answers, a 50-question evaluation set with my answer keys, and a report that lists every miss.

**2. Why care?** A desk assistant has a member waiting. The two alternatives I looked at:
- **manual lookup**: scrolling the site; the Alumni page alone is ~780 words;
- **the site's own search**, which returns pages, not answers. On 2026-10-13, "guest pass" gave 5 pages with *Home* first.

**It will save the desk assistant the scroll: one answer, with the quoted line and a link, which the site search doesn't give.** No users, adoption or accuracy are claimed.

**3. Who opens it?** Target role: **new-grad full-stack software engineer.** Reader: a hiring manager or engineer (end user: desk staff). In 60 seconds they'll see the evaluation table in the README, run one command, ask a fee question, get a cited answer, and watch it refuse an off-topic one.

**4. What does it prove?**
- **Source grounding** (exists in code): it retrieves 5 chunks and reranks to 3; the prompt requires citations and a refusal line.
- **Prompt contract** (will): Claude returns `{answer, quote, url, as_of}` or "not on the site"; a quote that isn't in the retrieved text fails.
- **Evaluation** (will): 50 questions I write from what members ask me at the desk (no member names or records), with my answer keys, scoring citation hit rate, correctness and refusals, and logging every miss.

Fair conclusion: I can specify, ground and evaluate an LLM app and measure where it's wrong. Not fair: that it is accurate in general, or used officially by Marino.

**5. In / out / first.**
- **In:** public `recreation.northeastern.edu` pages.
- **Out, deliberately:** internal staff documents (SharePoint training files), which the finished repo will never index; also live court availability.
- **First:** a public-only index plus a retrieval check: a script counts how many of the 50 questions find their source page in the top 3. *You'll know it ran* when `eval/report.md` is committed with per-question rows and the crawl date. That step also updates the repo's README and PRD, which still describe SharePoint ingestion.

**6. What could sink it?** **Date-dependent prices.** On 2026-10-13 the Alumni page listed five annual prices for one membership by start date: $480 from Sep 1, $360 from Dec 1, then $240, $220 and $120. A model that doesn't know today's date can confidently quote the wrong row. **I will:** pass today's date into the contract, require the quoted row, put date questions in the evaluation, and show the crawl date on every answer. **Limitation:** it is only as current as the last crawl.

**7. Why this project?** I work as a Facility Assistant at the Marino front desk, and these are the questions I get. It's a mix.
- **Already have:** backend and cloud. I wrote EventFlow Engine myself ([`robust-data-processor`](https://github.com/bagwe-shubham1727/robust-data-processor), Nov–Dec 2025): Node.js on Cloud Run, Pub/Sub, Firestore, with a load test in its README.
- **Honest:** marino-rag's current code was mostly AI-generated under my direction, so I don't count it as proof.
- **New to me:** writing answer keys, measuring an LLM's misses, and prompt contracts with Claude.

### Exists today (re-run 2026-10-13)
- marino-rag `dd3205e`: parsers and same-domain crawler, BGE retrieval with cross-encoder rerank, FastAPI `/chat`, a Next.js UI with source cards; **60 tests pass**.
- The site-search and Alumni-page checks (`evidence/`); this film, its beat sheet and its gate reports.

### Will exist
- A public-only index, with answers moved from OpenRouter to Claude under the prompt contract.
- The 50-question evaluation set, my answer keys, and `eval/report.md`, which lists every miss.
- A one-command run, the README evaluation table, and an updated README and PRD.
