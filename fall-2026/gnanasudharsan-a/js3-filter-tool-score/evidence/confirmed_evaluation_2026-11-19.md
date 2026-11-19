## Filter comparisons on 80 hand-audited development postings

| Variant | Corpus keep / reject / abstain | Decision flips | A3 / A6 fired | Labeled keep (R / N / U) | Labeled reject (R / N / U) | Labeled abstain (R / N / U) | Exact matches corrected / blind |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1.0 | 17 / 882 / 0 | 0 | 0 / 21 | 1 / 3 / 10 | 0 / 63 / 3 | 0 / 0 / 0 | 64/80 / 62/80 |
| C1 | 17 / 882 / 0 | 0 | 2 / 21 | 1 / 3 / 10 | 0 / 63 / 3 | 0 / 0 / 0 | 64/80 / 62/80 |
| C2 | 17 / 882 / 0 | 0 | 0 / 17 | 1 / 3 / 10 | 0 / 63 / 3 | 0 / 0 / 0 | 64/80 / 62/80 |
| C3′ (revised C3) | 0 / 882 / 17 | 17 | 0 / 21 | 0 / 0 / 0 | 0 / 63 / 3 | 1 / 3 / 10 | 73/80 / 71/80 |
| C4 | 15 / 884 / 0 | 2 | 0 / 21 | 1 / 2 / 9 | 0 / 64 / 4 | 0 / 0 / 0 | 65/80 / 63/80 |

## Shortlist label verification

31/75 confirmed labels in the workspace CSV. 44 outstanding.
Confirmed counts: CONTRADICTED 0, INSUFFICIENT 9, SUPPORTED 22.
Confirmed changes from original proposals: 2/31.
Source of truth: my_label in claim_labels.csv, with no suggestion-file fallback.
