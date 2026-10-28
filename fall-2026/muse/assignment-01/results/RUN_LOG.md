# Run log

- Timestamp (UTC): 2026-10-11T03:57:52.313660+00:00
- Command: `python3 run_experiment.py` from the assignment folder
- Python: standard library only (`math`, `random`, `json`, `collections`, `datetime`, `pathlib`)

## What ran

| File | Kind | Content |
|---|---|---|
| sampling_temps.json | ACTUAL RUN | E1: temperature sweep, logits [1,2,3], n=5000, seed 7 |
| sampling_wrong_peak.json | ACTUAL RUN | E2: confidently-wrong peak at temps 2.0/1.0/0.5/0.1 |
| sampling_repeatability.json | ACTUAL RUN | E3: same-seed identity + 5-seed spread vs theory |
| contract_dev.json | FIXTURE EVALUATION | Validator executed for real over 5 hand-written dev fixtures |
| contract_heldout.json | FIXTURE EVALUATION | Validator executed for real over 5 hand-written held-out fixtures |

No model was called and no API was contacted in any step. Fixture
provenance is recorded inside fixtures/*.json and repeated in the
contract_*.json result files.
