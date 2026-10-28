# Evaluation — first 6 of 25 rows (2026-10-12)

## Executive summary

**What this is:** the first six rows of the 25-company evaluation my pitch promises. For six employers I chose
(PayPal, Visa, Goldman Sachs, Mastercard, BlackRock, LSEG), it compares what my co-op sponsor check finds in
its current dataset with what the official U.S. government H-1B Employer Data Hub lists for fiscal year 2026.

**Why read it:** it is the first real evidence of where the tool is right and where it falls short, and it is
what the film means by "the first rows ran."

**What it found:**
- All six employers file H-1B petitions in the official hub (FY2026). My dataset has a sponsorship record for
  **none** of them: five are missing entirely, and Visa has a row with no approval count.
- The tool behaved as designed in all six: it said **unknown**, never zero, and told the student to ask a person.
  The failure is coverage, not a false "no".
- **A real flaw in my name matcher:** it strips "CO" and "LLC" but not "AND", so the hub's
  "GOLDMAN SACHS AND CO LLC" becomes "GOLDMAN SACHS AND" and would never match a student typing
  "Goldman Sachs". It must be fixed before the hub becomes the second data source.
- Name matching is the hard part, as the pitch predicted: every company appears under 2–7 legal names,
  substring traps are common ("J GOLDMAN AND CO L P", "IMMIVISA LAW GROUP"), and "LSEG" finds nothing — the
  hub knows it only as "London Stock Exchange Group Holdings".

## Run record

- **Who / how:** Claude Code, on Arundhati Kandelkar's instruction, 2026-10-12 ~18:45 ET.
- **Dataset side:** `eval_first_rows.py`, which imports my recipe's own `norm_name` and `resolve_company`
  (fork `arundhatik26/the-reallocation-engine` at `03784b0`; recipe unchanged). Output:
  `eval-first-rows-dataset-2026-10-12.json`. CSV
  `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`,
  sha256 `eccdee2addf472b1639269f42eec693b083b7ce251347d5fd0b2856cfdae6270`.
- **Hub side:** the USCIS H-1B Employer Data Hub dashboard, Fiscal Year = 2026, typing each word into the
  Employer (Petitioner) Name filter and reading every name it listed. No counts were read per company and no
  file was downloaded. Names are copied exactly as listed.
- **Not tested:** whether any of these employers sponsored *software* titles — the hub has no job-title field,
  so that check needs the DOL disclosure data. Other fiscal years. The remaining 19 companies.

## The six rows

| # | Company (as a student types it) | My dataset (recipe matcher) | Hub FY2026 — names listed for the search word | Agree? | Lesson |
|---|---|---|---|---|---|
| 1 | PayPal | `not-in-dataset` (no CSV name contains "PAYPAL") | PAYPAL DATA SERVICES INC · PAYPAL INC | **No** — hub has it, dataset doesn't | coverage gap; "PAYPAL INC" normalises to "PAYPAL", so a hub join would match |
| 2 | Visa | `no-sponsorship-record` — CSV line 28865 "VISA INC", Total Approvals blank | VISA U S A INC · VISA TECHNOLOGY AND OPERATIONS LLC (+ substring traps: IMMIVISA LAW GROUP, METHOD IMPROVISATION INC, MY VISA SERVICES, INC., TELEVISAUNIVISION MANAGEMENT COMPANY, V-ENVISAGE SOLUTIONS INC, VISAM TECHNOLOGIES INC.) | **No** — hub files under different legal names | the dataset's "VISA INC" is not a name the hub uses; "VISA U S A" ≠ "VISA" to an exact matcher |
| 3 | Goldman Sachs | `not-in-dataset` | GOLDMAN SACHS AND CO LLC · GOLDMAN SACHS BANK USA · GOLDMAN SACHS SERVICES LLC · GOLDMAN SACHS WEALTH SERVICES L P (+ trap: J GOLDMAN AND CO L P) | **No** | matcher flaw: "…AND CO LLC" → "GOLDMAN SACHS AND" |
| 4 | Mastercard | `not-in-dataset` | MASTERCARD INTERNATIONAL INCORPORATED · MASTERCARD TECHNOLOGIES LLC | **No** | coverage gap; two entities, which one a co-op is with matters |
| 5 | BlackRock | `not-in-dataset` | BLACKROCK CORPORATION US INC · BLACKROCK FINANCIAL MANAGEMENT INC · BLACKROCK INSTITUTIONAL SERVICES INC · BLACKROCK INSTITUTIONAL TRUST COMPANY N A · BLACKROCK INVESTMENT MANAGEMENT LLC · BLACKROCK MICROSYSTEMS LLC DBA BLACKROCK NEUROTECH · BLACKROCK RESOURCES LLC | **No** | 7 names, at least one an unrelated company (BlackRock Neurotech) |
| 6 | LSEG | `not-in-dataset` | "LSEG": *No matches.* — "LONDON STOCK": LONDON STOCK EXCHANGE GROUP HOLDINGS INC · LONDON STOCK EXCHANGE GROUP HOLDINGS, INC. | **No** | brand name ≠ legal name; the two hub names differ only by punctuation (both normalise to the same string — good) |

**Totals:** 6 of 6 listed in the hub · 0 of 6 with a sponsorship record in my dataset · 6 of 6 correctly
reported as unknown rather than zero · 1 matcher defect found (the "AND" case).

## Also seen on the hub (FY2026 top-employers chart)

JPMORGAN CHASE AND CO is ranked **#9** with **2,112** beneficiaries approved (chart footer: "Data as of:
6/30/202…", cut off on screen; the page describes the data as FY2026 Q3). My dataset has no row for it.
