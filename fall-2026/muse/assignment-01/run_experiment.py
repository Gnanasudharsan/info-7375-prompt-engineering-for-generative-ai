"""Run the controlled prompt experiment and preserve raw results.

Part A -- sampling mechanics (ACTUAL RUNS): real Python execution with fixed
seeds. Every number in results/sampling_*.json was computed by this script.

Part B -- prompt-contract validation (FIXTURE EVALUATION): the validator
from contracts.py is executed for real, but the *responses* it checks are
hand-written fixtures (fixtures/*.json), NOT model outputs. No model was
called, no API was contacted. Fixture files carry their own provenance.

Usage: python3 run_experiment.py
Writes: results/sampling_temps.json, results/sampling_wrong_peak.json,
        results/sampling_repeatability.json, results/contract_dev.json,
        results/contract_heldout.json, results/RUN_LOG.md
"""
import datetime
import json
from pathlib import Path

import sampling
import contracts

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)
RUN_STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()


def dump(name, payload):
    path = RESULTS / name
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path.name


# ---------------- Part A: sampling mechanics (actual runs) ----------------

# E1: temperature sweep on the lesson's three-token model.
e1 = sampling.temperature_sweep([1, 2, 3], [0.5, 1.0, 2.0],
                                count=5000, seed=7)
dump("sampling_temps.json", {
    "experiment": "E1",
    "kind": "ACTUAL RUN",
    "logits": [1, 2, 3],
    "count": 5000,
    "seed": 7,
    "records": e1,
})

# E2: confidently-wrong peak. Index 0 is stipulated WRONG with the top logit.
# Prediction (recorded before running): cooling concentrates mass on the
# wrong index; temperature does not repair the answer.
e2_probs = {t: sampling.probabilities([4, 1, 1], temperature=t)
            for t in (2.0, 1.0, 0.5, 0.1)}
e2_counts = {t: sampling.sample([4, 1, 1], count=5000, seed=7, temperature=t)
             for t in (2.0, 1.0, 0.5, 0.1)}
dump("sampling_wrong_peak.json", {
    "experiment": "E2",
    "kind": "ACTUAL RUN",
    "note": "index 0 is stipulated WRONG; it holds the largest logit",
    "prediction": "lower temperature increases the wrong answer's share",
    "probabilities": {str(t): p for t, p in e2_probs.items()},
    "counts": {str(t): c for t, c in e2_counts.items()},
})

# E3: repeatability. Same seed -> identical counts; different seeds differ
# but stay near theory.
theory = sampling.probabilities([1, 2, 3], temperature=0.5)
same_a = sampling.sample([1, 2, 3], count=5000, seed=7, temperature=0.5)
same_b = sampling.sample([1, 2, 3], count=5000, seed=7, temperature=0.5)
seed_records = []
for s in (7, 8, 9, 10, 11):
    c = sampling.sample([1, 2, 3], count=5000, seed=s, temperature=0.5)
    seed_records.append({"seed": s, "counts": c,
                         "total_variation": sampling.total_variation(c, theory)})
dump("sampling_repeatability.json", {
    "experiment": "E3",
    "kind": "ACTUAL RUN",
    "same_seed_identical": same_a == same_b,
    "theory": theory,
    "seeds": seed_records,
})

# ---------------- Part B: contract validation (fixtures) ----------------

evidence = json.loads((ROOT / "evidence" / "evidence.json").read_text())
source_ids = set(evidence)


def run_split(name):
    data = json.loads((ROOT / "fixtures" / name).read_text())
    assert data["split"] in ("dev", "held-out")
    responses = [c["response_text"] for c in data["cases"]]
    rate, failures = contracts.pass_rate(responses, source_ids)
    per_case = []
    for case in data["cases"]:
        ok, reason = contracts.validate(case["response_text"], source_ids)
        per_case.append({
            "id": case["id"],
            "kind": case["kind"],
            "expected_ok": case["expects"]["ok"],
            "observed_ok": ok,
            "observed_reason": reason,
            "matches_expectation": ok == case["expects"]["ok"],
            "tests": case["tests"],
        })
    return {
        "experiment": "B-" + data["split"],
        "kind": "FIXTURE EVALUATION",
        "warning": ("Responses are hand-written fixtures, NOT Claude outputs. "
                    "The validator ran for real; the responses did not come "
                    "from any model."),
        "n_cases": len(responses),
        "format_pass_rate": rate,
        "failures": failures,
        "per_case": per_case,
        "all_expectations_met": all(c["matches_expectation"] for c in per_case),
    }


dev_result = run_split("dev_cases.json")
heldout_result = run_split("heldout_cases.json")
dump("contract_dev.json", dev_result)
dump("contract_heldout.json", heldout_result)

# ---------------- Run log ----------------
log = """# Run log

- Timestamp (UTC): %s
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
""" % RUN_STAMP
(RESULTS / "RUN_LOG.md").write_text(log)

print("E1 temps:", [(r["temperature"], [round(p, 4) for p in r["probabilities"]],
                     round(r["total_variation"], 4)) for r in e1])
print("E2 wrong-peak P(index 0):",
      {t: round(p[0], 4) for t, p in e2_probs.items()})
print("E3 same-seed identical:", same_a == same_b)
print("E3 seed TVs:", [round(r["total_variation"], 4) for r in seed_records])
print("B-dev pass rate: %.2f  all expectations met: %s"
      % (dev_result["format_pass_rate"], dev_result["all_expectations_met"]))
print("B-heldout pass rate: %.2f  all expectations met: %s"
      % (heldout_result["format_pass_rate"], heldout_result["all_expectations_met"]))
print("Wrote 6 files to results/")
