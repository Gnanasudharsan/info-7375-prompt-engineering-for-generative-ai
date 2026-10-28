# PROJECT-BRIEF — Co-op Sponsor Check

Arundhati Kandelkar · INFO 7375 Final Project pitch · 2026-10-12, revised 2026-10-25. Past tense = shown in `evidence/`; everything else = will.

**1. What is it?** A Python tool that tells an international student whether a company has a public record of
sponsoring *software* jobs, and says "unknown" instead of "no" when the record is missing. When done: a public
GitHub repository (in my Reallocation Engine fork) with the tool, a second public data source, a 25-company
hand-checked evaluation set, and a log of where it fails.

**2. Why care?** It stops an F-1 student choosing a co-op from reading "not in my spreadsheet" as "won't sponsor
me." Alternative I looked at: the official **USCIS H-1B Employer Data Hub** (searched 2026-10-12 by Claude on my
instruction). It is the source of truth — free, downloadable, and it lists JPMorgan Chase, which my dataset lacks —
but it has **no job-title filter**, is searched one employer at a time, and its name search is loose ("Mellon" →
three BNY entities and Carnegie Mellon University). Mine will check a whole list for **software titles**, check
**co-op dates against two graduation scenarios**, and keep **"not in data" separate from "zero"**.

**3. Who opens it?** Target role: software / full-stack developer. Reader: a hiring manager or engineer at a bank or
fintech. In 60 seconds: README, one command, a report that says unknown where the data is silent, beside a table of
where the tool was right and wrong.

**4. What does it prove?** *Verification* — every value is labelled record / judgment / your input (exists; tested).
*Evaluation* — 25 answers checked against the hub (all 25 rows ran; predictions written first). *Source grounding* — every record-sourced value in
the run log cites its CSV line (exists: 48 `csv_line` fields). A reviewer can conclude I build small, tested data
tools and report where they fail — **not** that it is accurate for every company.

**5. In / out / first.** Out: no immigration advice, no visa predictions. In: sponsorship history for software titles
from public government-derived data. First: the evaluation table — **all 25 rows ran (2026-10-12 and 2026-10-25)**.

**6. What could sink it?** Company names. The hub lists Goldman under four legal names plus "J GOLDMAN AND CO L P";
the evaluation found two matcher defects: "…AND CO LLC" (fixed, with a test) and brand names (typing "Robinhood" misses ROBINHOOD MARKETS INC, 824 approvals — not yet fixed). Response: no fuzzy
auto-match; candidates go to a human (gate G2, exists); traps stay in the evaluation set; I report how many of 25
needed a human. Known limit: the dataset is built from an SEC list of funded startups, so big banks are missing.

**7. Why this project?** *(chosen 2026-10-12 from options Claude offered)* My own question — I am an international
student choosing a co-op. A mix. **Already have:** Java and Spring Boot services — evidence: Software Developer at
Giesecke+Devrient (G+D), Pune, Aug 2021–Sep 2024. This project does not show that work. **New:** joining a second public data source into a Python tool.

## Exists today

- Recipe + prototype `coop_sponsor_check.py`, fork commit `03784b0` (2026-10-03); PR
  [nikbearbrown/the-reallocation-engine#40](https://github.com/nikbearbrown/the-reallocation-engine/pull/40) open, DRAFT, not merged.
- 17 passing tests; sample run over 7 roles covering failure cases F1–F6 (re-run 2026-10-10, same results).
- Gates G1–G5 incl. the human name check (G2); every value labelled; CSV line cited in the run log.
- All 25 evaluation rows (`evidence/eval-25-rows-2026-10-25.md`): every company searched is in the hub; my tool found 2; it
  never guessed no; it missed three strong sponsors stored under legal names (Robinhood, SoFi, Chime).
- The "AND" defect fixed with a test using the hub's exact Goldman name (fork branch `final/arundhatik26-and-fix`,
  `379252f`; 18 tests pass).

## Will exist

- A fix for brand-name lookups (Robinhood, SoFi, Chime); then the USCIS hub joined as a second data source.
- A written failure analysis from the 25 rows.
- Source citations shown in the human-readable report, not only the run log.
- A README for a hiring manager with a one-command demo.
