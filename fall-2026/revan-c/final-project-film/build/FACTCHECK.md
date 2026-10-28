# FACTCHECK — Remnix Agent pitch film

Every factual claim in the narration or on screen. Verdicts: PASS (checked against
the source), CORRECTED (changed after checking), EXEMPT (a plan, stated as "will",
not a fact). Checked 2026-10-14.

Status: rows 3–8 and 11–14 checked by Claude in Revan's build session on 2026-10-14; rows 2, 9, 10, 16, 16b are Revan's own statements and checks (2026-10-14). Final sign-off: Revan C, pending. Updated 2026-10-25 for the resubmission (rows 1, 1b, 1c, 17, 18).

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | The project does not exist yet (spoken); the voice is synthetic and the script was written with Claude and reviewed by Revan (on screen) | CORRECTED | Revan; Kokoro `af_bella`; SOURCES.md | Was "the words are mine" (spoken) / "words by Revan" (on screen); graded down because Claude drafted the narration. 2026-10-25: the false spoken claim was removed and the on-screen label now reads "Synthetic voice (Kokoro) · written with Claude, reviewed by Revan". |
| 1b | BIDEA | Revan is a graduate student at Northeastern | PASS | Revan (confirmed 2026-10-25) | — |
| 1c | BPLAIN | Sending money abroad loses part of it to fees and the exchange rate | PASS | Money Map's own definition: "Fee = everything you lose compared with the mid-market rate: transfer fees plus any exchange-rate markup" (viewed 2026-10-14) | — |
| 2 | B00 | Revan built Money Map as a software engineer co-op at the MIT Digital Currency Initiative; built alone | PASS | Revan (stated 2026-10-14) | — |
| 3 | B00 | Money Map is public and live; compares banks, apps, transfer services and stablecoins for USD→Mexico | PASS | https://mit-dci.github.io/payments-dashboard/ viewed 2026-10-14 ("Compare banks, payment apps, money transfer services and stablecoins") | — |
| 4 | B00 | The screenshot is real, taken 2026-10-14 | PASS | `pantry/money-map-2026-10-14.png`, headless Chrome, 16:20 EDT | — |
| 5 | B01 | Money Map is a dashboard: you pick filters and read numbers | CORRECTED | Screenshot shows Send-via filters incl. Debit Card | Earlier draft implied Money Map can't answer "what if I pay by debit card?" — it can, via a filter. Replaced with a plain-words "why" question. |
| 5b | B01 | A sender's question might come in plain words | CORRECTED | No user data exists | Was "senders often ask in plain words": an unbacked claim about users. Softened to "might" in Step 6 honesty pass, 2026-10-14. |
| 6 | B05 | Sending $1,000 with Wise cost $7.54 (0.75%) on Money Map | PASS | Screenshot: Wise, ACH → Bank deposit, $7.54, 0.75%, remittance quotes Oct 14 00:51 EST | — |
| 7 | B05 | The answer card is constructed, not real output | PASS | Labelled CONSTRUCTED on screen for the whole beat | — |
| 8 | B06 | Money Map models a "stablecoin sandwich": USD → stablecoin → blockchain → MXN | PASS | Money Map page section "The stablecoin sandwich", viewed 2026-10-14 | — |
| 9 | B07 | Wise's comparison page does not include stablecoin routes | PASS | Revan's check, 2026-10-14 | — |
| 10 | B07 | Monito does not include stablecoin routes | PASS | Revan's check, 2026-10-14 | — |
| 11 | B07 | World Bank RPW covers US→Mexico | PASS | https://remittanceprices.worldbank.org/corridor/United-States/Mexico viewed 2026-10-14 | — |
| 12 | B07 | RPW's newest data for this corridor was collected in August 2025 | PASS | Same page: "Data collected on: Aug 04, 2025 - Aug 28, 2025" (Third Quarter 2025) | — |
| 13 | B07 | So a sender will get stablecoin routes next to the usual options, every number sourced | EXEMPT | Plan (future tense). $200/$500 detail moved to PROJECT-BRIEF.md (source: https://remittanceprices.worldbank.org/methodology) | Cut from narration 2026-10-14 for runtime |
| 14 | B12 | Money Map's stablecoin route moved from $7.42 to $8.99 within about an hour on 2026-10-14 | PASS | Page text read in this session: USDC via Bitso $7.42 (stablecoin prices "updated Oct 14 · 15:10 EST"); screenshot: USDC $8.99 (bitso bid "Oct 14 · 16:12 EST") | — |
| 15 | B13 | Reviewer could conclude Revan can build a small, checked AI tool; evidence will be test scores + wrong-answer log | EXEMPT | Plan, stated as "will" / "could" | Replaced the earlier B13 ("ask MIT DCI first") on 2026-10-14: Revan confirmed Money Map's data may be used |
| 16 | B14 | Picked because it builds on Money Map and points at fintech work Revan wants | PASS | Revan's project statement (target role: software engineer at fintech/crypto companies) — Revan to confirm wording | — |
| 16b | B14 | Existing skills: cost modeling, dashboard work, GitHub Pages; new: source grounding, tool calling, eval sets, PostgreSQL, FastAPI | PASS | Revan's project statement | — |
| 16c | B08 | Readers also include researchers and policymakers who study remittance costs | PASS | Revan (stated 2026-10-14); scoped to the one corridor Remnix covers | — |
| 17 | BPLAIN, B02–B04, B08–B11, B13, B15 | Everything about Remnix (repo, tables quotes/fx_rates/snapshots, POST /ask, tools get_quotes/compute_cost, pytest test set, log, scope) | EXEMPT | Plans, narrated with "will"; design names approved by Revan 2026-10-25 | — |
| 18 | B06 | A stablecoin is a digital dollar | PASS | General definition (USDC, the coin Money Map's route uses, is pegged to the U.S. dollar). The terms card (BDEFS) was removed 2026-10-25. | — |
