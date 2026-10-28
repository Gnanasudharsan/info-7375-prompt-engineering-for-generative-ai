# Alternatives looked at (2026-10-14)

## 1. Plain chat assistant: Claude, no special setup
- **How:** the prompt in `baseline-prompt.md`, sent 3 times through the Claude Code CLI in print mode
  (`claude -p --system-prompt "You are a helpful assistant." --tools ""`), model `claude-opus-5-5`.
  This is close to, but not identical to, the claude.ai chat app.
- **Raw outputs:** `baseline-claude-run1.md`, `-run2.md`, `-run3.md` (cost, timing and word counts in `baseline-claude-metrics.json`).
- **What happened (observed, 3 of 3 runs):**
  - It **did** catch the planted fake statistic ("68% would pay") every time, and said to treat it as a hypothesis.
    So "a plain chat misses fake numbers" is **not** a claim the pitch can make.
  - It cited **zero sources** (0 URLs in all 3 runs). It still stated many facts as true, with no label:
    survey willingness-to-pay is "consistently inflated", paid conversion "typically happens at low single-digit rates",
    fitness apps "already churn heavily", and kill thresholds like "under 2–3% pay".
    A reader can't tell which of these are established facts and which are the model's guesses.
  - The structure changed from run to run (851–1,118 words, different risk lists and ordering). There's no fixed schema,
    so you can't compare two ideas or two runs side by side.
  - There's no record you can check of what was examined, and no measure of how often it gets things right.
  - Reported cost: $0.05–$0.07 per run, 32–39 s. (These are as reported by the CLI; Aditya's plan may not bill this way.)
- **Takeaway for the pitch:** the gap isn't intelligence. It's per-claim evidence labels, a fixed and repeatable
  report format, and a test set that measures it.

## 2. Atlassian Team Playbook "Pre-mortem" play (a manual process)
- **Source:** https://www.atlassian.com/team-playbook/plays/pre-mortem (read 2026-10-14)
- **What it is:** a facilitated workshop: 3–11 people, about 10 min prep + 60 min run time, sticky notes or Trello/Confluence,
  brainstorm, dot-vote the top threats, assign owners to action items.
- **What it does well:** gathers team knowledge; gives each risk an owner.
- **What it doesn't do:** it's aimed at *project delivery* risk (deadlines, resources), not whether a product will be
  adopted. It needs a team and a meeting. Nothing checks whether a claim on a sticky note is supported by evidence.
- **Takeaway:** the Failure Lab is for the one PM with a raw idea *before* there is a team to run this play,
  and it adds evidence labels the workshop does not have.

## 3. Plain chat assistant: logged-out ChatGPT (1 run, 2026-10-15 00:24 UTC)
- Full notes: `baseline-chatgpt.md`, screenshot `baseline-chatgpt-screenshot.jpg`. The model wasn't shown.
- It also caught the planted 68% stat. It searched the web: citation chips on 2 paragraphs ("FitSpace +2" and "Federal Trade Commission +1", so more than 2 sources sat behind them) in about 1,500 words.
  It labeled its thresholds and churn math as "not benchmarks" but left most risk claims unlabeled.
- **Takeaway:** the stronger alternative. The pitch must say so and claim only the narrower difference: every claim labeled,
  every citation checked by code, and a fixed format that can be scored.

## 4. DimeADozen.ai (a paid AI validation service), homepage and example-reports page only, 2026-10-14
- Named in the ChatGPT-drafted storyboard; checked here before citing it.
- **What its own homepage says** (these are its claims, not verified by us): a free 2-minute idea score, a $9 Starter report,
  and a $129 "Entrepreneur" report of "typically 100+ pages with 500+ URL citations", source-linked. It says it validates
  "should you build this", not lender business plans.
- The example-reports page lists write-ups of past companies (Juicero, Quibi, WeWork, …) read across market,
  competition, timing and execution.
- **Not done:** I didn't run or buy a report (it needs an email, and payment for the full one). So I **can't** say how good its
  citations are or whether it labels guesses. The film must not claim it does or doesn't.
- **What the Failure Lab offers that this doesn't advertise:** a short, failure-first report built to be read in about 5 minutes, and an open
  test set with published scores, including where it fails. It also runs on your own source pack, for free. This
  is a difference in openness and length, not a claim of better quality.

## 5. ValidatorAI (free AI idea validator), homepage only, 2026-10-25
- validatorai.com describes itself as a tool to "validate startup, product and small business ideas", shows a live feed of
  "Latest idea scores" (e.g. "E-commerce 78"), and promises an answer to "Is my business idea good?" in under 60 seconds.
- Not run with a real idea (it asks for idea text; the homepage was enough to describe its focus).
- **Takeaway for ProductLens:** ValidatorAI and DimeADozen score **whole ideas**. ProductLens aims at **one feature decision
  in an existing product**, with per-claim labels and quote checks. That's a difference in focus, not a quality claim.

## 6. ChatGPT again, run by Aditya himself (2026-10-25), subtler planted flaw
See `baseline-v2-prompt.md`: it caught the misattributed Baymard claim immediately; one cited paragraph; almost no
fact/guess labels; no numeric success threshold.

## Not yet looked at (do not cite in the film unless checked)
- Version Lens (an AI co-pilot for PMs, surfaced by a 2026-10-25 web search). Not opened, so not cited.
