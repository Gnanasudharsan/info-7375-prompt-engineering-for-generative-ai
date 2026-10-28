# PROJECT-BRIEF — OPT Countdown

Saloni Mathure · INFO 7375 Fall 2026 · Final Project Pitch · written 2026-10-13

## 1. What is it?

OPT Countdown will be a command-line tool that takes an international student's OPT dates and a list of job postings, and sorts each posting into **apply**, **network first**, **skip**, or **blocked**, using the employer's public H-1B record, whether the posting is still live, and whether the employer can hire before the student's 90-day unemployment limit runs out.

**The artifact when done:** a public GitHub repository with a Node 20 command-line tool, its tests, a hand-labelled evaluation set with an evaluation log, and a sample report for a fictional student.

## 2. Why would anyone care?

It saves a student on OPT the per-posting research they now do by hand, and it is honest about what it cannot know. It does not guess when a fact is missing.

The alternatives I actually used or looked at while building the prototype (2026-10-03):

- **The manual process.** Look the employer up in H-1B data, open the posting to see if it is live, guess the hiring speed, and count days. I estimated about 20 minutes a posting. That figure is an assumption. I did not time it.
- **The Reallocation Engine's own liveness checker** (`npm run ats:liveness`). It called a fake Klaviyo job link **active**, because the dead link redirects to a live careers page. Greenhouse's job API returned **404** for the same link. My tool uses the API status, and the API wins when the two disagree.
- **The raw H-1B data on its own** (the engine's 80 Days to Stay CSV). Read naively, a company with no row looks like a company that won't sponsor. HubSpot has no row, and DraftKings has blank H-1B fields. My tool marks both **blocked** for a person to check. It does not skip them.

Neither alternative computes the **timeline**. A strong sponsor with a 60-day hiring process is no use to someone with 53 days left. In the worked run, Klaviyo and Toast, both strong sponsors, were skipped for exactly that reason.

## 3. Who opens it, and what do they do?

- **End user:** an international student on OPT. In the first sixty seconds they run one command and read a one-page report: their clock, then a decision and the evidence for each posting.
- **Reviewer:** a hiring manager or engineer for the roles I am targeting, which are new-grad software engineer and data analyst. In the first sixty seconds they read the README, run `node --test`, and open the evaluation log.

## 4. What does it prove about me?

- **Verification:** every number in the report carries a label saying where it came from: a record, the user's own input, or a model guess.
- **Evaluation:** I will hand-label a set of postings and measure how often each check (liveness, sponsorship join) is wrong.
- **Source grounding:** no posting gets a decision without a record behind it. A missing record means blocked.

What a reviewer could fairly conclude: I test my own tools and report where they fail. The evidence will be the test suite, the evaluation log, and the failure write-up. It would **not** prove that the tool helps anyone get hired. I will not claim that.

## 5. What is in, what is out, what comes first?

- **In:** sponsorship record, liveness, the timeline gate, a labelled report, tests, and an evaluation log.
- **Out (deliberately):** immigration advice. Cap-gap, STEM extension, and whether part-time work stops the clock stay with the school's DSO. The tool will say so in every report.
- **First piece:** move the prototype into its own repository so that a stranger can clone it, run `node --test`, and see all tests pass and the sample report written. **How you'd know it ran:** the test output, plus a sample report file generated in a fresh clone.

## 6. What could sink it?

The hiring-lag numbers are my own guesses. No dataset I have measures time-to-hire, and the lag decides many answers. The only "apply" in the worked run (Formlabs, 0.317) cleared the 0.3 bar by 0.017. **What I will do:** the report will show which decisions flip if the lag guess moves by 15 days either way, so that a fragile answer looks fragile.

## 7. Why this project?

It's a mix, and more learning than showing off.

- **Skills I already have:** JavaScript and Node. Evidence: CodeBuddies, my Node/Express team project for INFO 6150 (Fall 2024), at `github.com/salonimathure20/codebuddies-ai`.
- **Skills that are new to me:** building a labelled evaluation set and measuring a tool's own error rate, and writing reports where every value carries its source. The prototype was built on 2026-10-03 in one session where Claude Code did most of the hands-on work and I directed it. So it is evidence of the design, not of my solo coding.
- **What I don't know yet:** how many labelled postings the evaluation needs. I will start with 30 and check how much the error rate moves as I add more.

---

## Exists today (I can show it)

- The opt-countdown recipe and card in the Reallocation Engine, on branch `contrib/2026fa-salonimathure20-opt-countdown` (PR nikbearbrown/the-reallocation-engine#48, commit `81d0161`).
- A Node prototype with 12 offline tests. **Re-run 2026-10-13: 12/12 pass.**
- A worked run on 8 postings (6 real public Boston-area postings observed 2026-10-03, 1 deliberately fake job ID, and 2 title-only) for a **fictional** student with 53 days of runway. Result: Apply 1 · Consider 2 · Skip 3 · Blocked 2. Re-run 2026-10-13: same output, with only the timestamps changed.
- A documented defect: the engine's liveness checker called a dead job ID "active".

## Will exist (proposed, not built)

- A standalone public repository for OPT Countdown.
- A hand-labelled evaluation set (starting at 30 postings) and an evaluation log with error rates.
- A lag sensitivity check that flags decisions that flip at ±15 days.
- A failure write-up: where the tool, and Claude's output, was wrong and how it was caught.
