# What moves the score

The current filter is v1.1, with C1 and C4 enabled together. The unchanged v1.0 configuration is the default in `jobwatch/filter.py`. The archived decision files for v1.0, each independent change, and C1+C4 were replayed from the same three successful board bodies. The deliberate 404 board is excluded. See [replay checksums](evidence/filter_replay_2026-11-19.txt) and [the complete confusion counts](evidence/confirmed_evaluation_2026-11-19.md).

## Where the numbers came from

| Number or object | Origin |
|---|---|
| B1 +3 once, B2 +1 per topic capped at 5, B3 +1 per skill capped at 4, keep threshold 5 | Hand-set in v1.0 from the fictional persona and documented in FILTER.md. No fitting. Maximum score is 12. |
| Close-call scores 4–6 and A4 minimum 3+ years | Hand-set in v1.0. The close-call range samples either side of the threshold. A4 represents the persona's new-grad constraint. |
| C2 window of 120 cleaned characters on either side | Hand-set experimental setting. A nearby negation can refer to an unrelated clause. |
| C4 minimum B1 of 1 | Hand-set experimental gate. B1 is either 0 or 3, so this requires a matching title phrase without changing its weight. |
| Claude baseline and revised prompts | Inherited from JS2. These belong to the older judge path. The archived JS3 filter and MCP score lookup use deterministic rules. |
| MCP demo prompt | Written for a single fixed lookup. No comparison, repeated-session experiment, or training was performed. |

A repeatable decision can come from the same inputs, source snapshot, and code across sessions. Persistent behavior alone supplies no evidence of a weight update or training.

## Recommendations

- **Accept C1 as a rule-coverage fix.** Two additional A3 matches used actual citizenship language. The final decision stayed the same in both cases. There is no observed decision-level improvement.
- **Reject C2.** A6 fired on 17 postings instead of 21, with zero decision changes. The measured AWS GTM Partnership Lead example lost its explicit active-clearance match due to nearby unrelated negation. The motivating Product Manager false friend still fired.
- **Reject C3′ as a hard keep gate.** Here C3′ means the revised C3 already documented in FILTER.md, which accepts explicit level phrases as signals and ignores the generic deferral. There was no separately named C3′ rule in the project. It abstained on all 17 baseline keeps, including the only hand-confirmed relevant keep on the corrected labels. Exact agreement rose from 64/80 to 73/80 because 10 labeled uncertain keeps moved to abstention while one relevant keep was lost. Keep level uncertainty visible in the evidence.
- **Accept C4 provisionally.** It removed two baseline keeps, one human-labeled not relevant and one human-labeled uncertain. It retained the sole relevant keep in the corrected development set. The possible loss of relevant jobs with unconventional titles still needs held-out testing.

All 80 posting judgments were previously used to develop or assess these switches. Both the original blind results and the student's post-unblind corrections are reported. The shortlist labels judge individual claims, so they cannot substitute for posting relevance labels. A fresh, independently hand-labeled held-out set is still needed to meet that assignment requirement. Prefer a separate snapshot with enough borderline and potentially relevant postings to test changes that act on keeps.

## Held-out procedure for the student

1. Freeze v1.0 and the four switch definitions before opening any new verdicts.
2. Collect a fresh snapshot using the board allowlist. Exclude repeats from the current corpus by board and posting ID. Save the raw snapshots and note missing boards.
3. Select a blind sample before labeling. Include plausible keeps and threshold cases as well as random rejects, since a reject-heavy sample can make an always-rejecting policy look accurate. Save the seed and cohort membership separately from the label sheet.
4. Have the student apply `audit/LABELING_RULE.md` to the archived descriptions without viewing model or filter outputs. Freeze the student verdicts before unblinding.
5. Run the baseline and each switch alone on the same held-out postings. Report the confusion counts by cohort, including uncertain decisions and relevant postings lost. Retain the first held-out results if those results later drive another filter revision.
