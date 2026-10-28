# Source Check for Support AI — Project Brief

**Mayank Bhadrasen · INFO 7375 Final Project · solo project · Target role: AI automation engineer · Brief written 2026-10-14, revised 2026-10-22 for the resubmission**
**Stack:** n8n (workflow and routing) · Python (the checker and its tests) · Claude (claim extraction under a prompt contract)

**Status (2026-10-25):** still a pitch, with one piece built: the deterministic checker and its tests in [`slice/`](slice/README.md) (21 tests pass; Claude extraction, the n8n workflow and the Slack queue are not built). Past tense only for that slice; every other sentence about the tool uses "will".

## 1. What is it?
Source Check for Support AI will check a support chatbot's policy answer against the company's current policy documents before the answer reaches the customer, and hold it for a human when it can't find support.
When it is done, it will be a public GitHub repository containing:
- an importable n8n workflow
- a Python checker with offline tests
- a synthetic help center for a fictional company
- an evaluation log
- a README with a one-command demo

## 2. Why would anyone care?
It will stop a support bot from promising a refund, fee or eligibility rule that the company's current policy doesn't contain. This happens in practice. In *Moffatt v. Air Canada* (BC Civil Resolution Tribunal, February 2024), the airline's chatbot told a customer he could claim a bereavement fare after travelling, but the actual policy required the request before travel. The tribunal held Air Canada responsible for what its chatbot said.

Alternatives I looked at, on 2026-10-14:
- **Intercom Fin.** Its public page says it works from your policies, has "a full testing suite to run simulations, regression testing", and hands off to humans.
- **Zendesk AI agents.** They answer from the help-center articles a company connects as knowledge sources, and escalate to a human agent when they can't answer (Zendesk's own help center docs, read 2026-10-25; v1 had to rely on a third-party guide).
- **Manual review.** A support lead spot-checks bot transcripts, after the answers have already been sent.

What I did not find on those public pages: a check of each policy answer, at send time, against the current dated version of the policy. Source Check will hold the answer for approval when the source is missing, outdated or contradicted, and log which policy version each answer relied on. It will be vendor-neutral, sitting between any bot and the customer.

## 3. Who opens it, and what do they do in the first sixty seconds?
The reader is a hiring manager or engineer hiring an AI automation engineer. In the first sixty seconds they will:
1. Open the README and see three example decisions.
2. Run one command.
3. Watch an answer that relies on an outdated refund policy get **HELD**, with the reason and the policy line it contradicts.

The intended end user is a support team lead whose AI agent answers policy questions.

## 4. What does it prove about me?
That I can build an automation that knows when **not** to act. Course skills, and the planned evidence for each:
- **Prompt contracts:** Claude must return each claim as structured JSON mapped to a policy section, and the reply is validated before it is used.
- **Source grounding:** every claim is tied to a dated document.
- **Verification:** deterministic checks for numbers, dates and conditions. The model only extracts claims; it does not judge them.
- **Human approval gates:** a HOLD queue in Slack through n8n.
- **Evaluation:** a labelled synthetic test set of correct, outdated and invented answers, with the miss rate measured and reported.

A reviewer could fairly conclude that I design gates and measure them. They could not conclude that it is production-ready, and I will not report any accuracy figure until it has been measured.

## 5. What is in, what is out, what comes first?
- **In:** policy answers (refunds, fees, eligibility) for one fictional company's synthetic help center, in English.
- **Out:** it will **not** write answers or replace the support bot. It only checks answers that another bot drafted.
- **First (built 2026-10-22):** the Python checker plus the Air Canada-shaped test. The answer says "claim after travel", the policy says "before travel", and the result is HOLD with the cited policy line. Two more condition flips from the TA's feedback ("within 90 days of purchase" vs "90 days after"; "within 24 hours of booking" vs "24 hours before departure") also return HOLD, and a matching answer returns PASS. `python3 -m pytest` in `slice/` passes 21 of 21 (2026-10-25). Two gaps I found in review were then closed: a claim with extra fields now breaks the contract, and a policy version dated in the future is ignored until it takes effect. Three deliberate breaks (ignore condition words, ignore dates, allow extra fields) make 6, 6 and 2 tests fail ([evidence](slice/evidence/)).

## 6. What could sink it?
**Missed conditions.** The most dangerous error is a dropped timing or condition word ("after" instead of "before", "within 90 days"), which is exactly the shape of the Air Canada error. If Claude's claim extraction loses the condition, the checker could PASS a wrong answer.
What I will do about it:
- run deterministic checks on numbers, dates and condition words
- default to HOLD whenever extraction is uncertain
- seed the evaluation set with condition-flip cases
- report the miss rate honestly

A second risk is too many HOLDs, so a support team learns to ignore them. I will measure the hold rate as well.

## 7. Why this project?
It is a mix of showing off and learning.
- **Skills I already have, with evidence:**
  - n8n workflows with Claude: my public repos *AI-Marketing-Ad-Review* (Claude reviews ad copy, with a rule-based fallback, routed to HubSpot and Slack) and *Madison-Project* (n8n + Claude Haiku routing to a CRM, INFO7375 Assignment 4)
  - n8n data pipelines: *Applications-Made-Easy* and *One-Pipe*
  - Python: my Week 1 film's evidence code in the course repo
- **New to me:**
  - building and labelling an evaluation set, and measuring misses
  - validating a prompt contract
  - designing a hold-for-approval gate that records the policy version behind every decision

I picked it because Week 1 taught me that a fluent, confident output is not a checked one, and the Air Canada case shows what that costs a real company.

---
**Exists today (2026-10-25):** this brief · the research notes and sources behind sections 2 and 6 · this pitch film (v3.1) · the deterministic checker, 9 synthetic cases and 21 passing tests in `slice/`, with saved output · my earlier public repos listed in section 7 (evidence of skills, not of this project).

**Will exist:** Claude claim extraction under the JSON contract · the n8n workflow · the Slack hold queue · the full synthetic help center · the labelled evaluation set, with the miss rate and hold rate measured · the final README.
