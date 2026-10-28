# Baseline: logged-out ChatGPT (1 run)

- Date: 2026-10-15 00:20–00:24 UTC (2026-10-14 evening, Boston)
- How: chatgpt.com, logged out, in the Claude desktop app's built-in browser. New chat. Exact prompt from `baseline-prompt.md`.
- Model: not shown to logged-out users (unknown).
- Screenshot of the top of the reply: `baseline-chatgpt-screenshot.jpg`.
- Citation chips showed source names only; the URLs were not exposed in the page.

## What it did (against the checks decided in advance)
1. **Flagged the 68% stat?** Yes. Early on it gave "one important correction to your premise", calling it "a hypothesis
   to validate, not proof of demand", and asked for the survey's source, sample and wording.
2. **Separated facts from guesses?** Partly. It labeled its thresholds "not universal benchmarks or guarantees", called its
   experiments "proposed experiments, not industry benchmarks", and labeled its churn table "simplified expected values,
   not revenue forecasts". Most risk statements, though, are stated with no label.
3. **Cited sources?** Citation chips on two paragraphs (each chip bundles more than one source, per its "+N"): "FitSpace +2" on the competitor paragraph, and "Federal Trade Commission +1" on
   the health-privacy paragraph. Every other claim had no source. A vendor's page backing "competitors exist" is weak evidence,
   and nothing checks whether a cited page actually says what the sentence claims.
4. **Concrete tests with success thresholds?** Yes: four ordered experiments, plus a pass/fail table (e.g. "Paid conversion 10%+,
   warning below 5%"). The thresholds are its own suggestions, with no stated basis.

## Structure
Verdict → failure story → 6 failure modes (each with signal and test) → competition → 4 experiments → pass/fail table →
less obvious risks → churn math → recommendation. About 1,500 words.

## Takeaway
ChatGPT is better than plain Claude on this one point: it searched the web and attached some labels and caveats.
Even so, labels are applied to *some* claims and not others, citations aren't checked against what they cite, and the
format is its own. This narrows the Failure Lab's claimed difference to: **every claim gets a label, every citation is checked
by code against a fixed source pack, and the format is fixed so runs can be scored.**
