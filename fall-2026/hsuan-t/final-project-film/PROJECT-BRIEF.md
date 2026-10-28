# PROJECT BRIEF — The Reallocation Engine CLI

## 1. What is it?
I'm Isaac Tai, an F-1 student. My final project will be a command-line tool for F-1 STEM OPT students that checks, before you apply, whether a company has really sponsored work visas before, using government records instead of AI guesses. When it is done, it will be a local CLI plus a markdown decision report: it will score SWE, DevOps, QA, and cloud infrastructure roles against public immigration and corporate filings and give a clear `Apply` or `Skip`. What exists today is a prototype recipe (`tisaac-swe-stem-opt`, committed 2026-10-03) that scored three test roles on 2026-10-04 (`role-scores.md`).

## 2. Why would anyone care?
International students on F-1 STEM OPT face a 90-day unemployment clock and limited application capacity, so applying to a company that never sponsors is expensive.

**The real tool I tried: ChatGPT.** I asked it about sponsorship directly. The specific difference: with ChatGPT I had to ask about one company at a time, and every answer still had to be checked by hand. This tool will turn that check into a fixed script (an SOP) built for my own job-search situation: sponsorship will come straight from government records (the Labor Department's H-1B visa filings and the SEC's Form D funding filings), matched by me, and AI will only do the part it is good at, reading the job description. Every score will carry a source tag (`[record]`, `[rule-gate]`, `[model-judgment]`) so the user can see which part is data and which part is AI.

## 3. Who opens it, and what do they do with it?
**Target User:** F-1 STEM OPT job seekers.  
**First 60 Seconds (planned):** The student will open a terminal, run the CLI with a job posting URL (e.g., `reallocate score <job-url>`), and will get a markdown summary showing gate status, DOL H-1B filing record, SEC Form D funding evidence, duplicate status, and an `Apply` or `Skip` recommendation.

## 4. What does it prove about you?
It will show I can build **source-grounded AI workflows**:
1. **Prompt Contracts** that will constrain the model and stop hallucination.
2. Public datasets (DOL LCA disclosures, SEC Form D) used as deterministic gates instead of LLM memory. (The 2026-10-03 prototype already reads this file and tags each score with its source.)
3. Observable AI pipelines with audit logs, ADRs, and friction logs, plus an evaluation suite that will measure decision accuracy.

## 5. What is in, what is out, what comes first?
* **In Scope:**
  - Visa sponsorship verification using DOL H-1B disclosure data.
  - Role quality scoring and title matching for SWE/DevOps/QA tracks.
  - Lightweight duplicate suppression using hash keys (`company_normalized + title_normalized`).
  - Strict provenance tagging (`[record]`, `[model-judgment]`, `[rule-gate]`).
* **Out of Scope:**
  - Automated resume spamming or auto-apply bots (aggressively rejected to protect applicant reputation).
  - Heavy multi-user SaaS databases or web frontends (kept as a local CLI script).
* **What Comes First:**
  - The first piece I will make run is the sponsor lookup: matching company names against the H-1B filing records. The duplicate tracker will come next.

## 6. What could sink it?
**Company names that don't match the filing file.** A posting says "Toast", but the DOL/SEC file has 9 names containing TOAST, including `TOAST INC` (150 H-1B approvals), `TOAST HOLDINGS INC`, and `MOONTOAST INC` (no approvals). A wrong match gives a wrong verdict. The 2026-10-04 prototype run already shows the effect: `Isaac Super Fake Tech LLC` was not in the file (`[no-matched]`) and still came out `Apply`.
*What I will do:* I will confirm each company's legal name myself before it is scored, and when a name doesn't match, the tool will hold the role instead of scoring it.

## 7. Why this project?
* **Personal:** I'm an F-1 student. I face this sponsorship check myself on every application, and I used to trust AI answers about it blindly.
* **Shown, not claimed:** my friction logs and the source tags in the prototype's `role-scores.md` (2026-10-04) already show how I check AI work.
* **What I will learn:** to replace prompt-pasting with strict verification gates.

---

### Exists Today (as of 2026-10-10, can be shown)
* Prototype recipe `tisaac-swe-stem-opt` in *The Reallocation Engine* (committed 2026-10-03).
* It reads the DOL H-1B / SEC Form D CSV and tags each score with its source (`[record]`, `[model-judgment]`, `[no-matched]`).
* One real run on 3 test roles: `role-scores.md` (2026-10-04). Shown in the film (B01, B07), labelled REAL OUTPUT.

### Will Exist (planned)
* Single-command CLI that takes a job URL; URL extract and clean pipeline.
* Legal-name confirmation and HOLD for unmatched names.
* Quote-proof check before any disqualification.
* Local hash cache for duplicate postings.
* Evaluation suite for decision accuracy.

Everything shown in the film that is not REAL OUTPUT or REAL CSV ROWS is labelled CONSTRUCTED MOCK-UP on screen.
