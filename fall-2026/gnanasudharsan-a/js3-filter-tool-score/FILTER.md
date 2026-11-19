# FILTER.md — what reaches Ananya, and why
Version 1.0 — 2026-11-19. Written from persona/ananya-rao.* before reading any posting in the corpus
(only the board counts 638 / 169 / 92 were seen). Every later change gets a new version number and a
line in the changelog at the bottom, with what was measured.

## 1. The filter
A posting is checked in two stages. Matching is case-insensitive and on **whole words** (word
boundaries), never substrings.

### Stage A — hard rejects (any one rejects the posting)
| id | rule | reason |
|---|---|---|
| A1 | Title contains a seniority word: senior, sr, staff, principal, lead, manager, director, head, vp, distinguished | She is a new grad (MS Dec 2026); these titles mean years of experience she does not have. |
| A2 | Location is known and is neither in the US nor remote | Her persona needs a US-based or remote role. |
| A3 | Text states the role will not sponsor a visa ("unable to sponsor", "not able to sponsor", "no visa sponsorship", "without sponsorship now or in the future") or requires U.S. citizenship ("U.S. citizenship required", "must be a U.S. citizen") | Her persona: needs_sponsorship true (F-1, pre-OPT, H-1B from 2027). An explicit disclaimer or a citizenship requirement rules the role out. Silence is not a disclaimer. |
| A4 | Text requires N+ years of experience with N >= 3 ("3+ years", "5+ years of experience") | Mid-level and above; a "1-3 years" or "2+ years" range does not reject. |
| A5 | Text says a PhD is required | Her degree is an MS; "PhD preferred" does not reject. |
| A6 | Text requires a security clearance ("security clearance", "TS/SCI", "secret clearance", "clearance required") | Her persona excludes roles requiring an active clearance, and she cannot hold one on an F-1. |
| A7 | Text says the role is unpaid ("unpaid", "volunteer") | Her persona excludes unpaid roles. |

### Stage B — score (only for postings that pass Stage A)
| id | component | points | reason |
|---|---|---|---|
| B1 | Title has a role phrase: machine learning, ml engineer, ai engineer, applied ai, nlp, llm, research engineer | 3 (once) | Her target roles (resume.json target_roles) are hands-on ML / AI / NLP engineering, including Research Engineer. |
| B2 | Content has topic words: pytorch, transformers, hugging face, natural language, nlp, llm, large language model, embeddings, retrieval, rag, fine-tuning, inference, mlops, evaluation | 1 per distinct word, max 5 | The work itself is ML engineering, not only the title. Capped so long postings cannot win by repetition. |
| B3 | Content names her shipped skills: python, pytorch, sql, transformers, sentence-transformers, fastapi, mlflow, postgresql, aws | 1 per distinct skill, max 4 | She can do the job with what she has shipped. Capped for the same reason. |

**Keep** a posting if it passes Stage A and scores **>= 5**. Reason: B1 alone (3) is not enough. A role
title also needs at least two signals from the text that the work and the skills fit.
**Close call:** score 4, 5 or 6 (sampled in the audit).

## 2. Evidence rules (for every claim in a shortlist justification)
A claim is one sentence about one property: role, level, location, sponsorship or skills.
- **Supported**: a span of the posting's own text (title, location or content) states it. The span is quoted with its field.
- **Contradicted**: a span of the posting states the opposite.
- **Insufficient**: no span either way. Knowledge about the company, or what "most postings like this" say, does not count.
- A match of my filter words is **not** evidence that a claim is true (relevance is not entailment).

**Abstention ("I cannot tell"):** the agent does not call a posting relevant, and says "I cannot tell", when
(a) the content is missing or empty, or (b) the location is missing, or (c) the level claim is insufficient
**and** the title has no level signal. Sponsorship that is merely unmentioned is labeled insufficient but
does not by itself force abstention, because her rule only rejects an explicit disclaimer.

## 3. Expected sources
| board | system | fields the filter reads | expected gaps |
|---|---|---|---|
| greenhouse:anthropic | Greenhouse | title, location.name, content (HTML), departments | none expected |
| ashby:notion | Ashby | title, location + secondary locations, descriptionHtml/Plain, department | updated_at is None (not published by Ashby) |
| lever:spotify | Lever | text (title), categories.location / allLocations, description + lists + additional | updated_at is None |
| greenhouse:zz-no-such-board-7375 | Greenhouse | none (deliberate 404 from JS2) | always fails; its postings are absent, not zero |
When a field is missing, the filter treats it as missing, never as a default value: a missing location
cannot pass or fail A2 and forces "I cannot tell"; a failed board is reported as excluded from the shortlist.

## 4. Wrong versions my tests must catch
| # | wrong version | why it is plausible | what it breaks |
|---|---|---|---|
| W1 | Substring matching instead of whole words | `"ml" in text` looks simpler | "ml" matches **html**/**xml**, "ai" matches **email**/**maintain**, "lead" matches **leading** |
| W2 | Score by raw keyword count (no caps) | "more matches = more relevant" | a long posting repeating "python" 30 times outranks a short ML posting |
| W3 | Missing location treated as US (or as a reject) | `location or ""` is a common default | a posting with no location is decided instead of "I cannot tell" |
| W4 | Any "N years" rejects, including ranges and small N | one regex for years | "1-3 years" or "2+ years" wrongly rejects entry-level roles |
| W5 | Title-only filter (Stage B ignores content) | titles are short and clean | a "Machine Learning" title with sales/marketing content is kept |

## Changelog
- 1.0 (2026-11-19): first version, from the persona only (profile.yml: target roles, needs_sponsorship, excluded clearance and unpaid roles, open_to_remote). Nothing measured yet.
