# Source Check, first slice: the deterministic checker

The smallest piece of Source Check that runs, built after the v1 pitch feedback (2026-10-22). The TA's next step was "write the Air Canada-shaped fixture and the pytest that must return HOLD, then add two more condition-flip cases". This folder is that step, plus a matching case that must PASS so the checker can't pass its tests by holding everything.

**What it is:** `source_check/checker.py` compares claims with the current, dated policy, field by field (topic, relation, amount, unit, anchor), and returns PASS or HOLD with reasons and the policy line it used. It never asks a model whether an answer is right.

**What it is not (yet):** there is no Claude extraction. The claims in `data/cases.json` are written by hand in the claim contract. There is no n8n workflow and no Slack queue either. The airline and its policies are fictional and synthetic.

## Run it (Python 3.9+, pytest)

```bash
cd slice
python3 -m pytest -v                         # 21 tests
python3 -m source_check.demo                 # the Air Canada-shaped case -> HOLD
python3 -m source_check.demo matching_refund # -> PASS, logs policy RFD-2026-01
```

## The cases (`data/cases.json`)

| Case | The answer says | The current policy says | Expected |
|---|---|---|---|
| `air_canada_shape` | claim the bereavement fare **after** your trip | request it **before** travel | HOLD |
| `within_vs_after` | refund up to 90 days **after your flight** | **within** 90 days **of purchase** | HOLD |
| `booking_vs_departure` | free cancellation up to 24 hours **before departure** | free **within** 24 hours **of booking** | HOLD |
| `matching_refund` | refund within 90 days of purchase | same (RFD-2026-01) | PASS |
| `outdated_refund` | refund within 30 days of purchase | 90 days now; 30 was RFD-2024-06 | HOLD (outdated) |
| `no_source` | pets fly free | no policy covers it | HOLD |
| `extra_field` | refund within 90 days, plus "we'll waive the fee" (an extra field) | the contract has exactly 5 fields | HOLD (breaks the contract) |
| `future_policy` | refund within 60 days of purchase | 60 days starts only on 2027-03-01 (RFD-2027-03); 90 days is in effect | HOLD (not in effect yet) |
| `broken_contract` | "refunds are easy" (claim missing fields) | n/a | HOLD |

## Evidence (`evidence/`, 2026-10-25)

- `pytest_2026-10-25.txt`: **21 passed** (the tests pin today's date, so they give the same answer any day).
- `demo_2026-10-25.txt`: six demo runs, output as printed.
- `mutation_2026-10-25.txt`: three deliberate breaks. Ignore the condition words: **6 failed**. Ignore effective dates: **6 failed**. Allow extra fields: **2 failed**. So the tests can tell a working checker from one that drops condition words (the main risk in the pitch), trusts a policy before its date, or lets extra claims through.
- `*_2026-10-22.txt`: the first slice (7 cases, 15 tests), kept for the record.

## Who did what

- **The TA** named the first three cases (Air Canada shape, "within 90 days" vs "90 days after", one more condition flip).
- **Mayank** asked for the changes and set the rule that anything unverifiable is a HOLD (PROJECT-BRIEF.md, §6).
- **Claude Code** (2026-10-22) proposed the other four cases, wrote the checker, fixtures and tests, ran them, and ran the deliberate break.
- **Mayank's review of the code (2026-10-25):** walked through it function by function and chose two gaps to fix: a claim with extra fields was not rejected, and a policy dated in the future was treated as current. Claude implemented both fixes with tests.

See `../FRICTIONAL.md` and `../SOURCES.md`.
