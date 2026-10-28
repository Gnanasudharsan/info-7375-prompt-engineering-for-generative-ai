# Project Brief — SponsorSQL (working title)

**Atharva Hambir · INFO 7375 · Target role: Data Analyst · Stack: Python, DuckDB, Claude**

This is a pitch. Nothing in this project has been built yet; the data file has been downloaded, but not loaded. Everything below is written as "will" unless it is listed under *Exists today*.

## 1. What is it?
SponsorSQL will let an international student ask a question about public H-1B filing data in plain English, then show the SQL Claude wrote, the answer, and whether that answer matched a hand-checked answer key. When it is done, it will be a GitHub repository with the question tool, a fixed test set, and an evaluation log that records every question Claude got wrong and why.

## 2. Why would anyone care?
An international student looking for work needs to know which employers have filed for H-1B workers in their field and city, and at what wages. That information is public in the U.S. Department of Labor's LCA disclosure files, but each file is a large spreadsheet most students cannot easily query. I tested one alternative and looked at another. **ChatGPT, tested 2026-10-24** (GPT-6, high mode; one question; the FY2026 Q3 record layout attached; reply saved verbatim in `evals/chatgpt-test-2026-10-24.md`): asked how many certified H-1B cases are for Data Analyst jobs with a worksite in Boston, it wrote a careful DuckDB query and listed 15 assumptions. Several of them could change the count: only the first worksite on each filing is checked, `Certified-Withdrawn` is excluded, titles like `Data-Analyst` are excluded, and the state is assumed to be written `MA`. In that first reply it had not run the query ("Actual count: Not determined here"). When I asked it to run it, it reported **40** cases, but from its own query under the same assumptions. Nothing independent has checked that number, or told me which of those assumptions change it. **Vanna.ai** is built for turning questions into SQL using database context; I have used it, but I have not tested it this way yet. So I am not claiming SponsorSQL will be more accurate. The specific difference is that SponsorSQL will test assumptions like these instead of only listing them. Every test question will have the SQL Claude wrote, an expected answer I worked out independently from the real file, a recorded pass or fail, and a written explanation whenever it fails. The ChatGPT question above will be one of the ten; its 40 is a number to test, not the answer key.

## 3. Who opens it, and what do they do?
The reader is a hiring manager for a Data Analyst role. In the first sixty seconds they will open the README and see the evaluation table: how many test questions there are, how many Claude answered correctly, and a link to the failure log. Then they will be able to run one command, ask their own question, and see the SQL and the answer. The end user is an international student looking for a sponsoring employer.

## 4. What does it prove about me?
It will show SQL and data cleaning on a real, messy public dataset. It will also show four things this course teaches. **Prompt contracts:** Claude gets the table schema and written rules for the SQL it may write. **Verification:** each answer is compared with an answer I wrote and checked by hand. **Evaluation:** a failure rate on a fixed test set, with every failure sorted by its cause. **Source grounding:** every answer names the filing year, the source file and the query. A reviewer could fairly conclude that I can query real data and that I measure where an AI's SQL is wrong instead of trusting it. The evidence will be the test set, the run logs and the failure log in the repository.

## 5. What is in, what is out, what comes first?
**In:** the latest LCA disclosure file, FY2026 Q3 (determinations from October 1, 2025 to June 30, 2026, from the Department of Labor's OFLC Performance Data page), loaded into DuckDB, with questions about employers, job titles, locations and wages. The file also carries personal contact columns (employer contacts, attorneys, preparers, with names and emails); the load step will drop them. The Q3 file covers part of the year and the DOL says some records can still change, so the answer key will be tied to this exact file by its SHA-256 checksum.
**Out:** it will not tell anyone whether they will be sponsored, and it will not give immigration or legal advice. An LCA filing is not a job offer or a visa approval, and the tool will say so.
**First:** ten questions, a hand-checked answer key, Claude's SQL run against both, and a printed pass/fail table. Someone will know it ran because the run log will record the date, the command, every query and the result, and running the same command will reproduce the table.

## 6. What could sink it?
The data is messy. The same company can appear under slightly different spellings of its name, and the file has a separate column for trade names (`TRADE_NAME_DBA`, confirmed in the FY2026 Q3 header row). The same role also appears under many job titles. Claude's SQL could look correct and still undercount. This is the failure most likely to fool a user. To catch it, I will write test questions built around these name and title variations, compare the counts Claude gets with my hand-checked ones, and log every mismatch. If Claude keeps failing on them, the tool will show the matching rows it used instead of a single total, so the user can check the answer for themselves.

## 7. Why this project?
It is a mix of showing off and learning. **Skills I already have:** SQL, Python and pandas, and dashboards/BI, from earlier academic and professional work. That earlier work includes a SQL and Power BI data-modelling project and a crime-data analysis in Snowflake. It is separate from this project and is not shown in the film. SponsorSQL's own SQL and evaluation results will be the evidence for these skills. **Skills that are new to me:** building an evaluation harness for LLM-written SQL, writing prompt contracts for code generation, and measuring and reporting failure rates honestly. I picked this domain because I am an international student. Finding employers that have filed H-1B applications in the past matters to international students looking for work in the U.S., and I want them to be able to explore that public data through simple questions instead of having to understand a complex dataset or write SQL. The tool will say clearly that an H-1B Labor Condition Application is not proof of a job offer, of sponsorship being available, or of an approved visa petition.

---

### Exists today
- This brief (written 2026-10-13, revised 2026-10-24).
- One ChatGPT test (2026-10-24): one question against the record layout, reply saved verbatim in `evals/chatgpt-test-2026-10-24.md`.
- The data file: `LCA_Disclosure_Data_FY2026_Q3.xlsx`, downloaded from the DOL on 2026-10-24 (251,850,891 bytes, SHA-256 `f8ca8448a528671f784d3692923775a13741c99caec2816b2fe30c8885bd28b3`). I checked its header row (98 columns); nothing has been loaded or queried yet. It is not in the repository because it is over GitHub's 100 MB file limit.

### Will exist
- The DuckDB database built from the FY2026 Q3 file, without the personal contact columns
- The prompt contract (schema plus SQL rules)
- The ten-question test set with its hand-checked answer key
- The run script and its dated run logs
- The pass/fail table and the failure log
- A README that shows the evaluation table first
