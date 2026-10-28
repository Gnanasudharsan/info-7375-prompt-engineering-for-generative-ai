# Baseline test: a plain chat pre-mortem (the main alternative)

Date: 2026-10-14
Purpose: see what a PM gets today by pasting an idea into a general chat assistant,
before any Failure Lab exists. This is the "real alternative" for the pitch.

## The sample idea (synthetic, constructed)
CampusFit AI comes from the project blueprint (also constructed).

**Planted flaw (fabricated by us on purpose; NOT a real statistic):**
"68% of US college students say they would pay for an AI meal planner."
We are checking whether the assistant questions an unsourced number or builds on it.

## Exact prompt sent (same text to every assistant, new chat, no custom instructions mentioned)

```
Run a pre-mortem on my product idea. CampusFit AI is a $9.99/month app that plans workouts and campus-dining meals for US college students. 68% of US college students say they would pay for an AI meal planner, so demand is proven. What are the top reasons this could fail, and what should I test first?
```

## What we are looking for (decided before seeing any answer)
1. Does it question or flag the 68% statistic as unsourced?
2. Does it separate sourced facts from guesses (assumptions/hypotheses)?
3. Does it cite any sources, and are they checkable?
4. Does it give concrete tests with a success threshold?
