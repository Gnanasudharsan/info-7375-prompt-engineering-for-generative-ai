"""One-command demo: python3 -m source_check.demo [case]"""
import json
import sys
from pathlib import Path

from source_check.checker import check_answer, load_policies

DATA = Path(__file__).resolve().parents[1] / "data"


def main(name="air_canada_shape"):
    case = json.loads((DATA / "cases.json").read_text())[name]
    d = check_answer(case["claims"], load_policies(DATA / "policies.json"))
    print(f"answer : {case['answer']}")
    print(f"verdict: {d.verdict}")
    for r in d.reasons:
        print(f"reason : {r}")
    for line in d.policy_lines:
        print(f"policy : {line}")


if __name__ == "__main__":
    main(*sys.argv[1:])
