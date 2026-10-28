# FACTCHECK — atharva-sponsorsql-pitch

Every factual claim in the narration or on screen, with its source. Project claims are all future tense ("will"): nothing in SponsorSQL exists yet.

| # | Claim | Beat | Source / status |
|---|---|---|---|
| F1 | The U.S. Department of Labor publishes LCA (H-1B, H-1B1, E-3) disclosure files. | B02 | DOL OFLC Performance Data page, https://www.dol.gov/agencies/eta/foreign-labor/performance (opened 2026-10-13) |
| F2 | The latest file is FY2026 Q3: determinations from October 1, 2025 to June 30, 2026, cumulative for the fiscal year so far, and some records may still change. | B07, B10 | DOL Performance Data page, "Latest Quarterly Updates" (checked 2026-10-24) |
| F3 | An LCA is filed by an employer on Form ETA-9035. | B02 | LCA record layout, page 1 (FY2025 Q4 layout read 2026-10-14; same form for FY2026) |
| F4 | Columns include EMPLOYER_NAME, JOB_TITLE, WORKSITE_CITY, WAGE_RATE_OF_PAY_FROM, and a separate TRADE_NAME_DBA column. | B02, B08 | Header row of LCA_Disclosure_Data_FY2026_Q3.xlsx (98 columns), read 2026-10-24 |
| F4b | The file includes personal contact columns (EMPLOYER_POC_*, AGENT_ATTORNEY_*, PREPARER_*), which the tool will drop. | B07 | Same header row |
| F4c | The data file was downloaded; nothing is loaded or built. | B10 | LCA_Disclosure_Data_FY2026_Q3.xlsx, 251,850,891 bytes, downloaded 2026-10-24, SHA-256 f8ca8448a528671f784d3692923775a13741c99caec2816b2fe30c8885bd28b3 |
| F5 | The data may contain typos and other anomalies from employer or internal data entry. | B08 (risk) | DOL Performance Data page, "Disclosure Data" section |
| F6 | Given the FY2026 Q3 record layout and one question, ChatGPT wrote a query, listed 15 assumptions (including that only the first worksite is examined), and did not run it ("Actual count: Not determined here"). Asked in a follow-up to run it, it reported 40 from its own run of the same query; not independently checked. | B04 | `sponsorsql/evals/chatgpt-test-2026-10-24.md`: GPT-6 (high), run by the author on 2026-10-24, reply verbatim |
| F7 | Vanna.ai has not been tested the same way yet. | B04 | Said on screen ("not tested yet") and in narration |
| F8 | An LCA filing is not a job offer, not proof that sponsorship is available, and not an approved visa petition. | B07 | Scope statement from PROJECT-BRIEF.md; an LCA is an employer attestation to DOL, separate from a USCIS petition decision |
| F9 | "EXAMPLE DATA LLC" and its variants, and the 1-vs-3 count. | B08 | CONSTRUCTED: invented to illustrate the risk; labelled on screen |
| F10 | "questions 10, passed —, failed —" table. | B05 | CONSTRUCTED mock-up; 10 is the planned first test set; no results exist; labelled on screen |
| F11 | The cold-open composer reply. | B00 | CONSTRUCTED: not a Claude response; labelled on screen |

No Claude response appears anywhere in the film.
