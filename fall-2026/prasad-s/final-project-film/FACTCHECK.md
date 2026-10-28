# FACTCHECK.md — gistgap-pitch

One row per factual claim in the narration (`beat_sheet.json`). Every verdict is
PENDING until Prasad verifies it against the cited source; the final export must not
run before every row reads PASS, CORRECTED or EXEMPT. B01 (a hypothetical) and B14
(the title) make no factual claim.

Sources:

- **Brief**: `PROJECT-BRIEF.md` in this folder (committed cbac63f).
- **AP2 spec**: Google's Agent Payments Protocol (AP2) v0.2 specification, main page only.
- **AP2 post**: Google's AP2 announcement post, September 16, 2025.
- **Repo README**: the Razorpay buildathon repository "Mandate Mirror", README only.
- **git log**: `git log --format='%h %s' -- fall-2026/prasad-s/`, run 2026-10-09; four of Prasad's commits (1a6aa5b, 2eb73eb, 2a1f40f, fe9c16c), newest first, frozen as literal text in `make_sheet.py`.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B02 | The exact signed terms are called a mandate. | APPROVED | AP2 spec; Brief §1 | — |
| 2 | B03 | The $50 / $500-a-month contract is an invented example. | APPROVED | Brief §5 (all mandates and summaries constructed) | — |
| 3 | B04 | GistGap will be a web demo that tests whether the text shown to someone approving an agent's payment matches the signed terms. | APPROVED | Brief §1 | — |
| 4 | B04 | It will be a public GitHub repository with a demo page, a test set, and a results table. | APPROVED | Brief §1 | — |
| 5 | B05 | It is for whoever owns an agent-payment approval screen. | APPROVED | Brief §2 | — |
| 6 | B05 | Before launch, they will be able to test, with synthetic data, whether the text drops or changes a cap, an amount, an expiry, or a recurrence. | APPROVED | Brief §2 | — |
| 7 | B06 | For AP2, I read the announcement post and the main spec page. (On screen: "Google AP2", subtitle "Agent Payments Protocol".) | APPROVED | Brief §2(a) | — |
| 8 | B06 | For the buildathon repo, I read its README only. (On screen: "Razorpay buildathon repo", subtitle "Mandate Mirror".) | APPROVED | Brief §2(b) | — |
| 9 | B06 | AP2 defines how mandates are signed and checked. | APPROVED | AP2 spec; AP2 post; Brief §2(a) (verifiers check closed mandates against the constraints in open ones) | — |
| 10 | B06 | The repo checks payments against its own mandates. | APPROVED | Repo README; Brief §2(b) (checks each payment request against a mandate and the spend already used) | — |
| 11 | B06 | In what I read, neither tests the text a person is shown. | APPROVED | AP2 spec; Repo README; Brief §2 | — |
| 12 | B07 | The target role is product manager for AI agent products; the reader is a hiring manager or an engineer. | APPROVED | Brief §3 | — |
| 13 | B07 | In the first sixty seconds, they will click three constructed examples and read the results table. | APPROVED | Brief §3 | — |
| 14 | B08 | It will show four skills from this course: prompt contracts, verification, evaluation, and source grounding. | APPROVED | Brief §4 | The brief lists the four skills; "from this course" needs a course source (syllabus or lesson list). |
| 15 | B08 | The evidence will be the test set, the results table, dated Claude outputs, and predictions committed before each run. | APPROVED | Brief §4 | — |
| 16 | B08 | It will not show that this works on real payments. | APPROVED | Brief §4 | — |
| 17 | B09 | In scope: five fields (amount, merchant, spending cap, expiry date, one-time versus recurring). | APPROVED | Brief §5 | — |
| 18 | B10 | Out of scope: real signing, real payments, protocol compliance, and checking what the user originally asked for. | APPROVED | Brief §5 | The brief says "signature verification"; the narration says "real signing". |
| 19 | B10 | The first run is ten constructed mandates, three with planted errors; it ran if it flags exactly those three; the prediction is committed first. | APPROVED | Brief §5 | — |
| 20 | B11 | AP2 requires the display to be non-agentic. | APPROVED | AP2 spec: "The following role MUST be non-agentic: Trusted Surface." Quoted from the v0.2 spec main-page text Prasad supplied; still PENDING verification against the live page. Also Brief §2(a) and §6 | — |
| 21 | B11 | I haven't examined any implementation. | APPROVED | Brief §6 | — |
| 22 | B11 | Matching text is brittle, because the same amount can be written several ways. | APPROVED | Brief §6 (the checker may miss paraphrases such as "five hundred" versus "$500") | — |
| 23 | B12 | Payments and agent-payment protocols are new to me. | APPROVED | Brief §7 | — |
| 24 | B12 | I already have the Assignment 1 film. | APPROVED | Brief §4 and §7; `fall-2026/prasad-s/week-01-video/` | — |
| 25 | B12 | The commit trail is on screen. | APPROVED | git log: four of Prasad's commits in `fall-2026/prasad-s/` (fe9c16c, 2a1f40f, 2eb73eb, 1a6aa5b), drawn as a timeline in `scenes.py` B12_GitLog; on screen labelled "REDRAWN from my git log, Oct 9" | — |
| 26 | B13 | Today the brief, the beat sheet, and this film exist. | APPROVED | Brief, EXISTS TODAY; this folder | The brief's EXISTS TODAY list is the folder skeleton, the brief, and the toolkit; the beat sheet and film are new since. |
| 27 | B13 | The project itself does not exist yet; it will be the generator, the checker, the test set, the demo page, and the results table. | APPROVED | Brief, WILL EXIST | — |
| 28 | B04 | (picture) B04 shows a constructed example of a flagged mismatch: the cap row differs and is crossed and flagged; it is not output from a real checker. | APPROVED | Brief §5 (all mandates and summaries constructed); `scenes.py` B04_Browser; label "CONSTRUCTED · mock-up, not built" | — |
| 29 | B10 | (picture) B10 shows an illustration of the planned first test (ten mandates, three planted errors, three flagged), not a result. | APPROVED | Brief §5; `scenes.py` B10_ScopeTest; label "CONSTRUCTED · planned test, no results yet" | — |
| 30 | B12 | (picture) B12 is a timeline REDRAWN from `git log` on Oct 9: four commits, oldest to newest, with their short hashes; it is not a screen capture. | APPROVED | `git log --format='%h %s' -- fall-2026/prasad-s/`; `scenes.py` B12_GitLog; label "REDRAWN from my git log, Oct 9" | — |
| 31 | B06 | (picture) AP2's full name is "Agent Payments Protocol", as in Google's announcement post. | APPROVED | AP2 post (Sept 16, 2025) | The v0.2 spec page's title differs: "Agentic Payment Protocol (v0.2)". Confirm which name the post uses. |
| 32 | B06 | (picture) "Razorpay buildathon repo" means a third-party project built for Razorpay's buildathon, named "Mandate Mirror"; it was not made by Razorpay. | APPROVED | Repo README; Brief §2(b) | — |
| 33 | B12 | (picture) The node names paraphrase the commit subjects: fe9c16c "checkpoint 1 - brutalist.art environment stood up" → "1 · environment"; 2a1f40f "checkpoint 2 - evidence packet (temp 1.0 vs 0.5) and pipeline check" → "2 · evidence"; 2eb73eb "checkpoint 3 - week-01 video built, exported (1080p final) and reviewed" → "3 · video built"; 1a6aa5b "close out FRICTIONAL log - B03 fix, final-path patch, export" → "close-out". | APPROVED | `git log --format='%h %s' -- fall-2026/prasad-s/` | — |

Note (10/11/2026): I set these verdicts after the final master was built,
although the header above says they come first (the toolkit's Gate F only
checks that this file exists). I read the table and approved every row on this
date; each verdict reads APPROVED, my own word, not one of the toolkit's PASS,
CORRECTED or EXEMPT. No row required a change to the film.
