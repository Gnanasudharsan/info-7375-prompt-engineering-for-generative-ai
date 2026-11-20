# SCORE.md — what moves the score (Chapter 9)
Evidence: evidence/filter_numbers.txt (every number, printed from jobwatch/filter.py), evidence/score_offline_*.txt, evidence/score_claude_compare_*.txt,
raw Claude results in evidence/score_claude/{baseline,baseline_repeat,revision}/, predictions in heldout/PREDICTIONS.md (written before running).

## 1. Where every number came from
| number / object | value | origin |
|---|---|---|
| B1 title role phrase | 3 points, once | hand-set (FILTER.md v1.0, from the persona) |
| B2 topic words | +1 each, cap 5 | hand-set |
| B3 shipped skills | +1 each, cap 4 | hand-set |
| keep threshold | 5 | hand-set |
| A4 years rule | N >= 3 | hand-set, from the persona's new-grad constraint |
| close-call band | score 4-6 | hand-set |
| C2 negation window | 120 characters | hand-set; measured and rejected (FILTER.md changelog 1.1) |
| audit sample sizes | 30 random rejects, 15 close calls, 10 kept | 30 is the assignment's minimum (inherited); the others hand-set |
| Claude judge prompts | prompts/judge_baseline.md, judge_revision.md | inherited from JS1 |
| Claude model and isolation (fresh `claude -p`, empty temp dir, no tools) | JS1 claude_cli backend | inherited from JS1 |
| **fitted on labels** | — | **none.** No number was fitted; v1.1's changes were chosen by measuring on my dev labels, not by fitting. |

## 2. One change to one object at a time, on held-out labels
Held-out set: 28 postings never labeled before (heldout/sample.json), labeled blind by me (heldout/hand_verdicts.csv): **23 NOT_RELEVANT, 5 CANNOT_TELL, 0 RELEVANT.**
With no RELEVANT posting, these experiments can measure false keeps (postings I call NOT_RELEVANT that pass), not missed good jobs.

| object | change | held-out result | baseline |
|---|---|---|---|
| setting | keep threshold 5 -> 6 | 0 decisions changed | v1.0, threshold 5 |
| setting | keep threshold 5 -> 4 | 0 decisions changed | v1.0, threshold 5 |
| filter file | v1.0 -> v1.1 (C4) | 0 decisions changed | v1.0 |
| prompt | Claude judge baseline -> revision | 2 of 23 verdicts changed: #2 NOT_RELEVANT -> RELEVANT (a new false keep: I said NOT_RELEVANT), #7 NOT_RELEVANT -> RELEVANT (I said CANNOT_TELL) | baseline prompt |
| control | baseline prompt again, identical | 1 of 23 verdicts changed: #7 NOT_RELEVANT -> RELEVANT | baseline prompt |

What the numbers allow me to say:
- **Threshold and filter-file changes could not be measured** on this held-out set: none of its 28 postings scores 4-6, because my audit had already used all 15 close calls in the corpus as development data. This is a limit of my held-out design, not evidence that the threshold does not matter.
- **The prompt change is the size of the noise.** The control flipped 1 of 23 with no change at all; #7 flipped in both. Only #2 goes beyond the control, and it is a new false keep. So on 23 held-out postings, the revision did not make the judge agree with me more; I cannot claim it changed behavior beyond run-to-run variation.
- **5 of 28 postings (all Lever and Ashby) got no Claude verdict in any run** (judgment_unavailable): the JS1 judge's output contract (numeric id, Greenhouse field names) only fits Greenhouse postings. It failed closed: no verdict was invented.
- My prediction 3 (the revision would call fewer of my NOT_RELEVANT postings RELEVANT) was **wrong**. Prediction 4 (identical runs would differ a little) was **right**.

## 3. What persistence is not proof of
Every Claude call here is a fresh `claude -p` process in an empty temporary folder, with no tools and no memory between calls. The control run shows two identical
calls disagreeing on posting #7. If a behavior changes across sessions, that is consistent with sampling, a different prompt, different context, or a changed
model version. **It is not evidence that anything was trained:** I trained nothing, no label was ever sent to a model as training data, and the filter changes
in v1.1 are edits to a file I can diff. A behavior that "sticks" across sessions would need a mechanism I can point to (a file, a setting, a memory feature),
not an assumption that the model learned.

## Not tested
- The context given to Claude (persona included vs. not) and the tool list were not varied; only the prompt was.
- Recall: with 0 RELEVANT in the held-out set, missed good postings cannot be measured.
- More than two repeats of the control; 1 flip in 23 is one observation of the noise, not its rate.
