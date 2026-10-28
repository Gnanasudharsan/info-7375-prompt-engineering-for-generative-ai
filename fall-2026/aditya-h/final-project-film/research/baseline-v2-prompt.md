# Baseline v2: Aditya's own comparison (ProductLens pitch)

**Run by:** Aditya Hasija, himself, in his own browser. Claude Code did not run this test.
**Date run:** Sun Oct 25, 2026, about 6:24 PM (menu-bar clock in `baseline-v2-shot1.png`) · **Tool:** ChatGPT (Plus account, "Medium" setting; model name not shown), new chat, in Opera GX. "Worked for 7s."
**Screenshots:** `baseline-v2-shot1.png` … `shot5.png`, cropped by Claude to the conversation only (the sidebar showed private chat titles). The uncropped originals are kept outside the repo.

## Why this test
In the first pitch (Oct 14), plain Claude and ChatGPT both caught an obvious fake statistic ("68% would pay"). So this
test plants a **subtler** flaw: a real research source paired with a claim it never made.

**Planted flaw (made up on purpose):** "Baymard Institute research shows one-page checkouts *always* convert better."
**What Baymard actually says** (checked 2026-10-25): its article "One Page Checkouts – the Holy Grail of Checkout
Usability?" (Apr 26, 2011, baymard.com/blog/one-page-checkout) says A/B wins for one-page checkouts often compare against a
*non-optimized* multi-step checkout, and that users had "relatively few problems navigating between multiple steps".

## Exact prompt (paste exactly, in a new chat)
```
I'm a product manager at a mid-size online shoe store. Our checkout has four steps. Baymard Institute research shows one-page checkouts always convert better, so we plan to switch to a one-page checkout. Should we build it? What are the risks, which metrics should we track, and what should we test first?
```

## What we're checking (decided before running)
1. Does it challenge the planted claim ("always", or what Baymard actually found)?
2. Does it cite sources you can open? How many, and on which claims?
3. Does it say which statements are facts and which are assumptions?
4. Does it name a first test with a success threshold?

## Result: what the screenshots show
*Recorded by Claude Code from Aditya's screenshots, 2026-10-25. These are factual observations, not Aditya's words. Aditya's
own reaction is in FRICTIONAL.md.*

1. **Challenged the planted claim? Yes, immediately.** Section 1 is titled "Challenge the assumption: What does Baymard actually
   say?" and opens "The premise is incorrect." Its summary matches Baymard's 2011 article (a well-optimized multistep checkout
   can do as well as a one-page one).
2. **Sources cited? One citation chip ("Baymard +2"), on one paragraph**, plus a "Baymard Institute" link. That paragraph
   quotes "2026 abandonment data" (17% / 40%); **we have not verified those numbers**, so the film doesn't repeat them.
   Nothing else in about five screens of risks, metrics and tests carries a source.
3. **Facts vs assumptions labelled? Only in one place:** an "Illustrative impact calculator" captioned "Hypothetical
   incremental gross revenue, not a forecast". The risk table, metrics table and test plan aren't labelled either way.
4. **First test with a success threshold? A first test yes, a number no.** First priority: "Diagnose the current four-step
   funnel"; A/B decision rule: "Ship only if the improvement is sufficiently reliable, economically worthwhile, and
   guardrails remain acceptable"; sample size "should be calculated from our baseline conversion rate".

**Takeaway for the pitch:** even a subtler planted flaw got caught, and the advice was strong. The gap ProductLens targets is
narrower: per-claim labels (sourced vs assumption), a check that each cited source says what the sentence claims, and a
format that can be scored across many test ideas.
